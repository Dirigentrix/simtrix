"""Synchronous, deterministic phase event bus."""
from dataclasses import dataclass, field
from typing import Any, Callable

@dataclass(frozen=True)
class PhaseEvent:
    source: str
    phase: str
    timestamp_ms: int
    payload: dict[str, Any] = field(default_factory=dict)

class PhaseBus:
    def __init__(self) -> None:
        self._subscribers: list[Callable[[PhaseEvent], None]] = []
        self.history: list[PhaseEvent] = []

    def subscribe(self, callback: Callable[[PhaseEvent], None]) -> None:
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def publish(self, event: PhaseEvent) -> None:
        self.history.append(event)
        for callback in tuple(self._subscribers):
            callback(event)
