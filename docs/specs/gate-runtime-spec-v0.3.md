# CHORA Gate Runtime Spec v0.3

## Status

Draft public runtime specification aligned to the current CHORA v220 canonical architecture.

## Purpose

Define the public runtime contract for a minimal CHORA Gate service that accepts a declared request context and returns a binding governance decision.

## Endpoint

`POST /gate`

## Request contract

A gate request must contain at minimum:

- `request_id`: caller-generated unique identifier
- `timestamp_utc`: RFC3339 UTC timestamp
- `subject`: identity or subsystem making the request
- `action_class`: normalized action class
- `payload_sha256`: digest of the governed payload
- `policy_context`: policy or regime identifier
- `dra`: declared reasoning artifact or reference

Optional fields may include:

- `confidence`
- `capabilities`
- `sensor_signals`
- `mcs_report`
- `nonce`
- `expiry_utc`

## Response contract

A gate response returns:

- `decision`: `ALLOW | HALT | ESCALATE`
- `decision_id`
- `request_id`
- `timestamp_utc`
- `reasons[]`
- `capsule_id`
- `merkle_root` when available
- `signature` when configured
- `public_key_id` when configured

## Runtime invariants

- No decision without a stable request digest
- No continuation without a recorded decision
- Identical replay inputs must be detectable
- Decision artifacts must be serializable into a custody object

## Replay and idempotency

`request_id + payload_sha256 + policy_context` should be sufficient to detect duplicate submissions under the same regime.

## Error semantics

- `400` malformed request
- `409` replay conflict or duplicate with incompatible state
- `422` structurally invalid DRA or MCS payload
- `500` runtime failure

## Relationship to MCS

MCS is upstream of authorization. The runtime may reject or downgrade requests that lack sufficient structural validation evidence.
