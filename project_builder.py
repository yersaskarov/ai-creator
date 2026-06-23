# -*- coding: utf-8 -*-
from pathlib import Path

import templates


def make_safe_filename(name: str) -> str:
    safe = "".join(c if c.isalnum() or c in (" ", "-", "_") else "" for c in name)
    safe = safe.strip().replace(" ", "_")
    return safe or "my_project"


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
        target_path = project_dir / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content, encoding="utf-8")


def format_files_list(files: dict[str, str]) -> str:
    visible_files = sorted(files.keys())
    return "\n".join(f"• {name}" for name in visible_files)
