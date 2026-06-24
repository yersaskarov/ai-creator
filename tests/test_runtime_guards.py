import pytest

from runtime_guards import GenerationCooldown, GenerationLock, is_user_allowed, parse_allowed_ids


def test_parse_allowed_ids_none_returns_empty_set():
    assert parse_allowed_ids(None) == set()


def test_parse_allowed_ids_empty_string_returns_empty_set():
    assert parse_allowed_ids("") == set()


def test_parse_allowed_ids_returns_int_set():
    assert parse_allowed_ids("123456,987654") == {123456, 987654}


def test_parse_allowed_ids_ignores_spaces():
    assert parse_allowed_ids(" 123456 , 987654 ") == {123456, 987654}


def test_parse_allowed_ids_with_comma_and_spaces_returns_int_set():
    assert parse_allowed_ids("123, 456") == {123, 456}


@pytest.mark.parametrize("value", ["abc", "123;456", "12.5", "-1", "123,,456"])
def test_parse_allowed_ids_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        parse_allowed_ids(value)


def test_is_user_allowed_when_allowed_list_is_empty():
    assert is_user_allowed(123, set()) is True


def test_is_user_allowed_denies_user_not_in_allowed_list():
    assert is_user_allowed(999, {123, 456}) is False


def test_generation_lock_blocks_same_user_twice():
    lock = GenerationLock()

    assert lock.acquire(123) is True
    assert lock.acquire(123) is False


def test_generation_lock_does_not_block_other_users():
    lock = GenerationLock()

    assert lock.acquire(123) is True
    assert lock.acquire(456) is True


def test_generation_lock_releases_after_completion():
    lock = GenerationLock()

    assert lock.acquire(123) is True
    lock.release(123)

    assert lock.acquire(123) is True


def test_generation_lock_release_is_safe_for_missing_user():
    lock = GenerationLock()

    lock.release(123)

    assert lock.is_active(123) is False


def test_generation_cooldown_disabled_when_cooldown_is_zero():
    cooldown = GenerationCooldown(0)
    cooldown.record_finished(123)
    assert cooldown.seconds_remaining(123) == 0.0


def test_generation_cooldown_returns_zero_for_new_user():
    cooldown = GenerationCooldown(60)
    assert cooldown.seconds_remaining(999) == 0.0


def test_generation_cooldown_blocks_immediately_after_generation():
    cooldown = GenerationCooldown(60)
    cooldown.record_finished(123)
    assert cooldown.seconds_remaining(123) > 0


def test_generation_cooldown_does_not_affect_other_users():
    cooldown = GenerationCooldown(60)
    cooldown.record_finished(123)
    assert cooldown.seconds_remaining(456) == 0.0


def test_generation_cooldown_zero_does_not_record():
    cooldown = GenerationCooldown(0)
    cooldown.record_finished(123)
    # Internal dict must stay empty when cooldown is disabled
    assert 123 not in cooldown._last_finished
