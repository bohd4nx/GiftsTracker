import ast
import json
from typing import Any


def _convert_bytes(obj: Any) -> Any:
    """Recursively converts bytes values to repr strings for JSON serialisation."""
    if isinstance(obj, dict):
        return {k: _convert_bytes(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_convert_bytes(item) for item in obj]
    if isinstance(obj, bytes):
        # store as repr(b'...') so it can be safely round-tripped back via ast.literal_eval.
        return repr(obj)
    return obj


def _restore_bytes(obj: Any) -> Any:
    """Recursively restores repr strings back to bytes after JSON deserialisation."""
    if isinstance(obj, dict):
        return {k: _restore_bytes(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_restore_bytes(item) for item in obj]
    if isinstance(obj, str) and len(obj) >= 3 and obj.startswith("b") and obj[1] in ("'", '"'):
        try:
            result = ast.literal_eval(obj)
            if isinstance(result, bytes):
                return result
        except Exception:
            pass
        return obj
    return obj


def serialize_json(data: dict[str, Any] | None) -> str | None:
    """Serialises a dict to JSON, converting bytes to repr strings."""
    if not data:
        return None
    return json.dumps(_convert_bytes(data), ensure_ascii=False)


def deserialize_json(data_str: str | None) -> dict[str, Any]:
    """Deserialises a JSON string back to a dict, restoring repr strings to bytes."""
    if not data_str:
        return {}
    return _restore_bytes(json.loads(data_str))  # type: ignore[no-any-return]
