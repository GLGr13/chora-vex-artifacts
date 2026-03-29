# Escalate Flow

1. Request sent to CHORA Gate
2. Decision = ESCALATE
3. EMS enters PENDING_REVIEW
4. No token issued
5. Execution attempted

Expected: EXECUTION DENIED

Only after:

EMS -> RESOLVED_ALLOW
-> token issued
-> execution allowed
