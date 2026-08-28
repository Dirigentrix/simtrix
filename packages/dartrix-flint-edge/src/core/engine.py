"""Top-level deterministic edge coordinator."""
from typing import Any
from .constants import TICK_MS
from .phase_bus import PhaseBus, PhaseEvent
from telemetry.gea_listener import GeaTelemetry, parse_gea
from telemetry.ishida_parser import parse_ishida
from physics.brine_layers import BrineColumn
from physics.feed_stream import FeedStream
from coupling.sync_layer import SyncLayer

class FlintEdgeEngine:
    def __init__(self) -> None:
        self.clock_ms = 0
        self.bus = PhaseBus()
        self.brine = BrineColumn()
        self.feed = FeedStream()
        self.sync = SyncLayer()
        self.last_gea: GeaTelemetry | None = None
        self.last_ishida: dict[str, Any] = {}

    def ingest_gea(self, data: str | dict[str, Any]) -> PhaseEvent:
        self.last_gea = parse_gea(data)
        event = PhaseEvent("gea", self.last_gea.phase, self.clock_ms, self.last_gea.as_dict())
        self.bus.publish(event)
        return event

    def ingest_ishida(self, data: str | dict[str, Any]) -> PhaseEvent:
        self.last_ishida = parse_ishida(data)
        event = PhaseEvent("ishida", self.last_ishida.get("phase", "unknown"), self.clock_ms, self.last_ishida)
        self.bus.publish(event)
        return event

    def tick(self, elapsed_ms: int = TICK_MS) -> dict[str, Any]:
        if elapsed_ms <= 0: raise ValueError("elapsed_ms must be positive")
        self.clock_ms += elapsed_ms
        self.feed.advance(elapsed_ms)
        self.brine.advance(self.feed.volume_added(elapsed_ms))
        return {"clock_ms": self.clock_ms, "layers": self.brine.snapshot(), "feed_lpm": self.feed.rate_lpm, "sync": self.sync.status(self.last_gea, self.last_ishida)}
