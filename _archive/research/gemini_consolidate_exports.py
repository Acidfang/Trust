"""
GEMINI CONVERSATION CONSOLIDATOR
Parses all manually exported Gemini conversation markdown files
Creates a unified, searchable database
"""

import json
import re
from pathlib import Path
from datetime import datetime


def parse_gemini_export(md_file_path):
    """
    Parse a single exported Gemini markdown file
    Extract: conversation ID, topic, URL, content
    """
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR reading {md_file_path}: {e}")
        return None
    
    # Extract source URL
    url_match = re.search(r'> From: (https://gemini\.google\.com/app/[^\s]+)', content)
    url = url_match.group(1) if url_match else None
    
    # Extract conversation ID from URL
    conv_id = None
    if url:
        conv_id_match = re.search(r'/app/([a-f0-9]+)', url)
        conv_id = conv_id_match.group(1) if conv_id_match else None
    
    # Extract topic (first heading or filename)
    heading_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    topic = heading_match.group(1) if heading_match else Path(md_file_path).stem
    
    # Remove URL and heading from content
    text_content = re.sub(r'> From: .+\n', '', content)
    text_content = re.sub(r'^# .+\n', '', text_content, flags=re.MULTILINE)
    
    return {
        "conversation_id": conv_id,
        "topic": topic,
        "source_url": url,
        "file_path": str(md_file_path),
        "file_name": Path(md_file_path).name,
        "content": text_content.strip(),
        "content_length": len(text_content),
        "parsed_at": datetime.now().isoformat(),
    }


def consolidate_exports(base_dir="D:\\Downloads"):
    """
    Find all exported Gemini markdown files in Downloads
    Parse them and create unified database
    """
    
    print("="*70)
    print("GEMINI CONVERSATION CONSOLIDATOR")
    print("="*70)
    print()
    
    base_path = Path(base_dir)
    
    # Find all markdown files that look like Gemini exports
    # (starting with _ or containing "chat", "conversation", etc)
    md_files = []
    
    # Look for markdown files
    for md_file in base_path.glob("*.md"):
        # Filter: likely exports have _ prefix or specific patterns
        if md_file.name.startswith("_") or any(x in md_file.name.lower() for x in 
                                                   ["chat", "conversation", "gemini", "export"]):
            md_files.append(md_file)
    
    # Also check in subdirectories
    for md_file in base_path.glob("**/*.md"):
        if md_file not in md_files and (md_file.name.startswith("_") or 
                                       any(x in md_file.name.lower() for x in 
                                           ["chat", "conversation", "gemini", "brief"])):
            md_files.append(md_file)
    
    print(f"[1] Found {len(md_files)} markdown files to parse")
    print()
    
    # Parse all files
    conversations = []
    errors = []
    
    for i, md_file in enumerate(sorted(md_files), 1):
        print(f"    [{i}/{len(md_files)}] Parsing: {md_file.name[:60]}...")
        
        parsed = parse_gemini_export(md_file)
        if parsed:
            conversations.append(parsed)
        else:
            errors.append(str(md_file))
    
    print()
    print(f"[2] Successfully parsed {len(conversations)} conversations")
    
    if errors:
        print(f"    Errors parsing {len(errors)} files:")
        for err in errors[:5]:
            print(f"      - {err}")
    
    print()
    print(f"[3] Creating unified database...")
    
    # Create consolidated database
    database = {
        "created_at": datetime.now().isoformat(),
        "total_conversations": len(conversations),
        "base_directory": str(base_path),
        "conversations": sorted(conversations, key=lambda x: x['topic']),
        "stats": {
            "total_files_parsed": len(conversations),
            "total_content_size_bytes": sum(c['content_length'] for c in conversations),
            "avg_content_length": int(sum(c['content_length'] for c in conversations) / max(1, len(conversations))),
            "topics": sorted(list(set(c['topic'] for c in conversations))),
            "unique_conversation_ids": len(set(c['conversation_id'] for c in conversations if c['conversation_id'])),
        }
    }
    
    # Save unified database
    output_file = Path(base_path) / "gemini_consolidated_database.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print(f"    ✓ Saved to: {output_file}")
    print()
    
    # Print stats
    print(f"[4] Database Statistics:")
    print(f"    Total conversations: {database['total_conversations']}")
    print(f"    Total content: {database['stats']['total_content_size_bytes']:,} bytes")
    print(f"    Average conversation: {database['stats']['avg_content_length']:,} bytes")
    print(f"    Unique IDs: {database['stats']['unique_conversation_ids']}")
    print()
    
    # Print topics
    print(f"[5] Topics found ({len(database['stats']['topics'])}):")
    for topic in sorted(database['stats']['topics'])[:15]:
        print(f"    - {topic[:70]}")
    
    if len(database['stats']['topics']) > 15:
        print(f"    ... and {len(database['stats']['topics']) - 15} more")
    
    print()
    print("="*70)
    print("CONSOLIDATION COMPLETE")
    print("="*70)
    
    return database


if __name__ == "__main__":
    consolidate_exports()
