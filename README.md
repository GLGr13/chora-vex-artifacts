# CHORA

**External Continuation Authority for Governed AI Execution**

CHORA is an open specification and reference implementation for external continuation authority, structural reasoning discipline, and verifiable governance artifacts.

In CHORA, cognition may propose, but continuation authority is external and binding. The runtime is designed so that authorization is produced in a separate control plane, recorded as a verifiable decision artifact, and made available for downstream execution and audit.

## Current public state

- Canonical architecture: **v220**
- Public Gate: **live on VPS**
- Public verification surface: **Merkle v0.3**
- Phase 3 MCS: **shadow mode completed**
- Replay harness: **locked**
- Positioning: **open spec + reference implementation**

## What CHORA is

- A control-plane governance primitive for AI and agent execution
- An external continuation authority that emits `ALLOW`, `HALT`, or `ESCALATE`
- A structured path from proposal -> validation -> authorization -> custody
- A system for producing verifiable evidence capsules and replayable artifacts

## What CHORA is not

- Not a claim of perfect reasoning
- Not a hidden model-side heuristic loop
- Not merely advisory governance or post-hoc logging
- Not a substitute for execution attestation, custody, or downstream safety engineering

## Canonical architecture

```text
Proposal Layer
    -> Validation Layer (Sensors + MCS)
    -> Authority Layer (CHORA Gate)
    -> Supervisory Layer (EMS, future binding phase)
    -> Custody Layer
    -> Observability Layer
```

## Design laws

- No continuation without authorization
- No recovery without escalation
- No decision without custody

## Repository layout

```text
/docs        Public architecture, specifications, guides
/schemas     Machine-readable contracts
/src/chora   Reference implementation
/examples    Minimal example requests and specimen outputs
/tests       Runtime and verification tests
/scripts     Local tooling for dev, release, and verification
```

## Specs to read first

- [`docs/overview.md`](docs/overview.md)
- [`docs/architecture/v220-canonical-architecture.md`](docs/architecture/v220-canonical-architecture.md)
- [`docs/architecture/external-continuation-authority.md`](docs/architecture/external-continuation-authority.md)
- [`docs/specs/gate-runtime-spec-v0.3.md`](docs/specs/gate-runtime-spec-v0.3.md)
- [`docs/specs/evidence-capsule-spec-v0.3.md`](docs/specs/evidence-capsule-spec-v0.3.md)
- [`docs/specs/mcs-checklist-spec-v0.1.md`](docs/specs/mcs-checklist-spec-v0.1.md)
- [`docs/specs/dra-schema-v220.md`](docs/specs/dra-schema-v220.md)

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn chora.api.app:app --reload
```

Then open `/health` and POST a request to `/gate`.

## Status

This repository is intentionally structured as a **public shell first**:

1. Publish the architecture
2. Freeze the runtime contract
3. Publish schemas
4. Ship a minimal reference implementation
5. Add specimen capsules and golden verification vectors

## License

See [`LICENSE`](LICENSE).
