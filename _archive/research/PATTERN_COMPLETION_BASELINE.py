"""
Pattern Completion Baseline Generator
Extracts universal patterns from existing system to generate complete knowledge.
Instead of web searches, finds missing information through pattern recognition.
"""

import json
import sys
import re
from typing import Dict, List, Any, Tuple
from pathlib import Path

sys.path.insert(0, r'c:\Determined')

class PatternExtractor:
    """Extract universal patterns from existing ledger and codebase"""
    
    def __init__(self):
        self.patterns = {}
        self.entities = {}
        self.principles = {}
        self._patterns_loaded = False
        # Don't load patterns on init - load lazily when needed
    
    def _load_all_patterns(self):
        """Scan all JSON files and extract patterns"""
        
        # Load ledger files
        ledger_files = [
            r'c:\Determined\archive\ledgers.json',
            r'c:\Determined\archive\complete_app_ledger.json',
            r'c:\Determined\archive\app_ledger.json',
            r'c:\Determined\src\ledger_elections.jsonl',
            r'c:\Determined\src\ledger_app_state.jsonl'
        ]
        
        for ledger_file in ledger_files:
            try:
                p = Path(ledger_file)
                if not p.exists():
                    continue
                    
                with open(p, 'r') as f:
                    if ledger_file.endswith('.jsonl'):
                        for line in f:
                            try:
                                data = json.loads(line.strip())
                                if data:
                                    self._extract_from_entry(data)
                            except:
                                pass
                    else:
                        data = json.load(f)
                        if data:
                            self._extract_from_entry(data)
            except:
                pass
    
    def _extract_from_entry(self, entry: Dict):
        """Extract patterns from a single entry"""
        
        # Extract entities
        if 'entities' in entry:
            for entity in entry.get('entities', []):
                if isinstance(entity, dict):
                    name = entity.get('name', entity.get('id', 'unknown'))
                    self.entities[name] = entity
        
        # Extract field names (which are themselves patterns)
        for key, value in entry.items():
            if isinstance(value, dict) and key not in ['_meta', 'metadata']:
                if key not in self.patterns:
                    self.patterns[key] = {
                        'count': 0,
                        'examples': [],
                        'type_inference': set()
                    }
                    
                self.patterns[key]['count'] += 1
                if len(self.patterns[key]['examples']) < 3:
                    self.patterns[key]['examples'].append(value)
                
                # Infer types
                for k, v in value.items():
                    v_type = type(v).__name__
                    self.patterns[key]['type_inference'].add(f"{k}:{v_type}")
    
    def get_pattern_template(self, entity_type: str) -> Dict:
        """Generate a complete template for an entity type by pattern completion"""
        
        # Lazy load patterns on first use
        if not self._patterns_loaded:
            self._load_all_patterns()
            self._patterns_loaded = True
        
        entity_type_lower = entity_type.lower()
        
        # Search for closest matching pattern
        matching_patterns = []
        for pattern_name, pattern_data in self.patterns.items():
            if entity_type_lower in pattern_name.lower() or pattern_name.lower() in entity_type_lower:
                matching_patterns.append((pattern_name, pattern_data))
        
        if not matching_patterns:
            # Generate default template from universal principles
            return self._generate_default_template(entity_type)
        
        # Use most common matching pattern as template
        matching_patterns.sort(key=lambda x: x[1]['count'], reverse=True)
        best_pattern_name, best_pattern_data = matching_patterns[0]
        
        # Reconstruct template from examples
        if best_pattern_data['examples']:
            example = best_pattern_data['examples'][0]
            template = {}
            for k, v in example.items():
                if isinstance(v, (int, float)):
                    template[k] = 0  # Numeric
                elif isinstance(v, bool):
                    template[k] = False
                elif isinstance(v, list):
                    template[k] = []
                elif isinstance(v, dict):
                    template[k] = {}
                else:
                    template[k] = ""  # String
            return template
        
        return self._generate_default_template(entity_type)
    
    def _generate_default_template(self, entity_type: str) -> Dict:
        """Generate default template using universal principles"""
        
        template = {
            "identity": f"{entity_type}",
            "attributes": {},
            "principles": [],
            "coherence": 0.95,
            "integration_depth": 0,
            "uniqueness_factors": []
        }
        
        # Map entity type to principles
        principle_map = {
            "falcon": ["UNIFIED_FIELD", "CONSTRAINT"],
            "eagle": ["UNIFIED_FIELD", "CONSTRAINT"],
            "predator": ["UNIFIED_FIELD", "ENGAGEMENT"],
            "wolf": ["ENGAGEMENT", "TEMPORAL_INTEGRATION"],
            "pack": ["ENGAGEMENT", "PROACTIVITY"],
            "human": ["CONSTRAINT", "TEMPORAL_INTEGRATION", "PROACTIVITY"],
            "social": ["ENGAGEMENT", "ATTACHMENT"],
            "system": ["UNIFIED_FIELD", "CONSTRAINT"],
            "organism": ["UNIFIED_FIELD", "ENGAGEMENT"],
            "structure": ["CONSTRAINT", "RARITY"],
            "network": ["UNIFIED_FIELD", "ENGAGEMENT"],
            "entity": ["CONSTRAINT", "UNIFIED_FIELD"]
        }
        
        for keyword, principles in principle_map.items():
            if keyword in entity_type.lower():
                template["principles"] = principles
                break
        
        return template


class BaselineKnowledgeGenerator:
    """Generate complete baseline knowledge from patterns"""
    
    def __init__(self):
        self.extractor = PatternExtractor()
        self.universal_attributes = self._init_universal_attributes()
    
    def _init_universal_attributes(self) -> Dict:
        """Define universal attribute patterns"""
        
        return {
            "physical": {
                "size": (0, 100, "relative scale"),
                "mass": (0, 1e30, "kg"),
                "density": (0, 10000, "kg/m³"),
                "speed": (0, 400, "km/h"),
                "power": (0, 1e6, "watts")
            },
            "biological": {
                "lifespan": (0, 200, "years"),
                "reproduction_rate": (0, 1000, "per generation"),
                "metabolic_rate": (0, 100, "kcal/day"),
                "genetic_diversity": (0, 1, "ratio"),
                "mutation_frequency": (0, 0.01, "per generation")
            },
            "cognitive": {
                "intelligence": (0, 10, "relative scale"),
                "learning_capacity": (0, 1, "ratio"),
                "memory_span": (0, 100, "years"),
                "social_complexity": (0, 10, "levels"),
                "abstract_reasoning": (0, 1, "capability")
            },
            "ecological": {
                "habitat_range": (0, 180, "degrees latitude"),
                "population_density": (0, 1e6, "per km²"),
                "predator_count": (0, 50, "species"),
                "prey_count": (0, 500, "species"),
                "niche_specificity": (0, 1, "ratio")
            },
            "systemic": {
                "component_integration": (0, 1, "ratio"),
                "redundancy": (0, 10, "levels"),
                "efficiency": (0, 1, "ratio"),
                "adaptability": (0, 1, "ratio"),
                "resilience": (0, 1, "ratio")
            }
        }
    
    def generate_baseline_for_organism(self, organism_type: str) -> Dict:
        """Generate complete baseline knowledge for any organism"""
        
        # Validation: organism name cannot be empty
        if not organism_type or not organism_type.strip():
            return self._generate_error_baseline("Unknown organism", "name_required")
        
        organism_type = organism_type.strip()
        
        # Step 1: Get pattern template
        template = self.extractor.get_pattern_template(organism_type)
        
        # Step 2: Extract core attributes from type
        core_attrs = self._extract_attributes_from_type(organism_type, template)
        
        # Handle edge case: No attributes found for unknown organism
        if not core_attrs:
            print(f"⚠ Warning: No pattern match for '{organism_type}', using default template")
            core_attrs = {"complexity": 5, "adaptation": 5, "context": "unknown"}
        
        # Step 3: Generate derived attributes (patterns complete each other)
        derived_attrs = self._generate_derived_attributes(core_attrs)
        
        # Step 4: Infer principles from attributes
        principles = self._infer_principles_from_attributes(core_attrs)
        
        # Safety check: principles must not be empty
        if not principles:
            principles = ["CONSTRAINT_creates_DEPTH"]  # Safe default
        
        # Step 5: Generate field narratives using pattern completion
        narratives = self._generate_narratives_from_patterns(
            organism_type, 
            core_attrs, 
            derived_attrs,
            principles
        )
        
        return {
            "organism": organism_type,
            "template": template,
            "core_attributes": core_attrs,
            "derived_attributes": derived_attrs,
            "principles": principles,
            "narratives": narratives,
            "confidence": self._calculate_confidence(core_attrs, derived_attrs)
        }
    
    def _generate_error_baseline(self, organism_type: str, error_code: str) -> Dict:
        """Generate a minimal but valid baseline for error cases"""
        
        return {
            "organism": organism_type,
            "core_attributes": {"complexity": 0},
            "derived_attributes": {},
            "principles": ["CONSTRAINT_creates_DEPTH"],
            "narratives": {
                "evolution": {"teaser": "Unknown organism", "full": f"Error: {error_code}"},
                "genetics": {"teaser": "No data", "full": "No genetic information available"},
                "environment": {"teaser": "Unknown", "full": "Environmental data unavailable"},
                "unique": {"teaser": "Unknown", "full": "Unique characteristics unknown"},
                "reason": {"teaser": "Unknown", "full": "Coloration reason unknown"},
                "corrections": {"teaser": "Unknown", "full": "Field theory applications unknown"}
            },
            "confidence": 0.0,
            "error": error_code
        }
    
    def _extract_attributes_from_type(self, organism_type: str, template: Dict) -> Dict:
        """Extract/infer attributes from organism type name"""
        
        attributes = {}
        type_lower = organism_type.lower()
        
        # Pattern matching for common types
        attribute_map = {
            # Predator types
            "eagle|falcon|hawk": {
                "speed": 240,
                "vision": 8,
                "hunting_precision": 9,
                "social_structure": 1,
                "context": "aerial"
            },
            "wolf|canine": {
                "pack_coordination": 9,
                "social_hierarchy": 8,
                "endurance": 8,
                "communication": 9,
                "context": "terrestrial"
            },
            "lion|feline": {
                "strength": 9,
                "predatory_efficiency": 9,
                "social_structure": 8,
                "territory_size": 8,
                "context": "terrestrial"
            },
            
            # Herbivore types
            "elephant": {
                "memory": 10,
                "social_bonds": 10,
                "lifespan": 70,
                "intelligence": 9,
                "context": "terrestrial"
            },
            "whale|dolphin": {
                "intelligence": 9,
                "communication": 10,
                "social_complexity": 9,
                "diving_depth": 8,
                "context": "aquatic"
            },
            
            # Arthropod types
            "spider|insect": {
                "web_precision": 10,
                "sensory_integration": 9,
                "efficiency": 10,
                "lifespan": 2,
                "context": "terrestrial"
            },
            "bee|ant": {
                "collective_intelligence": 9,
                "organization": 10,
                "efficiency": 9,
                "reproduction_structure": 8,
                "context": "terrestrial"
            },
            
            # Microorganism types
            "bacteria|microbe": {
                "adaptation_speed": 10,
                "survival_capacity": 10,
                "reproduction": 10,
                "genetic_plasticity": 9,
                "context": "variable"
            },
            
            # Human
            "human": {
                "height": "1.7 m",
                "mass": "70 kg",
                "body_temperature": "37°C",
                "lifespan": "78 years",
                "DNA_base_pairs": "3.2 billion",
                "cells": "37 trillion",
                "abstract_thought": 10,
                "language": 10,
                "tool_creation": 10,
                "social_complexity": 10,
                "context": "terrestrial"
            },
            
            # Subatomic/Quantum particles
            "electron|photon|particle|quark": {
                "mass": "9.109 × 10⁻³¹ kg",
                "charge": "-1.602 × 10⁻¹⁹ C",
                "spin": "½ ℏ",
                "classical_radius": "2.818 × 10⁻¹⁵ m",
                "bohr_radius": "5.29 × 10⁻¹¹ m",
                "interaction_strength": 8,
                "context": "quantum fields"
            },
            
            # Molecules (water as example)
            "water|molecule": {
                "mass": "18.015 u",
                "o_h_bond_length": "0.0957 nm",
                "h_o_h_bond_angle": "104.5°",
                "dipole_moment": "1.85 D",
                "charge": "0 (neutral)",
                "boiling_point": "100°C",
                "density": "1000 kg/m³",
                "context": "chemical bonds"
            }
        }
        
        # Find matching pattern and apply
        for pattern, attrs in attribute_map.items():
            if any(p in type_lower for p in pattern.split('|')):
                attributes = attrs.copy()
                return attributes
        
        # Fallback: generate generic attributes
        attributes = {
            "complexity": 5,
            "adaptation": 5,
            "efficiency": 5,
            "habitat": "unknown"
        }
        
        return attributes
    
    def _generate_derived_attributes(self, core_attrs: Dict) -> Dict:
        """Generate derived attributes through pattern completion"""
        
        derived = {}
        
        # If we know speed, infer energy requirements
        if "speed" in core_attrs:
            derived["metabolic_scaling"] = core_attrs.get("speed", 5) * 2.5
        
        # If we know intelligence, infer learning capacity
        if "abstract_thought" in core_attrs or "intelligence" in core_attrs:
            intel = max(core_attrs.get("abstract_thought", 0), core_attrs.get("intelligence", 0))
            derived["learning_capacity"] = intel / 10
            derived["cultural_transmission"] = intel / 5
        
        # If social, infer communication
        if "social" in str(core_attrs):
            derived["communication_channels"] = len([k for k in core_attrs if "social" in k.lower()]) + 3
        
        # Pack coordination implies group hunting efficiency
        if "pack_coordination" in core_attrs:
            derived["group_hunting_efficiency"] = core_attrs["pack_coordination"] * 1.2
        
        # System integration implies coherence
        if "integration" in str(core_attrs):
            derived["system_coherence"] = 0.85
        
        return derived
    
    def _infer_principles_from_attributes(self, attributes: Dict) -> List[str]:
        """Infer which field theory principles apply"""
        
        principles = []
        
        # Unified field: tight integration
        if any(k in str(attributes) for k in ["pack", "herd", "colony", "social", "coordin"]):
            principles.append("UNIFIED_FIELD_creates_INEVITABILITY")
        
        # Constraint: specialized form
        if any(k in str(attributes) for k in ["precision", "specialized", "habitat", "niche"]):
            principles.append("CONSTRAINT_creates_DEPTH")
        
        # Temporal integration: memory/longevity
        if any(k in str(attributes) for k in ["memory", "lifespan", "generation", "history"]):
            principles.append("TEMPORAL_INTEGRATION_locks_PAST")
        
        # Engagement: choice/visibility
        if any(k in str(attributes) for k in ["intelligence", "abstract", "communication", "learning"]):
            principles.append("ENGAGEMENT_vs_DENIAL")
        
        # Proactivity: future planning
        if any(k in str(attributes) for k in ["planning", "tool", "culture", "adaptation"]):
            principles.append("PROACTIVITY_locks_FUTURE")
        
        return principles if principles else ["CONSTRAINT_creates_DEPTH"]  # Default
    
    def _generate_narratives_from_patterns(self, organism_type: str, 
                                          core_attrs: Dict, 
                                          derived_attrs: Dict,
                                          principles: List[str]) -> Dict:
        """Generate complete field narratives using pattern completion"""
        
        primary_principle = principles[0] if principles else "UNIFIED_FIELD_creates_INEVITABILITY"
        
        # University field narratives - work across all scales (electrons to civilizations)
        narratives = {
            "evolution": self._narrative_evolution(organism_type, core_attrs, primary_principle),
            "composition": self._narrative_composition(organism_type, core_attrs),  # Universal: what it's made of
            "environment": self._narrative_environment(organism_type, core_attrs, derived_attrs),
            "unique": self._narrative_unique(organism_type, core_attrs, derived_attrs),
            "purpose": self._narrative_purpose(organism_type, core_attrs, principles),  # Universal: why/what
            "corrections": self._narrative_corrections(organism_type, principles)
        }
        
        return narratives
    
    def _narrative_evolution(self, organism: str, attrs: Dict, principle: str) -> Dict:
        """Generate evolution narrative - how something came to have its current state/properties
        
        Universal across:
        - Particles: emerged from quantum fields, have intrinsic properties
        - Molecules: formed from atomic interactions, structures result from bonding
        - Organisms: developed through heredity and selection
        - Systems: emerged from component interactions
        - Concepts: developed through refinement and integration
        """
        
        # Determine entity type to use appropriate language
        attrs_list = list(attrs.keys())
        
        # For generic/universal application
        teaser = f"Acquired its {attrs_list[0] if attrs_list else 'properties'} through {principle.replace('_', ' ').lower()}"
        
        full = f"""
The {organism} has its current properties because of {principle.replace('_', ' ').lower()}.

Nature of {organism}:
The {organism} exists as a coherent entity because its component properties work together. 
Each property depends on the others being present:

Key Properties:
{chr(10).join([f'- {attr}: {attrs.get(attr, "inherent property")}' for attr in attrs_list[:4]])}

Integration: These properties are not independent. The {organism} cannot express one property without 
the others being present and in specific relationships. This tight integration defines what the {organism} IS.

Historical Context: The specific combination of these properties represents a stable configuration 
in natural space. Why this specific combination? Because it remains coherent—the properties reinforce 
each other through their interactions according to {principle.lower()}.

Distinction: Other configurations of similar properties would not remain stable. This particular 
{organism} persists because this integration works.
"""
        
        return {"teaser": teaser, "full": full}
    
    def _narrative_composition(self, organism: str, attrs: Dict) -> Dict:
        """Generate composition narrative - universal description of what something is made of/composed of
        
        Works universally across:
        - Particles: quarks, electrons, photons - elementary properties
        - Molecules: atoms, bonds, quantum states
        - Organisms: cells, tissues, systems
        - Systems: components, interactions, structures
        - Concepts: principles, relationships, structures
        """
        
        components = list(attrs.keys())[:4]
        values = [attrs.get(c, "present") for c in components]
        
        teaser = f"Composed of {len(components)} integrated properties/elements: {', '.join(components[:2])}"
        
        full = f"""
The {organism} is fundamentally made of {len(components)} tightly coupled elements:

Core Components:
{chr(10).join([f'- {attr}: {values[i]}' for i, attr in enumerate(components)])}

Functional Integration: These elements don't exist in isolation. Each element's behavior 
depends on all the others being present and in proper relationship. Remove any one element 
and the {organism} ceases to be coherent—it becomes something else entirely.

Integration Architecture:
- All {len(components)} elements are coupled through mutual dependencies
- Changes to any single element cascade through all others
- The specific relationships and ratios between elements define this particular {organism}
- The whole is not the sum of parts—it's a unified system where each element constrains the others

Why This Configuration: This particular arrangement of elements represents a stable, coherent 
configuration. Other combinations might have some of these elements, but not in ways that produce 
the unified, self-consistent system you see in the {organism}.
"""
        
        return {"teaser": teaser, "full": full}
    
    def _narrative_environment(self, organism: str, attrs: Dict, derived: Dict) -> Dict:
        """Generate environment narrative - where/how something exists
        
        Universal across all scales: describes enabling conditions for coherence
        """
        
        teaser = f"Exists within specific conditions that preserve its integrated state"
        
        context = attrs.get("context", "particular")
        
        full = f"""
The {organism} exists within {context} context with specific enabling conditions:

Conditions for Coherence:
- The presence of all its component properties
- Specific relationships between those properties maintained  
- Environmental factors that don't disrupt its integration
- Continuity of the principle that defines it

Why It Persists Here: The {organism}'s integrated system remains stable in {context} conditions 
because all the elements that compose it can maintain their relationships.

Why It Cannot Persist Elsewhere:
- Different conditions would break its component relationships
- Elements that are coupled here would become separated
- The integration that defines what the {organism} IS would collapse
- It would cease to be this entity and become something else

Key Point: The {organism} is not merely shaped by its context—it is defined by operating 
successfully within it. Outside that context, the entity ceases to exist as such.
"""
        
        return {"teaser": teaser, "full": full}
    
    def _narrative_unique(self, organism: str, attrs: Dict, derived: Dict) -> Dict:
        """Generate uniqueness narrative - what makes this entity distinct
        
        Universal across all scales - focuses on distinguishing characteristics and integration
        """
        
        unique_factors = list(attrs.keys())[:3]
        teaser = f"Distinctive by its integrated {', '.join(unique_factors[:2])} structure"
        
        full = f"""
The {organism} is uniquely distinguished by:

Characteristic Properties:
{chr(10).join([f'- {factor}: {attrs.get(factor, "distinctive")}' for factor in unique_factors])}

What Makes It Distinctive: This particular combination of properties is rare because:
- These specific properties are tightly coupled to each other
- Each property depends on the others being present in specific relationships
- Removing or fundamentally changing any one property creates a different entity
- Other entities may have some of these properties, but not in this particular integration

Integration Strength: {derived.get('system_coherence', 0.85)}/1.0
This reflects how tightly the properties constrain each other. Higher values mean tighter 
coupling—the properties more strongly define what this entity IS.

Why This Matters: The {organism} persists in its current form because this particular 
combination of properties and their relationships is stable. The integration works.
Change it, and you no longer have a {organism}.
"""
        
        return {"teaser": teaser, "full": full}
        
        return {"teaser": teaser, "full": full}
    
    def _narrative_purpose(self, organism: str, attrs: Dict, principles: List[str]) -> Dict:
        """Generate purpose narrative - universal across scales
        
        Why something exists, what it does, its role/function - works for:
        - Particles: interactions they mediate, forces they carry
        - Molecules: reactions they enable, bonds they form  
        - Organisms: ecological role, reproductive function
        - Systems: services they perform, outputs they produce
        - Concepts: problems they solve, frameworks they provide
        """
        
        primary_attrs = list(attrs.keys())[:2]
        attrs_names = ", ".join(primary_attrs) if primary_attrs else "its properties"
        principle = principles[0] if principles else "UNIFIED PRINCIPLE"
        
        teaser = f"Functions through integrating its {attrs_names}"
        
        full = f"""
The {organism}'s purpose—what it does and why it exists—emerges from what it IS.

Primary Function:
The {organism} exists as a coherent entity because it performs a function: integrating its 
component properties ({', '.join(primary_attrs)}) in stable relationship.

What It Does:
- Maintains coherence among its properties
- Performs whatever role results from that integrated structure  
- Perpetuates its existence by remaining stable
- Interacts with its context according to its nature

Universal Principle: {principle}
The {organism} follows this principle in all its operations. This principle is both its 
definition and its function.

Why It Exists Rather Than Not:
The {organism} persists because:
1. This integration is stable under current conditions
2. The properties work together to preserve the whole
3. The entity produces outcomes that maintain its coherence
4. Disruption of any component disrupts everything else

The Purpose Cycle:
{organism} → maintains integration → performs function → maintains context → {organism} persists

This is not purposefulness in a conscious sense. It is the outcome of being coherent—
the {organism} cannot help but "do what it does" because doing so is what being a {organism} IS.
"""
        
        return {"teaser": teaser, "full": full}
    
    def _narrative_corrections(self, organism: str, principles: List[str]) -> Dict:
        """Generate corrections narrative - misconceptions specific to the entity
        
        Instead of forcing biological language everywhere, identify what people
        Actually get wrong about this specific entity based on field theory
        """
        
        primary = principles[0] if principles else "UNIFIED_FIELD"
        
        teaser = f"Field theory reveals what we get wrong about {organism}"
        
        # Adaptive corrections based on entity type - detect from organism name
        organism_lower = organism.lower()
        
        if any(x in organism_lower for x in ["electron", "photon", "quark", "particle", "boson"]):
            # Physics-specific misconceptions
            full = f"""
What We Misunderstood About {organism}:

**MISCONCEPTION 1: {organism} is a solid tiny ball**
We thought: Like miniature billiard balls with fixed properties.
Why wrong: {organism} is a manifestation of quantum fields, not a classical object. It doesn't 
have a definite position or trajectory until measured. Its properties are relational—they 
only exist in interaction with other fields.
Field theory reveals: {organism} is better understood as excitation in a field than as a particle.

**MISCONCEPTION 2: Properties are properties, independent of context**
We thought: {organism} always has the same charge, spin, mass regardless of measurement.
Why wrong: The act of measurement affects the system. Which property we measure determines 
which properties remain indeterminate. The properties are entangled—knowing one limits knowing others.
Field theory reveals: Properties are not independent facts about the {organism}—they're complementary 
aspects of a unified entity that cannot all be known simultaneously.

**MISCONCEPTION 3: {organism} behavior is deterministic**
We thought: We just don't know enough to predict exactly what it will do.
Why wrong: {organism} behavior is fundamentally probabilistic. There is no hidden determinism 
waiting to be discovered. Probability is intrinsic to how {organism} exists.
Field theory reveals: Indeterminacy is not ignorance—it's a real feature of nature at this scale.

**MISCONCEPTION 4: {organism} exists independently of fields**
We thought: {organism} is a basic, unreducible thing.
Why wrong: {organism} is a specific excitation pattern in underlying quantum fields. It only 
exists in relation to those fields. Remove the field, and there is no {organism}.
Field theory reveals: {organism} is a localized manifestation of something more fundamental.

**MISCONCEPTION 5: We understand {organism}'s role**
We thought: We know what {organism} does and how it interacts.
Why wrong: Most of the universe is composed of things {organism} barely interacts with. We're 
limited to studying {organism} in the contexts where we can create and detect it. We're studying 
{organism} in a narrow slice of possible reality.
Field theory reveals: Our understanding is necessarily incomplete and biased by our experimental access.

**✓ The Correction**: {organism} is not a thing in classical space. It's a quantized excitation 
in a relativistic quantum field. Its properties are contextual, complementary, and probabilistic. 
Understanding {organism} requires accepting that fundamental reality is weirder than our intuitions about solid objects.
"""
        
        else:
            # Generic misconceptions for organisms/systems/concepts
            full = f"""
What We Misunderstood About {organism}:

**MISCONCEPTION 1: Components can be understood in isolation**
We thought: Study each part separately, then combine to understand the whole.
Why wrong: The {organism}'s components are tightly coupled. Each property depends on all the 
others being present in specific relationships. When you isolate a component, you've changed it 
fundamentally—it no longer behaves as it does within the whole.
Field theory reveals: The {organism} must be understood as a unified system, not as independent parts.

**MISCONCEPTION 2: The {organism}'s properties can be optimized independently**
We thought: Improve one property without affecting others.
Why wrong: Every property is coupled to all the others through the integration. Changing one 
property cascades through the entire system, affecting all the others. You cannot make local improvements.
Field theory reveals: The system is interdependent—local changes have global effects.

**MISCONCEPTION 3: The {organism} is universal or optimal**
We thought: What makes the {organism} successful should work everywhere.
Why wrong: The {organism}'s specific integration is successful in its particular context. Outside 
that context, this same integration becomes a liability. Excellence achieved through extreme 
specialization creates fragility in other contexts.
Field theory reveals: Optimization is always local and contextual, never universal.

**MISCONCEPTION 4: The {organism} can easily adapt to change**
We thought: Successful entities are flexible and can change when needed.
Why wrong: The tightness of integration that makes the {organism} excellent in its current form 
is exactly what prevents rapid adaptation. Loosening one coupling to adapt risks destabilizing the whole.
Field theory reveals: Excellence and adaptability are tradeoffs—you cannot maximize both.

**MISCONCEPTION 5: Understanding the {organism}'s current state tells us its future**
We thought: If we know what it is now, we can predict what it will become.
Why wrong: The {organism} is defined by its context. When context changes, the entire equilibrium 
shifts. Systems at the edge of stability can respond nonlinearly—small changes can trigger large effects.
Field theory reveals: Integration creates both stability and brittleness. Stable systems can suddenly collapse.

**✓ The Correction**: Understanding the {organism} requires understanding WHY this particular 
integration exists, not just describing WHAT it currently is. The {organism} is not a universal 
solution—it's a context-dependent equilibrium. When you see the {organism}, you're seeing a 
specific solution to specific constraints. Change the constraints, and you change everything.
"""
        
        return {"teaser": teaser, "full": full}
    
    def _calculate_confidence(self, core: Dict, derived: Dict) -> float:
        """Calculate confidence in generated baseline"""
        
        # More attributes = higher confidence in pattern match
        total_attrs = len(core) + len(derived)
        
        # Max out at 0.95 (leave room for new information)
        confidence = min(0.95, 0.5 + (total_attrs * 0.05))
        
        return round(confidence, 3)


# ============================================================================
# INTEGRATION: Use pattern completion in API
# ============================================================================

def generate_organism_from_patterns(organism_name: str) -> Dict:
    """Generate complete baseline for organism using pattern completion"""
    
    generator = BaselineKnowledgeGenerator()
    baseline = generator.generate_baseline_for_organism(organism_name)
    
    return baseline


if __name__ == "__main__":
    # Demo: Generate baseline for various organisms
    generator = BaselineKnowledgeGenerator()
    
    test_organisms = [
        "Peregrine Falcon",
        "Gray Wolf",
        "Human",
        "African Elephant",
        "Spider",
        "Bacterium"
    ]
    
    for organism in test_organisms:
        print(f"\n{'='*80}")
        print(f"BASELINE KNOWLEDGE: {organism}")
        print(f"{'='*80}\n")
        
        baseline = generator.generate_baseline_for_organism(organism)
        
        print(f"Core Attributes: {baseline['core_attributes']}")
        print(f"Principles: {baseline['principles']}")
        print(f"Confidence: {baseline['confidence']}\n")
        
        for field_name, narrative in baseline['narratives'].items():
            print(f"\n--- {field_name.upper()} ---")
            print(f"TEASER: {narrative['teaser']}")
            print(f"\nFULL:\n{narrative['full'][:300]}...\n")
