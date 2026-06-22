import json

import ai_generator


def test_clean_relative_path_accepts_safe_nested_path():
    assert ai_generator._clean_relative_path("prompts/teacher_prompt.txt") == "prompts/teacher_prompt.txt"


def test_clean_relative_path_rejects_parent_traversal():
    assert ai_generator._clean_relative_path("../.env") is None
    assert ai_generator._clean_relative_path("safe/../../.env") is None


def test_clean_relative_path_rejects_absolute_and_drive_paths():
    assert ai_generator._clean_relative_path("/etc/passwd") is None
    assert ai_generator._clean_relative_path("C:/Users/token.txt") is None


def test_parse_files_from_json_returns_clean_files():
    payload = {
        "files": {
            "README.md": "# Demo\n",
            "prompts/system_prompt.txt": "Be helpful.",
        }
    }

    assert ai_generator._parse_files_from_json(json.dumps(payload)) == payload["files"]


def test_parse_files_from_json_returns_none_for_invalid_json():
    assert ai_generator._parse_files_from_json('{"files": {"README.md": "unterminated}') is None


def test_parse_files_from_json_rejects_too_many_files():
    payload = {
        "files": {
            f"file_{index}.txt": "content"
            for index in range(ai_generator.MAX_AI_FILES + 1)
        }
    }

    assert ai_generator._parse_files_from_json(json.dumps(payload)) is None


def test_parse_files_from_json_rejects_oversized_file():
    payload = {
        "files": {
            "README.md": "x" * (ai_generator.MAX_AI_FILE_CHARS + 1)
        }
    }

    assert ai_generator._parse_files_from_json(json.dumps(payload)) is None
