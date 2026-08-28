"""Validate notebook integrity and public-repository hygiene."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_SUFFIXES = {
    ".7z",
    ".ckpt",
    ".csv",
    ".h5",
    ".keras",
    ".rar",
    ".zip",
}
MAX_FILE_SIZE = 10 * 1024 * 1024
TEXT_SUFFIXES = {".ipynb", ".md", ".py", ".txt", ".yml", ".yaml"}
PATTERNS = {
    "hard-coded Kaggle path": re.compile(r"(?:/kaggle/|\.\./input/)"),
    "hard-coded Windows user path": re.compile(r"[A-Za-z]:\\\\Users\\\\"),
    "possible embedded secret": re.compile(
        r"(?i)(?:api[_-]?key|client[_-]?secret|password|token)\s*=\s*['\"][^'\"]+['\"]"
    ),
}
REQUIRED_ASSETS = {
    ROOT / "assets" / "arabic_signs_reference.png",
    ROOT / "assets" / "cnn_accuracy.png",
    ROOT / "assets" / "fully_connected_accuracy.png",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    relative = path.relative_to(ROOT)
    if ".ipynb_checkpoints" in path.parts:
        fail(f"notebook checkpoint is tracked: {relative}")
    if path.suffix.lower() in FORBIDDEN_SUFFIXES:
        fail(f"dataset, archive, or model artifact is tracked: {relative}")
    if path.stat().st_size > MAX_FILE_SIZE:
        fail(f"file exceeds 10 MB: {relative}")
    if path.suffix.lower() not in TEXT_SUFFIXES:
        continue
    if path.resolve() == Path(__file__).resolve():
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    for description, pattern in PATTERNS.items():
        if pattern.search(text):
            fail(f"{description} in {relative}")

for asset in REQUIRED_ASSETS:
    if not asset.is_file():
        fail(f"required README asset is missing: {asset.relative_to(ROOT)}")

for path in ROOT.rglob("*.ipynb"):
    notebook = json.loads(path.read_text(encoding="utf-8"))
    if notebook.get("nbformat") != 4:
        fail(f"unexpected notebook format: {path.relative_to(ROOT)}")
    for index, cell in enumerate(notebook.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", "")
        source = "".join(source) if isinstance(source, list) else source
        try:
            ast.parse(source)
        except SyntaxError as error:
            fail(f"invalid Python in {path.relative_to(ROOT)}, cell {index}: {error}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for asset in REQUIRED_ASSETS:
    relative = asset.relative_to(ROOT).as_posix()
    if relative not in readme:
        fail(f"README does not reference {relative}")

print("Repository validation passed.")
