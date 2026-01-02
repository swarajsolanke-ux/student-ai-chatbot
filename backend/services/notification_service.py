# services/notification_service.py - Notification service
import sqlite3
from datetime import datetime
from typing import Optional

def create_notification(
    db: sqlite3.Connection,
    user_id: int,
    title: str,
    message: str,
    notification_type: str = "info",
    link: Optional[str] = None
) -> int:
    """Create a new notification for a user"""
    cursor = db.cursor()
    
    cursor.execute(
        """INSERT INTO notifications (user_id, title, message, type, is_read, link)
           VALUES (?, ?, ?, ?, 0, ?)""",
        (user_id, title, message, notification_type, link)
    )
    db.commit()
    
    notification_id = cursor.lastrowid
    print(f" Created notification #{notification_id} for user {user_id}: {title}")
    
    return notification_id

def notify_application_status_change(
    db: sqlite3.Connection,
    user_id: int,
    university_name: str,
    status: str
):
    """Send notification when application status changes"""
    status_messages = {
        "Submitted": f"Your application to {university_name} has been submitted successfully!",
        "Under Review": f"Good news! Your application to {university_name} is now under review.",
        "Missing Documents": f"Action required: Your application to {university_name} is missing some documents.",
        "Conditional Offer": f"Congratulations! You have received a conditional offer from {university_name}!",
        "Final Offer": f" Congratulations! You have received a final offer from {university_name}!",
        "Rejected": f"Unfortunately, your application to {university_name} was not successful this time."
    }
    
    notification_types = {
        "Submitted": "success",
        "Under Review": "info",
        "Missing Documents": "warning",
        "Conditional Offer": "success",
        "Final Offer": "success",
        "Rejected": "error"
    }
    
    message = status_messages.get(status, f"Your application status to {university_name} has changed to: {status}")
    notification_type = notification_types.get(status, "info")
    
    return create_notification(
        db, user_id,
        title=f"Application Update - {university_name}",
        message=message,
        notification_type=notification_type,
        link=f"/applications"
    )

def notify_scholarship_status_change(
    db: sqlite3.Connection,
    user_id: int,
    scholarship_name: str,
    status: str
):
    """Send notification when scholarship application status changes"""
    status_messages = {
        "Submitted": f"Your scholarship application for {scholarship_name} has been submitted!",
        "Under Review": f"Your {scholarship_name} application is now under review.",
        "Approved": f"🎉 Congratulations! You have been approved for the {scholarship_name}!",
        "Rejected": f"Unfortunately, your {scholarship_name} application was not successful."
    }
    
    notification_types = {
        "Submitted": "success",
        "Under Review": "info",
        "Approved": "success",
        "Rejected": "error"
    }
    
    message = status_messages.get(status, f"Your scholarship status has changed to: {status}")
    notification_type = notification_types.get(status, "info")
    
    return create_notification(
        db, user_id,
        title=f"Scholarship Update - {scholarship_name}",
        message=message,
        notification_type=notification_type,
        link=f"/scholarships"
    )

def notify_payment_success(
    db: sqlite3.Connection,
    user_id: int,
    feature_name: str,
    amount: float
):
    """Send notification when payment is successful"""
    return create_notification(
        db, user_id,
        title="Payment Successful",
        message=f"Your payment of ${amount:.2f} for {feature_name} was successful. Premium features activated!",
        notification_type="success",
        link="/payment-history"
    )

def notify_document_uploaded(
    db: sqlite3.Connection,
    user_id: int,
    document_type: str
):
    """Send notification when document is uploaded"""
    return create_notification(
        db, user_id,
        title="Document Uploaded",
        message=f"Your {document_type} has been uploaded successfully and is pending verification.",
        notification_type="info",
        link="/profile/documents"
    )

def get_user_notifications(
    db: sqlite3.Connection,
    user_id: int,
    is_read: Optional[bool] = None,
    limit: int = 50
):
    """Get notifications for a user"""
    cursor = db.cursor()
    
    query = "SELECT id, title, message, type, is_read, link, created_at FROM notifications WHERE user_id = ?"
    params = [user_id]
    
    if is_read is not None:
        query += " AND is_read = ?"
        params.append(1 if is_read else 0)
    
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, tuple(params))
    
    notifications = []
    for row in cursor.fetchall():
        notifications.append({
            "id": row[0],
            "title": row[1],
            "message": row[2],
            "type": row[3],
            "is_read": bool(row[4]),
            "link": row[5],
            "created_at": row[6]
        })
    
    return notifications

def mark_notification_read(db: sqlite3.Connection, notification_id: int, user_id: int) -> bool:
    """Mark a notification as read"""
    cursor = db.cursor()
    cursor.execute(
        "UPDATE notifications SET is_read = 1 WHERE id = ? AND user_id = ?",
        (notification_id, user_id)
    )
    db.commit()
    return cursor.rowcount > 0

def mark_all_read(db: sqlite3.Connection, user_id: int) -> int:
    """Mark all notifications as read for a user"""
    cursor = db.cursor()
    cursor.execute(
        "UPDATE notifications SET is_read = 1 WHERE user_id = ? AND is_read = 0",
        (user_id,)
    )
    db.commit()
    return cursor.rowcount

def get_unread_count(db: sqlite3.Connection, user_id: int) -> int:
    """Get count of unread notifications"""
    cursor = db.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM notifications WHERE user_id = ? AND is_read = 0",
        (user_id,)
    )
    return cursor.fetchone()[0]
