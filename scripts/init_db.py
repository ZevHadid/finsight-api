import sys
import os

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy_utils import database_exists, create_database
from app.db.session import engine, DATABASE_URL, SessionLocal
from app.db.base import Base
# Import models here to register them with Base.metadata
from app.models.user import User
from app.models.transaction import Transaction
from app.models.category import Category
from app.db.seed import seed_db

def init_db():
    # Create database if it doesn't exist
    if not database_exists(DATABASE_URL):
        print(f"Creating database: {DATABASE_URL}")
        create_database(DATABASE_URL)

    # Create tables in the database
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    # Seed default data
    print("Seeding database...")
    db = SessionLocal()
    try:
        seed_db(db)
    finally:
        db.close()
    print("Initialization complete.")

if __name__ == "__main__":
    init_db()
