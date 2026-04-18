#!/usr/bin/env python3
"""
MESSAGE TIMELINE GENERATOR

Creates a simple chronological timeline of ALL messages from conversations.
Output: What was said + when. Sorted chronologically.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class MessageTimelineGenerator:
    """Extract and timeline individual messages."""
    
    def __init__(self):
        """Initialize."""
        self.messages = []  # List of (timestamp, role, content, source)
    
    def load_gemini_json(self, json_path: str) -> int:
        """Load Gemini JSON and extract all messages."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different formats
            conversations = []
            if isinstance(data, dict):
                if 'conversations' in data:
                    conversations = data['conversations']
                elif 'entries' in data:
                    conversations = data['entries']
                else:
                    conversations = [data]
            else:
                conversations = data if isinstance(data, list) else [data]
            
            extracted = 0
            for conv_idx, conv in enumerate(conversations):
                count = self._extract_messages_from_conversation(conv, conv_idx)
                extracted += count
            
            return extracted
        
        except Exception as e:
            print(f"Error loading {json_path}: {e}")
            return 0
    
    def _extract_messages_from_conversation(self, conv: dict, conv_idx: int = 0) -> int:
        """Extract all individual messages from a conversation."""
        try:
            messages_list = []
            
            # Try to find messages in conversation
            if 'messages' in conv and isinstance(conv['messages'], list):
                messages_list = conv['messages']
            elif 'message' in conv:
                messages_list = [conv['message']]
            elif 'content' in conv:
                messages_list = [conv['content']]
            
            # Try to get conversation timestamp as baseline
            conv_timestamp = self._parse_timestamp(conv.get('timestamp', conv.get('created', None)))
            
            extracted = 0
            for msg_idx, msg in enumerate(messages_list):
                if isinstance(msg, dict):
                    # Extract message data
                    content = ""
                    role = "user"
                    timestamp = conv_timestamp
                    
                    # Get content
                    for field in ['text', 'content', 'message', 'body']:
                        if field in msg:
                            content = msg[field]
                            break
                    
                    # Get role (user/assistant/system)
                    for field in ['role', 'author', 'sender', 'type']:
                        if field in msg:
                            role = str(msg[field]).lower()
                            break
                    
                    # Get message-specific timestamp if available
                    for field in ['timestamp', 'created_at', 'time', 'date']:
                        if field in msg:
                            parsed_ts = self._parse_timestamp(msg[field])
                            if parsed_ts:
                                timestamp = parsed_ts
                                break
                    
                    # Add fallback: offset timestamp by message index if no individual timestamp
                    if timestamp == conv_timestamp and msg_idx > 0:
                        timestamp = datetime.fromtimestamp(
                            conv_timestamp.timestamp() + (msg_idx * 60)
                        )  # 1 minute offset per message if no timestamp
                    
                    # Only add non-empty messages
                    if content and isinstance(content, str) and content.strip():
                        self.messages.append({
                            'timestamp': timestamp,
                            'role': role,
                            'content': content.strip(),
                            'source': 'gemini',
                            'conv_idx': conv_idx,
                            'msg_idx': msg_idx
                        })
                        extracted += 1
                
                elif isinstance(msg, str) and msg.strip():
                    # Simple string message
                    timestamp = conv_timestamp
                    if msg_idx > 0:
                        timestamp = datetime.fromtimestamp(
                            conv_timestamp.timestamp() + (msg_idx * 60)
                        )
                    
                    self.messages.append({
                        'timestamp': timestamp,
                        'role': 'user',
                        'content': msg.strip(),
                        'source': 'gemini',
                        'conv_idx': conv_idx,
                        'msg_idx': msg_idx
                    })
                    extracted += 1
            
            return extracted
        
        except Exception as e:
            return 0
    
    def _parse_timestamp(self, ts) -> datetime:
        """Parse timestamp from various formats. Always returns a datetime."""
        if not ts:
            return datetime.now()
        
        try:
            if isinstance(ts, str):
                # Try common formats
                for fmt in [
                    "%Y-%m-%dT%H:%M:%S",
                    "%Y-%m-%d %H:%M:%S",
                    "%Y-%m-%dT%H:%M:%SZ",
                    "%Y-%m-%d"
                ]:
                    try:
                        result = datetime.strptime(ts[:19], fmt)
                        if result:
                            return result
                    except:
                        pass
            
            elif isinstance(ts, (int, float)):
                try:
                    result = datetime.fromtimestamp(ts)
                    if result:
                        return result
                except:
                    pass
        
        except:
            pass
        
        # Fallback: always return a valid datetime
        return datetime.now()
    
    def sort_chronologically(self):
        """Sort all messages by timestamp."""
        self.messages.sort(key=lambda m: m['timestamp'])
    
    def print_text_timeline(self, limit: Optional[int] = None):
        """Print timeline as readable text."""
        self.sort_chronologically()
        
        print("\n" + "="*80)
        print("MESSAGE TIMELINE")
        print("="*80)
        print(f"Total Messages: {len(self.messages)}")
        print("="*80 + "\n")
        
        display_messages = self.messages[:limit] if limit else self.messages
        
        for i, msg in enumerate(display_messages, 1):
            timestamp = msg['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            role = msg['role'].upper()
            content_preview = msg['content'][:70].replace('\n', ' ')
            
            print(f"{i:5}. [{timestamp}] {role:10} {content_preview}")
            if len(msg['content']) > 70:
                print(f"       ... (truncated, see JSON for full content)")
            print()
        
        if limit and len(self.messages) > limit:
            print(f"\n... and {len(self.messages) - limit} more messages")
        
        print("="*80 + "\n")
    
    def export_json(self, output_path: str) -> Dict:
        """Export all messages as JSON."""
        self.sort_chronologically()
        
        output_data = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "total_messages": len(self.messages),
                "date_range": {
                    "first": self.messages[0]['timestamp'].isoformat() if self.messages else None,
                    "last": self.messages[-1]['timestamp'].isoformat() if self.messages else None
                },
                "sources": list(set(m['source'] for m in self.messages))
            },
            "messages": [
                {
                    "timestamp": msg['timestamp'].isoformat(),
                    "role": msg['role'],
                    "content": msg['content'],
                    "source": msg['source']
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
    
    def export_text(self, output_path: str) -> Dict:
        """Export as simple text timeline."""
        self.sort_chronologically()
        
        lines = [
            "MESSAGE TIMELINE\n",
            f"Total Messages: {len(self.messages)}\n",
            f"Date Range: {self.messages[0]['timestamp'].strftime('%Y-%m-%d') if self.messages else 'N/A'} to {self.messages[-1]['timestamp'].strftime('%Y-%m-%d') if self.messages else 'N/A'}\n",
            "\n" + "="*80 + "\n\n"
        ]
        
        for i, msg in enumerate(self.messages, 1):
            timestamp = msg['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            role = msg['role'].upper()
            content = msg['content']
            
            lines.append(f"[{timestamp}] {role}\n")
            lines.append(f"{content}\n")
            lines.append(f"\n{'-'*80}\n\n")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        return {
            "status": "exported",
            "path": output_path,
            "messages": len(self.messages)
        }
    
    def get_statistics(self) -> Dict:
        """Get timeline statistics."""
        if not self.messages:
            return {}
        
        self.sort_chronologically()
        
        roles = {}
        for msg in self.messages:
            role = msg['role']
            roles[role] = roles.get(role, 0) + 1
        
        return {
            "total_messages": len(self.messages),
            "by_role": roles,
            "date_range": {
                "first": self.messages[0]['timestamp'].isoformat(),
                "last": self.messages[-1]['timestamp'].isoformat()
            },
            "sources": list(set(m['source'] for m in self.messages))
        }


def main():
    """Main execution."""
    print("\n" + "="*80)
    print("MESSAGE TIMELINE GENERATOR")
    print("="*80)
    
    generator = MessageTimelineGenerator()
    
    # Try to load consolidated database
    db_path = "gemini_consolidated_database.json"
    if Path(db_path).exists():
        print(f"\nLoading {db_path}...")
        count = generator.load_gemini_json(db_path)
        print(f"✓ Extracted {count} individual messages")
    else:
        print(f"\n✗ {db_path} not found")
        print("  Looking for JSON files...")
        
        json_files = list(Path(".").glob("*.json"))
        if json_files:
            print(f"  Found {len(json_files)} JSON files:")
            for f in json_files[:5]:
                print(f"    • {f.name}")
        
        return
    
    # Print preview
    if generator.messages:
        print("\nGenerating timeline...")
        generator.print_text_timeline(limit=10)
    
    # Export
    print("-"*80)
    
    # Export JSON
    json_result = generator.export_json("timeline_all_messages.json")
    print(f"✓ JSON timeline: {json_result['path']}")
    
    # Export Text
    text_result = generator.export_text("timeline_all_messages.txt")
    print(f"✓ Text timeline: {text_result['path']}")
    
    # Statistics
    stats = generator.get_statistics()
    print("\n" + "-"*80)
    print("STATISTICS")
    print(f"  Total Messages: {stats['total_messages']}")
    print(f"  By Role: {stats['by_role']}")
    print(f"  First: {stats['date_range']['first'][:10]}")
    print(f"  Last: {stats['date_range']['last'][:10]}")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
