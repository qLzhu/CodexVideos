from pathlib import Path

from app.core.template_engine import extract_variables, read_template, render_template, validate_variables


def validate_template(template_path: Path, variables: dict[str, object]) -> tuple[bool, list[str], set[str]]:
    text = read_template(template_path)
    ok, missing = validate_variables(text, variables)
    return ok, missing, extract_variables(text)


def render_template_file(template_path: Path, variables: dict[str, object]) -> str:
    text = read_template(template_path)
    return render_template(text, variables)
