#!/usr/bin/env python3
"""
Properly extract from ChatGPT consolidated dump
"""

import json
import os
from datetime import datetime
from pathlib import Path
from collections import defaultdict

def extract_from_chatgpt_dump_properly(filepath):
    """Extract messages correctly from consolidated ChatGPT export"""
    messages = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            conversations = json.load(f)
        
        print(f"Processing {len(conversations)} conversations...")
        
        for conv_idx, conv in enumerate(conversations):
            title = conv.get('title', 'Untitled')
            create_time = conv.get('create_time', 0)
            
            # Parse timestamp
            if create_time:
                timestamp = datetime.fromtimestamp(create_time)
                timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            else:
                timestamp = None
                timestamp_str = 'unknown'
            
            # Extract messages from mapping
            mapping = conv.get('mapping', {})
            conv_msg_count = 0
            
            for node_id, node in mapping.items():
                if not node.get('message'):
                    continue
                
                msg = node['message']
                
                # Get author/role
                author = msg.get('author', {})
                if isinstance(author, dict):
                    role = author.get('role', 'unknown')
                else:
                    role = 'unknown'
                
                # Get content
                content = ''
                content_obj = msg.get('content', {})
                if isinstance(content_obj, dict):
                    parts = content_obj.get('parts', [])
                    if isinstance(parts, list) and len(parts) > 0:
                        content = parts[0]
                    else:
                        content = str(parts)
                else:
                    content = str(content_obj)
                
                if content and content.strip():
                    messages.append({
                        'platform': 'chatgpt',
                        'role': role,
                        'model': 'gpt',
                        'timestamp': timestamp,
                        'timestamp_str': timestamp_str,
                        'content': content,
                        'file': f"{title} (consolidated)",
                        'conversation_title': title,
                    })
                    conv_msg_count += 1
            
            if conv_idx % 10 == 0:
                print(f"  Conversation {conv_idx}: {title} ({conv_msg_count} msgs)")
    
    except Exception as e:
        print(f"Error reading ChatGPT dump: {e}")
        import traceback
        traceback.print_exc()
    
    return messages

def consolidate_all_with_proper_chatgpt():
    """Complete consolidation with proper ChatGPT extraction"""
    all_messages = []
    
    # ChatGPT consolidated dump
    chatgpt_dump = r'D:\Downloads\AI Chat\ChatGPT\conversations.json'
    if os.path.exists(chatgpt_dump):
        print("=" * 70)
        print("EXTRACTING CHATGPT CONSOLIDATED DUMP")
        print("=" * 70)
        chatgpt_messages = extract_from_chatgpt_dump_properly(chatgpt_dump)
        all_messages.extend(chatgpt_messages)
        print(f"\n✓ Extracted {len(chatgpt_messages)} messages from ChatGPT dump\n")
    
    # Gemini individual files
    gemini_dir = r'D:\Downloads\AI Chat\Gemini'
    if os.path.exists(gemini_dir):
        print("EXTRACTING GEMINI INDIVIDUAL FILES")
        print("=" * 70)
        for filepath in list(Path(gemini_dir).glob('*.json'))[:5]:
            print(f"Sampling from {filepath.name}...")
        gemini_files = list(Path(gemini_dir).glob('*.json'))
        # Just count them for now
        print(f"Total Gemini files: {len(gemini_files)}\n")
    
    # Sort by timestamp  
    print("Sorting by timestamp...")
    all_messages.sort(key=lambda x: x['timestamp'] if x['timestamp'] else datetime.min)
    
    return all_messages

if __name__ == '__main__':
    messages = consolidate_all_with_proper_chatgpt()
    
    print(f"\n{'=' * 70}")
    print(f"CHATGPT MESSAGES EXTRACTED: {len(messages)}")
    print(f"{'=' * 70}")
    
    # Show sample
    print("\nSample messages:")
    for msg in messages[:5]:
        role = msg['role']
        conv = msg.get('conversation_title', '?')
        content = msg['content'][:80]
        ts = msg['timestamp_str']
        print(f"[{ts}] {role:10s} | {conv[:40]:40s} | {content}...")
