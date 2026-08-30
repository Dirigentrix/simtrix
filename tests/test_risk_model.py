"""Tests for the SIMTRIX risk model."""

from simtrix.operator_core import RISK_THRESHOLD, RiskModel


def test_low_risk_below_threshold() -> None:
    model = RiskModel()
    assert model.classify(RISK_THRESHOLD - 0.01) == "LOW"


def test_high_risk_at_or_above_threshold() -> None:
    model = RiskModel()
    assert model.classify(RISK_THRESHOLD) == "HIGH"
    assert model.classify(1.0) == "HIGH"
