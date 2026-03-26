from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError

from app.core.config import settings
from app.api.v1.endpoints import auth, home, transaction, category, admin
from app.db.base import Base
from app.db.session import engine, DATABASE_URL, SessionLocal
from app.db.seed import seed_db
from sqlalchemy_utils import database_exists, create_database

# Create database if it doesn't exist
if not database_exists(DATABASE_URL):
    create_database(DATABASE_URL)

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Seed default data
db = SessionLocal()
try:
    seed_db(db)
finally:
    db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

@CsrfProtect.load_config
def get_csrf_config():
    return [("secret_key", settings.CSRF_SECRET)]

@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(home.router, prefix="/api/v1/home", tags=["Home"])
app.include_router(transaction.router, prefix="/api/v1", tags=["Transactions"])
app.include_router(category.router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {"message": "Welcome to Finsight API!"}
