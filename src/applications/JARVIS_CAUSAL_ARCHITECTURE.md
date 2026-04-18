---
name: JARVIS Causal Architecture
description: Reverse-causal redesign - constraints flow backward, data flows forward through intersection points
type: project
---

# JARVIS v4: Reverse Causal Architecture

## Current Problem (v3)

```
Kernel (data source)
    ↓ (renders election data)
Renderer (function)
    ↓ (produces PNG)
HTTP Server (serves it)
    ↓ (sends to frontend)
Frontend (displays it)
```

**Issue**: Rendering waits for kernel data → threading hangs

## Correct Design (v4)

**Reverse causal chains with intersection points:**

```
Phase 1: KERNEL FOUNDATION
├─ ARIAKernel records ALL election state needed
├─ UFMEngine computes ALL 6 primitives deterministically
└─ Every election immutable in ledger

Phase 2: PRIMITIVES DEFINITION
├─ ⊙ (Singularity): election position in space
├─ β (Duality): branch weight/probability
├─ κ⊕ (Manifestation): certainty level [0-1]
├─ λ (Ledger): historical weight
├─ Θ (Frequency): recurrence pattern
└─ τ (Coherence): quality metric

*** INTERSECTION 1: Election ↔ Primitives ***
Validation: Election output = Primitive schema (deterministic)

Phase 3: RENDER SPECIFICATION (Declares Constraints)
├─ What should be shown?
├─ How should each primitive appear?
├─ What's the visual grammar?
└─ How do colors/positions/sizes map?

Render spec DOES NOT render. It DECLARES what rendering means.

*** INTERSECTION 2: Render Spec ↔ Primitives ***
Validation: Every primitive has visual meaning, bijection 1:1

Phase 4: ELECTION DECISION (Produces Data)
├─ Election decides what to show based on constraints
├─ Reads render spec (what's possible to show)
├─ Computes primitives (what is being shown)
└─ Stores decision in ledger

*** INTERSECTION 3: Election ↔ Render Spec ***
Validation: Election output satisfies all constraints

Phase 5: RENDERER (Executes Spec)
├─ Takes election primitives
├─ Applies render spec rules
├─ Produces PNG bytes
└─ Stores in cache

*** INTERSECTION 4: Renderer ↔ Render Spec ***
Validation: Pixel output matches spec exactly

Phase 6: HTTP SPECIFICATION (Declares What's Available)
├─ GET / → serves HTML
├─ GET /api/state → kernel status
├─ GET /api/frame → election primitives (JSON)
├─ GET /api/render → cached PNG bytes
└─ All responses match schemas

*** INTERSECTION 5: HTTP Spec ↔ Renderer Output ***
Validation: HTTP provides exactly what renderer produces

Phase 7: FRONTEND INTERFACE (Respects All Constraints)
├─ Only requests available endpoints
├─ Only displays what HTTP returns
├─ Only declares actions that elections can decide
└─ Validates display against render spec

*** INTERSECTION 6: Frontend ↔ HTTP Spec ***
Validation: Frontend never requests unavailable endpoints
```

---

## Architecture Components

### LAYER 1: Constraint Declaration (Future)

**RenderSpecification** (New - Phase 3)
```python
RENDER_SPEC = {
    "canvas": {
        "width": 2048,
        "height": 2048,
        "background": "#0a0a0a"
    },
    "primitives": {
        "singularity": {
            "visual": "sphere_center",
            "x_from": "⊙.x",
            "y_from": "⊙.y",
            "color": "rgb(255, 255, 255)"
        },
        "duality": {
            "visual": "branch_lines",
            "weight_from": "β",
            "opacity_from": "β"
        },
        "manifestation": {
            "visual": "glow_intensity",
            "value_from": "κ⊕",
            "intensity_scale": [0, 255]
        },
        "ledger": {
            "visual": "sphere_radius",
            "size_from": "λ",
            "size_scale": [10, 100]
        },
        "frequency": {
            "visual": "pulse_rate",
            "frequency_from": "Θ"
        },
        "coherence": {
            "visual": "color_saturation",
            "saturation_from": "τ"
        }
    }
}
```

This is a CONSTRAINT DECLARATION, not a render function.

**FrontendCapabilities** (New - Phase 7)
```python
FRONTEND_SPEC = {
    "actions": {
        "user_click": {
            "declared": True,
            "decision_space": ["analyze_election", "explore_branch", "inspect_primitive"]
        },
        "user_input": {
            "declared": True,
            "decision_space": ["text_entry", "slider_adjust", "button_toggle"]
        }
    },
    "displays": {
        "consciousness_depth": {
            "source": "election.compute_consciousness_depth()",
            "format": "gauge",
            "range": [0, 10]
        },
        "election_3d": {
            "source": "/api/render",
            "format": "png",
            "size": "2048x2048"
        }
    }
}
```

This DECLARES what the user can do and see, not how it's rendered.

---

### LAYER 2: Execution (Present)

**ElectionDecision** (Modified - Phase 4)

Currently election just reads kernel state. Needs to:
1. Read render spec (what's showable)
2. Decide what to show (within constraints)
3. Compute primitives (what it decided)
4. Record decision (ledger entry)

```python
class ElectionDecision:
    def __init__(self, render_spec, kernel_history):
        self.render_spec = render_spec  # constraints
        self.kernel_history = kernel_history  # data
        self.primitives = None

    def decide(self):
        """Decide what to show, respecting render spec constraints"""
        # What does the spec allow us to show?
        allowed_visuals = self.render_spec["primitives"].keys()

        # Compute all primitives from kernel history
        self.primitives = {
            "singularity": self._compute_singularity(),
            "duality": self._compute_duality(),
            "manifestation": self._compute_manifestation(),
            "ledger": self._compute_ledger(),
            "frequency": self._compute_frequency(),
            "coherence": self._compute_coherence(),
        }

        # Validate: all primitives in valid ranges
        self._validate_primitives()

        # Validate: all primitives are showable in render spec
        for prim in self.primitives:
            assert prim in allowed_visuals

        return self.primitives
```

**Renderer** (Modified - Phase 5)

Currently: election data → render function → PNG

New: render spec constraints + election primitives → PNG

```python
class Renderer:
    def __init__(self, render_spec):
        self.spec = render_spec  # constraints to follow

    def render(self, primitives):
        """Render using primitives, following spec constraints"""
        # Don't decide what to show. Constraints already decided.
        # Just execute the spec.

        canvas = Canvas(self.spec["canvas"])

        # For each primitive in spec
        for primitive_name, primitive_spec in self.spec["primitives"].items():
            primitive_value = primitives[primitive_name]

            # Apply spec rule
            visual = primitive_spec["visual"]
            if visual == "sphere_center":
                self._draw_sphere_at_center(
                    canvas,
                    x=primitive_value["x"],
                    y=primitive_value["y"],
                    color=primitive_spec["color"]
                )
            elif visual == "sphere_radius":
                self._update_sphere_radius(
                    canvas,
                    scale=self.spec["primitives"]["ledger"]["size_scale"],
                    value=primitive_value
                )
            # ... etc for each visual

        return canvas.render_to_png()
```

---

### LAYER 3: Data Source (Past)

**Kernel + Ledger** (Unchanged - Phase 1)

Already foundation. Just needs to ensure:
- [ ] Every election record is complete
- [ ] All fields needed for primitive computation exist
- [ ] Ledger is immutable

---

## Causal Flow (How It Works Now)

1. **User Interface** declares: "I can show consciousness depth as gauge, 3D as PNG"
2. **Render Spec** declares: "⊙→sphere center, λ→radius, τ→saturation"
3. **Election Decides**: "Here are primitives that satisfy those constraints"
4. **Renderer Executes**: "Applying spec rules to primitives → PNG"
5. **HTTP Serves**: "Here's the PNG you requested"
6. **Frontend Displays**: "Showing what spec allows"

No waiting. Constraints pre-satisfy data needs.

---

## Implementation Order (Bottom-Up Causal)

### Step 1: Verify Kernel Foundation
```python
# Check every election has all fields
assert all(
    field in election
    for election in kernel.elections
    for field in REQUIRED_FIELDS_FOR_PRIMITIVES
)
```

### Step 2: Define Render Specification
```python
# RENDER_SPEC is a configuration file, not a function
RENDER_SPEC = load_yaml("render_spec.yaml")
validate_spec(RENDER_SPEC)  # Check it's internally consistent
```

### Step 3: Create Election Semantics
```python
# Election reads spec, computes accordingly
def election_decide(kernel_history, render_spec):
    decision = ElectionDecision(render_spec, kernel_history)
    return decision.decide()  # Returns primitives matching spec
```

### Step 4: Build Renderer
```python
# Renderer only executes spec, never invents rules
renderer = Renderer(RENDER_SPEC)
png_bytes = renderer.render(primitives)
```

### Step 5: Define HTTP Contract
```python
HTTP_SPEC = {
    "/api/render": {
        "returns": "image/png",
        "size": RENDER_SPEC["canvas"],
        "always_valid": True
    }
}
```

### Step 6: Implement Frontend
```python
# Frontend only requests what HTTP spec allows
def fetch_visualization():
    return fetch("/api/render")  # spec says this exists
```

---

## Intersection Validation Tests

After each phase, run intersection tests:

```python
# After Phase 2: Primitives Definition
def test_primitives_deterministic():
    """Same election history → same primitives"""
    history = kernel.elections
    prim1 = compute_primitives(history)
    prim2 = compute_primitives(history)
    assert prim1 == prim2

# After Phase 3: Render Spec
def test_spec_coverage():
    """Every primitive in spec"""
    spec_primitives = RENDER_SPEC["primitives"].keys()
    computed_primitives = UFMENGINE_PRIMITIVES.keys()
    assert spec_primitives == computed_primitives

# After Phase 4: Election Decision
def test_election_satisfies_spec():
    """Election output matches spec schema"""
    decision = election_decide(kernel_history, RENDER_SPEC)
    primitives = decision.primitives
    spec_keys = RENDER_SPEC["primitives"].keys()
    assert set(primitives.keys()) == set(spec_keys)

# After Phase 5: Renderer
def test_renderer_produces_valid_png():
    """Renderer output is valid PNG"""
    renderer = Renderer(RENDER_SPEC)
    png = renderer.render(primitives)
    assert is_valid_png(png)
    assert png_size(png) == RENDER_SPEC["canvas"]

# After Phase 6: HTTP
def test_http_serves_render_output():
    """HTTP endpoint returns renderer output"""
    expected_png = renderer.render(primitives)
    actual_png = http_get("/api/render")
    assert actual_png == expected_png

# After Phase 7: Frontend
def test_frontend_only_requests_available():
    """Frontend never requests undefined endpoints"""
    requests = capture_frontend_requests()
    valid_endpoints = HTTP_SPEC.keys()
    assert all(req.endpoint in valid_endpoints for req in requests)
```

---

## Why This Works

1. **No data-driven decisions** → constraints pre-satisfied
2. **No forward causality** → no waiting for data
3. **No threading issues** → constraints already met at decision time
4. **No surprises** → every chain knows what next chain expects

Each layer satisfies the layer above it by definition.

---

## Key Differences from v3

| Aspect | v3 (Forward) | v4 (Reverse) |
|--------|-------------|-------------|
| Renderer | Reads kernel, invents rules | Follows spec rules |
| Election | Outputs arbitrary primitives | Outputs spec-satisfying primitives |
| Spec | Optional documentation | Mandatory constraint |
| Frontend | Requests what it wants | Requests what spec allows |
| HTTP | Serves whatever renderer produces | Serves what HTTP spec declares |

---

**Status**: Causal architecture designed. Intersection points identified. Build order clear.

**Next Phase**: Implement Phase 1-2 verification, then Phase 3-4 execution redesign.
