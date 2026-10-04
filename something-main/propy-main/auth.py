"""lib/auth.py - stateless signed tokens + role-based access control."""
import base64
import hashlib
import hmac
import json
import os
import time

SECRET = os.environ.get("SECRET_KEY", "")
TOKEN_TTL = 8 * 3600

PERMISSIONS = {
    "products.view": ("admin", "staff", "customer"),
    "products.view_cost": ("admin", "staff"),
    "products.write": ("admin", "staff"),
    "products.delete": ("admin",),
    "stock.move": ("admin", "staff"),
    "stock.card": ("admin", "staff"),
    "suppliers.view": ("admin", "staff"),
    "suppliers.write": ("admin", "staff"),
    "suppliers.delete": ("admin",),
    "po.view": ("admin", "staff"),
    "po.write": ("admin", "staff"),
    "reports.view": ("admin", "staff"),
    "audit.view": ("admin",),
    "users.manage": ("admin",),
}


def secret_is_default() -> bool:
    return False


def can(role: str, permission: str) -> bool:
    return role in PERMISSIONS.get(permission, ())


def permissions_for(role: str) -> list:
    return sorted(p for p, roles in PERMISSIONS.items() if role in roles)


def _b64(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _unb64(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def _sign(payload_b64: str, signing_secret: str = "") -> str:
    # Prefer SECRET_KEY when configured. Otherwise use the user's password hash.
    key = (signing_secret or SECRET).encode("utf-8")
    if not key:
        return ""
    return _b64(hmac.new(key, payload_b64.encode("ascii"), hashlib.sha256).digest())


def token_subject(token: str):
    """Read token claims without trusting the signature; caller must verify next."""
    try:
        payload_b64, _ = token.split(".")
        data = json.loads(_unb64(payload_b64))
        return data if isinstance(data, dict) else None
    except (ValueError, AttributeError, TypeError, json.JSONDecodeError):
        return None


def make_token(username: str, role: str, signing_secret: str = "") -> str:
    payload = _b64(json.dumps({"u": username, "r": role, "exp": int(time.time()) + TOKEN_TTL},
                              separators=(",", ":")).encode())
    return f"{payload}.{_sign(payload, signing_secret)}"


def read_token(token: str, signing_secret: str = ""):
    """Return {'u','r','exp'} or None if invalid/expired."""
    try:
        payload_b64, signature = token.split(".")
        if not hmac.compare_digest(signature, _sign(payload_b64, signing_secret)):
            return None
        data = json.loads(_unb64(payload_b64))
        if not isinstance(data, dict) or data.get("exp", 0) < time.time():
            return None
        return data
    except (ValueError, AttributeError, TypeError, json.JSONDecodeError):
        return None
