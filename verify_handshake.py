#!/usr/bin/env python3
"""
verify_handshake.py

Minimal CHORA handshake adapter for pre-meeting verification.

What it does:
- Loads a handshake capsule JSON
- Normalizes key fields into a CHORA-friendly internal view
- Validates required structure
- Verifies commitment binding
- Checks token time window
- Provides a mock-aware signature verification status
- Produces a fail-closed boundary authorization decision

Usage:
    python verify_handshake.py /path/to/capsule.json
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from chora_token_crypto import verify_payload_signature


# ----------------------------
# Enums / Data Structures
# ----------------------------

class Outcome(str, Enum):
    ALLOW = "ALLOW"
    HALT = "HALT"
    ESCALATE = "ESCALATE"


class BoundaryStatus(str, Enum):
    AUTHORIZED = "AUTHORIZED"
    DENIED = "DENIED"
    PENDING = "PENDING"


class SignatureStatus(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    NOT_PRESENT = "NOT_PRESENT"


@dataclass
class ValidationResult:
    ok: bool
    message: str


@dataclass
class NormalizedCapsule:
    raw: Dict[str, Any]

    capsule_id: Optional[str]
    outcome: Optional[str]
    reason_code: Optional[str]
    nonce: Optional[str]

    commitment_hash: Optional[str]
    public_inputs_commitment_hash: Optional[str]
    start_root: Optional[str]
    public_salt: Optional[str]

    continuation_token_payload: Optional[Dict[str, Any]]
    continuation_token_signature: Optional[str]

    issuer: Optional[str]
    iat: Optional[str]
    exp: Optional[str]


@dataclass
class VerificationReport:
    structure: ValidationResult
    commitment_binding: ValidationResult
    token_window: ValidationResult
    signature_status: SignatureStatus
    boundary_status: BoundaryStatus
    notes: Tuple[str, ...]


# ----------------------------
# Helpers
# ----------------------------

def _safe_get(obj: Dict[str, Any], *path: str) -> Any:
    """Safely traverse nested dicts."""
    current: Any = obj
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def _parse_utc(ts: Optional[str]) -> Optional[datetime]:
    """
    Parse RFC3339-ish timestamps like 2026-03-17T19:06:55Z.
    Returns timezone-aware UTC datetime or None.
    """
    if not ts or not isinstance(ts, str):
        return None
    try:
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


# ----------------------------
# Phase 1 — Load and normalize
# ----------------------------

def load_handshake_capsule(path: str | Path) -> NormalizedCapsule:
    """
    Load a handshake capsule JSON and normalize key fields into a CHORA-friendly view.
    """
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    token_payload = _safe_get(raw, "continuation_token", "payload")
    public_inputs = _safe_get(raw, "intent_data", "public_inputs")

    return NormalizedCapsule(
        raw=raw,
        capsule_id=_safe_get(raw, "capsule_id"),
        outcome=_safe_get(raw, "outcome"),
        reason_code=_safe_get(raw, "reason_code"),
        nonce=_safe_get(raw, "nonce"),
        commitment_hash=_safe_get(raw, "intent_data", "commitment_hash"),
        public_inputs_commitment_hash=_safe_get(raw, "intent_data", "public_inputs", "commitment_hash"),
        start_root=_safe_get(raw, "intent_data", "public_inputs", "start_root"),
        public_salt=_safe_get(raw, "intent_data", "public_inputs", "public_salt"),
        continuation_token_payload=token_payload if isinstance(token_payload, dict) else None,
        continuation_token_signature=_safe_get(raw, "continuation_token", "signature"),
        issuer=_safe_get(raw, "continuation_token", "payload", "issuer"),
        iat=_safe_get(raw, "continuation_token", "payload", "iat"),
        exp=_safe_get(raw, "continuation_token", "payload", "exp"),
    )


# ----------------------------
# Phase 2 — Structural validation
# ----------------------------

def validate_capsule_structure(capsule: NormalizedCapsule) -> ValidationResult:
    """
    Fail-closed structural validation.
    """
    required_fields = {
        "capsule_id": capsule.capsule_id,
        "outcome": capsule.outcome,
        "reason_code": capsule.reason_code,
        "intent_data.commitment_hash": capsule.commitment_hash,
        "intent_data.public_inputs.commitment_hash": capsule.public_inputs_commitment_hash,
        "continuation_token.payload": capsule.continuation_token_payload,
        "continuation_token.signature": capsule.continuation_token_signature,
        "continuation_token.payload.issuer": capsule.issuer,
        "continuation_token.payload.iat": capsule.iat,
        "continuation_token.payload.exp": capsule.exp,
    }

    missing = [name for name, value in required_fields.items() if value in (None, "", {})]
    if missing:
        return ValidationResult(
            ok=False,
            message=f"Missing required field(s): {', '.join(missing)}"
        )

    if capsule.outcome not in {o.value for o in Outcome}:
        return ValidationResult(
            ok=False,
            message=f"Invalid outcome: {capsule.outcome}"
        )

    if _parse_utc(capsule.iat) is None:
        return ValidationResult(
            ok=False,
            message=f"Invalid iat timestamp: {capsule.iat!r}"
        )

    if _parse_utc(capsule.exp) is None:
        return ValidationResult(
            ok=False,
            message=f"Invalid exp timestamp: {capsule.exp!r}"
        )

    return ValidationResult(ok=True, message="Required structure is present and parseable")


# ----------------------------
# Phase 6 — Commitment binding
# ----------------------------

def verify_commitment_binding(capsule: NormalizedCapsule) -> ValidationResult:
    """
    Verify that the commitment hash in the capsule matches the one in public inputs.
    """
    if not capsule.commitment_hash or not capsule.public_inputs_commitment_hash:
        return ValidationResult(
            ok=False,
            message="Commitment binding cannot be checked because one or both hashes are missing"
        )

    if capsule.commitment_hash != capsule.public_inputs_commitment_hash:
        return ValidationResult(
            ok=False,
            message=(
                "Commitment binding mismatch: "
                f"intent_data.commitment_hash={capsule.commitment_hash} "
                f"!= public_inputs.commitment_hash={capsule.public_inputs_commitment_hash}"
            )
        )

    return ValidationResult(ok=True, message="Commitment hashes match exactly")


# ----------------------------
# Phase 5 — Mock-aware signature placeholder
# ----------------------------

def verify_token_signature(
    payload: Optional[Dict[str, Any]],
    signature: Optional[str],
    issuer: Optional[str],
) -> SignatureStatus:
    """
    Signature verification.

    Rules:
    - If payload/issuer/signature missing, return NOT_PRESENT
    - Otherwise verify Ed25519 over RFC 8785 JCS canonical payload bytes
    """
    if not payload or not issuer:
        return SignatureStatus.NOT_PRESENT

    if not signature:
        return SignatureStatus.NOT_PRESENT

    try:
        public_key_hex = Path("keys/chora_token_public_key.hex").read_text().strip()
    except Exception:
        return SignatureStatus.INVALID

    if verify_payload_signature(payload, signature, public_key_hex):
        return SignatureStatus.VALID

    return SignatureStatus.INVALID


# ----------------------------
# Phase 4 — Token time window
# ----------------------------

def verify_token_window(capsule: NormalizedCapsule) -> ValidationResult:
    """
    Verify iat/exp are sane and token is currently within window.
    """
    iat = _parse_utc(capsule.iat)
    exp = _parse_utc(capsule.exp)
    if iat is None or exp is None:
        return ValidationResult(ok=False, message="Token timestamps are not parseable")

    if exp <= iat:
        return ValidationResult(ok=False, message="Token exp is not later than iat")

    now = datetime.now(timezone.utc)

    if now < iat:
        return ValidationResult(
            ok=False,
            message=f"Token not yet valid (now={now.isoformat()}, iat={iat.isoformat()})"
        )

    if now > exp:
        return ValidationResult(
            ok=False,
            message=f"Token expired (now={now.isoformat()}, exp={exp.isoformat()})"
        )

    return ValidationResult(ok=True, message="Token is currently within validity window")


# ----------------------------
# Phase 3 — Boundary decision adapter
# ----------------------------

def derive_boundary_state(
    capsule: NormalizedCapsule,
    structure_ok: bool,
    binding_ok: bool,
    token_window_ok: bool,
    signature_status: SignatureStatus,
) -> BoundaryStatus:
    """
    Derive CHORA boundary state from the capsule surface.

    Rules:
    - malformed => DENIED
    - HALT => DENIED
    - ESCALATE => PENDING
    - ALLOW + valid-ish shape + binding + token window + acceptable sig state => AUTHORIZED
    """
    if not structure_ok or not binding_ok:
        return BoundaryStatus.DENIED

    if capsule.outcome == Outcome.HALT.value:
        return BoundaryStatus.DENIED

    if capsule.outcome == Outcome.ESCALATE.value:
        return BoundaryStatus.PENDING

    if capsule.outcome == Outcome.ALLOW.value:
        if not token_window_ok:
            return BoundaryStatus.DENIED

        if signature_status == SignatureStatus.VALID:
            return BoundaryStatus.AUTHORIZED

        return BoundaryStatus.DENIED

    return BoundaryStatus.DENIED


# ----------------------------
# Phase 4 — Runtime boundary hook
# ----------------------------

def verify_boundary_crossing(path: str | Path) -> VerificationReport:
    """
    Full fail-closed boundary verification.
    """
    notes = []

    capsule = load_handshake_capsule(path)

    structure = validate_capsule_structure(capsule)
    if not structure.ok:
        return VerificationReport(
            structure=structure,
            commitment_binding=ValidationResult(False, "Not checked because structure failed"),
            token_window=ValidationResult(False, "Not checked because structure failed"),
            signature_status=SignatureStatus.NOT_PRESENT,
            boundary_status=BoundaryStatus.DENIED,
            notes=("Fail-closed: malformed capsule denies execution",),
        )

    commitment_binding = verify_commitment_binding(capsule)
    token_window = verify_token_window(capsule)
    signature_status = verify_token_signature(
        capsule.continuation_token_payload,
        capsule.continuation_token_signature,
        capsule.issuer,
    )

    boundary_status = derive_boundary_state(
        capsule=capsule,
        structure_ok=structure.ok,
        binding_ok=commitment_binding.ok,
        token_window_ok=token_window.ok,
        signature_status=signature_status,
    )

    if signature_status == SignatureStatus.INVALID:
        notes.append(
            "Signature is present but not cryptographically verified"
        )

    if boundary_status == BoundaryStatus.AUTHORIZED:
        notes.append("Boundary crossing is authorized under current adapter rules")
    elif boundary_status == BoundaryStatus.PENDING:
        notes.append("Boundary crossing is pending external resolution")
    else:
        notes.append("Boundary crossing is denied")

    return VerificationReport(
        structure=structure,
        commitment_binding=commitment_binding,
        token_window=token_window,
        signature_status=signature_status,
        boundary_status=boundary_status,
        notes=tuple(notes),
    )


# ----------------------------
# CLI
# ----------------------------

def _print_line(label: str, value: str) -> None:
    print(f"{label:<22} {value}")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python verify_handshake.py /path/to/capsule.json", file=sys.stderr)
        return 2

    path = argv[1]
    try:
        report = verify_boundary_crossing(path)
    except FileNotFoundError:
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"ERROR: unexpected failure: {exc}", file=sys.stderr)
        return 1

    _print_line("STRUCTURE:", "OK" if report.structure.ok else f"FAIL — {report.structure.message}")
    _print_line(
        "COMMITMENT BINDING:",
        "OK" if report.commitment_binding.ok else f"FAIL — {report.commitment_binding.message}"
    )
    _print_line(
        "TOKEN WINDOW:",
        "OK" if report.token_window.ok else f"FAIL — {report.token_window.message}"
    )
    _print_line("TOKEN SIGNATURE:", report.signature_status.value)
    _print_line("BOUNDARY STATUS:", report.boundary_status.value)

    if report.notes:
        print("\nNotes:")
        for note in report.notes:
            print(f" - {note}")

    # Exit non-zero unless authorized.
    return 0 if report.boundary_status == BoundaryStatus.AUTHORIZED else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
