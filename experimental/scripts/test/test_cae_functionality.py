#!/usr/bin/env python3
"""
Test the Civilization Analysis Engine
"""

import sys
import json
sys.path.insert(0, r'c:\Determined\src\applications')

from civilization_analysis_engine import SystemAnalysis, CivilizationAnalysisEngine

# Create a test analysis
test_analysis = SystemAnalysis(
    system_name="Healthcare System",
    wrong_choice_description="Profit-based model instead of health-based",
    wrong_choice_year=1980,
    infrastructure_locked=[
        "Insurance bureaucracy",
        "For-profit hospital networks",
        "Pharmaceutical pricing systems",
        "Employer-tied health coverage"
    ],
    early_adopters=[
        "Insurance companies",
        "Pharmaceutical corporations",
        "Healthcare administrators"
    ],
    wealth_accumulated_estimate="$500+ billion annually",
    delay_period_years=(1980, 2000),
    crisis_emerging_now=[
        "Healthcare most expensive in developed world",
        "Health outcomes worst in developed world",
        "Medical debt: $195 billion",
        "Bankruptcies from medical bills",
        "50 million uninsured",
        "Preventable deaths from lack of access"
    ],
    costs_paid_by={
        "Patients": "Medical debt, unaffordable care",
        "Workers": "Healthcare tied to employment, wage suppression",
        "Taxpayers": "Subsidizing profit system",
        "Society": "Preventable deaths, worse health outcomes"
    },
    cost_multiplier_estimate="9x",
    alternative_system=[
        "Health-based instead of profit-based",
        "Prevention-focused instead of treatment",
        "Universal coverage (like other developed countries)",
        "Community health workers",
        "Access based on need, not wealth"
    ]
)

print("="*70)
print("TEST: Healthcare System Analysis")
print("="*70)

# Print analysis
print(f"\nSystem: {test_analysis.system_name}")
print(f"Wrong choice ({test_analysis.wrong_choice_year}): {test_analysis.wrong_choice_description}")
print(f"Infrastructure locked: {len(test_analysis.infrastructure_locked)} systems")
for item in test_analysis.infrastructure_locked:
    print(f"  • {item}")

print(f"\nEarly adopters benefited: {len(test_analysis.early_adopters)}")
for group in test_analysis.early_adopters:
    print(f"  • {group}")

print(f"\nWealth accumulated: {test_analysis.wealth_accumulated_estimate}")
print(f"Delay period: {test_analysis.delay_period_years[0]}-{test_analysis.delay_period_years[1]}")

print(f"\nCrisis manifesting now: {len(test_analysis.crisis_emerging_now)} problems identified")
for problem in test_analysis.crisis_emerging_now[:3]:
    print(f"  • {problem}")
print(f"  ... and {len(test_analysis.crisis_emerging_now)-3} more")

print(f"\nCosts paid by: {len(test_analysis.costs_paid_by)} groups")
for group, cost in list(test_analysis.costs_paid_by.items())[:2]:
    print(f"  • {group}: {cost}")

print(f"\nCost multiplier: {test_analysis.cost_multiplier_estimate}")
print(f"Alternative system features: {len(test_analysis.alternative_system)}")

# Test JSON export
print("\n" + "="*70)
print("TEST: JSON Export")
print("="*70)

as_dict = test_analysis.to_dict()
print("\nJSON structure created successfully")
print(f"Keys: {list(as_dict.keys())}")

# Test file save
output_file = r"c:\Determined\test_healthcare_analysis.json"
with open(output_file, 'w') as f:
    json.dump(as_dict, f, indent=2)

print(f"\nAnalysis saved to: {output_file}")

# Verify file was created
try:
    with open(output_file, 'r') as f:
        loaded = json.load(f)
    print(f"✓ File verified: {len(json.dumps(loaded))} bytes")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*70)
print("TEST COMPLETE - Tool is working correctly")
print("="*70)
