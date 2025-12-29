# routers/university.py - University search, recommendation, and comparison
from fastapi import APIRouter, HTTPException, Depends, Query
from models.university import (
    UniversitySearchFilter, UniversitySearchResponse, UniversityBasic,
    UniversityRecommendationRequest, UniversityRecommendation, RecommendationResponse,
    ComparisonRequest
)
from services import ai_service
from middleware.auth_middleware import get_current_active_user, get_optional_user
from sqlite import get_db
import sqlite3
from typing import List, Optional

router = APIRouter(prefix="/universities", tags=["Universities"])

@router.get("/search", response_model=UniversitySearchResponse)
def search_universities(
    country: Optional[str] = Query(None),
    major: Optional[str] = Query(None),
    min_tuition: Optional[int] = Query(None),
    max_tuition: Optional[int] = Query(None),
    min_gpa: Optional[float] = Query(None),
    max_gpa: Optional[float] = Query(None),
    language: Optional[str] = Query(None),
    scholarship_track: Optional[bool] = Query(None),
    search_query: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: sqlite3.Connection = Depends(get_db),
    current_user: Optional[dict] = Depends(get_optional_user)
):
    """Advanced university search with filters"""
    cursor = db.cursor()
    
    # Build query
    query = "SELECT DISTINCT u.id, u.name, u.country, u.city, u.tuition_fee, u.min_gpa, u.scholarship_available, u.ranking FROM universities u"
    where_clauses = ["u.is_active = 1"]
    params = []
    
    if major:
        query += " JOIN university_majors um ON u.id = um.university_id JOIN majors m ON um.major_id = m.id"
        where_clauses.append("m.name LIKE ?")
        params.append(f"%{major}%")
    
    if country:
        where_clauses.append("u.country = ?")
        params.append(country)
    
    if min_tuition is not None:
        where_clauses.append("u.tuition_fee >= ?")
        params.append(min_tuition)
    
    if max_tuition is not None:
        where_clauses.append("u.tuition_fee <= ?")
        params.append(max_tuition)
    
    if min_gpa is not None:
        where_clauses.append("u.min_gpa >= ?")
        params.append(min_gpa)
    
    if max_gpa is not None:
        where_clauses.append("u.min_gpa <= ?")
        params.append(max_gpa)
    
    if language:
        where_clauses.append("u.language LIKE ?")
        params.append(f"%{language}%")
    
    if scholarship_track is True:
        where_clauses.append("u.scholarship_available = 1")
    
    if search_query:
        where_clauses.append("(u.name LIKE ? OR u.country LIKE ? OR u.city LIKE ?)")
        params.extend([f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"])
    
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    # Count total
    count_query = query.replace(
        "SELECT DISTINCT u.id, u.name, u.country, u.city, u.tuition_fee, u.min_gpa, u.scholarship_available, u.ranking",
        "SELECT COUNT(DISTINCT u.id)"
    )
    cursor.execute(count_query, params)
    total_count = cursor.fetchone()[0]
    
    # Add pagination
    offset = (page - 1) * page_size
    query += " ORDER BY u.ranking ASC, u.name ASC LIMIT ? OFFSET ?"
    params.extend([page_size, offset])
    
    cursor.execute(query, params)
    universities = []
    
    for row in cursor.fetchall():
        universities.append(UniversityBasic(
            id=row[0],
            name=row[1],
            country=row[2],
            city=row[3],
            tuition_fee=row[4],
            min_gpa=row[5],
            scholarship_available=bool(row[6]),
            ranking=row[7]
        ))
    
    total_pages = (total_count + page_size - 1) // page_size
    
    return UniversitySearchResponse(
        universities=universities,
        total_count=total_count,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        filters_applied={
            "country": country,
            "major": major,
            "scholarship_track": scholarship_track
        }
    )

@router.get("/{university_id}")
def get_university_detail(
    university_id: int,
    db: sqlite3.Connection = Depends(get_db)
):
    """Get detailed university information"""
    cursor = db.cursor()
    
    cursor.execute(
        """SELECT id, name, country, city, tuition_fee, min_gpa, language, scholarship_available,
                  overview, duration, accommodation_info, website, ranking, acceptance_rate
           FROM universities WHERE id = ? AND is_active = 1""",
        (university_id,)
    )
    uni = cursor.fetchone()
    
    if not uni:
        raise HTTPException(status_code=404, detail="University not found")
    
    # Get media
    cursor.execute(
        "SELECT id, media_type, media_url, caption FROM university_media WHERE university_id = ? ORDER BY display_order",
        (university_id,)
    )
    media = [{"id": r[0], "media_type": r[1], "media_url": r[2], "caption": r[3]} for r in cursor.fetchall()]
    
    # Get majors
    cursor.execute(
        """SELECT m.id, m.name, m.category, m.difficulty, m.career_paths, m.average_cost
           FROM majors m
           JOIN university_majors um ON m.id = um.major_id
           WHERE um.university_id = ?""",
        (university_id,)
    )
    majors = [{"id": r[0], "name": r[1], "category": r[2], "difficulty": r[3], 
               "career_paths": r[4], "average_cost": r[5]} for r in cursor.fetchall()]
    
    return {
        "id": uni[0],
        "name": uni[1],
        "country": uni[2],
        "city": uni[3],
        "tuition_fee": uni[4],
        "min_gpa": uni[5],
        "language": uni[6],
        "scholarship_available": bool(uni[7]),
        "overview": uni[8],
        "duration": uni[9],
        "accommodation_info": uni[10],
        "website": uni[11],
        "ranking": uni[12],
        "acceptance_rate": uni[13],
        "media": media,
        "majors": majors
    }

@router.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(
    request: UniversityRecommendationRequest,
    current_user: dict = Depends(get_current_active_user),
    db: sqlite3.Connection = Depends(get_db)
):
    """Get AI-based university recommendations"""
    user_id = current_user["user_id"]
    
    # Get assessment results
    cursor = db.cursor()
    cursor.execute(
        """SELECT personality_type, scores, strengths
           FROM assessment_results
           WHERE user_id = ?
           ORDER BY completed_at DESC
           LIMIT 1""",
        (user_id,)
    )
    assessment = cursor.fetchone()
    
    assessment_results = {}
    if assessment:
        import json
        assessment_results = {
            "personality_type": assessment[0],
            "scores": json.loads(assessment[1]) if assessment[1] else {},
            "strengths": json.loads(assessment[2]) if assessment[2] else []
        }
    
    # Get recommendations
    recommendations = ai_service.recommend_universities(
        user_id, db, request.preferred_major or "", assessment_results, request.max_results
    )
    
    return RecommendationResponse(
        recommendations=recommendations,
        criteria_used={
            "gpa": True,
            "budget": True,
            "scholarship": True,
            "assessment": bool(assessment),
            "country_preference": True
        }
    )

@router.post("/compare")
def compare_universities(
    request: ComparisonRequest,
    db: sqlite3.Connection = Depends(get_db)
):
    """Compare 2-3 universities"""
    if len(request.university_ids) < 2 or len(request.university_ids) > 3:
        raise HTTPException(status_code=400, detail="Please select 2 or 3 universities to compare")
    
    cursor = db.cursor()
    universities = []
    
    for uni_id in request.university_ids:
        cursor.execute(
            """SELECT id, name, country, tuition_fee, min_gpa, scholarship_available,
                      ranking, acceptance_rate, duration
               FROM universities WHERE id = ?""",
            (uni_id,)
        )
        uni = cursor.fetchone()
        if uni:
            universities.append({
                "id": uni[0],
                "name": uni[1],
                "country": uni[2],
                "tuition_fee": uni[3],
                "min_gpa": uni[4],
                "scholarship_available": bool(uni[5]),
                "ranking": uni[6],
                "acceptance_rate": uni[7],
                "duration": uni[8]
            })
    
    # Create comparison table
    comparison_table = {
        "Tuition Fee": [u["tuition_fee"] for u in universities],
        "Min GPA": [u["min_gpa"] for u in universities],
        "Scholarship": [u["scholarship_available"] for u in universities],
        "Ranking": [u["ranking"] for u in universities],
        "Acceptance Rate": [u["acceptance_rate"] for u in universities]
    }
    
    return {
        "universities": universities,
        "comparison_table": comparison_table
    }
