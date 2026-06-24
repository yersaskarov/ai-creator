# -*- coding: utf-8 -*-
from pathlib import Path

import templates
from path_safety import clean_relative_path as _safe_path

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
    result = _safe_path(path)
    if result is None:
        raise ValueError(f"Unsafe or invalid file path: {path!r}")
    return result


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
