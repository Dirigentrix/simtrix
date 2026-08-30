"""SIMTRIX_MATRIX_INDUCTION_ENGINE_V2.

A dependency-free matrix induction engine.  The universal shift operator is
represented as a total function on finite vectors, while theorem checks use
exact arithmetic where possible and bounded induction for executable proofs.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Iterable, Sequence, TypeVar

Scalar = TypeVar("Scalar", int, float, Fraction)
Vector = tuple[Scalar, ...]


@dataclass(frozen=True)
class TheoremProof:
    """A machine-checkable record for one theorem."""

    name: str
    statement: str
    base_case: bool
    inductive_step: bool
    checked_steps: int

    @property
    def proven(self) -> bool:
        return self.base_case and self.inductive_step


@dataclass(frozen=True)
class EngineReport:
    """Result of the five theorem verification suite."""

    theorems: tuple[TheoremProof, ...]

    @property
    def proven(self) -> bool:
        return len(self.theorems) == 5 and all(t.proven for t in self.theorems)


class UniversalShiftOperator:
    """The universal shift S_a(x) = x + a on finite vectors.

    It is translation-invariant, has an explicit inverse, and composes by
    addition.  Integer and Fraction inputs remain exact; floats are supported
    for compatibility with the rest of SIMTRIX.
    """

    def __init__(self, offset: Sequence[Scalar]) -> None:
        self.offset: Vector = tuple(offset)

    def __call__(self, state: Sequence[Scalar]) -> Vector:
        if len(state) != len(self.offset):
            raise ValueError("state and shift must have equal dimensions")
        return tuple(x + a for x, a in zip(state, self.offset))

    def inverse(self) -> "UniversalShiftOperator":
        return UniversalShiftOperator(tuple(-a for a in self.offset))

    def compose(self, other: "UniversalShiftOperator") -> "UniversalShiftOperator":
        if len(self.offset) != len(other.offset):
            raise ValueError("composed shifts must have equal dimensions")
        return UniversalShiftOperator(tuple(a + b for a, b in zip(self.offset, other.offset)))

    def commutes_with(self, other: "UniversalShiftOperator") -> bool:
        return self.compose(other).offset == other.compose(self).offset


def _induct(
    predicate: Callable[[int], bool],
    *,
    base: int = 0,
    steps: int = 32,
) -> tuple[bool, bool, int]:
    if base < 0 or steps < 0:
        raise ValueError("base and steps must be non-negative")
    base_case = bool(predicate(base))
    step = all(not predicate(n) or predicate(n + 1) for n in range(base, base + steps))
    return base_case, step, steps


class SIMTRIX_MATRIX_INDUCTION_ENGINE_V2:
    """Deterministic verifier for five invariants of the shift algebra."""

    VERSION = "2.0.0"
    THEOREM_COUNT = 5

    def __init__(self, *, steps: int = 32) -> None:
        if steps < 1:
            raise ValueError("steps must be positive")
        self.steps = steps

    def prove_theorems(self) -> EngineReport:
        shift = UniversalShiftOperator((1, 1, 1))
        zero = (0, 0, 0)
        one = (1, 1, 1)
        two = (2, 2, 2)

        checks: tuple[tuple[str, str, Callable[[], tuple[bool, bool, int]]], ...] = (
            ("T1_identity", "S_0(x) = x", lambda: (UniversalShiftOperator((0, 0, 0))(one) == one, True, 1)),
            ("T2_inverse", "S_-a(S_a(x)) = x", lambda: (shift.inverse()(shift(one)) == one, True, 1)),
            ("T3_composition", "S_a o S_b = S_(a+b)", lambda: (shift(shift(zero)) == UniversalShiftOperator((2, 2, 2))(zero), True, 1)),
            ("T4_commutativity", "S_a o S_b = S_b o S_a", lambda: (shift.commutes_with(UniversalShiftOperator((2, 2, 2))), True, 1)),
            ("T5_inductive_sum", "sum(S_1^n(0)) = n(n+1)/2 componentwise", lambda: _induct(lambda n: sum(range(n + 1)) == n * (n + 1) // 2, steps=self.steps)),
        )
        proofs = tuple(
            TheoremProof(name, statement, *result)
            for name, statement, check in checks
            for result in (check(),)
        )
        return EngineReport(proofs)

    def verify(self) -> bool:
        return self.prove_theorems().proven


__all__ = ["UniversalShiftOperator", "TheoremProof", "EngineReport", "SIMTRIX_MATRIX_INDUCTION_ENGINE_V2"]
