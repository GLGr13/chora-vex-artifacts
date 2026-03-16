# CHORA Gate HTTP API

POST /gate

Example request:

{
  "confidence": 0.91
}

Example response:

{
  "decision": "ALLOW",
  "capsule_id": "example"
}

Possible decisions:

ALLOW
HALT
ESCALATE
