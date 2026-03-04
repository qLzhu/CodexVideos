"""Minimal YAML subset loader for offline MVP.
Supports mappings/lists with 2-space indentation, scalars, booleans, numbers, strings.
"""

from __future__ import annotations


def _parse_scalar(v: str):
    v = v.strip()
    if v == "":
        return ""
    if v.lower() in {"true", "false"}:
        return v.lower() == "true"
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    try:
        if "." in v:
            return float(v)
        return int(v)
    except ValueError:
        return v


def safe_load(data):
    text = data.read() if hasattr(data, "read") else str(data)
    lines = [ln.rstrip("\n") for ln in text.splitlines()]
    lines = [ln for ln in lines if ln.strip() and not ln.lstrip().startswith("#")]
    if not lines:
        return {}

    def parse_block(i: int, indent: int):
        obj = {}
        arr = None
        while i < len(lines):
            line = lines[i]
            cur = len(line) - len(line.lstrip(" "))
            if cur < indent:
                break
            if cur > indent:
                i += 1
                continue

            stripped = line.strip()
            if stripped.startswith("- "):
                if arr is None:
                    arr = []
                item = stripped[2:].strip()
                if ":" in item and not item.startswith(('"', "'")):
                    key, val = item.split(":", 1)
                    node = {key.strip(): _parse_scalar(val) if val.strip() else {}}
                    if not val.strip():
                        child, ni = parse_block(i + 1, indent + 2)
                        node[key.strip()] = child
                        i = ni
                    else:
                        i += 1
                    arr.append(node)
                else:
                    arr.append(_parse_scalar(item))
                    i += 1
                continue

            if ":" in stripped:
                key, val = stripped.split(":", 1)
                key = key.strip()
                val = val.strip()
                if val == "":
                    child, ni = parse_block(i + 1, indent + 2)
                    obj[key] = child
                    i = ni
                else:
                    obj[key] = _parse_scalar(val)
                    i += 1
                continue

            i += 1

        if arr is not None and not obj:
            return arr, i
        return obj, i

    parsed, _ = parse_block(0, 0)
    return parsed
