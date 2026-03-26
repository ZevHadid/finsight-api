from sqlalchemy.orm import Session
from app.services import user_service, category_service
from app.schemas.user import UserCreate
from app.schemas.category import CategoryCreate
from app.core.config import settings

def seed_db(db: Session):
    # Check if admin already exists
    admin_email = settings.FIRST_USER_ADMIN_EMAIL
    existing_admin = user_service.get_user_by_email(db, email=admin_email)
    
    if not existing_admin:
        print(f"Seeding default admin user: {admin_email}")
        admin_in = UserCreate(
            name="Super Admin",
            email=admin_email,
            password=settings.FIRST_USER_ADMIN_PASSWORD,
            is_admin=True
        )
        user_service.create_user(db, user=admin_in)

    # Seed default categories
    default_categories = [
        ("Housing", "Rent, mortgage, etc."),
        ("Food", "Groceries, dining out, etc."),
        ("Transportation", "Fuel, public transit, etc."),
        ("Entertainment", "Movies, games, concerts, etc."),
        ("Utilities", "Electricity, water, internet, etc."),
        ("Income", "Salary, bonuses, gifts, etc."),
        ("Other", "Miscellaneous expenses or income.")
    ]

    for name, desc in default_categories:
        if not category_service.get_category_by_name(db, name=name):
            print(f"Seeding category: {name}")
            category_in = CategoryCreate(name=name, description=desc)
            category_service.create_category(db, category=category_in)
