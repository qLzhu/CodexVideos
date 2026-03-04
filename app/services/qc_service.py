import json
from pathlib import Path

from app.core.config_loader import load_yaml
from app.core.qc_engine import run_rule_qc
from app.utils.logger import setup_logger
from app.utils.paths import ROOT_DIR, create_run_dir


def run_qc(job_config_path: Path) -> dict:
    config = load_yaml(job_config_path)
    run_dir = create_run_dir("run")
    logger = setup_logger("codexvideos.qc", run_dir / "logs" / "qc.log")
    logger.info("加载QC任务: %s", job_config_path)

    input_path = ROOT_DIR / config["input_file"]
    rules_path = ROOT_DIR / config.get("qc_rules_file", "configs/qc_rules.yaml")

    text = input_path.read_text(encoding="utf-8")
    rules = load_yaml(rules_path)
    report = run_rule_qc(text, rules)
    report["job_name"] = config.get("name")

    json_path = run_dir / "qc_report.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    md = ["# 质检报告", f"- Job: {config.get('name')}", f"- Score: {report['score']}", f"- Passed: {report['passed']}", "", "## 命中详情", json.dumps(report["hits"], ensure_ascii=False, indent=2)]
    md_path = run_dir / "qc_report.md"
    md_path.write_text("\n".join(md), encoding="utf-8")

    logger.info("QC完成: %s %s", json_path, md_path)
    return {"run_dir": str(run_dir), "json": str(json_path), "md": str(md_path), "report": report}
