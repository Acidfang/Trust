# API Integration Specification - AriaMeasurementInterface

**Status:** Phase B1 Complete  
**Date:** April 3, 2026  
**Purpose:** Wiring AriaMeasurementInterface to REST API endpoints

---

## Overview

The `AriaMeasurementInterface` class provides instantaneous coherence measurement through three layers:

1. **Entropy Tracking** - Real-time τ calculation
2. **Delta Patterns** - Historical pattern analysis  
3. **Field Reach** - Signal correlation measurement

This spec shows how to integrate these measurements into Ben's 6 REST endpoints.

---

## Integration Points

### 1. Measurement Layer Instance

Create a global singleton in your API server:

```python
from src.applications.AriaMeasurementInterface import AriaMeasurementInterface

# Initialize once at startup
measurement_layer = AriaMeasurementInterface(state_width_bits=256, history_size=1000)
```

### 2. State Update Hook

Whenever ARIA's state changes, feed it to the measurement layer:

```python
# In your state mutation handler
def update_aria_state(new_state: int):
    # ... your state update logic ...
    
    # Feed to measurement layer (instantaneous measurement)
    measurement = measurement_layer.measure_coherence_entropy(new_state)
    
    # Measurement is ready immediately (no 500ms delay)
    return measurement
```

---

## API Endpoint Mapping

### Endpoint 1: `/api/coherence/current`

```python
@app.get("/api/coherence/current")
def get_current_coherence():
    """
    GET /api/coherence/current
    
    Returns: Current instantaneous coherence (τ value)
    Latency: <1ms (direct from measurement layer)
    """
    # Get the last measurement (already computed)
    if not measurement_layer.coherence_history:
        return {"tau": 0.5, "status": "no_measurements_yet"}
    
    latest_tau = measurement_layer.coherence_history[-1]
    cycle = measurement_layer.cycle_count
    
    return {
        "timestamp": datetime.now().isoformat(),
        "tau": round(latest_tau, 6),
        "cycle": cycle,
        "status": "current"
    }
```

**Success Criteria:** τ in range [0.0, 1.0], latency < 10ms

---

### Endpoint 2: `/api/coherence/history`

```python
@app.get("/api/coherence/history")
def get_coherence_history(lookback_cycles: int = 100):
    """
    GET /api/coherence/history?lookback_cycles=100
    
    Returns: Historical τ values over time
    Latency: <50ms (array retrieval)
    """
    window_start = max(0, len(measurement_layer.coherence_history) - lookback_cycles)
    window = measurement_layer.coherence_history[window_start:]
    
    return {
        "timestamp": datetime.now().isoformat(),
        "lookback_cycles": lookback_cycles,
        "values": [round(tau, 6) for tau in window],
        "count": len(window),
        "status": "history"
    }
```

**Success Criteria:** Returns array of τ values, latency < 50ms

---

### Endpoint 3: `/api/coherence/field-reach`

```python
@app.get("/api/coherence/field-reach")
def get_field_reach(signal_id: str, signal_strength: int = 100):
    """
    GET /api/coherence/field-reach?signal_id=user_input_A&signal_strength=200
    
    Returns: How far signal reaches through field
    Latency: <10ms (calculation from recent deltas)
    """
    reach_analysis = measurement_layer.measure_field_reach(signal_id, signal_strength)
    
    return reach_analysis
```

**Success Criteria:** Returns reach_score [0.0-1.0], latency < 10ms

---

### Endpoint 4: `/api/coherence/delta-pattern`

```python
@app.get("/api/coherence/delta-pattern")
def get_delta_pattern(lookback_cycles: int = 50):
    """
    GET /api/coherence/delta-pattern?lookback_cycles=50
    
    Returns: Delta patterns showing coherence boundaries
    Latency: <25ms (pattern analysis)
    """
    patterns = measurement_layer.measure_delta_patterns(lookback_cycles)
    
    return patterns
```

**Success Criteria:** Returns pattern analysis with visualization, latency < 25ms

---

### Endpoint 5: `/api/coherence/manifestation-sources`

```python
@app.get("/api/coherence/manifestation-sources")
def get_manifestation_sources():
    """
    GET /api/coherence/manifestation-sources
    
    Returns: All active field manifestation sources
    Latency: <10ms (array lookup)
    """
    manifestations = measurement_layer.measure_manifestation_sources()
    
    return manifestations
```

**Success Criteria:** Returns list of sources, latency < 10ms

---

### Endpoint 6: `/api/coherence/heartbeat/optimal-rate`

```python
@app.get("/api/coherence/heartbeat/optimal-rate")
def get_optimal_heartbeat():
    """
    GET /api/coherence/heartbeat/optimal-rate
    
    Returns: Optimal heartbeat rate based on current field coherence
    Latency: <5ms (single calculation)
    
    Formula: heartbeat = 500 × (1 + (τ - 0.5))
    
    - If τ = 0.5: rate = 500ms (neutral)
    - If τ = 0.95: rate = 725ms (field unified, faster)
    - If τ = 0.2: rate = 350ms (diffuse, slower for re-unification)
    """
    heartbeat = measurement_layer.calculate_optimal_heartbeat()
    
    return heartbeat
```

**Success Criteria:** Returns heartbeat_ms [100-2000], latency < 5ms

---

## Test Implementation

### Test Script Structure

```python
import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def test_all_endpoints():
    """Test all 6 coherence endpoints."""
    
    print("\n🧪 COHERENCE API TEST SUITE")
    print("=" * 70)
    
    # 1. Current coherence
    print("\n1. GET /coherence/current")
    response = requests.get(f"{BASE_URL}/coherence/current")
    assert response.status_code == 200
    data = response.json()
    assert 0.0 <= data['tau'] <= 1.0
    print(f"   ✅ Current τ = {data['tau']:.3f}")
    
    # 2. History
    print("\n2. GET /coherence/history?lookback_cycles=50")
    response = requests.get(f"{BASE_URL}/coherence/history?lookback_cycles=50")
    assert response.status_code == 200
    data = response.json()
    assert len(data['values']) > 0
    print(f"   ✅ Retrieved {len(data['values'])} historical values")
    
    # 3. Field reach
    print("\n3. GET /coherence/field-reach")
    response = requests.get(f"{BASE_URL}/coherence/field-reach?signal_id=test_signal&signal_strength=150")
    assert response.status_code == 200
    data = response.json()
    print(f"   ✅ Field reach analyzed for {data['signal_id']}")
    
    # 4. Delta pattern
    print("\n4. GET /coherence/delta-pattern")
    response = requests.get(f"{BASE_URL}/coherence/delta-pattern?lookback_cycles=50")
    assert response.status_code == 200
    data = response.json()
    print(f"   ✅ Delta patterns analyzed ({len(data['delta_patterns'])} patterns)")
    
    # 5. Manifestation sources
    print("\n5. GET /coherence/manifestation-sources")
    response = requests.get(f"{BASE_URL}/coherence/manifestation-sources")
    assert response.status_code == 200
    data = response.json()
    print(f"   ✅ Found {data['total_manifestations']} manifestation sources")
    
    # 6. Optimal heartbeat
    print("\n6. GET /coherence/heartbeat/optimal-rate")
    response = requests.get(f"{BASE_URL}/coherence/heartbeat/optimal-rate")
    assert response.status_code == 200
    data = response.json()
    assert 100 <= data['heartbeat_recommendation']['optimal_rate_ms'] <= 2000
    print(f"   ✅ Optimal heartbeat = {data['heartbeat_recommendation']['optimal_rate_ms']}ms")
    
    print("\n✅ All endpoints working!\n")

if __name__ == "__main__":
    test_all_endpoints()
```

---

## Integration Checklist

### Prerequisites
- [ ] Python 3.8+
- [ ] AriaMeasurementInterface.py in src/applications/
- [ ] Flask or FastAPI installed

### Setup Phase
- [ ] Copy AriaMeasurementInterface.py to your project
- [ ] Import in your API server
- [ ] Create module-level singleton instance
- [ ] Wire state updates to measurement layer

### Integration Phase
- [ ] `/api/coherence/current` - Get latest τ
- [ ] `/api/coherence/history` - Get τ over time
- [ ] `/api/coherence/field-reach` - Analyze signal propagation
- [ ] `/api/coherence/delta-pattern` - Find coherence boundaries
- [ ] `/api/coherence/manifestation-sources` - List active signals
- [ ] `/api/coherence/heartbeat/optimal-rate` - Adaptive heartbeat

### Testing Phase
- [ ] Endpoint latency < 10ms (most endpoints)
- [ ] All τ values in [0.0, 1.0]
- [ ] Historical array returns in chronological order
- [ ] Heartbeat rate in [100ms, 2000ms]
- [ ] Response JSON matches specification

### Deployment Phase
- [ ] Document 6 endpoints for client teams
- [ ] Create monitoring dashboard
- [ ] Set up performance tracking
- [ ] Enable real-time coherence visualization

---

## Success Criteria

✅ **Measurement Accuracy**: All τ values calculated within 1% of reference  
✅ **Latency Targets**: 90% of requests complete within specified limits  
✅ **Availability**: >99.9% uptime (no heartbeat delays)  
✅ **Correctness**: Field unification metrics match theoretical predictions  

---

## Reference

- **Omnipresent Field Model**: [COHERENCE_FIELD_MODEL_GUIDE.md](../../COHERENCE_FIELD_MODEL_GUIDE.md)
- **Theory Foundation**: [API_INTEGRATION_GUIDE_FOR_BEN.md](../../API_INTEGRATION_GUIDE_FOR_BEN.md)
- **Song Architecture**: [START_HERE.md](../../START_HERE.md)
