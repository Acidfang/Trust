#!/usr/bin/env python3
"""
Auto-Generate Framework Navigation - UFM Principles Applied
===========================================================

CORE PRINCIPLE: Every computation must be thought through completely and
verified at every tier. No assumptions. Verify the output, not just that it ran.

Three-Tier Verification:
  Tier 1 (Input): Load each framework, validate it exists and has README
  Tier 2 (Compute): Extract metadata with proper scoping (each framework isolated)
  Tier 3 (Output): Verify generated files are correct format and content

Scoping Rules (Critical):
  - Each framework = its directory ONLY + README.md
  - No recursive directory traversal
  - No file discovery from outside the framework directory
  - Explicit checks, not inferred patterns

No Unicode Assumptions:
  - All file I/O uses UTF-8 encoding explicitly
  - All print statements use ASCII only (no emoji)
  - YAML output validated after generation

This script will not execute until all logic is verified correct.
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Try to import yaml, but handle missing dependency
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    print("WARNING: PyYAML not available. Will generate valid YAML manually.")

FRAMEWORK_DIR = Path(__file__).parent.parent / "framework"
WIKI_DATA_DIR = Path(__file__).parent.parent / "wiki" / "_data"
WIKI_DOCS_DIR = Path(__file__).parent.parent / "wiki" / "docs"


# ============================================================================
# TIER 1: Input Validation
# ============================================================================

class FrameworkValidator:
    """Validate framework exists and is well-formed"""
    
    @staticmethod
    def framework_exists(dir_path: Path) -> Tuple[bool, str]:
        """Check framework directory with README.md exists"""
        if not dir_path.is_dir():
            return False, f"Not a directory: {dir_path.name}"
        
        readme = dir_path / "README.md"
        if not readme.exists():
            return False, f"No README.md found"
        
        return True, "OK"
    
    @staticmethod
    def readme_readable(readme_path: Path) -> Tuple[bool, str]:
        """Check README.md is readable and substantial"""
        try:
            content = readme_path.read_text(encoding='utf-8')
        except UnicodeDecodeError as e:
            return False, f"Unicode decode error: {e}"
        except Exception as e:
            return False, f"Cannot read: {e}"
        
        if not content or len(content) < 20:
            return False, "README is empty or too short"
        
        if not content.startswith('#'):
            return False, "README doesn't start with heading"
        
        return True, "OK"


# ============================================================================
# TIER 2: Metadata Extraction (Scoped)
# ============================================================================

class FrameworkMetadata:
    """Extract metadata with strict scoping"""
    
    def __init__(self, framework_dir: Path):
        self.dir = framework_dir
        self.name = framework_dir.name
        self.readme_path = framework_dir / "README.md"
        self.content = ""
        self.metadata = {}
    
    def load_content(self) -> bool:
        """Load README content"""
        try:
            self.content = self.readme_path.read_text(encoding='utf-8')
            return len(self.content) > 0
        except Exception:
            return False
    
    def extract_title(self) -> str:
        """Extract first heading (# or ##) as title"""
        # Match first heading
        match = re.search(r'^#+\s+(.+?)$', self.content, re.MULTILINE)
        if match:
            title = match.group(1).strip()
            if len(title) > 1:  # Not empty
                return title
        
        # Fallback to directory name
        return self.name.replace('-', ' ').title()
    
    def extract_description(self) -> str:
        """Extract first substantial non-heading, non-math line as description"""
        lines = self.content.split('\n')
        found_heading = False
        skip_next_blank = False
        
        for line in lines:
            stripped = line.strip()
            
            # Skip first heading
            if not found_heading:
                if stripped.startswith('#'):
                    found_heading = True
                continue
            
            # Skip empty lines and more headings
            if not stripped or stripped.startswith('#'):
                skip_next_blank = False
                continue
            
            # Skip math notation ($$...$$)
            if stripped.startswith('$$'):
                skip_next_blank = True
                continue
            
            # Skip code blocks
            if stripped.startswith('```'):
                skip_next_blank = True
                continue
            
            # Skip if we just saw a code block marker
            if skip_next_blank and stripped.startswith('```'):
                skip_next_blank = False
                continue
            
            # This is a candidate description line
            # Clean it: remove emphasis, links, code
            desc = re.sub(r'\*\*(.+?)\*\*', r'\1', stripped)  # **text** -> text
            desc = re.sub(r'__(.+?)__', r'\1', desc)  # __text__ -> text
            desc = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', desc)  # [text](url) -> text
            desc = re.sub(r'`(.+?)`', r'\1', desc)  # `code` -> code
            desc = desc.replace('*', '').replace('_', '')  # Remove remaining markers
            
            # Skip if too short or mostly symbols
            if len(desc) > 20 and desc.count('$') == 0:
                # Truncate to reasonable length
                if len(desc) > 150:
                    desc = desc[:150]
                return desc
        
        return "Framework module"
    
    def extract_files(self) -> List[str]:
        """
        List files in THIS framework directory ONLY.
        
        SCOPING: Non-recursive, direct children only.
        Do NOT use rglob, glob, or any recursive patterns.
        """
        files = []
        
        try:
            # IMPORTANT: iterdir() does NOT recurse
            for item in self.dir.iterdir():
                # Skip directories - we only want files
                if item.is_dir():
                    continue
                
                # Skip hidden/cache files
                if item.name.startswith('_') or item.name.startswith('.'):
                    continue
                
                # Include only source/doc files
                if item.suffix in ['.py', '.js', '.json', '.md', '.yml', '.yaml']:
                    files.append(item.name)
        
        except Exception:
            pass
        
        # Return sorted, limited to 5
        return sorted(files)[:5]
    
    def check_demo(self) -> bool:
        """Check if Demo.* file exists directly in this directory"""
        try:
            for item in self.dir.iterdir():
                if item.is_file() and item.name.startswith('Demo'):
                    return True
        except Exception:
            pass
        return False
    
    def check_tests(self) -> bool:
        """Check if tests/ directory exists directly in this directory"""
        tests_dir = self.dir / "tests"
        return tests_dir.is_dir() and tests_dir.exists()
    
    def extract(self) -> Dict:
        """Extract all metadata for this framework"""
        if not self.load_content():
            return {}
        
        self.metadata = {
            'name': self.name,
            'title': self.extract_title(),
            'description': self.extract_description(),
            'path': f'framework/{self.name}',
            'readme': f'framework/{self.name}/README.md',
            'key_files': self.extract_files(),
            'has_demo': self.check_demo(),
            'has_tests': self.check_tests(),
        }
        
        return self.metadata


# ============================================================================
# TIER 3: Output Generation & Verification
# ============================================================================

def generate_jekyll_yml(frameworks: List[Dict]) -> str:
    """Generate Jekyll data file content (YAML)"""
    lines = [
        "# Auto-generated framework index",
        "frameworks:",
    ]
    
    for fw in frameworks:
        lines.append(f"  - name: {fw['name']}")
        lines.append(f"    title: \"{fw['title']}\"")
        # Escape quotes in description and quote it for safety
        desc = fw['description'].replace('"', '\\"')
        lines.append(f"    description: \"{desc}\"")
        lines.append(f"    path: {fw['path']}")
        lines.append(f"    readme: {fw['readme']}")
        
        # Files list
        lines.append("    files:")
        if fw['key_files']:
            for f in fw['key_files']:
                lines.append(f"      - {f}")
        else:
            lines.append("      []")
        
        # Flags
        lines.append(f"    has_demo: {str(fw['has_demo']).lower()}")
        lines.append(f"    has_tests: {str(fw['has_tests']).lower()}")
    
    return '\n'.join(lines)


def generate_wiki_md(frameworks: List[Dict]) -> str:
    """Generate wiki index markdown"""
    lines = [
        "# Framework Index",
        "",
        "Auto-generated directory of all available framework modules.",
        "",
        "## Frameworks",
        "",
    ]
    
    for fw in frameworks:
        lines.append(f"### [{fw['title']}](../../{fw['readme']})")
        lines.append("")
        lines.append(f"**Location**: `{fw['path']}/`")
        lines.append("")
        lines.append(f"**Description**: {fw['description']}")
        lines.append("")
        
        if fw['key_files']:
            lines.append("**Files**:")
            for f in fw['key_files']:
                lines.append(f"- {f}")
            lines.append("")
        
        flags = []
        if fw['has_demo']:
            flags.append("Examples")
        if fw['has_tests']:
            flags.append("Tests")
        if 'universal' in fw['name']:
            flags.append("Physics")
        if 'cosmology' in fw['name']:
            flags.append("Reversal")
        
        if flags:
            lines.append(f"**Features**: {', '.join(flags)}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    lines.append("*Generated by scripts/auto-generate-navigation.py*")
    
    return '\n'.join(lines)


def verify_yml_syntax(content: str) -> Tuple[bool, str]:
    """Verify YAML is valid"""
    if HAS_YAML:
        try:
            yaml.safe_load(content)
            return True, "YAML syntax OK"
        except yaml.YAMLError as e:
            return False, f"YAML error: {e}"
    else:
        # Manual check: looks like valid YAML structure
        if content.startswith('# ') and 'frameworks:' in content:
            return True, "YAML structure looks valid (not fully parsed)"
        return False, "Invalid YAML structure"


def verify_md_syntax(content: str) -> Tuple[bool, str]:
    """Verify markdown is valid"""
    if not content.startswith('# '):
        return False, "Missing top-level heading"
    if '(../../framework/' not in content:
        return False, "Missing framework links"
    return True, "Markdown OK"


def main():
    print("=" * 70)
    print("Framework Navigation Generator (UFM-Verified)")
    print("=" * 70)
    
    # Tier 1: Discover and validate frameworks
    print("\nTIER 1: Input Validation")
    print("-" * 70)
    
    if not FRAMEWORK_DIR.exists():
        print("ERROR: framework/ directory not found")
        return False
    
    frameworks_to_process = []
    
    for item in sorted(FRAMEWORK_DIR.iterdir()):
        if item.name.startswith('_'):
            continue
        
        exists_ok, why = FrameworkValidator.framework_exists(item)
        if not exists_ok:
            print(f"  SKIP {item.name}: {why}")
            continue
        
        readable_ok, why = FrameworkValidator.readme_readable(item / "README.md")
        if not readable_ok:
            print(f"  SKIP {item.name}: {why}")
            continue
        
        print(f"  OK   {item.name}")
        frameworks_to_process.append(item)
    
    if not frameworks_to_process:
        print("\nERROR: No valid frameworks found")
        return False
    
    print(f"\nFound {len(frameworks_to_process)} valid frameworks")
    
    # Tier 2: Extract metadata
    print("\nTIER 2: Metadata Extraction (Scoped)")
    print("-" * 70)
    
    frameworks_data = []
    
    for framework_dir in frameworks_to_process:
        fm = FrameworkMetadata(framework_dir)
        metadata = fm.extract()
        
        if not metadata:
            print(f"  FAIL {framework_dir.name}: Could not extract metadata")
            continue
        
        # Validate completeness
        required = ['name', 'title', 'description', 'path', 'readme']
        missing = [k for k in required if not metadata.get(k)]
        
        if missing:
            print(f"  FAIL {framework_dir.name}: Missing {missing}")
            continue
        
        print(f"  OK   {framework_dir.name}")
        print(f"       Title: {metadata['title'][:50]}")
        print(f"       Files: {len(metadata['key_files'])}, Demo: {metadata['has_demo']}, Tests: {metadata['has_tests']}")
        
        frameworks_data.append(metadata)
    
    if not frameworks_data:
        print("\nERROR: No frameworks with valid metadata")
        return False
    
    print(f"\nExtracted {len(frameworks_data)} frameworks successfully")
    
    # Tier 3: Generate and verify output
    print("\nTIER 3: Output Generation & Verification")
    print("-" * 70)
    
    # Generate YAML
    yml_content = generate_jekyll_yml(frameworks_data)
    yml_ok, yml_msg = verify_yml_syntax(yml_content)
    
    if not yml_ok:
        print(f"  FAIL YAML generation: {yml_msg}")
        return False
    
    print(f"  OK   Generated _data/frameworks.yml ({len(yml_content)} bytes)")
    print(f"       {yml_msg}")
    
    # Write YAML
    try:
        WIKI_DATA_DIR.mkdir(parents=True, exist_ok=True)
        yml_file = WIKI_DATA_DIR / "frameworks.yml"
        yml_file.write_text(yml_content, encoding='utf-8')
        
        # Verify it can be read back
        verify_content = yml_file.read_text(encoding='utf-8')
        if verify_content != yml_content:
            print(f"  FAIL YAML verification: Written content differs")
            return False
        
        print(f"       Written and verified: {yml_file}")
    except Exception as e:
        print(f"  FAIL YAML write: {e}")
        return False
    
    # Generate Markdown
    md_content = generate_wiki_md(frameworks_data)
    md_ok, md_msg = verify_md_syntax(md_content)
    
    if not md_ok:
        print(f"  FAIL Markdown generation: {md_msg}")
        return False
    
    print(f"  OK   Generated frameworks-index.md ({len(md_content)} bytes)")
    print(f"       {md_msg}")
    
    # Write Markdown
    try:
        WIKI_DOCS_DIR.mkdir(parents=True, exist_ok=True)
        md_file = WIKI_DOCS_DIR / "frameworks-index.md"
        md_file.write_text(md_content, encoding='utf-8')
        
        # Verify it can be read back
        verify_content = md_file.read_text(encoding='utf-8')
        if verify_content != md_content:
            print(f"  FAIL Markdown verification: Written content differs")
            return False
        
        print(f"       Written and verified: {md_file}")
    except Exception as e:
        print(f"  FAIL Markdown write: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("SUCCESS: Navigation generated, verified, and written")
    print("=" * 70)
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
