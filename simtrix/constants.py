"""
SIMTRIX — Stałe systemu DARTRIX / Wankel OS
Warstwa I: Aramejska Matematyka Rdzeniowa
Wartości zgodne z pełną specyfikacją z 30.08.2026
"""

# Wektor Życia — 24 rdzenie, podzielone na 4 podprzestrzenie
CHRONOS = (5, 3, 1, 9, 8, 8)       # 6 rdzeni
DANIEL  = (4, 50, 10, 1, 10, 30)   # 6 rdzeni
ADRIAN  = (1, 4, 200, 10, 50)      # 5 rdzeni
RATAJCZYK = (200, 9, 1, 400, 300, 10, 20)  # 7 rdzeni

ALL_CORES = CHRONOS + DANIEL + ADRIAN + RATAJCZYK  # Razem: 24 rdzenie

# Niezredukowane stany KOSA
K_SUM = sum(CHRONOS)   # 34
O_SUM = sum(DANIEL)    # 105
S_SUM = sum(ADRIAN)    # 265
A_SUM = sum(RATAJCZYK) # 940

# Master Seed — globalny stan organizmu
MASTER_SEED = K_SUM + O_SUM + S_SUM + A_SUM  # 1344

# NATURE — Flora i Fauna jako rdzenie wektorowe
FLORA = {
    "swierk":   (300, 200, 20),
    "brzoza":   (2, 200, 7, 1),
    "jablon":   (400, 80, 8, 1),
}

FAUNA = {
    "wilk":     (6, 30, 200),
    "ptak":     (10, 40, 70),
    "pies":     (2, 10, 50),
    "kot":      (20, 9, 300),
}

# Semantyka podprzestrzeni
SUBSPACE = {
    "chronos":   ("czas", "impuls", "gęstość", "energia"),
    "daniel":    ("stabilność", "punkt_zerowy", "modulacja"),
    "adrian":    ("masa_logiczna", "waga_decyzji"),
    "ratajczyk": ("struktura", "napięcie", "topologia"),
}
