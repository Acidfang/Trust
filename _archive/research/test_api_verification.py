#!/usr/bin/env python
"""Test script for Universal Tracker API"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("=" * 60)
    print("TEST 1: Health Check")
    print("=" * 60)
    r = requests.get(f"{BASE_URL}/api/health")
    print(f"✓ Status: {r.status_code}")
    print(f"✓ Response: {json.dumps(r.json(), indent=2)}")
    return r.status_code == 200

def test_platforms():
    """Test platforms endpoint"""
    print("\n" + "=" * 60)
    print("TEST 2: List Platforms")
    print("=" * 60)
    r = requests.get(f"{BASE_URL}/api/platforms")
    print(f"✓ Status: {r.status_code}")
    data = r.json()
    print(f"✓ Total platforms: {data.get('count', 0)}")
    print(f"✓ Ready platforms: {data.get('ready', [])}")
    return r.status_code == 200

def test_scrape_job():
    """Test scraping job creation and monitoring"""
    print("\n" + "=" * 60)
    print("TEST 3: Create Scraping Job")
    print("=" * 60)
    
    payload = {
        "platforms": ["twitter", "reddit"],
        "query": "climate change",
        "limit": 50
    }
    
    r = requests.post(f"{BASE_URL}/api/scrape", json=payload)
    print(f"✓ Status: {r.status_code}")
    data = r.json()
    print(f"✓ Response: {json.dumps(data, indent=2)}")
    
    job_id = data.get("job_id")
    if not job_id:
        print("✗ No job_id returned!")
        return False
    
    print(f"\n✓ Job created: {job_id}")
    
    # Monitor job progress
    print("\n" + "=" * 60)
    print(f"TEST 4: Monitor Job Progress (ID: {job_id})")
    print("=" * 60)
    
    for i in range(10):  # Check for up to 10 seconds
        r = requests.get(f"{BASE_URL}/api/status/{job_id}")
        data = r.json()
        status = data.get("status", "unknown")
        progress = data.get("progress", 0)
        
        print(f"[{i+1}s] Status: {status:12} Progress: {progress}%")
        
        if status == "complete":
            print("\n✓ Job completed!")
            
            # Get results
            print("\n" + "=" * 60)
            print("TEST 5: Get Job Results")
            print("=" * 60)
            
            r = requests.get(f"{BASE_URL}/api/results/{job_id}")
            if r.status_code == 200:
                results = r.json()
                print(f"✓ Total posts found: {results.get('total_posts', 0)}")
                print(f"✓ Total comments found: {results.get('total_comments', 0)}")
                print(f"✓ Results by platform:")
                for result in results.get("results", []):
                    print(f"   - {result['platform']}: {result['posts']} posts, {result['comments']} comments")
            else:
                print(f"✗ Failed to get results: {r.status_code}")
            
            return True
        
        elif status == "error":
            print(f"✗ Job failed: {data.get('error', 'unknown error')}")
            return False
        
        time.sleep(1)
    
    print("✗ Job did not complete in time")
    return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("UNIVERSAL TRACKER - API VERIFICATION TEST SUITE")
    print("=" * 60)
    
    try:
        results = {
            "Health": test_health(),
            "Platforms": test_platforms(),
            "Scraping": test_scrape_job(),
        }
        
        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)
        for test_name, passed in results.items():
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{status}: {test_name}")
        
        all_passed = all(results.values())
        if all_passed:
            print("\n✓✓✓ ALL TESTS PASSED ✓✓✓")
            print("\nThe Universal Tracker API is fully functional!")
            return 0
        else:
            print("\n✗✗✗ SOME TESTS FAILED ✗✗✗")
            return 1
    
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
