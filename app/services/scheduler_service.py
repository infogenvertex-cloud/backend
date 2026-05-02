import logging
from datetime import date

from app.config import settings
from app.database import SessionLocal
from app.services.subscription_service import get_expiring_subscriptions, expire_overdue_subscriptions
from app.services.whatsapp_service import send_text_message

logger = logging.getLogger(__name__)


async def check_expiring_subscriptions():
    logger.info("Running daily subscription expiry check...")
    db = SessionLocal()
    try:
        expired_count = expire_overdue_subscriptions(db)
        if expired_count:
            logger.info(f"Marked {expired_count} subscriptions as expired.")

        expiring = get_expiring_subscriptions(db, days=settings.EXPIRY_REMINDER_DAYS)
        logger.info(f"Found {len(expiring)} subscriptions expiring soon.")

        for sub in expiring:
            member = sub.member
            days_left = (sub.end_date - date.today()).days
            message = (
                f"Hi {member.name}, your gym subscription "
                f"({sub.plan.replace('_', ' ')}) expires in {days_left} day(s) "
                f"on {sub.end_date.strftime('%d-%m-%Y')}. "
                f"Please renew to continue your fitness journey!"
            )
            await send_text_message(member.phone, message)
            logger.info(f"Sent expiry reminder to {member.name} ({member.phone})")
    except Exception as e:
        logger.error(f"Error in scheduler: {e}")
    finally:
        db.close()
