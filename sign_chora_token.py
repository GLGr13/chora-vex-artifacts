from __future__ import annotations
import json
import sys
from pathlib import Path
from nacl.signing import SigningKey
import rfc8785

def canonical_bytes(obj):
    out = rfc8785.dumps(obj)
    return out.encode("utf-8") if isinstance(out, str) else out

def main():
    if len(sys.argv) != 3:
        print("Usage: python sign_chora_token.py payload.json output.json")
        raise SystemExit(2)

    payload_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    payload = json.loads(payload_path.read_text())
    sk_hex = Path("keys/chora_token_signing_key.hex").read_text().strip()
    sk = SigningKey(bytes.fromhex(sk_hex))

    msg = canonical_bytes(payload)
    sig_hex = sk.sign(msg).signature.hex()

    out = {
        "payload": payload,
        "signature": sig_hex,
    }
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()
