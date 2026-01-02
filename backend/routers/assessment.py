
from fastapi import APIRouter, HTTPException, Depends
from models.assessment import SubmitAssessment, AssessmentResultResponse, RecommendationsResponse
from services import ai_service
from middleware.auth_middleware import get_current_active_user
from sqlite import get_db
import sqlite3
import json
from datetime import datetime
import logging
from pydantic import BaseModel
from typing import List 

router = APIRouter(prefix="/assessment", tags=["Assessment"])

class AssessmentRequest(BaseModel):
    test_type: str
    answers: List[dict]  # Flexible format for answers

@router.post("/evaluate", response_model=dict)
async def evaluate_assessment(
    assessment: AssessmentRequest,
    current_user: dict = Depends(get_current_active_user),
    db: sqlite3.Connection = Depends(get_db)
):
    """Evaluate assessment and return major recommendations"""
    user_id = current_user["user_id"]
    

    results = ai_service.evaluate_assessment(
        assessment.test_type,
        assessment.answers
    )
    
    logging.info(f"results :{results}")
    # Store assessment results
    cursor = db.cursor()
    cursor.execute(
        """INSERT INTO assessment_results 
           (user_id, test_type, personality_type, scores, strengths, weaknesses)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            user_id,
            assessment.test_type,
            results.get("personality_type", ""),
            json.dumps(results.get("scores", {})),
            json.dumps(results.get("strengths", [])),
            json.dumps(results.get("weaknesses", [])),
            
        )
    )
    result_id = cursor.lastrowid
    
    # Get major recommendations
    recommendations = ai_service.recommend_majors(user_id, db, results)

    logging.info(f'recommanded majors by AI:{recommendations}')
    
    # Store major recommendations
    for rec in recommendations:
        cursor.execute(
            """INSERT INTO major_recommendations
               (user_id, major_name, match_score, explanation,
                difficulty_level, career_paths, estimated_cost, study_duration, roadmap)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user_id,
                #result_id,
                rec.get("major_name", ""),
                rec.get("match_score", 0.0),
                rec.get("explanation", ""),
                rec.get("difficulty_level", ""),
                rec.get("career_paths", ""),
                rec.get("estimated_cost", 0),
                rec.get("study_duration", ""),
                json.dumps(rec.get("roadmap", []))
            )
        )
    
    db.commit()
    
    return {
        "success": True,
        "result_id": result_id,
        "assessment_summary": results,
        "recommendations": recommendations,
        "total_count": len(recommendations)
    }

@router.get("/results/{result_id}")
async def get_assessment_results(
    result_id: int,
    current_user: dict = Depends(get_current_active_user),
    db: sqlite3.Connection = Depends(get_db)
):
    """Get specific assessment results"""
    user_id = current_user["user_id"]
    cursor = db.cursor()
    
    # Get assessment result
    cursor.execute(
        """SELECT id, personality_type, scores, strengths, weaknesses, completed_at
           FROM assessment_results
           WHERE id = ? AND user_id = ?""",
        (result_id, user_id)
    )
    result = cursor.fetchone()
    print(f"result:{result}")
    if not result:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get recommendations
    cursor.execute(
        """SELECT major_name, match_score, explanation, difficulty_level, career_paths,
                  estimated_cost, study_duration, roadmap
           FROM major_recommendations
           WHERE user_id = ?
           ORDER BY match_score DESC""",
        (result_id,)
    )
    recommendations = []
    for row in cursor.fetchall():
        recommendations.append({
            "major_name": row[0],
            "match_score": row[1],
            "explanation": row[2],
            "difficulty_level": row[3],
            "career_paths": row[4],
            "estimated_cost": row[5],
            "study_duration": row[6],
            "roadmap": json.loads(row[7]) if row[7] else []
        })
    print(f"recommandadtion list:{recommendations}")
    return {
        "result_id": result[0],
        "personality_type": result[1],
        "scores": json.loads(result[2]) if result[2] else {},
        "strengths": json.loads(result[3]) if result[3] else [],
        "weaknesses": json.loads(result[4]) if result[4] else [],
       # "insights": result[5],
        "completed_at": result[6],
        "recommendations": recommendations
    }

@router.get("/my-results")
async def get_my_assessments(
    current_user: dict = Depends(get_current_active_user),
    db: sqlite3.Connection = Depends(get_db)
):
    """Get all assessment results for current user"""
    user_id = current_user["user_id"]
    cursor = db.cursor()
    
    cursor.execute(
        """SELECT id, test_type, personality_type, completed_at
           FROM assessment_results
           WHERE user_id = ?
           ORDER BY completed_at DESC""",
        (user_id,)
    )
    
    results = []
    for row in cursor.fetchall():
        results.append({
            "id": row[0],
            "test_type": row[1],
            "personality_type": row[2],
            "completed_at": row[3]
        })
    
    return {"results": results, "total_count": len(results)}
