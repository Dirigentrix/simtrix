import numpy as np
import time
import math
import sys
from typing import Dict, Any, Tuple


class DartrixFlowMatrixEngine:
    """
    Silnik Macierzy Przepływu DARTRIX (M_flow)
    Zsynchronizowany ze struną SIMTRIX (46.62 Hz) oraz osiami F_L, F_R, F_axis, F_time.
    """
    def __init__(self, base_freq: float = 46.62):
        self.base_freq = base_freq
        
        # DEFINICJA MACIERZY PRZEPŁYWU M_flow (4x4)
        # Row 0: F_L    (FIBERS - Wejście/Sensory)
        # Row 1: F_R    (RESPONSE - Wykonanie/SIOMTRIX)
        # Row 2: F_axis (FUNCTION - Rezonans 888Hz / XOR)
        # Row 3: F_time (EVOLUTION - Czas/12-D)
        self.m_flow = np.array([
            [1.00, 0.15, 0.00, 0.05],
            [0.20, 1.00, 0.35, 0.00],
            [0.00, 0.25, 1.00, 0.20],
            [0.10, 0.00, 0.15, 1.00]
        ], dtype=np.float64)

    def calculate_resonance_vector(self, triada_vector: np.ndarray, timestamp: float) -> Tuple[np.ndarray, float]:
        """
        Mnożenie macierzowe: F_out = M_flow * Triada_Input * S(46.62, t)
        """
        # Stan struny SIMTRIX S(46.62, t)
        string_phase = math.sin(2 * math.pi * self.base_freq * timestamp)
        
        # Transformacja macierzowa
        transformed_vector = np.dot(self.m_flow, triada_vector)
        
        # Sprzężenie rezonansowe z wyciszeniem szumu (XOR Component)
        f_vector = transformed_vector * string_phase
        return f_vector, string_phase


class KartrixTerminalCLI:
    """
    Interaktywny Terminal KARTRIX
    Zarządza wprowadzaniem poleceń, wizualizacją macierzy i generowaniem wektorów sterujących.
    """
    def __init__(self):
        self.engine = DartrixFlowMatrixEngine()
        self.start_time = time.time()
        self.is_running = True

    def render_header(self):
        print("═" * 75)
        print(" ⚡ TERMINAL KARTRIX v4.0 — INTERFEJS MACIERZY PRZEPŁYWU (M_flow)")
        print("    DARTRIX Core (888Hz) ⊗ SIMTRIX String Engine (46.62Hz)")
        print("═" * 75)
        print(" System gotowy. Wprowadź wektor Triady: [Diagnosta, Wilk, Hydra, Ryzyko]")
        print(" Dostępne komendy: 'exit' - wyjście, 'matrix' - podgląd M_flow, 'pulse' - cykl ciągły\n")

    def display_matrix(self):
        print("\n 📐 BAZOWA MACIERZ PRZEPŁYWU DARTRIX (M_flow):")
        labels = ["F_L (Fibers)  ", "F_R (Response)", "F_axis (Rezon)", "F_time (Evol) "]
        print("                   F_L    F_R   F_axis F_time")
        for idx, row in enumerate(self.engine.m_flow):
            formatted_row = "  ".join(f"{val:6.2f}" for val in row)
            print(f" {labels[idx]} | {formatted_row} |")
        print()

    def process_command(self, raw_input: str):
        cmd = raw_input.strip().lower()

        if cmd == "exit":
            print("\n⏹ Zamykanie Terminala KARTRIX. Rezonans 888Hz wstrzymany.")
            self.is_running = False
            return

        elif cmd == "matrix":
            self.display_matrix()
            return

        elif cmd == "pulse":
            self.run_pulse_mode(cycles=5)
            return

        # Próba sparsowania 4 wartości numerycznych dla Triady
        try:
            parts = [float(x) for x in raw_input.replace(",", " ").split()]
            if len(parts) != 4:
                print("❌ BŁĄD: Wprowadź dokładnie 4 wartości liczbowe (np. 0.8 0.9 0.7 0.3)")
                return
            
            triada = np.array(parts, dtype=np.float64)
            self.execute_flow_calculation(triada)

        except ValueError:
            print("❌ BŁĄD: Niepoprawny format danych. Użyj liczb oddzielonych spacjami.")

    def execute_flow_calculation(self, triada: np.ndarray):
        current_t = time.time() - self.start_time
        f_vec, phase = self.engine.calculate_resonance_vector(triada, current_t)

        print(f"\n 📊 [ANALIZA SYGNAŁU] t={current_t:.3f}s | Faza SIMTRIX (46.62Hz): {phase:+.4f}")
        print(" ─────────────────────────────────────────────────────────")
        print(f"  • WEJŚCIE TRIADY  -> Diagnosta: {triada[0]:.2f} | Wilk: {triada[1]:.2f} | Hydra: {triada[2]:.2f} | Ryzyko: {triada[3]:.2f}")
        print(f"  • WEKTOR F_out    -> F_L: {f_vec[0]:+7.4f}  (FIBERS / Line)")
        print(f"                       F_R: {f_vec[1]:+7.4f}  (RESPONSE / SIOMTRIX)")
        print(f"                       F_axis: {f_vec[2]:+7.4f}  (FUNCTION / 888Hz)")
        print(f"                       F_time: {f_vec[3]:+7.4f}  (EVOLUTION / Time)")
        print(" ─────────────────────────────────────────────────────────")
        
        # Generowanie przykładowej ramki KARTRIX dla maszyny/agenta
        kartrix_cmd = {
            "target": "SIOMTRIX_EXECUTION_LAYER",
            "power_output_pct": round(abs(float(f_vec[1])) * 100, 2),
            "xor_stability_index": round(float(f_vec[2]), 4),
            "status": "OPTIMAL" if abs(f_vec[2]) > 0.1 else "NOISE_REDUCED"
        }
        print(f" ⚙️ [KARTRIX COMMAND FRAME]: {kartrix_cmd}\n")

    def run_pulse_mode(self, cycles: int = 5):
        print(f"\n🔄 Uruchamianie trybu PULSE ({cycles} cykli rezonansowych)...")
        dummy_triada = np.array([0.85, 0.90, 0.75, 0.20])
        for i in range(1, cycles + 1):
            print(f"\n--- PULSE #{i} ---")
            self.execute_flow_calculation(dummy_triada)
            time.sleep(0.3)

    def start(self):
        self.render_header()
        while self.is_running:
            try:
                user_in = input("KARTRIX> ")
                if user_in.strip():
                    self.process_command(user_in)
            except KeyboardInterrupt:
                print("\n⏹ Przerwanie z poziomu konsoli.")
                break


if __name__ == "__main__":
    terminal = KartrixTerminalCLI()
    terminal.start()
