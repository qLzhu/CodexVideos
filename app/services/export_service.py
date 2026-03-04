from pathlib import Path

from app.core.exporter import export_csv, export_json, export_md, export_zip


def export_results(run_dir: Path) -> dict:
    exports_dir = run_dir / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)

    md_sources = list(run_dir.glob("*.md"))
    json_sources = list(run_dir.glob("*.json"))

    manifest = {
        "run_dir": str(run_dir),
        "md_files": [str(p.name) for p in md_sources],
        "json_files": [str(p.name) for p in json_sources],
    }
    md_path = export_md(exports_dir / "manifest.md", "# 导出清单\n\n" + "\n".join(f"- {f}" for f in manifest["md_files"] + manifest["json_files"]))
    json_path = export_json(exports_dir / "manifest.json", manifest)
    csv_rows = [{"file": f} for f in manifest["md_files"] + manifest["json_files"]]
    csv_path = export_csv(exports_dir / "manifest.csv", csv_rows)

    files_for_zip = [md_path, json_path, csv_path] + md_sources + json_sources
    zip_path = export_zip(exports_dir / "bundle.zip", files_for_zip, run_dir)

    return {"exports_dir": str(exports_dir), "files": [str(md_path), str(json_path), str(csv_path), str(zip_path)]}
