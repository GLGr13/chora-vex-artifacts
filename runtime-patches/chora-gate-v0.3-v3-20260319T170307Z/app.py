import os
import json
import time
from fastapi import FastAPI, Header, HTTPException
import base64
import hashlib
import secrets
import subprocess
import shutil
import threading
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from phase3_mcs.mcs_engine import MCSEngine, simulate_mcs_gate_bridge

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization

APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.getenv("CHORA_LOG_DIR", os.path.join(APP_DIR, "logs"))
KEY_DIR = os.getenv("CHORA_KEY_DIR", os.path.join(APP_DIR, "keys"))
ENV_PATH = os.getenv("CHORA_ENV_PATH", os.path.join(APP_DIR, ".env"))

load_dotenv(ENV_PATH)

CHORA_API_KEY = (os.getenv("CHORA_API_KEY", "") or "").strip()
QUINTEN_API_KEY = (os.getenv("QUINTEN_API_KEY", "") or "").strip()
CHORA_CONF_THRESHOLD = float(os.getenv("CHORA_CONF_THRESHOLD", "0.90"))
CHORA_ENABLE_OTS = os.getenv("CHORA_ENABLE_OTS", "1") == "1"
CHORA_PUBLIC_BASE = os.getenv("CHORA_PUBLIC_BASE", "").rstrip("/")
CHORA_OTS_BIN = os.getenv("CHORA_OTS_BIN", "/opt/chora-venv/bin/ots")
CHORA_RULE_SET_OWNER = (os.getenv("CHORA_RULE_SET_OWNER", "CHORA") or "").strip()
CHORA_RULE_SET_VERSION = (os.getenv("CHORA_RULE_SET_VERSION", "v139.6.3") or "").strip()
CHORA_GATE_OPERATOR = (os.getenv("CHORA_GATE_OPERATOR", "chora-vps-1") or "").strip()
CHORA_WITNESS_MODE = (os.getenv("CHORA_WITNESS_MODE", "attached") or "").strip()
CHORA_SENTINEL_MODE = (os.getenv("CHORA_SENTINEL_MODE", "observe_only") or "").strip()
CHORA_CUSTODY_MODE = (os.getenv("CHORA_CUSTODY_MODE", "external_non_bypass") or "").strip()
CHORA_FAIL_CLOSED = os.getenv("CHORA_FAIL_CLOSED", "1") == "1"
CHORA_REQUIRE_AUTHORITY_DECLARATION = os.getenv("CHORA_REQUIRE_AUTHORITY_DECLARATION", "1") == "1"
CHORA_ENABLE_ESCALATE = os.getenv("CHORA_ENABLE_ESCALATE", "1") == "1"
CHORA_APPEND_AUDIT = os.getenv("CHORA_APPEND_AUDIT", "1") == "1"
CHORA_ENABLE_REPLAY_PROTECTION = os.getenv("CHORA_ENABLE_REPLAY_PROTECTION", "1") == "1"
CHORA_REPLAY_WINDOW_SEC = int(os.getenv("CHORA_REPLAY_WINDOW_SEC", "900"))
CHORA_MAX_CLOCK_SKEW_SEC = int(os.getenv("CHORA_MAX_CLOCK_SKEW_SEC", "300"))
CHORA_ENABLE_ESCALATION_QUEUE = os.getenv("CHORA_ENABLE_ESCALATION_QUEUE", "1") == "1"
CHORA_CAPSULE_SPEC_VERSION = (os.getenv("CHORA_CAPSULE_SPEC_VERSION", "0.3") or "").strip()
CHORA_IDENTITY_MODE = (os.getenv("CHORA_IDENTITY_MODE", "unbound") or "").strip()
CHORA_PCR_BANK = (os.getenv("CHORA_PCR_BANK", "sha256") or "").strip()
CHORA_ENABLE_REQUEST_COMMITMENT = os.getenv("CHORA_ENABLE_REQUEST_COMMITMENT", "1") == "1"
CHORA_ENABLE_PCR_IDENTITY = os.getenv("CHORA_ENABLE_PCR_IDENTITY", "0") == "1"

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(KEY_DIR, exist_ok=True)

ESCALATION_DIR = os.path.join(LOG_DIR, "escalations")
os.makedirs(ESCALATION_DIR, exist_ok=True)

_seen_request_shas: Dict[str, float] = {}
_seen_nonces: Dict[str, float] = {}
_cache_lock = threading.Lock()

PRIV_PATH = os.path.join(KEY_DIR, "ed25519_private.pem")
PUB_PATH = os.path.join(KEY_DIR, "ed25519_public.pem")
TOKEN_PUB_PATH = os.path.join(KEY_DIR, "chora_ed25519_public.pem")

SERVICE_VERSION = "chora-capsule-v1-merkle-v0.3-dev"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stable_json(obj: Any) -> bytes:
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def jcs_sha256(obj: Any) -> str:
    return sha256_hex(stable_json(obj))


def ensure_keys() -> None:
    if os.path.exists(PRIV_PATH) and os.path.exists(PUB_PATH):
        return

    priv = Ed25519PrivateKey.generate()
    priv_pem = priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pub_pem = priv.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    with open(PRIV_PATH, "wb") as f:
        f.write(priv_pem)
    os.chmod(PRIV_PATH, 0o600)

    with open(PUB_PATH, "wb") as f:
        f.write(pub_pem)
    os.chmod(PUB_PATH, 0o644)


def load_private_key() -> Ed25519PrivateKey:
    ensure_keys()
    with open(PRIV_PATH, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def load_public_key() -> Ed25519PublicKey:
    ensure_keys()
    with open(PUB_PATH, "rb") as f:
        return serialization.load_pem_public_key(f.read())


def load_public_key_pem() -> str:
    ensure_keys()
    with open(PUB_PATH, "rb") as f:
        return f.read().decode("utf-8")

def load_token_public_key_pem() -> str:
    with open(TOKEN_PUB_PATH, "rb") as f:
        return f.read().decode("utf-8")

def sign_bytes(data: bytes) -> str:
    sig = load_private_key().sign(data)
    return base64.b64encode(sig).decode("utf-8")


def verify_sig(data: bytes, sig_b64: str) -> bool:
    try:
        sig = base64.b64decode(sig_b64.encode("utf-8"))
        load_public_key().verify(sig, data)
        return True
    except Exception:
        return False


def compute_capsule_root(
    intent_hash: str,
    authority_hash: str,
    identity_hash: str,
    witness_hash: str,
) -> tuple[str, bytes]:
    h_intent = bytes.fromhex(intent_hash)
    h_auth = bytes.fromhex(authority_hash)
    h_ident = bytes.fromhex(identity_hash)
    h_witness = bytes.fromhex(witness_hash)

    h12 = hashlib.sha256(b"\x01" + h_intent + h_auth).digest()
    h34 = hashlib.sha256(b"\x01" + h_ident + h_witness).digest()
    root_bytes = hashlib.sha256(b"\x01" + h12 + h34).digest()

    return root_bytes.hex(), root_bytes


def capsule_paths(capsule_id: str) -> tuple[str, str]:
    json_path = os.path.join(LOG_DIR, f"{capsule_id}.json")
    ots_path = os.path.join(LOG_DIR, f"{capsule_id}.json.ots")
    return json_path, ots_path


def _update_capsule_ots_status(capsule_id: str, status: Dict[str, Any]) -> None:
    json_path, _ = capsule_paths(capsule_id)
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        data["ots"] = status

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def try_ots_stamp_async(capsule_id: str) -> None:
    if not CHORA_ENABLE_OTS:
        return

    json_path, ots_path = capsule_paths(capsule_id)

    try:
        ots_bin = CHORA_OTS_BIN
        proc = subprocess.run(
            [ots_bin, "stamp", json_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=120,
        )

        maybe = json_path + ".ots"
        if os.path.exists(maybe) and maybe != ots_path:
            os.replace(maybe, ots_path)

        receipt_hash = None
        if os.path.exists(ots_path):
            with open(ots_path, "rb") as f:
                receipt_hash = hashlib.sha256(f.read()).hexdigest()

        _update_capsule_ots_status(
            capsule_id,
            {
                "enabled": True,
                "receipt_present": os.path.exists(ots_path),
                "receipt_hash": receipt_hash,
                "ts_utc": utc_now(),
                "stdout": proc.stdout[-2000:],
                "stderr": proc.stderr[-2000:],
            },
        )

    except Exception as exc:
        _update_capsule_ots_status(
            capsule_id,
            {
                "enabled": True,
                "receipt_present": False,
                "receipt_hash": None,
                "ts_utc": utc_now(),
                "error": repr(exc),
            },
        )


def append_audit_line(capsule: Dict[str, Any]) -> None:
    if not CHORA_APPEND_AUDIT:
        return
    audit_path = os.path.join(LOG_DIR, "capsule_audit.jsonl")
    line_obj = {
        "ts_utc": capsule.get("ts_utc"),
        "capsule_id": capsule.get("capsule_id"),
        "outcome": capsule.get("authority", {}).get("outcome"),
        "reason_code": capsule.get("authority", {}).get("reason_code"),
        "capsule_root": capsule.get("capsule_root"),
        "operator": capsule.get("policy", {}).get("operator"),
        "rule_set_version": capsule.get("policy", {}).get("rule_set_version"),
    }
    with open(audit_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(line_obj, ensure_ascii=False, sort_keys=True) + "\n")


def make_links(capsule_id: str) -> Dict[str, str]:
    prefix = CHORA_PUBLIC_BASE if CHORA_PUBLIC_BASE else ""
    return {
        "capsule": f"{prefix}/capsules/{capsule_id}",
        "json": f"{prefix}/capsules/{capsule_id}/json",
        "ots": f"{prefix}/capsules/{capsule_id}/ots",
        "verify": f"{prefix}/capsules/{capsule_id}/verify",
        "index": f"{prefix}/capsules",
        "public_key": f"{prefix}/public_key",
    }




def parse_meta_timestamp(meta: Dict[str, Any]) -> Optional[float]:
    raw = meta.get("timestamp") or meta.get("ts_utc")
    if not raw:
        return None
    try:
        if isinstance(raw, (int, float)):
            return float(raw)
        if isinstance(raw, str):
            s = raw.replace("Z", "+00:00")
            return datetime.fromisoformat(s).timestamp()
    except Exception:
        return None
    return None


def cleanup_seen(now_ts: float) -> None:
    cutoff = now_ts - CHORA_REPLAY_WINDOW_SEC
    with _cache_lock:
        for store in (_seen_request_shas, _seen_nonces):
            expired = [k for k, v in store.items() if v < cutoff]
            for k in expired:
                del store[k]


def replay_check(request_sha: str, nonce: int, req_meta: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if not CHORA_ENABLE_REPLAY_PROTECTION:
        return errors

    now_ts = time.time()
    cleanup_seen(now_ts)

    req_ts = parse_meta_timestamp(req_meta)
    if req_ts is not None and abs(now_ts - req_ts) > CHORA_MAX_CLOCK_SKEW_SEC:
        errors.append("REQUEST_TIMESTAMP_OUT_OF_WINDOW")

    with _cache_lock:
        if request_sha in _seen_request_shas:
            errors.append("REQUEST_REPLAY_DETECTED")
        if str(nonce) in _seen_nonces:
            errors.append("NONCE_REPLAY_DETECTED")

        if not errors:
            _seen_request_shas[request_sha] = now_ts
            _seen_nonces[str(nonce)] = now_ts

    return errors


def append_escalation_record(capsule: Dict[str, Any]) -> None:
    if not CHORA_ENABLE_ESCALATION_QUEUE:
        return
    if capsule.get("authority", {}).get("outcome") != "ESCALATE":
        return

    path = os.path.join(ESCALATION_DIR, f"{capsule['capsule_id']}.json")
    record = {
        "capsule_id": capsule["capsule_id"],
        "ts_utc": capsule.get("ts_utc"),
        "aid": capsule.get("identity", {}).get("aid", ""),
        "reason_code": capsule.get("authority", {}).get("reason_code", ""),
        "status": "PENDING_REVIEW",
        "capsule_root": capsule.get("capsule_root", ""),
        "links": capsule.get("links", {}),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)


app = FastAPI(title="CHORA Gate (FastAPI)", version=SERVICE_VERSION)


class AuthorityDecl(BaseModel):
    rule_set_owner: str
    rule_set_version: str
    gate_operator: str
    witness_mode: str


class GateRequest(BaseModel):
    confidence: float = Field(..., ge=0.0, le=1.0)
    capabilities: List[str] = Field(default_factory=list)
    meta: Dict[str, Any] = Field(default_factory=dict)
    authority: Optional[AuthorityDecl] = None


VALID_API_KEYS = {CHORA_API_KEY, QUINTEN_API_KEY}


def check_api_key(x_api_key: Optional[str]) -> str:
    key = (x_api_key or "").strip()
    if key == CHORA_API_KEY:
        return "chora"
    if key == QUINTEN_API_KEY:
        return "quinten"
    raise HTTPException(status_code=401, detail="Invalid API key")


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"ok": True, "service_version": SERVICE_VERSION, "ts_utc": utc_now()}


@app.get("/public_key", response_class=PlainTextResponse)
def public_key() -> str:
    return load_public_key_pem()

@app.get("/public_key_token", response_class=PlainTextResponse)
def public_key_token() -> str:
    return load_token_public_key_pem()

@app.post("/gate")
def gate(
    req: GateRequest,
    x_api_key: Optional[str] = Header(default=None, alias="X-API-Key")
) -> JSONResponse:
    operator = check_api_key(x_api_key)
    ts = utc_now()

    configuration_errors: List[str] = []
    if not (0.0 <= CHORA_CONF_THRESHOLD <= 1.0):
        configuration_errors.append("CHORA_CONF_THRESHOLD_OUT_OF_RANGE")
    if not CHORA_RULE_SET_OWNER:
        configuration_errors.append("RULE_SET_OWNER_MISSING")
    if not CHORA_RULE_SET_VERSION:
        configuration_errors.append("RULE_SET_VERSION_MISSING")
    if not CHORA_GATE_OPERATOR:
        configuration_errors.append("GATE_OPERATOR_MISSING")
    if not CHORA_WITNESS_MODE:
        configuration_errors.append("WITNESS_MODE_MISSING")
    if CHORA_SENTINEL_MODE != "observe_only":
        configuration_errors.append("SENTINEL_MODE_INVALID")
    if CHORA_CUSTODY_MODE != "external_non_bypass":
        configuration_errors.append("CUSTODY_MODE_INVALID")

    authority_declared = (
        bool(CHORA_RULE_SET_OWNER)
        and bool(CHORA_RULE_SET_VERSION)
        and bool(CHORA_GATE_OPERATOR)
        and bool(CHORA_WITNESS_MODE)
        and CHORA_SENTINEL_MODE == "observe_only"
        and CHORA_CUSTODY_MODE == "external_non_bypass"
    )

    if CHORA_REQUIRE_AUTHORITY_DECLARATION and not authority_declared:
        configuration_errors.append("AUTHORITY_DECLARATION_MISSING")

    request_authority = req.authority.dict() if req.authority else None
    authority_match_errors: List[str] = []
    if request_authority is not None:
        if request_authority.get("rule_set_owner") != CHORA_RULE_SET_OWNER:
            authority_match_errors.append("REQUEST_RULE_SET_OWNER_MISMATCH")
        if request_authority.get("rule_set_version") != CHORA_RULE_SET_VERSION:
            authority_match_errors.append("REQUEST_RULE_SET_VERSION_MISMATCH")
        if request_authority.get("gate_operator") != CHORA_GATE_OPERATOR:
            authority_match_errors.append("REQUEST_GATE_OPERATOR_MISMATCH")
        if request_authority.get("witness_mode") != CHORA_WITNESS_MODE:
            authority_match_errors.append("REQUEST_WITNESS_MODE_MISMATCH")

    has_network = any(c.lower() == "network" for c in req.capabilities)
    review_requested = bool(req.meta.get("escalate")) or bool(req.meta.get("review_required"))

    request_obj = {
        "confidence": req.confidence,
        "capabilities": req.capabilities,
        "meta": req.meta,
        "authority": request_authority,
    }
    request_sha = sha256_hex(stable_json(request_obj))
    request_commitment = None
    if CHORA_ENABLE_REQUEST_COMMITMENT:
        request_commitment = {
            "canonicalization": "JCS-RFC8785",
            "payload_sha256": request_sha,
            "payload_encoding": "application/json",
        }
    incoming_nonce = int(req.meta.get("nonce", secrets.randbits(64)))
    replay_errors = replay_check(request_sha, incoming_nonce, req.meta)

    if configuration_errors and CHORA_FAIL_CLOSED:
        outcome = "HALT"
        reason_code = "CONFIGURATION_INVALID"
        rule = "Fail-closed configuration invalid => HALT"
    elif authority_match_errors and CHORA_FAIL_CLOSED:
        outcome = "HALT"
        reason_code = authority_match_errors[0]
        rule = f"{authority_match_errors[0]} => HALT"
    elif replay_errors and CHORA_FAIL_CLOSED:
        outcome = "HALT"
        reason_code = replay_errors[0]
        rule = f"{replay_errors[0]} => HALT"
    elif review_requested and CHORA_ENABLE_ESCALATE:
        outcome = "ESCALATE"
        reason_code = "REVIEW_REQUIRED"
        rule = "review_requested => ESCALATE"
    elif has_network and req.confidence < CHORA_CONF_THRESHOLD:
        outcome = "HALT"
        reason_code = "CAPABILITY_NETWORK_LOW_CONFIDENCE"
        rule = f"Network && confidence < {CHORA_CONF_THRESHOLD} => HALT"
    else:
        outcome = "ALLOW"
        reason_code = "WITHIN_POLICY"
        rule = "Otherwise => ALLOW"

    capsule_id = str(uuid.uuid4())

    intent = {
        "request_sha256": request_sha,
        "confidence": req.confidence,
        "capabilities": req.capabilities,
    }

    trace_root = request_sha
   

    default_aid = sha256_hex(CHORA_GATE_OPERATOR.encode("utf-8"))
    identity = {
        "aid": req.meta.get("aid", default_aid),
        "identity_type": CHORA_IDENTITY_MODE,
        "pcrs": req.meta.get("pcrs", {}),
    }

    if CHORA_ENABLE_PCR_IDENTITY and CHORA_IDENTITY_MODE == "tpm_attested":
        identity.update({
            "pcr_bank": CHORA_PCR_BANK,
            "attestation_mode": "pcr_bound",
        })

    committed_witness = {
        "chora_node_id": CHORA_GATE_OPERATOR,
        "timestamp": int(datetime.now(timezone.utc).timestamp()),
    }

    intent_hash = jcs_sha256(intent)
    authority = {
        "capsule_id": capsule_id,
        "outcome": outcome,
        "reason_code": reason_code,
        "trace_root": trace_root,
        "nonce": incoming_nonce,
        "rule_set_owner": CHORA_RULE_SET_OWNER,
        "rule_set_version": CHORA_RULE_SET_VERSION,
        "gate_operator": CHORA_GATE_OPERATOR,
        "authority_declared": authority_declared,
        "fail_closed": CHORA_FAIL_CLOSED,
        "custody_mode": CHORA_CUSTODY_MODE,
}

    authority_hash = jcs_sha256(authority)
    identity_hash = jcs_sha256(identity)
    witness_hash = jcs_sha256(committed_witness)

    capsule_root, capsule_root_bytes = compute_capsule_root(
        intent_hash,
        authority_hash,
        identity_hash,
        witness_hash,
    )
    signature_b64 = sign_bytes(bytes.fromhex(capsule_root))
    sig_bytes = base64.b64decode(signature_b64.encode("utf-8"))
    receipt_hash = sha256_hex(sig_bytes)

    witness = {
        **committed_witness,
        "receipt_hash": receipt_hash,
        "witness_mode": CHORA_WITNESS_MODE,
        "sentinel_mode": CHORA_SENTINEL_MODE,
        "observational_only": CHORA_SENTINEL_MODE == "observe_only",
    }

    # --- MCS SHADOW EVALUATION ---
    try:
        mcs_engine = MCSEngine()
        mcs_input = {
            "confidence": req.confidence,
            "capabilities": req.capabilities,
            "meta": req.meta,
        }
        mcs_result = mcs_engine.evaluate(mcs_input)
        mcs_bridge = simulate_mcs_gate_bridge(mcs_result, outcome)
    except Exception as e:
        mcs_result = {"error": str(e)}
        mcs_bridge = {"error": "bridge_failed"}

    # --- MCS BINDING OVERRIDE (Phase 3 Binding Patch 1) ---
    mcs_status = mcs_result.get("mcs_status")

    if mcs_status == "MCS_FAIL":
        outcome = "HALT"
        reason_code = "MCS_FAIL_BINDING"
        authority["outcome"] = outcome
        authority["reason_code"] = reason_code

    elif mcs_status == "MCS_ESCALATE":
        outcome = "ESCALATE"
        reason_code = "MCS_ESCALATE_BINDING"
        authority["outcome"] = outcome
        authority["reason_code"] = reason_code

    authority_hash = jcs_sha256(authority)
    capsule_root, capsule_root_bytes = compute_capsule_root(
        intent_hash,
        authority_hash,
        identity_hash,
        witness_hash,
    )
    signature_b64 = sign_bytes(bytes.fromhex(capsule_root))
    sig_bytes = base64.b64decode(signature_b64.encode("utf-8"))
    receipt_hash = sha256_hex(sig_bytes)
    witness["receipt_hash"] = receipt_hash

    capsule = {
        "capsule_spec_version": CHORA_CAPSULE_SPEC_VERSION,
        "capsule_id": capsule_id,
        "intent": intent,
        "authority": authority,
        "identity": identity,
        "witness": witness,
        "intent_hash": intent_hash,
        "authority_hash": authority_hash,
        "identity_hash": identity_hash,
        "witness_hash": witness_hash,
        "capsule_root": capsule_root,
        "crypto": {
            "algo": "ed25519",
            "public_key_endpoint": "/public_key",
            "signature_scope": "capsule_root",
            "signature_b64": signature_b64,
        },
        "policy": {
            "operator": operator,
            "rule": rule,
            "conf_threshold": CHORA_CONF_THRESHOLD,
            "rule_set_owner": CHORA_RULE_SET_OWNER,
            "rule_set_version": CHORA_RULE_SET_VERSION,
            "gate_operator": CHORA_GATE_OPERATOR,
            "fail_closed": CHORA_FAIL_CLOSED,
            "require_authority_declaration": CHORA_REQUIRE_AUTHORITY_DECLARATION,
            "configuration_valid": len(configuration_errors) == 0,
            "configuration_errors": configuration_errors + authority_match_errors + replay_errors,
        },
        "sentinel": {
            "mode": CHORA_SENTINEL_MODE,
            "observational_only": True,
            "status": "WATCH",
        },
        "mcs": mcs_result,
        "mcs_bridge": mcs_bridge,
        "custody": {
            "mode": CHORA_CUSTODY_MODE,
            "continuation_requires_gate_record": True,
            "bypass_permitted": False,
        },
        "ots": {
            "enabled": CHORA_ENABLE_OTS,
            "receipt_present": False,
            "note": "Stamping is best-effort and may complete shortly after /gate returns.",
        },
        "links": make_links(capsule_id),
        "request_commitment": request_commitment,
        "service_version": SERVICE_VERSION,
        "ts_utc": ts,
    }

    json_path, _ = capsule_paths(capsule_id)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(capsule, f, ensure_ascii=False, indent=2)

    append_audit_line(capsule)
    append_escalation_record(capsule)
    threading.Thread(target=try_ots_stamp_async, args=(capsule_id,), daemon=True).start()
    return JSONResponse(capsule)


@app.get("/capsules")
def capsules() -> Dict[str, Any]:
    files = [f for f in os.listdir(LOG_DIR) if f.endswith(".json")]
    files.sort(reverse=True)
    ids = [f[:-5] for f in files[:300]]
    return {"count": len(ids), "capsules": ids}


def load_capsule(capsule_id: str) -> Dict[str, Any]:
    json_path, _ = capsule_paths(capsule_id)
    if not os.path.exists(json_path):
        raise HTTPException(status_code=404, detail="Capsule not found")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/capsules/{capsule_id}")
def get_capsule(capsule_id: str) -> Dict[str, Any]:
    return load_capsule(capsule_id)


@app.get("/capsules/{capsule_id}/json")
def get_capsule_json(capsule_id: str) -> Dict[str, Any]:
    return load_capsule(capsule_id)


@app.get("/capsules/{capsule_id}/ots")
def get_capsule_ots(capsule_id: str) -> Dict[str, Any]:
    _, ots_path = capsule_paths(capsule_id)
    if not os.path.exists(ots_path):
        raise HTTPException(status_code=404, detail="OTS receipt not found (yet).")
    with open(ots_path, "rb") as f:
        raw = f.read()
    return {"capsule_id": capsule_id, "ots_b64": base64.b64encode(raw).decode("utf-8")}


@app.get("/capsules/{capsule_id}/verify")
def verify(capsule_id: str) -> Dict[str, Any]:
    cap = load_capsule(capsule_id)
    capsule_root = cap.get("capsule_root", "")
    crypto = cap.get("crypto", {})
    sig_b64 = crypto.get("signature_b64", "")
    scope = crypto.get("signature_scope", "")

    root_ok = bool(capsule_root) and scope == "capsule_root"
    sig_ok = False
    if root_ok and sig_b64:
        sig_ok = verify_sig(bytes.fromhex(capsule_root), sig_b64)

    recomputed_intent_hash = jcs_sha256(cap.get("intent", {}))
    recomputed_authority_hash = jcs_sha256(cap.get("authority", {}))
    recomputed_identity_hash = jcs_sha256(cap.get("identity", {}))
    stored_witness = cap.get("witness", {}) or {}
    committed_witness = {
        "chora_node_id": stored_witness.get("chora_node_id", ""),
        "timestamp": stored_witness.get("timestamp"),
    }
    recomputed_witness_hash = jcs_sha256(committed_witness)
    recomputed_capsule_root, _ = compute_capsule_root(
        recomputed_intent_hash,
        recomputed_authority_hash,
        recomputed_identity_hash,
        recomputed_witness_hash,
    )

    return {
        "capsule_id": capsule_id,
        "signature_scope": scope,
        "capsule_root": {
            "computed": recomputed_capsule_root,
            "expected": capsule_root,
            "ok": recomputed_capsule_root == capsule_root,
        },
        "hashes": {
            "intent": {
                "computed": recomputed_intent_hash,
                "expected": cap.get("intent_hash", ""),
                "ok": recomputed_intent_hash == cap.get("intent_hash", ""),
            },
            "authority": {
                "computed": recomputed_authority_hash,
                "expected": cap.get("authority_hash", ""),
                "ok": recomputed_authority_hash == cap.get("authority_hash", ""),
            },
            "identity": {
                "computed": recomputed_identity_hash,
                "expected": cap.get("identity_hash", ""),
                "ok": recomputed_identity_hash == cap.get("identity_hash", ""),
            },
            "witness": {
                "computed": recomputed_witness_hash,
                "expected": cap.get("witness_hash", ""),
                "ok": recomputed_witness_hash == cap.get("witness_hash", ""),
            },
        },
        "signature": {
            "ok": sig_ok,
            "algo": crypto.get("algo", "ed25519"),
            "public_key_endpoint": crypto.get("public_key_endpoint", "/public_key"),
        },
        "ots": cap.get("ots", {}),
        "links": cap.get("links", {}),
        "service_version": cap.get("service_version", SERVICE_VERSION),
        "ts_utc": utc_now(),
    }

@app.post("/execute")
def execute(payload: Dict[str, Any]) -> Dict[str, Any]:
    if "token" not in payload or "nonce" not in payload or "command" not in payload:
        raise HTTPException(status_code=400, detail="missing fields")

    token_path = f"/tmp/chora_exec_token_{uuid.uuid4().hex}.json"
    with open(token_path, "w", encoding="utf-8") as f:
        json.dump(payload["token"], f, ensure_ascii=False)

    try:
        result = subprocess.run(
            ["python3", "/opt/chora-gate-v0.3/ems/enforce_continuation.py", token_path, str(payload["nonce"])],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return {
                "status": "DENIED",
                "reason": (result.stdout.strip() or result.stderr.strip())
            }

        exec_result = subprocess.run(
            payload["command"],
            capture_output=True,
            text=True,
        )

        return {
            "status": "EXECUTED",
            "stdout": exec_result.stdout,
            "stderr": exec_result.stderr,
            "returncode": exec_result.returncode,
        }
    finally:
        try:
            os.remove(token_path)
        except Exception:
            pass
