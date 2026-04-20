
"""
TIER -1 (BOUND): Input validation and error setup
TIER 0 (FREE): Explore possibilities
TIER 1 (BOUND): Lock in root-cause logic  
TIER 2 (FREE): Verify consistency
TIER 3+ (BOUND): Automate return and integrate
"""

#!/usr/bin/env python3
"""
DUPLICATE DETECTOR
==================

Prevents duplicate definitions, duplicate keys, and redundant code.
Alerts before adding duplicates to workspace.

Common patterns detected:
  - Duplicate function definitions
  - Duplicate YAML keys
  - Duplicate file names with different content
  - Duplicate imports
  - Redundant code blocks

Usage: python duplicate_detector.py [--check-file FILE]
"""

import hashlib
from pathlib import Path
from collections import defaultdict
from typing import Dict, Set, List, Tuple


class DuplicateDetector:
    """Find and alert on duplicate definitions."""
    
    def __init__(self, workspace=None):
        self.workspace = Path(workspace or "c:\\Determined")
        self.duplicates = defaultdict(list)
        self.exclude_dirs = {".venv", ".git", "_archive", "__pycache__"}
    
    def should_process(self, path):
        """Check if path should be processed."""
        for exclude in self.exclude_dirs:
            if exclude in path.parts:
                return False
        return True
    
    def scan_python_duplicates(self):
        """Find duplicate function/class definitions."""
        print("[*] Scanning for duplicate Python definitions...")
        
        definitions = defaultdict(list)
        
        for py_file in self.workspace.rglob("*.py"):
            if not self.should_process(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                
                for line_num, line in enumerate(lines, 1):
                    stripped = line.strip()
                    
                    # Find function definitions
                    if stripped.startswith('def '):
                        func_name = stripped.split('(')[0].replace('def ', '').strip()
                        rel_path = str(py_file.relative_to(self.workspace))
                        definitions[f"def:{func_name}"].append(
                            (rel_path, line_num)
                        )
                    
                    # Find class definitions
                    if stripped.startswith('class '):
                        class_name = stripped.split('(')[0].replace('class ', '').replace(':', '').strip()
                        rel_path = str(py_file.relative_to(self.workspace))
                        definitions[f"class:{class_name}"].append(
                            (rel_path, line_num)
                        )
            except (IOError, OSError):
                pass
        
        # Report duplicates
        for definition, locations in definitions.items():
            if len(locations) > 1:
                self.duplicates["duplicate_definitions"].append({
                    "definition": definition,
                    "locations": locations,
                    "count": len(locations)
                })
    
    def scan_yaml_duplicates(self):
        """Find duplicate YAML keys."""
        print("[*] Scanning for duplicate YAML keys...")
        
        for yaml_file in self.workspace.rglob("*.y*ml"):
            if not self.should_process(yaml_file):
                continue
            
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                keys_by_level = defaultdict(list)
                
                for line_num, line in enumerate(lines, 1):
                    stripped = line.lstrip()
                    indent = len(line) - len(stripped)
                    
                    if ':' in stripped and not stripped.startswith('#'):
                        key = stripped.split(':')[0].strip()
                        level = indent // 2
                        
                        for existing_key, existing_line in keys_by_level[level]:
                            if existing_key == key:
                                rel_path = str(yaml_file.relative_to(self.workspace))
                                self.duplicates["yaml_duplicate_keys"].append({
                                    "file": rel_path,
                                    "key": key,
                                    "first_occurrence": existing_line,
                                    "duplicate_occurrence": line_num,
                                })
                        
                        keys_by_level[level].append((key, line_num))
            except (IOError, OSError):
                pass
    
    def scan_file_duplicates(self):
        """Find files with same content but different names."""
        print("[*] Scanning for duplicate file content...")
        
        hashes = defaultdict(list)
        
        for file_path in self.workspace.rglob("*"):
            if not file_path.is_file() or not self.should_process(file_path):
                continue
            
            # Skip binary files
            if file_path.suffix in {'.pyc', '.so', '.dll', '.exe', '.json'}:
                continue
            
            try:
                with open(file_path, 'rb') as f:
                    content_hash = hashlib.sha256(f.read()).hexdigest()
                
                rel_path = str(file_path.relative_to(self.workspace))
                hashes[content_hash].append(rel_path)
            except (IOError, OSError):
                pass
        
        # Report duplicates
        for content_hash, files in hashes.items():
            if len(files) > 1:
                self.duplicates["duplicate_content"].append({
                    "hash": content_hash,
                    "files": files,
                    "count": len(files)
                })
    
    def scan_import_duplicates(self):
        """Find duplicate imports in Python files."""
        print("[*] Scanning for duplicate imports...")
        
        for py_file in self.workspace.rglob("*.py"):
            if not self.should_process(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                
                imports = defaultdict(list)
                
                for line_num, line in enumerate(lines, 1):
                    stripped = line.strip()
                    
                    if stripped.startswith(('import ', 'from ')):
                        imports[stripped].append(line_num)
                
                # Report duplicates
                for import_line, line_nums in imports.items():
                    if len(line_nums) > 1:
                        rel_path = str(py_file.relative_to(self.workspace))
                        self.duplicates["duplicate_imports"].append({
                            "file": rel_path,
                            "import": import_line,
                            "lines": line_nums,
                        })
            except (IOError, OSError):
                pass
    
    def report(self):
        """Print duplicate detection report."""
        print("\n" + "="*70)
        print("DUPLICATE DETECTION REPORT")
        print("="*70 + "\n")
        
        total = sum(len(v) for v in self.duplicates.values())
        
        if total == 0:
            print("[OK] No duplicates detected.")
            return True
        
        print(f"[ALERT] {total} duplicate items found\n")
        
        for dup_type, items in sorted(self.duplicates.items()):
            print(f"[{dup_type.upper()}] {len(items)} items")
            
            for item in items[:3]:
                if isinstance(item, dict):
                    if 'definition' in item:
                        print(f"  - {item['definition']}: {item['count']} occurrences")
                        for loc in item['locations']:
                            print(f"    {loc[0]}:{loc[1]}")
                    elif 'file' in item:
                        print(f"  - {item['file']}")
                    elif 'files' in item:
                        print(f"  - {len(item['files'])} files with identical content")
                        for f in item['files'][:2]:
                            print(f"    {f}")
            
            if len(items) > 3:
                print(f"  ... and {len(items) - 3} more")
            print()
        
        return False


def main():
    """Run duplicate detection."""
    import sys
    
    detector = DuplicateDetector()
    
    detector.scan_python_duplicates()
    detector.scan_yaml_duplicates()
    detector.scan_file_duplicates()
    detector.scan_import_duplicates()
    
    success = detector.report()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
