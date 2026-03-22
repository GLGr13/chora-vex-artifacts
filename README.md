# CHORA x VEX Artifacts

## Governed Execution

This repository contains the public reference artifacts for the CHORA x VEX governed execution architecture.

### Enforcement guarantee

Enforcement is implemented at the runtime boundary via `verify_continuation_token`, which prevents execution unless a valid, signed continuation artifact is present.

### Core invariant

No valid authorization artifact -> No execution

This changes the execution model from:

model decides -> system executes

to:

model proposes -> external authority decides -> execution is conditionally allowed

### Canonical execution-binding reference

- `docs/execution-binding/CHORA_VEX_EXECUTION_BINDING_CONTRACT_v1.md`
- `docs/execution-binding/CONTRACT_V1_DIAGRAM_MAPPING.md`

### Canonical figures

- `docs/figures/chora_execution_pipeline.png`
- `docs/figures/chora_governed_loops.png`

### Canonical tag

`execution-binding-v1.0`

---

# CHORA - External Continuation Authority

CHORA is a control-plane system that enforces **external authorization over execution**.

It separates:
- Proposal (reasoning / model output)
- Authorization (CHORA Gate decision)
- Execution (allowed continuation)

No system is allowed to continue without an explicit, verifiable decision.

## System Model

Proposal -> CHORA Gate -> Execution
                 v
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
