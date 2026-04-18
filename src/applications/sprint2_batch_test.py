#!/usr/bin/env python3
"""
Sprint 2 Batch Testing - Generate test votes for participation portal
"""

import sys
import subprocess
import json
from pathlib import Path

def run_batch_vote(voter_name, issue, choice):
    """Run a batch vote"""
    cmd = [
        sys.executable,
        "participation_portal.py",
        "--batch",
        voter_name,
        issue,
        choice
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
    print(result.stdout)
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        return False
    return True

def main():
    print("="*70)
    print("SPRINT 2: PARTICIPATION PORTAL - BATCH TESTING")
    print("="*70)
    print("\nRecording test votes from multiple participants...")
    
    # Test votes - 3+ people voting on both issues
    test_votes = [
        # Issue A votes
        ("Alice Chen", "A", "REMOVE"),
        ("Bob Martinez", "A", "KEEP_INVESTIGATE"),
        ("Carol Wang", "A", "KEEP_INVESTIGATE"),
        ("David Lee", "A", "REMOVE"),
        
        # Issue B votes
        ("Alice Chen", "B", "INVESTIGATE"),
        ("Bob Martinez", "B", "PATTERN_CHECK"),
        ("Carol Wang", "B", "TRIGGER_ALERT"),
        ("David Lee", "B", "INVESTIGATE"),
    ]
    
    success_count = 0
    for voter_name, issue, choice in test_votes:
        print(f"\n[{success_count+1}/{len(test_votes)}] Recording: {voter_name} → Issue {issue}: {choice}")
        if run_batch_vote(voter_name, issue, choice):
            success_count += 1
    
    print(f"\n{'='*70}")
    print(f"\n[OK] SPRINT 2 TEST COMPLETE")
    print(f"{'='*70}")
    print(f"Successfully recorded {success_count}/{len(test_votes)} votes")
    
    # Display final ledger
    ledger_path = Path(__file__).parent / "participation_ledger.jsonl"
    if ledger_path.exists():
        votes = []
        with open(ledger_path, 'r') as f:
            for line in f:
                if line.strip():
                    votes.append(json.loads(line))
        
        print(f"\nLedger Summary:")
        print(f"Total votes recorded: {len(votes)}")
        
        issue_a_votes = [v for v in votes if v['issue'] == 'A']
        issue_b_votes = [v for v in votes if v['issue'] == 'B']
        
        print(f"\nIssue A (Parameter Orphan):")
        for vote in issue_a_votes:
            print(f"  - {vote['voter_name']}: {vote['vote_choice']}")
        
        print(f"\nIssue B (Temporal Anomaly):")
        for vote in issue_b_votes:
            print(f"  - {vote['voter_name']}: {vote['vote_choice']}")
    
    return success_count == len(test_votes)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
