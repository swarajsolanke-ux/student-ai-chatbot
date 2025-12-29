# __init__.py - Models package initialization
from .user import (
    OTPRequest, OTPVerify, UserRegister, UserLogin, SocialAuthRequest,
    TokenResponse, TokenRefresh, User, StudentProfileCreate, StudentProfileUpdate,
    StudentProfile, UserWithProfile, Document, DocumentUpload
)
from .assessment import (
    Question, AssessmentTest, AssessmentTestResponse, Answer, SubmitAssessment,
    AssessmentScore, AssessmentResult, AssessmentResultResponse, MajorRecommendation,
    MajorRecommendationResponse, RecommendationsResponse, StudyRoadmap, RoadmapStep
)
from .university import (
    Major, MajorCreate, University, UniversityCreate, UniversityUpdate,
    UniversityMedia, UniversityMediaCreate, UniversityDetail, UniversityBasic,
    UniversitySearchFilter, UniversitySearchResponse, UniversityRecommendationRequest,
    UniversityRecommendation, RecommendationResponse, ComparisonRequest, UniversityComparison
)
from .application import (
    ApplicationCreate, ApplicationUpdate, Application, ApplicationDocument,
    ApplicationDetail, ApplicationListItem, ApplicationsResponse, ApplicationStatus
)
from .scholarship import (
    Scholarship, ScholarshipCreate, ScholarshipUpdate, ScholarshipApplication,
    ScholarshipApplicationCreate, ScholarshipDetail, ScholarshipListItem,
    ScholarshipSearchFilter, ScholarshipSearchResponse, EligibilityCheckRequest,
    EligibilityCheckResponse
)
from .partner import (
    Partner, PartnerCreate, PartnerUpdate, ServiceOffer, ServiceOfferCreate,
    ServiceOfferDetail, ServiceLeadCreate, ServiceLead, PartnerCategory,
    AllServicesResponse
)
from .payment import (
    PremiumFeature, PremiumFeatureCreate, PaymentCreate, Payment,
    PaymentInitiateResponse, PaymentVerifyRequest, PaymentVerifyResponse,
    PaymentHistory, UserPremiumStatus, PaymentMethod, PaymentStatus
)
from .notification import (
    Notification, NotificationCreate, NotificationUpdate, NotificationsResponse,
    NotificationType
)

__all__ = [
    # User models
    "OTPRequest", "OTPVerify", "UserRegister", "UserLogin", "SocialAuthRequest",
    "TokenResponse", "TokenRefresh", "User", "StudentProfileCreate", "StudentProfileUpdate",
    "StudentProfile", "UserWithProfile", "Document", "DocumentUpload",
    
    # Assessment models
    "Question", "AssessmentTest", "AssessmentTestResponse", "Answer", "SubmitAssessment",
    "AssessmentScore", "AssessmentResult", "AssessmentResultResponse", "MajorRecommendation",
    "MajorRecommendationResponse", "RecommendationsResponse", "StudyRoadmap", "RoadmapStep",
    
    # University models
    "Major", "MajorCreate", "University", "UniversityCreate", "UniversityUpdate",
    "UniversityMedia", "UniversityMediaCreate", "UniversityDetail", "UniversityBasic",
    "UniversitySearchFilter", "UniversitySearchResponse", "UniversityRecommendationRequest",
    "UniversityRecommendation", "RecommendationResponse", "ComparisonRequest", "UniversityComparison",
    
    # Application models
    "ApplicationCreate", "ApplicationUpdate", "Application", "ApplicationDocument",
    "ApplicationDetail", "ApplicationListItem", "ApplicationsResponse", "ApplicationStatus",
    
    # Scholarship models
    "Scholarship", "ScholarshipCreate", "ScholarshipUpdate", "ScholarshipApplication",
    "ScholarshipApplicationCreate", "ScholarshipDetail", "ScholarshipListItem",
    "ScholarshipSearchFilter", "ScholarshipSearchResponse", "EligibilityCheckRequest",
    "EligibilityCheckResponse",
    
    # Partner models
    "Partner", "PartnerCreate", "PartnerUpdate", "ServiceOffer", "ServiceOfferCreate",
    "ServiceOfferDetail", "ServiceLeadCreate", "ServiceLead", "PartnerCategory",
    "AllServicesResponse",
    
    # Payment models
    "PremiumFeature", "PremiumFeatureCreate", "PaymentCreate", "Payment",
    "PaymentInitiateResponse", "PaymentVerifyRequest", "PaymentVerifyResponse",
    "PaymentHistory", "UserPremiumStatus", "PaymentMethod", "PaymentStatus",
    
    # Notification models
    "Notification", "NotificationCreate", "NotificationUpdate", "NotificationsResponse",
    "NotificationType",
]
