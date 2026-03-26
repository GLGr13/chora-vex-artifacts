from __future__ import annotations

from typing import Any, Dict

import rfc8785
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey


def canonical_bytes(obj: Dict[str, Any]) -> bytes:
    out = rfc8785.dumps(obj)
    if isinstance(out, str):
        return out.encode("utf-8")
    return out


def verify_payload_signature(
    payload: Dict[str, Any],
    signature: str,
    public_key_hex: str,
) -> bool:
    try:
        vk = VerifyKey(bytes.fromhex(public_key_hex))
        msg = canonical_bytes(payload)
        sig = bytes.fromhex(signature)
        vk.verify(msg, sig)
        return True
    except BadSignatureError:
        return False
    except Exception:
        return False
