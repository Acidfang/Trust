#!/usr/bin/env python3
"""
Final proper extraction from ChatGPT consolidated dump
"""

import json
from datetime import datetime

def extract_content_safely(content_obj):
    """Safely extract text content from ChatGPT message structure"""
    try:
        if isinstance(content_obj, dict):
            parts = content_obj.get('parts', [])
            if isinstance(parts, list):
                # Join all parts as text
                text_parts = []
                for part in parts:
                    if isinstance(part, str):
                        text_parts.append(part)
                    elif isinstance(part, dict):
                        # Might have nested structure
                        if '__text_pydantic' in part:
                            text_parts.append(part['__text_pydantic'])
                        elif 'text' in part:
                            text_parts.append(part['text'])
                        else:
                            text_parts.append(str(part))
                    else:
                        text_parts.append(str(part))
                return '\n'.join(text_parts)
        return ''
    except:
        return ''

def extract_properly(filepath):
    """Extract with all edge cases handled"""
    messages = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        conversations = json.load(f)
    
    total_msg_count = 0
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
        conv_msg_count = 0
        
        for node in mapping.values():
            if not node.get('message'):
                continue
            
            msg = node['message']
            
            # Role from author
            author = msg.get('author', {})
            if isinstance(author, dict):
                role = author.get('role', 'unknown')
            else:
                role = 'unknown'
            
            # Content extraction
            content_obj = msg.get('content', {})
            content = extract_content_safely(content_obj)
            
            if content and len(content.strip()) > 0:
                messages.append({
                    'platform': 'chatgpt',
                    'role': role,
                    'model': 'gpt',
                    'timestamp': timestamp,
                    'timestamp_str': timestamp_str,
                    'content': content,
                    'conversation_title': title,
                })
                conv_msg_count += 1
        
        total_msg_count += conv_msg_count
    
    return messages

filepath = r'D:\Downloads\AI Chat\ChatGPT\conversations.json'
print("Extracting ChatGPT consolidated dump...")
messages = extract_properly(filepath)

print(f"✓ Extracted {len(messages)} messages\n")

# Show breakdown by conversation
from collections import Counter
conv_titles = [m['conversation_title'] for m in messages]
conv_counts = Counter(conv_titles)

print("Messages per conversation (top 15):")
for title, count in conv_counts.most_common(15):
    print(f"  {count:4d} - {title[:60]}")

print(f"\nTotal: {len(messages)} messages")
print(f"Total conversations: {len(conv_counts)}")
