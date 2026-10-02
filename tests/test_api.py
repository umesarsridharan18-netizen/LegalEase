import os

os.environ["MOCK_AI"] = "true"

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_generate_mock():
    payload = {
        "document_type": "Freelance Work Contract",
        "parties": "Jane Doe (Provider), TechNova Inc. (Client)",
        "terms": "Payment within 30 days; Confidentiality",
        "effective_date": "October 1, 2026",
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["mock"] is True
    assert "Freelance Work Contract" in data["document"]
