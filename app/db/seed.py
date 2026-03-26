from sqlalchemy.orm import Session
from app.services import user_service
from app.schemas.user import UserCreate

def seed_db(db: Session):
    # Check if admin already exists
    admin_email = "admin@finsight.com"
    existing_admin = user_service.get_user_by_email(db, email=admin_email)
    
    if not existing_admin:
        print(f"Seeding default admin user: {admin_email}")
        admin_in = UserCreate(
            name="Super Admin",
            email=admin_email,
            password="admin123",
            is_admin=True
        )
        user_service.create_user(db, user=admin_in)
