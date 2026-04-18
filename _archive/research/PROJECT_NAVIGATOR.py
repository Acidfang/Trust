#!/usr/bin/env python3
"""
PROJECT NAVIGATOR - Quick index and search of the entire project.

Creates a searchable index so you can find files by pattern or keyword.
"""

import os
from pathlib import Path
import json

SKIP_DIRS = {
    '.git', '__pycache__', '.venv', 'venv', 'node_modules', 
    '.pytest_cache', 'dist', 'build', 'wiki_assets'
}

def build_project_index():
    """Build searchable index of entire project."""
    root = Path(r'c:\Determined')
    index = {
        'timestamp': __import__('datetime').datetime.now().isoformat(),
        'root': str(root),
        'files': [],
        'directories': [],
        'extension_count': {},
        'python_modules': [],
        'markdown_docs': [],
        'configuration': []
    }
    
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        
        rel_dir = Path(dirpath).relative_to(root)
        if str(rel_dir) != '.':
            index['directories'].append({
                'path': str(rel_dir),
                'name': Path(dirpath).name
            })
        
        for filename in sorted(filenames):
            filepath = Path(dirpath) / filename
            rel_path = filepath.relative_to(root)
            
            ext = filepath.suffix or 'no_ext'
            index['extension_count'][ext] = index['extension_count'].get(ext, 0) + 1
            
            file_info = {
                'path': str(rel_path),
                'name': filename,
                'extension': ext,
                'size': filepath.stat().st_size
            }
            
            index['files'].append(file_info)
            
            # Categorize
            if ext == '.py':
                index['python_modules'].append(str(rel_path))
            elif ext == '.md':
                index['markdown_docs'].append(str(rel_path))
            elif ext in {'.json', '.yaml', '.yml', '.toml', '.ini', '.cfg'}:
                index['configuration'].append(str(rel_path))
    
    return index

def save_index(index, output_path=r'c:\Determined\PROJECT_INDEX.json'):
    """Save index to JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    return output_path

def print_index_summary(index):
    """Print summary of index."""
    print("=" * 80)
    print("PROJECT INDEX SUMMARY")
    print("=" * 80)
    print(f"Timestamp: {index['timestamp']}")
    print(f"Root: {index['root']}")
    print()
    print(f"Total Files: {len(index['files'])}")
    print(f"Total Directories: {len(index['directories'])}")
    print()
    print("Files by Extension:")
    for ext in sorted(index['extension_count'].keys()):
        count = index['extension_count'][ext]
        print(f"  {ext:15} : {count:4} files")
    print()
    print("Key File Categories:")
    print(f"  Python Modules  : {len(index['python_modules'])} files")
    print(f"  Markdown Docs   : {len(index['markdown_docs'])} files")
    print(f"  Configuration   : {len(index['configuration'])} files")
    print()
    print("Top-Level Python Files:")
    for fpath in sorted(index['python_modules'])[:10]:
        if '\\' not in fpath.lstrip('\\'):
            print(f"  - {fpath}")
    print()
    print("Top-Level Markdown Files:")
    for fpath in sorted(index['markdown_docs'])[:10]:
        if '\\' not in fpath.lstrip('\\'):
            print(f"  - {fpath}")
    print()
    print("=" * 80)

def main():
    """Main entry point."""
    print("Building project index...")
    index = build_project_index()
    
    output = save_index(index)
    print(f"✓ Index saved to: {output}")
    
    print_index_summary(index)
    
    return index

if __name__ == '__main__':
    main()
