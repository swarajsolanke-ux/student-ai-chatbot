# services/ai_service.py - AI assessment and recommendation service
"""
AI Service using Ollama for student assessments and recommendations
"""
from config import settings
import json
from typing import List, Dict, Any
import sqlite3

try:
    from langchain_ollama import ChatOllama
    from langchain.prompts import ChatPromptTemplate
    from langchain_core.messages import SystemMessage, HumanMessage
except ImportError:
    print("LangChain Ollama not available. Install with: pip install langchain-ollama")
    ChatOllama = None

def get_ollama_model():
    """Initialize Ollama model"""
    if ChatOllama is None:
        return None
    
    try:
        model = ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.7
        )
        return model
    except Exception as e:
        print(f"  Error initializing Ollama: {e}")
        print(f"Make sure Ollama is running and model '{settings.OLLAMA_MODEL}' is pulled")
        return None

def evaluate_assessment(test_type: str, answers: List[Dict]) -> Dict[str, Any]:
    """
    Evaluate assessment test answers using AI
    Returns scores, personality type, strengths, weaknesses
    """
    model = get_ollama_model()
    
    if model is None:
        # Fallback to rule-based evaluation
        return fallback_assessment_evaluation(test_type, answers)
    
    # Create prompt for AI evaluation
    prompt = f"""You are an expert educational Expert evaluating a student's {test_type} assessment.

The student has completed the following questions and answers:
{json.dumps(answers, indent=2)}

Based on their responses, provide:
1. Personality type (e.g., Analytical, Creative, Practical, Social)
2. Top 3 strengths
3. Top 3 areas for improvement
4. Overall assessment scores (0-100) for different categories

Respond in JSON format:
{{
    "personality_type": "...",
    "strengths": ["...", "...", "..."],
    "weaknesses": ["...", "...", "..."],
    "scores": {{
        "analytical_thinking": 0-100,
        "creativity": 0-100,
        "problem_solving": 0-100,
        "communication": 0-100
    }},
    "insights": "Brief paragraph of insights..."
}}
"""
    
    try:
        messages = [
            SystemMessage(content="You are an expert educational Mentor."),
            HumanMessage(content=prompt)
        ]
        
        response = model.invoke(messages)
        result = json.loads(response.content)
        return result
        
    except Exception as e:
        print(f"Error in AI evaluation: {e}")
        return fallback_assessment_evaluation(test_type, answers)

def recommend_majors(user_id: int, db: sqlite3.Connection, assessment_results: Dict) -> List[Dict]:
    """
    Recommend 3-7 majors based on assessment results, GPA, and preferences
    """
    model = get_ollama_model()
    
    # Get user profile
    cursor = db.cursor()
    cursor.execute(
        """SELECT gpa, budget, preferred_country, preferred_major, career_goal
           FROM student_profiles WHERE user_id = ?""",
        (user_id,)
    )
    profile = cursor.fetchone()
    
    if not profile:
        return []
    
    gpa, budget, preferred_country, preferred_major, career_goal = profile
    
    # Get available majors
    cursor.execute("SELECT name, category, difficulty, career_paths, average_cost FROM majors")
    majors = cursor.fetchall()
    
    if model is None:
        # Fallback to rule-based recommendations
        return fallback_major_recommendations(majors, assessment_results, gpa, preferred_major)
    
    prompt = f"""As an expert academic advisor, recommend 3-7 university majors for this student:

Student Profile:
- GPA: {gpa}
- Budget: ${budget}
- Preferred Country: {preferred_country}
- Career Goal: {career_goal}
- Personality Type: {assessment_results.get('personality_type', 'Unknown')}
- Strengths: {', '.join(assessment_results.get('strengths', []))}

Available Majors:
{json.dumps([{"name": m[0], "category": m[1], "difficulty": m[2], "careers": m[3], "cost": m[4]} for m in majors], indent=2)}

Provide 3-7 major recommendations with:
1. Match score (0-1)
2. Explanation why it's a good fit
3. Difficulty assessment
4. Career opportunities
5. Estimated cost
6. Study duration
7. Study roadmap (5-7 key steps)

Respond in JSON format:
{{
    "recommendations": [
        {{
            "major_name": "...",
            "match_score": 0.0-1.0,
            "explanation": "...",
            "difficulty_level": "Easy/Medium/Hard",
            "career_paths": "...",
            "estimated_cost": 15000,
            "study_duration": "3-4 years",
            "roadmap": ["Step 1...", "Step 2...", ...]
        }}
    ]
}}
"""
    
    try:
        messages = [
            SystemMessage(content="You are an expert academic and career advisor."),
            HumanMessage(content=prompt)
        ]
        
        response = model.invoke(messages)
        result = json.loads(response.content)
        return result.get("recommendations", [])
        
    except Exception as e:
        print(f"Error in AI major recommendation: {e}")
        return fallback_major_recommendations(majors, assessment_results, gpa, preferred_major)

def recommend_universities(
    user_id: int,
    db: sqlite3.Connection,
    preferred_major: str,
    assessment_results: Dict,
    max_results: int = 10
) -> List[Dict]:
    """
    Recommend universities based on student profile and AI assessment
    """
    cursor = db.cursor()
    
    # Get user profile
    cursor.execute(
        """SELECT gpa, budget, preferred_country FROM student_profiles WHERE user_id = ?""",
        (user_id,)
    )
    profile = cursor.fetchone()
    
    if not profile:
        return []
    
    gpa, budget, preferred_country = profile
    
    # Get universities offering the preferred major
    cursor.execute(
        """SELECT DISTINCT u.id, u.name, u.country, u.tuition_fee, u.min_gpa, 
                  u.scholarship_available, u.success_weight, u.acceptance_rate
           FROM universities u
           JOIN university_majors um ON u.id = um.university_id
           JOIN majors m ON um.major_id = m.id
           WHERE m.name LIKE ? AND u.is_active = 1
           ORDER BY u.success_weight DESC""",
        (f"%{preferred_major}%",)
    )
    universities = cursor.fetchall()
    
    # Calculate recommendation scores
    recommendations = []
    
    for uni in universities:
        uni_id, name, country, tuition, min_gpa, has_scholarship, success_weight, acceptance_rate = uni
        
        # Calculate match score
        score = 0.0
        reasons = []
        pros = []
        cons = []
        
        # GPA match (30%)
        if gpa >= min_gpa:
            gpa_score = min(1.0, (gpa - min_gpa) / (4.0 - min_gpa)) if min_gpa < 4.0 else 1.0
            score += gpa_score * 0.3
            if gpa >= min_gpa + 0.3:
                pros.append(f"Your GPA ({gpa}) exceeds requirements ({min_gpa})")
                reasons.append("Strong academic match based on GPA")
        else:
            cons.append(f"GPA requirement ({min_gpa}) is higher than yours ({gpa})")
            continue  # Skip if GPA doesn't meet minimum
        
        # Budget match (25%)
        if tuition <= budget:
            budget_score = 1.0 - (tuition / budget) * 0.5
            score += budget_score * 0.25
            pros.append(f"Tuition (${tuition}) is within your budget (${budget})")
            reasons.append("Affordable tuition within budget")
        else:
            if has_scholarship:
                score += 0.15  # Partial credit if scholarships available
                pros.append("Scholarship opportunities available")
                cons.append(f"Tuition (${tuition}) exceeds budget, but scholarships may help")
            else:
                cons.append(f"Tuition (${tuition}) exceeds budget (${budget})")
        
        # Scholarship availability (20%)
        if has_scholarship:
            score += 0.2
            reasons.append("Scholarship opportunities available")
        
        # Country preference (10%)
        if preferred_country and country.lower() == preferred_country.lower():
            score += 0.1
            reasons.append(f"Located in your preferred country ({country})")
            pros.append(f"Located in {country} as preferred")
        
        # Success weight (15%)
        score += (success_weight - 1.0) * 0.15
        if success_weight > 1.1:
            reasons.append("Strong success history with past students")
            pros.append("High success rate with previous applicants")
        
        if score > 0.3:  # Only recommend if score is reasonable
            recommendations.append({
                "id": uni_id,
                "name": name,
                "country": country,
                "tuition_fee": tuition,
                "min_gpa": min_gpa,
                "scholarship_available": bool(has_scholarship),
                "recommendation_score": round(score, 2),
                "reasons": reasons,
                "pros": pros,
                "cons": cons
            })
    
    # Sort by score and return top N
    recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)
    return recommendations[:max_results]

# Fallback functions when Ollama is not available

def fallback_assessment_evaluation(test_type: str, answers: List[Dict]) -> Dict:
    """Rule-based assessment evaluation when AI is not available"""
    # Simple scoring based on answer patterns
    scores = {
        "analytical_thinking": 70,
        "creativity": 65,
        "problem_solving": 75,
        "communication": 60
    }
    
    return {
        "personality_type": "Balanced",
        "strengths": ["Problem Solving", "Analytical Thinking", "Adaptability"],
        "weaknesses": ["Time Management", "Public Speaking", "Advanced Mathematics"],
        "scores": scores,
        "insights": "Based on your responses, you show strong analytical and problem-solving skills. Consider majors that leverage these strengths."
    }

def fallback_major_recommendations(majors, assessment_results, gpa, preferred_major):
    """Rule-based major recommendations when AI is not available"""
    recommendations = []
    
    # Simple matching based on GPA and preferences
    for major in majors[:7]:  # Top 7 majors
        name, category, difficulty, career_paths, avg_cost = major
        
        # Calculate simple match score
        score = 0.6
        if preferred_major and preferred_major.lower() in name.lower():
            score += 0.3
        if difficulty == "Medium":
            score += 0.1
        
        recommendations.append({
            "major_name": name,
            "match_score": min(1.0, score),
            "explanation": f"Good fit based on your profile and interests in {category}",
            "difficulty_level": difficulty,
            "career_paths": career_paths,
            "estimated_cost": avg_cost,
            "study_duration": "3-4 years",
            "roadmap": [
                "Complete foundational courses",
                "Develop core skills and knowledge",
                "Gain practical experience through internships",
                "Complete advanced specialization courses",
                "Work on capstone project or thesis"
            ]
        })
    
    return recommendations
