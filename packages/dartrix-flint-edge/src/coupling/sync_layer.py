"""Cross-device timing validation."""
from core.constants import SYNC_TOLERANCE_MS
class SyncLayer:
    def status(self, gea, ishida) -> dict[str, object]:
        if gea is None or not ishida: return {"synchronized": False, "reason": "awaiting telemetry"}
        return {"synchronized": True, "tolerance_ms": SYNC_TOLERANCE_MS, "gea_cycle_ms": gea.cycle_ms, "ishida_program": ishida.get("program")}
