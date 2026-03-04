import json
from pathlib import Path

from app.adapters.model_adapter import get_model_adapter
from app.core.config_loader import load_yaml
from app.core.template_engine import read_template, render_template
from app.utils.logger import setup_logger
from app.utils.paths import ROOT_DIR, create_run_dir
from app.utils.security import mask_sensitive


def run_generate(job_config_path: Path, dry_run: bool = False, model_provider_override: str | None = None) -> dict:
    config = load_yaml(job_config_path)
    run_dir = create_run_dir("run")
    logger = setup_logger("codexvideos.run", run_dir / "logs" / "run.log")
    logger.info("加载任务配置: %s", job_config_path)

    template_path = ROOT_DIR / config["template"]
    variables = config.get("variables", {})
    provider = model_provider_override or config.get("model_provider", "mock")

    logger.info("任务变量(脱敏): %s", mask_sensitive(variables))
    template_text = read_template(template_path)
    prompt = render_template(template_text, variables)

    prompt_file = run_dir / f"{config.get('output_name', 'result')}_prompt.md"
    prompt_file.write_text(prompt, encoding="utf-8")

    result_text = ""
    if dry_run:
        logger.info("dry_run=true，跳过模型调用")
    else:
        adapter = get_model_adapter(provider)
        result_text = adapter.generate(prompt)

    result_file = run_dir / f"{config.get('output_name', 'result')}.md"
    result_file.write_text(result_text or prompt, encoding="utf-8")

    summary = {
        "job_name": config.get("name"),
        "provider": provider,
        "dry_run": dry_run,
        "run_dir": str(run_dir),
        "outputs": [str(prompt_file), str(result_file)],
    }
    summary_file = run_dir / "summary.json"
    summary_file.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("任务完成: %s", summary_file)
    return summary
