
from pydantic import BaseModel, Field,ConfigDict
from typing import List, Optional, Dict,Any
from datetime import datetime


class Question(BaseModel):
    id: int
    text: str
    options: List[str]
    category: Optional[str] = None

class AssessmentTest(BaseModel):
    id: int
    test_type: str  
    questions: str  # JSON string of questions
    
    class Config:
        from_attributes = True

class AssessmentTestResponse(BaseModel):
    test_type: str
    questions: List[Question]
    total_questions: int



class Answer(BaseModel):
    question_id: int
    selected_option: int  # Index of selected option

class SubmitAssessment(BaseModel):
    user_id: int
    test_type: str
    answers: List[Answer]

# ============= Assessment Results =============

class AssessmentScore(BaseModel):
    category: str
    score: float
    percentage: float

class AssessmentResult(BaseModel):
    id: int
    user_id: int
    test_type: str
    answers: str  # JSON
    scores: str  # JSON
    personality_type: Optional[str] = None
    strengths: Optional[str] = None  # JSON
    weaknesses: Optional[str] = None  # JSON
    completed_at: datetime
    
    class Config:
        from_attributes = True

class AssessmentResultResponse(BaseModel):
    test_type: str
    personality_type: Optional[str] = None
    scores: List[AssessmentScore]
    strengths: List[str]
    weaknesses: List[str]
    completed_at: datetime
    insights: str

# ============= Major Recommendations =============

class MajorRecommendationCreate(BaseModel):
    user_id: int
    major_name: str
    match_score: float
    explanation: str
    difficulty_level: str
    career_paths: str
    estimated_cost: int
    study_duration: str
    roadmap: str

class MajorRecommendation(BaseModel):
    id: int
    user_id: int
    major_name: str
    match_score: float = Field(..., ge=0.0, le=1.0)
    explanation: str
    difficulty_level: str
    career_paths: str  # Comma-separated
    estimated_cost: int
    study_duration: str
    roadmap: str  # JSON or markdown
    created_at: datetime
    
    class Config:
        from_attributes = True

class MajorRecommendationResponse(BaseModel):
    major_name: str
    match_score: float
    match_percentage: int
    explanation: str
    difficulty_level: str
    career_paths: List[str]
    estimated_cost: int
    cost_formatted: str
    study_duration: str
    roadmap_steps: List[str]
    pros: List[str]
    cons: List[str]

class RecommendationsResponse(BaseModel):
    recommendations: List[MajorRecommendationResponse]
    total_count: int
    assessment_summary: Dict[str, Any]

# ============= Study Roadmap =============

class RoadmapStep(BaseModel):
    step: int
    title: str
    description: str
    duration: str
    resources: List[str]

class StudyRoadmap(BaseModel):
    major_name: str
    total_duration: str
    steps: List[RoadmapStep]
    milestones: List[str]
    recommended_certifications: List[str]

# ============= Complete Assessment Flow =============

class StartAssessmentResponse(BaseModel):
    session_id: str
    message: str
    first_test: AssessmentTestResponse

class AssessmentProgress(BaseModel):
    user_id: int
    completed_tests: List[str]
    pending_tests: List[str]
    completion_percentage: int
    can_get_recommendations: bool
