# CHORA Evidence Capsule Spec v0.3

## Purpose

Define the portable artifact format used to preserve CHORA governance decisions in a replayable, verifiable, and custody-friendly structure.

## Capsule minimum contents

- Capsule identifier
- Request digest
- Decision object
- Reason set
- Policy context
- MCS or sensor summary
- Merkle commitment fields when applicable
- Signature envelope when applicable
- Verification metadata

## Verification goals

A verifier should be able to:

1. Recompute canonical digests
2. Verify inclusion or commitment fields
3. Verify the signature scope
4. Determine the exact governed decision

## Canonicalization

JSON serialization should follow a deterministic canonicalization process. JCS-compatible output is recommended for signed payloads and public verification vectors.
