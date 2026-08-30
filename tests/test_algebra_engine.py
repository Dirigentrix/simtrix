"""Tests for SIMTRIX algebra primitives."""

from math import sqrt

import pytest

from simtrix.algebra_engine import (
    ANGLE_DEGREES,
    EXPECTED_NORM,
    GAMMA,
    RESONANCE_HZ,
    SIMTRIX_VECTOR,
    norm,
    tensor_trace,
    triad_tensor,
)


def test_basis_vector_norm() -> None:
    assert norm(SIMTRIX_VECTOR) == pytest.approx(sqrt(300.0))
    assert EXPECTED_NORM == pytest.approx(sqrt(300.0))


def test_triad_tensor_trace() -> None:
    tensor = triad_tensor()
    assert len(tensor) == 7
    assert all(len(row) == 7 for row in tensor)
    assert tensor_trace(tensor) == pytest.approx(300.0)


def test_constants() -> None:
    assert ANGLE_DEGREES == pytest.approx(36.2042)
    assert GAMMA == pytest.approx(2.691602)
    assert RESONANCE_HZ == pytest.approx(46.62)
