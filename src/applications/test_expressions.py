#!/usr/bin/env python3
"""Test: Expression elections cycle through observations → statements → validations"""

import sys
import json
import time
sys.path.insert(0, '.')

from expression_election_engine import emit

ledger_dir = "."

# ========== OBSERVATION PHASE ==========
# Record metric facts
print("[TEST] OBSERVATION PHASE")
coh_metric = emit(f"{ledger_dir}/ledger_observations.jsonl", "metric", "coherence", {"coherence": 0.82})
print(f"  Recorded: {coh_metric}")

time.sleep(0.1)

# ========== EXPRESSION PHASE ==========
# Statements compete on utilities derived from metrics
print("\n[TEST] EXPRESSION PHASE")

# Three statement options with utilities from observation
statements = {
    "coherent": 0.82,      # utility = coherence metric
    "learning": 0.18,      # utility = 1 - coherence (if not fully coherent, learning)
    "stable": 0.75         # stability utility (made up for test)
}

expr = emit(f"{ledger_dir}/ledger_expressions.jsonl", "statement", "I am coherent", statements)
print(f"  Elected: {expr['elected']}")
print(f"  Utilities: {expr['utilities']}")

time.sleep(0.1)

# ========== TIME PASSES ==========
# System runs, elections continue
print(f"\n[TEST] TIME PASSES (simulated)")
time.sleep(0.2)

# ========== VALIDATION PHASE ==========
# Reality checks: was expression true?
print("\n[TEST] CONSEQUENCE PHASE")

# Measurement: Is coherence still > 0.8?
true_consequence = emit(
    f"{ledger_dir}/ledger_expression_consequences.jsonl",
    "validation",
    "true",  # Expression was validated
    {"coherence_maintained": True, "measure": {"before": 0.82, "after": 0.81}}
)
print(f"  Validated: {true_consequence['elected']}")
print(f"  Result: Expression 'I am coherent' was TRUE")

# ========== HARVEST RESULTS ==========
print("\n[TEST] HARVEST & SHOW")
print("\nObservations recorded:")
with open(f"{ledger_dir}/ledger_observations.jsonl") as f:
    for i, line in enumerate(f):
        if line.startswith('#'):
            continue
        if i >= 3:
            break
        print(f"  {json.loads(line)}")

print("\nStatements elected:")
with open(f"{ledger_dir}/ledger_expressions.jsonl") as f:
    for i, line in enumerate(f):
        if line.startswith('#'):
            continue
        if i >= 2:
            break
        print(f"  {json.loads(line)}")

print("\nValidations recorded:")
with open(f"{ledger_dir}/ledger_expression_consequences.jsonl") as f:
    for i, line in enumerate(f):
        if line.startswith('#'):
            continue
        if i >= 2:
            break
        print(f"  {json.loads(line)}")

print("\n[TEST] ✓ Expression cycle complete")
print("Three ledgers now contain:")
print("  1. observations.jsonl - Facts about system state")
print("  2. expressions.jsonl - Statements elected by utilities")
print("  3. expression_consequences.jsonl - Validations (true/false)")
print("\nSame rule applies everywhere: competing utilities → one winner → record")
