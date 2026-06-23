# -*- coding: utf-8 -*-
import re
from pathlib import Path, PurePosixPath

import templates

RESERVED_WINDOWS_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}


def make_safe_filename(name: str) -> str:
    safe = "".join(c if c.isalnum() or c in (" ", "-", "_") else "" for c in name)
    safe = safe.strip().replace(" ", "_")
    if not safe:
        return "my_project"
    if safe.upper() in RESERVED_WINDOWS_NAMES:
        return f"{safe}_project"
    return safe


def _clean_relative_path(path: str) -> str:
    normalized = str(path).replace("\\", "/").strip()
    if not normalized or normalized == ".":
        raise ValueError("File path must be a non-empty relative path")
    if ".." in normalized:
        raise ValueError("File path must not contain parent traversal")
    if re.search(r"(^|/)[A-Za-z]:", normalized):
        raise ValueError("File path must not contain a drive prefix")

    posix_path = PurePosixPath(normalized)
    if posix_path.is_absolute():
        raise ValueError("File path must be relative")
    if any(part in ("", ".", "..") for part in posix_path.parts):
        raise ValueError("File path contains unsafe path segments")

    return "/".join(posix_path.parts)


def build_static_files(data: dict) -> dict[str, str]:
    main_filename, main_content = templates.build_main_file(data)

    files = {
        main_filename: main_content,
        ".env.example": templates.build_env_example(data),
        "README.md": templates.build_readme(data, main_filename),
    }

    if data["language"] == "JavaScript / TypeScript":
        files["package.json"] = templates.build_package_json(data)
    else:
        files["requirements.txt"] = templates.build_requirements(data)

    if templates.should_include_prompts(data):
        for filename, content in templates.PROMPTS.items():
            files[f"prompts/{filename}"] = content

    return files


def write_files(project_dir: Path, files: dict[str, str]) -> None:
    for relative_path, content in files.items():
        safe_relative_path = _clean_relative_path(relative_path)
        target_path = project_dir / safe_relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content, encoding="utf-8")


def format_files_list(files: dict[str, str]) -> str:
    visible_files = sorted(files.keys())
    return "\n".join(f"• {name}" for name in visible_files)
