#!/usr/bin/env python3
"""Test the adaptive visualization system."""

from FIELD_IMAGE_GENERATOR import FieldImageGenerator

# Simulate the entity data
test_entities = {
    "Cell": {
        "name": "Cell",
        "attributes": {"organelles": "nucleus", "type": "biological"},
        "scale_badge": "Cellular"
    },
    "Ecosystem": {
        "name": "Ecosystem",
        "attributes": {"components": "Species, terrain, climate", "interactions": "Predation, competition, symb"},
        "scale_badge": "Ecological"
    },
    "Civilization": {
        "name": "Civilization",
        "attributes": {"components": "Humans, laws, technology", "organization": "Government, economy"},
        "scale_badge": "Societal"
    }
}

g = FieldImageGenerator()

for entity_name, entity_data in test_entities.items():
    print(f"\nTesting {entity_name}:")
    print(f"  Entity name: {entity_data['name']}")
    
    complexity = g.analyze_complexity(entity_data)
    print(f"  Complexity level: {complexity['level']}")
    print(f"  Total complexity: {complexity['total_complexity']}")
    
    svg = g.generate_adaptive_visualization(entity_data)
    print(f"  SVG output length: {len(svg)} bytes")
    
    # Check for entity-specific markers
    if entity_name == "Cell":
        has_expected = 'mitochondria' in svg and 'organelle' in svg
        print(f"  Contains mitochondria/organelles: {has_expected}")
    elif entity_name == "Ecosystem":
        has_expected = 'producer' in svg and 'consumer' in svg
        print(f"  Contains food web elements: {has_expected}")
    elif entity_name == "Civilization":
        has_expected = 'information' in svg and 'global' in svg
        print(f"  Contains civilization markers: {has_expected}")
    
    print(f"  SVG starts with: {svg[:80]}...")
