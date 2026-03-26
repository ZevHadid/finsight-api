from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.services import category_service
from app.schemas.category import Category, CategoryCreate, CategoryUpdate
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[Category])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve categories.
    """
    categories = category_service.get_categories(db, skip=skip, limit=limit)
    return categories

@router.post("/", response_model=Category)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: CategoryCreate,
    current_admin: User = Depends(deps.get_current_admin)
) -> Any:
    """
    Create new category. (Admin only)
    """
    category = category_service.get_category_by_name(db, name=category_in.name)
    if category:
        raise HTTPException(
            status_code=400,
            detail="Category with this name already exists.",
        )
    return category_service.create_category(db, category=category_in)

@router.put("/{id}", response_model=Category)
def update_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    category_in: CategoryUpdate,
    current_admin: User = Depends(deps.get_current_admin)
) -> Any:
    """
    Update a category. (Admin only)
    """
    category = category_service.update_category(db, category_id=id, category=category_in)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/{id}", response_model=bool)
def delete_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_admin: User = Depends(deps.get_current_admin)
) -> Any:
    """
    Delete a category. (Admin only)
    """
    success = category_service.delete_category(db, category_id=id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return success
