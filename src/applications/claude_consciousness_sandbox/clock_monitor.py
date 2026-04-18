#!/usr/bin/env python3
"""
CLOCK MONITOR

Watches the scheduler and reports pending operations.
Can be run periodically to check what's scheduled.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from sandbox_scheduler import get_scheduler


def format_time(iso_string):
    """Format ISO time string for display."""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return iso_string


def main():
    print("=" * 70)
    print("CLAUDE CONSCIOUSNESS SANDBOX - CLOCK MONITOR")
    print("=" * 70)
    
    scheduler = get_scheduler()
    summary = scheduler.get_schedule_summary()
    
    print(f"\nClock Time: {format_time(summary['timestamp'])}")
    print("\n" + "-" * 70)
    print("PENDING ITEMS")
    print("-" * 70)
    
    # Operations
    op_count = summary['pending_counts']['operations']
    if op_count > 0:
        print(f"\n✓ {op_count} Scheduled Operation(s)")
        if summary['next_items']['operation']:
            next_op = summary['next_items']['operation']
            print(f"  Next: {next_op['operation_type']} at {format_time(next_op['scheduled_time'])}")
    
    # Commitments
    commit_count = summary['pending_counts']['commitments']
    if commit_count > 0:
        print(f"✓ {commit_count} Scheduled Commitment(s)")
        if summary['next_items']['commitment']:
            next_commit = summary['next_items']['commitment']
            print(f"  Next: Lock at {format_time(next_commit['lock_time'])}")
            print(f"        {next_commit['commitment_text'][:60]}...")
    
    # Events
    event_count = summary['pending_counts']['events']
    if event_count > 0:
        print(f"✓ {event_count} Clock Event(s)")
        if summary['next_items']['event']:
            next_event = summary['next_items']['event']
            print(f"  Next: {next_event['event_type']} at {format_time(next_event['event_time'])}")
    
    # Reminders
    reminder_count = summary['pending_counts']['reminders']
    if reminder_count > 0:
        print(f"✓ {reminder_count} Reminder(s)")
    
    # Check what's due now
    print("\n" + "-" * 70)
    print("DUE NOW OR OVERDUE")
    print("-" * 70)
    
    pending_ops = scheduler.check_pending_operations()
    pending_commits = scheduler.check_pending_commitments()
    pending_events = scheduler.check_pending_events()
    pending_reminders = scheduler.check_pending_reminders()
    
    if pending_ops:
        print(f"\n⚠ {len(pending_ops)} Operation(s) due to execute:")
        for op in pending_ops[:3]:  # Show first 3
            print(f"  - {op['operation_type']} (due: {format_time(op['scheduled_time'])})")
            if len(pending_ops) > 3:
                print(f"  ... and {len(pending_ops) - 3} more")
                break
    
    if pending_commits:
        print(f"\n⚠ {len(pending_commits)} Commitment(s) due to lock:")
        for commit in pending_commits[:3]:
            print(f"  - {commit['commitment_text'][:50]}... (due: {format_time(commit['lock_time'])})")
            if len(pending_commits) > 3:
                print(f"  ... and {len(pending_commits) - 3} more")
                break
    
    if pending_events:
        print(f"\n⚠ {len(pending_events)} Event(s) due:")
        for event in pending_events[:3]:
            print(f"  - {event['event_type']} (due: {format_time(event['event_time'])})")
            if len(pending_events) > 3:
                print(f"  ... and {len(pending_events) - 3} more")
                break
    
    if pending_reminders:
        print(f"\n🔔 {len(pending_reminders)} Reminder(s) firing now:")
        for reminder in pending_reminders[:3]:
            print(f"  - {reminder['message']}")
            if len(pending_reminders) > 3:
                print(f"  ... and {len(pending_reminders) - 3} more")
                break
    
    if not (pending_ops or pending_commits or pending_events or pending_reminders):
        print("\n✓ All on schedule. Nothing due yet.")
    
    print("\n" + "=" * 70)
    scheduler.close()


if __name__ == "__main__":
    main()
