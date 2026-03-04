import pytest

from app.core.template_engine import extract_variables, render_template, TemplateError


def test_extract_and_render_template():
    text = "Hello {{name}}, genre={{genre}}"
    vars_found = extract_variables(text)
    assert vars_found == {"name", "genre"}
    rendered = render_template(text, {"name": "Alice", "genre": "悬疑"})
    assert "Alice" in rendered
    assert "悬疑" in rendered


def test_render_template_missing_vars():
    text = "Hello {{name}}, {{role}}"
    with pytest.raises(TemplateError):
        render_template(text, {"name": "Alice"})
