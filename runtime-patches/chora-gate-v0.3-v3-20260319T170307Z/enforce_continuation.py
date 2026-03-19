#!/usr/bin/env python3
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timezone


TOKEN_PUBKEY = "/opt/chora-gate-v0.3/keys/chora_ed25519_public.pem"


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def verify_signature(payload_str, signature_hex):
    sig_path = Path("/tmp/chora_sig.bin")
    payload_path = Path("/tmp/chora_payload.json")

    payload_path.write_text(payload_str, encoding="utf-8")
    sig_path.write_bytes(bytes.fromhex(signature_hex))

    result = subprocess.run([
        "openssl", "pkeyutl",
        "-verify",
        "-pubin",
        "-inkey", TOKEN_PUBKEY,
        "-rawin",
        "-in", str(payload_path),
        "-sigfile", str(sig_path)
    ], capture_output=True)

    return result.returncode == 0


def main():
    if len(sys.argv) < 3:
        print("usage: enforce_continuation.py <token.json> <expected_nonce>", file=sys.stderr)
        sys.exit(1)

    token_path = Path(sys.argv[1])
    expected_nonce = str(sys.argv[2])

    if not token_path.exists():
        print("DENY: token not found")
        sys.exit(2)

    token = json.loads(token_path.read_text(encoding="utf-8"))
    payload = token["payload"]
    signature = token["signature"]

    required = [
        "schema",
        "issuer",
        "iat",
        "exp",
        "ledger_event_id",
        "resolution_event_id",
        "source_capsule_root",
        "nonce",
    ]
    missing = [k for k in required if k not in payload]
    if missing:
        print(f"DENY: missing required fields: {','.join(missing)}")
        sys.exit(3)

    if payload["schema"] != "chora.continuation.token.v3":
        print("DENY: unsupported token schema")
        sys.exit(4)

    payload_str = canonical(payload)
    if not verify_signature(payload_str, signature):
        print("DENY: invalid signature")
        sys.exit(5)

    now = datetime.now(timezone.utc)
    exp = datetime.fromisoformat(payload["exp"])
    if now > exp:
        print("DENY: token expired")
        sys.exit(6)

    if str(payload["nonce"]) != expected_nonce:
        print("DENY: nonce mismatch")
        sys.exit(7)

    print("ALLOW: continuation authorized")
    sys.exit(0)


if __name__ == "__main__":
    main()
