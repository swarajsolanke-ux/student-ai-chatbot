# partner.py - Partner services models (Cars, Banks, Telecom, Travel)
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime, date
from enum import Enum

# ============= Enums =============

class PartnerCategory(str, Enum):
    CAR = "car"
    BANK = "bank"
    TELECOM = "telecom"
    TRAVEL = "travel"

class LeadStatus(str, Enum):
    NEW = "New"
    CONTACTED = "Contacted"
    QUALIFIED = "Qualified"
    CONVERTED = "Converted"
    LOST = "Lost"

# ============= Partner Models =============

class PartnerBase(BaseModel):
    name: str
    category: PartnerCategory
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    contact_email: Optional[EmailStr] = None

class PartnerCreate(PartnerBase):
    pass

class PartnerUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class Partner(PartnerBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

# ============= Service Offers =============

class ServiceOfferBase(BaseModel):
    partner_id: int
    title: str
    description: str
    discount_percentage: Optional[float] = Field(None, ge=0, le=100)
    terms: Optional[str] = None
    image_url: Optional[str] = None
    valid_until: Optional[str] = None  # YYYY-MM-DD

class ServiceOfferCreate(ServiceOfferBase):
    pass

class ServiceOfferUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    discount_percentage: Optional[float] = Field(None, ge=0, le=100)
    terms: Optional[str] = None
    image_url: Optional[str] = None
    valid_until: Optional[str] = None
    is_active: Optional[bool] = None

class ServiceOffer(ServiceOfferBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

# ============= Service Offer Detail =============

class ServiceOfferDetail(ServiceOffer):
    partner_name: str
    partner_logo: Optional[str] = None
    partner_category: str
    days_until_expiry: Optional[int] = None
    is_expired: bool

# ============= Lead Generation =============

class ServiceLeadCreate(BaseModel):
    user_id: int
    partner_id: int
    offer_id: int
    student_name: str
    student_email: EmailStr
    student_phone: str
    message: Optional[str] = Field(None, max_length=500)

class ServiceLeadUpdate(BaseModel):
    status: LeadStatus
    notes: Optional[str] = None

class ServiceLead(BaseModel):
    id: int
    user_id: int
    partner_id: int
    offer_id: int
    student_name: str
    student_email: str
    student_phone: str
    message: Optional[str] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ServiceLeadDetail(ServiceLead):
    partner_name: str
    offer_title: str
    partner_category: str

# ============= Service Categories Response =============

class ServiceCategoryOffers(BaseModel):
    category: str
    category_name: str
    partners: List[Partner]
    offers: List[ServiceOfferDetail]
    total_offers: int

class AllServicesResponse(BaseModel):
    cars: ServiceCategoryOffers
    banks: ServiceCategoryOffers
    telecom: ServiceCategoryOffers
    travel: ServiceCategoryOffers

# ============= Partner-specific Models =============

class CarOfferDetails(ServiceOfferDetail):
    car_make: Optional[str] = None
    car_model: Optional[str] = None
    price_range: Optional[str] = None

class BankOfferDetails(ServiceOfferDetail):
    account_type: Optional[str] = None
    minimum_balance: Optional[int] = None
    benefits: Optional[List[str]] = None

class TelecomOfferDetails(ServiceOfferDetail):
    data_amount: Optional[str] = None
    call_minutes: Optional[str] = None
    monthly_price: Optional[float] = None

class TravelOfferDetails(ServiceOfferDetail):
    destination: Optional[str] = None
    service_type: Optional[str] = None  # flight, visa, insurance
    price: Optional[float] = None

# ============= Partner Portal (Admin for Partners) =============

class PartnerLogin(BaseModel):
    email: EmailStr
    password: str

class PartnerDashboardStats(BaseModel):
    total_leads: int
    new_leads: int
    converted_leads: int
    conversion_rate: float
    active_offers: int
    leads_by_month: dict

class PartnerLeadsList(BaseModel):
    leads: List[ServiceLeadDetail]
    total_count: int
    by_status: dict
    page: int
    page_size: int

# ============= Student View =============

class MyServiceRequests(BaseModel):
    requests: List[ServiceLeadDetail]
    total_count: int
    by_category: dict
    by_status: dict
