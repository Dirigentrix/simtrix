"""Ishida program message parser."""
from typing import Any
from core.constants import TELEMETRY_ISHIDA_PROGRAM

def parse_ishida(data: str | dict[str, Any]) -> dict[str, Any]:
    raw = {p.split("=", 1)[0].strip().lower(): p.split("=", 1)[1].strip() for p in data.split(";") if "=" in p} if isinstance(data, str) else {str(k).lower(): v for k, v in data.items()}
    program = str(raw.get("program", ""))
    if program and program != TELEMETRY_ISHIDA_PROGRAM: raise ValueError(f"unsupported Ishida program: {program}")
    if "weight_g" in raw:
        raw["weight_g"] = float(raw["weight_g"])
    return raw
