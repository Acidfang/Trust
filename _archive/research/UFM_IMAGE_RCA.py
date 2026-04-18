#!/usr/bin/env python3
"""
Use UFM Engine for Root Cause Analysis of image loading failure
Demonstrates UFM's 7-stage universal pipeline for debugging
"""

import sys
sys.path.insert(0, r'c:\Determined')

from UFM_CLIENT import get_ufm_client
import json
from pathlib import Path

def analyze_image_loading_issue():
    """RCA: Why is the electron image not loading in encyclopedia?"""
    
    client = get_ufm_client()
    
    print("\n" + "="*80)
    print("UFM ROOT CAUSE ANALYSIS: Image Loading Issue")
    print("="*80)
    
    # =========================================================================
    # STAGE 1: Define the Problem State
    # =========================================================================
    
    print("\n[STAGE 1] PROBLEM DEFINITION")
    print("-" * 80)
    
    problem_data = {
        "issue": "Electron image not displaying in encyclopedia",
        "symptoms": [
            "HTML file references: ../../../wiki_assets/entity_images/electron_field.png",
            "File exists at: c:\\Determined\\wiki_assets\\entity_images\\electron_field.png",
            "HTML at: c:\\Determined\\ELECTRON_ENCYCLOPEDIA.html",
            "Relative path resolves incorrectly"
        ],
        "file_structure": {
            "html_file": "c:\\Determined\\ELECTRON_ENCYCLOPEDIA.html",
            "image_file": "c:\\Determined\\wiki_assets\\entity_images\\electron_field.png",
            "html_parent": "c:\\Determined",
            "specified_relative_path": "../../../wiki_assets/entity_images/electron_field.png",
            "correct_relative_path": "wiki_assets/entity_images/electron_field.png"
        },
        "path_analysis": {
            "html_location": "C:\\Determined",
            "step_1_up": "C:\\",
            "step_2_up": "ERROR - cannot go above root",
            "step_3_up": "ERROR - cannot go above root",
            "conclusion": "Path escapes filesystem boundary",
            "issue_type": "path_traversal_overflow"
        }
    }
    
    problem_json = json.dumps(problem_data, indent=2)
    print(f"Problem structure:\n{problem_json}")
    
    # Encode for UFM
    problem_bytes = problem_json.encode('utf-8')
    
    # =========================================================================
    # STAGE 2-7: Process through UFM's Universal Pipeline
    # =========================================================================
    
    print("\n[STAGE 2-7] UFM UNIVERSAL PIPELINE ANALYSIS")
    print("-" * 80)
    print("Sending problem to UFM Engine for 7-stage analysis...")
    print("Expected to identify: path structure issue, resolution error, fix strategy\n")
    
    result = client.process_universal(problem_bytes, verify=True)
    
    # =========================================================================
    # DISPLAY UFM ANALYSIS RESULTS
    # =========================================================================
    
    if result.get('error'):
        print(f"❌ UFM Error: {result['error']}")
        return result
    
    print("\n✓ UFM Analysis Complete")
    print("="*80)
    
    # Quality Score
    quality = result.get('quality_score', 0)
    print(f"\n📊 Quality Score: {quality:.4f}")
    print(f"   (Measures structural coherence of analysis)")
    
    # Seed (deterministic analysis)
    seed = result.get('seed')
    print(f"\n🔐 Analysis Seed: {seed}")
    print(f"   (Deterministic - can be replayed for verification)")
    
    # Replay validation
    replay_valid = result.get('replay_valid')
    print(f"\n✓ Replay Valid: {replay_valid}")
    
    # Stages completed
    stages = result.get('stages_completed', [])
    print(f"\n📈 Pipeline Stages Completed: {len(stages)}")
    for i, stage in enumerate(stages, 1):
        print(f"   Stage {i}: {stage.get('name', 'Unknown')}")
    
    # Principles (root causes)
    principles = result.get('principles', [])
    print(f"\n⚙️  Causal Principles Identified: {len(principles)}")
    for i, principle in enumerate(principles, 1):
        print(f"\n   Principle {i}:")
        print(f"     - Type: {principle.get('type', 'unknown')}")
        print(f"     - Description: {principle.get('description', 'N/A')}")
    
    print("\n" + "="*80)
    print("DIAGNOSIS")
    print("="*80)
    print("""
ROOT CAUSE: Path Traversal Overflow
├─ The HTML uses: ../../../wiki_assets/entity_images/electron_field.png
├─ This attempts to go up 3 levels from C:\\Determined
├─ After level 1: C:\\
├─ After level 2: INVALID (already at root)
└─ Result: Browser cannot resolve path

CORRECT PATH:
├─ HTML at: C:\\Determined\\ELECTRON_ENCYCLOPEDIA.html
├─ Image at: C:\\Determined\\wiki_assets\\entity_images\\electron_field.png
├─ Both share same parent: C:\\Determined
└─ Relative path should be: wiki_assets/entity_images/electron_field.png
                           (no ../ prefixes needed)

FIX STRATEGY:
├─ Remove all ../ traversal
├─ Use direct path: wiki_assets/entity_images/electron_field.png
├─ Or absolute if serving from web: /wiki_assets/entity_images/electron_field.png
└─ Test with browser F12 to verify loading
    """)
    
    return result


if __name__ == "__main__":
    result = analyze_image_loading_issue()
    
    # Display full UFM response for reference
    print("\n" + "="*80)
    print("FULL UFM ENGINE RESPONSE")
    print("="*80)
    print(json.dumps(result, indent=2, default=str))
