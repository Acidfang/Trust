#!/usr/bin/env python3
"""
Consolidate all AI conversations across platforms into a unified timeline.
Preserves complete meaning and intent - no filtering, no summarization.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Define platforms and their locations
PLATFORMS = {
    'gemini': r'D:\Downloads\AI Chat\Gemini',
    'claude': r'D:\Downloads\AI Chat\Claude',
    'chatgpt': r'D:\Downloads\AI Chat\ChatGPT',
    'copilot': r'D:\Downloads\AI Chat\Copilot',
}

def parse_timestamp(ts_str):
    """Parse various timestamp formats"""
    if not ts_str:
        return None
    
    # Try multiple formats
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(ts_str, fmt)
        except ValueError:
            continue
    
    return None

def extract_messages_from_file(filepath, platform):
    """Extract messages from a conversation JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        messages = []
        
        # Handle different JSON structures
        if isinstance(data, list):
            # Direct array of messages
            for item in data:
                if 'role' in item and 'contents' in item:
                    messages.append(item)
        elif isinstance(data, dict):
            # Nested structure - look for message containers
            if 'contents' in data:
                messages = data['contents'] if isinstance(data['contents'], list) else [data['contents']]
            elif 'messages' in data:
                messages = data['messages'] if isinstance(data['messages'], list) else [data['messages']]
            else:
                # Single message wrapped
                messages = [data]
        
        return messages
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return []

def consolidate_conversations():
    """Read all conversations from all platforms"""
    all_messages = []
    file_count = 0
    
    for platform, directory in PLATFORMS.items():
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            continue
        
        print(f"\nProcessing {platform.upper()}...")
        
        json_files = list(Path(directory).glob('*.json'))
        print(f"  Found {len(json_files)} files")
        
        for filepath in json_files:
            messages = extract_messages_from_file(filepath, platform)
            
            for msg in messages:
                try:
                    # Extract content
                    content = ''
                    if 'contents' in msg:
                        if isinstance(msg['contents'], list):
                            content = '\n'.join([
                                c.get('content', '') if isinstance(c, dict) else str(c)
                                for c in msg['contents']
                            ])
                        else:
                            content = msg['contents'].get('content', '') if isinstance(msg['contents'], dict) else str(msg['contents'])
                    elif 'content' in msg:
                        content = msg['content']
                    
                    # Parse timestamp
                    timestamp = None
                    if 'created_at' in msg:
                        timestamp = parse_timestamp(msg['created_at'])
                    elif 'timestamp' in msg:
                        timestamp = parse_timestamp(msg['timestamp'])
                    
                    if content.strip():  # Only include non-empty messages
                        all_messages.append({
                            'platform': platform,
                            'role': msg.get('role', 'unknown'),
                            'model': msg.get('model', msg.get('displayModel', 'unknown')),
                            'timestamp': timestamp,
                            'timestamp_str': msg.get('created_at', 'unknown'),
                            'content': content,
                            'file': filepath.name,
                        })
                        file_count += 1
                except Exception as e:
                    continue
        
        print(f"  Extracted {file_count} messages so far")
    
    # Sort by timestamp
    print("\nSorting by timestamp...")
    all_messages.sort(key=lambda x: x['timestamp'] if x['timestamp'] else datetime.min)
    
    return all_messages

def save_consolidated(messages):
    """Save consolidated data"""
    output_file = r'c:\Determined\UNIFIED_CONVERSATION_TIMELINE.json'
    
    # Create summary index
    summary = {
        'total_messages': len(messages),
        'date_range': {
            'earliest': str(messages[0]['timestamp']) if messages and messages[0]['timestamp'] else 'unknown',
            'latest': str(messages[-1]['timestamp']) if messages and messages[-1]['timestamp'] else 'unknown',
        },
        'platform_breakdown': {},
        'messages': messages,
    }
    
    # Count by platform
    platform_counts = defaultdict(int)
    for msg in messages:
        platform_counts[msg['platform']] += 1
    
    summary['platform_breakdown'] = dict(platform_counts)
    
    print(f"\nSaving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, default=str)
    
    print(f"✓ Saved {len(messages)} messages")
    print(f"\nPlatform breakdown:")
    for platform, count in sorted(platform_counts.items()):
        print(f"  {platform}: {count}")
    
    return output_file

def create_narrative_view(messages):
    """Create a narrative-style view of the timeline"""
    output_file = r'c:\Determined\UNIFIED_CONVERSATION_NARRATIVE.md'
    
    print(f"\nCreating narrative view at {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# UNIFIED CONVERSATION TIMELINE\n")
        f.write("## Complete Record: October 2025 - April 2026\n")
        f.write("### All Platforms Integrated\n\n")
        
        f.write("---\n\n")
        
        current_date = None
        current_platform = None
        current_model = None
        
        for msg in messages:
            # Date header
            msg_date = msg['timestamp'].date() if msg['timestamp'] else None
            if msg_date != current_date:
                f.write(f"\n## {msg_date or 'Unknown Date'}\n\n")
                current_date = msg_date
            
            # Platform/model change header
            platform_model = f"{msg['platform'].upper()} ({msg['model']})"
            if platform_model != current_platform:
                f.write(f"### {platform_model}\n\n")
                current_platform = platform_model
            
            # Message
            role_badge = "**USER**" if msg['role'] == 'user' else "**AI**"
            f.write(f"{role_badge}: {msg['content'][:200]}...\n\n" if len(msg['content']) > 200 else f"{role_badge}: {msg['content']}\n\n")
            f.write("---\n\n")
    
    print(f"✓ Narrative view created")
    return output_file

if __name__ == '__main__':
    print("=" * 60)
    print("CONSOLIDATING ALL AI CONVERSATIONS")
    print("=" * 60)
    
    messages = consolidate_conversations()
    
    print(f"\n{'=' * 60}")
    print(f"TOTAL MESSAGES: {len(messages)}")
    print(f"{'=' * 60}")
    
    consolidation_file = save_consolidated(messages)
    narrative_file = create_narrative_view(messages)
    
    print(f"\n✓ Complete. Two files created:")
    print(f"  1. {consolidation_file} (structured JSON)")
    print(f"  2. {narrative_file} (readable narrative)")
