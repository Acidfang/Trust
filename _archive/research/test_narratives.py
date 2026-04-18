#!/usr/bin/env python
"""Test that narratives are now contextually coherent and universal"""

from PATTERN_COMPLETION_BASELINE import BaselineKnowledgeGenerator

def test_entity_narratives(entity_name):
    """Generate and display narratives for any entity"""
    gen = BaselineKnowledgeGenerator()
    result = gen.generate_baseline_for_organism(entity_name)
    
    print(f"\n{'='*80}")
    print(f"NARRATIVE QUALITY CHECK: {entity_name}")
    print(f"{'='*80}\n")
    
    for field, narrative in result['narratives'].items():
        print(f"{field.upper()}")
        print(f"  Teaser: {narrative['teaser']}")
        print(f"  Content length: {len(narrative['full'])} chars")
        print(f"  Contains 'millions of years': {'breeding' in narrative['full'].lower()}")
        print(f"  Contains 'breeding programs': {'breeding' in narrative['full'].lower()}")
        print()
        # Print first 200 chars of full narrative
        print(f"  Preview: {narrative['full'][:200]}...")
        print()

if __name__ == "__main__":
    # Test with entities at different scales
    test_entity_narratives("Electron")
    test_entity_narratives("Water Molecule")
    test_entity_narratives("Human")
    
    print("\n✓ Narrative generation complete")
