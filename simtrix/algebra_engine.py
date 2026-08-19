"""Deterministic SIMTRIX algebra primitives; standard library only."""

from __future__ import annotations

from math import acos, sqrt
from typing import Sequence

SIMTRIX_VECTOR = (10.0, 10.0, 10.0)
DARTRIX_VECTOR = (10.0, 10.0, 10.0)
SIMU_SION_VECTOR = (10.0, 10.0, 10.0)
EXPECTED_NORM = sqrt(300.0)
ANGLE_DEGREES = 36.2042
GAMMA = 2.691602
RESONANCE_HZ = 46.62


def dot(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("vectors must have equal dimensions")
    return sum(a * b for a, b in zip(left, right))


def norm(vector: Sequence[float]) -> float:
    return sqrt(dot(vector, vector))


def angle_degrees(left: Sequence[float], right: Sequence[float]) -> float:
    denominator = norm(left) * norm(right)
    if denominator == 0:
        raise ValueError("zero vector has no angle")
    cosine = max(-1.0, min(1.0, dot(left, right) / denominator))
    return acos(cosine) * 180.0 / 3.141592653589793


def triad_tensor() -> tuple[tuple[float, ...], ...]:
    """Return a 7x7 diagonal tensor whose trace is exactly 300."""
    diagonal = 300.0 / 7.0
    return tuple(tuple(diagonal if i == j else 0.0 for j in range(7)) for i in range(7))


def tensor_trace(tensor: Sequence[Sequence[float]]) -> float:
    return sum(tensor[i][i] for i in range(min(len(tensor), *(len(row) for row in tensor))))


def resonance(gamma: float = GAMMA) -> float:
    return gamma * (RESONANCE_HZ / GAMMA)
