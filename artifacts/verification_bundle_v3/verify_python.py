import json
import jcs
from pathlib import Path
from cryptography.hazmat.primitives.serialization import load_pem_public_key

token = json.loads(Path("token.json").read_text(encoding="utf-8"))
payload = token["payload"]
sig = bytes.fromhex(token["signature"])

payload_bytes = jcs.canonicalize(payload)
pub = load_pem_public_key(Path("public_key_token.pem").read_bytes())
pub.verify(sig, payload_bytes)

print("PYTHON: SIGNATURE VALID")
