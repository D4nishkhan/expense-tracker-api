"""Expenses router with CRUD, filtering, pagination, and totals."""

from datetime import date as date_type

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
from app.database import get_db

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post(
    "",
    response_model=schemas.ExpenseOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new expense",
)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    """Create a new expense record."""
    return crud.create_expense(db=db, expense=expense)


@router.get(
    "/total",
    response_model=schemas.ExpenseTotal,
    summary="Get total expenses",
)
def get_total(
    category: str | None = Query(None, description="Filter by category"),
    start_date: date_type | None = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: date_type | None = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    """Return the total amount and count of expenses matching the filters."""
    return crud.get_expenses_total(
        db=db, category=category, start_date=start_date, end_date=end_date
    )


@router.get(
    "",
    response_model=list[schemas.ExpenseOut],
    summary="List expenses with optional filtering and pagination",
)
def list_expenses(
    category: str | None = Query(None, description="Filter by category"),
    start_date: date_type | None = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: date_type | None = Query(None, description="End date (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
):
    """Return a paginated list of expenses, optionally filtered by category and/or date range."""
    return crud.get_expenses(
        db=db,
        category=category,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{expense_id}",
    response_model=schemas.ExpenseOut,
    summary="Get a single expense by id",
)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    """Return a single expense by id. Returns 404 if not found."""
    db_expense = crud.get_expense(db=db, expense_id=expense_id)
    if db_expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found",
        )
    return db_expense


@router.put(
    "/{expense_id}",
    response_model=schemas.ExpenseOut,
    summary="Update an existing expense",
)
def update_expense(
    expense_id: int,
    expense: schemas.ExpenseUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing expense. Returns 404 if not found."""
    db_expense = crud.update_expense(db=db, expense_id=expense_id, expense=expense)
    if db_expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found",
        )
    return db_expense


@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an expense",
)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    """Delete an expense by id. Returns 404 if not found."""
    deleted = crud.delete_expense(db=db, expense_id=expense_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found",
        )
    return None