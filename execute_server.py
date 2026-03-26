from __future__ import annotations

from typing import Any, Dict

from fastapi import FastAPI
from pydantic import BaseModel

from verify_handshake import verify_boundary_crossing, BoundaryStatus

app = FastAPI(title="CHORA Runtime Enforcement Demo")


class ExecuteRequest(BaseModel):
    capsule: Dict[str, Any]
    action: str = "demo_action"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/execute")
def execute(req: ExecuteRequest):
    from pathlib import Path
    import json
    tmp_path = Path("/tmp/execute_request_capsule.json")
    tmp_path.write_text(json.dumps(req.capsule), encoding="utf-8")
    result = verify_boundary_crossing(tmp_path)

    if result.boundary_status == BoundaryStatus.AUTHORIZED:
        return {
            "status": "EXECUTED",
            "action": req.action,
            "boundary_status": result.boundary_status,
            "token_signature": result.signature_status,
            "notes": result.notes,
        }

    return {
        "status": "DENIED",
        "action": req.action,
        "boundary_status": result.boundary_status,
        "token_signature": result.signature_status,
        "notes": result.notes,
    }
