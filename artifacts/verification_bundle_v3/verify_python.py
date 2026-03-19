import json, base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

token = json.loads(Path("token.json").read_text())
payload = token["payload"]
sig_hex = token["signature"]

canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

pub = serialization.load_pem_public_key(Path("public_key_token.pem").read_bytes())

try:
    pub.verify(bytes.fromhex(sig_hex), canonical)
    print("PYTHON: SIGNATURE VALID")
except Exception as e:
    print("PYTHON: SIGNATURE INVALID", e)
