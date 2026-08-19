from src.config import get_logger
from src.database import SessionLocal
from src.jwt_auth.models import User
from src.utils.password_helper import hash_password

logger = get_logger(__name__)

SAMPLE_USERS = [
    {
        "name": "Test User",
        "email_address": "testuser@example.com",
        "password": "Test@123",
        "phone_number": "9876543210",
    },
    {
        "name": "Demo User",
        "email_address": "demouser@example.com",
        "password": "demo@123",
        "phone_number": "9876543211",
    },
]


def seed_users() -> None:
    db = SessionLocal()

    try:
        for sample_user in SAMPLE_USERS:
            existing_user = (
                db.query(User)
                .filter(User.email_address == sample_user["email_address"])
                .first()
            )

            if existing_user:
                logger.info(
                    "User already exists, skipping: %s",
                    sample_user["email_address"],
                )
                continue

            user = User(
                name=sample_user["name"],
                email_address=sample_user["email_address"],
                password_hash=hash_password(sample_user["password"]),
                phone_number=sample_user["phone_number"],
                is_active=True,
                created_by="automation",
                updated_by="automation",
            )

            db.add(user)

        db.commit()
        logger.info("static users inserted successfully")

    except Exception:
        db.rollback()
        logger.exception("Error seeding users")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_users()
