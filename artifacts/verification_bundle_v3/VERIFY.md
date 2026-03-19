# CHORA v3 Verification Bundle

Signed object: token.payload

Canonicalization:
- JSON sorted keys
- separators (",", ":")
- UTF-8 encoding
- no whitespace

Signature:
- Ed25519
- hex encoded
- over canonical payload bytes

Nonce:
- string
- must match exactly (no coercion)

Expected SHA256:
<PASTE payload.sha256 HERE>
