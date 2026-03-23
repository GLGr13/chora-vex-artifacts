cat << 'EOF' > docs/runtime-contracts-v1-diagram.md
# CHORA Runtime Contracts v1 — Execution Flow

## Runtime Authority Flow

```text
+------------------------------+
|           PROPOSAL           |
|   model / agent / pipeline   |
+------------------------------+
               |
               v
+------------------------------+
|      CHORA GATE              |
|   external authority layer   |
|                              |
|   ALLOW / HALT / ESCALATE    |
+------------------------------+
      |            |          |
      |            |          |
      v            v          v
   ALLOW         HALT     ESCALATE
      |                       |
      |                       v
      |            +----------------------+
      |            |         EMS          |
      |            |   supervisory path   |
      |            |                      |
      |            | RESOLVED_ALLOW/HALT  |
      |            +----------------------+
      |                       |
      |             if RESOLVED_ALLOW
      |                       |
      +-----------+-----------+
                  |
                  v
+------------------------------+
|   CONTINUATION TOKEN (v3)    |
|   JCS payload + Ed25519      |
+------------------------------+
               |
               v
+------------------------------+
|      VEX / AEM RUNTIME       |
|                              |
| verify_continuation_token()  |
| enforce execution boundary   |
|                              |
| NO TOKEN -> NO EXECUTION     |
+------------------------------+
               |
               v
        segment boundary
               |
               +--> re-authorize next step


