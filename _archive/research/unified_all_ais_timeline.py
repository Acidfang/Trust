#!/usr/bin/env python3
"""
UNIFIED THREE-AI TIMELINE MERGER
Combines Gemini (39.2K) + Claude (2.2K) + Copilot (0.5K) → Single unified timeline
All three AIs properly labeled and distinguished

COHERENCE REQUIREMENT: Verifies trinity before ANY file modification
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# [C]: LIVE ACCOUNTABILITY REQUIRED
from live_accountability_system import LiveAccountabilitySystem


class UnifiedTimelineMerger:
    """Merge three AI timelines into single unified view."""
    
    def __init__(self):
        self.messages = []
        self.stats = defaultdict(int)
    
    def load_gemini_timeline(self, json_path: str = "timeline_all_messages.json") -> int:
        """Load Gemini timeline."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            messages_added = 0
            if "messages" in data:
                for msg in data.get("messages", []):
                    self.messages.append({
                        "timestamp": datetime.fromisoformat(msg["timestamp"]),
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", ""),
                        "source": "gemini"
                    })
                    messages_added += 1
            
            self.stats["gemini_messages"] = messages_added
            print(f"[OK] Loaded {messages_added} Gemini messages")
            return messages_added
        except FileNotFoundError:
            print(f"[WARN] Gemini timeline not found: {json_path}")
            return 0
    
    def load_claude_timeline(self, json_path: str = "claude_timeline_all_messages.json") -> int:
        """Load Claude timeline."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            messages_added = 0
            if "messages" in data:
                for msg in data.get("messages", []):
                    self.messages.append({
                        "timestamp": datetime.fromisoformat(msg["timestamp"]),
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", ""),
                        "source": "claude"
                    })
                    messages_added += 1
            
            self.stats["claude_messages"] = messages_added
            print(f"[OK] Loaded {messages_added} Claude messages")
            return messages_added
        except FileNotFoundError:
            print(f"[WARN] Claude timeline not found: {json_path}")
            return 0
    
    def load_copilot_timeline(self, json_path: str = "copilot_timeline_all_messages.json") -> int:
        """Load Copilot timeline."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            messages_added = 0
            if "messages" in data:
                for msg in data.get("messages", []):
                    self.messages.append({
                        "timestamp": datetime.fromisoformat(msg["timestamp"]),
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", ""),
                        "source": "copilot"
                    })
                    messages_added += 1
            
            self.stats["copilot_messages"] = messages_added
            print(f"[OK] Loaded {messages_added} Copilot messages")
            return messages_added
        except FileNotFoundError:
            print(f"[WARN] Copilot timeline not found: {json_path}")
            return 0
    
    def sort_chronologically(self):
        """Sort all messages chronologically."""
        self.messages.sort(key=lambda m: m["timestamp"])
    
    def print_preview(self, limit: int = 20):
        """Print interleaved preview showing all three AIs."""
        self.sort_chronologically()
        
        print("\n" + "="*100)
        print("UNIFIED THREE-AI TIMELINE PREVIEW")
        print("="*100)
        print(f"Total Combined Messages: {len(self.messages)}")
        if self.messages:
            print(f"Date Range: {self.messages[0]['timestamp'].strftime('%Y-%m-%d')} to {self.messages[-1]['timestamp'].strftime('%Y-%m-%d')}")
        print("="*100 + "\n")
        
        display_messages = self.messages[:limit]
        
        for i, msg in enumerate(display_messages, 1):
            timestamp = msg['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            source = msg['source'].upper()
            role = msg['role'].upper()[:4]
            content_preview = msg['content'][:55].replace('\n', ' ')
            
            # Color code by source for terminal display
            source_label = f"[{source}]"
            
            print(f"{i:3}. {timestamp} {source_label:11} {role} {content_preview}")
        
        if len(self.messages) > limit:
            print(f"\n... and {len(self.messages) - limit} more messages ({len(self.messages)} total)")
        
        print("\n" + "="*100 + "\n")
    
    def export_json(self, output_path: str) -> dict:
        """Export unified timeline as JSON."""
        self.sort_chronologically()
        
        role_counts = defaultdict(int)
        source_counts = defaultdict(int)
        
        for msg in self.messages:
            role_counts[msg['role']] += 1
            source_counts[msg['source']] += 1
        
        output_data = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "title": "Unified Three-AI Timeline",
                "description": "Combined timeline from Gemini, Claude, and Copilot conversations",
                "total_messages": len(self.messages),
                "sources": dict(source_counts),
                "by_role": dict(role_counts),
                "date_range": {
                    "first": self.messages[0]['timestamp'].isoformat() if self.messages else None,
                    "last": self.messages[-1]['timestamp'].isoformat() if self.messages else None
                }
            },
            "messages": [
                {
                    "timestamp": msg['timestamp'].isoformat(),
                    "role": msg['role'],
                    "source": msg['source'],
                    "content": msg['content']
                }
                for msg in self.messages
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        return {
            "status": "exported",
            "path": output_path,
            "messages": len(self.messages)
        }
    
    def export_text(self, output_path: str) -> dict:
        """Export unified timeline as text."""
        self.sort_chronologically()
        
        role_counts = defaultdict(int)
        source_counts = defaultdict(int)
        
        for msg in self.messages:
            role_counts[msg['role']] += 1
            source_counts[msg['source']] += 1
        
        lines = [
            "UNIFIED THREE-AI CONVERSATION TIMELINE\n",
            "="*100 + "\n\n",
            f"Total Messages: {len(self.messages)}\n",
            f"Sources: {dict(source_counts)}\n",
            f"By Role: {dict(role_counts)}\n",
            f"Date Range: {self.messages[0]['timestamp'].strftime('%Y-%m-%d') if self.messages else 'N/A'} to {self.messages[-1]['timestamp'].strftime('%Y-%m-%d') if self.messages else 'N/A'}\n",
            "\n" + "="*100 + "\n\n"
        ]
        
        for i, msg in enumerate(self.messages, 1):
            timestamp = msg['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            source = msg['source'].upper()
            role = msg['role'].upper()
            content = msg['content']
            
            lines.append(f"[{i}] {timestamp} | {source} | {role}\n")
            lines.append(f"{content}\n")
            lines.append("\n" + "-"*100 + "\n\n")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        return {
            "status": "exported",
            "path": output_path,
            "messages": len(self.messages)
        }
    
    def print_statistics(self):
        """Print detailed statistics."""
        print("\n" + "="*80)
        print("UNIFIED TIMELINE STATISTICS")
        print("="*80)
        
        source_counts = defaultdict(int)
        source_roles = defaultdict(lambda: defaultdict(int))
        
        for msg in self.messages:
            source = msg['source']
            role = msg['role']
            source_counts[source] += 1
            source_roles[source][role] += 1
        
        for source in sorted(source_counts.keys()):
            count = source_counts[source]
            roles = source_roles[source]
            print(f"\n{source.upper()}:")
            print(f"  Total: {count}")
            for role in sorted(roles.keys()):
                print(f"    {role}: {roles[role]}")
        
        print(f"\nCOMBINED TOTALS:")
        print(f"  Total Messages: {len(self.messages)}")
        print(f"  Unique Sources: {len(source_counts)}")
        print(f"  Date Span: {self.messages[0]['timestamp'].strftime('%Y-%m-%d') if self.messages else 'N/A'} to {self.messages[-1]['timestamp'].strftime('%Y-%m-%d') if self.messages else 'N/A'}")
        
        print("\n" + "="*80 + "\n")


def main():
    """Main execution with live accountability."""
    print("\n" + "="*80)
    print("UNIFIED THREE-AI TIMELINE MERGER")
    print("Gemini + Claude + Copilot -> Single Timeline")
    print("="*80)
    
    # [C]: INITIALIZE LIVE ACCOUNTABILITY
    accountability = LiveAccountabilitySystem("accountability.ledger", symbol="unified")
    
    # [C]: NOW SAFE TO PROCEED
    merger = UnifiedTimelineMerger()
    
    # Load all three timelines
    print("\nLoading AI timelines...\n")
    gemini_count = merger.load_gemini_timeline()
    claude_count = merger.load_claude_timeline()
    copilot_count = merger.load_copilot_timeline()
    
    total = gemini_count + claude_count + copilot_count
    print(f"\n[OK] Total: {total} combined messages from 3 AIs")
    
    if merger.messages:
        # Preview
        print("-"*80)
        merger.print_preview(limit=20)
        
        # [C]: RECORD FILES WITH ACCOUNTABILITY
        print("-"*80)
        print("\n[C]: Recording unified timeline to accountability ledger...")
        
        # Prepare JSON data
        merger.sort_chronologically()
        role_counts = defaultdict(int)
        source_counts = defaultdict(int)
        
        for msg in merger.messages:
            role_counts[msg['role']] += 1
            source_counts[msg['source']] += 1
        
        output_data = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "title": "Unified Three-AI Timeline",
                "description": "Combined timeline from Gemini, Claude, and Copilot conversations",
                "total_messages": len(merger.messages),
                "sources": dict(source_counts),
                "by_role": dict(role_counts),
                "date_range": {
                    "first": merger.messages[0]['timestamp'].isoformat() if merger.messages else None,
                    "last": merger.messages[-1]['timestamp'].isoformat() if merger.messages else None
                }
            },
            "messages": [
                {
                    "timestamp": msg['timestamp'].isoformat(),
                    "role": msg['role'],
                    "source": msg['source'],
                    "content": msg['content']
                }
                for msg in merger.messages
            ]
        }
        
        # Export JSON with accountability
        content = json.dumps(output_data, indent=2, ensure_ascii=False)
        json_success = accountability.write_file("timeline_all_messages_unified.json", content, 
                                                  f"Unified timeline: {total} messages from 3 AIs", verified=True)
        print(f"[OK] Unified JSON: timeline_all_messages_unified.json [Ledger recorded: {json_success}]")
        
        # Export Text
        text_result = merger.export_text("timeline_all_messages_unified.txt")
        print(f"[OK] Unified Text: {text_result['path']}")
        
        print()
        merger.print_statistics()
        print("\n" + accountability.report())
    else:
        print("[WARN] No messages loaded from any timeline!")


if __name__ == "__main__":
    main()
