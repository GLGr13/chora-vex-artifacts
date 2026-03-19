#!/usr/bin/env python3
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta


TOKEN_PRIVKEY = "/opt/chora-gate-v0.3/keys/chora_ed25519_private.pem"


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def main():
    if len(sys.argv) < 2:
        print("usage: generate_signed_token.py <ledger_event_id> [nonce]", file=sys.stderr)
        sys.exit(1)

    ledger_event_id = sys.argv[1]
    nonce = sys.argv[2] if len(sys.argv) > 2 else "default-nonce"
    nonce = str(nonce)

    ems_path = Path(f"/opt/chora-gate-v0.3/ems/ems_{ledger_event_id}.json")
    if not ems_path.exists():
        print("EMS record not found", file=sys.stderr)
        sys.exit(2)

    with ems_path.open("r", encoding="utf-8") as f:
        ems = json.load(f)

    if not ems.get("continuation_authorized"):
        print("continuation not authorized", file=sys.stderr)
        sys.exit(3)

    if not ems.get("resolution_event_id"):
        print("resolution_event_id missing", file=sys.stderr)
        sys.exit(4)

    now = datetime.now(timezone.utc)
    payload = {
        "schema": "chora.continuation.token.v3",
        "issuer": "chora-gate-v0.3",
        "iat": now.isoformat(),
        "exp": (now + timedelta(minutes=10)).isoformat(),
        "ledger_event_id": ems["ledger_event_id"],
        "resolution_event_id": ems["resolution_event_id"],
        "source_capsule_root": ems["source_capsule_root"],
        "nonce": nonce,
    }

    payload_str = canonical(payload)
    payload_bytes = payload_str.encode("utf-8")

    tmp_payload = Path("/tmp/chora_token_payload_v3.json")
    tmp_sig = Path("/tmp/chora_token_sig_v3.bin")

    tmp_payload.write_bytes(payload_bytes)

    subprocess.run([
        "openssl", "pkeyutl",
        "-sign",
        "-inkey", TOKEN_PRIVKEY,
        "-rawin",
        "-in", str(tmp_payload),
        "-out", str(tmp_sig)
    ], check=True)

    signature_hex = tmp_sig.read_bytes().hex()

    token = {
        "payload": payload,
        "signature": signature_hex,
        "meta": {
            "signature_scope": "payload",
            "canonicalization": "json.sort_keys,separators,no_pretty,no_ascii_escape",
            "canonical_bytes_encoding": "utf-8",
            "public_key_endpoint": "/public_key_token",
            "schema_version": "v3"
        }
    }

    out_path = Path(f"/opt/chora-gate-v0.3/ems/token_{ledger_event_id}.json")
    out_path.write_text(json.dumps(token, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps({
        "written": str(out_path),
        "schema": payload["schema"],
        "expires_at": payload["exp"],
        "public_key_endpoint": "/public_key_token"
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
