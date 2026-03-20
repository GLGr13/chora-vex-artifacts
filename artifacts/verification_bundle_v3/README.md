# CHORA v3 Token Verification Bundle (RFC 8785 JCS)

Canonical verification bundle for CHORA continuation token contract v3.

## Contract

- Schema: `chora.continuation.token.v3`
- Canonicalization: `RFC8785-JCS`
- Signature algorithm: `Ed25519`
- Signed bytes: UTF-8 bytes of the JCS-canonicalized `payload` object

## Files

- `token.json` — current signed token artifact
- `reference_token.json` — canonical reference token artifact
- `public_key_token.pem` — public verification key
- `verify_node.mjs` — Node verifier
- `verify_python.py` — Python verifier
- `package.json` — Node package manifest
- `package-lock.json` — locked Node dependency manifest
- `VERIFY.md` — verification notes

## Node verification

```bash
npm install
node verify_node.mjs
