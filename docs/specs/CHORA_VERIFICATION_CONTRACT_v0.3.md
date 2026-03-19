# CHORA Verification Contract v0.3

This document defines the minimal verification contract required for deterministic cross-system validation of CHORA v0.3 artifacts.

## Scope

This contract is intended to align external verification implementations against the current CHORA v0.3 runtime behavior.

It is intentionally narrower than the full CHORA specification.

## 1. Canonicalization

CHORA v0.3 request commitment uses:

- RFC 8785 (JCS)
- UTF-8 encoding
- deterministic canonical JSON

## 2. Hash Components

The capsule verification surface consists of four component hashes:

- intent_hash
- authority_hash
- identity_hash
- witness_hash

These are recomputed and checked independently.

## 3. Capsule Root

The signed verification object is:

- capsule_root

The signature scope is:

- capsule_root

It is not the full serialized capsule JSON directly.

## 4. Signature

- Algorithm: Ed25519
- Signature is computed over capsule_root
- Public key endpoint:
  https://gate.choragate.network/public_key

## 5. Witness Verification

Witness integrity is recomputed using the same scope as the live verification path.

External validators should align to reference artifacts when testing parity.

## 6. Determinism Requirement

Given the same reference artifact:

- component hashes must match
- capsule_root must match
- signature verification must match

## 7. Failure Surfaces

If verification diverges, the likely causes are:

- canonicalization mismatch
- component field mismatch
- witness scope mismatch
- signature scope mismatch
- public key mismatch
- encoding mismatch

## 8. Canonical Reference Practice

CHORA publishes:

- specimen capsules
- reference bundles
- public key snapshots

These act as reproducible verification anchors.

## 9. Boundary

This contract defines the capsule verification path.

It does not resolve token-verification mismatches without a dedicated token reference artifact.
