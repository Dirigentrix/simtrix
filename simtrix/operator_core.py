"""SIMTRIX Triad operator: Diagnosta, Wilk and Hydra."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Any

from .algebra_engine import ANGLE_DEGREES, GAMMA, RESONANCE_HZ, triad_tensor, tensor_trace

CORE_ID = 181141
RISK_THRESHOLD = 0.72


@dataclass(frozen=True)
class RiskModel:
    threshold: float = RISK_THRESHOLD
    resonance_hz: float = RESONANCE_HZ
    gamma: float = GAMMA

    def classify(self, score: float) -> str:
        if not 0.0 <= score <= 1.0:
            raise ValueError("risk score must be between 0 and 1")
        return "HIGH" if score >= self.threshold else "LOW"


class SimtrixOperatorCore:
    """Coordinates the three complementary Triad perspectives."""

    CORE_ID = CORE_ID
    VERSION = "0.1.0"

    def __init__(self) -> None:
        self.risk = RiskModel()
        self.agents = ("Diagnosta", "Wilk", "Hydra")

    def evaluate(self, risk_score: float = 0.0, context: Any = None) -> dict[str, Any]:
        return {
            "core_id": self.CORE_ID,
            "version": self.VERSION,
            "triad": list(self.agents),
            "risk_score": risk_score,
            "risk_class": self.risk.classify(risk_score),
            "threshold": self.risk.threshold,
            "resonance_hz": self.risk.resonance_hz,
            "context_present": context is not None,
        }

    def diagnostics(self) -> dict[str, Any]:
        tensor = triad_tensor()
        return {"tensor_size": "7x7", "tensor_trace": tensor_trace(tensor), "angle_degrees": ANGLE_DEGREES, "gamma": GAMMA}


def main() -> None:
    parser = argparse.ArgumentParser(description="SIMTRIX Triad operator core")
    parser.add_argument("--risk", type=float, default=0.0, help="risk score in [0, 1]")
    parser.add_argument("--diagnostics", action="store_true", help="show algebra diagnostics")
    args = parser.parse_args()
    core = SimtrixOperatorCore()
    result = core.diagnostics() if args.diagnostics else core.evaluate(args.risk)
    print(json.dumps(result, ensure_ascii=False, indent=2))
