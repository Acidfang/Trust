#!/usr/bin/env python3
"""
Quick UFM Integration Verification
"""

import urllib.request
import json
import sys

BASE_URL = "http://localhost:5000"

print("\n" + "="*70)
print("UFM INTEGRATION VERIFICATION - Phase 1")
print("="*70)

tests_passed = 0
tests_total = 0

# Test 1: UFM Health
tests_total += 1
print("\n[1] UFM Engine Health")
try:
    with urllib.request.urlopen(f"{BASE_URL}/api/ufm/health", timeout=3) as r:
        data = json.loads(r.read().decode())
        print(f"    ✓ Status: {data.get('ufm_engine')}")
        print(f"    ✓ Version: {data.get('engine_version')}")
        print(f"    ✓ Integration: {data.get('integration')}")
        tests_passed += 1
except Exception as e:
    print(f"    ✗ Error: {e}")

# Test 2: Process Electron through UFM
tests_total += 1
print("\n[2] UFM Processing - Electron")
try:
    payload = json.dumps({
        "entity_name": "Electron",
        "data": "Fundamental particle"
    }).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/api/ufm/process",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=3) as r:
        data = json.loads(r.read().decode())
        ufm = data.get('ufm_analysis', {})
        print(f"    ✓ Entity: {data.get('entity_name')}")
        print(f"    ✓ Quality Score: {ufm.get('quality_score'):.4f}")
        print(f"    ✓ Stages: {len(ufm.get('stages', []))} completed")
        tests_passed += 1
except Exception as e:
    print(f"    ✗ Error: {e}")

# Test 3: Process Wolf Pack
tests_total += 1
print("\n[3] UFM Processing - Wolf Pack")
try:
    payload = json.dumps({
        "entity_name": "Wolf Pack",
        "data": "Emergent social structure"
    }).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/api/ufm/process",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=3) as r:
        data = json.loads(r.read().decode())
        ufm = data.get('ufm_analysis', {})
        print(f"    ✓ Entity: {data.get('entity_name')}")
        print(f"    ✓ Quality Score: {ufm.get('quality_score'):.4f}")
        print(f"    ✓ Replay Valid: {ufm.get('replay_valid')}")
        tests_passed += 1
except Exception as e:
    print(f"    ✗ Error: {e}")

# Test 4: Local Pattern
tests_total += 1
print("\n[4] Local Pattern Baseline - Falcon")
try:
    with urllib.request.urlopen(f"{BASE_URL}/api/entity/Falcon", timeout=3) as r:
        data = json.loads(r.read().decode())
        print(f"    ✓ Entity: {data.get('entity')}")
        print(f"    ✓ Confidence: {data.get('confidence')}")
        print(f"    ✓ Scale Agnostic: {data.get('scale_agnostic')}")
        tests_passed += 1
except Exception as e:
    print(f"    ✗ Error: {e}")

# Test 5: Local Pattern - Human
tests_total += 1
print("\n[5] Local Pattern Baseline - Human")
try:
    with urllib.request.urlopen(f"{BASE_URL}/api/entity/Human", timeout=3) as r:
        data = json.loads(r.read().decode())
        local_conf = data.get('confidence')
        print(f"    ✓ Entity: {data.get('entity')}")
        print(f"    ✓ Confidence: {local_conf}")
        print(f"    ✓ Fields: {len(data.get('field_narratives', {}))} narratives")
        
        # Now get UFM quality for same entity
        try:
            payload = json.dumps({
                "entity_name": "Human",
                "data": "Complex reasoning entity"
            }).encode('utf-8')
            req = urllib.request.Request(
                f"{BASE_URL}/api/ufm/process",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=3) as r2:
                ufm_data = json.loads(r2.read().decode())
                ufm_quality = ufm_data.get('ufm_analysis', {}).get('quality_score')
                print(f"\n    UFM Quality Score: {ufm_quality:.4f}")
                print(f"    Local Confidence: {local_conf:.4f}")
                diff = abs(local_conf - ufm_quality)
                print(f"    Difference: {diff:.4f} {'✓' if diff < 0.1 else '⚠ (check alignment)'}")
                tests_passed += 1
        except Exception as e:
            print(f"    ⚠ UFM comparison: {e}")

except Exception as e:
    print(f"    ✗ Error: {e}")

# Summary
print("\n" + "="*70)
print(f"RESULTS: {tests_passed}/{tests_total} tests passed")
if tests_passed == tests_total:
    print("✓ Phase 1 Integration: SUCCESS")
    print("  UFM Engine and Local Patterns are integrated and working")
else:
    print(f"⚠ {tests_total - tests_passed} test(s) need attention")
print("="*70 + "\n")

sys.exit(0 if tests_passed == tests_total else 1)
