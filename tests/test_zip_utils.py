import zipfile

from zip_utils import create_project_zip


def test_create_project_zip_creates_archive(tmp_path):
    project_dir = tmp_path / "my_project"
    project_dir.mkdir()
    (project_dir / "README.md").write_text("hello", encoding="utf-8")
    zip_path = tmp_path / "my_project.zip"

    create_project_zip(project_dir, zip_path, tmp_path)

    assert zip_path.exists()


def test_create_project_zip_includes_files(tmp_path):
    project_dir = tmp_path / "my_project"
    project_dir.mkdir()
    (project_dir / "README.md").write_text("hello", encoding="utf-8")
    zip_path = tmp_path / "my_project.zip"

    create_project_zip(project_dir, zip_path, tmp_path)

    with zipfile.ZipFile(zip_path) as zipf:
        assert "my_project/README.md" in zipf.namelist()


def test_create_project_zip_preserves_nested_directories(tmp_path):
    project_dir = tmp_path / "my_project"
    prompts_dir = project_dir / "prompts"
    prompts_dir.mkdir(parents=True)
    (prompts_dir / "system.txt").write_text("prompt", encoding="utf-8")
    zip_path = tmp_path / "my_project.zip"

    create_project_zip(project_dir, zip_path, tmp_path)

    with zipfile.ZipFile(zip_path) as zipf:
        assert "my_project/prompts/system.txt" in zipf.namelist()


def test_create_project_zip_returns_zip_path(tmp_path):
    project_dir = tmp_path / "my_project"
    project_dir.mkdir()
    (project_dir / "main.py").write_text("print('hello')", encoding="utf-8")
    zip_path = tmp_path / "my_project.zip"

    result = create_project_zip(project_dir, zip_path, tmp_path)

    assert result == zip_path
