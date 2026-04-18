#!/usr/bin/env python3
"""
Enhanced Book Production with Illustration Integration
Embeds all tier illustrations, state matrix, and coherence field into books
"""

import re
import json
from pathlib import Path
from datetime import datetime
import shutil

class IllustrationIntegratedBookBuilder:
    """Builds books with fully integrated illustrations"""
    
    def __init__(self, source_dir, output_dir, illustration_dir):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.illustration_dir = Path(illustration_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.tier_map = {
            '-1': ('Tier -1', 'Self (Coherence)', 'tier_minus1_complete.svg'),
            '0': ('Tier 0', 'Formation (Connection)', 'tier_0.svg'),
            '1': ('Tier 1', 'Competence (Conflict)', 'tier_1.svg'),
            '2': ('Tier 2', 'Contribution (Consistency)', 'tier_2.svg'),
            '3': ('Tier 3', 'Transcendence', 'tier_3.svg'),
        }
        
        self.tier_files = {
            '-1': 'cold_hard_truth_tier_minus1_v4.md',
            '0': 'cold_hard_truth_tier_0_v3.md',
            '1': 'cold_hard_truth_tier_1_v3.md',
            '2': 'cold_hard_truth_tier_2_v4.md',
            '3': 'cold_hard_truth_tier_3.md'
        }
    
    def read_tier_file(self, tier_num):
        """Read tier source file"""
        filepath = self.source_dir / self.tier_files[tier_num]
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def build_tier_markdown_with_illustration(self, tier_num):
        """Build tier markdown with embedded illustration"""
        content = self.read_tier_file(tier_num)
        tier_label, tier_desc, svg_file = self.tier_map[tier_num]
        
        # Add illustration reference at the beginning
        illustration_section = f"""
## Visual Reference

Below is the complete state progression for {tier_label}:

![{tier_label} State Progression]({svg_file})

---

"""
        
        # Insert after the opening section
        # Find first main heading and insert after it
        parts = content.split('\n# ', 1)
        if len(parts) > 1:
            heading_end = content.find('\n\n')
            if heading_end > 0:
                enhanced = content[:heading_end+2] + illustration_section + content[heading_end+2:]
            else:
                enhanced = content + '\n\n' + illustration_section
        else:
            enhanced = content + '\n\n' + illustration_section
        
        return enhanced
    
    def copy_illustrations_to_output(self):
        """Copy illustration files to output directory"""
        illustrations_dir = self.output_dir / 'illustrations'
        illustrations_dir.mkdir(exist_ok=True)
        
        for tier_num in ['-1', '0', '1', '2', '3']:
            _, _, svg_file = self.tier_map[tier_num]
            src = self.illustration_dir / svg_file
            dst = illustrations_dir / svg_file
            if src.exists():
                shutil.copy2(src, dst)
                print(f"  ✓ Copied {svg_file}")
        
        # Copy reference visualizations
        for ref_file in ['all_states_matrix.svg', 'coherence_field_distribution.svg', 'decision_consequence_paths.svg']:
            src = self.illustration_dir / ref_file
            dst = illustrations_dir / ref_file
            if src.exists():
                shutil.copy2(src, dst)
                print(f"  ✓ Copied {ref_file}")
        
        return illustrations_dir
    
    def build_complete_book_with_illustrations(self):
        """Build unified book with all illustrations integrated"""
        print("\n Building complete book with illustrations...")
        
        # Start with front matter
        book = self._build_front_matter()
        
        # Add each tier with its illustration
        for tier_num in ['-1', '0', '1', '2', '3']:
            tier_label, tier_desc, svg_file = self.tier_map[tier_num]
            
            print(f"\n  Processing {tier_label}...")
            
            # Get tier content
            tier_content = self.read_tier_file(tier_num)
            
            # Add tier section header
            book += f"\n\n---\n\n# {tier_label}: {tier_desc}\n\n"
            
            # Add illustration reference
            book += f"""## Visual Reference

The complete state progression for {tier_label} is shown below:

![{tier_label} State Progression](illustrations/{svg_file})

---

"""
            
            # Add tier content
            book += tier_content
        
        # Add reference section with all visualizations
        book += self._build_reference_section()
        
        # Write to file
        output_file = self.output_dir / 'THE_COLD_HARD_TRUTH_With_Illustrations.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(book)
        
        print(f"\n✓ Complete book with illustrations: {output_file}")
        return output_file
    
    def _build_front_matter(self):
        """Build book front matter"""
        return """# THE COLD HARD TRUTH
## A Complete System for Understanding Coherence, Connection, and Transcendence

**April 15, 2026**

---

## Introduction

This book contains the complete TCHT system: 5 tiers, 31 decision states, and the visual framework for understanding how they interconnect.

Each tier is accompanied by illustrations showing the state progression, decision points, entry markers, and feedback loops.

### How to Use This Book

1. **Read sequentially** to understand the full system
2. **Refer to the tier illustrations** to see state relationships
3. **Check the reference section** for complete state matrix and coherence field
4. **Use the decision matrix** to understand how choices create consequences

---

## The Five Tiers

| Tier | Theme | Function | States |
|------|-------|----------|--------|
| **Tier -1** | Self (Coherence) | Understanding yourself with honesty | 10 |
| **Tier 0** | Formation (Connection) | Real vs. performed connection | 6 |
| **Tier 1** | Competence (Conflict) | Resolving conflict at source | 4 |
| **Tier 2** | Contribution (Consistency) | Maintaining correct patterns | 4 |
| **Tier 3** | Transcendence | Integration of all prior work | 7 |

**Total States**: 31  
**Total Decision Points**: 12 (where choices matter)  
**Total Work States**: 19 (where action happens)

---

## Using the Illustrations

### Visual Language

All illustrations use consistent encoding:

- 🔴 **Red circle** = Decision point (a choice is required)
- 🟢 **Green circle** = Work state (action/processing required)
- ↓ **Solid line** = Primary progression path
- ⟿ **Dashed curved line** = Loop back (unresolved entry marker)
- ⟱ **Long dashed line** = Full reset (escalation)

### Reading Strategy

**Quick (30 seconds)**: Scan the title, follow the vertical flow, notice colors

**Engaged (5 minutes)**: Read each state name, trace loops, understand consequences

**Deep (15+ minutes)**: Study the state definitions, map entry markers, understand the system

---

## Reference Guide

For quick navigation:
- See "Complete State Matrix" in the Reference section for all 31 states
- See "Coherence Field Distribution" to understand where tension accumulates
- Check individual tier illustrations for specific state progressions

---

"""
    
    def _build_reference_section(self):
        """Build reference section with visualizations"""
        return """

---

# REFERENCE SECTION

## Complete State Matrix

All 31 states across all 5 tiers in one view:

![Complete State Matrix](illustrations/all_states_matrix.svg)

---

## Coherence Field Distribution

This visualization shows the potential energy distribution across the system. Darker (red) areas indicate where tension accumulates through unresolved entry markers.

![Coherence Field Distribution](illustrations/coherence_field_distribution.svg)

### Understanding the Field

- **Tier -1 (Red zone)**: High tension from initial unresolved patterns
- **Tier 0-1 (Orange zone)**: Tension from deferred decisions and surface conflicts
- **Tier 2-3 (Green zone)**: Decreasing tension as patterns stabilize and integrate

Entry markers appear as "hot spots" showing exactly where unresolved issues create accumulated pressure.

---

## A/B/C Choice Consequences

Example visualization showing how different choice paths lead to different outcomes:

![A/B/C Choice Consequences](illustrations/decision_consequence_paths.svg)

### The Three Choices

**A) Continue as you are** (red path)
- Easiest in the moment
- Tension increases
- Often loops back later with more severity

**B) Engage honestly** (green path)  
- Harder in the moment
- Moves toward resolution
- Creates learning and growth

**C) Avoid** (orange path)
- Feels safe
- Defers tension
- Reappears larger later

---

## System Statistics

- **Total States**: 31
- **Total Decision Points**: 12 (where choice matters)
- **Total Work States**: 19 (where action happens)
- **Average States Per Tier**: 6.2
- **Entry Markers**: 11+ unique tension patterns
- **Cross-Tier Connections**: Multiple

---

## Quick Reference: All States by Tier

### Tier -1: Self (Coherence) — 10 States
T-1.1 Awareness → T-1.2 Distinction → T-1.3 Causality → T-1.4 Regulation → T-1.5 Consistency → T-1.6 Correction → T-1.7 Alignment → T-1.8 Persistence → T-1.9 Adaptability → T-1.10 Integrity

### Tier 0: Formation (Connection) — 6 States
T0.1 Existence → T0.2 Difference → T0.3 Interaction → T0.4 Recognition → T0.5 Selection → T0.6 Initial Alignment

### Tier 1: Competence (Conflict) — 4 States
T1.1 Identify Real Conflict → T1.2 Trace Causality → T1.3 Resolve at Source → T1.4 Avoid Repetition

### Tier 2: Contribution (Consistency) — 4 States
T2.1 Consistency of Patterns → T2.2 Reinforcement → T2.3 Prevention → T2.4 Early Correction

### Tier 3: Transcendence — 7 States
T3.1 Adaptation → T3.2 Resilience → T3.3 Expansion → T3.4 Integration → T3.5 Synchronization → T3.6 Refinement → T3.7 Scaling

---

## How to Read This Book

1. **Understand Tier -1 first** - It's the foundation for everything else
2. **Visual reference during reading** - Stop and look at the illustration when you reach it
3. **Trace loops in your own experience** - Which entry markers affect you?
4. **Identify your current state** - Use the state matrix to locate yourself
5. **Study the field visualization** - See where you're experiencing the most tension

---

**Complete with integrated illustrations**  
**All visual references organized in the illustrations/ directory**  
**Generated April 15, 2026**

"""
    
    def generate_all_formats(self):
        """Generate markdown with integrated illustrations"""
        print("Generating book with fully integrated illustrations...\n")
        
        # Copy illustrations first
        print("Copying illustrations to output directory...")
        self.copy_illustrations_to_output()
        
        # Build markdown with illustrations
        markdown_file = self.build_complete_book_with_illustrations()
        
        print("\n✓ Book generation complete")
        print(f"\nGenerated files:")
        print(f"  - {markdown_file} (markdown with illustration references)")
        print(f"  - illustrations/ directory (all SVG files)")
        
        return markdown_file


if __name__ == '__main__':
    source_dir = Path(__file__).parent.parent / 'docs' / 'reference' / 'tcht'
    output_dir = Path(__file__).parent / 'output'
    illustration_dir = Path(__file__).parent.parent / 'illustration_mastery' / 'examples'
    
    print("=" * 70)
    print("ILLUSTRATION-INTEGRATED BOOK BUILDER")
    print("=" * 70)
    
    builder = IllustrationIntegratedBookBuilder(source_dir, output_dir, illustration_dir)
    builder.generate_all_formats()
    
    print("\n" + "=" * 70)
    print("✓ Books with illustrations ready for use")
    print("=" * 70)
