"""Tests for the SIMTRIX operator core."""

from simtrix.operator_core import CORE_ID, RISK_THRESHOLD, SimtrixOperatorCore


def test_risk_threshold_boundary() -> None:
    core = SimtrixOperatorCore()
    assert core.evaluate(RISK_THRESHOLD)["risk_class"] == "HIGH"
    assert core.evaluate(RISK_THRESHOLD - 0.01)["risk_class"] == "LOW"


def test_core_identifier() -> None:
    result = SimtrixOperatorCore().evaluate()
    assert result["core_id"] == CORE_ID == 181141


def test_diagnostics_return_structure() -> None:
    diagnostics = SimtrixOperatorCore().diagnostics()
    assert {"tensor_size", "tensor_trace", "angle_degrees", "gamma", "symbolic_algebra_self_test", "induction_steps"} <= diagnostics.keys()
    assert diagnostics["tensor_size"] == "7x7"
    assert diagnostics["tensor_trace"] == 300.0
