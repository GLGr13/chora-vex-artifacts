# CHORA Continuation Token — Contract v3

## Overview
Contract v3 defines a deterministic, cross-language verifiable continuation token.

The token is a signed canonical payload. Verification MUST succeed independently of implementation language.

---

## Components

### 1. Canonical Payload
File: `payload.canonical.json`

- UTF-8 encoded JSON
- Deterministic field ordering
- No extra whitespace or formatting variations
- Represents the exact signed content

---

### 2. Payload Hash
File: `payload.sha256`

- SHA-256 hash of `payload.canonical.json`
- Hex encoded
- MUST include trailing newline (`\n`)

---

### 3. Token
File: `token.json`

Contains:
- signature
- metadata (if any)
- reference to payload

Signature MUST be computed over the canonical payload bytes (not the hash, not a wrapper)

---

### 4. Public Key
File: `public_key_token.pem`

- Used for signature verification
- Verification MUST NOT require any private material

---

## Signing Rules

- Input: raw bytes of `payload.canonical.json`
- No transformations allowed before signing
- No re-serialization allowed during verification

---

## Verification Rules

A verifier MUST:

1. Read `payload.canonical.json` as bytes
2. Compute SHA-256 and match `payload.sha256`
3. Verify signature using `public_key_token.pem`
4. Return VALID only if all checks pass

---

## Determinism Requirements

- Same payload MUST always produce:
  - identical hash
  - identical signature
- Verification MUST succeed identically across implementations

---

## Versioning

- This is Contract Version: v3
- Any breaking change requires a new version (v4)

---

## Security Notes

- Do NOT modify payload after signing
- Do NOT sign non-canonical JSON
- Treat canonical payload as immutable

---

## Reference Implementation

See:
`artifacts/verification_bundle_v3/`

Includes:
- Python verifier
- Node verifier
- canonical payload
- signature
- public key

---

## Status

- Locked and tagged: `v3-verification-bundle-locked`
- Canonical commit: `6975c1e`
