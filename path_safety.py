# -*- coding: utf-8 -*-
import re
from pathlib import PurePosixPath


def clean_relative_path(path: str) -> str | None:
    """Return a sanitised relative POSIX path, or None if the path is unsafe.

    Blocks: parent traversal (..), drive-letter prefixes, absolute paths, and
    empty or dot-only segments.  Backslashes are normalised to forward slashes.
    """
    normalized = str(path).replace("\\", "/").strip()

    if not normalized or normalized == ".":
        return None
    if ".." in normalized:
        return None
    if re.search(r"(^|/)[A-Za-z]:", normalized):
        return None

    posix_path = PurePosixPath(normalized)
    if posix_path.is_absolute():
        return None
    if any(part in ("", ".", "..") for part in posix_path.parts):
        return None

    return "/".join(posix_path.parts)
