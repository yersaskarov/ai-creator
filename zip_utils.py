# -*- coding: utf-8 -*-
import zipfile
from pathlib import Path


def create_project_zip(project_dir: Path, zip_path: Path, archive_root: Path) -> Path:
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in project_dir.rglob("*"):
            if file.is_file():
                zipf.write(file, arcname=file.relative_to(archive_root))

    return zip_path
