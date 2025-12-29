# payment.py - Payment and premium features models
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# ============= Enums =============

class PaymentMethod(str, Enum):
    KNET = "KNET"
    APPLE_PAY = "ApplePay"
    CARD = "Card"

class PaymentStatus(str, Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REFUNDED = "Refunded"

# ============= Premium Features =============

class PremiumFeatureBase(BaseModel):
    feature_name: str
    description: str
    price: float = Field(..., ge=0)
    duration_days: int = Field(..., ge=0)

class PremiumFeatureCreate(PremiumFeatureBase):
    pass

class PremiumFeatureUpdate(BaseModel):
    feature_name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    duration_days: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None

class PremiumFeature(PremiumFeatureBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

# ============= Payment Models =============

class PaymentCreate(BaseModel):
    user_id: int
    feature_id: int
    payment_method: PaymentMethod
    return_url: Optional[str] = None  # For redirects after payment

class PaymentInitiateResponse(BaseModel):
    payment_id: int
    amount: float
    currency: str
    payment_method: str
    payment_url: Optional[str] = None  # URL to payment gateway
    status: str
    message: str

class Payment(BaseModel):
    id: int
    user_id: int
    feature_id: int
    amount: float
    currency: str
    payment_method: str
    transaction_id: Optional[str] = None
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ============= Payment Verification =============

class PaymentVerifyRequest(BaseModel):
    payment_id: int
    transaction_id: Optional[str] = None
    payment_data: Optional[dict] = None  # Gateway-specific data

class PaymentVerifyResponse(BaseModel):
    payment_id: int
    status: PaymentStatus
    message: str
    feature_activated: bool
    activation_details: Optional[dict] = None

# ============= Payment History =============

class PaymentHistoryItem(BaseModel):
    id: int
    feature_name: str
    amount: float
    currency: str
    payment_method: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None

class PaymentHistory(BaseModel):
    payments: list[PaymentHistoryItem]
    total_count: int
    total_spent: float
    by_status: dict

# ============= Premium Access =============

class UserPremiumStatus(BaseModel):
    is_premium: bool
    active_features: list[str]
    expiry_dates: dict
    total_features: int

class FeatureAccessCheck(BaseModel):
    feature_name: str
    has_access: bool
    reason: Optional[str] = None
    upgrade_url: Optional[str] = None

# ============= Simulated Payment (for testing) =============

class SimulatedPaymentRequest(BaseModel):
    payment_id: int
    simulate_success: bool = True
    delay_seconds: int = Field(0, ge=0, le=10)

class SimulatedPaymentResponse(BaseModel):
    payment_id: int
    simulated_transaction_id: str
    status: PaymentStatus
    message: str

# ============= Payment Gateway Integration =============

class KNETPaymentRequest(BaseModel):
    amount: float
    currency: str = "KWD"
    reference: str
    return_url: str

class KNETPaymentResponse(BaseModel):
    payment_url: str
    payment_id: str
    tracking_id: str

class ApplePayRequest(BaseModel):
    payment_id: int
    apple_pay_token: dict

class CardPaymentRequest(BaseModel):
    payment_id: int
    card_number: str
    card_holder: str
    expiry_month: int = Field(..., ge=1, le=12)
    expiry_year: int
    cvv: str = Field(..., min_length=3, max_length=4)

# ============= Admin Payment Management =============

class PaymentStats(BaseModel):
    total_revenue: float
    revenue_by_feature: dict
    revenue_by_month: dict
    total_transactions: int
    successful_transactions: int
    failed_transactions: int
    success_rate: float
    avg_transaction_value: float

class RefundRequest(BaseModel):
    payment_id: int
    reason: str
    refund_amount: Optional[float] = None  # None = full refund

class RefundResponse(BaseModel):
    payment_id: int
    refund_amount: float
    status: str
    message: str
    refund_transaction_id: Optional[str] = None
