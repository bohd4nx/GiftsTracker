import ast
import json


def _convert_bytes(obj):
    """Recursively converts bytes values to their repr string for JSON serialization."""
    if isinstance(obj, dict):
        return {k: _convert_bytes(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_convert_bytes(item) for item in obj]
    if isinstance(obj, bytes):
        # Store as repr(b'...') so it can be safely round-tripped back via ast.literal_eval.
        return repr(obj)
    return obj


def _restore_bytes(obj):
    """Recursively restores repr strings back to bytes after JSON deserialization."""
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


def serialize_json(data: dict | None) -> str | None:
    """Serializes a dict to a JSON string, converting any bytes values to repr strings."""
    if not data:
        return None
    return json.dumps(_convert_bytes(data), ensure_ascii=False)


def deserialize_json(data_str: str | None) -> dict:
    """Deserializes a JSON string back to a dict, restoring repr strings to bytes."""
    if not data_str:
        return {}
    return _restore_bytes(json.loads(data_str))
