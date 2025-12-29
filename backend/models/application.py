# application.py - Enhanced application models
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

# ============= Enums =============

class ApplicationStatus(str, Enum):
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    UNDER_REVIEW = "Under Review"
    MISSING_DOCUMENTS = "Missing Documents"
    CONDITIONAL_OFFER = "Conditional Offer"
    FINAL_OFFER = "Final Offer"
    REJECTED = "Rejected"

# ============= Application Models =============

class ApplicationCreate(BaseModel):
    user_id: int
    university_id: int
    major_id: int
    notes: Optional[str] = Field(None, max_length=1000)

class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None
    admin_notes: Optional[str] = None

class Application(BaseModel):
    id: int
    user_id: int
    university_id: int
    major_id: int
    status: str
    application_date: datetime
    last_updated: datetime
    notes: Optional[str] = None
    admin_notes: Optional[str] = None
    
    class Config:
        from_attributes = True

# ============= Application Documents =============

class ApplicationDocumentCreate(BaseModel):
    application_id: int
    document_type: str
    file_name: str

class ApplicationDocument(BaseModel):
    id: int
    application_id: int
    document_type: str
    file_path: str
    file_name: str
    uploaded_at: datetime
    is_verified: bool
    
    class Config:
        from_attributes = True

# ============= Application Detail Response =============

class ApplicationDetail(Application):
    university_name: str
    university_country: str
    major_name: str
    documents: List[ApplicationDocument] = []
    timeline: List[dict] = []
    required_documents: List[str] = []
    missing_documents: List[str] = []

class ApplicationListItem(BaseModel):
    id: int
    university_name: str
    major_name: str
    status: str
    application_date: datetime
    last_updated: datetime
    completion_percentage: int

class ApplicationsResponse(BaseModel):
    applications: List[ApplicationListItem]
    total_count: int
    by_status: dict

# ============= Application Submission =============

class SubmitApplicationRequest(BaseModel):
    application_id: int
    confirm_documents: bool = Field(..., description="Confirm all required documents are uploaded")

class ApplicationSubmissionResponse(BaseModel):
    application_id: int
    status: str
    message: str
    next_steps: List[str]
    estimated_review_time: str

# ============= Admin Application Management =============

class AdminApplicationUpdate(BaseModel):
    status: ApplicationStatus
    admin_notes: Optional[str] = None
    send_notification: bool = True

class AdminApplicationFilter(BaseModel):
    status: Optional[ApplicationStatus] = None
    university_id: Optional[int] = None
    date_from: Optional[str] = None  # YYYY-MM-DD
    date_to: Optional[str] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

class ApplicationStats(BaseModel):
    total_applications: int
    by_status: dict
    by_university: dict
    avg_processing_time_days: float
    pending_review_count: int

# ============= Document Requirements =============

class DocumentRequirement(BaseModel):
    document_type: str
    description: str
    is_mandatory: bool
    accepted_formats: List[str]
    max_size_mb: int

class ApplicationRequirements(BaseModel):
    university_id: int
    major_id: int
    required_documents: List[DocumentRequirement]
    additional_requirements: List[str]
    deadlines: dict
