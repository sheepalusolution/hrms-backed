from datetime import datetime, timedelta
from typing import Set

class TokenBlacklist:
    """
    Simple in-memory token blacklist.
    You can later replace this with a DB or Redis implementation.
    """

    _blacklist: Set[str] = set()

    @classmethod
    def add_token(cls, token: str):
        """Add a token to the blacklist."""
        cls._blacklist.add(token)

    @classmethod
    def is_blacklisted(cls, token: str) -> bool:
        """Check if token is blacklisted."""
        return token in cls._blacklist

    @classmethod
    def remove_token(cls, token: str):
        """Remove token from blacklist (optional)."""
        cls._blacklist.discard(token)

    @classmethod
    def clear(cls):
        """Clear all blacklisted tokens."""
        cls._blacklist.clear()
