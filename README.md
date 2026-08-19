# SIMTRIX

SIMTRIX to bez-zależnościowy rdzeń operatora Triady oraz deterministyczny silnik algebraiczny w Pythonie 3.10+.

## Architektura

Pakiet składa się z dwóch warstw:

- `operator_core.py` — fasada `SimtrixOperatorCore`, model ryzyka i orkiestracja Triady.
- `algebra_engine.py` — czyste funkcje algebry wektorowej i tensorowej, bez bibliotek zewnętrznych.

`__init__.py` udostępnia klasę rdzenia i wersję `0.1.0`, a `__main__.py` umożliwia uruchomienie pakietowe.

## Triada

Triada łączy trzy perspektywy:

1. Diagnosta — identyfikacja stanu, pomiar i klasyfikacja.
2. Wilk — heurystyka decyzyjna, kierunek działania i odporność.
3. Hydra — równoległe rozważanie wariantów oraz kontrola skutków ubocznych.

Operator scala wynik w jeden rekord: identyfikator rdzenia `181141`, wersję, stan ryzyka i parametry rezonansu.

## Model ryzyka

`RiskModel` przyjmuje wynik z przedziału `[0, 1]`. Próg decyzyjny wynosi `0.72`:

- wynik `< 0.72` → `LOW`,
- wynik `>= 0.72` → `HIGH`.

Rezonans referencyjny wynosi `46.62 Hz`, a współczynnik gamma `2.691602`.

## Dekompozycja algebraiczna

Silnik definiuje trzy wektory SIMTRIX, DARTRIX i SIMU-SION. Wektor bazowy `(10, 10, 10)` ma normę:

`||v|| = sqrt(10² + 10² + 10²) = sqrt(300) = 17.320508...`

`triad_tensor()` buduje tensor `7 x 7` diagonalny, z elementami `300/7`, dlatego jego ślad wynosi dokładnie `300`. Zdefiniowany kąt referencyjny to `36.2042°`. Rezonans jest parametrem `46.62 Hz`; relacja skali jest zapisana przez `gamma = 2.691602`.

## Uruchomienie CLI

Z katalogu głównego repozytorium:

```bash
python -m simtrix
python -m simtrix --risk 0.8
python -m simtrix --diagnostics
```

## Użycie pakietowe

```python
from simtrix import SimtrixOperatorCore

core = SimtrixOperatorCore()
print(core.evaluate(0.5))
print(core.diagnostics())
```

Projekt używa wyłącznie biblioteki standardowej Pythona i nie wymaga instalowania zależności zewnętrznych. Licencję i dalsze testy można dodać w kolejnych commitach.
