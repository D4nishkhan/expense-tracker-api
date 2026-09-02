# Expense Tracker

A full-stack expense tracking application built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **HTML/CSS/JavaScript**.

The application provides a RESTful API for managing expenses and a web-based frontend for interacting with the API.

## Live Demo

- **Frontend:** https://expense-tracker-frontend-3tpw.onrender.com
- **Backend API:** https://expense-tracker-api-30jh.onrender.com
- **Swagger UI:** https://expense-tracker-api-30jh.onrender.com/docs

## Features

- **CRUD operations** for expenses (create, read, update, delete)
- **Filtering** by category and date range
- **Pagination** via `skip` and `limit` query parameters
- **Total expense** endpoint with optional filters
- **Validation & error handling** with Pydantic and proper HTTP status codes
- **Environment variables** for configuration via `pydantic-settings`
- **Automated tests** with `pytest`
- **PostgreSQL** database for production deployment
- **Responsive web frontend** for managing expenses

## Project Structure

```text
c:\FastAPI-Basics\
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers/
│       ├── __init__.py
│       └── expenses.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_expenses.py
├── index.html
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── main.py
Expense Fields
Field	Type	Required	Description
id	int	auto	Primary key
title	string	yes	Title (1–200 chars)
amount	float	yes	Must be greater than 0
category	string	yes	Category (1–100 chars)
date	date	yes	Date in YYYY-MM-DD format
description	string	no	Optional description (max 2000 chars)
Setup
1. Install dependencies
pip install -r requirements.txt
2. Run the server
uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000

Interactive docs (Swagger UI):

http://127.0.0.1:8000/docs
API Endpoints
Method	Path	Status	Description
GET	/	200	Health check / welcome
POST	/expenses	201	Create a new expense
GET	/expenses	200	List expenses (filter + pagination)
GET	/expenses/total	200	Total amount & count of expenses
GET	/expenses/{id}	200	Get a single expense
PUT	/expenses/{id}	200	Update an expense
DELETE	/expenses/{id}	204	Delete an expense
Query Parameters for GET /expenses
Parameter	Type	Default	Description
category	string	—	Filter by category
start_date	date	—	Filter expenses on/after this date
end_date	date	—	Filter expenses on/before this date
skip	int	0	Number of records to skip (≥ 0)
limit	int	10	Max records to return (1–100)
Example: Create an Expense
curl -X POST http://127.0.0.1:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Groceries",
    "amount": 50.25,
    "category": "Food",
    "date": "2025-01-15",
    "description": "Weekly grocery shopping"
  }'
Example: List with Filters and Pagination
curl "http://127.0.0.1:8000/expenses?category=Food&start_date=2025-01-01&end_date=2025-01-31&skip=0&limit=10"
Example: Get Total
curl "http://127.0.0.1:8000/expenses/total?category=Food"
Running Tests
pytest -v

Tests use an in-memory SQLite database and cover:

Creating expenses (including validation errors)
Reading a single expense (including 404)
Listing with category and date-range filters
Pagination
Updating expenses (including 404)
Deleting expenses (including 404)
Total endpoint with filters
Configuration

Environment variables are loaded from .env:

Variable	Default	Description
DATABASE_URL	sqlite:///./expenses.db	SQLAlchemy database URL
APP_NAME	Expense Tracker API	Application name
APP_VERSION	1.0.0	Application version
Deployment

The application is deployed on Render.

Frontend: Render Static Site
Backend: Render Web Service
Production Database: Render PostgreSQL

The live application can be accessed using the links in the Live Demo section above.
