from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parents[2]
CONFIGS_DIR = ROOT_DIR / "configs"
TEMPLATES_DIR = ROOT_DIR / "templates"
PROJECTS_DIR = ROOT_DIR / "projects"
OUTPUTS_DIR = ROOT_DIR / "outputs"
DATA_DIR = ROOT_DIR / "data"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def create_run_dir(prefix: str = "run") -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = OUTPUTS_DIR / f"{prefix}-{ts}"
    ensure_dir(run_dir)
    ensure_dir(run_dir / "logs")
    ensure_dir(run_dir / "exports")
    return run_dir
