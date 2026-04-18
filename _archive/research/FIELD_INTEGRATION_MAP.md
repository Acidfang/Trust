# FIELD INTEGRATION MAP — Causal Chains Before Implementation

## Current System State

### Frontend (ENCYCLOPEDIA.html) Entities
- Electron ✓ can generate
- Atom (generic) - needs generic atom handler
- Water Molecule ✓ can generate as "Water"
- Cell ✗ no generator yet
- Human ✗ no generator yet
- Ecosystem ✗ no generator yet
- Civilization ✗ no generator yet

### API Server Routes
```
GET /api/entity/{name}       → Returns narrative + metadata from ENTITY_DATABASE
GET /api/image/{name}        → Should return SVG visualization
```

### Causal Chain 1: User navigates to atomic scale

```
Frontend: User clicks "Atom"
    ↓
Frontend: route to ?entity=Atom
    ↓
Frontend: Call GET /api/entity/Atom
    ↓ (ENTITY_DATABASE must have "Atom" entry)
API: Return { name: "Atom", scale_badge: "Atomic scale", ... }
    ↓
Frontend: Display entity narrative
    ↓
Frontend: Call GET /api/image/Atom
    ↓ (API MUST return valid SVG or graceful 404)
API: Generate visualization for generic atom
    ↓
Frontend: Display <img> with SVG
```

### Causal Chain 2: V5 Generator Dependencies

```
Request: GET /api/image/Carbon
    ↓
API: Check if "Carbon" in entity_map
    ↓ NO → Check if "Carbon" in element_z_map (z=6)
    ↓ YES → Call builder.generate_generic_atom_svg('Carbon', 6)
    ↓
V5: Build from Aufbau principle (1s² 2s² 2p²)
    ↓
V5: Return 2233 bytes SVG
    ↓
API: Return Response(svg, mimetype='image/svg+xml')
    ↓
Status 200 + SVG content
```

### Causal Chain 3: Database consistency

ENTITY_DATABASE keys MUST match frontend entity list:
- Electron ✓
- Atom ✓
- Water Molecule ✓
- Cell ✓
- Human ✓
- Ecosystem ✓
- Civilization ✓

ALL MUST EXIST in ENTITY_DATABASE or frontend /api/entity call fails.

### What V5 Can Generate

**MEASURED Entities:**
- Electron (measured quantum properties)
- Hydrogen (measured from spectroscopy)
- Water (measured from crystallography)

**DETERMINISTICALLY Derived Entities:**
- Any element (Carbon, Oxygen, Nitrogen, etc.) → Uses Aufbau + Bohr
- Simple molecules (H₂O, CH₄, etc.) → Uses VSEPR theory

**NOT YET IMPLEMENTED:**
- Cell visualization (biological complexity)
- Human visualization (organismal coherence)
- Ecosystem visualization (collective dynamics)
- Civilization visualization (societal field)

## Field Interaction Points to Preserve

1. **ENTITY_DATABASE keys** must remain unchanged so frontend navigation doesn't break
2. **API routes** must not change (/api/entity, /api/image)
3. **Response formats** must stay compatible with HTML img tag expectations
4. **Error handling** must gracefully degrade (return 404 with JSON not 500)

## Integration Decision Points

### For "Atom" entity:
- Show generic atom (Hydrogen)?
- Show carbon (most abundant in life)?
- Show periodic table modal?
- Show error with available elements?

### For Cell, Human, Ecosystem, Civilization:
- Return placeholder visualization?
- Return error 404 with message?
- Create minimal visualizations now?
- Defer implementation and show in development?

## Verification Before Deployment

- [ ] All 7 ENCYCLOPEDIA.html entities have ENTITY_DATABASE entries
- [ ] All requests to /api/entity/{name} return proper data
- [ ] All requests to /api/image/{name} return valid SVG or proper 404
- [ ] V5 generator properly imported and instantiated
- [ ] No bytecode caching issues (__pycache__ cleared)
- [ ] test_v5_import.py passes
- [ ] TEST_DETERMINISTIC_API works for all elements
- [ ] ENCYCLOPEDIA.html displays entities without JS errors

## Field Coherence Pre-Check

Question: Does every API call have a predictable outcome?
- GET /api/entity/Electron → ENTITY_DATABASE['Electron'] exists? Yes
- GET /api/image/Electron → V5 can generate? Yes (_generate_electron_measured)
- GET /api/entity/Atom → ENTITY_DATABASE['Atom'] exists? Yes
- GET /api/image/Atom → V5 can generate? ??? (needs handler)
- GET /api/entity/Cell → ENTITY_DATABASE['Cell'] exists? Yes
- GET /api/image/Cell → V5 can generate? ??? (not implemented)

**RISK**: Chain breaks at /api/image for Atom, Cell, Human, Ecosystem, Civilization

**FIX OPTIONS:**
1. Create fallback handlers that return graceful error 404
2. Create minimal visualizations for these scales using available V5 methods
3. Combine existing element visualizations (e.g., Cell = arranged atoms)
4. Return "under development" placeholder SVG

## Recommendation

**Minimum Viable Integration:**
1. Keep ENTITY_DATABASE exactly as is (don't break frontend)
2. Map ENCYCLOPEDIA entities to V5 where possible
3. For unmapped entities (Cell, Human, Ecosystem, Civilization):
   - Return proper 404 with message
   - Include fallback SVG with "visualization under development"
4. This preserves causal chains while building incrementally

This way:
- Frontend doesn't break
- Users see explanatory messages
- V5 system works fully for what's implemented
- Clear path to extend for biological scales
