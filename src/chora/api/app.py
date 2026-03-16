from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from fastapi import FastAPI

from chora.core.models import GateRequest, GateResponse

app = FastAPI(title="CHORA Gate", version="0.3.0a0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "chora-gate", "version": "0.3.0a0"}


@app.get("/public_key")
def public_key() -> dict[str, str | None]:
    return {"public_key_id": "demo-key", "public_key": None}


@app.post("/gate", response_model=GateResponse)
def gate(request: GateRequest) -> GateResponse:
    decision = "ALLOW"
    reasons = ["default reference implementation path"]

    if request.mcs_report and request.mcs_report.get("recommended_gate_bias") == "HALT":
        decision = "HALT"
        reasons = ["mcs recommended halt"]
    elif request.confidence is not None and request.confidence < 0.5:
        decision = "ESCALATE"
        reasons = ["confidence below reference threshold"]

    now = datetime.now(timezone.utc).isoformat()
    decision_id = sha256(f"{request.request_id}:{decision}:{now}".encode()).hexdigest()[:16]
    capsule_id = f"capsule-{decision_id}"

    return GateResponse(
        decision=decision,
        decision_id=decision_id,
        request_id=request.request_id,
        timestamp_utc=now,
        reasons=reasons,
        capsule_id=capsule_id,
        merkle_root=None,
        signature=None,
        public_key_id="demo-key",
    )


@app.get("/capsules/{capsule_id}")
def get_capsule(capsule_id: str) -> dict[str, object]:
    return {
        "capsule_id": capsule_id,
        "status": "stub",
        "note": "Specimen retrieval endpoint placeholder for public repo shell"
    }


@app.get("/capsules/{capsule_id}/verify")
def verify_capsule(capsule_id: str) -> dict[str, object]:
    return {
        "capsule_id": capsule_id,
        "verified": False,
        "note": "Verification pipeline placeholder for public repo shell"
    }
