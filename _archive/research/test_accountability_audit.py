#!/usr/bin/env python3
"""
Run comprehensive accountability audit
Check if anything is missed in the project
"""

from singularity_storage import SingularityStore
import json

def run_audit():
    store = SingularityStore()
    
    print("═" * 80)
    print("COMPREHENSIVE ACCOUNTABILITY AUDIT")
    print("═" * 80)
    print()
    
    # Run the main verification
    print("1. EXTRACTING ALL INTENTS FROM RECORD...")
    all_intents = store.extract_all_intents()
    print(f"   Found: {len(all_intents)} intent entries")
    if all_intents:
        print(f"   Sample: {all_intents[0]}")
    print()
    
    # Track evolution
    print("2. TRACKING INTENT EVOLUTION...")
    evolution = store.track_intent_evolution()
    print(f"   Primary intent: {evolution.get('primary_intent')}")
    print(f"   Stability: {evolution.get('stability_score', 0)*100:.0f}%")
    print(f"   Total statements: {evolution.get('total_statements')}")
    print(f"   Unique intents: {evolution.get('intent_diversity')}")
    print(f"   Intent changes: {evolution.get('intent_changes')}")
    print()
    
    # Track meaning
    print("3. TRACKING MEANING EVOLUTION...")
    meaning = store.track_meaning_evolution()
    print(f"   Persistent topics: {len(meaning.get('persistent_topics', []))}")
    if meaning.get('persistent_topics'):
        print(f"   Top topics: {[t[0] for t in meaning.get('persistent_topics', [])[:5]]}")
    print(f"   Major shifts: {meaning.get('major_meaning_shifts')}")
    print()
    
    # Detect drift
    print("4. DETECTING INTENT DRIFT...")
    drift = store.detect_intent_drift()
    print(f"   Drift detected: {drift.get('drift_detected')}")
    print(f"   Direction: {drift.get('drift_direction')}")
    print(f"   Magnitude: {drift.get('drift_magnitude', 0)*100:.0f}%")
    print()
    
    # Track improvements
    print("5. TRACKING IMPROVEMENTS...")
    improvements = store.improvement_trajectory()
    print(f"   Total improvements: {improvements.get('total_improvements', 0)}")
    print(f"   Improvement areas: {improvements.get('improvement_areas', [])}")
    print()
    
    # Map to features
    print("6. MAPPING INTENTS TO FEATURES...")
    mapping = store.map_intent_to_features()
    print(f"   Total intents analyzed: {mapping.get('total_intents_found', 0)}")
    print(f"   Intents satisfied: {mapping.get('intents_satisfied', 0)}")
    print(f"   Alignment score: {mapping.get('alignment_score', 0)*100:.0f}%")
    print(f"   Gaps found: {len(mapping.get('gaps_identified', []))}")
    if mapping.get('gaps_identified'):
        print(f"   Unmapped intents: {[g['intent'] for g in mapping.get('gaps_identified', [])]}")
    print()
    
    # Verify nothing missed
    print("7. COMPREHENSIVE INTEGRITY CHECK...")
    verification = store.verify_nothing_missed()
    print(f"   Completeness: {verification.get('completeness_score', 0)*100:.0f}%")
    print(f"   Status: {verification.get('final_assessment')}")
    print("   Integrity checks:")
    for check, result in verification.get('integrity_checks', {}).items():
        status = "✓" if result else "✗"
        print(f"     {status} {check}")
    print()
    
    # Master accountability report
    print("8. MASTER ACCOUNTABILITY REPORT...")
    report = store.accountability_report()
    print(f"   Total statements analyzed: {report.get('data_overview', {}).get('total_statements_analyzed')}")
    print(f"   Unique intents: {report.get('data_overview', {}).get('unique_intents')}")
    print(f"   Primary intent: {report.get('data_overview', {}).get('primary_intent')}")
    print(f"   Intent coverage: {report.get('project_alignment', {}).get('intent_coverage', 0)*100:.0f}%")
    print(f"   Features implemented: {len(report.get('project_alignment', {}).get('features_implemented', []))}")
    print(f"   System health: {report.get('recommendations', {}).get('system_health')}")
    print(f"   Summary: {report.get('executive_summary')}")
    print()
    
    # Print final assessment
    print("═" * 80)
    print("AUDIT COMPLETE")
    print("═" * 80)
    print()
    print(f"FINAL ASSESSMENT: {verification.get('final_assessment')}")
    print(f"Nothing missed: {verification.get('completeness_score', 0) > 0.8}")
    print(f"All meanings preserved: {verification.get('integrity_checks', {}).get('meanings_preserved')}")
    print(f"Temporal coherence: {verification.get('integrity_checks', {}).get('temporal_coherence')}")
    print()
    
    # Save full report
    with open('accountability_audit_report.json', 'w') as f:
        json.dump({
            "evolution": evolution,
            "meaning": meaning,
            "drift": drift,
            "improvements": improvements,
            "mapping": mapping,
            "verification": verification,
            "accountability": report
        }, f, indent=2)
    
    print("Full report saved to: accountability_audit_report.json")

if __name__ == "__main__":
    run_audit()
