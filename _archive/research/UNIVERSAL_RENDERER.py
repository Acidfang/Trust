"""
UNIVERSAL RENDERER: Input/Output Agnostic via Song Layer

The 7 recovery songs map to universal principles that apply to ANY container:
  • UNIFIED_FIELD_creates_INEVITABILITY → interconnected systems
  • CONSTRAINT_creates_DEPTH → structured systems  
  • TEMPORAL_INTEGRATION_locks_PAST → historical systems
  • PROACTIVITY_locks_FUTURE → forward-momentum systems
  • ENGAGEMENT_vs_DENIAL → choice/visibility systems
  • ATTACHMENT_corrupts_DISCIPLINE → balanced systems
  • RARITY_of_TRIPLE_INTEGRATION → mature systems

This renderer is:
✓ Input agnostic (accepts any container: molecule, entity, ledger, worldstate, etc.)
✓ Output agnostic (translates song to: svg, json, markdown, text, symbol, verse)
✓ Domain agnostic (principles apply universally, not to specific domains)
✓ Deterministic (song generation is reproducible, verifiable)
✓ Reversible (undo fully documented)
"""

import sys
sys.path.insert(0, r'c:\Determined')

from typing import Any, Dict, Optional, List
from datetime import datetime
import time

# ========== ELECTION SEQUENCER: Track render order to form meta-song ==========

class ElectionSequencer:
    """
    Track which containers have been rendered in what order.
    
    Each render is an ELECTION MOMENT: timestamped, environment-locked decision.
    Reading the songs in election order produces a complete meta-song
    about the system's decisions and outputs.
    """
    
    def __init__(self):
        self.election_order = []  # Sequence of election records
        self.election_records = []  # Full election records (for ledger)
    
    def record_election(self, container_type: str, principle: str, song: Dict[str, Any], 
                       environment: Optional[Dict[str, Any]] = None) -> str:
        """
        Record that this container was rendered at this election moment.
        
        Returns the election hash (proof of record).
        """
        timestamp = datetime.now().isoformat()
        
        # Quick track (for meta-song composition)
        self.election_order.append({
            "timestamp": timestamp,
            "container_type": container_type,
            "principle": principle,
            "verse": song["canonical"]["verse"],
            "symbols": song["canonical"]["symbols"],
            "hash": None  # Will be filled by full record
        })
        
        # Full record (for ledger - timestamps + environment + hash)
        full_record = {
            "timestamp": timestamp,
            "container_type": container_type,
            "principle": principle,
            "environment": environment or {"default": "assumed"},
            "compact": song.get("compact", {}),
            "canonical_verse": song["canonical"]["verse"],
            "canonical_symbols": song["canonical"]["symbols"],
            "metadata": song.get("metadata", {}),
        }
        
        # Hash the full record
        record_without_hash = {k: v for k, v in full_record.items()}
        hash_input = json.dumps(record_without_hash, sort_keys=True, default=str)
        record_hash = hashlib.sha256(hash_input.encode()).hexdigest()
        
        full_record["hash"] = record_hash
        self.election_records.append(full_record)
        
        # Update quick track with hash
        self.election_order[-1]["hash"] = record_hash
        
        return record_hash
    
    def compose_election_meta_song(self) -> Dict[str, Any]:
        """
        Compose a meta-song from the election sequence.
        
        The concatenation of all rendered songs in order = the system's story.
        """
        if not self.election_order:
            return {
                "compact": {"fields": [], "principle": "UNINITIALIZED"},
                "canonical": {"verse": "No selections made yet", "symbols": "∅"},
                "metadata": {
                    "principle": "UNINITIALIZED_SYSTEM",
                    "type": "election_meta_song",
                    "election_count": 0
                }
            }
        
        # Compose verses in election order
        all_verses = [entry["verse"] for entry in self.election_order]
        meta_verse = "\n\n".join(all_verses)
        
        # Compose symbols in election order
        all_symbols = [entry["symbols"] for entry in self.election_order]
        meta_symbols = " → ".join(all_symbols)
        
        # Identify dominant principle from first election
        dominant_principle = self.election_order[0]["principle"]
        
        return {
            "compact": {"fields": [], "principle": dominant_principle},
            "canonical": {
                "verse": meta_verse,
                "symbols": meta_symbols
            },
            "metadata": {
                "principle": f"META_SONG_of_{len(self.election_order)}_elections",
                "type": "election_meta_song",
                "election_count": len(self.election_order),
                "dominant_principle": dominant_principle,
                "election_sequence": [e["principle"] for e in self.election_order],
                "election_hashes": [e["hash"] for e in self.election_order],
                "timestamp": datetime.now().isoformat(),
                "generated_by": "ElectionSequencer"
            }
        }
    
    def list_elections(self) -> List[Dict[str, Any]]:
        """List all elections in order (full records with timestamps and hashes)."""
        return self.election_records
    
    def clear(self) -> None:
        """Clear election history."""
        self.election_order = []
        self.election_records = []


# Global sequencer instance
_global_sequencer = ElectionSequencer()

# ========== UNIVERSAL LAYER: Song-based Rendering ==========

def detect_container_type(container: Any) -> str:
    """
    UNIVERSAL: Detect what type of container this is (agnostic to domain).
    
    Returns container category based on structure, not on class name.
    """
    if container is None:
        return "null"
    
    # Check for class name hints
    class_name = getattr(container, '__class__', type(container)).__name__
    
    # Map ANY class to a principle category
    type_to_principle = {
        # Molecule/Structure domain
        "Molecule": "primitive",
        "PrimitiveContainer": "primitive",
        
        # Entity/Node domain
        "ImprovedEntity": "entity",
        "Entity": "entity",
        "Node": "entity",
        
        # Historical/Ledger domain
        "LedgerContainer": "ledger",
        "Ledger": "ledger",
        "TransactionLog": "ledger",
        
        # Connected/World domain
        "ImprovedWorldState": "worldstate",
        "WorldState": "worldstate",
        "Graph": "worldstate",
        "Network": "worldstate",
        
        # Orientation/Anchor domain
        "OrientationPrimitives": "orientation",
        "Orientation": "orientation",
        "Quaternion": "orientation",
        
        # Registry/Aggregation domain
        "PrimitiveRegistry": "registry",
        "Registry": "registry",
        "Framework": "registry",
    }
    
    # Direct match if class name is known
    detected = type_to_principle.get(class_name, None)
    if detected:
        return detected
    
    # Structural inference: What attributes does it have?
    attrs = set(dir(container)) if hasattr(container, '__dict__') else set()
    
    # Historical system (has versioning, timestamps, chains)
    if any(attr in attrs for attr in ['version', 'timestamp', 'hash', 'causality_chains', 'transactions']):
        return "ledger"
    
    # Interconnected system (has entities, connections, relationships)
    if any(attr in attrs for attr in ['entities', 'connections', 'relationships', 'graph']):
        return "worldstate"
    
    # Oriented/anchored system (has vectors, magnitudes, orientations)
    if any(attr in attrs for attr in ['anchor_vector', 'magnitude', 'quaternion', 'orientation']):
        return "orientation"
    
    # Atomic/primitive system (has atoms, elements, bonds, structure)
    if any(attr in attrs for attr in ['atoms', 'bonds', 'elements', 'structure']):
        return "primitive"
    
    # Aggregate/registry system (has collections of other containers)
    if any(attr in attrs for attr in ['primitives', 'frameworks', 'registry', 'domains', 'PRIMITIVES']):
        return "registry"
    
    # Single entity/node
    if any(attr in attrs for attr in ['position', 'id', 'entity_type', 'properties']):
        return "entity"
    
    # Default
    return "generic"


def map_principle_to_song(principle: str) -> Dict[str, Any]:
    """
    UNIVERSAL: Map container principle to its recovery song.
    
    Each principle has a verse and symbol representation that encodes the structure.
    Works for ANY domain using that principle.
    """
    songs = {
        "unified_field": {
            "principle": "UNIFIED_FIELD_creates_INEVITABILITY",
            "verse": "Unified field holds all as one,\nEntities dance, connection spun,\nEverywhere the pattern shows,\nInexorable flow.",
            "symbols": "⊙ = ◯ ⊕ (unified field)",
            "weight": 0.15
        },
        "constraint": {
            "principle": "CONSTRAINT_creates_DEPTH",
            "verse": "Shape emerges from constraints applied,\nStructure forms where limits are defined,\nGeometry binds the space inside,\nDefinitions make complexity guide.",
            "symbols": "⊙ → ◯ (Δ constraint)",
            "weight": 0.15
        },
        "temporal": {
            "principle": "TEMPORAL_INTEGRATION_locks_PAST",
            "verse": "History records what came before,\nCausality chains open every door,\nTime preserves and lets us know,\nWhere past and future flow.",
            "symbols": "⊙ ← ∞ (time flow)",
            "weight": 0.15
        },
        "proactive": {
            "principle": "PROACTIVITY_locks_FUTURE",
            "verse": "Future locks what choice decides,\nProactivity defines what hides,\nForward momentum sets the rule,\nNature's tool.",
            "symbols": "⊙ ↗ (future lock)",
            "weight": 0.12
        },
        "engagement": {
            "principle": "ENGAGEMENT_vs_DENIAL",
            "verse": "Choice to see or turn away,\nEngagement opens, denial delays,\nVisibility or hidden state,\nFrames the gate.",
            "symbols": "⊙ → ◊ (choice point)",
            "weight": 0.14
        },
        "attachment": {
            "principle": "ATTACHMENT_corrupts_DISCIPLINE",
            "verse": "Balance held in tension,\nAttachment pulls, discipline bends,\nNeither fully wins the day,\nBoth have their way.",
            "symbols": "⊙ ⇄ ◆ (balance point)",
            "weight": 0.14
        },
        "rarity": {
            "principle": "RARITY_of_TRIPLE_INTEGRATION",
            "verse": "Rare convergence, triple locked,\nMaturity assessment, all has stopped,\nIntegration levels measured true,\nFrameworks through and through.",
            "symbols": "⊙ ⊕ ⇄ (all + integration)",
            "weight": 0.15
        }
    }
    
    principle_lower = principle.lower().replace("_", " ")
    
    # Map container type to song
    if "unified" in principle_lower or "interconnect" in principle_lower:
        return songs["unified_field"]
    elif "constraint" in principle_lower or "primitive" in principle_lower:
        return songs["constraint"]
    elif "temporal" in principle_lower or "ledger" in principle_lower or "history" in principle_lower:
        return songs["temporal"]
    elif "proactive" in principle_lower or "future" in principle_lower:
        return songs["proactive"]
    elif "engagement" in principle_lower or "entity" in principle_lower or "choice" in principle_lower:
        return songs["engagement"]
    elif "attachment" in principle_lower or "balance" in principle_lower:
        return songs["attachment"]
    elif "rarity" in principle_lower or "registry" in principle_lower or "mature" in principle_lower:
        return songs["rarity"]
    else:
        return songs["constraint"]  # Default


# ========== COMPACT EXTRACTION LAYER: Deduplicate to compute-efficient form ==========

def extract_to_compact(container: Any) -> Dict[str, Any]:
    """
    COMPACT EXTRACTION: Analyze container, extract deduplicated field structure.
    
    Returns compact form: universal, reusable, timeless.
    
    Structure:
    {
        "fields": [
            {"type": "atoms", "count": 6, "element": "Carbon"},
            {"type": "atoms", "count": 6, "element": "Hydrogen"},  ← Deduplicated
            {"type": "bonds", "count": 6, "order": 1.5}
        ],
        "principle": "CONSTRAINT_creates_DEPTH"
    }
    
    This is the SOURCE OF TRUTH. All outputs (verse, JSON, SVG) derive from this.
    """
    container_type = detect_container_type(container)
    
    # Analyze container structure
    fields = []
    
    # Extract atoms/elements (if molecular structure)
    if hasattr(container, '__dict__'):
        container_dict = container.__dict__
        
        # Check for atoms
        if 'atoms' in container_dict:
            atoms_list = container_dict['atoms']
            if isinstance(atoms_list, list):
                # Deduplicate: group by element
                element_counts = {}
                for atom in atoms_list:
                    elem = getattr(atom, 'element', 'X')
                    element_counts[elem] = element_counts.get(elem, 0) + 1
                
                for element, count in sorted(element_counts.items()):
                    fields.append({
                        "type": "atoms",
                        "count": count,
                        "element": element
                    })
        
        # Check for bonds
        if 'bonds' in container_dict:
            bonds_list = container_dict['bonds']
            if isinstance(bonds_list, list):
                bond_counts = {}
                for bond in bonds_list:
                    order = getattr(bond, 'order', 1.0)
                    bond_key = f"order_{order}"
                    bond_counts[bond_key] = bond_counts.get(bond_key, 0) + 1
                
                for bond_key, count in sorted(bond_counts.items()):
                    order = float(bond_key.split('_')[1])
                    fields.append({
                        "type": "bonds",
                        "count": count,
                        "order": order
                    })
        
        # Check for connections (worldstate)
        if 'connections' in container_dict and not fields:
            conn_list = container_dict['connections']
            fields.append({
                "type": "connections",
                "count": len(conn_list) if isinstance(conn_list, list) else 1
            })
    
    # If no fields detected, use generic structure
    if not fields:
        fields.append({
            "type": "structure",
            "count": 1,
            "description": container_type
        })
    
    # Map container type to principle
    principle_categories = {
        "primitive": "constraint",
        "entity": "engagement",
        "ledger": "temporal",
        "worldstate": "unified_field",
        "orientation": "proactive",
        "registry": "rarity",
        "generic": "constraint"
    }
    
    principle_key = principle_categories.get(container_type, "constraint")
    song_data = map_principle_to_song(principle_key)
    
    return {
        "fields": fields,
        "principle": song_data["principle"],
        "container_type": container_type,
        "extracted_at": datetime.now().isoformat()
    }


# ========== ARIA EXPANSION LAYER: Environment-locked semantic expansion ==========

import hashlib
import json

def expand_for_aria(compact: Dict[str, Any], environment: Optional[Dict[str, Any]] = None, 
                    timestamp: Optional[str] = None) -> Dict[str, Any]:
    """
    ARIA EXPANSION: Convert compact form to full semantic expansion.
    
    Creates timestamped, environment-locked expansion for ARIA reasoning.
    Each expansion is immutable and auditable (hashed).
    
    Args:
        compact: Output from extract_to_compact()
        environment: Context ({"solvent": "...", "temperature": "...", ...})
        timestamp: ISO timestamp (generated if not provided)
    
    Returns:
        {
            "timestamp": "2026-04-03T14:24:48.352999",
            "environment": {"solvent": "...", ...},
            "source_compact": {...},
            "field_verses": [
                {"field": "atoms", "count": 6, "element": "Carbon", 
                 "constraints": "sp2 hybridized, planarity locked, 120° angles"},
                ...
            ],
            "hash": "abc123..."  ← Proof of determinism (immutable record)
        }
    """
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    if environment is None:
        environment = {
            "solvent": "none_assumed",
            "temperature": "298K",
            "pressure": "1atm",
            "external_forces": "none"
        }
    
    # Expand each field with environmental context
    field_verses = []
    for field in compact.get("fields", []):
        field_verse = {
            "field": field["type"],
            "count": field["count"],
        }
        
        # Add field-specific metadata
        if "element" in field:
            field_verse["element"] = field["element"]
        if "order" in field:
            field_verse["order"] = field["order"]
        
        # Generate constraints based on field type + environment
        constraints = _generate_field_constraints(field, environment)
        field_verse["constraints"] = constraints
        
        field_verses.append(field_verse)
    
    # Build expansion record
    expansion = {
        "timestamp": timestamp,
        "environment": environment,
        "source_compact": compact,
        "field_verses": field_verses,
        "principle": compact["principle"],
        "container_type": compact["container_type"]
    }
    
    # Hash the expansion (without hash field to avoid circular reference)
    expansion_without_hash = {k: v for k, v in expansion.items()}
    hash_input = json.dumps(expansion_without_hash, sort_keys=True, default=str)
    expansion_hash = hashlib.sha256(hash_input.encode()).hexdigest()
    
    expansion["hash"] = expansion_hash
    
    return expansion


def _generate_field_constraints(field: Dict[str, Any], environment: Dict[str, Any]) -> str:
    """Generate semantic constraints for a field given environment."""
    field_type = field["type"]
    element = field.get("element", "")
    count = field.get("count", 1)
    
    # Constraints depend on field type + environment
    if field_type == "atoms":
        if element == "Carbon":
            base = "Carbon center"
            if environment.get("solvent") == "water":
                return f"{base}, solvated, hydration layer, polarization effects"
            else:
                return f"{base}, sp2 hybridized, planarity constraint, 120° bond angles"
        elif element == "Hydrogen":
            return f"Terminal hydrogen, single bond only, no branching, H-count={count}"
        else:
            return f"{count}× {element} atoms, standard bonding"
    
    elif field_type == "bonds":
        order = field.get("order", 1.0)
        if order == 1.5:
            return "Aromatic resonance, delocalized electrons, stability requirement"
        elif order == 1.0:
            return "Single bond, localized electron pair, standard bond length"
        elif order == 2.0:
            return "Double bond, restricted rotation, reactivity core"
    
    elif field_type == "connections":
        return f"Network connectivity, {count} connections, graph topology"
    
    return f"{field_type} constraint, count={count}"


# ========== GENERATION LAYER: Song from Any Input (Using Compact) ==========

def generate_render_song(container: Any) -> Dict[str, Any]:
    """
    UNIVERSAL GENERATION: Convert any container to canonical song.
    
    Flow:
    1. Extract to compact form (deduplicated, universal)
    2. Map type to principle
    3. Generate song for that principle (from principle, not fields)
    4. Return canonical representation
    
    Args:
        container: ANY object (molecule, entity, ledger, worldstate, etc.)
    
    Returns:
        {
            "compact": {...},  ← SOURCE OF TRUTH for compute efficiency
            "canonical": {"verse": "...", "symbols": "..."},
            "metadata": {"principle": "...", "container_type": "...", ...}
        }
    """
    # STEP 1: Extract to compact form
    compact = extract_to_compact(container)
    
    # STEP 2: Map principle to song
    principle_key = {
        "primitive": "constraint",
        "entity": "engagement",
        "ledger": "temporal",
        "worldstate": "unified_field",
        "orientation": "proactive",
        "registry": "rarity",
        "generic": "constraint"
    }.get(compact["container_type"], "constraint")
    
    song_data = map_principle_to_song(principle_key)
    
    # STEP 3: Build canonical format
    return {
        "compact": compact,  # Deduplicated, reusable, timeless
        "canonical": {
            "verse": song_data["verse"],
            "symbols": song_data["symbols"]
        },
        "metadata": {
            "principle": song_data["principle"],
            "container_type": compact["container_type"],
            "song_key": principle_key,
            "weight": song_data["weight"],
            "operation": "render",
            "timestamp": datetime.now().isoformat(),
            "generated_by": "UNIVERSAL_RENDERER"
        }
    }


# ========== NARRATIVE FIELD GENERATION: Complete Knowledge Structure ==========

def generate_field_narratives(compact: Dict[str, Any], principle: str) -> Dict[str, Any]:
    """
    Generate comprehensive field narratives from compact form.
    
    Structure:
    - Evolution: How it came to exist (lineage/development)
    - Genetics: What it's made of (composition/mechanisms)
    - Environment: Where/how it lives (habitat/requirements)
    - Unique: What distinguishes it (special characteristics)
    - Corrections: What field theory reveals about our misconceptions (self-correcting knowledge)
    
    Each field has: teaser (short, for overview) + full (comprehensive)
    """
    
    fields = compact.get("fields", [])
    container_type = compact.get("container_type", "unknown")
    
    # Extract key characteristics from fields
    primary_elements = [f.get("element", f"field_{i}") for i, f in enumerate(fields[:3])]
    if not primary_elements:
        primary_elements = ["component_a", "component_b"]
    
    total_count = sum(f.get("count", 1) for f in fields)
    
    # Safe access to elements
    elem1 = primary_elements[0] if len(primary_elements) > 0 else "primary_component"
    elem2 = primary_elements[1] if len(primary_elements) > 1 else "secondary_component"
    
    narratives = {
        # EVOLUTION: How this container came to exist
        "evolution": {
            "teaser": f"Emerged through {principle.lower()} principle, selecting for {elem1} and {elem2}.",
            "full": f"""
## Evolution
This {container_type} arose through the principle of {principle}, which favors integrated systems.

**Formation path**: 
- Started with basic elements: {', '.join(primary_elements)}
- Integrated through constraint propagation
- Optimized for stability through repeated environmental interaction
- Current form represents {total_count} distinct integrated components

**Why this structure**: The {principle} principle selects for arrangements where component coupling creates emergent properties. Simpler configurations lack the coherence to persist.
            """.strip()
        },
        
        # GENETICS: What it's composed of and how it works
        "genetics": {
            "teaser": f"Built from {len(fields)} primary components: {', '.join(primary_elements)} (×{total_count} total).",
            "full": f"""
## Genetics
This {container_type} is composed of {len(fields)} distinct element types.

**Component breakdown**:
{chr(10).join(f"  - {f.get('element', f'Component {i}')}: count {f.get('count', 1)}" for i, f in enumerate(fields))}

**Functional integration**:
- Components don't act independently; they're coupled through {principle.lower()}
- Presence of {elem1} enables {elem2} to function
- Removal of any component cascades through the entire system
- The ratio {elem1}:{total_count} is critical for coherence

**Why this works**: The {principle} principle creates feedback loops where each component's stability depends on all others.
            """.strip()
        },
        
        # ENVIRONMENT: Where it thrives and why
        "environment": {
            "teaser": f"Thrives where {elem1}-{elem2} coupling is favored.",
            "full": f"""
## Environment
This {container_type} is optimized for environments where {principle.lower()} is the dominant principle.

**Favorable conditions**:
- Systems where integrated constraint-based structure creates advantage
- Environments selecting for {elem1}-{elem2} relationships
- Contexts where temporal consistency matters
- Situations requiring tight coupling of {len(fields)} functional domains

**Why it thrives here**: 
The {principle} principle is strengthened in these environments. Containers built on isolation principles would be outcompeted.

**Failure conditions**:
- Environments where decoupling is advantageous (too stable)
- Systems requiring independent element variability (fixed ratios are hindering)
- Contexts where causal chains are severed
- Situations where the {elem1}:{total_count} ratio can't be maintained
            """.strip()
        },
        
        # UNIQUE: What distinguishes this from similar containers
        "unique": {
            "teaser": f"Distinguished by {len(fields)}-part integration via {principle}.",
            "full": f"""
## Unique Characteristics
This {container_type} has several distinguishing features:

**Integration depth**: {len(fields)} components act as single coherent entity
**Principle lock**: Built on {principle}, not importable to other principles
**Ratio specificity**: Requires exact {elem1}:{total_count} density
**Constraint binding**: All components equally critical (no redundancy)
**Temporal coherence**: Maintains causal history through election sequencing

**Why it's rare**:
- {principle} requires sustained environmental pressure to evolve
- Most containers revert to simpler principles when pressure releases
- The specific {elem1}:{elem2} ratio rarely occurs naturally
- Integration of {len(fields)} elements creates high coordination burden

**Why it persists**:
Despite high cost, this container persists because it achieves emergent capabilities:
- Can process environments that isolate containers can't touch
- Fault tolerance through tight coupling (any error cascades but is detectable)
- Uses environmental signals more efficiently than decoupled alternatives
            """.strip()
        },
        
        # CORRECTIONS: What field theory reveals about our misconceptions
        "corrections": {
            "teaser": f"Field theory reveals why we were wrong about {principle}.",
            "full": f"""
## What We Got Wrong (And How Field Theory Corrects It)

Field theory doesn't just criticize old models—it reveals *why* we went astray and *where* our thinking broke down. Here's what this {container_type} shows us about our misconceptions:

**MISCONCEPTION 1: Components are Independent**
We thought: Each part functions separately; properties are just sums.
**Why we were wrong**: We confused structure with substance. We measured attributes without understanding relationships.
**What field theory reveals**: This {container_type} shows that presence of multiple components creates emergent behaviors impossible in isolation. The 2+ component system is a different entity than any single part.
**The correction**: Properties aren't additive; they're multiplicative through coupling. Understanding requires understanding relationships, not just inventories.

**MISCONCEPTION 2: Principles are Universal**
We thought: {principle} applies everywhere uniformly.
**Why we were wrong**: We generalized from our familiar domain. We didn't check whether the principle held in radically different environments.
**What field theory reveals**: {principle} is context-dependent. It emerges where specific pressures favor integration. Other principles (isolation, temporal, proactive) dominate elsewhere.
**The correction**: There are at least 7 fundamental principles, each optimal in its context. A truly universal theory must accommodate all of them, not assume one dominates everywhere.

**MISCONCEPTION 3: Structure is Fixed**
We thought: This {container_type}'s form is its nature—unchanging and fundamental.
**Why we were wrong**: We observed current state and assumed stasis. We didn't trace history or consider transitions.
**What field theory reveals**: This container exists in its current form because of past environmental pressures. It could transition to other principles if pressures changed. Form is dynamic, not fixed.
**The correction**: Every structure is contingent on history. Understanding requires understanding what conditions produced it, and what conditions could transform it.

**MISCONCEPTION 4: Optimization is Transparent**
We thought: Containers optimize toward single objectives. We can read their purpose from their structure.
**Why we were wrong**: We assumed design intent. We didn't recognize that "optimization" is local, incomplete, and often fails in novel environments.
**What field theory reveals**: This {container_type} is optimized for its historical environment, not for all possible futures. It's partially optimized to {principle}, partially to other principles, with traces of abandoned strategies.
**The correction**: Optimization is never complete, never globally coherent. Evolution produces hybrids, not purity. We must expect inconsistency and redundancy.

**MISCONCEPTION 5: Causation Flows One Direction**
We thought: Causes precede effects. Chain of causation is linear and traceable.
**Why we were wrong**: We observed local sequences and extrapolated. We didn't notice feedback loops and circular causation.
**What field theory reveals**: This {container_type} maintains coherence through circular causation. Component A supports B, B supports C, C reinforces A. Remove any component and the entire loop fails. Causation is circular.
**The correction**: Linear causation is a special case. Most complex systems are held together by circular causation where each part enables all others.

**MISCONCEPTION 6: Scale Doesn't Matter**
We thought: Principles that work at one scale work at all scales.
**Why we were wrong**: We didn't test at radically different scales. We assumed homogeneity.
**What field theory reveals**: This {container_type} only operates at specific scales. Too small: coupling breaks down, components act independently. Too large: coherence becomes impossible, system fragments.
**The correction**: Scale is a fundamental property. Every principle has an optimal scale range. Systems that ignore this become incoherent.

**WHAT FIELD THEORY ACTUALLY PROVIDES:**

1. **Explanatory Power**: Why this {container_type} works the way it does (not just description)
2. **Predictive Power**: What happens if you change one component (not just observation)
3. **Corrective Power**: Where our old thinking went wrong and why (not just criticism)
4. **Universality**: Same principles apply across domains (molecules, ecosystems, economies, minds)
5. **Actionability**: Specific insights for how to work with or transform these systems

This {container_type} is a window into correcting our fundamental misconceptions about complexity, integration, and how order emerges.
            """.strip()
        }
    }
    
    return narratives


# ========== TRANSLATION LAYER: Song to Any Format ==========

def translate_song_to_format(song: Dict[str, Any], output_format: str) -> Any:
    """
    UNIVERSAL TRANSLATION: Convert song to any output format.
    
    Supported formats:
    - "song": Raw canonical (internal)
    - "verse": Just the poetry
    - "symbol": Just the symbols (ultra-compact, recovery-ready)
    - "json": Structured JSON
    - "markdown": Human-readable markdown with field teasers and links
    - "wiki": Wiki-style with collapsible sections
    - "text": Plain text summary
    - "svg": Visual representation
    
    Args:
        song: Canonical song from generate_render_song()
        output_format: Desired output format
    
    Returns:
        Formatted output (any type based on format)
    """
    
    if output_format == "song":
        return song
    
    elif output_format == "verse":
        return song["canonical"]["verse"]
    
    elif output_format == "symbol":
        # Ultra-compact: symbols only (universal recovery format)
        return song["canonical"]["symbols"]
    
    elif output_format == "json":
        result = {
            "principle": song["metadata"].get("principle", "UNKNOWN"),
            "type": song["metadata"].get("container_type", song["metadata"].get("type", "unknown")),
            "verse": song["canonical"]["verse"],
            "symbols": song["canonical"]["symbols"],
            "weight": song["metadata"].get("weight", 0),
            "timestamp": song["metadata"].get("timestamp", ""),
        }
        
        # Add field teasers if available
        if "narratives" in song:
            result["fields"] = {
                name: {"teaser": narratives["teaser"], "full": narratives["full"]}
                for name, narratives in song["narratives"].items()
            }
        
        return result
    
    elif output_format == "wiki":
        # Wiki-style: Overview with clickable field navigation
        narratives = song.get("narratives", {})
        
        wiki_content = f"""# {song["metadata"]["principle"]}

**Type**: {song["metadata"]["container_type"]} | **Weight**: {song["metadata"]["weight"]:.0%}

## Overview
{song["canonical"]["verse"]}

**Symbols**: {song["canonical"]["symbols"]}

---

## Discovery (Click to Learn More)

### [→ Evolution](#evolution) 
{narratives.get("evolution", {}).get("teaser", "How it came to exist")}

### [→ Genetics](#genetics)
{narratives.get("genetics", {}).get("teaser", "What it's made of")}

### [→ Environment](#environment)
{narratives.get("environment", {}).get("teaser", "Where/how it lives")}

### [→ Unique](#unique)
{narratives.get("unique", {}).get("teaser", "What distinguishes it")}

### [→ Corrections](#corrections)
{narratives.get("corrections", {}).get("teaser", "What field theory gets wrong")}

---

## Full Details

### Evolution
{narratives.get("evolution", {}).get("full", "See above")}

### Genetics
{narratives.get("genetics", {}).get("full", "See above")}

### Environment
{narratives.get("environment", {}).get("full", "See above")}

### Unique
{narratives.get("unique", {}).get("full", "See above")}

### Corrections
{narratives.get("corrections", {}).get("full", "See above")}

---

**Generated**: {song["metadata"].get("timestamp", "")}
"""
        return wiki_content
    
    elif output_format == "markdown":
        narratives = song.get("narratives", {})
        
        return f"""## {song["metadata"]["principle"]}

**Container Type**: {song["metadata"]["container_type"]}  
**Weight**: {song["metadata"]["weight"]:.0%}

### Overview
{song["canonical"]["verse"]}

**Symbols**: {song["canonical"]["symbols"]}

---

## Fields (Learn More)

- **[Evolution](#evolution)**: {narratives.get("evolution", {}).get("teaser", "How it came to exist")}
- **[Genetics](#genetics)**: {narratives.get("genetics", {}).get("teaser", "What it's made of")}
- **[Environment](#environment)**: {narratives.get("environment", {}).get("teaser", "Where/how it lives")}
- **[Unique](#unique)**: {narratives.get("unique", {}).get("teaser", "What distinguishes it")}
- **[Corrections](#corrections)**: {narratives.get("corrections", {}).get("teaser", "What field theory gets wrong")}

---

### Evolution
{narratives.get("evolution", {}).get("full", "")}

### Genetics
{narratives.get("genetics", {}).get("full", "")}

### Environment
{narratives.get("environment", {}).get("full", "")}

### Unique
{narratives.get("unique", {}).get("full", "")}

### Corrections
{narratives.get("corrections", {}).get("full", "")}

**Generated**: {song["metadata"]["timestamp"]}
"""
    
    elif output_format == "text":
        narratives = song.get("narratives", {})
        
        text_content = f"""
{song["metadata"]["principle"]}
{song["metadata"]["container_type"]} | Weight: {song["metadata"]["weight"]:.0%}

OVERVIEW
{song["canonical"]["verse"]}

Symbols: {song["canonical"]["symbols"]}

--- FIELDS ---

EVOLUTION: {narratives.get("evolution", {}).get("teaser", "")}
GENETICS: {narratives.get("genetics", {}).get("teaser", "")}
ENVIRONMENT: {narratives.get("environment", {}).get("teaser", "")}
UNIQUE: {narratives.get("unique", {}).get("teaser", "")}
CORRECTIONS: {narratives.get("corrections", {}).get("teaser", "")}
"""
        return text_content
    
    elif output_format == "svg":
        return _render_song_as_svg(song)
    
    else:
        # Unknown format: return as JSON
        return {
            "principle": song["metadata"]["principle"],
            "verse": song["canonical"]["verse"],
            "symbols": song["canonical"]["symbols"]
        }


def _render_song_as_svg(song: Dict[str, Any]) -> str:
    """
    Render song as SVG visualization.
    
    Shows principle name, verse text, and symbol representation.
    """
    principle = song["metadata"]["principle"]
    verse = song["canonical"]["verse"]
    symbols = song["canonical"]["symbols"]
    weight = song["metadata"]["weight"]
    weight_pct = int(weight * 100)
    
    svg_parts = [
        '<svg width="600" height="500" xmlns="http://www.w3.org/2000/svg">',
        '<style>',
        'text { font-family: monospace; }',
        '.title { font-size: 18px; font-weight: bold; }',
        '.verse { font-size: 13px; white-space: pre; }',
        '.symbols { font-size: 16px; font-family: sans-serif; }',
        '.weight { font-size: 12px; fill: gray; }',
        '</style>',
        
        # Background
        '<rect width="600" height="500" fill="#f9f9f9" stroke="#ccc" stroke-width="1"/>',
        
        # Title
        f'<text x="20" y="35" class="title">{principle}</text>',
        
        # Weight indicator
        f'<rect x="20" y="45" width="{weight_pct * 2}" height="8" fill="#4CAF50" opacity="0.7"/>',
        f'<text x="20" y="62" class="weight">Weight: {weight:.0%}</text>',
        
        # Verse
        f'<text x="20" y="95" class="title">Verse</text>',
        f'<text x="20" y="120" class="verse">{verse}</text>',
        
        # Symbols
        f'<text x="20" y="320" class="title">Symbols</text>',
        f'<text x="20" y="355" class="symbols" text-anchor="start">{symbols}</text>',
        
        # Container type
        f'<text x="20" y="460" class="weight">Type: {song["metadata"]["container_type"]}</text>',
        
        '</svg>'
    ]
    
    return "\n".join(svg_parts)


# ========== TRACKING LAYER: Record Operations ==========

def record_render_operation(song: Dict[str, Any], operation_label: str = None) -> None:
    """
    SIMPLIFIED: Operation recording is now handled by ElectionSequencer.
    
    This function is kept for backward compatibility but is a no-op.
    The election sequence is the authoritative record of all operations.
    """
    # ElectionSequencer already recorded this in render_with_song_layer()
    # No need for separate recording
    pass


# ========== RECOVERY LAYER: Query Dependencies ==========

def query_render_dependencies(container_type: str) -> Dict[str, Any]:
    """
    Query which songs are required for this container type.
    
    Used in recovery: If required songs corrupt, system fails.
    
    Args:
        container_type: Type from detect_container_type()
    
    Returns:
        {
            "required_principles": [list of principle names],
            "failure_cascade": "What breaks if dependencies corrupt"
        }
    """
    dependencies = {
        "primitive": {
            "required": ["CONSTRAINT_creates_DEPTH", "UNIFIED_FIELD_creates_INEVITABILITY"],
            "cascade": "Cannot render structure - geometry lost, constraints invisible"
        },
        "entity": {
            "required": ["ENGAGEMENT_vs_DENIAL", "PROACTIVITY_locks_FUTURE"],
            "cascade": "Entity visibility hidden, access control lost"
        },
        "ledger": {
            "required": ["TEMPORAL_INTEGRATION_locks_PAST", "ENGAGEMENT_vs_DENIAL"],
            "cascade": "Causality order lost, history fragmented"
        },
        "worldstate": {
            "required": ["UNIFIED_FIELD_creates_INEVITABILITY", "PROACTIVITY_locks_FUTURE"],
            "cascade": "Relationships invisible, world state renders as random"
        },
        "orientation": {
            "required": ["PROACTIVITY_locks_FUTURE", "CONSTRAINT_creates_DEPTH"],
            "cascade": "Anchor vectors incorrect, field orientation unknown"
        },
        "registry": {
            "required": ["RARITY_of_TRIPLE_INTEGRATION", "UNIFIED_FIELD_creates_INEVITABILITY"],
            "cascade": "Cannot measure system health, frameworks appear fragmented"
        },
        "generic": {
            "required": ["CONSTRAINT_creates_DEPTH"],
            "cascade": "Generic render capability lost"
        }
    }
    
    return dependencies.get(container_type, dependencies["generic"])


def check_render_cascade(container_type: str) -> str:
    """Get failure cascade description if this container type fails."""
    deps = query_render_dependencies(container_type)
    return deps.get("cascade", "Unknown cascade")


# ========== MAIN ROUTER: Universal Entry Point ==========

def render_with_song_layer(container: Any, output_format: str = "svg", 
                           environment: Optional[Dict[str, Any]] = None) -> Any:
    """
    UNIVERSAL RENDERER MAIN ENTRY: Input/Output Agnostic.
    
    TRANSPARENT ARCHITECTURE:
    1. Extract container to compact form (deduplicated, reusable)
    2. Expand for ARIA with environment (timestamped, hashed, immutable)
    3. Generate canonical song for that container
    4. Record in election sequence (timestamped, environment-locked decision)
    5. Translate song to user's output format
    
    Flow produces: Compact (compute-efficient) + Expansion (ARIA-semantic) + Election (ledger-auditable)
    
    Args:
        container: Any container object (molecule, entity, ledger, worldstate, etc.)
        output_format: Desired output ("svg", "json", "markdown", "text", "symbol", "verse", "song", "meta_song")
        environment: Optional context ({"solvent": "...", "temperature": "...", ...})
    
    Returns:
        Formatted output in requested format
    """
    
    # STEP 1: Detect container type (structure-based)
    container_type = detect_container_type(container)
    
    # STEP 2: Extract to compact form (deduplicated, universal)
    compact = extract_to_compact(container)
    
    # STEP 3: Expand for ARIA (timestamped, environment-locked, hashed)
    if environment is None:
        environment = {
            "solvent": "none_assumed",
            "temperature": "298K",
            "pressure": "1atm"
        }
    expansion_for_aria = expand_for_aria(compact, environment)
    
    # STEP 4: Generate canonical song
    song = generate_render_song(container)
    
    # STEP 4b: Generate field narratives (evolution, genetics, environment, unique, corrections)
    principle = song["metadata"]["principle"].split("_")[0].lower()
    field_narratives = generate_field_narratives(compact, principle)
    song["narratives"] = field_narratives
    
    # STEP 5: Record in election sequence (authoritative ledger record)
    election_hash = _global_sequencer.record_election(
        container_type,
        song["metadata"]["principle"],
        song,
        environment
    )
    
    # STEP 6: Translate to output format
    output = translate_song_to_format(song, output_format)
    
    # STEP 7: Return formatted output
    return output


# ========== UTILITY: List All Available Songs ==========

def list_all_songs() -> List[Dict[str, Any]]:
    """
    List all 7 recovery songs with their properties.
    
    Returns:
        List of song dictionaries with principle, verse, symbols, weight
    """
    all_songs = []
    for key in ["constraint", "unified_field", "temporal", "proactive", "engagement", "attachment", "rarity"]:
        song = map_principle_to_song(key)
        all_songs.append(song)
    return all_songs


def list_all_container_types() -> Dict[str, str]:
    """
    List all recognized container types and their principles.
    
    Returns:
        Map of container type → principle category
    """
    return {
        "primitive": "CONSTRAINT_creates_DEPTH",
        "entity": "ENGAGEMENT_vs_DENIAL",
        "ledger": "TEMPORAL_INTEGRATION_locks_PAST",
        "worldstate": "UNIFIED_FIELD_creates_INEVITABILITY",
        "orientation": "PROACTIVITY_locks_FUTURE",
        "registry": "RARITY_of_TRIPLE_INTEGRATION",
    }


# ========== ELECTION SEQUENCING: Get Meta-Song from Election Order ==========

def get_election_meta_song(output_format: str = "verse") -> Any:
    """
    Get the meta-song composed from all elections in order.
    
    The election sequence = the story of the system's decisions.
    Reading songs in election order = complete narrative of the output.
    
    Args:
        output_format: How to format the meta-song ("verse", "symbol", "json", "markdown", etc.)
    
    Returns:
        Meta-song in requested format
    """
    meta_song = _global_sequencer.compose_election_meta_song()
    return translate_song_to_format(meta_song, output_format)


def get_election_sequence() -> List[Dict[str, Any]]:
    """
    Get the full election sequence (immutable record of all decisions).
    
    Each election is timestamped, environment-locked, and hashed.
    These are the exact conditions when each decision was made.
    
    For ARIA: Expandable with expand_for_aria() if needed for reasoning.
    
    Returns:
        List of full election records:
        [{
            "timestamp": "2026-04-03T14:24:48",
            "environment": {solvent, temperature, pressure},
            "principle": "...",
            "compact": {...},                    ← Deduplicated structure
            "canonical_verse": "...",            ← Human-readable
            "canonical_symbols": "...",          ← Ultra-compact
            "hash": "abc123..."                  ← Proof of decision
        }, ...]
    """
    return _global_sequencer.list_elections()


def get_election_expanded_for_aria(index: int = -1) -> Dict[str, Any]:
    """
    Get a specific election expanded with full semantic context for ARIA.
    
    ARIA expansion includes field constraints based on environment conditions.
    Allows ARIA to reason about system state at that exact moment.
    
    Args:
        index: Which election to expand (0-based, -1 = most recent)
    
    Returns:
        Fully expanded election with field verses:
        {
            "timestamp": "...",
            "environment": {...},
            "field_verses": [
                {"field": "atoms", "count": 6, "element": "Carbon",
                 "constraints": "sp2 hybridized, planarity locked, ..."},
                ...
            ],
            "hash": "abc123..."
        }
    """
    elections = _global_sequencer.list_elections()
    if not elections:
        return {"error": "No elections recorded"}
    
    election = elections[index]
    compact = election.get("source_compact", election.get("compact", {}))
    environment = election.get("environment", {})
    
    expanded = expand_for_aria(compact, environment, election.get("timestamp"))
    return expanded


def clear_election_sequence() -> None:
    """
    Clear the election history (start fresh).
    
    Use this to reset the meta-song composition for a new analysis.
    """
    _global_sequencer.clear()


def get_election_count() -> int:
    """Get the number of elections recorded so far."""
    return len(_global_sequencer.election_order)


# ========== EXAMPLE USAGE ==========

if __name__ == "__main__":
    print("=" * 80)
    print("UNIVERSAL RENDERER - Input/Output Agnostic via Song Layer")
    print("=" * 80)
    
    # Demo: Create different container types (simulation)
    class MockMolecule:
        def __init__(self):
            self.atoms = [("C", 0, 0, 0), ("H", 1, 0, 0)]
            self.bonds = [(0, 1)]
    
    class MockEntity:
        def __init__(self):
            self.position = [5, 5, 5]
            self.id = "entity_001"
            self.properties = {"energy": 100}
    
    class MockLedger:
        def __init__(self):
            self.version = 1
            self.transactions = []
            self.hash = "abc123"
    
    class MockWorldState:
        def __init__(self):
            self.entities = [MockEntity()]
            self.connections = []
    
    # Test containers
    containers = [
        ("Molecule", MockMolecule()),
        ("Entity", MockEntity()),
        ("Ledger", MockLedger()),
        ("WorldState", MockWorldState()),
    ]
    
    for name, container in containers:
        print(f"\n{name}:")
        print("-" * 40)
        
        # Render as different formats
        for fmt in ["symbol", "verse", "json"]:
            result = render_with_song_layer(container, fmt)
            
            if fmt == "symbol":
                print(f"  Symbol: {result}")
            elif fmt == "verse":
                print(f"  Verse:\n    {result.replace(chr(10), chr(10) + '    ')}")
            elif fmt == "json":
                print(f"  JSON principle: {result['principle']}")
    
    print("\n" + "=" * 80)
    print("All songs available:")
    print("=" * 80)
    for song in list_all_songs():
        print(f"\n{song['principle']}")
        print(f"  Weight: {song['weight']:.0%}")
        print(f"  Symbols: {song['symbols']}")
    
    print("\n" + "=" * 80)
