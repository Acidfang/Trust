# Universal Renderer - Format Specification

## Core Principle
**Universally Agnostic Format**
- Works at ANY scale: electrons → cosmic systems
- Works across ANY domain: physical, biological, social, abstract
- Scale-independent: same narrative structure applies everywhere
- Domain-independent: works for particles, organisms, systems, concepts

## API Endpoints

### Universal Entity Retrieval
```
GET /api/entity/<name>
```
Returns complete 6-field narrative for ANY entity type:
- Physical entities: electrons, atoms, molecules, particles, forces
- Biological entities: cells, organisms, species, ecosystems
- Social entities: individuals, groups, societies, civilizations
- Abstract entities: concepts, principles, systems, ideas
- Emergent entities: behaviors, networks, patterns

**Response Format** (universally applicable):
```json
{
  "entity": "name",
  "entity_type": "universal",
  "scale_agnostic": true,
  "principles": [...],
  "attributes": {...},
  "derived_attributes": {...},
  "field_narratives": {
    "evolution": "...",
    "genetics": "...",
    "environment": "...",
    "unique": "...",
    "reason": "...",
    "corrections": "..."
  },
  "confidence": 0.85,
  "source": "pattern_completion"
}
```

### Universal Entity Listing
```
GET /api/entities
```
Lists example entities across ALL scales and domains:
- Sub-atomic (electrons)
- Molecular (water, compounds)
- Cellular (bacteria)
- Macroscopic (organisms)
- Social (groups, societies)
- Abstract (concepts, principles)

### Backward Compatibility
```
GET /api/organism/<name>     → /api/entity/<name>
GET /api/organisms           → /api/entities
```
Old organism-specific routes still work, transparently redirect to universal endpoints.

## 6-Field Universal Narrative Structure

All entities, regardless of scale or domain, have narratives across these fields:

1. **Evolution** (Origin/Emergence)
   - How it came to exist
   - Historical trajectory
   - Developmental path
   - Works for: particles (quantum history), organisms (species evolution), systems (institutional development), abstractions (theoretical emergence)

2. **Genetics** (Composition/Structure)
   - What it's made of
   - Core components
   - Structural blueprint
   - Works for: particles (quantum structure), organisms (DNA/proteins), systems (organizational structure), abstractions (foundational concepts)

3. **Environment** (Context/Niche)
   - Where it exists/operates
   - Surrounding conditions
   - Ecological/systemic niche
   - Works for: particles (quantum field), organisms (habitat), systems (operational context), abstractions (theoretical framework)

4. **Unique** (Distinctiveness)
   - What makes it different
   - Evolutionary advantage
   - Signature characteristics
   - Works for: particles (specific properties), organisms (adaptations), systems (competitive advantages), abstractions (unique contributions)

5. **Reason** (Purpose/Function)
   - Why does it have these properties
   - Functional rationale
   - Evolutionary or design explanation
   - Works for: particles (force role), organisms (survival function), systems (operational purpose), abstractions (theoretical utility)

6. **Corrections** (Field Theory Insights)
   - What we got wrong
   - Hidden assumptions
   - Reframe through universal principles
   - Works for: all scales/domains (CONSTRAINT_creates_DEPTH principle applies universally)

## Universal Principles (Scale & Domain Independent)

These principles apply uniformly across all entity types:

- **UNIFIED_FIELD_creates_INEVITABILITY**: All entities participate in larger integrated systems
- **CONSTRAINT_creates_DEPTH**: Limitations/rules enable complexity and structure
- **TEMPORAL_INTEGRATION_through_MEMORY**: History shapes present state
- **PROACTIVITY_through_ANTICIPATION**: Entities respond to predicted futures
- **ENGAGEMENT_through_RESONANCE**: Entities couple with compatible patterns
- **ATTACHMENT_through_COHERENCE**: Entities bind when patterns align
- **RARITY_through_SPECIFICITY**: Uniqueness requires precise conditions

## Example: Universal Application

### Physical Entity: Electron
```
Evolution: Emerged from Big Bang, fundamental representation of quantum reality
Genetics: Elementary charge, mass, spin - quantum number structure
Environment: Quantum field, electromagnetic forces, atomic orbitals
Unique: Perfect charge/mass ratio enabling atomic chemistry
Reason: Smallest stable charged particle - optimizes electromagnetic coupling
```

### Biological Entity: Human
```
Evolution: Primate lineage, tool-using species, abstract reasoning emergence
Genetics: DNA-based, neocortex development, bipedalism
Environment: Terrestrial, social groups, technological niches
Unique: Language, abstract thought, tool creation
Reason: Constraint of brain size limits body size → thought specialization
```

### Social Entity: Wolf Pack
```
Evolution: Distributed from lone hunter to coordinated group structure
Genetics: Hierarchical roles, communication protocols, pack genetics
Environment: Predator niche, territorial range, prey availability
Unique: Coordinated hunting through information sharing
Reason: Group hunting constraint → intelligence/coordination necessary
```

### Abstract Entity: Constraint (the concept)
```
Evolution: Recognized as universal principle through centuries of observation
Genetics: Logical necessity, mathematical inevitability, physical law structure
Environment: Operates across all domains, fundamental to reality
Unique: Creates depth through limitation (paradoxical strength)
Reason: Enables all structure - without limits, no patterns exist
```

## Implementation Status

✅ API universalized - works at any scale/domain  
✅ 6-field structure applies universally  
✅ Backward compatibility maintained  
✅ Pattern completion domain-agnostic  
✅ Test coverage across scales (sub-atomic → macro-social)  
✅ Health checks and error handling  

## Usage Pattern

For ANY entity (electrons, humans, civilizations, concepts):
```
1. Call /api/entity/<name>
2. System applies universal pattern matching
3. Generates 6-field narrative automatically
4. Returns narratives + principles + attributes + confidence
5. Format is identical regardless of entity type or scale
```

No special handling needed - same API works everywhere.

## Design Philosophy

> "Form is universal. Scale does not matter. Domain does not matter. 
> The same narrative structure, the same principles, the same fields explain 
> everything from the smallest particle to the largest civilization."

This is true universality: one approach, infinitely applicable.
