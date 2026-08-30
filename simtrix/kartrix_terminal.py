"""
KARTRIX Terminal — Rozszerzone komendy DARTRIX / Wankel OS
Komendy: KX:CORE.*, KX:NATURE.*
"""
import sys
from simtrix.constants import MASTER_SEED, FLORA, FAUNA
from simtrix.wankel_cpu import WankelCPU


class KartrixTerminal:
    def __init__(self):
        self.cpu = WankelCPU()
        self.state = None

    def run(self, argv):
        if not argv:
            self._help()
            return

        cmd = argv[0].upper()

        # ─── CORE ───
        if cmd == "KX:CORE.RUN":
            seed = int(argv[1].split("=")[1]) if len(argv) > 1 else MASTER_SEED
            self.state = self.cpu.seed_state(seed)
            print(f"✅ Stan zainicjowany. SEED = {seed}")

        elif cmd == "KX:CORE.CYCLE":
            if self.state is None:
                print("⚠️  Najpierw uruchom: KX:CORE.RUN")
                return
            mode = argv[1].split("=")[1] if len(argv) > 1 else "WANKEL"
            self.state = self.cpu.cycle(self.state, mode)
            print(f"✅ Cykl wykonany. Cykl nr: {self.state['cycle']}, Energia: {self.state['energy']}")

        elif cmd == "KX:CORE.TRACE":
            if self.state is None:
                print("⚠️  Najpierw uruchom: KX:CORE.RUN")
                return
            depth = int(argv[1].split("=")[1]) if len(argv) > 1 else 24
            print(f"📜 Ślad (głębokość {depth}):")
            for step in self.state["trace"][-depth:]:
                print(f"  Rdzeń {step['core_id']:2d} | {step['source']:10s} | {step['operator']:12s} | wartość: {step['value']}")

        # ─── NATURE ───
        elif cmd.startswith("KX:NATURE.ADD_TREE"):
            t = argv[1].split("=")[1].lower() if len(argv) > 1 else ""
            if t in FLORA:
                print(f"🌲 Dodano drzewo: {t.upper()} → rdzeń = {FLORA[t]}")
            else:
                print(f"❌ Nieznany typ drzewa: {t}")

        elif cmd.startswith("KX:NATURE.ADD_FAUNA"):
            a = argv[1].split("=")[1].lower() if len(argv) > 1 else ""
            if a in FAUNA:
                print(f"🦊 Dodano zwierzę: {a.upper()} → rdzeń = {FAUNA[a]}")
            else:
                print(f"❌ Nieznany typ: {a}")

        else:
            print(f"❌ Nieznana komenda: {cmd}")
            self._help()

    def _help(self):
        print("""
KARTRIX Terminal — DARTRIX / Wankel OS
────────────────────────────────────────
KX:CORE.RUN --SEED=1344         Inicjalizuj stan organizmu
KX:CORE.CYCLE --MODE=WANKEL     Pełny cykl przez 24 rdzenie
KX:CORE.TRACE --DEPTH=24       Pokaż ścieżkę przetworzenia

KX:NATURE.ADD_TREE --TYPE=SWIERK
KX:NATURE.ADD_TREE --TYPE=BRZOZA
KX:NATURE.ADD_TREE --TYPE=JABLON

KX:NATURE.ADD_FAUNA --TYPE=WILK
KX:NATURE.ADD_FAUNA --TYPE=PTAK
KX:NATURE.ADD_FAUNA --TYPE=PIES
KX:NATURE.ADD_FAUNA --TYPE=KOT
        """.strip())


if __name__ == "__main__":
    KartrixTerminal().run(sys.argv[1:])
