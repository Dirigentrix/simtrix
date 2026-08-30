"""SIMTRIX - Algebraic Engine with Triad Architecture + Wankel OS"""
from .operator_core import SimtrixOperatorCore, RiskModel, RISK_THRESHOLD
from .algebra_engine import (
    vector_norm, triad_tensor,
    REFERENCE_ANGLE, GAMMA, REFERENCE_RESONANCE
)
from .constants import (
    CHRONOS, DANIEL, ADRIAN, RATAJCZYK, ALL_CORES,
    K_SUM, O_SUM, S_SUM, A_SUM, MASTER_SEED,
    FLORA, FAUNA, SUBSPACE
)
from .wankel_cpu import WankelCPU, WankelCore

__version__ = "0.2.0"
__all__ = [
    "SimtrixOperatorCore", "RiskModel", "RISK_THRESHOLD",
    "vector_norm", "triad_tensor",
    "REFERENCE_ANGLE", "GAMMA", "REFERENCE_RESONANCE",
    "CHRONOS", "DANIEL", "ADRIAN", "RATAJCZYK", "ALL_CORES",
    "K_SUM", "O_SUM", "S_SUM", "A_SUM", "MASTER_SEED",
    "FLORA", "FAUNA", "SUBSPACE",
    "WankelCPU", "WankelCore"
]
