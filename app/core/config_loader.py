import os
from pathlib import Path
from typing import Any

import yaml

from app.schemas.config import AppConfig


class ConfigError(Exception):
    pass


def load_env_file(path: Path = Path('.env')) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ.setdefault(key.strip(), value.strip())


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ConfigError(f"配置文件不存在: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = dict(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_app_config(config_path: Path, cli_overrides: dict[str, Any] | None = None) -> AppConfig:
    load_env_file()
    yaml_cfg = load_yaml(config_path)

    env_cfg = {
        "app_name": os.getenv("APP_NAME"),
        "environment": os.getenv("APP_ENV"),
        "default_model_provider": os.getenv("MODEL_PROVIDER"),
        "output_dir": os.getenv("OUTPUT_DIR"),
    }
    env_cfg = {k: v for k, v in env_cfg.items() if v is not None}

    merged = deep_merge(AppConfig().model_dump(), yaml_cfg)
    merged = deep_merge(merged, env_cfg)
    if cli_overrides:
        merged = deep_merge(merged, {k: v for k, v in cli_overrides.items() if v is not None})
    return AppConfig(**merged)
