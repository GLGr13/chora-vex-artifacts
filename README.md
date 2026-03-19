# CHORA — External Continuation Authority

CHORA is a control-plane system that enforces **external authorization over execution**.

It separates:
- Proposal (reasoning / model output)
- Authorization (CHORA Gate decision)
- Execution (allowed continuation)

No system is allowed to continue without an explicit, verifiable decision.

## System Model

Proposal → CHORA Gate → Execution
                 ↓
           Evidence Capsule

- Systems propose actions
- CHORA Gate evaluates structural validity and risk
- Gate returns:
  - ALLOW
  - HALT
  - ESCALATE
- A cryptographic Evidence Capsule is emitted for every decision

## Core Principle

No continuation without authorization  
No decision without custody

## Repository Role

This repository is not the source of truth.

It is a projection of a live CHORA runtime:

- Runtime (VPS) = authoritative system
- Repository (GitHub) = public evidence surface

All contents are exported from the runtime via a deterministic sync process.

## Artifacts

All verification artifacts are located under:

/artifacts

### Specimen Capsules
artifacts/specimen-capsules/

### Reference Bundles
artifacts/reference-bundles/

### Public Keys
artifacts/keys/

## Verification

A CHORA capsule can be independently verified using:

- Canonical serialization (RFC 8785 / JCS)
- Signature verification (Ed25519)
- Public key from /artifacts/keys

## Sync Mechanism

scripts/sync_runtime_to_repo.sh

This script:
- exports runtime docs and tracker state
- publishes artifacts (capsules, bundles, keys)
- commits only when changes occur

## Status

- Live runtime deployed
- Evidence capsules actively emitted
- Repository aligned with runtime

## Final Note

This repository represents a live control-plane system exporting verifiable governance artifacts.
