from abc import ABC, abstractmethod


class BaseModelAdapter(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError


class MockModelAdapter(BaseModelAdapter):
    def generate(self, prompt: str, **kwargs) -> str:
        suffix = kwargs.get("suffix", "[MOCK-GENERATED]")
        return f"{suffix}\n{prompt}"


class EchoModelAdapter(BaseModelAdapter):
    def generate(self, prompt: str, **kwargs) -> str:
        return prompt


def get_model_adapter(provider: str) -> BaseModelAdapter:
    provider = provider.lower()
    if provider == "mock":
        return MockModelAdapter()
    if provider == "echo":
        return EchoModelAdapter()
    raise ValueError(f"不支持的模型 provider: {provider}")
