# university.py - Enhanced university models
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import datetime

# ============= Major Models =============

class MajorBase(BaseModel):
    name: str
    category: Optional[str] = None
    difficulty: str = Field(..., pattern='^(Easy|Medium|Hard)$')
    career_paths: str
    average_cost: int
    description: Optional[str] = None
    required_skills: Optional[str] = None

class MajorCreate(MajorBase):
    pass

class Major(MajorBase):
    id: int
    
    class Config:
        from_attributes = True

# ============= University Models =============

class UniversityBase(BaseModel):
    name: str
    country: str
    city: Optional[str] = None
    tuition_fee: int = Field(..., ge=0)
    min_gpa: float = Field(..., ge=0.0, le=4.0)
    language: str
    scholarship_available: bool = False
    overview: Optional[str] = None
    duration: Optional[str] = None
    accommodation_info: Optional[str] = None
    website: Optional[str] = None
    ranking: Optional[int] = None
    acceptance_rate: Optional[float] = Field(None, ge=0.0, le=1.0)

class UniversityCreate(UniversityBase):
    success_weight: float = 1.0

class UniversityUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    tuition_fee: Optional[int] = Field(None, ge=0)
    min_gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    language: Optional[str] = None
    scholarship_available: Optional[bool] = None
    overview: Optional[str] = None
    duration: Optional[str] = None
    accommodation_info: Optional[str] = None
    website: Optional[str] = None
    ranking: Optional[int] = None
    acceptance_rate: Optional[float] = Field(None, ge=0.0, le=1.0)
    success_weight: Optional[float] = None
    is_active: Optional[bool] = None

class University(UniversityBase):
    id: int
    success_weight: float
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============= University Media =============

class UniversityMediaCreate(BaseModel):
    university_id: int
    media_type: str = Field(..., pattern='^(image|video)$')
    media_url: str
    caption: Optional[str] = None
    display_order: int = 0

class UniversityMedia(BaseModel):
    id: int
    university_id: int
    media_type: str
    media_url: str
    caption: Optional[str] = None
    display_order: int
    
    class Config:
        from_attributes = True

# ============= University-Major Relationship =============

class UniversityMajorCreate(BaseModel):
    university_id: int
    major_id: int
    tuition_fee: Optional[int] = None
    duration_years: Optional[int] = None
    special_requirements: Optional[str] = None

class UniversityMajor(BaseModel):
    id: int
    university_id: int
    major_id: int
    tuition_fee: Optional[int] = None
    duration_years: Optional[int] = None
    special_requirements: Optional[str] = None
    
    class Config:
        from_attributes = True

# ============= University Detail Response =============

class UniversityDetail(University):
    media: List[UniversityMedia] = []
    majors: List[Major] = []
    similar_universities: List['UniversityBasic'] = []

class UniversityBasic(BaseModel):
    id: int
    name: str
    country: str
    city: Optional[str] = None
    tuition_fee: int
    min_gpa: float
    scholarship_available: bool
    ranking: Optional[int] = None
    
    class Config:
        from_attributes = True

# ============= Search and Filter =============

class UniversitySearchFilter(BaseModel):
    country: Optional[List[str]] = None
    major: Optional[str] = None
    min_tuition: Optional[int] = Field(None, ge=0)
    max_tuition: Optional[int] = Field(None, ge=0)
    min_gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    max_gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    language: Optional[List[str]] = None
    scholarship_track: Optional[bool] = None  # True = scholarship only, False = all, None = all
    search_query: Optional[str] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

class UniversitySearchResponse(BaseModel):
    universities: List[UniversityBasic]
    total_count: int
    page: int
    page_size: int
    total_pages: int
    filters_applied: dict

# ============= AI Recommendation =============

class UniversityRecommendationRequest(BaseModel):
    user_id: int
    preferred_major: Optional[str] = None
    max_results: int = Field(10, ge=1, le=20)

class UniversityRecommendation(UniversityBasic):
    recommendation_score: float = Field(..., ge=0.0, le=1.0)
    reasons: List[str]
    pros: List[str]
    cons: List[str]

class RecommendationResponse(BaseModel):
    recommendations: List[UniversityRecommendation]
    criteria_used: dict

# ============= Comparison =============

class ComparisonRequest(BaseModel):
    university_ids: List[int] = Field(..., min_length=2, max_length=3)

class UniversityComparison(BaseModel):
    universities: List[UniversityDetail]
    comparison_table: dict
    winner: Optional[dict] = None  # Best overall based on multiple factors

# ============= Admin Management =============

class UniversityStats(BaseModel):
    total_universities: int
    by_country: dict
    by_scholarship: dict
    avg_tuition: float
    total_applications: int

# Enable forward references
UniversityDetail.model_rebuild()
