#!/usr/bin/env python3
"""
Sprint 2: Participation Portal
Enables humans to vote on resolution of discovered inconsistencies
Records all votes immutably to ledger
"""

import json
import os
from datetime import datetime
from pathlib import Path
import hashlib
import uuid

LEDGER_PATH = Path(__file__).parent / "participation_ledger.jsonl"
ISSUES_DATA = {
    "A": {
        "title": "PARAMETER_NO_APPLICATION",
        "severity": "MEDIUM",
        "description": "Parameter 'unknown' is defined but shows no application across 642 elections",
        "question": "Should we remove the orphaned parameter?",
        "resolution_options": {
            "REMOVE": "Delete the unused parameter from configuration",
            "KEEP_INVESTIGATE": "Keep it but investigate why it's unused",
            "RENAME": "Rename to something meaningful and document it"
        }
    },
    "B": {
        "title": "TEMPORAL_ANOMALY",
        "severity": "MEDIUM",
        "description": "Found 1 election with time gap 10x larger than normal (10.39s vs avg 0.18s)",
        "question": "What caused this temporal anomaly and how should we respond?",
        "resolution_options": {
            "INVESTIGATE": "Deeper analysis of the anomalous election",
            "IGNORE_NORMAL": "Treat as system noise, it's within acceptable variance",
            "TRIGGER_ALERT": "Flag as requiring immediate investigation protocol",
            "PATTERN_CHECK": "Check if this pattern repeats in future elections"
        }
    }
}

def initialize_ledger():
    """Create ledger file if it doesn't exist"""
    if not LEDGER_PATH.exists():
        LEDGER_PATH.touch()
        print(f"[OK] Created participation ledger at: {LEDGER_PATH}")

def display_issue(issue_id):
    """Display an issue with its options"""
    issue = ISSUES_DATA[issue_id]
    print(f"\n{'='*70}")
    print(f"ISSUE {issue_id}: {issue['title']}")
    print(f"{'='*70}")
    print(f"Severity: {issue['severity']}")
    print(f"Description: {issue['description']}")
    print(f"\n❓ {issue['question']}")
    print(f"\nResolution Options:")
    
    for idx, (key, desc) in enumerate(issue['resolution_options'].items(), 1):
        print(f"  {idx}. [{key}] {desc}")
    
    return issue

def get_voter_identity():
    """Get or create voter identity"""
    print("\n" + "="*70)
    print("VOTER IDENTIFICATION")
    print("="*70)
    voter_name = input("Enter your name (or identifier): ").strip()
    voter_email = input("Enter your email (optional): ").strip() or "anonymous"
    
    voter_id = hashlib.sha256(f"{voter_name}:{voter_email}".encode()).hexdigest()[:16]
    
    return {
        "name": voter_name,
        "email": voter_email,
        "voter_id": voter_id,
        "timestamp": datetime.now().isoformat()
    }

def validate_vote_choice(issue_id, choice_num, issue):
    """Validate and return the vote choice"""
    options = list(issue['resolution_options'].keys())
    try:
        idx = int(choice_num) - 1
        if 0 <= idx < len(options):
            return options[idx]
    except ValueError:
        pass
    return None

def record_vote(voter, issue_id, vote_choice, issue):
    """Record a vote immutably to ledger"""
    vote_record = {
        "vote_id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "voter_name": voter['name'],
        "voter_id": voter['voter_id'],
        "issue": issue_id,
        "issue_title": issue['title'],
        "vote_choice": vote_choice,
        "vote_description": issue['resolution_options'][vote_choice],
        "causality": f"HUMAN_VOTE_ISSUE_{issue_id}"
    }
    
    # Calculate immutability hash
    vote_record['vote_hash'] = hashlib.sha256(
        json.dumps(vote_record, sort_keys=True, default=str).encode()
    ).hexdigest()
    
    # Append to ledger (immutable record)
    with open(LEDGER_PATH, 'a') as f:
        f.write(json.dumps(vote_record) + '\n')
    
    return vote_record

def display_voting_status():
    """Show current voting statistics"""
    if not LEDGER_PATH.exists():
        print("No votes recorded yet.")
        return {}
    
    votes_by_issue = {}
    total_voters = set()
    
    with open(LEDGER_PATH, 'r') as f:
        for line in f:
            if line.strip():
                vote = json.loads(line)
                issue = vote['issue']
                choice = vote['vote_choice']
                total_voters.add(vote['voter_id'])
                
                if issue not in votes_by_issue:
                    votes_by_issue[issue] = {}
                if choice not in votes_by_issue[issue]:
                    votes_by_issue[issue][choice] = 0
                
                votes_by_issue[issue][choice] += 1
    
    print(f"\n{'='*70}")
    print("VOTING STATUS")
    print(f"{'='*70}")
    print(f"Total unique voters: {len(total_voters)}")
    print(f"Total votes recorded: {sum(sum(c.values()) for c in votes_by_issue.values())}")
    
    for issue_id in ['A', 'B']:
        if issue_id in votes_by_issue:
            print(f"\nIssue {issue_id} ({ISSUES_DATA[issue_id]['title']}):")
            for choice, count in sorted(votes_by_issue[issue_id].items()):
                print(f"  {choice}: {count} vote(s)")
        else:
            print(f"\nIssue {issue_id} ({ISSUES_DATA[issue_id]['title']}): No votes yet")
    
    return votes_by_issue

def interactive_voting():
    """Main interactive voting interface"""
    initialize_ledger()
    
    print("\n" + "="*70)
    print("[VOTING] ZEROPOINT PARTICIPATION PORTAL - SPRINT 2")
    print("="*70)
    print("You are participating in resolving 2 identified inconsistencies")
    print("Your votes are recorded immutably to the ledger")
    print("Future systems will see your choice and reasoning")
    
    print("\n[INFO] CURRENT STATUS:")
    display_voting_status()
    
    voter = get_voter_identity()
    print(f"\n[OK] Your voter ID: {voter['voter_id']}")
    
    votes_this_session = []
    
    while True:
        print("\n" + "="*70)
        print("VOTING MENU")
        print("="*70)
        print("1. Vote on Issue A (Parameter Orphan)")
        print("2. Vote on Issue B (Temporal Anomaly)")
        print("3. View all votes")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            issue = display_issue('A')
            vote_choice = input("\nEnter your choice (1-3): ").strip()
            validated = validate_vote_choice('A', vote_choice, issue)
            
            if validated:
                vote_record = record_vote(voter, 'A', validated, issue)
                votes_this_session.append(vote_record)
                print(f"\n✅ Vote recorded: {validated}")
                print(f"   Hash: {vote_record['vote_hash'][:16]}...")
            else:
                print("❌ Invalid choice. Please try again.")
        
        elif choice == '2':
            issue = display_issue('B')
            vote_choice = input("\nEnter your choice (1-4): ").strip()
            validated = validate_vote_choice('B', vote_choice, issue)
            
            if validated:
                vote_record = record_vote(voter, 'B', validated, issue)
                votes_this_session.append(vote_record)
                print(f"\n[OK] Vote recorded: {validated}")
                print(f"   Hash: {vote_record['vote_hash'][:16]}...")
            else:
                print("[ERR] Invalid choice. Please try again.")
        
        elif choice == '3':
            display_voting_status()
        
        elif choice == '4':
            break
        
        else:
            print("[ERR] Invalid option. Try again.")
    
    print("\n" + "="*70)
    print(f"SESSION COMPLETE - {len(votes_this_session)} votes recorded")
    print("="*70)
    
    return votes_this_session

def batch_vote(voter_name, vote_issue, vote_choice):
    """Programmatic voting (for testing/automation)"""
    initialize_ledger()
    
    if vote_issue not in ISSUES_DATA:
        raise ValueError(f"Unknown issue: {vote_issue}")
    
    issue = ISSUES_DATA[vote_issue]
    options = list(issue['resolution_options'].keys())
    
    if vote_choice not in options:
        raise ValueError(f"Unknown choice {vote_choice}. Must be one of: {options}")
    
    voter = {
        "name": voter_name,
        "email": "batch_voter",
        "voter_id": hashlib.sha256(f"{voter_name}:batch".encode()).hexdigest()[:16],
        "timestamp": datetime.now().isoformat()
    }
    
    vote_record = record_vote(voter, vote_issue, vote_choice, issue)
    return vote_record

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        # Batch voting mode: python participation_portal.py --batch <name> <issue> <choice>
        if len(sys.argv) < 5:
            print("Usage: python participation_portal.py --batch <name> <issue> <choice>")
            print("Example: python participation_portal.py --batch 'Alice' A REMOVE")
            sys.exit(1)
        
        voter_name = sys.argv[2]
        issue = sys.argv[3]
        choice = sys.argv[4]
        
        try:
            vote = batch_vote(voter_name, issue, choice)
            print(f"[OK] Vote recorded: {voter_name} voted '{choice}' for Issue {issue}")
            print(f"   Vote ID: {vote['vote_id']}")
        except Exception as e:
            print(f"[ERR] Error: {e}")
            sys.exit(1)
    else:
        # Interactive mode
        interactive_voting()
