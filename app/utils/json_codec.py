import json


def serialize_json(data: dict | None) -> str | None:
    if not data:
        return None

    def convert_bytes(obj):
        if isinstance(obj, dict):
            return {k: convert_bytes(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_bytes(item) for item in obj]
        elif isinstance(obj, bytes):
            return repr(obj)
        return obj

    return json.dumps(convert_bytes(data), ensure_ascii=False)


def deserialize_json(data_str: str | None) -> dict:
    if not data_str:
        return {}

    parsed = json.loads(data_str)

    def restore_bytes(obj):
        if isinstance(obj, dict):
            return {k: restore_bytes(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [restore_bytes(item) for item in obj]
        elif isinstance(obj, str) and obj.startswith("b'") and obj.endswith("'"):
            try:
                return eval(obj)
            except:
                return obj
        return obj

    return restore_bytes(parsed)
