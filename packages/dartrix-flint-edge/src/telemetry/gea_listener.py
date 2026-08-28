"""GEA telemetry normalization."""
from dataclasses import dataclass
from typing import Any
from core.constants import TELEMETRY_GEA_CYCLE_MS

@dataclass(frozen=True)
class GeaTelemetry:
    cycle_ms: int
    phase: str
    values: dict[str, Any]
    def as_dict(self) -> dict[str, Any]: return {"cycle_ms": self.cycle_ms, "phase": self.phase, **self.values}

def parse_gea(data: str | dict[str, Any]) -> GeaTelemetry:
    raw = {p.split("=", 1)[0].strip(): p.split("=", 1)[1].strip() for p in data.split(";") if "=" in p} if isinstance(data, str) else dict(data)
    cycle = int(raw.pop("cycle_ms", TELEMETRY_GEA_CYCLE_MS)); phase = str(raw.pop("phase", "unknown")).lower()
    return GeaTelemetry(cycle, phase, raw)
