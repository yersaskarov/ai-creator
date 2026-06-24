# -*- coding: utf-8 -*-
import time


def parse_allowed_ids(value: str | None) -> set[int]:
    if not value:
        return set()

    allowed_ids = set()
    for item in value.split(","):
        item = item.strip()
        if not item:
            raise ValueError("ALLOWED_TELEGRAM_IDS contains an empty item")
        if not item.isdecimal():
            raise ValueError("ALLOWED_TELEGRAM_IDS contains an invalid Telegram ID")

        user_id = int(item)
        if user_id <= 0:
            raise ValueError("ALLOWED_TELEGRAM_IDS must contain positive Telegram IDs")

        allowed_ids.add(user_id)
    return allowed_ids


def is_user_allowed(user_id: int, allowed_ids: set[int]) -> bool:
    return not allowed_ids or user_id in allowed_ids


class GenerationLock:
    def __init__(self) -> None:
        self._active_user_ids: set[int] = set()

    def acquire(self, user_id: int) -> bool:
        if user_id in self._active_user_ids:
            return False
        self._active_user_ids.add(user_id)
        return True

    def release(self, user_id: int) -> None:
        self._active_user_ids.discard(user_id)

    def is_active(self, user_id: int) -> bool:
        return user_id in self._active_user_ids


class GenerationCooldown:
    """Per-user cooldown between generation requests.

    Set cooldown_seconds=0 to disable.  Thread safety is not required because
    the Telegram bot runs in a single async event loop.
    """

    def __init__(self, cooldown_seconds: int) -> None:
        self._cooldown = cooldown_seconds
        self._last_finished: dict[int, float] = {}

    def seconds_remaining(self, user_id: int) -> float:
        """Return seconds the user must wait before generating again (0 = OK)."""
        if self._cooldown <= 0:
            return 0.0
        last = self._last_finished.get(user_id)
        if last is None:
            return 0.0
        elapsed = time.monotonic() - last
        return max(0.0, self._cooldown - elapsed)

    def record_finished(self, user_id: int) -> None:
        """Mark that user_id just finished a generation attempt."""
        if self._cooldown > 0:
            self._last_finished[user_id] = time.monotonic()
