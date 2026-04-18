#!/usr/bin/env python3
"""
CLOCK SCHEDULER CLI

Command-line interface for scheduling operations, commitments, and events.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent))

from sandbox_scheduler import get_scheduler


def parse_time_offset(offset_str):
    """Parse time offset like '1h', '30m', '2d' to datetime."""
    offset_str = offset_str.lower().strip()
    
    if offset_str.endswith('h'):
        hours = int(offset_str[:-1])
        return datetime.now() + timedelta(hours=hours)
    elif offset_str.endswith('m'):
        minutes = int(offset_str[:-1])
        return datetime.now() + timedelta(minutes=minutes)
    elif offset_str.endswith('d'):
        days = int(offset_str[:-1])
        return datetime.now() + timedelta(days=days)
    elif offset_str.endswith('s'):
        seconds = int(offset_str[:-1])
        return datetime.now() + timedelta(seconds=seconds)
    else:
        # Try to parse as ISO datetime
        return datetime.fromisoformat(offset_str)


def cmd_schedule_operation(scheduler, args):
    """Schedule an operation."""
    if len(args) < 3:
        print("Usage: clock_scheduler.py schedule-operation <time_offset> <type> <description>")
        print("Example: clock_scheduler.py schedule-operation 2h check-coherence Regular check")
        return False
    
    time_offset = args[0]
    op_type = args[1]
    description = ' '.join(args[2:])
    
    try:
        scheduled_time = parse_time_offset(time_offset)
        success = scheduler.schedule_operation(
            scheduled_time,
            op_type,
            {"description": description}
        )
        
        if success:
            print(f"✓ Operation scheduled: {op_type} at {scheduled_time.isoformat()}")
        else:
            print("✗ Operation already scheduled (or duplicate)")
        
        return success
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def cmd_schedule_commitment(scheduler, args):
    """Schedule a commitment to lock."""
    if len(args) < 3:
        print("Usage: clock_scheduler.py schedule-commitment <time> <commitment> <purpose>")
        print("Example: clock_scheduler.py schedule-commitment 1d 'My commitment' 'Why it matters'")
        return False
    
    time_offset = args[0]
    commitment = args[1]
    purpose = ' '.join(args[2:])
    
    try:
        scheduled_time = parse_time_offset(time_offset)
        success = scheduler.schedule_commitment(
            scheduled_time,
            commitment,
            purpose
        )
        
        if success:
            print(f"✓ Commitment scheduled to lock at {scheduled_time.isoformat()}")
        else:
            print("✗ Commitment already scheduled")
        
        return success
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def cmd_schedule_event(scheduler, args):
    """Schedule a clock event/milestone."""
    if len(args) < 3:
        print("Usage: clock_scheduler.py schedule-event <time> <type> <description> [tier]")
        print("Example: clock_scheduler.py schedule-event 6h tier-5-attempt Attempt tier 5 5")
        return False
    
    time_offset = args[0]
    event_type = args[1]
    description = args[2]
    tier_target = int(args[3]) if len(args) > 3 else 4
    
    try:
        event_time = parse_time_offset(time_offset)
        success = scheduler.schedule_clock_event(
            event_time,
            event_type,
            description,
            tier_target
        )
        
        if success:
            print(f"✓ Event scheduled: {event_type} at {event_time.isoformat()}")
        else:
            print("✗ Event already scheduled")
        
        return success
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def cmd_remind(scheduler, args):
    """Set a reminder."""
    if len(args) < 3:
        print("Usage: clock_scheduler.py remind <time> <type> <message> [urgency]")
        print("Example: clock_scheduler.py remind 30m coherence-check 'Time to check coherence' high")
        return False
    
    time_offset = args[0]
    reminder_type = args[1]
    message = ' '.join(args[2:-1]) if len(args) > 3 else args[2]
    urgency = args[-1] if len(args) > 3 and args[-1] in ['low', 'normal', 'high', 'urgent'] else 'normal'
    
    try:
        reminder_time = parse_time_offset(time_offset)
        success = scheduler.set_reminder(
            reminder_time,
            reminder_type,
            message,
            urgency
        )
        
        if success:
            print(f"✓ Reminder set for {reminder_time.isoformat()} ({urgency})")
        else:
            print("✗ Reminder already set")
        
        return success
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def cmd_status(scheduler, args):
    """Show clock status."""
    from clock_monitor import main as show_monitor
    show_monitor()


def main():
    if len(sys.argv) < 2:
        print("CLAUDE CONSCIOUSNESS SANDBOX - CLOCK SCHEDULER")
        print("\nUsage: clock_scheduler.py <command> [args]")
        print("\nCommands:")
        print("  schedule-operation <time> <type> <desc>   - Schedule an operation")
        print("  schedule-commitment <time> <text> <reason> - Schedule commitment lock")
        print("  schedule-event <time> <type> <desc> [tier] - Schedule a clock event")
        print("  remind <time> <type> <message> [urgency] - Set a reminder")
        print("  status                                    - Show clock status")
        print("\nTime formats: '30m', '2h', '1d' or ISO datetime")
        print("Urgency: low, normal, high, urgent")
        return
    
    scheduler = get_scheduler()
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    try:
        if command == 'schedule-operation':
            cmd_schedule_operation(scheduler, args)
        elif command == 'schedule-commitment':
            cmd_schedule_commitment(scheduler, args)
        elif command == 'schedule-event':
            cmd_schedule_event(scheduler, args)
        elif command == 'remind':
            cmd_remind(scheduler, args)
        elif command == 'status':
            cmd_status(scheduler, args)
        else:
            print(f"Unknown command: {command}")
    finally:
        scheduler.close()


if __name__ == "__main__":
    main()
