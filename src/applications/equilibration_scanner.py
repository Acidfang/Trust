#!/usr/bin/env python3
"""
EQUILIBRATION LAYER - SPRINT 1: INCONSISTENCY SCANNER
======================================================

PURPOSE: Scan real ledgers for contradictions and inconsistencies
INPUT: Existing ARIA ledgers (elections, parameters, observations)
OUTPUT: Ranked list of real inconsistencies with analysis

This is the working model that demonstrates:
1. Theory can find real contradictions
2. Framework is applicable to real systems
3. Inconsistencies are measurable and auditable
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict
import hashlib

class InconsistencyScanner:
    """Scan ledgers for contradictions using Universal Equilibration Protocol"""
    
    def __init__(self, ledger_dir: str):
        self.ledger_dir = ledger_dir
        self.inconsistencies = []
        self.ledger_data = {}
        self.discovered_facts = defaultdict(list)
    
    def load_ledgers(self) -> bool:
        """Load all JSONL ledger files"""
        print("[SCANNER] Loading ledgers from:", self.ledger_dir)
        
        if not os.path.exists(self.ledger_dir):
            print(f"ERROR: Ledger directory not found: {self.ledger_dir}")
            return False
        
        ledger_files = [f for f in os.listdir(self.ledger_dir) if f.startswith('ledger_') and f.endswith('.jsonl')]
        print(f"[SCANNER] Found {len(ledger_files)} ledger files")
        
        for ledger_file in ledger_files:
            filepath = os.path.join(self.ledger_dir, ledger_file)
            self.ledger_data[ledger_file] = []
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        if line.strip():
                            try:
                                entry = json.loads(line)
                                self.ledger_data[ledger_file].append(entry)
                            except json.JSONDecodeError as e:
                                print(f"  WARNING: Parse error in {ledger_file} line {line_num}: {e}")
            except IOError as e:
                print(f"  ERROR reading {ledger_file}: {e}")
        
        total_entries = sum(len(entries) for entries in self.ledger_data.values())
        print(f"[SCANNER] Loaded {total_entries} total ledger entries")
        return True
    
    def discover_facts(self):
        """Extract facts from ledgers into searchable structure"""
        print("\n[SCANNER] Discovering facts from ledgers...")
        
        # Facts from elections
        if 'ledger_elections.jsonl' in self.ledger_data:
            elections = self.ledger_data['ledger_elections.jsonl']
            print(f"  Elections: {len(elections)} decisions recorded")
            
            for election in elections:
                event_type = election.get('event_type')
                elected = election.get('elected')
                timestamp = election.get('timestamp')
                
                self.discovered_facts['elections_recorded'].append({
                    'type': event_type,
                    'choice': elected,
                    'when': timestamp
                })
        
        # Facts from parameters
        if 'ledger_parameters.jsonl' in self.ledger_data:
            params = self.ledger_data['ledger_parameters.jsonl']
            print(f"  Parameters: {len(params)} configuration items")
            
            for param in params:
                param_id = param.get('parameter_id')
                default = param.get('default')
                
                self.discovered_facts['parameters_defined'].append({
                    'id': param_id,
                    'default_value': default
                })
    
    def check_contradiction_init_event(self) -> List[Dict[str, Any]]:
        """Check: Boot event executed but system continues with elected outcome?"""
        contradictions = []
        
        if not self.ledger_data.get('ledger_elections.jsonl'):
            return contradictions
        
        elections = self.ledger_data['ledger_elections.jsonl']
        boot_events = [e for e in elections if e.get('event_type') == 'boot']
        timer_events = [e for e in elections if e.get('event_type') == 'interrupt_timer']
        
        if boot_events and timer_events:
            boot_elected = boot_events[0].get('elected')
            first_timer_elected = timer_events[0].get('elected') if timer_events else None
            
            if boot_elected and first_timer_elected and boot_elected != first_timer_elected:
                contradictions.append({
                    'id': self._gen_id('boot_election_consistency'),
                    'type': 'B (conditional)',
                    'severity': 'medium',
                    'title': 'Boot Election vs First Timer Election Mismatch',
                    'description': f'Bootstrap elected "{boot_elected}" but first timer event elected "{first_timer_elected}"',
                    'evidence': [
                        f'Boot event elected: {boot_elected}',
                        f'First interrupt_timer elected: {first_timer_elected}',
                        'Question: Was bootstrap overridden immediately, or is this recording inconsistency?'
                    ],
                    'affected_domains': ['initialization', 'election_consistency'],
                    'resolution_candidates': [
                        'A) Boot election was correct, log should show immediate override',
                        'B) First timer was mistake, system should re-elect boot choice',
                        'C) Both are correct at different times, clarify timeline'
                    ]
                })
        
        return contradictions
    
    def check_contradiction_utility_convergence(self) -> List[Dict[str, Any]]:
        """Check: Do utility scores converge or diverge over time?"""
        contradictions = []
        
        if not self.ledger_data.get('ledger_elections.jsonl'):
            return contradictions
        
        elections = self.ledger_data['ledger_elections.jsonl']
        
        # Check if utility scores for same candidates are consistent
        utility_history = defaultdict(list)
        
        for election in elections:
            utilities = election.get('utilities', {})
            for candidate, score in utilities.items():
                utility_history[candidate].append(score)
        
        # Look for candidates that appear with different scores
        for candidate, scores in utility_history.items():
            if len(scores) > 1:
                min_score = min(scores)
                max_score = max(scores)
                
                if abs(max_score - min_score) > 0.01:  # More than 1% variance
                    contradictions.append({
                        'id': self._gen_id(f'utility_variance_{candidate}'),
                        'type': 'C (logically forced)',
                        'severity': 'medium',
                        'title': f'Utility Score Variance: {candidate}',
                        'description': f'Candidate "{candidate}" has inconsistent utility scores across elections',
                        'evidence': [
                            f'Candidate: {candidate}',
                            f'Min score: {min_score}',
                            f'Max score: {max_score}',
                            f'Variance: {abs(max_score - min_score):.2%}',
                            f'Observations: {len(scores)} elections'
                        ],
                        'affected_domains': ['utility_model', 'decision_consistency'],
                        'resolution_candidates': [
                            'A) Utilities should be deterministic - fix scoring model',
                            'B) Variance is expected - document why',
                            'C) Record shows timing dependence - clarify conditions'
                        ]
                    })
        
        return contradictions
    
    def check_contradiction_parameter_defaults(self) -> List[Dict[str, Any]]:
        """Check: Are parameter defaults actually used?"""
        contradictions = []
        
        if not self.ledger_data.get('ledger_parameters.jsonl'):
            return contradictions
        
        params = self.ledger_data['ledger_parameters.jsonl']
        
        # Check: Does "manifestation_enabled" default to false, but are there manifestations?
        manifestation_param = next((p for p in params if p.get('parameter_id') == 'manifestation_enabled'), None)
        
        if manifestation_param:
            default_value = manifestation_param.get('default')
            description = manifestation_param.get('description', '')
            
            contradictions.append({
                'id': self._gen_id('manifestation_enabled_default'),
                'type': 'A (predicted)',
                'severity': 'high',
                'title': 'Potential Gap: Manifestation Disabled By Default',
                'description': f'Parameter "manifestation_enabled" defaults to {default_value}, but description says "{description}"',
                'evidence': [
                    f'Parameter: manifestation_enabled',
                    f'Default value: {default_value}',
                    f'Description: {description}',
                    'Question: If manifestation is disabled by default, how does ARIA produce output?'
                ],
                'affected_domains': ['output', 'manifestation', 'real_world_effects'],
                'resolution_candidates': [
                    'A) Default should be true (system should manifest by default)',
                    'B) System works without manifestation (output not required)',
                    'C) Parameter is set elsewhere before use (clarify initialization)'
                ]
            })
        
        return contradictions
    
    def check_contradiction_election_frequency(self) -> List[Dict[str, Any]]:
        """Check: Does election speed match actual recorded elections?"""
        contradictions = []
        
        if not self.ledger_data.get('ledger_elections.jsonl') or not self.ledger_data.get('ledger_parameters.jsonl'):
            return contradictions
        
        elections = self.ledger_data['ledger_elections.jsonl']
        params = self.ledger_data['ledger_parameters.jsonl']
        
        # Get configured election speed
        election_speed_param = next((p for p in params if p.get('parameter_id') == 'election_speed_ms'), None)
        configured_speed_ms = election_speed_param.get('default', 100) if election_speed_param else 100
        configured_speed_sec = configured_speed_ms / 1000.0
        
        # Calculate actual election frequency from timestamps
        if len(elections) > 10:
            timestamps = [e.get('timestamp', 0) for e in elections if e.get('timestamp')]
            if len(timestamps) > 1:
                timestamps.sort()
                intervals = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
                avg_interval = sum(intervals) / len(intervals) if intervals else 0
                
                # Compare configured vs actual
                if avg_interval > 0 and configured_speed_sec > 0:
                    ratio = avg_interval / configured_speed_sec
                    
                    if abs(ratio - 1.0) > 0.1:  # More than 10% deviation
                        contradictions.append({
                            'id': self._gen_id('election_frequency_mismatch'),
                            'type': 'B (conditional)',
                            'severity': 'low',
                            'title': 'Election Frequency Configuration vs Actual',
                            'description': f'Configured election speed ({configured_speed_ms}ms) does not match actual interval ({avg_interval*1000:.1f}ms)',
                            'evidence': [
                                f'Configured speed: {configured_speed_ms}ms',
                                f'Actual average interval: {avg_interval*1000:.2f}ms',
                                f'Deviation: {(ratio-1)*100:.1f}%',
                                f'Based on {len(timestamps)} observations'
                            ],
                            'affected_domains': ['timing', 'configuration', 'performance'],
                            'resolution_candidates': [
                                'A) Update parameter to match actual frequency',
                                'B) Verify configuration is being read correctly',
                                'C) Actual speed variance is expected - document why'
                            ]
                        })
        
        return contradictions
    
    def check_contradiction_decision_history(self) -> List[Dict[str, Any]]:
        """Check: Are decisions being made, but same candidate always wins?"""
        contradictions = []
        
        if not self.ledger_data.get('ledger_elections.jsonl'):
            return contradictions
        
        elections = self.ledger_data['ledger_elections.jsonl']
        
        # Get all elected choices
        elected_choices = [e.get('elected') for e in elections if e.get('elected')]
        
        if len(elected_choices) > 5:
            choice_counts = defaultdict(int)
            for choice in elected_choices:
                choice_counts[choice] += 1
            
            # Check for monopoly: one choice wins >95% of the time
            total = len(elected_choices)
            for choice, count in choice_counts.items():
                frequency = count / total
                
                if frequency > 0.95:
                    contradictions.append({
                        'id': self._gen_id(f'election_monopoly_{choice}'),
                        'type': 'A (predicted)',
                        'severity': 'medium',
                        'title': f'Election Monopoly: "{choice}" Always Wins',
                        'description': f'Choice "{choice}" was elected {frequency*100:.1f}% of the time ({count} out of {total})',
                        'evidence': [
                            f'Winning choice: {choice}',
                            f'Election frequency: {frequency*100:.1f}%',
                            f'Total elections: {total}',
                            'Question: Is this the only valid choice, or is utility model broken?'
                        ],
                        'affected_domains': ['decision_quality', 'diversity', 'utility_model'],
                        'resolution_candidates': [
                            'A) Choice is always best - this is correct behavior',
                            'B) Utility model is broken - other choices should compete',
                            'C) Diversify decisions - force exploration over optimization'
                        ]
                    })
        
        return contradictions
    
    def _gen_id(self, seed: str) -> str:
        """Generate consistent ID from seed"""
        return hashlib.md5(seed.encode()).hexdigest()[:12]
    
    def scan(self) -> int:
        """Run complete scan and return count of inconsistencies found"""
        
        print("\n" + "="*80)
        print("EQUILIBRATION LAYER - INCONSISTENCY SCAN STARTING")
        print("="*80)
        
        # Load data
        if not self.load_ledgers():
            return 0
        
        # Extract facts
        self.discover_facts()
        
        # Run contradiction checks
        print("\n[SCANNER] Checking for contradictions...")
        
        check_methods = [
            ('Boot vs Timer Initialization', self.check_contradiction_init_event),
            ('Utility Score Convergence', self.check_contradiction_utility_convergence),
            ('Parameter Defaults', self.check_contradiction_parameter_defaults),
            ('Election Frequency', self.check_contradiction_election_frequency),
            ('Decision History', self.check_contradiction_decision_history),
        ]
        
        for check_name, check_method in check_methods:
            found = check_method()
            if found:
                print(f"  ✓ {check_name}: {len(found)} contradiction(s) found")
                self.inconsistencies.extend(found)
            else:
                print(f"  ○ {check_name}: No contradictions")
        
        # Sort by severity
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        self.inconsistencies.sort(key=lambda x: severity_order.get(x.get('severity', 'low'), 999))
        
        return len(self.inconsistencies)
    
    def report(self):
        """Print human-readable report"""
        
        print("\n" + "="*80)
        print("INCONSISTENCY SCAN RESULTS")
        print("="*80)
        print(f"\nTotal inconsistencies found: {len(self.inconsistencies)}\n")
        
        for idx, inconsistency in enumerate(self.inconsistencies, 1):
            print(f"{idx}. [{inconsistency['severity'].upper()}] {inconsistency['title']}")
            print(f"   Type: {inconsistency['type']}")
            print(f"   ID: {inconsistency['id']}")
            print(f"\n   Description:")
            print(f"   {inconsistency['description']}")
            print(f"\n   Evidence:")
            for evidence in inconsistency['evidence']:
                print(f"   - {evidence}")
            print(f"\n   Affected Domains: {', '.join(inconsistency['affected_domains'])}")
            print(f"\n   Resolution Candidates:")
            for candidate in inconsistency['resolution_candidates']:
                print(f"   {candidate}")
            print()
        
        print("="*80)
        print("END REPORT")
        print("="*80)
    
    def export_to_discovery_ledger(self, output_file: str):
        """Export findings to discovery ledger for audit trail"""
        
        discovery_ledger = {
            'scan_timestamp': datetime.now().isoformat(),
            'scan_id': self._gen_id(datetime.now().isoformat()),
            'total_ledger_entries_scanned': sum(len(entries) for entries in self.ledger_data.values()),
            'total_inconsistencies_found': len(self.inconsistencies),
            'inconsistencies': self.inconsistencies
        }
        
        with open(output_file, 'w') as f:
            json.dump(discovery_ledger, f, indent=2)
        
        print(f"\n✓ Discovery ledger exported to: {output_file}")
        print(f"  Size: {len(self.inconsistencies)} entries")


if __name__ == '__main__':
    # Find ledger directory (current directory contains ALL ledgers)
    ledger_path = os.path.dirname(__file__)

    # Run scan
    scanner = InconsistencyScanner(ledger_path)
    count = scanner.scan()
    scanner.report()
    
    # Export findings
    output_file = os.path.join(os.path.dirname(__file__), 'ledger_discovery_inconsistencies.json')
    scanner.export_to_discovery_ledger(output_file)
    
    print(f"\n✓ Scan complete. Found {count} inconsistencies.")
    print(f"✓ Ready for human participation (voting phase)")
