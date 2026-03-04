from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class AppConfig:
    app_name: str = "CodexVideos"
    environment: str = "dev"
    default_model_provider: str = "mock"
    output_dir: str = "outputs"

    def model_dump(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ModelConfig:
    provider: str = "mock"
    model_name: str = "mock-echo"
    params: dict[str, Any] = field(default_factory=dict)


@dataclass
class JobConfig:
    name: str = ""
    type: str = "generate"
    template: str | None = None
    project: str = "demo_project"
    variables: dict[str, Any] = field(default_factory=dict)
    output_name: str = "result"
    model_provider: str | None = None
    input_file: str | None = None
    qc_rules_file: str = "configs/qc_rules.yaml"
