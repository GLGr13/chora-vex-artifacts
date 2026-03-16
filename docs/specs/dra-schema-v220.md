# Declared Reasoning Artifact (DRA) Schema v220

## Purpose

The DRA is the declared reasoning envelope presented to CHORA. It is not a transcript requirement. It is a structural declaration that allows validation and governance logic to evaluate whether continuation is eligible.

## Suggested fields

- `goal`
- `regime`
- `premises[]`
- `constraints[]`
- `assumptions[]`
- `branches_considered[]`
- `known_unknowns[]`
- `declared_completion_state`
- `confidence_statement`

## Governance role

A DRA allows CHORA and MCS to reason about declared structure without requiring unrestricted access to hidden reasoning traces.
