#!/usr/bin/env python3
"""
Phase 1 Integration Test: Local Pattern + UFM Engine
Tests the unified API endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_ufm_health():
    """Test 1: UFM Health Check"""
    print("\n" + "="*60)
    print("TEST 1: UFM Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/ufm/health", timeout=5)
        data = response.json()
        print(f"✓ UFM Engine Status: {data.get('ufm_engine')}")
        print(f"  Engine Version: {data.get('engine_version')}")
        print(f"  Renderer Status: {data.get('renderer_status')}")
        print(f"  Integration: {data.get('integration')}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_process_electron():
    """Test 2: Process Electron through UFM"""
    print("\n" + "="*60)
    print("TEST 2: Process Electron through UFM")
    print("="*60)
    
    try:
        payload = {
            "entity_name": "Electron",
            "data": "Electron: fundamental particle with charge and spin"
        }
        response = requests.post(f"{BASE_URL}/api/ufm/process", json=payload, timeout=5)
        data = response.json()
        
        print(f"✓ Entity: {data.get('entity_name')}")
        ufm = data.get('ufm_analysis', {})
        print(f"  Quality Score: {ufm.get('quality_score'):.4f}")
        print(f"  Seed: {ufm.get('seed')}")
        print(f"  Replay Valid: {ufm.get('replay_valid')}")
        print(f"  Stages Completed: {', '.join(ufm.get('stages', []))}")
        
        principles = ufm.get('principles', [])
        print(f"  Principles ({len(principles)} per stage):")
        for i, p in enumerate(principles[:2]):  # Show first 2
            print(f"    {i+1}. {p.get('name')} ({p.get('symbol')}): weight={p.get('weight')}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_process_wolf_pack():
    """Test 3: Process Wolf Pack through UFM"""
    print("\n" + "="*60)
    print("TEST 3: Process Wolf Pack through UFM")
    print("="*60)
    
    try:
        payload = {
            "entity_name": "Wolf Pack",
            "data": "Wolf Pack: emergent social structure with hierarchy and cooperative hunting"
        }
        response = requests.post(f"{BASE_URL}/api/ufm/process", json=payload, timeout=5)
        data = response.json()
        
        print(f"✓ Entity: {data.get('entity_name')}")
        ufm = data.get('ufm_analysis', {})
        print(f"  Quality Score: {ufm.get('quality_score'):.4f}")
        print(f"  Replay Valid: {ufm.get('replay_valid')}")
        print(f"  Stages: {', '.join(ufm.get('stages', []))}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_local_pattern():
    """Test 4: Local Pattern Baseline"""
    print("\n" + "="*60)
    print("TEST 4: Local Pattern Baseline (Falcon)")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/entity/Falcon", timeout=5)
        data = response.json()
        
        print(f"✓ Entity: {data.get('entity')}")
        print(f"  Confidence: {data.get('confidence')}")
        print(f"  Entity Type: {data.get('entity_type')}")
        print(f"  Scale Agnostic: {data.get('scale_agnostic')}")
        print(f"  Source: {data.get('source')}")
        print(f"  Principles: {len(data.get('principles', []))} found")
        
        narratives = data.get('field_narratives', {})
        print(f"  Field Narratives: {', '.join(narratives.keys())}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_comparison():
    """Test 5: Quality Score Comparison"""
    print("\n" + "="*60)
    print("TEST 5: Comparison - Local vs UFM Quality Metrics")
    print("="*60)
    
    try:
        # Get local pattern
        local_resp = requests.get(f"{BASE_URL}/api/entity/Human", timeout=5)
        local_data = local_resp.json()
        local_confidence = local_data.get('confidence')
        
        # Process same entity through UFM
        ufm_payload = {
            "entity_name": "Human",
            "data": "Human: complex reasoning entity with language and culture"
        }
        ufm_resp = requests.post(f"{BASE_URL}/api/ufm/process", json=ufm_payload, timeout=5)
        ufm_data = ufm_resp.json()
        ufm_quality = ufm_data.get('ufm_analysis', {}).get('quality_score')
        
        print(f"✓ Entity: Human")
        print(f"  Local Pattern Confidence: {local_confidence:.4f}")
        print(f"  UFM Quality Score: {ufm_quality:.4f}")
        print(f"  Difference: {abs(local_confidence - ufm_quality):.4f}")
        print(f"  Alignment: {'GOOD ✓' if abs(local_confidence - ufm_quality) < 0.05 else 'CHECK ⚠'}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "  PHASE 1 INTEGRATION TEST - UFM Engine + Local Patterns".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    # Wait for server startup
    print("\nWaiting for API server...")
    time.sleep(2)
    
    results = []
    tests = [
        ("UFM Health", test_ufm_health),
        ("Process Electron", test_process_electron),
        ("Process Wolf Pack", test_process_wolf_pack),
        ("Local Pattern", test_local_pattern),
        ("Quality Comparison", test_comparison),
    ]
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ Test failed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎯 Phase 1 Integration: SUCCESS")
        print("   UFM Engine and Local Patterns are integrated and working")
    else:
        print(f"\n⚠ Phase 1 Integration: {total - passed} tests failed")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
