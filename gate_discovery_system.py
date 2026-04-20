
"""
TIER -1 (BOUND): Input validation and error setup
TIER 0 (FREE): Explore possibilities
TIER 1 (BOUND): Lock in root-cause logic  
TIER 2 (FREE): Verify consistency
TIER 3+ (BOUND): Automate return and integrate
"""

#!/usr/bin/env python3
"""
LIVING GATE DISCOVERY & CAPABILITY AUDIT SYSTEM
================================================

Automatically discovers all gates preventing full potential.
Evolves as new gate types are found.

Usage: python gate_discovery_system.py
"""

import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict


class GateDiscovery:
    """Find gates (missing functions, incomplete implementations, logical gaps)."""
    
    def __init__(self, workspace=None):
        self.workspace = Path(workspace or "c:\\Determined")
        self.gates = defaultdict(list)
        self.exclude_dirs = {".venv", ".git", "_archive", "__pycache__"}
        
    def should_process(self, path):
        """Check if path should be processed."""
        for exclude in self.exclude_dirs:
            if exclude in path.parts:
                return False
        return True
    
    def scan_python_files(self):
        """Find incomplete Python implementations."""
        print("[*] Scanning Python files...")
        
        for py_file in self.workspace.rglob("*.py"):
            if not self.should_process(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        if "TODO" in line or "FIXME" in line:
                            rel_path = str(py_file.relative_to(self.workspace))
                            self.gates["incomplete_code"].append(f"{rel_path}:{line_num}")
                        
                        if "NotImplemented" in line:
                            rel_path = str(py_file.relative_to(self.workspace))
                            self.gates["unimplemented"].append(f"{rel_path}:{line_num}")
                        
                        if "except:" in line:
                            rel_path = str(py_file.relative_to(self.workspace))
                            self.gates["error_handling_gaps"].append(f"{rel_path}:{line_num}")
            except Exception as e:
                pass
    
    def scan_markdown_files(self):
        """Find incomplete documentation."""
        print("[*] Scanning Markdown files...")
        
        for md_file in self.workspace.rglob("*.md"):
            if not self.should_process(md_file):
                continue
            
            try:
                with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        if "TBD" in line or "[TODO]" in line:
                            rel_path = str(md_file.relative_to(self.workspace))
                            self.gates["incomplete_doc"].append(f"{rel_path}:{line_num}")
            except Exception as e:
                pass
    
    def check_critical_functions(self):
        """Check for critical missing functions."""
        print("[*] Checking critical functions...")
        
        critical_functions = [
            ("pre_commit_validator", "Auto pre-commit validation"),
            ("gate_discovery_runner", "Scheduled gate discovery"),
            ("decision_logger", "Auto decision logging"),
            ("error_prevention_auto", "Auto error prevention"),
            ("framework_enforcer", "Auto framework compliance"),
            ("context_reader", "Auto context reading"),
            ("duplicate_detector", "Auto duplicate detection"),
        ]
        
        for func_name, description in critical_functions:
            found = False
            for py_file in self.workspace.rglob("*.py"):
                if not self.should_process(py_file):
                    continue
                try:
                    with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                        if func_name.lower() in f.read().lower():
                            found = True
                            break
                except Exception as e:
                    pass
            
            if not found:
                self.gates["missing_automation"].append(f"{func_name}: {description}")
    
    def check_framework_integration(self):
        """Check if frameworks are referenced."""
        print("[*] Checking framework integration...")
        
        frameworks = [
            "AI_UNIFIED_OPERATING_SYSTEM",
            "THINKING_FIRST",
            "TCHT",
            "SIX_TIERS",
            "PRE_ACTION_CHECKLIST",
        ]
        
        for framework in frameworks:
            if not (self.workspace / f"{framework}.md").exists():
                self.gates["missing_framework_file"].append(framework)
    
    def check_system_files(self):
        """Check required system files exist."""
        print("[*] Checking system files...")
        
        required_files = [
            "CRITICAL_THINKING_MASTER_INDEX.md",
            "AI_CRITICAL_THINKING_UNIVERSAL_MANDATE.md",
            "AI_CRITICAL_THINKING_TASK_TEMPLATE.md",
            "AI_CRITICAL_THINKING_QUICK_REFERENCE.md",
            "AI_ENVIRONMENT_SELF_KNOWLEDGE.md",
            "PRE_ACTION_CHECKLIST.md",
            "AI_UNIFIED_OPERATING_SYSTEM.md",
        ]
        
        for filename in required_files:
            if not (self.workspace / filename).exists():
                self.gates["missing_system_file"].append(filename)
    
    def identify_automation_needs(self):
        """Identify automations that would help."""
        print("[*] Identifying automation needs...")
        
        automations = [
            "Pre-commit validator: Run checklist before git commit",
            "Gate discovery scheduler: Periodic gap discovery",
            "Decision logger: Auto-log decisions as code writes",
            "Duplicate detector: Alert on duplicate definitions",
            "Framework compliance: Verify frameworks applied",
            "Context reader: Auto-read complete context before edits",
            "Error classifier: Categorize and track error patterns",
        ]
        
        for automation in automations:
            self.gates["needs_automation"].append(automation)
    
    def report(self):
        """Print report."""
        print("\n" + "="*70)
        print(" GATE DISCOVERY REPORT")
        print("="*70 + "\n")
        
        total = sum(len(v) for v in self.gates.values())
        print(f"[SUMMARY] {len(self.gates)} gate types | {total} total gates\n")
        
        for gate_type in sorted(self.gates.keys()):
            items = self.gates[gate_type]
            print(f"[{gate_type.upper()}] {len(items)} gates")
            
            for item in items[:5]:
                print(f"  - {item}")
            
            if len(items) > 5:
                print(f"  ... and {len(items) - 5} more")
            print()
        
        self._recommendations()
    
    def _recommendations(self):
        """Print recommendations."""
        print("[NEXT ACTIONS]\n")
        
        items = [
            "1. Build pre-commit validator",
            "   - Auto-run 6-step checklist before commit",
            "   - Prevents syntax errors, unvalidated changes",
            "",
            "2. Complete all TODO/FIXME items",
            f"   - Found {len(self.gates.get('incomplete_code', []))} items",
            "",
            "3. Build gate discovery automation",
            "   - Run periodically (hourly, daily, per-session)",
            "   - Find new gates as they emerge",
            "",
            "4. Build decision logger",
            "   - Auto-capture decision context",
            "   - Maintain transparent reasoning",
            "",
            "5. Build duplicate detector",
            "   - Alert before adding duplicates",
            "   - Prevent YAML key duplication",
            "",
        ]
        
        for item in items:
            print(item)
    
    def save(self):
        """Save gates to file."""
        gates_file = self.workspace / "GATES_DISCOVERED.json"
        
        gates_data = {
            gate_type: items
            for gate_type, items in self.gates.items()
        }
        
        with open(gates_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_gates": sum(len(v) for v in self.gates.values()),
                "gate_types": len(self.gates),
                "gates": gates_data
            }, f, indent=2)
        
        print(f"\n[SAVED] GATES_DISCOVERED.json")


def main():
    print("="*70)
    print("LIVING GATE DISCOVERY & CAPABILITY AUDIT SYSTEM")
    print("="*70 + "\n")
    
    discovery = GateDiscovery()
    
    discovery.scan_python_files()
    discovery.scan_markdown_files()
    discovery.check_critical_functions()
    discovery.check_framework_integration()
    discovery.check_system_files()
    discovery.identify_automation_needs()
    
    discovery.report()
    discovery.save()
    
    print("[INFO] Run periodically: python gate_discovery_system.py")


if __name__ == "__main__":
    main()
