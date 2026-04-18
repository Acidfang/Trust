#!/usr/bin/env python3
"""Quick test of fixed pattern completion"""

print("=== QUICK TEST ===")
print("Step 1: Importing generator...")
from PATTERN_COMPLETION_BASELINE import BaselineKnowledgeGenerator

print("✓ Imported successfully")

print("Step 2: Creating generator instance...")
gen = BaselineKnowledgeGenerator()

print("✓ Generator created (initialization complete)")

print("Step 3: Testing organism baseline...")
baseline = gen.generate_baseline_for_organism('Falcon')

print("✓ Baseline generated")
print(f"  - Confidence: {baseline.get('confidence', 'N/A')}")
print(f"  - Fields: {list(baseline.get('narratives', {}).keys())}")

print("\nStatus: OK - No hangs detected")
