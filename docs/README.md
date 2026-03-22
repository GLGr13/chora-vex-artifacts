# CHORA x VEX Public Architecture Index

This repository contains the public reference artifacts for the CHORA x VEX governed execution architecture.

## Canonical execution-binding surface

- `execution-binding/CHORA_VEX_EXECUTION_BINDING_CONTRACT_v1.md`
- `execution-binding/CONTRACT_V1_DIAGRAM_MAPPING.md`

## Enforcement guarantee

Enforcement is implemented at the runtime boundary via `verify_continuation_token`, which prevents execution unless a valid, signed continuation artifact is present.

## Core invariant

No valid authorization artifact -> No execution

## Canonical figures

- `figures/chora_execution_pipeline.png`
- `figures/chora_governed_loops.png`

## Canonical tag

`execution-binding-v1.0`
