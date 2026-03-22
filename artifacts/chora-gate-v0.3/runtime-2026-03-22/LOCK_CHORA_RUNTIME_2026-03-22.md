# CHORA Runtime Lock — 2026-03-22

## Status
This document locks the CHORA Gate runtime at a canonical, verified state.

## Snapshot Artifact
Path:
`/root/chora-gate-v0.3_live_canonical_2026-03-22.tar.gz`

SHA256:
`df48168651b7a56603d447497384d644105bdd383f331be061ecf033a59b3c3e`

---

## Core Guarantees

### 1. Canonicalization (RFC 8785 JCS)
- All hashing uses `jcs.canonicalize`
- Capsule, token payload, and verification are byte-consistent

### 2. Evidence Capsule Integrity
- Merkle root recomputation verified
- Ed25519 signature valid
- OTS anchoring functional

### 3. MCS Binding (Phase 3 — Active)
- `MCS_FAIL → HALT`
- `MCS_ESCALATE → ESCALATE`
- Policy rule aligned with authority outcome

### 4. EMS Token Contract v3
- Payload is the signed object (JCS canonical bytes)

## Verified End-to-End Flow (canonical bytes)

REQUEST → GATE → CAPSULE → EMS → TOKEN → VERIFY → EXECUTE

> Execution proof:
> CHORA_PUBLIC_EXEC_OK
