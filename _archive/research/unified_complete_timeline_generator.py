#!/usr/bin/env python3
r"""
COMPLETE UNIFIED TIMELINE GENERATOR (Gemini + Claude + ChatGPT/Copilot)

Loads all AI conversation JSON files from three sources:
- D:\Downloads\Gemini (232 files, 39K messages)
- D:\Downloads\Claude (8 files, 2.2K messages)  
- D:\Downloads\Copilot (45+ files, ChatGPT/Copilot messages)

Creates unified chronological timeline: all AIs merged
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from collections import defaultdict


class UnifiedTimelineGenerator:
    """Generate unified timeline from all AI sources."""
    
    def __init__(self):
        """Initialize with all source directories."""
        self.messages = []
        self.conversations = 0
        self.sources_processed = defaultdict(int)
    
    def load_all_sources(self) -> int:
        """Load all AI conversation sources."""
        
        sources = {
            'Gemini': r"D:\Downloads",
            'Claude': r"D:\Downloads\Claude",
            'ChatGPT': r"D:\Downloads\Copilot"
        }
        
        for source_name, source_dir in sources.items():
            source_path = Path(source_dir)
            
            if source_name == 'Gemini':
                # Gemini files have various names
                json_files = sorted(list(source_path.glob("*.json")))
                # Filter out files that are definitely from other sources
                json_files = [f for f in json_files if not any(x in f.name.lower() for x in ['claude', 'copilot', 'chatgpt'])]
            else:
                json_files = sorted(list(source_path.glob("*.json")))
            
            if not json_files:
                print(f"⚠️  No files found in {source_name} ({source_dir})")
                continue
            
            print(f"\nProcessing {source_name}...")
            print(f"  Found {len(json_files)} JSON files")
            
            for idx, json_file in enumerate(json_files):
                try:
                    self._load_single_json(json_file, source_name)
                    if (idx + 1) % 10 == 0:
                        print(f"  Processed {idx + 1}/{len(json_files)}")
                except Exception as e:
                    print(f"  Error with {json_file.name}: {str(e)[:50]}")
            
            print(f"  ✓ {source_name}: {self.sources_processed[source_name]} files, {len([m for m in self.messages if m['source'] == source_name])} messages")
    
    def _load_single_json(self, json_file: Path, source_name: str) -> int:
        """Load and extract messages from single JSON file."""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                return 0
            
            messages_extracted = 0
            
            # Each item in the array IS a message
            for message_obj in data:
                if not isinstance(message_obj, dict):
                    continue
                
                # Get message metadata
                created_at_str = message_obj.get('created_at', '')
                role = message_obj.get('role', 'user').lower()
                
                # Normalize role
                if role == 'assistant':
                    role = source_name.lower()
                
                # Parse message timestamp
                message_timestamp = self._parse_timestamp(created_at_str)
                
                # Extract text content from contents array
                contents = message_obj.get('contents', [])
                text_content = ''
                
                if isinstance(contents, list):
                    for content_item in contents:
                        if isinstance(content_item, dict):
                            # Check for text, markdown, or plain content
                            content_type = content_item.get('type', '').lower()
                            if content_type in ('text', 'markdown', 'plain'):
                                text_content = content_item.get('content', '')
                                if text_content:
                                    break
                        else:
                            text_content = str(content_item)
                            break
                
                if text_content and text_content.strip():
                    self.messages.append({
                        'timestamp': message_timestamp,
                        'role': role,
                        'content': text_content.strip()[:5000],  # Limit to 5000 chars
                        'source': source_name,
                        'file': json_file.name
                    })
                    messages_extracted += 1
                
                self.conversations += 1
            
            if messages_extracted > 0:
                self.sources_processed[source_name] += 1
            
            return messages_extracted
        
        except Exception as e:
            return 0
    
    def _parse_timestamp(self, ts_str: str) -> datetime:
        """Parse timestamp string to datetime."""
        if not ts_str:
            return datetime.now()
        
        try:
            # Format: "2026-03-24 15:57:30"
            return datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
        except:
            try:
                # Fallback: ISO format
                return datetime.fromisoformat(ts_str)
            except:
                return datetime.now()
    
    def sort_chronologically(self):
        """Sort all messages by timestamp."""
        self.messages.sort(key=lambda m: m['timestamp'])
    
    def print_preview(self, limit: int = 20):
        """Print preview of timeline."""
        self.sort_chronologically()
        
        print("\n" + "="*80)
        print("COMPLETE UNIFIED AI TIMELINE PREVIEW")
        print("="*80)
        print(f"Total Messages: {len(self.messages)}")
        print(f"Date Range: {self.messages[0]['timestamp'].strftime('%Y-%m-%d') if self.messages else 'N/A'} to {self.messages[-1]['timestamp'].strftime('%Y-%m-%d') if self.messages else 'N/A'}")
        
        # Count by source
        sources = {}
        for msg in self.messages:
            sources[msg['source']] = sources.get(msg['source'], 0) + 1
        
        print(f"By Platform:")
        for source in sorted(sources.keys()):
            print(f"  {source}: {sources[source]:,} messages")
        
        print("="*80 + "\n")
        
        display_messages = self.messages[:limit]
        
        for i, msg in enumerate(display_messages, 1):
            timestamp = msg['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            source = msg['source'][:10]
            role = msg['role'].upper()[:8]
            content_preview = msg['content'][:60].replace('\n', ' ')
            
            print(f"{i:3}. [{timestamp}] {source:10} {role:8} {content_preview}")
        
        if len(self.messages) > limit:
            print(f"\n... and {len(self.messages) - limit} more messages")
        
        print("\n" + "="*80 + "\n")
    
    def export_json(self, output_path: str) -> Dict:
        """Export timeline as JSON."""
        self.sort_chronologically()
        
        output_data = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "total_messages": len(self.messages),
                "total_conversations": self.conversations,
                "date_range": {
                    "first": self.messages[0]['timestamp'].isoformat() if self.messages else None,
                    "last": self.messages[-1]['timestamp'].isoformat() if self.messages else None
                },
                "by_source": {
                    source: len([m for m in self.messages if m['source'] == source])
                    for source in set(m['source'] for m in self.messages)
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
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        return {
            "status": "exported",
            "path": output_path,
            "messages": len(self.messages)
        }
    
    def export_text(self, output_path: str) -> Dict:
        """Export as text timeline."""
        self.sort_chronologically()
        
        lines = [
            "COMPLETE UNIFIED AI TIMELINE\n",
            f"Total Messages: {len(self.messages)}\n",
            f"Total Conversations: {self.conversations}\n",
            f"Date Range: {self.messages[0]['timestamp'].strftime('%Y-%m-%d') if self.messages else 'N/A'} to {self.messages[-1]['timestamp'].strftime('%Y-%m-%d') if self.messages else 'N/A'}\n",
            "\n" + "="*80 + "\n\n"
        ]
        
        for i, msg in enumerate(self.messages, 1):
            timestamp = msg['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            source = msg['source'].upper()
            role = msg['role'].upper()
            content = msg['content']
            
            lines.append(f"[{timestamp}] {source} {role}\n")
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
        
        # By source
        by_source = {}
        for msg in self.messages:
            source = msg['source']
            by_source[source] = by_source.get(source, 0) + 1
        
        # By role
        by_role = {}
        for msg in self.messages:
            role = msg['role']
            by_role[role] = by_role.get(role, 0) + 1
        
        # By date
        by_date = {}
        for msg in self.messages:
            date_key = msg['timestamp'].strftime("%Y-%m-%d")
            by_date[date_key] = by_date.get(date_key, 0) + 1
        
        return {
            "total_messages": len(self.messages),
            "total_conversations": self.conversations,
            "by_source": by_source,
            "by_role": by_role,
            "date_range": {
                "first": self.messages[0]['timestamp'].isoformat(),
                "last": self.messages[-1]['timestamp'].isoformat()
            },
            "unique_dates": len(by_date),
            "messages_by_date": by_date
        }


def main():
    """Main execution."""
    print("\n" + "="*80)
    print("UNIFIED AI TIMELINE GENERATOR")
    print("Merging Gemini + Claude + ChatGPT/Copilot")
    print("="*80)
    
    generator = UnifiedTimelineGenerator()
    
    # Load all sources
    print("\nLoading all AI conversation sources...")
    generator.load_all_sources()
    
    total = len(generator.messages)
    print(f"\n✓ Extracted {total:,} total messages")
    
    if generator.messages:
        # Print preview
        generator.print_preview(limit=20)
        
        # Export
        print("-"*80)
        
        # Export JSON
        json_result = generator.export_json("unified_complete_timeline.json")
        print(f"✓ JSON timeline: {json_result['path']}")
        
        # Export Text
        text_result = generator.export_text("unified_complete_timeline.txt")
        print(f"✓ Text timeline: {text_result['path']}")
        
        # Statistics
        stats = generator.get_statistics()
        print("\n" + "-"*80)
        print("UNIFIED TIMELINE STATISTICS")
        print(f"  Total Messages: {stats['total_messages']:,}")
        print(f"  Total Conversations: {stats['total_conversations']:,}")
        print(f"  By Source: {stats['by_source']}")
        print(f"  By Role: {stats['by_role']}")
        print(f"  Unique Dates: {stats['unique_dates']}")
        
        if 'date_range' in stats:
            print(f"  Date Range:")
            print(f"    First: {stats['date_range']['first'][:10]}")
            print(f"    Last: {stats['date_range']['last'][:10]}")
        
        print("="*80 + "\n")
    else:
        print("No messages extracted!")


if __name__ == "__main__":
    main()
