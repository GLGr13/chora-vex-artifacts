# CHORA Token Contract v3

CHORA Token Contract v3 is the first payload-signed continuation token contract.

## Core Rule

The signed object is the RFC 8785 JCS canonical token payload.

Verification rule:

payload -> RFC 8785 JCS canonical bytes -> Ed25519 signature -> verification

The signed object is not:
- capsule_root bytes
- a wrapper object
- a derived hash unless explicitly versioned that way

## Required Signed Fields

The canonical signed payload must contain:

- schema
- issuer
- iat
- exp
- ledger_event_id
- resolution_event_id
- source_capsule_root
- nonce

Recommended schema value:

- chora.continuation.token.v3

## Signature Rules

- algorithm: Ed25519
- signature input: raw UTF-8 bytes of the RFC 8785 JCS canonical payload
- signature scope: payload

## Canonicalization Rules

- canonicalization method: RFC 8785 JCS
- encoding: UTF-8
- no pretty printing
- no silent normalization after emission
- exact emitted string values must be preserved

## Timestamp Rules

- iat and exp are signed payload fields
- exact emitted representation must be preserved during verification
- no normalization during verification
- no timezone rewriting during verification

## Nonce Rules

- nonce is signed payload data
- nonce must be a string
- verifiers must not coerce nonce between numeric and string forms

## Capsule Linkage Rule

source_capsule_root remains part of the signed token payload.

This is the signed linkage between continuation authorization and capsule custody.

## Omission Rule

- absent optional fields are omitted, not null
- verifiers must verify exactly the emitted payload
- implementations must not inject missing fields prior to verification

## Extensibility Rule

Any material change to signed payload semantics requires a schema version bump.

## Acceptance Rule

A v3 token is aligned only when two independent systems can truthfully state:

same payload -> same JCS bytes -> same signature input -> same verification result
