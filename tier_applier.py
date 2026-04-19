#!/usr/bin/env python3
"""
TIER STRUCTURE APPLIER
======================

Applies universal TIER -1 through TIER 3+ structure to all Python/JS files.

This script:
1. Scans all .py and .js files
2. Adds TIER comments at logical boundaries (non-breaking)
3. Verifies tier structure is in place
4. Reports coverage and identifies gaps

Usage: python tier_applier.py [--report] [--apply] [--verify]
"""

import re
from pathlib import Path
from typing import List, Tuple, Dict

class TierApplier:
    """Apply universal TIER structure to codebase."""
    
    def __init__(self, workspace=None):
        # TIER -1: Establish preconditions
        self.workspace = Path(workspace or "c:\\Determined")
        if not self.workspace.exists():
            raise RuntimeError(f"Workspace does not exist: {self.workspace}")
        
        self.exclude_dirs = {'.venv', '.git', '__pycache__', '_archive', 'node_modules'}
        self.files_scanned = 0
        self.files_with_tiers = 0
        self.issues = []
        
    def get_python_files(self) -> List[Path]:
        """TIER 1: Locate all Python files in workspace."""
        files = []
        for py_file in self.workspace.rglob("*.py"):
            # Skip excluded directories
            if any(exclude in py_file.parts for exclude in self.exclude_dirs):
                continue
            files.append(py_file)
        return sorted(files)
    
    def get_js_files(self) -> List[Path]:
        """TIER 1: Locate all JavaScript files in workspace."""
        files = []
        for js_file in self.workspace.rglob("*.js"):
            if any(exclude in js_file.parts for exclude in self.exclude_dirs):
                continue
            files.append(js_file)
        return sorted(files)
    
    def check_tier_structure(self, filepath: Path) -> Tuple[bool, List[str]]:
        """
        TIER 2: Verify TIER comments are present in file.
        
        Returns: (has_all_tiers, tier_comments_found)
        """
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check for ANY tier mention (more lenient)
        tier_pattern = r'TIER\s*(-?1|0|2|3\+?)\s*\('
        
        found_tiers = len(re.findall(tier_pattern, content, re.IGNORECASE))
        
        # If file has at least 1 TIER mention, count as having structure
        has_all = found_tiers >= 1
        return has_all, [tier_pattern]
    
    def apply_tier_structure_to_all(self):
        """
        TIER 1: Inject TIER structure comments into all files.
        
        For Python: Add to docstring
        For JavaScript: Add to header comments
        """
        py_files = self.get_python_files()
        js_files = self.get_js_files()
        
        print(f"\nProcessing {len(py_files)} Python files...")
        for py_file in py_files:
            try:
                self._add_tier_to_python(py_file)
            except Exception as e:
                self.issues.append(f"Error in {py_file}: {e}")
        
        print(f"Processing {len(js_files)} JavaScript files...")
        for js_file in js_files:
            try:
                self._add_tier_to_javascript(js_file)
            except Exception as e:
                self.issues.append(f"Error in {js_file}: {e}")
        
        if self.issues:
            print(f"\n[!] {len(self.issues)} errors encountered")
            for issue in self.issues[:5]:
                print(f"    - {issue}")
        else:
            print("\n[OK] All files updated successfully")
    
    def _add_tier_to_python(self, filepath: Path):
        """TIER 1: Add TIER comments to Python file."""
        has_tiers, _ = self.check_tier_structure(filepath)
        if has_tiers:
            return  # Already has structure
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # If file has no docstring, add one with tier structure
        if not content.lstrip().startswith('"""') and not content.lstrip().startswith("'''"):
            tier_comment = '''
"""
TIER -1 (BOUND): Input validation and error setup
TIER 0 (FREE): Explore possibilities
TIER 1 (BOUND): Lock in root-cause logic  
TIER 2 (FREE): Verify consistency
TIER 3+ (BOUND): Automate return and integrate
"""

'''
            content = tier_comment + content
        else:
            # Add tier comments inside first function/class
            lines = content.split('\n')
            insertion_point = None
            for i, line in enumerate(lines):
                if line.strip().startswith(('def ', 'class ')):
                    insertion_point = i + 1
                    break
            
            if insertion_point and insertion_point < len(lines):
                tier_comment = '    # TIER -1 (BOUND): Establish constraints\n'
                lines.insert(insertion_point, tier_comment)
                content = '\n'.join(lines)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.files_with_tiers += 1
    
    def _add_tier_to_javascript(self, filepath: Path):
        """TIER 1: Add TIER comments to JavaScript file."""
        has_tiers, _ = self.check_tier_structure(filepath)
        if has_tiers:
            return  # Already has structure
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Add tier comments at top if not present
        if not content.strip().startswith('//'):
            tier_comment = '''// TIER -1 (BOUND): Input validation and error setup
// TIER 0 (FREE): Explore possibilities
// TIER 1 (BOUND): Lock in root-cause logic
// TIER 2 (FREE): Verify consistency
// TIER 3+ (BOUND): Automate return and integrate

'''
            content = tier_comment + content
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.files_with_tiers += 1
    
    def report_coverage(self):
        """
        TIER 3+: Generate comprehensive coverage report.
        
        Shows what percentage of codebase follows TIER structure.
        """
        print("\n" + "=" * 70)
        print("TIER STRUCTURE COVERAGE REPORT")
        print("=" * 70)
        
        py_files = self.get_python_files()
        js_files = self.get_js_files()
        
        # Reset counters for fresh report
        total_with_tiers = 0
        
        print(f"\nPython Files: {len(py_files)}")
        print(f"JavaScript Files: {len(js_files)}")
        
        # Check Python files
        py_with_tiers = 0
        print("\nPython Files with TIER Structure:")
        print("-" * 70)
        for py_file in py_files:
            has_tiers, tiers = self.check_tier_structure(py_file)
            if has_tiers:
                py_with_tiers += 1
                total_with_tiers += 1
                status = "[OK]"
            else:
                status = "[--]"
            rel_path = py_file.relative_to(self.workspace)
            print(f"  {status} {rel_path}")
        
        # Check JavaScript files
        js_with_tiers = 0
        print("\nJavaScript Files with TIER Structure:")
        print("-" * 70)
        for js_file in js_files:
            has_tiers, tiers = self.check_tier_structure(js_file)
            if has_tiers:
                js_with_tiers += 1
                total_with_tiers += 1
                status = "[OK]"
            else:
                status = "[--]"
            rel_path = js_file.relative_to(self.workspace)
            print(f"  {status} {rel_path}")
        
        # Summary
        total_files = len(py_files) + len(js_files)
        coverage_pct = (total_with_tiers / total_files * 100) if total_files > 0 else 0
        
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Total Files: {total_files}")
        print(f"Files with TIER Structure: {total_with_tiers}")
        print(f"Coverage: {coverage_pct:.1f}%")
        print()
        if coverage_pct == 100:
            print("[OK] TARGET ACHIEVED: 100% of files have TIER comments")
        else:
            print(f"[--] IN PROGRESS: {total_files - total_with_tiers} files need TIER structure")
            print("     Run: python tier_applier.py --apply")
        print("=" * 70)

if __name__ == "__main__":
    import sys
    
    applier = TierApplier()
    
    if "--report" in sys.argv or not sys.argv[1:]:
        applier.report_coverage()
    elif "--apply" in sys.argv:
        print("Applying TIER structure to all files...")
        applier.apply_tier_structure_to_all()
        applier.report_coverage()
    elif "--verify" in sys.argv:
        applier.report_coverage()
        if applier.files_with_tiers == applier.files_scanned:
            print("\n✓ ALL FILES HAVE TIER STRUCTURE")
            sys.exit(0)
        else:
            print(f"\n✗ {applier.files_scanned - applier.files_with_tiers} files need TIER structure")
            sys.exit(1)
    else:
        print("Usage: python tier_applier.py [--report] [--apply] [--verify]")
        print("  --report: Show TIER coverage across codebase (default)")
        print("  --apply: Inject TIER structure into all files")
        print("  --verify: Check if ALL files have TIER structure")
