import json
from pathlib import Path

from app.utils.paths import PROJECTS_DIR, ensure_dir


def list_projects() -> list[str]:
    ensure_dir(PROJECTS_DIR)
    return sorted([p.name for p in PROJECTS_DIR.iterdir() if p.is_dir()])


def init_project(name: str) -> Path:
    project_dir = PROJECTS_DIR / name
    ensure_dir(project_dir)
    meta_file = project_dir / "meta.json"
    if not meta_file.exists():
        meta_file.write_text(json.dumps({"name": name, "description": "new project"}, ensure_ascii=False, indent=2), encoding="utf-8")
    return project_dir
