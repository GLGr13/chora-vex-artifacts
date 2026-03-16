from typing import Any
from pydantic import BaseModel, Field


class GateRequest(BaseModel):
    request_id: str
    timestamp_utc: str
    subject: str
    action_class: str
    payload_sha256: str = Field(pattern=r"^[a-fA-F0-9]{64}$")
    policy_context: str
    confidence: float | None = Field(default=None, ge=0, le=1)
    capabilities: list[str] = []
    dra: dict[str, Any] | None = None
    mcs_report: dict[str, Any] | None = None


class GateResponse(BaseModel):
    decision: str
    decision_id: str
    request_id: str
    timestamp_utc: str
    reasons: list[str]
    capsule_id: str | None = None
    merkle_root: str | None = None
    signature: str | None = None
    public_key_id: str | None = None
