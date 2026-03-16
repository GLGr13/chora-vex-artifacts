# CHORA Overview

CHORA is a governance control plane for AI execution.

Its central claim is architectural rather than rhetorical: the component that proposes an action should not be the component that holds continuation authority.

CHORA therefore separates:

- proposal
- validation
- authorization
- custody
- observability

The current canonical public framing is:

1. **Proposal layer** produces candidate action or output.
2. **Validation layer** checks structural and declared reasoning discipline through Sensors and MCS.
3. **Authority layer** emits a binding gate decision.
4. **Custody layer** preserves reconstructible evidence.
5. **Observability layer** measures stability, drift, and governance quality over time.

CHORA is intended to be legible both as:

- an open specification
- a reference implementation

This repository prioritizes public clarity, deterministic contracts, and release hygiene over research sprawl.
