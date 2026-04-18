#!/usr/bin/env python3
r"""
COPILOT MESSAGE TIMELINE GENERATOR (44 JSON exports)
Loads all Copilot conversation JSON files from D:\Downloads\Copilot
Extracts individual messages with real timestamps

COHERENCE REQUIREMENT: Verifies trinity before ANY file modification
"""

import json
from pathlib import Path
from datetime import datetime
import sys

# [C]: LIVE ACCOUNTABILITY REQUIRED
from live_accountability_system import LiveAccountabilitySystem


class CopilotTimelineGenerator:
    """Extract timeline from 44 Copilot JSON exports."""
    
    def __init__(self, json_dir: str = r"D:\Downloads\Copilot"):
        """Initialize with JSON directory."""
        self.json_dir = Path(json_dir)
        self.messages = []
        self.conversations_processed = 0
    
    def load_all_json_exports(self) -> int:
        """Load all JSON files from Copilot folder."""
        json_files = sorted(list(self.json_dir.glob("*.json")))
        
        if not json_files:
            print(f"No JSON files found in {self.json_dir}")
            return 0
        
        print(f"Found {len(json_files)} Copilot JSON files to process...")
        
        for idx, json_file in enumerate(json_files):
            try:
                self._load_single_json(json_file)
                print(f"  Processed {idx + 1}/{len(json_files)}: {json_file.name}")
            except Exception as e:
                print(f"  Error with {json_file.name}: {e}")
        
        return len(self.messages)
    
    def _load_single_json(self, json_file: Path) -> int:
        """Load and extract messages from single JSON file."""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                return 0
            
            messages_extracted = 0
            
            for message_obj in data:
                if not isinstance(message_obj, dict):
                    continue
                
                # Get message metadata
                created_at_str = message_obj.get('created_at', '')
                role = message_obj.get('role', 'user').lower()
                
                # Map assistant role to copilot
                if role == 'assistant':
                    role = 'copilot'
                
                # Parse message timestamp
                message_timestamp = self._parse_timestamp(created_at_str)
                
                # Extract text content from contents array
                contents = message_obj.get('contents', [])
                text_content = ''
                
                if isinstance(contents, list):
                    for content_item in contents:
                        if isinstance(content_item, dict):
                            # Check for text or markdown type content
                            content_type = content_item.get('type', '')
                            if content_type in ('text', 'markdown'):
                                text_content = content_item.get('content', '')
                                break
                        else:
                            text_content = str(content_item)
                            break
                
                if text_content and text_content.strip():
                    self.messages.append({
                        'timestamp': message_timestamp,
                        'role': role,
                        'content': text_content.strip()[:5000],
                        'source': 'copilot',
                        'file': json_file.name
                    })
                    messages_extracted += 1
                
                self.conversations_processed += 1
            
            return messages_extracted
        
        except Exception as e:
            return 0
    
    def _parse_timestamp(self, ts_str: str) -> datetime:
        """Parse timestamp string to datetime."""
        if not ts_str:
            return datetime.now()
        
        try:
            return datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
        except:
            try:
                return datetime.fromisoformat(ts_str)
            except:
                return datetime.now()
    
    def sort_chronologically(self):
        """Sort all messages by timestamp."""
        self.messages.sort(key=lambda m: m['timestamp'])
    
    def print_preview(self, limit: int = 15):
        """Print preview of timeline."""
        self.sort_chronologically()
        
        print("\n" + "="*80)
        print("COPILOT MESSAGE TIMELINE PREVIEW")
        print("="*80)
        print(f"Total Messages: {len(self.messages)}")
        print(f"Date Range: {self.messages[0]['timestamp'].strftime('%Y-%m-%d') if self.messages else 'N/A'} to {self.messages[-1]['timestamp'].strftime('%Y-%m-%d') if self.messages else 'N/A'}")
        print("="*80 + "\n")
        
        display_messages = self.messages[:limit]
        
        for i, msg in enumerate(display_messages, 1):
            timestamp = msg['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            role = msg['role'].upper()[:8]
            content_preview = msg['content'][:60].replace('\n', ' ')
            # Handle encoding issues on Windows
            try:
                content_preview = content_preview.encode(sys.stdout.encoding, errors='ignore').decode(sys.stdout.encoding)
            except:
                content_preview = content_preview.encode('ascii', errors='ignore').decode('ascii')
            
            print(f"{i:3}. [{timestamp}] {role:8} {content_preview}")
        
        if len(self.messages) > limit:
            print(f"\n... and {len(self.messages) - limit} more messages")
        
        print("\n" + "="*80 + "\n")
    
    def export_json(self, output_path: str, accountability=None) -> dict:
        """Export timeline as JSON with accountability if provided."""
        self.sort_chronologically()
        
        output_data = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "total_messages": len(self.messages),
                "total_conversations": self.conversations_processed,
                "date_range": {
                    "first": self.messages[0]['timestamp'].isoformat() if self.messages else None,
                    "last": self.messages[-1]['timestamp'].isoformat() if self.messages else None
                }
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
        
        content = json.dumps(output_data, indent=2, ensure_ascii=False)
        
        if accountability:
            description = f"Copilot timeline: {len(self.messages)} messages from {self.conversations_processed} conversations"
            success = accountability.write_file(output_path, content, description, verified=True)
            return {
                "status": "exported" if success else "export_failed",
                "path": output_path,
                "messages": len(self.messages),
                "ledger_recorded": success
            }
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {
                "status": "exported",
                "path": output_path,
                "messages": len(self.messages)
            }
    
    def export_text(self, output_path: str) -> dict:
        """Export as text timeline."""
        self.sort_chronologically()
        
        lines = [
            "COPILOT MESSAGE TIMELINE\n",
            f"Total Messages: {len(self.messages)}\n",
            f"Total Conversations: {self.conversations_processed}\n",
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
    
    def get_statistics(self) -> dict:
        """Get timeline statistics."""
        if not self.messages:
            return {}
        
        self.sort_chronologically()
        
        roles = {}
        for msg in self.messages:
            role = msg['role']
            roles[role] = roles.get(role, 0) + 1
        
        dates = {}
        for msg in self.messages:
            date_key = msg['timestamp'].strftime("%Y-%m-%d")
            dates[date_key] = dates.get(date_key, 0) + 1
        
        return {
            "total_messages": len(self.messages),
            "total_conversations": self.conversations_processed,
            "by_role": roles,
            "date_range": {
                "first": self.messages[0]['timestamp'].isoformat(),
                "last": self.messages[-1]['timestamp'].isoformat()
            },
            "unique_dates": len(dates),
            "messages_by_date": dates
        }


def main():
    """Main execution with live accountability."""
    print("\n" + "="*80)
    print("COPILOT MESSAGE TIMELINE GENERATOR (44 JSON exports)")
    print("="*80)
    
    # [C]: INITIALIZE LIVE ACCOUNTABILITY
    accountability = LiveAccountabilitySystem("accountability.ledger", symbol="copilot")
    
    generator = CopilotTimelineGenerator()
    
    # Load all JSON files
    print("\nLoading all Copilot JSON exports...")
    count = generator.load_all_json_exports()
    print(f"\n[OK] Extracted {count} total messages from {generator.conversations_processed} conversations")
    
    if generator.messages:
        # Print preview
        generator.print_preview(limit=15)
        
        print("-"*80)
        print("\n[C]: Recording outputs to accountability ledger...")
        
        # Export JSON with accountability
        json_result = generator.export_json("copilot_timeline_all_messages.json", accountability=accountability)
        status = "[OK]" if json_result.get('ledger_recorded') else "[FAIL]"
        print(f"{status} JSON timeline: {json_result['path']} [Ledger recorded]")
        
        # Export Text
        text_result = generator.export_text("copilot_timeline_all_messages.txt")
        print(f"[OK] Text timeline: {text_result['path']}")
        
        # Statistics
        stats = generator.get_statistics()
        print("\n" + "-"*80)
        print("COPILOT TIMELINE STATISTICS")
        print(f"  Total Messages: {stats['total_messages']}")
        print(f"  Total Conversations: {stats['total_conversations']}")
        print(f"  By Role: {stats['by_role']}")
        print(f"  Unique Dates: {stats['unique_dates']}")
        print(f"  First: {stats['date_range']['first'][:10]}")
        print(f"  Last: {stats['date_range']['last'][:10]}")
        
        print("\n" + accountability.report())
        print("="*80 + "\n")
    else:
        print("No messages extracted!")


if __name__ == "__main__":
    main()
