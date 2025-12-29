# scholarship.py - Enhanced scholarship models
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
from enum import Enum

# ============= Enums =============

class ScholarshipStatus(str, Enum):
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    UNDER_REVIEW = "Under Review"
    APPROVED = "Approved"
    REJECTED = "Rejected"

# ============= Scholarship Models =============

class ScholarshipBase(BaseModel):
    name: str
    country: str
    provider: str
    min_gpa: float = Field(..., ge=0.0, le=4.0)
    max_age: Optional[int] = None
    nationality_requirement: Optional[str] = None
    coverage: str
    amount: int = Field(..., ge=0)
    deadline: str  # YYYY-MM-DD format
    description: Optional[str] = None
    required_documents: Optional[str] = None
    website: Optional[str] = None

class ScholarshipCreate(ScholarshipBase):
    pass

class ScholarshipUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    provider: Optional[str] = None
    min_gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    max_age: Optional[int] = None
    nationality_requirement: Optional[str] = None
    coverage: Optional[str] = None
    amount: Optional[int] = Field(None, ge=0)
    deadline: Optional[str] = None
    description: Optional[str] = None
    required_documents: Optional[str] = None
    website: Optional[str] = None
    is_active: Optional[bool] = None

class Scholarship(ScholarshipBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

# ============= Scholarship Application =============

class ScholarshipApplicationCreate(BaseModel):
    user_id: int
    scholarship_id: int

class ScholarshipApplicationUpdate(BaseModel):
    status: Optional[ScholarshipStatus] = None

class ScholarshipApplication(BaseModel):
    id: int
    user_id: int
    scholarship_id: int
    status: str
    eligibility_score: Optional[float] = None
    submitted_at: Optional[datetime] = None
    last_updated: datetime
    
    class Config:
        from_attributes = True

# ============= Scholarship Detail Response =============

class ScholarshipDetail(Scholarship):
    days_until_deadline: int
    is_eligible: bool
    eligibility_reasons: List[str]
    application_steps: List[str]

class ScholarshipListItem(BaseModel):
    id: int
    name: str
    country: str
    provider: str
    amount: int
    amount_formatted: str
    deadline: str
    days_until_deadline: int
    is_eligible: bool
    coverage: str
    
    class Config:
        from_attributes = True

# ============= Search and Filter =============

class ScholarshipSearchFilter(BaseModel):
    country: Optional[List[str]] = None
    min_amount: Optional[int] = Field(None, ge=0)
    max_amount: Optional[int] = Field(None, ge=0)
    coverage_type: Optional[str] = None  # full, partial
    nationality: Optional[str] = None
    only_eligible: bool = False
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

class ScholarshipSearchResponse(BaseModel):
    scholarships: List[ScholarshipListItem]
    total_count: int
    page: int
    page_size: int
    total_pages: int
    eligible_count: int

# ============= Eligibility Check =============

class EligibilityCheckRequest(BaseModel):
    user_id: int
    scholarship_id: int

class EligibilityFactor(BaseModel):
    factor: str
    required: str
    actual: str
    meets_requirement: bool

class EligibilityCheckResponse(BaseModel):
    is_eligible: bool
    overall_score: float
    factors: List[EligibilityFactor]
    recommendations: List[str]
    missing_requirements: List[str]

# ============= Application Detail =============

class ScholarshipApplicationDetail(ScholarshipApplication):
    scholarship_name: str
    scholarship_country: str
    scholarship_amount: int
    deadline: str
    days_until_deadline: int
    required_documents: List[str]
    uploaded_documents: List[str]
    missing_documents: List[str]
    timeline: List[dict]

class MyScholarshipApplications(BaseModel):
    applications: List[ScholarshipApplicationDetail]
    total_count: int
    by_status: dict

# ============= Scholarship Stats =============

class ScholarshipStats(BaseModel):
    total_scholarships: int
    by_country: dict
    total_amount_available: int
    avg_amount: int
    upcoming_deadlines: List[dict]
    total_applications: int
    approval_rate: float
