# CHORA Token Verification Contract v0.3

This document defines the minimal contract required for deterministic cross-system verification of a CHORA continuation token.

It is intentionally narrow.
It does not define the full CHORA runtime.
It defines only the rules required to verify one token artifact reproducibly across systems.

## Scope

This contract applies to the token verification bundle associated with this document.

The goal is strict determinism:

same token payload  
→ same canonical bytes  
→ same signature input  
→ same verification result

## 1. Verification Object

The verification object is the token payload itself after canonicalization.

Bundle files:

- `token_payload.json` = human-readable token payload
- `token_jcs.json` = exact canonical serialized token payload
- `token_signature.b64` = detached signature
- `public_key.pem` = verification key
- `expected_result.json` = expected verification outcome

## 2. Canonicalization

Canonicalization rules:

- RFC 8785 (JCS)
- UTF-8 encoding
- deterministic canonical JSON
- keys sorted as required by JCS
- no insignificant whitespace
- arrays preserved in emitted order
- numbers preserved according to RFC 8785 rules

The canonical verification input is the exact UTF-8 byte sequence of `token_jcs.json`.

## 3. Signed Fields

The signed object consists only of the fields present in the canonical token payload.

Rules:

- fields present in `token_jcs.json` are part of the signed object
- absent optional fields are omitted entirely
- omitted fields are not represented as null unless explicitly present in the emitted token
- external transport metadata is not part of the signed object
- file names are not part of the signed object

## 4. Signature Input

Signature input is:

- the raw UTF-8 bytes of `token_jcs.json`

The signature input is not:

- not the pretty-printed JSON
- not the original non-canonical JSON text
- not a SHA-256 digest unless explicitly stated otherwise in the bundle

## 5. Signature Algorithm

Signature rules:

- algorithm: Ed25519
- signature format: Base64 in `token_signature.b64`
- public key format: PEM in `public_key.pem`

Verification must be performed directly against the canonical UTF-8 bytes defined above.

## 6. Public Key Source

The verification key for this bundle is the exact key contained in:

- `public_key.pem`

No other key source should be used for verifying this bundle.

If a live endpoint also exposes a public key, the bundle PEM remains authoritative for this artifact comparison.

## 7. Timestamp Rules

Timestamp fields, if present in the token payload, must be preserved exactly as emitted.

Rules:

- no normalization
- no timezone rewriting
- no truncation
- no rounding
- no conversion between string and numeric form unless the emitted artifact already uses that form

External validators must verify the exact emitted representation.

## 8. Nonce Rules

Nonce fields, if present, must be preserved exactly as emitted.

Rules:

- treat nonce as exact payload data
- do not coerce numeric nonce into string form
- do not coerce string nonce into numeric form
- do not trim, normalize, or reinterpret

## 9. Expiry Rules

Expiry fields, if present, must be preserved exactly as emitted.

Rules:

- exact field name must match
- exact value must match
- exact representation must match
- expiry validation logic must be applied only after successful signature verification unless the verifier explicitly documents another order

## 10. Determinism Requirement

A compliant verifier must produce the same result as the bundle reference when given:

- the exact `token_jcs.json`
- the exact `token_signature.b64`
- the exact `public_key.pem`

Required parity:

- same canonical bytes
- same signature input
- same Ed25519 verification result

## 11. Expected Result

The authoritative expected result is defined in:

- `expected_result.json`

At minimum it should declare:

- canonicalization method
- signature algorithm
- signature input definition
- expected verification result

## 12. Failure Surfaces

If verification diverges, the likely causes are:

- canonicalization mismatch
- optional field omission mismatch
- UTF-8 encoding mismatch
- signature input mismatch
- public key mismatch
- field type mismatch
- timestamp representation mismatch
- nonce representation mismatch
- wrong token artifact being tested

## 13. Boundary

This contract defines only the token verification path for the supplied token artifact.

It does not by itself define:

- runtime authorization policy
- token issuance policy
- execution semantics
- capsule verification semantics
- broader CHORA custody semantics

## 14. Acceptance Rule

For this bundle, verification alignment is considered achieved only when both systems can truthfully state:

same token payload  
→ same canonical bytes  
→ same signature input  
→ same verification result
