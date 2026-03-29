# CHORA Compliance Checklist

## Authority

- [ ] Gate returns only ALLOW / HALT / ESCALATE
- [ ] No implicit authorization paths exist

## EMS

- [ ] ESCALATE always routes through EMS
- [ ] No continuation without RESOLVED_ALLOW

## Enforcement

- [ ] Execution requires valid continuation token
- [ ] Verification is fail-closed

## Segmentation

- [ ] Execution is boundary-based
- [ ] Token required per segment

## Security

- [ ] Signature verification enforced
- [ ] Nonce uniqueness enforced
- [ ] execution_target binding enforced

## Integrity

- [ ] Decisions are reproducible
- [ ] No bypass around verification boundary
