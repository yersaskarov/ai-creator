# -*- coding: utf-8 -*-


def parse_allowed_ids(value: str | None) -> set[int]:
    if not value:
        return set()

    allowed_ids = set()
    for item in value.split(","):
        item = item.strip()
        if not item:
            continue
        try:
            allowed_ids.add(int(item))
        except ValueError:
            continue
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
