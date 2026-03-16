# External Continuation Authority

CHORA externalizes continuation authority.

The system may reason, propose, estimate, or compose, but it does not continue solely because it produced an answer. Continuation must be authorized by a separate control-plane mechanism that records its decision in a reconstructible form.

## Why this matters

In safety-critical engineering, the proposing component is often distinct from the component that authorizes or commits a state transition.

CHORA applies the same principle to AI execution:

```text
proposal -> validation -> authorization -> execution
```

Without a valid authorization artifact, continuation should not proceed.

## Decision surface

The minimal decision set is:

- `ALLOW`
- `HALT`
- `ESCALATE`

## Implication

CHORA is not merely advisory. Its architectural role is to sit before continuation and produce a governance decision that downstream systems can verify, store, and bind to execution.
