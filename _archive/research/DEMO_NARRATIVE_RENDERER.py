#!/usr/bin/env python3
"""
DEMO: Comprehensive Narrative Rendering
Shows how the Universal Renderer generates complete knowledge structures
with Evolution, Genetics, Environment, Unique, and Field Theory Corrections.
"""

import sys
sys.path.insert(0, r'c:\Determined')

from UNIVERSAL_RENDERER import render_with_song_layer


# ============================================================================
# EXAMPLE: FALCON (Bird of Prey)
# ============================================================================

class Falcon:
    """A peregrine falcon - built from evolutionary and genetic principles"""
    def __init__(self):
        # Aerodynamic components
        self.eyes = 8  # Super-acute vision
        self.wings = 2  # Delta-wing design
        self.talon_pairs = 4  # Sharp killing tools
        self.vertebrae_lock = 1  # Spine fusion in dive
        self.muscle_fiber_type = "fast_twitch"
        
        # Behavioral integrations
        self.dive_reflex = "integrated"
        self.prey_tracking = "coupled_to_vision"
        self.hunting_strategy = "unified"


class Wolf:
    """A gray wolf - built from pack/social integration"""
    def __init__(self):
        # Physical components
        self.teeth = 42
        self.limbs = 4
        self.pack_members = 5
        self.scent_glands = 1
        self.communication_types = 7  # Howl, bark, growl, whine, etc.
        
        # Social integrations
        self.hierarchy = "coupled_to_all"
        self.cooperation = "unified"
        self.territory_defense = "collective"


class Human:
    """A human - complex multi-system integration"""
    def __init__(self):
        # Biological systems
        self.neurons = 86_000_000_000
        self.organs = 11
        self.sensory_types = 5
        self.language_capability = "recursive"
        
        # Cognitive integrations
        self.consciousness = "unified_field"
        self.theory_of_mind = "embedded"
        self.abstract_reasoning = "iterative"


# ============================================================================
# DEMO RENDERER
# ============================================================================

def demo_render(name, organism, format_type):
    """Render an organism with its complete narrative structure"""
    
    print(f"\n{'='*80}")
    print(f"RENDERING: {name} (format: {format_type})")
    print(f"{'='*80}\n")
    
    output = render_with_song_layer(organism, output_format=format_type)
    
    if isinstance(output, dict):
        # Pretty print JSON
        import json
        print(json.dumps(output, indent=2)[:2000] + "\n[...truncated...]")
    else:
        # Print text/markdown
        print(output)


# ============================================================================
# RUN DEMO
# ============================================================================

if __name__ == "__main__":
    
    print("\n" + "="*80)
    print("UNIVERSAL RENDERER: COMPREHENSIVE NARRATIVE GENERATION DEMO")
    print("="*80)
    print("""
This demo shows how the renderer generates complete knowledge structures
from any container, with fields for:
  • Evolution - How it came to exist
  • Genetics - What it's made of  
  • Environment - Where/how it lives
  • Unique - What distinguishes it
  • Corrections - What field theory gets wrong

Each field has both a teaser (for overview) and full narrative.
Different output formats show different levels of detail and organization.
    """)
    
    # Demo 1: Falcon in WIKI format (overview + navigation)
    falcon = Falcon()
    demo_render("PEREGRINE FALCON", falcon, "wiki")
    
    input("\n[Press Enter to continue to markdown format...]")
    
    # Demo 2: Wolf in MARKDOWN format (detailed with links)
    wolf = Wolf()
    demo_render("GRAY WOLF", wolf, "markdown")
    
    input("\n[Press Enter to continue to JSON format (structured)...]")
    
    # Demo 3: Human in JSON format (structured with full narratives)
    human = Human()
    demo_render("HUMAN", human, "json")
    
    input("\n[Press Enter to continue to TEXT format (compact)...]")
    
    # Demo 4: Falcon in TEXT format (ultra-compact)
    demo_render("PEREGRINE FALCON", falcon, "text")
    
    print("\n" + "="*80)
    print("DEMO COMPLETE")
    print("="*80)
    print("""
KEY OBSERVATIONS:

1. WIKI FORMAT: Overview with field navigation - like Wikipedia main page
   Shows teaser for each field, clicking reveals full narrative

2. MARKDOWN FORMAT: Detailed documentation - generates complete knowledge
   Each field fully explained with evolution, genetics, environment, etc.

3. JSON FORMAT: Structured data - all narratives accessible as objects
   Good for programmatic access and API consumption

4. TEXT FORMAT: Ultra-compact summary - field teasers only
   Quick reference without full details

Each output is generated from the same compact form, meaning:
- No manual documentation needed
- Consistency guaranteed
- Changes to organism auto-propagate to all outputs
- Field theory corrections automatically updated based on current understanding
    """)
