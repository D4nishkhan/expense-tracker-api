"""Pydantic schemas for request and response validation."""

from datetime import date as date_type

from pydantic import BaseModel, Field, field_validator


class ExpenseBase(BaseModel):
    """Shared fields for create and update."""

    title: str = Field(..., min_length=1, max_length=200, description="Title of the expense")
    amount: float = Field(..., gt=0, description="Amount must be greater than 0")
    category: str = Field(..., min_length=1, max_length=100, description="Category of the expense")
    date: date_type = Field(..., description="Date of the expense (YYYY-MM-DD)")
    description: str | None = Field(None, max_length=2000, description="Optional description")

    @field_validator("title", "category")
    @classmethod
    def strip_and_validate_non_empty(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Field cannot be empty or only whitespace")
        return cleaned


class ExpenseCreate(ExpenseBase):
    """Schema for creating a new expense."""


class ExpenseUpdate(ExpenseBase):
    """Schema for updating an existing expense (all fields required)."""


class ExpenseOut(ExpenseBase):
    """Schema for returning an expense in responses."""

    id: int

    model_config = {"from_attributes": True}


class ExpenseTotal(BaseModel):
    """Schema for the total expense response."""

    total: float
    count: int