# CHORA Gate Specification

External Continuation Authority for Governed Execution

---

## Overview

CHORA defines a minimal control-plane primitive that governs whether execution may continue.

It introduces a non-bypassable boundary between reasoning and execution.

> Reasoning may propose.  
> Only CHORA may authorize continuation.

---

## Core Invariant

Execution is prevented unless a valid, signed, time-valid, context-bound continuation artifact is present.

---

## Architecture Roles

- CHORA Gate — continuation authority (ALLOW / HALT / ESCALATE)
- EMS — supervisory resolution for escalations
- Execution Runtime (e.g. VEX/AEM) — enforcement + verification
- MCS — structural validation upstream of authority

---

## Why This Matters

Most systems allow implicit continuation.

CHORA removes that assumption.

Continuation must be explicitly granted.

---

## Specification

See:

- /spec/chora-gate-v0.4.md
- /spec/ems-contract-v1.md
- /spec/segmented-execution-v1.md
- /spec/mcs-sensor-channel-v1.md

---

## Compliance

Implementations MUST satisfy:

- No continuation without authorization
- No valid continuation artifact → no execution
- No bypass around verification boundary
- ESCALATE must resolve through EMS before continuation

See /compliance/checklist.md.

---

## Status

Draft v0.4 — aligned with live CHORA Gate implementation and CHORA–VEX interop.

---

## Philosophy

CHORA does not improve reasoning.

It enforces whether execution is allowed.

This is a control-plane primitive, not a model capability.
