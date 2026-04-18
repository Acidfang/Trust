#!/usr/bin/env python3
"""
Re-consolidate with complete ChatGPT dump included
"""

import json
import os
from datetime import datetime
from pathlib import Path
from collections import defaultdict

PLATFORMS = {
    'gemini': r'D:\Downloads\AI Chat\Gemini',
    'claude': r'D:\Downloads\AI Chat\Claude',
    'chatgpt': r'D:\Downloads\AI Chat\ChatGPT',
    'copilot': r'D:\Downloads\AI Chat\Copilot',
}

def parse_timestamp(ts_str):
    if not ts_str:
        return None
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

def extract_from_chatgpt_dump(filepath):
    """Extract messages from the consolidated ChatGPT dump"""
    messages = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            conversations = json.load(f)
        
        for conv in conversations:
            title = conv.get('title', 'Untitled')
            conv_id = conv.get('id', '')
            create_time = conv.get('create_time', 0)
            
            # Parse timestamp from create_time (Unix timestamp)
            if create_time:
                timestamp = datetime.fromtimestamp(create_time)
                timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            else:
                timestamp = None
                timestamp_str = 'unknown'
            
            # Extract messages from mapping
            mapping = conv.get('mapping', {})
            for node_id, node in mapping.items():
                if node.get('message'):
                    msg = node['message']
                    role = msg.get('role', 'unknown')
                    
                    # Extract content
                    content = ''
                    if 'content' in msg:
                        content_data = msg['content']
                        if isinstance(content_data, list):
                            content = '\n'.join([
                                part.get('text', '') if isinstance(part, dict) else str(part)
                                for part in content_data
                            ])
                        elif isinstance(content_data, dict):
                            content = content_data.get('text', '')
                        else:
                            content = str(content_data)
                    
                    if content.strip():
                        messages.append({
                            'platform': 'chatgpt',
                            'role': role,
                            'model': 'gpt',
                            'timestamp': timestamp,
                            'timestamp_str': timestamp_str,
                            'content': content,
                            'file': f"{title} (consolidated dump)",
                            'conversation_title': title,
                        })
    
    except Exception as e:
        print(f"Error reading ChatGPT dump: {e}")
    
    return messages

def extract_messages_from_file(filepath, platform):
    """Extract messages from individual JSON files"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        messages = []
        
        if isinstance(data, list):
            for item in data:
                if 'role' in item and 'contents' in item:
                    messages.append(item)
        elif isinstance(data, dict):
            if 'contents' in data:
                messages = data['contents'] if isinstance(data['contents'], list) else [data['contents']]
            elif 'messages' in data:
                messages = data['messages'] if isinstance(data['messages'], list) else [data['messages']]
            else:
                messages = [data]
        
        return messages
    except:
        return []

def consolidate_conversations():
    """Read all conversations including the complete ChatGPT dump"""
    all_messages = []
    
    # First: Extract from ChatGPT consolidated dump (PRIORITY)
    chatgpt_dump = r'D:\Downloads\AI Chat\ChatGPT\conversations.json'
    if os.path.exists(chatgpt_dump):
        print("Reading ChatGPT consolidated dump...")
        chatgpt_messages = extract_from_chatgpt_dump(chatgpt_dump)
        all_messages.extend(chatgpt_messages)
        print(f"  Extracted {len(chatgpt_messages)} messages from dump")
    
    # Second: Individual files (other platforms + remaining ChatGPT files)
    for platform, directory in PLATFORMS.items():
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            continue
        
        print(f"\nProcessing individual {platform.upper()} files...")
        
        json_files = list(Path(directory).glob('*.json'))
        # Exclude the consolidated dump from re-processing
        json_files = [f for f in json_files if f.name != 'conversations.json']
        
        print(f"  Found {len(json_files)} individual files")
        
        extracted_count = 0
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
                    
                    if content.strip():
                        all_messages.append({
                            'platform': platform,
                            'role': msg.get('role', 'unknown'),
                            'model': msg.get('model', msg.get('displayModel', 'unknown')),
                            'timestamp': timestamp,
                            'timestamp_str': msg.get('created_at', 'unknown'),
                            'content': content,
                            'file': filepath.name,
                        })
                        extracted_count += 1
                except:
                    continue
        
        print(f"  Extracted {extracted_count} messages from individual files")
    
    # Sort by timestamp
    print("\nSorting by timestamp...")
    all_messages.sort(key=lambda x: x['timestamp'] if x['timestamp'] else datetime.min)
    
    return all_messages

def save_consolidated(messages):
    """Save consolidated data"""
    output_file = r'c:\Determined\UNIFIED_CONVERSATION_TIMELINE_COMPLETE.json'
    
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

if __name__ == '__main__':
    print("=" * 70)
    print("RE-CONSOLIDATING WITH COMPLETE CHATGPT DUMP")
    print("=" * 70)
    
    messages = consolidate_conversations()
    
    print(f"\n{'=' * 70}")
    print(f"TOTAL MESSAGES: {len(messages)} (updated from 48,285)")
    print(f"{'=' * 70}")
    
    consolidation_file = save_consolidated(messages)
