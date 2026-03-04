from typing import Any

SENSITIVE_KEYS = {"api_key", "apikey", "secret", "token", "password", "access_key"}


def mask_sensitive(data: Any):
    if isinstance(data, dict):
        masked = {}
        for k, v in data.items():
            if any(s in k.lower() for s in SENSITIVE_KEYS):
                masked[k] = "***MASKED***"
            else:
                masked[k] = mask_sensitive(v)
        return masked
    if isinstance(data, list):
        return [mask_sensitive(item) for item in data]
    return data
