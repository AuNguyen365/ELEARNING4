"""
Runtime globals for the application.

Expose module-level variables which can be initialised at startup.
Do not store request-specific state here. Only store application-wide singletons
such as database engine, caches, or the Settings instance.
"""
from typing import Optional

from app.core.config import settings

# Settings instance (imported for convenience)
APP_SETTINGS = settings

# Database engine placeholder (initialised elsewhere)
DB_ENGINE = None  # type: Optional[object]


def init_db_engine(engine: object) -> None:
    """Initialize the global DB_ENGINE.

    Call this from your application startup logic with the real engine.
    """
    global DB_ENGINE
    DB_ENGINE = engine


# Simple in-memory token blacklist for logout support. In production you would
# prefer a persistent store (Redis) with TTLs matching token expiry.
TOKEN_BLACKLIST = set()


def blacklist_token(token: str) -> None:
    """Add a token to the in-memory blacklist."""
    TOKEN_BLACKLIST.add(token)


def is_token_blacklisted(token: str) -> bool:
    return token in TOKEN_BLACKLIST
