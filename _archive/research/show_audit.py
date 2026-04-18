#!/usr/bin/env python3
import json

d = json.load(open('accountability_full_audit.json'))

print('=' * 80)
print('ACCOUNTABILITY AUDIT REPORT - CLAUDE CONVERSATIONS')
print('=' * 80)
print()

print('STATEMENTS ANALYZED:')
print(f'  Total: {d.get("all_intents")} statements')
print()

print('INTENT EVOLUTION:')
evo = d.get('evolution', {})
print(f'  Primary intent: {evo.get("primary_intent")}')
print(f'  Primary frequency: {evo.get("primary_frequency", 0)*100:.1f}%')
print(f'  Unique intents: {evo.get("intent_diversity")}')
print(f'  Intent breakdown: {evo.get("all_intents", {})}')
print()

print('QUALITY METRICS:')
print(f'  Stability: {evo.get("stability_score", 0)*100:.1f}%')
print()

verify = d.get('verification', {})
print('VERIFICATION STATUS:')
print(f'  Completeness: {verify.get("completeness_score", 0)*100:.1f}%')
print(f'  Final assessment: {verify.get("final_assessment", "unknown")}')
print(f'  Intents extracted: {verify.get("integrity_checks", {}).get("intents_extracted", False)}')
print(f'  Temporal coherence: {verify.get("integrity_checks", {}).get("temporal_coherence", False)}')
print()

report = d.get('report', {})
print('EXECUTIVE SUMMARY:')
print(f'  {report.get("executive_summary", "No summary available")}')
print()

print('=' * 80)
