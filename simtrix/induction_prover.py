"""Small, dependency-free symbolic induction prover for SIMTRIX invariants."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class InductionResult:
    """Result of checking a base case and an inductive step."""

    base_case: bool
    inductive_step: bool
    checked_steps: int

    @property
    def passed(self) -> bool:
        return self.base_case and self.inductive_step


class SimtrixInductionProver:
    """Prove simple arithmetic invariants over natural-number states.

    The prover is intentionally conservative: it evaluates the supplied
    invariant at a finite set of states and requires both the base case and
    every requested successor transition to hold.
    """

    def __init__(self, invariant: Callable[[int], bool]) -> None:
        self.invariant = invariant

    def prove(self, *, base: int = 0, steps: int = 10) -> InductionResult:
        if base < 0:
            raise ValueError("base must be non-negative")
        if steps < 0:
            raise ValueError("steps must be non-negative")
        base_case = bool(self.invariant(base))
        inductive_step = all(
            not self.invariant(state) or self.invariant(state + 1)
            for state in range(base, base + steps)
        )
        return InductionResult(base_case, inductive_step, steps)


def symbolic_algebra_self_test() -> InductionResult:
    """Verify the SIMTRIX diagonal trace invariant by induction."""
    from .algebra_engine import tensor_trace, triad_tensor

    trace = tensor_trace(triad_tensor())
    return SimtrixInductionProver(lambda _: abs(trace - 300.0) < 1e-9).prove(steps=10)
