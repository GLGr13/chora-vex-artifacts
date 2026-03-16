from fastapi.testclient import TestClient
from chora.api.app import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_gate_allow() -> None:
    payload = {
        "request_id": "req-1",
        "timestamp_utc": "2026-03-16T00:00:00Z",
        "subject": "demo-agent",
        "action_class": "respond",
        "payload_sha256": "a" * 64,
        "policy_context": "public-demo",
        "confidence": 0.91
    }
    response = client.post("/gate", json=payload)
    assert response.status_code == 200
    assert response.json()["decision"] == "ALLOW"
