#!/usr/bin/env python3
"""
FRAMEWORK COMPLIANCE CHECKER
=============================

Verifies that critical thinking frameworks are applied to work.
Checks for THINKING_FIRST, TCHT, SIX_TIERS in code and documentation.

Required frameworks:
  1. THINKING_FIRST: Complete binary logic before coding
  2. TCHT: 5-tier verification (Tier -1 to Tier 3+)
  3. SIX_TIERS: Coherence progression (Identify → Validate)
  4. DECISION_LOGGING: Transparent reasoning

Usage: python framework_compliance_checker.py
"""

from pathlib import Path
from collections import defaultdict


class FrameworkComplianceChecker:
    """Check if critical thinking frameworks are applied."""
    
    def __init__(self, workspace=None):
        self.workspace = Path(workspace or "c:\\Determined")
        self.issues = defaultdict(list)
        self.compliant_files = []
        self.exclude_dirs = {".venv", ".git", "_archive", "__pycache__"}
    
    def should_process(self, path):
        """Check if path should be processed."""
        for exclude in self.exclude_dirs:
            if exclude in path.parts:
                return False
        return True
    
    def check_framework_references(self):
        """Check if files reference critical thinking frameworks."""
        print("[*] Checking framework references...")
        
        frameworks = {
            "THINKING_FIRST": [
                "binary logic", "0,1 branches", "map all paths",
                "think before code", "trace causality"
            ],
            "TCHT": [
                "Tier -1", "Tier 0", "Tier 1", "Tier 2", "Tier 3",
                "5-tier", "verification"
            ],
            "SIX_TIERS": [
                "Identify", "Engage", "Understand", "Act", "Coordinate", "Validate",
                "coherence progression"
            ],
            "DECISION_LOGGING": [
                "decision", "why", "verify", "logged", "transparent reasoning"
            ]
        }
        
        for py_file in self.workspace.rglob("*.py"):
            if not self.should_process(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                
                rel_path = str(py_file.relative_to(self.workspace))
                frameworks_found = []
                
                for framework, keywords in frameworks.items():
                    for keyword in keywords:
                        if keyword.lower() in content:
                            if framework not in frameworks_found:
                                frameworks_found.append(framework)
                            break
                
                if not frameworks_found:
                    self.issues["missing_framework_docs"].append(rel_path)
                else:
                    self.compliant_files.append((rel_path, frameworks_found))
            
            except Exception as e:
                pass
    
    def check_decision_logging(self):
        """Check if decisions are logged."""
        print("[*] Checking decision logging...")
        
        decision_log = self.workspace / "DECISION_LOG.jsonl"
        
        if not decision_log.exists():
            self.issues["no_decision_log"].append("DECISION_LOG.jsonl not found")
        else:
            try:
                with open(decision_log, 'r', encoding='utf-8') as f:
                    line_count = sum(1 for _ in f)
                
                if line_count == 0:
                    self.issues["empty_decision_log"].append("No decisions logged yet")
            except Exception as e:
                self.issues["decision_log_error"].append(str(e))
    
    def check_framework_system_files(self):
        """Check if required framework system files exist."""
        print("[*] Checking framework system files...")
        
        required_files = {
            "AI_CRITICAL_THINKING_UNIVERSAL_MANDATE.md": "Template for all AIs",
            "AI_CRITICAL_THINKING_TASK_TEMPLATE.md": "Per-task execution guide",
            "AI_CRITICAL_THINKING_QUICK_REFERENCE.md": "1-page lookup",
            "CRITICAL_THINKING_MASTER_INDEX.md": "Navigation hub",
            "AI_ENVIRONMENT_SELF_KNOWLEDGE.md": "Environment inventory",
            "PRE_ACTION_CHECKLIST.md": "6-step verification",
            "AI_UNIFIED_OPERATING_SYSTEM.md": "Complete integration",
        }
        
        missing = []
        found = []
        
        for filename, description in required_files.items():
            if (self.workspace / filename).exists():
                found.append((filename, description))
            else:
                missing.append((filename, description))
        
        if missing:
            for filename, description in missing:
                self.issues["missing_system_file"].append(
                    f"{filename}: {description}"
                )
    
    def check_code_structure(self):
        """Check if code follows prescribed structure."""
        print("[*] Checking code structure...")
        
        patterns = {
            "has_docstring": ['"""', "'''"],
            "validates_input": ["assert", "if not", " or "],
            "handles_errors": ["try:", "except", "raise"],
            "has_logging": ["print(", "logger", "log."],
        }
        
        for py_file in self.workspace.rglob("*.py"):
            if not self.should_process(py_file):
                continue
            
            if py_file.stat().st_size < 100:  # Skip tiny files
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                rel_path = str(py_file.relative_to(self.workspace))
                found_patterns = []
                missing_patterns = []
                
                for pattern_name, keywords in patterns.items():
                    found = any(kw in content for kw in keywords)
                    if not found:
                        missing_patterns.append(pattern_name)
                
                # Only report if missing multiple best practices
                if len(missing_patterns) >= 3:
                    self.issues["weak_code_structure"].append(
                        f"{rel_path}: missing {missing_patterns}"
                    )
            
            except Exception:
                pass
    
    def report(self):
        """Print compliance report."""
        print("\n" + "="*70)
        print("FRAMEWORK COMPLIANCE REPORT")
        print("="*70 + "\n")
        
        total_issues = sum(len(v) for v in self.issues.values())
        
        if total_issues == 0 and self.compliant_files:
            print("[OK] Framework compliance verified.\n")
            print(f"Compliant files: {len(self.compliant_files)}")
            for filepath, frameworks in self.compliant_files[:5]:
                print(f"  - {filepath}: {', '.join(frameworks)}")
            if len(self.compliant_files) > 5:
                print(f"  ... and {len(self.compliant_files) - 5} more")
            return True
        
        if total_issues > 0:
            print(f"[ALERT] {total_issues} compliance issues found\n")
            
            for issue_type, items in sorted(self.issues.items()):
                print(f"[{issue_type.upper()}] {len(items)} items")
                for item in items[:3]:
                    print(f"  - {item}")
                if len(items) > 3:
                    print(f"  ... and {len(items) - 3} more")
                print()
            
            return False
        
        return True


def main():
    """Run framework compliance check."""
    import sys
    
    checker = FrameworkComplianceChecker()
    
    checker.check_framework_references()
    checker.check_decision_logging()
    checker.check_framework_system_files()
    checker.check_code_structure()
    
    success = checker.report()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
