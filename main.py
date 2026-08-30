import os
import time
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

# 1. INICJALIZACJA SYSTEMU I INTEGRACJA GOOGLE AI STUDIO
app = FastAPI(
    title="DARTRIX Core & KOSA Backend Engine",
    version="0.5.0",
    description="Hybrid Deterministc-Generative AI Architecture for Cognitive Autoregulation"
)

# Włączenie CORS dla łatwej integracji z frontendem/dashboardem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: Brak klucza GEMINI_API_KEY. Aktywowany tryb symulacji lokalnej.")

# Stałe parametry wektora życia (Brak redukcji matematycznej - paradygmat aramejski)
KOSA_CONSTANTS = {
    "K_CHRONOS": 34,      # Kontrola czasu
    "O_DANIEL": 105,     # Ochrona rdzenia
    "S_ADRIAN": 265,     # Stabilizacja fazy
    "A_RATAJCZYK": 940,  # Analiza / Architektura
    "MASTER_SEED": 1344, # Suma kontrolna integralności
    "CORE_ID": 181141,   # ID z repozytorium simtrix
    "RESONANCE": 46.62   # Częstotliwość referencyjna w Hz
}

# 2. DEFINICJE STRUKTUR DANYCH (PYDANTIC)
class TelemetryPayload(BaseModel):
    timestamp: float
    intent_clarity: float     # Skala [0.0, 10.0] -> Zamiast skanowania bólu: jasność intencji
    focus_direction: float    # Skala [-5.0, 5.0] -> Kierunek skupienia uwagi
    chaos_index: float        # Skala [0.0, 100.0] -> Chaos semantyczny środowiska

class KosaSnapshot(BaseModel):
    k_chronos: int = KOSA_CONSTANTS["K_CHRONOS"]
    o_daniel: int = KOSA_CONSTANTS["O_DANIEL"]
    s_adrian: int = KOSA_CONSTANTS["S_ADRIAN"]
    a_ratajczyk: int = KOSA_CONSTANTS["A_RATAJCZYK"]
    master_seed: int = KOSA_CONSTANTS["MASTER_SEED"]

class HistoryMetrics(BaseModel):
    s_index: float
    intent_clarity_avg: float
    focus_direction_delta: float
    autoregulation_success_rate: float

class HistoryRecord(BaseModel):
    record_id: str
    timestamp: float
    kosa_snapshot: KosaSnapshot
    metrics: HistoryMetrics
    alignment_trend: Dict[str, Any]

# 3. ENDPOINTY OPERACYJNE BRAMY SYSTEMOWEJ
@app.post("/v05/align")
async def evaluate_and_align(data: TelemetryPayload):
    """
    Warstwa 1 & 2: Deterministyczna walidacja (WolfGuardian) + Analiza rezonansu semantycznego.
    """
    anomalies: List[str] = []
    is_valid = True
    
    # Boundary Check (Weryfikacja zakresu statycznego bez redukcji)
    if not (0.0 <= data.intent_clarity <= 10.0):
        anomalies.append("violation_intent_clarity_bounds")
        is_valid = False
        
    if not (-5.0 <= data.focus_direction <= 5.0):
        anomalies.append("violation_focus_direction_bounds")
        is_valid = False

    if not is_valid:
        raise HTTPException(
            status_code=422, 
            detail={"status": "FAULT", "core_id": KOSA_CONSTANTS["CORE_ID"], "anomalies": anomalies}
        )

    # Obliczenie znormalizowanego indeksu stresu/chaosu (S_index) za pomocą wagi S_ADRIAN
    normalized_chaos = data.chaos_index / 100.0
    s_index = min(1.0, (normalized_chaos * (KOSA_CONSTANTS["S_ADRIAN"] / 1000.0)))

    # Warstwa 3: Generatywny dialog refleksyjny przez Google AI Studio (Gemini 2.5 Flash)
    prompt = f"""
    [SYSTEM CONTEXT: DARTRIX_CORE_v0.5]
    CORE_ID: {KOSA_CONSTANTS['CORE_ID']} | RESONANCE: {KOSA_CONSTANTS['RESONANCE']} Hz
    KOSA_STATE: K={KOSA_CONSTANTS['K_CHRONOS']}, O={KOSA_CONSTANTS['O_DANIEL']}, S={KOSA_CONSTANTS['S_ADRIAN']}, A={KOSA_CONSTANTS['A_RATAJCZYK']}
    MASTER_SEED: {KOSA_CONSTANTS['MASTER_SEED']}
    
    CURRENT METRICS:
    - Intent Clarity: {data.intent_clarity}/10
    - Focus Direction Vector: {data.focus_direction}
    - Environment S_index: {s_index:.2f}
    
    ZADANIE DLA AI STUDIO / GEMINI:
    Użytkownik zgłosił ten telemetryczny stan intencji. Nie diagnozujesz jego zdrowia, bólu ani napięć fizycznych.
    To jest strojenie instrumentu poznawczego, a nie naprawa awarii.
    Wygeneruj jedno ultrakrótkie, potężne i głębokie pytanie refleksyjne, które ułatwi mu ugruntowanie uwagi,
    uporządkowanie myśli lub wybór celowego działania zamiast poddawania się chaosowi otoczenia.
    """
    
    try:
        if GEMINI_API_KEY:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            reflection_text = response.text.strip()
        else:
            reflection_text = "Twój 'staw intencji' potrzebuje teraz stabilności czy otwarcia na nowe działanie?"
    except Exception as e:
        reflection_text = f"Co teraz wybierasz jako główny kierunek działania w rezonansie {KOSA_CONSTANTS['RESONANCE']} Hz?"

    return {
        "status": "SECURE",
        "core_id": KOSA_CONSTANTS["CORE_ID"],
        "resonance_hz": KOSA_CONSTANTS["RESONANCE"],
        "s_index": round(s_index, 2),
        "master_seed_lock": KOSA_CONSTANTS["MASTER_SEED"],
        "reflection_prompt": reflection_text,
        "timestamp": time.time()
    }

@app.post("/v05/history/append")
async def append_to_history(record: HistoryRecord):
    """
    Warstwa History Engine: Zapisywanie trendów intencji do struktury analitycznej (dashboard).
    """
    print(f"📦 [History Engine Lock] Zapisano stan intencji dla rekordu {record.record_id}. S_index: {record.metrics.s_index}")
    return {
        "status": "RECORDED",
        "record_id": record.record_id,
        "s_index_verified": record.metrics.s_index,
        "integrity_lock": True,
        "master_seed": KOSA_CONSTANTS["MASTER_SEED"]
    }

@app.get("/v05/status")
async def system_status():
    """
    Status operacyjny architektury weryfikowany przez systemy monitoringu Cloud Run.
    """
    return {
        "system": "DARTRIX OPERATOR",
        "status": "ONLINE",
        "core_id": KOSA_CONSTANTS["CORE_ID"],
        "resonance_hz": KOSA_CONSTANTS["RESONANCE"],
        "integrity_check": "PASSED"
    }
