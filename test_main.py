from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_endpoint_enforces_bounds():
    response = client.post(
        "/predict",
        json={"features": [-1000.0, 1000.0]},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["riskScore"] <= 100
    assert payload["riskScore"] >= 0


def test_cors_headers():
    response = client.options("/health", headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "content-type",
    })
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") in ["*", "http://localhost:3000"]


