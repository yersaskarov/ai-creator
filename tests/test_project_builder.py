import project_builder


def base_project_data(**overrides):
    data = {
        "project_name": "Demo Project",
        "project_type": "Telegram-Р±РѕС‚",
        "custom_idea": "",
        "goal": "Test goal",
        "experience": "РќР°С‡РёРЅР°СЋС‰РёР№",
        "model": "GPT",
        "language": "Python",
        "hosting": "Local",
        "extra_answer": "",
        "readme_detail": "",
    }
    data.update(overrides)
    return data


def test_make_safe_filename_keeps_plain_name():
    assert project_builder.make_safe_filename("Project") == "Project"


def test_make_safe_filename_replaces_spaces():
    assert project_builder.make_safe_filename("My Project Name") == "My_Project_Name"


def test_make_safe_filename_removes_special_characters():
    assert project_builder.make_safe_filename(" My @Project!!! 2026 ") == "My_Project_2026"


def test_make_safe_filename_falls_back_for_empty_or_forbidden_only_name():
    assert project_builder.make_safe_filename("") == "my_project"
    assert project_builder.make_safe_filename("!!!") == "my_project"


def test_build_static_files_adds_python_requirements_and_env_example():
    files = project_builder.build_static_files(base_project_data(language="Python"))

    assert "requirements.txt" in files
    assert ".env.example" in files
    assert "package.json" not in files


def test_build_static_files_adds_javascript_package_json_and_env_example():
    files = project_builder.build_static_files(
        base_project_data(language="JavaScript / TypeScript")
    )

    assert "package.json" in files
    assert ".env.example" in files
    assert "requirements.txt" not in files


def test_build_static_files_adds_prompt_files_when_prompts_are_enabled(monkeypatch):
    monkeypatch.setattr(
        project_builder.templates,
        "PROMPTS",
        {"system_prompt.md": "system prompt"},
    )
    monkeypatch.setattr(project_builder.templates, "should_include_prompts", lambda data: True)

    files = project_builder.build_static_files(base_project_data())

    assert files["prompts/system_prompt.md"] == "system prompt"


def test_build_static_files_skips_prompt_files_when_prompts_are_disabled(monkeypatch):
    monkeypatch.setattr(
        project_builder.templates,
        "PROMPTS",
        {"system_prompt.md": "system prompt"},
    )
    monkeypatch.setattr(project_builder.templates, "should_include_prompts", lambda data: False)

    files = project_builder.build_static_files(base_project_data())

    assert "prompts/system_prompt.md" not in files


def test_write_files_creates_files_in_target_directory(tmp_path):
    project_builder.write_files(tmp_path, {"README.md": "hello"})

    assert (tmp_path / "README.md").exists()


def test_write_files_creates_nested_directories(tmp_path):
    project_builder.write_files(tmp_path, {"prompts/system_prompt.md": "prompt"})

    assert (tmp_path / "prompts" / "system_prompt.md").exists()


def test_write_files_preserves_file_contents(tmp_path):
    content = "line 1\nline 2\n"

    project_builder.write_files(tmp_path, {"nested/file.txt": content})

    assert (tmp_path / "nested" / "file.txt").read_text(encoding="utf-8") == content


def test_format_files_list_returns_readable_text():
    result = project_builder.format_files_list(
        {
            "main.py": "",
            "README.md": "",
        }
    )

    assert result == "\u2022 README.md\n\u2022 main.py"


def test_format_files_list_handles_empty_file_list():
    assert project_builder.format_files_list({}) == ""
