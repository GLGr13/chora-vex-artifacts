# CHORA Verification Bundle

A full payload-signed token verification bundle will be published here.

Target bundle contents:

- payload.json
- payload.jcs.json
- signature.b64
- public_key.pem
- verify.py

Verification contract:

payload
→ RFC 8785 JCS canonical bytes
→ Ed25519 signature
→ deterministic verification
