#!/usr/bin/env python3
"""
GENERATOR WITH LIVE ACCOUNTABILITY
Example: Claude timeline generator modified to use accountability system
Every JSON output is recorded in binary ledger before file write.
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

from live_accountability_system import LiveAccountabilitySystem


class ClaudeTimelineWithAccountability:
    """Claude timeline generator with live ledger accountability."""
    
    def __init__(self, ledger_path: str = "accountability.ledger"):
        self.accountability = LiveAccountabilitySystem(ledger_path, symbol="claude")
        self.messages = []
        self.stats = defaultdict(int)
    
    def load_claude_timeline(self, json_path: str = "claude_timeline.json") -> int:
        """Load Claude timeline from JSON."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            messages_added = 0
            if "messages" in data:
                for msg in data.get("messages", []):
                    self.messages.append({
                        "timestamp": msg.get("timestamp", datetime.now().isoformat()),
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", ""),
                        "source": "claude"
                    })
                    messages_added += 1
            
            self.stats["claude_loaded"] = messages_added
            return messages_added
        
        except FileNotFoundError:
            print(f"File not found: {json_path}")
            return 0
    
    def generate_timeline(self) -> dict:
        """Generate unified timeline."""
        if not self.messages:
            return {"messages": [], "stats": dict(self.stats)}
        
        # Sort by timestamp
        sorted_messages = sorted(self.messages, key=lambda m: m.get("timestamp", ""))
        
        timeline = {
            "generated_at": datetime.now().isoformat(),
            "total_messages": len(sorted_messages),
            "messages": sorted_messages,
            "source_stats": dict(self.stats)
        }
        
        return timeline
    
    def save_with_accountability(self, output_path: str = "claude_timeline_complete.json") -> bool:
        """
        Save timeline to JSON with mandatory ledger recording.
        
        Ledger records BEFORE file write.
        If ledger fails, file is NOT written.
        """
        
        timeline = self.generate_timeline()
        content = json.dumps(timeline, indent=2)
        
        description = f"Generated Claude timeline: {timeline['total_messages']} messages"
        
        # This calls live_accountability_system internally
        # Ledger records first, then file writes
        return self.accountability.write_file(
            output_path,
            content,
            description,
            verified=True
        )
    
    def get_accountability_report(self) -> str:
        """Get ledger accountability report."""
        return self.accountability.report()


# Test generator with accountability
if __name__ == "__main__":
    gen = ClaudeTimelineWithAccountability("accountability_generator_test.ledger")
    
    # Clear ledger
    gen.accountability.ledger_path.write_bytes(b"")
    
    print("[GENERATOR WITH LIVE ACCOUNTABILITY TEST]")
    print()
    
    # Simulate some messages
    gen.messages = [
        {
            "timestamp": "2026-04-08T10:00:00",
            "role": "user",
            "content": "Test message 1",
            "source": "claude"
        },
        {
            "timestamp": "2026-04-08T10:01:00",
            "role": "assistant",
            "content": "Test response 1",
            "source": "claude"
        }
    ]
    
    # Save with accountability - ledger records first
    success = gen.save_with_accountability("test_claude_timeline.json")
    
    print(f"Save with accountability: {'✓ SUCCESS' if success else '✗ FAILED'}")
    print()
    
    print(gen.get_accountability_report())
    print()
    
    # Verify file exists
    if Path("test_claude_timeline.json").exists():
        print("✓ JSON file created and recorded in ledger")
        with open("test_claude_timeline.json") as f:
            data = json.load(f)
            print(f"  Messages: {data['total_messages']}")
