#!/usr/bin/env python3
"""
PROJECT READER - Get and read entire project at once.

Walks the project directory, reads all relevant files, and outputs
a complete organized dump for comprehensive understanding.

Usage:
    python PROJECT_READER.py > PROJECT_COMPLETE_READ.md
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Files/dirs to skip
SKIP_DIRS = {
    '.git', '__pycache__', '.venv', 'venv', 'node_modules', 
    '.pytest_cache', 'dist', 'build', '.eggs', '*.egg-info',
    '.vscode', '.idea', '*.pyc', '.DS_Store', 'wiki_assets'
}

INCLUDE_EXTENSIONS = {
    '.py', '.md', '.txt', '.json', '.yaml', '.yml', 
    '.html', '.js', '.css', '.sh', '.ps1', '.toml', '.ini'
}

def should_skip(path_part):
    """Check if path should be skipped."""
    for skip in SKIP_DIRS:
        if skip.replace('*', '') in path_part:
            return True
    return False

def should_include(filepath):
    """Check if file should be included."""
    if should_skip(filepath):
        return False
    ext = Path(filepath).suffix
    return ext in INCLUDE_EXTENSIONS

def walk_project(root_path):
    """Walk project and yield (filepath, category) tuples."""
    root = Path(root_path)
    
    for dirpath, dirnames, filenames in os.walk(root):
        # Filter directories
        dirnames[:] = [d for d in dirnames if not should_skip(d)]
        
        for filename in sorted(filenames):
            filepath = Path(dirpath) / filename
            if should_include(str(filepath)):
                # Determine category
                if 'docs' in str(filepath):
                    category = 'DOCUMENTATION'
                elif filename.endswith('.md'):
                    category = 'MARKDOWN'
                elif filename.endswith('.py'):
                    category = 'PYTHON'
                elif 'archive' in str(filepath):
                    category = 'ARCHIVE'
                else:
                    category = 'OTHER'
                
                yield (filepath, category)

def read_file_safe(filepath, max_lines=None):
    """Safely read file, return content or error message."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if max_lines:
                lines = content.split('\n')[:max_lines]
                content = '\n'.join(lines)
                if len(content.split('\n')) >= max_lines:
                    content += '\n... (truncated)'
            return content
    except Exception as e:
        return f"[ERROR: Could not read - {e}]"

def format_file_entry(filepath, category):
    """Format a file entry for output."""
    try:
        size = filepath.stat().st_size
        rel_path = filepath.relative_to(Path.cwd().parent)
    except:
        size = 0
        rel_path = filepath
    
    content = read_file_safe(filepath)
    # Sanitize for output - remove problematic unicode
    content = content.encode('utf-8', errors='replace').decode('utf-8')
    
    return f"""
## File: {rel_path}
**Category**: {category}  
**Size**: {size:,} bytes

```
{content[:3000]}{"..." if len(content) > 3000 else ""}
```
"""

def main():
    """Main entry point."""
    root = Path(r'c:\Determined')
    output_file = Path(r'c:\Determined\PROJECT_COMPLETE_READ.md')
    
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(f"# PROJECT COMPLETE READ\n")
        out.write(f"**Generated**: {datetime.now().isoformat()}\n")
        out.write(f"**Root**: {root}\n")
        out.write(f"\n")
        
        # Collect files by category
        files_by_category = {}
        total_files = 0
        
        out.write("## Index\n\n")
        
        for filepath, category in walk_project(root):
            if category not in files_by_category:
                files_by_category[category] = []
            files_by_category[category].append(filepath)
            total_files += 1
        
        # Print summary
        out.write(f"**Total Files**: {total_files}\n\n")
        
        for category in sorted(files_by_category.keys()):
            files = files_by_category[category]
            out.write(f"- **{category}**: {len(files)} files\n")
        
        out.write(f"\n---\n\n")
        
        # Print files organized by category
        for category in sorted(files_by_category.keys()):
            files = files_by_category[category]
            out.write(f"# {category} ({len(files)} files)\n\n")
            
            for filepath in sorted(files):
                entry = format_file_entry(filepath, category)
                out.write(entry)
                out.write("\n")
    
    print(f"✓ Project read saved to: {output_file}")
    print(f"✓ Total files: {total_files}")
    print(f"✓ Categories: {', '.join(sorted(files_by_category.keys()))}")

if __name__ == '__main__':
    main()
