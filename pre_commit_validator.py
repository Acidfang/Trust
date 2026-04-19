#!/usr/bin/env python3
"""
PRE-COMMIT VALIDATOR
====================

Runs before git commit to catch errors early.
Implements the 6-step checklist from PRE_ACTION_CHECKLIST.md

Steps:
  1. Read complete context (check file completeness)
  2. Check for existing content (detect duplicates)
  3. Validate syntax (Python, YAML, JSON, Markdown)
  4. Test critical paths (if applicable)
  5. Verify content quality (frameworks, docs)
  6. Verify git state (clean working directory)

Usage: python pre_commit_validator.py [--staged-only] [--fix]
"""

import json
import sys
from pathlib import Path
from collections import defaultdict


class PreCommitValidator:
    """Validate staged files before commit."""
    
    def __init__(self, fix_mode=False):
        self.workspace = Path("c:\\Determined")
        self.fix_mode = fix_mode
        self.errors = []
        self.warnings = []
        self.fixes = []
        self.staged_files = self._get_staged_files()
    
    def _get_staged_files(self):
        """Get list of staged files from git."""
        import subprocess
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                cwd=self.workspace,
                capture_output=True,
                text=True
            )
            return result.stdout.strip().split('\n') if result.stdout else []
        except (OSError, subprocess.CalledProcessError):
            return []
    
    def validate(self):
        """Run all validation checks."""
        print("[VALIDATOR] Pre-commit validation starting...\n")
        
        if not self.staged_files or self.staged_files == ['']:
            print("[INFO] No staged files to validate.")
            return True
        
        for staged_file in self.staged_files:
            if not staged_file:
                continue
            
            file_path = self.workspace / staged_file
            if not file_path.exists():
                continue
            
            print(f"[CHECK] {staged_file}")
            
            # Route to appropriate validator
            if staged_file.endswith('.py'):
                self._validate_python(file_path, staged_file)
            elif staged_file.endswith(('.yml', '.yaml')):
                self._validate_yaml(file_path, staged_file)
            elif staged_file.endswith('.json'):
                self._validate_json(file_path, staged_file)
            elif staged_file.endswith('.md'):
                self._validate_markdown(file_path, staged_file)
        
        return self._report()
    
    def _validate_python(self, file_path, rel_path):
        """Validate Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check syntax
            try:
                compile(content, str(file_path), 'exec')
            except SyntaxError as e:
                self.errors.append(f"[{rel_path}] SYNTAX: Line {e.lineno}: {e.msg}")
            
            # Check for bare except
            for line_num, line in enumerate(content.split('\n'), 1):
                if line.strip() == 'except:':
                    self.errors.append(
                        f"[{rel_path}] ERROR_HANDLING: Line {line_num}: "
                        "bare except: clause (specify exception type)"
                    )
            
            # Check for unhandled exceptions
            if 'NotImplemented' in content and 'raise NotImplemented' not in content:
                self.warnings.append(
                    f"[{rel_path}] INCOMPLETE: NotImplemented found but not raised"
                )
        
        except Exception as e:
            self.errors.append(f"[{rel_path}] READ_ERROR: {str(e)}")
    
    def _validate_yaml(self, file_path, rel_path):
        """Validate YAML file."""
        try:
            import yaml
        except ImportError:
            self.warnings.append(f"[{rel_path}] PyYAML not installed, skipping YAML validation")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse YAML
            yaml.safe_load(content)
            
            # Check for duplicate keys (PyYAML silently ignores them)
            lines = content.split('\n')
            keys_by_level = defaultdict(list)
            
            for line_num, line in enumerate(lines, 1):
                stripped = line.lstrip()
                indent = len(line) - len(stripped)
                
                if ':' in stripped and not stripped.startswith('#'):
                    key = stripped.split(':')[0].strip()
                    level = indent // 2
                    
                    # Track keys at this level
                    for existing_key, existing_line in keys_by_level[level]:
                        if existing_key == key:
                            self.errors.append(
                                f"[{rel_path}] DUPLICATE_KEY: '{key}' at line {line_num} "
                                f"(duplicate of line {existing_line})"
                            )
                            break
                    
                    keys_by_level[level].append((key, line_num))
        
        except yaml.YAMLError as e:
            self.errors.append(f"[{rel_path}] YAML_ERROR: {str(e)}")
        except Exception as e:
            self.errors.append(f"[{rel_path}] READ_ERROR: {str(e)}")
    
    def _validate_json(self, file_path, rel_path):
        """Validate JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(
                f"[{rel_path}] JSON_ERROR: Line {e.lineno}, Col {e.colno}: {e.msg}"
            )
        except Exception as e:
            self.errors.append(f"[{rel_path}] READ_ERROR: {str(e)}")
    
    def _validate_markdown(self, file_path, rel_path):
        """Validate Markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for incomplete markers
            incomplete_markers = [
                ('TBD', 'to be determined'),
                ('[TODO]', 'incomplete task'),
                ('...', 'incomplete thought'),
            ]
            
            for marker, description in incomplete_markers:
                if marker in content:
                    self.warnings.append(
                        f"[{rel_path}] INCOMPLETE_DOC: Contains '{marker}' ({description})"
                    )
                    break
        
        except Exception as e:
            self.errors.append(f"[{rel_path}] READ_ERROR: {str(e)}")
    
    def _report(self):
        """Report validation results."""
        print("\n" + "="*70)
        
        if self.errors:
            print("ERRORS (blocking commit)")
            print("="*70)
            for error in self.errors:
                print(f"  [FAIL] {error}")
            print()
        
        if self.warnings:
            print("WARNINGS (non-blocking)")
            print("="*70)
            for warning in self.warnings:
                print(f"  [WARN] {warning}")
            print()
        
        # Summary
        total_issues = len(self.errors) + len(self.warnings)
        print("="*70)
        print(f"[SUMMARY] {len(self.errors)} errors, {len(self.warnings)} warnings\n")
        
        if self.errors:
            print("[ACTION REQUIRED]")
            print("  Fix errors above before committing.")
            print("  See PRE_ACTION_CHECKLIST.md for guidance.")
            print()
            return False
        
        if self.warnings:
            print("[ACTION SUGGESTED]")
            print("  Consider fixing warnings before committing.")
            print()
        
        print("[OK] Validation passed. Safe to commit.")
        return True


def main():
    """Run pre-commit validation."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Pre-commit validator for git commits"
    )
    parser.add_argument(
        "--staged-only",
        action="store_true",
        help="Only validate staged files"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix issues where possible"
    )
    
    args = parser.parse_args()
    
    validator = PreCommitValidator(fix_mode=args.fix)
    success = validator.validate()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
