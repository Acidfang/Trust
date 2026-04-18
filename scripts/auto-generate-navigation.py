#!/usr/bin/env python3
"""
Auto-Generate Navigation from Framework Modules
================================================

Scans framework/ directory for all modules with README.md files.
Extracts metadata and auto-generates:
  1. Wiki navigation data (_data/frameworks.yml)
  2. Framework index markdown file (wiki/docs/frameworks-index.md)
  3. Verifies correctness before commit

Run: python auto-generate-navigation.py [--verify] [--commit]
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Optional
import yaml

# ============================================================================
# Configuration
# ============================================================================

FRAMEWORK_DIR = Path(__file__).parent.parent / "framework"
WIKI_DATA_DIR = Path(__file__).parent.parent / "wiki" / "_data"
WIKI_DOCS_DIR = Path(__file__).parent.parent / "wiki" / "docs"

# ============================================================================
# Framework Metadata Extractor
# ============================================================================

class FrameworkMetadata:
    """Extract metadata from framework README.md"""
    
    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
        self.readme = path / "README.md"
        self.metadata = {}
        
    def exists(self) -> bool:
        return self.readme.exists()
    
    def extract(self) -> Dict:
        """Extract title, description, key info from README"""
        if not self.exists():
            return {}
        
        content = self.readme.read_text(encoding='utf-8')
        
        # Extract title (first h1)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else self.name.replace('-', ' ').title()
        
        # Extract description - try multiple patterns
        # Pattern 1: Subtitle (## FOO)
        desc_match = re.search(r'^##\s+(.+?)$', content, re.MULTILINE)
        if desc_match:
            description = desc_match.group(1).strip()[:150]
        else:
            # Pattern 2: Any paragraph after h1
            para_match = re.search(r'^#[^\n]*\n+(.+?)(?:\n\n|$)', content, re.MULTILINE)
            description = para_match.group(1).strip() if para_match else ""
            description = description.replace('\n', ' ')[:150]
        
        # Extract usage section
        usage_match = re.search(r'## Usage\n\n```(.+?)```', content, re.DOTALL)
        usage = usage_match.group(0) if usage_match else None
        
        # Extract key files
        files_match = re.findall(r'- `(.+?)`', content)
        key_files = files_match[:5] if files_match else []
        
        self.metadata = {
            'name': self.name,
            'title': title,
            'description': description,
            'path': f'framework/{self.name}',
            'readme': f'framework/{self.name}/README.md',
            'key_files': key_files,
            'has_demo': (self.path / 'Demo.py').exists() or (self.path / 'demo.py').exists() or (self.path / 'demo.js').exists(),
            'has_tests': (self.path / 'test.py').exists() or (self.path / 'tests').exists(),
        }
        
        return self.metadata


class FrameworkIndexGenerator:
    """Generate navigation files from framework metadata"""
    
    def __init__(self):
        self.frameworks: List[Dict] = []
        
    def discover_frameworks(self) -> List[FrameworkMetadata]:
        """Find all framework directories with README.md"""
        frameworks = []
        
        if not FRAMEWORK_DIR.exists():
            print(f"⚠ Framework directory not found: {FRAMEWORK_DIR}")
            return frameworks
        
        for item in sorted(FRAMEWORK_DIR.iterdir()):
            if item.is_dir() and not item.name.startswith('_'):
                fm = FrameworkMetadata(item)
                if fm.exists():
                    frameworks.append(fm)
        
        return frameworks
    
    def extract_all_metadata(self, frameworks: List[FrameworkMetadata]) -> List[Dict]:
        """Extract metadata from all frameworks"""
        results = []
        for fm in frameworks:
            metadata = fm.extract()
            if metadata:
                results.append(metadata)
        return results
    
    def generate_jekyll_data(self, frameworks: List[Dict]) -> str:
        """Generate _data/frameworks.yml for Jekyll navigation"""
        data = {
            'frameworks': frameworks,
            'generated_at': __import__('datetime').datetime.now().isoformat(),
            'count': len(frameworks),
        }
        
        return yaml.dump(data, default_flow_style=False, sort_keys=False)
    
    def generate_wiki_index(self, frameworks: List[Dict]) -> str:
        """Generate wiki/docs/frameworks-index.md"""
        content = """# Framework Index

Auto-generated navigation for all framework modules.

Last updated: {timestamp}

## Available Frameworks

""".format(timestamp=__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        for fw in frameworks:
            content += f"### [{fw['title']}](../../../{fw['readme']})\n\n"
            content += f"Location: `{fw['path']}/`\n\n"
            
            if fw['description']:
                content += f"Description: {fw['description']}\n\n"
            
            content += "Contents:\n"
            if fw['key_files']:
                for f in fw['key_files']:
                    content += f"- {f}\n"
            content += "\n"
            
            content += "Features:\n"
            if fw['has_demo']:
                content += "- Demo/Examples included\n"
            if fw['has_tests']:
                content += "- Tests included\n"
            if 'universal' in fw['name']:
                content += "- Core physics foundation\n"
            if 'cosmology' in fw['name']:
                content += "- Time-reversal dynamics\n"
            content += "\n"
            
            content += "---\n\n"
        
        content += f"""## Framework Statistics

Total Frameworks: {len(frameworks)}
Generated: {__import__('datetime').datetime.now().isoformat()}

## Quick Start

1. Navigate to framework directory: `cd framework/{frameworks[0]['name']}`
2. Check README: `cat README.md`
3. Run demo: `python Demo.py` (if available)

---

Navigation auto-generated by `scripts/auto-generate-navigation.py`
"""
        
        return content
    
    def verify_correctness(self, frameworks: List[Dict]) -> bool:
        """Verify all framework metadata is complete and correct"""
        print("\n🔍 Verifying framework metadata...")
        
        all_valid = True
        
        for fw in frameworks:
            required_fields = ['name', 'title', 'description', 'path', 'readme']
            missing = [f for f in required_fields if not fw.get(f)]
            
            if missing:
                print(f"  ✗ {fw.get('name', '?')}: Missing {missing}")
                all_valid = False
            else:
                print(f"  ✓ {fw['name']}: Valid")
                print(f"    - Title: {fw['title']}")
                print(f"    - Path: {fw['path']}")
                print(f"    - Files: {len(fw.get('key_files', []))} listed")
        
        if all_valid:
            print("\n✓ All frameworks valid\n")
        else:
            print("\n✗ Some frameworks have incomplete metadata\n")
        
        return all_valid
    
    def generate_all(self, verify: bool = True) -> bool:
        """Run complete generation pipeline"""
        print("🔧 Discovering frameworks...\n")
        frameworks_meta = self.discover_frameworks()
        
        if not frameworks_meta:
            print("⚠ No frameworks found with README.md")
            return False
        
        print(f"Found {len(frameworks_meta)} frameworks:")
        for fm in frameworks_meta:
            print(f"  - {fm.name}")
        
        print("\n📊 Extracting metadata...\n")
        frameworks_data = self.extract_all_metadata(frameworks_meta)
        
        if verify and not self.verify_correctness(frameworks_data):
            return False
        
        print("📝 Generating Jekyll data (_data/frameworks.yml)...")
        jekyll_yaml = self.generate_jekyll_data(frameworks_data)
        
        WIKI_DATA_DIR.mkdir(parents=True, exist_ok=True)
        jekyll_file = WIKI_DATA_DIR / "frameworks.yml"
        jekyll_file.write_text(jekyll_yaml)
        print(f"  ✓ Created {jekyll_file}")
        
        print("\n📋 Generating wiki index (wiki/docs/frameworks-index.md)...")
        wiki_index = self.generate_wiki_index(frameworks_data)
        
        WIKI_DOCS_DIR.mkdir(parents=True, exist_ok=True)
        wiki_file = WIKI_DOCS_DIR / "frameworks-index.md"
        wiki_file.write_text(wiki_index, encoding='utf-8')
        print(f"  ✓ Created {wiki_file}")
        
        print("\n✓ Navigation auto-generated successfully\n")
        return True


# ============================================================================
# Main
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Auto-generate framework navigation")
    parser.add_argument('--verify', action='store_true', default=True, help="Verify metadata (default: yes)")
    parser.add_argument('--no-verify', action='store_false', dest='verify', help="Skip verification")
    parser.add_argument('--commit', action='store_true', help="Auto-commit changes to git (requires clean working tree)")
    
    args = parser.parse_args()
    
    generator = FrameworkIndexGenerator()
    success = generator.generate_all(verify=args.verify)
    
    if not success:
        sys.exit(1)
    
    if args.commit:
        print("📦 Committing changes...")
        os.system('cd ' + str(FRAMEWORK_DIR.parent) + ' && git add wiki/_data/frameworks.yml wiki/docs/frameworks-index.md && git commit -m "Automation: Auto-generate framework navigation from discovery" && git push origin master')
        print("✓ Committed and pushed")
    
    sys.exit(0)


if __name__ == '__main__':
    main()
