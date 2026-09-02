"""SQLAlchemy models for the Expense Tracker API."""

from datetime import date as date_type

from sqlalchemy import Column, Date, Float, Integer, String, Text

from app.database import Base


class Expense(Base):
    """Represents a single expense record."""

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    description = Column(Text, nullable=True)