"""Nominal feed-stream model."""
from core.constants import FEED_STREAM_NOMINAL_LPM
class FeedStream:
    def __init__(self, rate_lpm: float = FEED_STREAM_NOMINAL_LPM) -> None:
        if rate_lpm < 0: raise ValueError("rate must be non-negative")
        self.rate_lpm = float(rate_lpm)
    def advance(self, elapsed_ms: int) -> None: pass
    def volume_added(self, elapsed_ms: int) -> float: return self.rate_lpm * elapsed_ms / 60000.0
