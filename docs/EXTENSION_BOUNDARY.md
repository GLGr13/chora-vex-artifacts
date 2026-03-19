# CHORA — v0.3 Extension Boundary

## Principle

v0.3 is a stable commitment layer.

It is NOT modified for new features.

## Rule

Future phases attach to the capsule — they do not modify it.

## External Extensions

- EMS (continuation tokens)
- Execution receipts
- Drift sensors
- Governance metrics

## Binding Pattern

All external artifacts must reference:
- capsule_id
- capsule_root

## Forbidden

- Expanding witness_hash scope
- Changing capsule_root structure
- Embedding execution payloads into capsule

## Upgrade Condition

Only a new spec version (v0.4+) can change commitment structure.

## Conclusion

v0.3 remains minimal, stable, and verifiable.
