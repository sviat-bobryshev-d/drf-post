from datetime import datetime


def datetime_to_iso(d: datetime) -> str:
    d = d.isoformat()
    if d.endswith("+00:00"):
        d = d[:-6] + "Z"
    return d
