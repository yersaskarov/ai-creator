# -*- coding: utf-8 -*-
import pytest

from path_safety import clean_relative_path


def test_accepts_simple_filename():
    assert clean_relative_path("README.md") == "README.md"


def test_accepts_nested_path():
    assert clean_relative_path("prompts/teacher_prompt.txt") == "prompts/teacher_prompt.txt"


def test_normalizes_backslashes():
    assert clean_relative_path("prompts\\teacher_prompt.txt") == "prompts/teacher_prompt.txt"


def test_rejects_parent_traversal():
    assert clean_relative_path("../.env") is None


def test_rejects_nested_parent_traversal():
    assert clean_relative_path("safe/../../.env") is None


def test_rejects_absolute_path():
    assert clean_relative_path("/etc/passwd") is None


def test_rejects_drive_letter_path():
    assert clean_relative_path("C:/Users/token.txt") is None


def test_rejects_empty_string():
    assert clean_relative_path("") is None


def test_rejects_dot_only_path():
    assert clean_relative_path(".") is None


def test_accepts_deeply_nested_path():
    result = clean_relative_path("a/b/c/file.txt")
    assert result == "a/b/c/file.txt"


@pytest.mark.parametrize("unsafe", [
    "../.env",
    "safe/../../.env",
    "/etc/passwd",
    "C:/Users/token.txt",
    "nested\\..\\.env",
    "",
    ".",
])
def test_rejects_all_unsafe_paths(unsafe):
    assert clean_relative_path(unsafe) is None
