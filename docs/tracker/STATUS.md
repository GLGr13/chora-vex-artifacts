# CHORA Progress Status

Last Updated: 2026-03-19T07:12:36Z

## Phase3 Mcs Sensor Channel
Status: DONE_INTERNAL

### Done
- [x] MCS_ESCALATE_BINDING
- [x] structural escalation logic
- [x] MCS binding affects gate outcome

### Missing
- [ ] explicit MCS artifact/schema
- [ ] shadow vs binding mode switch
- [ ] external visibility of mode state
- [ ] stable sensor result format
- [ ] formal MCS decision semantics
- [ ] reproducible MCS evaluation interface

## Phase4 Coordination Ledger
Status: PARTIAL

### Done
- [x] linked hash chain exists
- [x] prior state hash chaining works
- [x] ledger entries can be appended

### Missing
- [ ] append-only enforcement guarantee
- [ ] replay verification command/script
- [ ] continuity verification across full chain
- [ ] chain audit command
- [ ] query interface
- [ ] event retrieval by event_id
- [ ] deterministic export format
- [ ] ledger integrity recovery procedure

## Phase5 Ems
Status: DONE_CORE

### Done
- [x] EMS stub exists
- [x] EMS resolution flow exists
- [x] continuation authorization exists
- [x] signed token generation exists
- [x] signature verification exists
- [x] runtime enforcement exists

### Missing
- [ ] EMS to execution audit linkage
- [ ] EMS resolution to execution reference binding
- [ ] optional EMS introspection endpoint
- [ ] supervision trail queryability
- [ ] deterministic record of which execution consumed which EMS resolution

## Phase6 Drift Sensors
Status: NOT_STARTED

### Done
- none

### Missing
- [ ] decision distribution drift
- [ ] nonce violation rate
- [ ] expired token attempts
- [ ] unusual deny spike detection
- [ ] escalation distribution drift
- [ ] execution anomaly rate

## Phase7 Governance Metrics
Status: NOT_STARTED

### Done
- none

### Missing
- [ ] allow deny ratio
- [ ] escalation frequency
- [ ] EMS resolution latency
- [ ] execution reliability
- [ ] token expiry failure rate
- [ ] nonce mismatch failure rate
- [ ] replay attempt count
- [ ] drift trends
- [ ] authorization to execution latency
- [ ] full custody coverage rate

## Next Locked Step
Execution Semantics Completion Track
- [ ] Define execution event schema
- [ ] Implement append-only execution log
- [ ] Bind token to execution (hash and metadata)
- [ ] Persist nonce registry
- [ ] Generate execution evidence artifact
- [ ] Link execution event to ledger entry
- [ ] Link execution event to EMS resolution
- [ ] Add replay check against persistent nonce store
- [ ] Add execution record verification command
- [ ] Add execution artifact export format

## System Invariant
Proposal → Validation → Authorization → Execution → Evidence
