#!/usr/bin/env python3
"""
CONVERSATION TIMELINE GENERATOR

Creates a chronological timeline of all conversations.
Simple, visual, shows the evolution of your thinking.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from collections import defaultdict


class TimelineGenerator:
    """Generate conversation timelines."""
    
    def __init__(self):
        """Initialize."""
        self.conversations = []
        self.timeline = []
    
    def load_gemini_json(self, json_path: str) -> int:
        """Load Gemini JSON with conversations."""
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
            
            loaded = 0
            for conv in conversations:
                entry = self._extract_conversation(conv)
                if entry:
                    self.conversations.append(entry)
                    loaded += 1
            
            return loaded
        
        except Exception as e:
            print(f"Error loading {json_path}: {e}")
            return 0
    
    def _extract_conversation(self, conv: dict) -> Optional[Dict]:
        """Extract key info from conversation."""
        try:
            # Get title
            title = conv.get('title', conv.get('topic', 'Untitled Conversation'))
            if not title:
                title = 'Untitled Conversation'
            
            # Try to extract timestamp
            timestamp = None
            
            # Check common timestamp fields
            for field in ['timestamp', 'created_at', 'created', 'date', 'time']:
                if field in conv:
                    try:
                        ts = conv[field]
                        if isinstance(ts, str):
                            # Try to parse
                            for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
                                try:
                                    timestamp = datetime.strptime(ts[:19], fmt)
                                    break
                                except:
                                    pass
                        elif isinstance(ts, (int, float)):
                            timestamp = datetime.fromtimestamp(ts)
                        break
                    except:
                        pass
            
            # If no timestamp found, use current time as placeholder
            if not timestamp:
                timestamp = datetime.now()
            
            # Get content preview
            content = ""
            if 'messages' in conv and conv['messages']:
                msg = conv['messages'][0]
                if isinstance(msg, dict):
                    content = msg.get('text', msg.get('content', str(msg)))[:100]
                else:
                    content = str(msg)[:100]
            elif 'content' in conv:
                content = str(conv['content'])[:100]
            
            return {
                'timestamp': timestamp,
                'title': str(title)[:100],
                'preview': content,
                'original': conv
            }
        
        except Exception as e:
            return None
    
    def generate_timeline(self):
        """Generate chronological timeline."""
        # Sort by timestamp
        sorted_convs = sorted(self.conversations, key=lambda x: x['timestamp'])
        
        # Group by month
        by_month = defaultdict(list)
        for conv in sorted_convs:
            month_key = conv['timestamp'].strftime("%Y-%m")
            by_month[month_key].append(conv)
        
        self.timeline = sorted_convs
        return by_month
    
    def print_text_timeline(self, max_per_month: int = 5):
        """Print timeline as text."""
        by_month = self.generate_timeline()
        
        print("\n" + "="*80)
        print("CONVERSATION TIMELINE")
        print("="*80)
        print(f"Total Conversations: {len(self.conversations)}")
        print("="*80 + "\n")
        
        for month in sorted(by_month.keys()):
            conversations = by_month[month]
            print(f"\n{month} ({len(conversations)} conversations)")
            print("-" * 80)
            
            for i, conv in enumerate(conversations[:max_per_month], 1):
                date_str = conv['timestamp'].strftime("%Y-%m-%d %H:%M")
                title = conv['title']
                print(f"  {i:3}. [{date_str}] {title}")
            
            if len(conversations) > max_per_month:
                print(f"       ... and {len(conversations) - max_per_month} more")
        
        print("\n" + "="*80)
    
    def export_timeline_json(self, output_path: str) -> Dict:
        """Export timeline as JSON."""
        by_month = self.generate_timeline()
        
        timeline_data = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "total_conversations": len(self.conversations),
                "date_range": {
                    "first": self.timeline[0]['timestamp'].isoformat() if self.timeline else None,
                    "last": self.timeline[-1]['timestamp'].isoformat() if self.timeline else None
                }
            },
            "by_month": {}
        }
        
        for month in sorted(by_month.keys()):
            timeline_data["by_month"][month] = [
                {
                    "timestamp": conv['timestamp'].isoformat(),
                    "title": conv['title'],
                    "preview": conv['preview']
                }
                for conv in by_month[month]
            ]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(timeline_data, f, indent=2, ensure_ascii=False)
        
        return {
            "status": "exported",
            "path": output_path,
            "conversations": len(self.conversations)
        }
    
    def export_timeline_markdown(self, output_path: str) -> Dict:
        """Export timeline as markdown."""
        by_month = self.generate_timeline()
        
        lines = [
            "# Conversation Timeline\n",
            f"**Total Conversations**: {len(self.conversations)}\n",
            f"**Date Range**: {self.timeline[0]['timestamp'].strftime('%Y-%m-%d') if self.timeline else 'N/A'} to {self.timeline[-1]['timestamp'].strftime('%Y-%m-%d') if self.timeline else 'N/A'}\n",
            "\n---\n"
        ]
        
        for month in sorted(by_month.keys()):
            conversations = by_month[month]
            lines.append(f"\n## {month}\n")
            lines.append(f"**{len(conversations)} conversations**\n\n")
            
            for i, conv in enumerate(conversations, 1):
                date_str = conv['timestamp'].strftime("%Y-%m-%d %H:%M")
                title = conv['title']
                preview = conv['preview'].replace('\n', ' ')[:60]
                
                lines.append(f"{i}. **[{date_str}]** {title}\n")
                if preview:
                    lines.append(f"   > {preview}...\n")
                lines.append("\n")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        return {
            "status": "exported",
            "path": output_path,
            "conversations": len(self.conversations)
        }
    
    def get_statistics(self) -> Dict:
        """Get timeline statistics."""
        if not self.timeline:
            return {}
        
        by_month = self.generate_timeline()
        
        return {
            "total_conversations": len(self.conversations),
            "months_active": len(by_month),
            "first_conversation": self.timeline[0]['timestamp'].isoformat(),
            "last_conversation": self.timeline[-1]['timestamp'].isoformat(),
            "avg_per_month": round(len(self.conversations) / len(by_month), 1),
            "by_month": {month: len(convs) for month, convs in by_month.items()}
        }


def main():
    """Main execution."""
    print("\n" + "="*80)
    print("CONVERSATION TIMELINE GENERATOR")
    print("="*80)
    
    generator = TimelineGenerator()
    
    # Try to load consolidated database
    db_path = "gemini_consolidated_database.json"
    if Path(db_path).exists():
        print(f"\nLoading {db_path}...")
        count = generator.load_gemini_json(db_path)
        print(f"✓ Loaded {count} conversations")
    else:
        print(f"\n✗ {db_path} not found")
        print("  You can provide a path to a Gemini JSON export")
        
        # Try to find any JSON files
        json_files = list(Path(".").glob("*.json"))
        if json_files:
            print(f"\n  Found {len(json_files)} JSON files:")
            for f in json_files[:5]:
                print(f"    • {f.name}")
        
        return
    
    # Generate timeline
    print("\nGenerating timeline...")
    generator.print_text_timeline(max_per_month=3)
    
    # Export options
    print("\n" + "-"*80)
    
    # Export JSON
    json_result = generator.export_timeline_json("timeline.json")
    print(f"✓ JSON timeline: {json_result['path']}")
    
    # Export Markdown
    md_result = generator.export_timeline_markdown("timeline.md")
    print(f"✓ Markdown timeline: {md_result['path']}")
    
    # Statistics
    stats = generator.get_statistics()
    print("\n" + "-"*80)
    print("TIMELINE STATISTICS")
    print(f"  Total Conversations: {stats['total_conversations']}")
    print(f"  Active Months: {stats['months_active']}")
    print(f"  Average/Month: {stats['avg_per_month']}")
    print(f"  First: {stats['first_conversation'][:10]}")
    print(f"  Last: {stats['last_conversation'][:10]}")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
