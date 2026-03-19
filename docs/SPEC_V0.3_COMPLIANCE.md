# CHORA Gate — Evidence Capsule v0.3 Compliance

## Status
This implementation is strictly compliant with Evidence Capsule Specification v0.3.

## Commitment Model

The CHORA Gate produces a capsule composed of:

- intent
- authority
- identity
- witness (committed subset only)

Each component is:
- Canonicalized (RFC 8785 JCS)
- Hashed (SHA-256)

capsule_root = H(intent_hash || authority_hash || identity_hash || witness_hash)

## Witness Commitment

Committed subset:
- chora_node_id
- timestamp

Non-committed (post-seal metadata):
- receipt_hash
- witness_mode
- sentinel_mode
- observational_only

## Signature

- Ed25519
- scope: capsule_root

## Verification

Verification recomputes:
- intent_hash
- authority_hash
- identity_hash
- witness_hash (committed subset only)
- capsule_root

Then verifies signature.

## Authority Integrity

All authority mutations (including MCS binding) are included before final hashing.

## Custody

- custody_mode: external_non_bypass
- sentinel_mode: observe_only

## Conclusion

This implementation preserves deterministic verification, minimal commitment surface, and strict v0.3 compliance.
