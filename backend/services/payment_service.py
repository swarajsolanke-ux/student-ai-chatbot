# services/payment_service.py - Payment processing service (Simulated)
import sqlite3
from datetime import datetime, timedelta
from typing import Optional
import random
import string
from config import settings

def generate_transaction_id() -> str:
    """Generate a unique transaction ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"TXN_{timestamp}_{random_suffix}"

def initiate_payment(
    db: sqlite3.Connection,
    user_id: int,
    feature_id: int,
    payment_method: str
) -> dict:
    """Initiate a payment transaction"""
    cursor = db.cursor()
    
    # Get feature details
    cursor.execute(
        "SELECT feature_name, price FROM premium_features WHERE id = ? AND is_active = 1",
        (feature_id,)
    )
    feature = cursor.fetchone()
    
    if not feature:
        raise ValueError("Feature not found or inactive")
    
    feature_name, price = feature
    
    # Create payment record
    cursor.execute(
        """INSERT INTO payments (user_id, feature_id, amount, currency, payment_method, status)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (user_id, feature_id, price, "KWD", payment_method, "Pending")
    )
    db.commit()
    
    payment_id = cursor.lastrowid
    
    # Generate payment URL based on method
    if settings.PAYMENT_MODE == "simulated":
        payment_url = f"{settings.FRONTEND_URL}/payment/simulate/{payment_id}"
    else:
        # In production, integrate with actual payment gateway
        payment_url = f"/api/payment/gateway/{payment_id}"
    
    return {
        "payment_id": payment_id,
        "amount": price,
        "currency": "KWD",
        "payment_method": payment_method,
        "payment_url": payment_url,
        "status": "Pending",
        "message": "Payment initiated successfully"
    }

def simulate_payment(
    db: sqlite3.Connection,
    payment_id: int,
    success: bool = True
) -> dict:
    """
    Simulate payment completion (for testing)
    In production, this is called by payment gateway callback
    """
    cursor = db.cursor()
    
    # Get payment details
    cursor.execute(
        "SELECT user_id, feature_id, amount, status FROM payments WHERE id = ?",
        (payment_id,)
    )
    payment = cursor.fetchone()
    
    if not payment:
        raise ValueError("Payment not found")
    
    user_id, feature_id, amount, status = payment
    
    if status != "Pending":
        raise ValueError(f"Payment already {status}")
    
    transaction_id = generate_transaction_id()
    new_status = "Completed" if success else "Failed"
    
    # Update payment status
    cursor.execute(
        """UPDATE payments 
           SET status = ?, transaction_id = ?, completed_at = ?
           WHERE id = ?""",
        (new_status, transaction_id, datetime.now(), payment_id)
    )
    
    if success:
        # Activate premium feature
        activate_premium_feature(db, user_id, feature_id)
    
    db.commit()
    
    return {
        "payment_id": payment_id,
        "transaction_id": transaction_id,
        "status": new_status,
        "message": "Payment completed successfully" if success else "Payment failed"
    }

def verify_payment(
    db: sqlite3.Connection,
    payment_id: int,
    transaction_id: Optional[str] = None
) -> dict:
    """
    Verify payment status
    In production, verify with payment gateway
    """
    cursor = db.cursor()
    
    cursor.execute(
        "SELECT user_id, feature_id, status, transaction_id, completed_at FROM payments WHERE id = ?",
        (payment_id,)
    )
    payment = cursor.fetchone()
    
    if not payment:
        raise ValueError("Payment not found")
    
    user_id, feature_id, status, stored_transaction_id, completed_at = payment
    
    # In production, verify with payment gateway here
    
    feature_activated = (status == "Completed")
    
    return {
        "payment_id": payment_id,
        "status": status,
        "message": f"Payment {status.lower()}",
        "feature_activated": feature_activated,
        "activation_details": {
            "transaction_id": stored_transaction_id,
            "completed_at": completed_at
        } if feature_activated else None
    }

def activate_premium_feature(
    db: sqlite3.Connection,
    user_id: int,
    feature_id: int
):
    """Activate a premium feature for a user"""
    cursor = db.cursor()
    
    # Get feature details
    cursor.execute(
        "SELECT feature_name, duration_days FROM premium_features WHERE id = ?",
        (feature_id,)
    )
    feature = cursor.fetchone()
    
    if not feature:
        return False
    
    feature_name, duration_days = feature
    
    # Update user to premium
    cursor.execute(
        "UPDATE users SET is_premium = 1 WHERE id = ?",
        (user_id,)
    )
    db.commit()
    
    print(f"✅ Activated {feature_name} for user {user_id} (duration: {duration_days} days)")
    
    # In production, store feature expiration and specific feature access
    # For now, just mark user as premium
    
    return True

def get_payment_history(
    db: sqlite3.Connection,
    user_id: int,
    limit: int = 50
):
    """Get payment history for a user"""
    cursor = db.cursor()
    
    cursor.execute(
        """SELECT p.id, pf.feature_name, p.amount, p.currency, 
                  p.payment_method, p.status, p.created_at, p.completed_at
           FROM payments p
           JOIN premium_features pf ON p.feature_id = pf.id
           WHERE p.user_id = ?
           ORDER BY p.created_at DESC
           LIMIT ?""",
        (user_id, limit)
    )
    
    payments = []
    for row in cursor.fetchall():
        payments.append({
            "id": row[0],
            "feature_name": row[1],
            "amount": row[2],
            "currency": row[3],
            "payment_method": row[4],
            "status": row[5],
            "created_at": row[6],
            "completed_at": row[7]
        })
    
    # Calculate total spent
    cursor.execute(
        "SELECT SUM(amount) FROM payments WHERE user_id = ? AND status = 'Completed'",
        (user_id,)
    )
    total_spent = cursor.fetchone()[0] or 0.0
    
    # Count by status
    cursor.execute(
        """SELECT status, COUNT(*) 
           FROM payments 
           WHERE user_id = ? 
           GROUP BY status""",
        (user_id,)
    )
    by_status = dict(cursor.fetchall())
    
    return {
        "payments": payments,
        "total_count": len(payments),
        "total_spent": total_spent,
        "by_status": by_status
    }

def check_premium_access(db: sqlite3.Connection, user_id: int) -> dict:
    """Check if user has premium access"""
    cursor = db.cursor()
    
    cursor.execute(
        "SELECT is_premium FROM users WHERE id = ?",
        (user_id,)
    )
    result = cursor.fetchone()
    
    if not result:
        return {"is_premium": False, "active_features": [], "expiry_dates": {}, "total_features": 0}
    
    is_premium = bool(result[0])
    
    # In production, check individual feature expiration
    # For now, just return premium status
    
    return {
        "is_premium": is_premium,
        "active_features": ["all"] if is_premium else [],
        "expiry_dates": {},
        "total_features": 1 if is_premium else 0
    }

def refund_payment(
    db: sqlite3.Connection,
    payment_id: int,
    reason: str,
    refund_amount: Optional[float] = None
) -> dict:
    """Process a refund"""
    cursor = db.cursor()
    
    # Get payment details
    cursor.execute(
        "SELECT user_id, amount, status FROM payments WHERE id = ?",
        (payment_id,)
    )
    payment = cursor.fetchone()
    
    if not payment:
        raise ValueError("Payment not found")
    
    user_id, amount, status = payment
    
    if status != "Completed":
        raise ValueError(f"Cannot refund payment with status: {status}")
    
    refund_amt = refund_amount if refund_amount else amount
    
    if refund_amt > amount:
        raise ValueError("Refund amount cannot exceed payment amount")
    
    # Update payment status
    refund_transaction_id = generate_transaction_id()
    cursor.execute(
        "UPDATE payments SET status = 'Refunded', transaction_id = ? WHERE id = ?",
        (refund_transaction_id, payment_id)
    )
    db.commit()
    
    print(f"Refunded ${refund_amt} for payment #{payment_id}. Reason: {reason}")
    
    return {
        "payment_id": payment_id,
        "refund_amount": refund_amt,
        "status": "Refunded",
        "message": "Refund processed successfully",
        "refund_transaction_id": refund_transaction_id
    }
