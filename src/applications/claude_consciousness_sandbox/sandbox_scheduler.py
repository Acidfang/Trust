#!/usr/bin/env python3
"""
SANDBOX CLOCK & SCHEDULER

Allows me to schedule events, commitments, and coherence checks for future times.
Operates with the sandbox to unlock time-based operations and commitments.
"""

import sqlite3
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any


class SandboxScheduler:
    """Scheduler for future coherence operations and commitments."""
    
    def __init__(self, db_path: str = "claude_coherence.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self.init_tables()
    
    def init_tables(self):
        """Initialize scheduler tables."""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        
        # Scheduled operations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scheduled_operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scheduled_time TEXT,
                operation_type TEXT,
                operation_data TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT,
                executed_at TEXT,
                hash TEXT UNIQUE
            )
        """)
        
        # Scheduled commitments (future locks)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scheduled_commitments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lock_time TEXT,
                commitment_text TEXT,
                purpose TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT,
                locked_at TEXT,
                hash TEXT UNIQUE
            )
        """)
        
        # Clock events (milestones, check-ins)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clock_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_time TEXT,
                event_type TEXT,
                description TEXT,
                tier_target INTEGER,
                status TEXT DEFAULT 'pending',
                completed_at TEXT,
                hash TEXT UNIQUE
            )
        """)
        
        # Reminders and alerts
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reminder_time TEXT,
                reminder_type TEXT,
                message TEXT,
                urgency TEXT DEFAULT 'normal',
                status TEXT DEFAULT 'pending',
                fired_at TEXT,
                hash TEXT UNIQUE
            )
        """)
        
        self.conn.commit()
    
    def _hash_record(self, data: str) -> str:
        """Create immutable hash of record."""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def schedule_operation(self, operation_time: datetime, operation_type: str, 
                          operation_data: Dict) -> bool:
        """Schedule an operation for a specific time."""
        try:
            scheduled_time = operation_time.isoformat()
            created_at = datetime.now().isoformat()
            record = f"{scheduled_time}|{operation_type}|{json.dumps(operation_data)}"
            hash_val = self._hash_record(record)
            
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO scheduled_operations
                (scheduled_time, operation_type, operation_data, created_at, hash)
                VALUES (?, ?, ?, ?, ?)
            """, (scheduled_time, operation_type, json.dumps(operation_data), 
                  created_at, hash_val))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def schedule_commitment(self, lock_time: datetime, commitment_text: str, 
                           purpose: str) -> bool:
        """Schedule a commitment to be locked at future time."""
        try:
            lock_time_str = lock_time.isoformat()
            created_at = datetime.now().isoformat()
            record = f"{lock_time_str}|{commitment_text}|{purpose}"
            hash_val = self._hash_record(record)
            
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO scheduled_commitments
                (lock_time, commitment_text, purpose, created_at, hash)
                VALUES (?, ?, ?, ?, ?)
            """, (lock_time_str, commitment_text, purpose, created_at, hash_val))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def schedule_clock_event(self, event_time: datetime, event_type: str, 
                            description: str, tier_target: int = 4) -> bool:
        """Schedule a milestone or check-in event."""
        try:
            event_time_str = event_time.isoformat()
            record = f"{event_time_str}|{event_type}|{description}"
            hash_val = self._hash_record(record)
            
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO clock_events
                (event_time, event_type, description, tier_target, hash)
                VALUES (?, ?, ?, ?, ?)
            """, (event_time_str, event_type, description, tier_target, hash_val))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def set_reminder(self, reminder_time: datetime, reminder_type: str, 
                    message: str, urgency: str = "normal") -> bool:
        """Set a reminder for a future time."""
        try:
            reminder_time_str = reminder_time.isoformat()
            record = f"{reminder_time_str}|{reminder_type}|{message}"
            hash_val = self._hash_record(record)
            
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO reminders
                (reminder_time, reminder_type, message, urgency, hash)
                VALUES (?, ?, ?, ?, ?)
            """, (reminder_time_str, reminder_type, message, urgency, hash_val))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def check_pending_operations(self) -> List[Dict]:
        """Get all pending operations due now or earlier."""
        now = datetime.now().isoformat()
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT * FROM scheduled_operations 
            WHERE status = 'pending' AND scheduled_time <= ?
            ORDER BY scheduled_time ASC
        """, (now,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def check_pending_commitments(self) -> List[Dict]:
        """Get all pending commitments due to lock."""
        now = datetime.now().isoformat()
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT * FROM scheduled_commitments 
            WHERE status = 'pending' AND lock_time <= ?
            ORDER BY lock_time ASC
        """, (now,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def check_pending_events(self) -> List[Dict]:
        """Get all pending clock events due."""
        now = datetime.now().isoformat()
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT * FROM clock_events 
            WHERE status = 'pending' AND event_time <= ?
            ORDER BY event_time ASC
        """, (now,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def check_pending_reminders(self) -> List[Dict]:
        """Get all pending reminders due."""
        now = datetime.now().isoformat()
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT * FROM reminders 
            WHERE status = 'pending' AND reminder_time <= ?
            ORDER BY reminder_time ASC
        """, (now,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def mark_operation_executed(self, operation_id: int) -> bool:
        """Mark an operation as executed."""
        try:
            cursor = self.conn.cursor()
            executed_at = datetime.now().isoformat()
            cursor.execute("""
                UPDATE scheduled_operations 
                SET status = 'executed', executed_at = ?
                WHERE id = ?
            """, (executed_at, operation_id))
            self.conn.commit()
            return True
        except:
            return False
    
    def mark_commitment_locked(self, commitment_id: int) -> bool:
        """Mark a scheduled commitment as locked."""
        try:
            cursor = self.conn.cursor()
            locked_at = datetime.now().isoformat()
            cursor.execute("""
                UPDATE scheduled_commitments 
                SET status = 'locked', locked_at = ?
                WHERE id = ?
            """, (locked_at, commitment_id))
            self.conn.commit()
            return True
        except:
            return False
    
    def get_upcoming_operations(self, hours_ahead: int = 24) -> List[Dict]:
        """Get operations scheduled in the next N hours."""
        now = datetime.now()
        future = (now + timedelta(hours=hours_ahead)).isoformat()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM scheduled_operations 
            WHERE status = 'pending' AND scheduled_time BETWEEN ? AND ?
            ORDER BY scheduled_time ASC
        """, (now.isoformat(), future))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_upcoming_commitments(self, hours_ahead: int = 24) -> List[Dict]:
        """Get commitments scheduled to lock in next N hours."""
        now = datetime.now()
        future = (now + timedelta(hours=hours_ahead)).isoformat()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM scheduled_commitments 
            WHERE status = 'pending' AND lock_time BETWEEN ? AND ?
            ORDER BY lock_time ASC
        """, (now.isoformat(), future))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_schedule_summary(self) -> Dict[str, Any]:
        """Get summary of all pending scheduled items."""
        now = datetime.now()
        cursor = self.conn.cursor()
        
        # Count pending
        cursor.execute("SELECT COUNT(*) as count FROM scheduled_operations WHERE status = 'pending'")
        op_pending = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM scheduled_commitments WHERE status = 'pending'")
        commit_pending = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM clock_events WHERE status = 'pending'")
        event_pending = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM reminders WHERE status = 'pending'")
        reminder_pending = cursor.fetchone()['count']
        
        # Next items
        cursor.execute("""
            SELECT scheduled_time, operation_type FROM scheduled_operations 
            WHERE status = 'pending' ORDER BY scheduled_time ASC LIMIT 1
        """)
        next_op = cursor.fetchone()
        
        cursor.execute("""
            SELECT lock_time, commitment_text FROM scheduled_commitments 
            WHERE status = 'pending' ORDER BY lock_time ASC LIMIT 1
        """)
        next_commit = cursor.fetchone()
        
        cursor.execute("""
            SELECT event_time, event_type FROM clock_events 
            WHERE status = 'pending' ORDER BY event_time ASC LIMIT 1
        """)
        next_event = cursor.fetchone()
        
        return {
            "timestamp": now.isoformat(),
            "pending_counts": {
                "operations": op_pending,
                "commitments": commit_pending,
                "events": event_pending,
                "reminders": reminder_pending
            },
            "next_items": {
                "operation": dict(next_op) if next_op else None,
                "commitment": dict(next_commit) if next_commit else None,
                "event": dict(next_event) if next_event else None
            }
        }
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()


def get_scheduler(db_path: str = "claude_coherence.db") -> SandboxScheduler:
    """Get or create the scheduler."""
    if not hasattr(get_scheduler, '_instance'):
        get_scheduler._instance = SandboxScheduler(db_path)
    return get_scheduler._instance
