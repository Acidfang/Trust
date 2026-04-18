#!/usr/bin/env python3
"""Verify all accountability ledger entries."""

from live_accountability_system import LiveAccountabilitySystem

accountability = LiveAccountabilitySystem("accountability.ledger", symbol="verification")
entries = accountability.read_ledger()

print("[ACCOUNTABILITY LEDGER ENTRIES]")
print(f"Total Entries: {len(entries)}\n")

for i, entry in enumerate(entries, 1):
    print(f"{i}. Entry keys: {list(entry.keys())}")
    print(f"   Full entry: {entry}")
    print()

print(accountability.report())
