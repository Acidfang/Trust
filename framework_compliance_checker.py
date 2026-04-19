#!/usr/bin/env python3
"""
FRAMEWORK COMPLIANCE CHECKER
=============================

Verifies that critical thinking frameworks are applied to work.
Checks for THINKING_FIRST, TCHT, SIX_TIERS in code and documentation.

THIS MODULE EXEMPLIFIES THE SONG STRUCTURE:
- TIER -1: Honest verification requirements
- TIER 0:  Explore multiple check paths
- TIER 1:  Root-cause framework violations
- TIER 2:  Verify consistency across all files
- TIER 3+: Automated compliance reporting

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
        # ================================================================
        # TIER -1 (BOUND): Establish honest preconditions
        # ================================================================
        # What MUST be true for this checker to work?
        self.workspace = Path(workspace or "c:\\Determined")
        self.issues = defaultdict(list)
        self.compliant_files = []
        self.exclude_dirs = {".venv", ".git", "_archive", "__pycache__"}
        
        # Honest assessment: These are our actual constraints
        self._preconditions_met = (
            self.workspace.exists()
            and self.workspace.is_dir()
        )
    
    def should_process(self, path):
        """Check if path should be processed."""
        for exclude in self.exclude_dirs:
            if exclude in path.parts:
                return False
        return True
    
    def run_all_checks(self):
        """
        Execute all compliance checks in tier-structured sequence.
        TIER -1 → 0 → 1 → 2 → 3+
        """
        # ================================================================
        # TIER -1 (BOUND): Verify we can even proceed
        # ================================================================
        print("[TIER -1] Verifying preconditions...")
        if not self._preconditions_met:
            print(f"[TIER -1 FAIL] Workspace not accessible: {self.workspace}")
            return False
        print("[TIER -1 OK] Preconditions met\n")
        
        # ================================================================
        # TIER 0 (FREE): Explore multiple verification paths
        # ================================================================
        print("[TIER 0] Planning verification approaches...")
        checks = [
            ("framework_references", self.check_framework_references,
             "Verify frameworks are referenced in code"),
            ("decision_logging", self.check_decision_logging,
             "Verify decisions are logged"),
            ("system_files", self.check_framework_system_files,
             "Verify required framework files exist"),
            ("code_structure", self.check_code_structure,
             "Verify code follows best practices"),
        ]
        print(f"[TIER 0] {len(checks)} verification approaches available\n")
        
        # ================================================================
        # TIER 1 (BOUND): Execute root-cause checks
        # ================================================================
        print("[TIER 1] Executing verification checks...")
        for check_name, check_func, description in checks:
            try:
                check_func()
                print(f"[TIER 1] {check_name}: executed")
            except Exception as e:
                self.issues["execution_error"].append(
                    f"{check_name}: {str(e)}"
                )
                print(f"[TIER 1 ERROR] {check_name}: {str(e)}")
        print()
        
        # ================================================================
        # TIER 2 (FREE): Verify consistency across ALL findings
        # ================================================================
        print("[TIER 2] Verifying consistency across all checks...")
        consistency_issues = self._verify_consistency()
        if consistency_issues:
            for issue in consistency_issues:
                self.issues["consistency_violation"].append(issue)
            print(f"[TIER 2] {len(consistency_issues)} consistency issues found\n")
        else:
            print("[TIER 2] Consistency verified\n")
        
        # ================================================================
        # TIER 3+ (BOUND): Generate automated report
        # ================================================================
        print("[TIER 3+] Generating compliance report...")
        return self.report()
    
    def _verify_consistency(self):
        """
        TIER 2: Check that violations are consistent.
        If one file is missing frameworks, are they ALL missing?
        If one file has errors, do related files also have errors?
        """
        issues = []
        
        # Consistency check: framework documentation
        doc_files = list(self.workspace.glob("AI_CRITICAL_THINKING*.md"))
        if len(doc_files) > 0:
            # We have SOME framework docs
            # Do Python files reference them?
            if self.compliant_files == []:
                issues.append(
                    "Inconsistency: Framework docs exist but Python files don't reference them"
                )
        
        # Consistency check: decision logging
        decision_log_exists = (self.workspace / "DECISION_LOG.jsonl").exists()
        frameworks_use_logging = any(
            "decision" in f[0].lower()
            for f in self.compliant_files
        )
        if decision_log_exists and not frameworks_use_logging:
            issues.append(
                "Inconsistency: Decision log exists but not integrated in code"
            )
        
        return issues
    
    def check_framework_references(self):
        """
        TIER 1: Root-cause check for framework references.
        Not just "do they mention frameworks?" but "are they using them correctly?"
        """
        print("[TIER 1] Checking framework references...")
        
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
        """TIER 1: Root-cause check for decision transparency."""
        print("[TIER 1] Checking decision logging...")
        
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
        """TIER 1: Root-cause check for framework system file completeness."""
        print("[TIER 1] Checking framework system files...")
        
        required_files = {
            "AI_CRITICAL_THINKING_UNIVERSAL_MANDATE.md": "Template for all AIs",
            "AI_CRITICAL_THINKING_TASK_TEMPLATE.md": "Per-task execution guide",
            "AI_CRITICAL_THINKING_QUICK_REFERENCE.md": "1-page lookup",
            "CRITICAL_THINKING_MASTER_INDEX.md": "Navigation hub",
            "AI_ENVIRONMENT_SELF_KNOWLEDGE.md": "Environment inventory",
            "PRE_ACTION_CHECKLIST.md": "6-step verification",
            "AI_UNIFIED_OPERATING_SYSTEM.md": "Complete integration",
        }
        
        for filename, description in required_files.items():
            if not (self.workspace / filename).exists():
                self.issues["missing_system_file"].append(
                    f"{filename}: {description}"
                )
    
    def check_code_structure(self):
        """TIER 1: Root-cause check for code quality patterns."""
        print("[TIER 1] Checking code structure...")
        
        patterns = {
            "has_docstring": ['"""', "'''"],
            "validates_input": ["assert", "if not", " or "],
            "handles_errors": ["try:", "except", "raise"],
            "has_logging": ["print(", "logger", "log."],
        }
        
        for py_file in self.workspace.rglob("*.py"):
            if not self.should_process(py_file):
                continue
            
            if py_file.stat().st_size < 100:
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                rel_path = str(py_file.relative_to(self.workspace))
                missing_patterns = []
                
                for pattern_name, keywords in patterns.items():
                    found = any(kw in content for kw in keywords)
                    if not found:
                        missing_patterns.append(pattern_name)
                
                if len(missing_patterns) >= 3:
                    self.issues["weak_code_structure"].append(
                        f"{rel_path}: missing {missing_patterns}"
                    )
            
            except Exception:
                pass
    
    def report(self):
        """
        TIER 3+: Generate automated compliance report.
        Return boolean: True if compliant, False otherwise.
        """
        print("\n" + "="*70)
        print("FRAMEWORK COMPLIANCE REPORT [TIER 3+]")
        print("="*70 + "\n")
        
        total_issues = sum(len(v) for v in self.issues.values())
        
        if total_issues == 0 and self.compliant_files:
            print("[OK] Framework compliance verified.\n")
            print(f"✓ Compliant files: {len(self.compliant_files)}")
            for filepath, frameworks in self.compliant_files[:5]:
                print(f"    {filepath}: {', '.join(frameworks)}")
            if len(self.compliant_files) > 5:
                print(f"    ... and {len(self.compliant_files) - 5} more")
            print("\n[TIER 3+ RESULT] PASSED\n")
            return True
        
        if total_issues > 0:
            print(f"[ALERT] {total_issues} compliance issues found\n")
            
            for issue_type, items in sorted(self.issues.items()):
                print(f"[{issue_type.upper()}] {len(items)} items")
                for item in items[:3]:
                    print(f"    {item}")
                if len(items) > 3:
                    print(f"    ... and {len(items) - 3} more")
                print()
            
            print("[TIER 3+ RESULT] FAILED - Issues detected\n")
            return False
        
        print("[TIER 3+ RESULT] INDETERMINATE - No issues, no compliance found\n")
        return False


if __name__ == "__main__":
    """Execute compliance checker with full tier structure."""
    checker = FrameworkComplianceChecker()
    success = checker.run_all_checks()
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
