# notification.py - Notification models
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

# ============= Enums =============

class NotificationType(str, Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"

# ============= Notification Models =============

class NotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str
    type: NotificationType = NotificationType.INFO
    link: Optional[str] = None

class Notification(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: str
    is_read: bool
    link: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class NotificationUpdate(BaseModel):
    is_read: bool = True

# ============= Notification Response =============

class NotificationsResponse(BaseModel):
    notifications: List[Notification]
    total_count: int
    unread_count: int
    page: int
    page_size: int

class NotificationStats(BaseModel):
    total_notifications: int
    unread_count: int
    by_type: dict

# ============= Bulk Operations =============

class MarkAllAsReadResponse(BaseModel):
    marked_count: int
    message: str

# Models index file
