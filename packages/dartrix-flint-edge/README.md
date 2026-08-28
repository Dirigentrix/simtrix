# DARTRIX-FLINT-EDGE v1.0

A small, dependency-free Python edge core for coordinating GEA telemetry, Ishida program data, brine-layer physics, and feed-stream coupling.

The engine is intentionally deterministic: telemetry is normalized into phase events, the phase bus fans events out to subscribers, and each tick advances the physical model. Constants encode the v1.0 plant contract.

## Quick start

```python
from core.engine import FlintEdgeEngine

engine = FlintEdgeEngine()
engine.ingest_gea({"cycle_ms": 730, "phase": "fill"})
engine.ingest_ishida("PROGRAM=002;WEIGHT_G=1250;PHASE=DISCHARGE")
state = engine.tick()
```

The package is laid out as a `src` distribution and has no runtime dependencies.
