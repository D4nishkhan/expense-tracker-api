"""CRUD operations and query helpers for expenses."""

from datetime import date as date_type

from sqlalchemy import func
from sqlalchemy.orm import Session

import app.models as models
import app.schemas as schemas


def create_expense(db: Session, expense: schemas.ExpenseCreate) -> models.Expense:
    """Create a new expense record in the database."""
    db_expense = models.Expense(
        title=expense.title,
        amount=expense.amount,
        category=expense.category,
        date=expense.date,
        description=expense.description,
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expense(db: Session, expense_id: int) -> models.Expense | None:
    """Return a single expense by id, or None if not found."""
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()


def get_expenses(
    db: Session,
    category: str | None = None,
    start_date: date_type | None = None,
    end_date: date_type | None = None,
    skip: int = 0,
    limit: int = 10,
) -> list[models.Expense]:
    """Return a paginated, filtered list of expenses."""
    query = db.query(models.Expense)

    if category:
        query = query.filter(models.Expense.category == category)
    if start_date:
        query = query.filter(models.Expense.date >= start_date)
    if end_date:
        query = query.filter(models.Expense.date <= end_date)

    return query.order_by(models.Expense.date.desc()).offset(skip).limit(limit).all()


def get_expenses_total(
    db: Session,
    category: str | None = None,
    start_date: date_type | None = None,
    end_date: date_type | None = None,
) -> dict:
    """Return the total amount and count of expenses matching the filters."""
    query = db.query(models.Expense)

    if category:
        query = query.filter(models.Expense.category == category)
    if start_date:
        query = query.filter(models.Expense.date >= start_date)
    if end_date:
        query = query.filter(models.Expense.date <= end_date)

    total = query.with_entities(func.sum(models.Expense.amount)).scalar() or 0.0
    count = query.count()

    return {"total": float(total), "count": count}


def update_expense(
    db: Session, expense_id: int, expense: schemas.ExpenseUpdate
) -> models.Expense | None:
    """Update an existing expense. Returns None if not found."""
    db_expense = get_expense(db, expense_id)
    if db_expense is None:
        return None

    db_expense.title = expense.title
    db_expense.amount = expense.amount
    db_expense.category = expense.category
    db_expense.date = expense.date
    db_expense.description = expense.description

    db.commit()
    db.refresh(db_expense)
    return db_expense


def delete_expense(db: Session, expense_id: int) -> bool:
    """Delete an expense by id. Returns True if deleted, False if not found."""
    db_expense = get_expense(db, expense_id)
    if db_expense is None:
        return False

    db.delete(db_expense)
    db.commit()
    return True