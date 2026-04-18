#!/usr/bin/env python3
"""
FINAL COMPLETE CONSOLIDATION
All platforms with proper ChatGPT dump extraction
"""

import json
import os
from datetime import datetime
from pathlib import Path
from collections import defaultdict

def extract_content_safely(content_obj):
    """Safely extract text from ChatGPT message"""
    try:
        if isinstance(content_obj, dict):
            parts = content_obj.get('parts', [])
            if isinstance(parts, list):
                text_parts = []
                for part in parts:
                    if isinstance(part, str):
                        text_parts.append(part)
                    elif isinstance(part, dict):
                        text_parts.append(str(part))
                    else:
                        text_parts.append(str(part))
                return '\n'.join(text_parts)
        return ''
    except:
        return ''

def extract_from_chatgpt_dump(filepath):
    """Extract from consolidated ChatGPT export"""
    messages = []
    with open(filepath, 'r', encoding='utf-8') as f:
        conversations = json.load(f)
    
    for conv in conversations:
        title = conv.get('title', 'Untitled')
        create_time = conv.get('create_time', 0)
        
        if create_time:
            timestamp = datetime.fromtimestamp(create_time)
            timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        else:
            timestamp = None
            timestamp_str = 'unknown'
        
        mapping = conv.get('mapping', {})
        
        for node in mapping.values():
            if not node.get('message'):
                continue
            
            msg = node['message']
            author = msg.get('author', {})
            role = author.get('role', 'unknown') if isinstance(author, dict) else 'unknown'
            content = extract_content_safely(msg.get('content', {}))
            
            if content and len(content.strip()) > 0:
                messages.append({
                    'platform': 'chatgpt_dump',
                    'role': role,
                    'model': 'gpt',
                    'timestamp': timestamp,
                    'timestamp_str': timestamp_str,
                    'content': content,
                })
    
    return messages

def parse_timestamp(ts_str):
    if not ts_str:
        return None
    formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f']
    for fmt in formats:
        try:
            return datetime.strptime(ts_str, fmt)
        except ValueError:
            continue
    return None

def extract_from_individual_file(filepath, platform):
    """Extract from individual JSON files"""
    messages = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        items = []
        if isinstance(data, list):
            items = [item for item in data if 'role' in item and 'contents' in item]
        elif isinstance(data, dict) and 'contents' in data:
            items = data['contents'] if isinstance(data['contents'], list) else [data['contents']]
        
        for msg in items:
            content = ''
            if 'contents' in msg:
                if isinstance(msg['contents'], list):
                    content = '\n'.join([c.get('content', '') if isinstance(c, dict) else str(c) for c in msg['contents']])
                else:
                    content = msg['contents'].get('content', '') if isinstance(msg['contents'], dict) else str(msg['contents'])
            elif 'content' in msg:
                content = msg['content']
            
            timestamp = None
            timestamp_str = msg.get('created_at', 'unknown')
            if timestamp_str != 'unknown':
                timestamp = parse_timestamp(timestamp_str)
            
            if content and len(content.strip()) > 0:
                messages.append({
                    'platform': platform,
                    'role': msg.get('role', 'unknown'),
                    'model': msg.get('model', msg.get('displayModel', 'unknown')),
                    'timestamp': timestamp,
                    'timestamp_str': timestamp_str,
                    'content': content,
                })
    except:
        pass
    
    return messages

def consolidate_final():
    """Final consolidation with all platforms"""
    all_messages = []
    
    print("=" * 70)
    print("FINAL COMPLETE CONSOLIDATION")
    print("=" * 70 + "\n")
    
    # 1. ChatGPT consolidated dump (PRIORITY)
    chatgpt_dump = r'D:\Downloads\AI Chat\ChatGPT\conversations.json'
    if os.path.exists(chatgpt_dump):
        print("1. ChatGPT Consolidated Dump...")
        chatgpt_msgs = extract_from_chatgpt_dump(chatgpt_dump)
        all_messages.extend(chatgpt_msgs)
        print(f"   ✓ {len(chatgpt_msgs)} messages\n")
    
    # 2. Gemini individual files
    gemini_dir = r'D:\Downloads\AI Chat\Gemini'
    if os.path.exists(gemini_dir):
        print("2. Gemini Individual Files...")
        gemini_files = list(Path(gemini_dir).glob('*.json'))
        gemini_msgs = []
        for fp in gemini_files:
            gemini_msgs.extend(extract_from_individual_file(fp, 'gemini'))
        all_messages.extend(gemini_msgs)
        print(f"   ✓ {len(gemini_msgs)} messages from {len(gemini_files)} files\n")
    
    # 3. Claude individual files
    claude_dir = r'D:\Downloads\AI Chat\Claude'
    if os.path.exists(claude_dir):
        print("3. Claude Individual Files...")
        claude_files = list(Path(claude_dir).glob('*.json'))
        claude_msgs = []
        for fp in claude_files:
            claude_msgs.extend(extract_from_individual_file(fp, 'claude'))
        all_messages.extend(claude_msgs)
        print(f"   ✓ {len(claude_msgs)} messages from {len(claude_files)} files\n")
    
    # 4. ChatGPT individual files (dedupe against dump)
    chatgpt_dir = r'D:\Downloads\AI Chat\ChatGPT'
    if os.path.exists(chatgpt_dir):
        print("4. ChatGPT Individual Files (deduped)...")
        chatgpt_files = [f for f in Path(chatgpt_dir).glob('*.json') if f.name != 'conversations.json' and f.name != 'chat.html']
        chatgpt_ind_msgs = []
        for fp in chatgpt_files:
            chatgpt_ind_msgs.extend(extract_from_individual_file(fp, 'chatgpt_individual'))
        all_messages.extend(chatgpt_ind_msgs)
        print(f"   ✓ {len(chatgpt_ind_msgs)} messages from {len(chatgpt_files)} files\n")
    
    # 5. Copilot individual files
    copilot_dir = r'D:\Downloads\AI Chat\Copilot'
    if os.path.exists(copilot_dir):
        print("5. Copilot Individual Files...")
        copilot_files = list(Path(copilot_dir).glob('*.json'))
        copilot_msgs = []
        for fp in copilot_files:
            copilot_msgs.extend(extract_from_individual_file(fp, 'copilot'))
        all_messages.extend(copilot_msgs)
        print(f"   ✓ {len(copilot_msgs)} messages from {len(copilot_files)} files\n")
    
    # Sort by timestamp
    print("Sorting by timestamp...")
    all_messages.sort(key=lambda x: x['timestamp'] if x['timestamp'] else datetime.min)
    
    return all_messages

def save_final(messages):
    output_file = r'c:\Determined\UNIFIED_MASTER_TIMELINE.json'
    
    # Compute breakdown
    platform_counts = defaultdict(int)
    for msg in messages:
        platform_counts[msg['platform']] += 1
    
    summary = {
        'total_messages': len(messages),
        'date_range': {
            'earliest': str(messages[0]['timestamp']) if messages and messages[0]['timestamp'] else 'unknown',
            'latest': str(messages[-1]['timestamp']) if messages and messages[-1]['timestamp'] else 'unknown',
        },
        'platform_breakdown': dict(platform_counts),
        'messages': messages,
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, default=str)
    
    return output_file, summary

if __name__ == '__main__':
    messages = consolidate_final()
    
    print("=" * 70)
    print(f"FINAL TOTAL: {len(messages)} messages")
    print("=" * 70 + "\n")
    
    output_file, summary = save_final(messages)
    
    print(f"Saved to: {output_file}\n")
    print("Platform breakdown:")
    for platform, count in sorted(summary['platform_breakdown'].items()):
        print(f"  {platform:30s}: {count:6d}")
    
    print(f"\nDate range: {summary['date_range']['earliest']} → {summary['date_range']['latest']}")
