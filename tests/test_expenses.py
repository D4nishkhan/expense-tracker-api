"""Tests for the Expense Tracker API."""

from datetime import date


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def create_expense(client, **overrides):
    """Create an expense with sensible defaults; override any field via kwargs."""
    payload = {
        "title": "Lunch",
        "amount": 15.50,
        "category": "Food",
        "date": "2025-01-10",
        "description": "Lunch with team",
    }
    payload.update(overrides)
    return client.post("/expenses", json=payload)


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["version"] == "1.0.0"


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
def test_create_expense(client):
    response = create_expense(client)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Lunch"
    assert data["amount"] == 15.50
    assert data["category"] == "Food"
    assert data["date"] == "2025-01-10"
    assert data["description"] == "Lunch with team"
    assert "id" in data


def test_create_expense_without_description(client):
    response = create_expense(client, description=None)
    assert response.status_code == 201
    assert response.json()["description"] is None


def test_create_expense_invalid_amount(client):
    response = create_expense(client, amount=-5)
    assert response.status_code == 422


def test_create_expense_missing_title(client):
    payload = {"amount": 10, "category": "Food", "date": "2025-01-10"}
    response = client.post("/expenses", json=payload)
    assert response.status_code == 422


def test_create_expense_empty_title(client):
    response = create_expense(client, title="   ")
    assert response.status_code == 422


def test_create_expense_invalid_date(client):
    response = create_expense(client, date="not-a-date")
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Read one
# ---------------------------------------------------------------------------
def test_get_expense(client):
    create_resp = create_expense(client)
    expense_id = create_resp.json()["id"]

    response = client.get(f"/expenses/{expense_id}")
    assert response.status_code == 200
    assert response.json()["id"] == expense_id


def test_get_expense_not_found(client):
    response = client.get("/expenses/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


# ---------------------------------------------------------------------------
# List + filtering + pagination
# ---------------------------------------------------------------------------
def test_list_expenses(client):
    create_expense(client, title="A", category="Food")
    create_expense(client, title="B", category="Transport")

    response = client.get("/expenses")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_list_expenses_filter_by_category(client):
    create_expense(client, title="A", category="Food")
    create_expense(client, title="B", category="Transport")
    create_expense(client, title="C", category="Food")

    response = client.get("/expenses?category=Food")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(e["category"] == "Food" for e in data)


def test_list_expenses_filter_by_date_range(client):
    create_expense(client, title="A", date="2025-01-05")
    create_expense(client, title="B", date="2025-01-15")
    create_expense(client, title="C", date="2025-01-25")

    response = client.get("/expenses?start_date=2025-01-10&end_date=2025-01-20")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "B"


def test_list_expenses_pagination(client):
    for i in range(15):
        create_expense(client, title=f"Expense {i}")

    response = client.get("/expenses?skip=0&limit=5")
    assert response.status_code == 200
    assert len(response.json()) == 5

    response = client.get("/expenses?skip=10&limit=5")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_list_expenses_invalid_pagination(client):
    response = client.get("/expenses?skip=-1")
    assert response.status_code == 422

    response = client.get("/expenses?limit=0")
    assert response.status_code == 422

    response = client.get("/expenses?limit=101")
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------
def test_update_expense(client):
    create_resp = create_expense(client)
    expense_id = create_resp.json()["id"]

    update_payload = {
        "title": "Updated Lunch",
        "amount": 20.00,
        "category": "Food",
        "date": "2025-01-11",
        "description": "Updated description",
    }
    response = client.put(f"/expenses/{expense_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Lunch"
    assert data["amount"] == 20.00
    assert data["description"] == "Updated description"


def test_update_expense_not_found(client):
    update_payload = {
        "title": "Updated",
        "amount": 20.00,
        "category": "Food",
        "date": "2025-01-11",
    }
    response = client.put("/expenses/9999", json=update_payload)
    assert response.status_code == 404


def test_update_expense_invalid_data(client):
    create_resp = create_expense(client)
    expense_id = create_resp.json()["id"]

    update_payload = {
        "title": "Updated",
        "amount": -10,
        "category": "Food",
        "date": "2025-01-11",
    }
    response = client.put(f"/expenses/{expense_id}", json=update_payload)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
def test_delete_expense(client):
    create_resp = create_expense(client)
    expense_id = create_resp.json()["id"]

    response = client.delete(f"/expenses/{expense_id}")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/expenses/{expense_id}")
    assert response.status_code == 404


def test_delete_expense_not_found(client):
    response = client.delete("/expenses/9999")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Total
# ---------------------------------------------------------------------------
def test_total_expenses(client):
    create_expense(client, amount=10.50)
    create_expense(client, amount=20.00)
    create_expense(client, amount=5.50, category="Transport")

    response = client.get("/expenses/total")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 36.00
    assert data["count"] == 3


def test_total_expenses_filtered_by_category(client):
    create_expense(client, amount=10.50, category="Food")
    create_expense(client, amount=20.00, category="Food")
    create_expense(client, amount=5.50, category="Transport")

    response = client.get("/expenses/total?category=Food")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 30.50
    assert data["count"] == 2


def test_total_expenses_filtered_by_date_range(client):
    create_expense(client, amount=10.00, date="2025-01-05")
    create_expense(client, amount=20.00, date="2025-01-15")
    create_expense(client, amount=5.00, date="2025-01-25")

    response = client.get("/expenses/total?start_date=2025-01-10&end_date=2025-01-20")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 20.00
    assert data["count"] == 1


def test_total_expenses_empty(client):
    response = client.get("/expenses/total")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0.0
    assert data["count"] == 0