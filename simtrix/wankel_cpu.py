"""
SIMTRIX — WankelCPU
Warstwa II: 24-rdzeniowy procesor wykonawczy DARTRIX
Cykl sekwencyjny: state -> O1 -> O2 -> ... -> O24
"""
from .constants import ALL_CORES, MASTER_SEED, SUBSPACE


class WankelCore:
    """Pojedynczy rdzeń przetwarzający stan organizmu."""

    def __init__(self, core_id: int, value: int, source: str, operator: str):
        self.id = core_id
        self.value = value
        self.source = source
        self.operator = operator

    def apply(self, state: dict) -> dict:
        """Zastosuj operator rdzenia do stanu, zwróć nowy stan."""
        new_state = state.copy()
        new_state["trace"].append({
            "core_id": self.id,
            "source": self.source,
            "operator": self.operator,
            "value": self.value,
        })
        # Waga rdzenia modyfikuje energię stanu
        new_state["energy"] = (new_state["energy"] * self.value) % MASTER_SEED
        return new_state


class WankelCPU:
    """24-rdzeniowy procesor — serce DARTRIX / Wankel OS."""

    def __init__(self):
        self.cores = self._build_cores()

    def _build_cores(self) -> list:
        """Zbuduj wszystkie rdzenie z przypisaniem do podprzestrzeni."""
        sources = (["chronos"]*6) + (["daniel"]*6) + (["adrian"]*5) + (["ratajczyk"]*7)
        ops = []
        for src in sources:
            ops.extend(SUBSPACE[src])
        # Wypełnij do 24 operatorów
        while len(ops) < 24:
            ops.append("transform")

        return [
            WankelCore(idx, val, src, op)
            for idx, (val, src, op) in enumerate(zip(ALL_CORES, sources, ops), 1)
        ]

    def seed_state(self, seed: int = MASTER_SEED) -> dict:
        """Stwórz początkowy stan organizmu z podanym nasionem."""
        return {
            "seed": seed,
            "energy": seed,
            "cycle": 0,
            "trace": [],
            "nature": {"trees": {}, "fauna": {}},
        }

    def cycle(self, state: dict, mode: str = "WANKEL") -> dict:
        """Wykonaj pełny cykl przez wszystkie 24 rdzenie."""
        if mode != "WANKEL":
            raise ValueError(f"Tryb nieobsługiwany: {mode}")

        state = state.copy()
        state["cycle"] += 1

        for core in self.cores:
            state = core.apply(state)

        return state

    def trace_depth(self, state: dict) -> int:
        """Zwróć głębokość ścieżki przetworzenia."""
        return len(state["trace"])
