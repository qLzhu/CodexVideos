import re
from pathlib import Path


class TemplateError(Exception):
    pass


VARIABLE_PATTERN = re.compile(r"{{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}}")


def read_template(path: Path) -> str:
    if not path.exists():
        raise TemplateError(f"模板不存在: {path}")
    return path.read_text(encoding="utf-8")


def extract_variables(template_text: str) -> set[str]:
    return set(VARIABLE_PATTERN.findall(template_text))


def validate_variables(template_text: str, variables: dict[str, object]) -> tuple[bool, list[str]]:
    required = extract_variables(template_text)
    missing = sorted([var for var in required if var not in variables])
    return len(missing) == 0, missing


def render_template(template_text: str, variables: dict[str, object]) -> str:
    ok, missing = validate_variables(template_text, variables)
    if not ok:
        raise TemplateError(f"模板变量缺失: {', '.join(missing)}")

    rendered = template_text
    for k, v in variables.items():
        rendered = re.sub(r"{{\s*" + re.escape(k) + r"\s*}}", str(v), rendered)
    return rendered
