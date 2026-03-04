import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.services.run_service import run_generate
from app.services.template_service import render_template_file
from app.utils.paths import CONFIGS_DIR, OUTPUTS_DIR, PROJECTS_DIR, ROOT_DIR, TEMPLATES_DIR

app = FastAPI(title="CodexVideos API", version="0.2.0")


class TemplateRenderRequest(BaseModel):
    template: str = Field(..., description="Template path, relative to repo root")
    variables: dict[str, object] = Field(default_factory=dict)


class JobRunRequest(BaseModel):
    job_config: str = Field(..., description="Job config path, relative to repo root")
    dry_run: bool = True
    model_provider: str | None = None
    mock_mode: bool = False


def _safe_relative_path(base: Path, target: Path) -> str:
    try:
        return str(target.relative_to(base))
    except ValueError:
        return str(target)


def _resolve_repo_path(path_text: str) -> Path:
    path = (ROOT_DIR / path_text).resolve()
    if ROOT_DIR not in path.parents and path != ROOT_DIR:
        raise HTTPException(status_code=400, detail="Path must be inside repository")
    return path


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/version")
def version() -> dict[str, str]:
    return {"version": "0.2.0", "service": "CodexVideos API"}


@app.get("/api/projects")
def api_projects() -> dict[str, list[dict[str, object]]]:
    projects: list[dict[str, object]] = []
    for project_dir in sorted([p for p in PROJECTS_DIR.iterdir() if p.is_dir()], key=lambda p: p.name):
        meta_path = project_dir / "meta.json"
        meta = {}
        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        files = sorted([str(file.relative_to(project_dir)) for file in project_dir.glob("**/*") if file.is_file()])
        projects.append({"name": project_dir.name, "meta": meta, "files": files})
    return {"items": projects}


@app.get("/api/templates")
def api_templates() -> dict[str, list[dict[str, str]]]:
    templates = []
    for path in sorted(TEMPLATES_DIR.glob("**/*.md")):
        templates.append(
            {
                "name": path.stem,
                "path": _safe_relative_path(ROOT_DIR, path),
                "category": _safe_relative_path(TEMPLATES_DIR, path.parent),
            }
        )
    return {"items": templates}


@app.post("/api/templates/render")
def api_templates_render(payload: TemplateRenderRequest) -> dict[str, object]:
    template_path = _resolve_repo_path(payload.template)
    if not template_path.exists():
        raise HTTPException(status_code=404, detail="Template not found")
    rendered = render_template_file(template_path, payload.variables)
    return {"template": payload.template, "variables": payload.variables, "rendered": rendered}


@app.post("/api/jobs/run")
def api_jobs_run(payload: JobRunRequest) -> dict[str, object]:
    job_path = _resolve_repo_path(payload.job_config)
    if not job_path.exists():
        raise HTTPException(status_code=404, detail="Job config not found")

    if payload.mock_mode:
        return {
            "job_name": "mock_job",
            "provider": payload.model_provider or "mock",
            "dry_run": True,
            "run_dir": "outputs/mock-run",
            "outputs": ["outputs/mock-run/mock_prompt.md", "outputs/mock-run/mock_result.md"],
            "message": "Mock mode enabled in API",
        }

    summary = run_generate(
        job_config_path=job_path,
        dry_run=payload.dry_run,
        model_provider_override=payload.model_provider,
    )
    return summary


@app.get("/api/jobs")
def api_jobs() -> dict[str, list[dict[str, object]]]:
    items: list[dict[str, object]] = []
    for run_dir in sorted([p for p in OUTPUTS_DIR.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True):
        summary_file = run_dir / "summary.json"
        if not summary_file.exists():
            continue
        try:
            data = json.loads(summary_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        data["run_dir"] = _safe_relative_path(ROOT_DIR, Path(data.get("run_dir", run_dir)))
        data["summary_file"] = _safe_relative_path(ROOT_DIR, summary_file)
        items.append(data)
    return {"items": items}


@app.get("/api/reports/qc")
def api_reports_qc() -> dict[str, list[dict[str, object]]]:
    items: list[dict[str, object]] = []
    for run_dir in sorted([p for p in OUTPUTS_DIR.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True):
        json_report = run_dir / "qc_report.json"
        md_report = run_dir / "qc_report.md"
        if not json_report.exists() and not md_report.exists():
            continue
        entry: dict[str, object] = {
            "run_dir": _safe_relative_path(ROOT_DIR, run_dir),
            "json_path": _safe_relative_path(ROOT_DIR, json_report) if json_report.exists() else None,
            "md_path": _safe_relative_path(ROOT_DIR, md_report) if md_report.exists() else None,
            "json_content": None,
            "md_content": None,
        }
        if json_report.exists():
            entry["json_content"] = json.loads(json_report.read_text(encoding="utf-8"))
        if md_report.exists():
            entry["md_content"] = md_report.read_text(encoding="utf-8")
        items.append(entry)
    return {"items": items}


@app.get("/api/jobs/configs")
def api_job_configs() -> dict[str, list[str]]:
    configs = [str(path.relative_to(ROOT_DIR)) for path in sorted((CONFIGS_DIR / "jobs").glob("*.yaml"))]
    return {"items": configs}
