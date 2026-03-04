import argparse
import json
from pathlib import Path

from app.core.config_loader import ConfigError, load_app_config
from app.services.export_service import export_results
from app.services.project_service import init_project, list_projects
from app.services.qc_service import run_qc
from app.services.run_service import run_generate
from app.services.template_service import render_template_file, validate_template
from app.utils.paths import ROOT_DIR


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m app.cli", description="CodexVideos CLI")
    sub = parser.add_subparsers(dest="command")

    p_config = sub.add_parser("config", help="展示应用配置")
    p_config.add_argument("--config", default="configs/app.yaml")

    p_project = sub.add_parser("project", help="项目管理")
    project_sub = p_project.add_subparsers(dest="subcommand")
    p_project_init = project_sub.add_parser("init", help="初始化项目")
    p_project_init.add_argument("name")
    project_sub.add_parser("list", help="列出项目")

    p_template = sub.add_parser("template", help="模板管理")
    template_sub = p_template.add_subparsers(dest="subcommand")
    p_tpl_validate = template_sub.add_parser("validate", help="校验模板变量")
    p_tpl_validate.add_argument("--template", required=True)
    p_tpl_validate.add_argument("--vars", default="{}")
    p_tpl_render = template_sub.add_parser("render", help="渲染模板")
    p_tpl_render.add_argument("--template", required=True)
    p_tpl_render.add_argument("--vars", default="{}")

    p_run = sub.add_parser("run", help="任务执行")
    run_sub = p_run.add_subparsers(dest="subcommand")
    p_run_generate = run_sub.add_parser("generate", help="执行生成任务")
    p_run_generate.add_argument("--config", required=True)
    p_run_generate.add_argument("--dry-run", action="store_true")
    p_run_generate.add_argument("--model-provider", default=None)

    p_qc = sub.add_parser("qc", help="质检")
    qc_sub = p_qc.add_subparsers(dest="subcommand")
    p_qc_run = qc_sub.add_parser("run", help="执行质检")
    p_qc_run.add_argument("--config", required=True)

    p_export = sub.add_parser("export", help="导出")
    export_sub = p_export.add_subparsers(dest="subcommand")
    p_export_results = export_sub.add_parser("results", help="导出结果")
    p_export_results.add_argument("--run-dir", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "config":
        try:
            cfg = load_app_config(ROOT_DIR / args.config)
            print(json.dumps(cfg.model_dump(), ensure_ascii=False, indent=2))
            return 0
        except ConfigError as e:
            print(e)
            return 1

    if args.command == "project":
        if args.subcommand == "init":
            p = init_project(args.name)
            print(f"项目已初始化: {p}")
            return 0
        if args.subcommand == "list":
            for p in list_projects():
                print(p)
            return 0

    if args.command == "template":
        variables = json.loads(args.vars)
        if args.subcommand == "validate":
            ok, missing, required = validate_template(ROOT_DIR / args.template, variables)
            print(f"required={sorted(required)}")
            if ok:
                print("模板校验通过")
                return 0
            print(f"模板校验失败，缺失变量: {missing}")
            return 1
        if args.subcommand == "render":
            print(render_template_file(ROOT_DIR / args.template, variables))
            return 0

    if args.command == "run" and args.subcommand == "generate":
        summary = run_generate(ROOT_DIR / args.config, dry_run=args.dry_run, model_provider_override=args.model_provider)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    if args.command == "qc" and args.subcommand == "run":
        result = run_qc(ROOT_DIR / args.config)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == "export" and args.subcommand == "results":
        result = export_results(Path(args.run_dir))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
