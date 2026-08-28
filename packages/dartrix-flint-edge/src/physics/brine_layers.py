"""Conservative fourteen-layer brine column model."""
from core.constants import BRINE_VOLUME_L, LAYER_COUNT

class BrineColumn:
    def __init__(self, layers: list[float] | None = None) -> None:
        self.layers = list(layers) if layers is not None else [BRINE_VOLUME_L / LAYER_COUNT] * LAYER_COUNT
        if len(self.layers) != LAYER_COUNT: raise ValueError("exactly 14 layers required")
    def advance(self, volume_l: float) -> None:
        if volume_l < 0: raise ValueError("volume cannot be negative")
        self.layers[-1] += volume_l
        mean = sum(self.layers) / LAYER_COUNT
        for i in range(LAYER_COUNT - 1): self.layers[i] += (self.layers[i + 1] - self.layers[i]) * 0.01
        self.layers[-1] = max(0.0, sum(self.layers) - sum(self.layers[:-1]))
    def snapshot(self) -> list[float]: return self.layers.copy()
