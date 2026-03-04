import csv
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def export_md(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def export_json(path: Path, data: dict | list) -> Path:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def export_csv(path: Path, rows: list[dict]) -> Path:
    if not rows:
        rows = [{"message": "no_data"}]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


def export_zip(zip_path: Path, files: list[Path], base_dir: Path) -> Path:
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
        for file in files:
            if file.exists() and file.is_file():
                zf.write(file, arcname=file.relative_to(base_dir))
    return zip_path
