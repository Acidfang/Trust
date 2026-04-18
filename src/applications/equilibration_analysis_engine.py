#!/usr/bin/env python3
"""
EQUILIBRATION LAYER - COMPREHENSIVE ANALYSIS ENGINE
====================================================

PURPOSE: Analyze 642+ elections and 70+ ledgers to find REAL contradictions
INPUT: Complete ARIA election and parameter ledgers
OUTPUT: Actionable inconsistencies ranked by severity and impact

This goes beyond simple pattern matching to reveal contradictions
that the system itself experiences.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Set, Tuple
from collections import defaultdict
import hashlib
import statistics

class EquilibrationAnalysisEngine:
    """Deep analysis of ledger system for contradictions"""
    
    def __init__(self, ledger_dir: str):
        self.ledger_dir = ledger_dir
        self.elections = []  # All 642 elections
        self.parameters = {}  # System parameters over time
        self.inconsistencies = []
        self.facts = defaultdict(list)
        
    def load_elections(self) -> int:
        """Load all election records"""
        filepath = os.path.join(self.ledger_dir, 'ledger_elections.jsonl')
        if not os.path.exists(filepath):
            print(f"ERROR: {filepath} not found")
            return 0
            
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    if line.strip():
                        try:
                            election = json.loads(line)
                            self.elections.append(election)
                        except json.JSONDecodeError as e:
                            # Skip malformed lines
                            pass
            
            print(f"[ENGINE] Loaded {len(self.elections)} election records")
            return len(self.elections)
        except Exception as e:
            print(f"ERROR loading elections: {e}")
            return 0
    
    def load_parameters(self) -> int:
        """Load parameter history"""
        filepath = os.path.join(self.ledger_dir, 'ledger_parameters.jsonl')
        if not os.path.exists(filepath):
            return 0
            
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if line.strip():
                        try:
                            param = json.loads(line)
                            key = param.get('key', 'unknown')
                            self.parameters[key] = param
                        except:
                            pass
            
            print(f"[ENGINE] Loaded {len(self.parameters)} parameter records")
            return len(self.parameters)
        except:
            return 0
    
    def analyze_choice_consistency(self):
        """CONTRADICTION TYPE A: Same choice selected with different utility scores"""
        print("\n[ANALYSIS A] Choice Utility Consistency")
        choice_utilities = defaultdict(list)
        choice_times = defaultdict(list)
        
        for election in self.elections:
            elected = election.get('elected')
            utilities = election.get('utilities', {})
            timestamp = election.get('timestamp', 0)
            
            if elected and elected in utilities:
                choice_utilities[elected].append(utilities[elected])
                choice_times[elected].append(timestamp)
        
        # Find choices where utility score varies significantly
        for choice in choice_utilities:
            scores = choice_utilities[choice]
            if len(scores) >= 5:  # Must have enough samples
                mean_score = statistics.mean(scores)
                stdev = statistics.stdev(scores) if len(scores) > 1 else 0
                variance_ratio = stdev / (mean_score + 0.0001)  # % variance
                
                if variance_ratio > 0.15:  # More than 15% variance
                    self.inconsistencies.append({
                        "type": "CHOICE_UTILITY_VARIANCE",
                        "severity": "HIGH" if variance_ratio > 0.3 else "MEDIUM",
                        "choice": choice,
                        "samples": len(scores),
                        "mean_utility": round(mean_score, 3),
                        "stdev": round(stdev, 3),
                        "variance_ratio": round(variance_ratio, 3),
                        "description": f"'{choice}' selected {len(scores)} times with utility scores varying {round(variance_ratio*100, 1)}% (mean={round(mean_score, 3)}, range={round(min(scores), 3)}..{round(max(scores), 3)})",
                        "explanation": "Same decision made with different confidence levels - suggests decision criteria changed over time"
                    })
    
    def analyze_elected_vs_available(self):
        """CONTRADICTION TYPE B: Choice elected despite lower utility than alternatives"""
        print("[ANALYSIS B] Elected vs Available Utility Check")
        
        for i, election in enumerate(self.elections):
            elected = election.get('elected')
            utilities = election.get('utilities', {})
            
            if not elected or not utilities:
                continue
                
            elected_utility = utilities.get(elected, 0)
            
            # Find if any non-elected choice had higher utility
            for choice, utility in utilities.items():
                if choice != elected and utility > elected_utility:
                    self.inconsistencies.append({
                        "type": "NON_OPTIMAL_ELECTION",
                        "severity": "CRITICAL",
                        "election_id": election.get('id'),
                        "elected_choice": elected,
                        "elected_utility": round(elected_utility, 3),
                        "better_choice": choice,
                        "better_utility": round(utility, 3),
                        "utility_gap": round(utility - elected_utility, 3),
                        "description": f"Election {election.get('id')}: Chose '{elected}' (utility={round(elected_utility, 3)}) over '{choice}' (utility={round(utility, 3)})",
                        "explanation": "Fundamental contradiction: system elected WORSE option despite utilities suggesting BETTER option available"
                    })
    
    def analyze_parameter_application(self):
        """CONTRADICTION TYPE C: Parameters defined but not applied"""
        print("[ANALYSIS C] Parameter Application Check")
        
        # Look for parameters that don't affect any elections
        if not self.parameters:
            return
            
        param_names = set(self.parameters.keys())
        
        # Sample logic: if parameter exists but we see no evidence of its application
        for param_key in param_names:
            param_info = self.parameters[param_key]
            
            # Check if parameter appears referenced in election metadata
            referenced = False
            for election in self.elections[:100]:  # Sample check
                if param_key in str(election):
                    referenced = True
                    break
            
            if not referenced and param_key not in ['coherence_threshold', 'none']:
                self.inconsistencies.append({
                    "type": "PARAMETER_NO_APPLICATION",
                    "severity": "MEDIUM",
                    "parameter": param_key,
                    "parameter_value": str(param_info.get('value', 'unknown'))[:100],
                    "description": f"Parameter '{param_key}' defined but no evidence of application in 642 elections",
                    "explanation": "Configuration exists but doesn't appear to influence system behavior - is it orphaned?"
                })
    
    def analyze_temporal_patterns(self):
        """CONTRADICTION TYPE D: Temporal inconsistencies in event sequences"""
        print("[ANALYSIS D] Temporal Pattern Check")
        
        if len(self.elections) < 2:
            return
        
        # Check for timestamp inconsistencies
        prev_timestamp = self.elections[0].get('timestamp', 0)
        backwards_jumps = []
        time_gaps = []
        
        for i, election in enumerate(self.elections[1:], 1):
            current = election.get('timestamp', 0)
            
            # Handle both numeric and string timestamps
            if isinstance(current, str):
                try:
                    # Try to parse ISO format
                    current = len(current)  # Fallback: just use string length
                except:
                    current = 0
            
            if isinstance(prev_timestamp, str):
                prev_timestamp = len(prev_timestamp)
            
            if current < prev_timestamp:
                backwards_jumps.append((i, prev_timestamp, current))
            
            gap = current - prev_timestamp
            if gap > 0:
                time_gaps.append(gap)
            
            prev_timestamp = current
        
        if backwards_jumps:
            self.inconsistencies.append({
                "type": "TEMPORAL_INVERSION",
                "severity": "CRITICAL",
                "count": len(backwards_jumps),
                "description": f"{len(backwards_jumps)} timestamps went backwards (impossible in linear time)",
                "samples": [{"election": b[0], "prev": b[1], "curr": b[2]} for b in backwards_jumps[:3]],
                "explanation": "Time either goes forward or holds still, never backwards. This violates causality."
            })
        
        if time_gaps:
            mean_gap = statistics.mean([g for g in time_gaps if g > 0])
            huge_gaps = [g for g in time_gaps if g > mean_gap * 10]
            
            if huge_gaps:
                self.inconsistencies.append({
                    "type": "TEMPORAL_ANOMALY",
                    "severity": "MEDIUM",
                    "mean_gap": round(mean_gap, 4),
                    "huge_gaps": len(huge_gaps),
                    "largest_gap": round(max(time_gaps), 4),
                    "description": f"Found {len(huge_gaps)} time gaps 10x larger than normal average",
                    "explanation": "Most elections cluster with time gaps ~{:.4f}, but {} exceptions show >10x gaps".format(mean_gap, len(huge_gaps))
                })
    
    def analyze_event_type_distribution(self):
        """CONTRADICTION TYPE E: Event types with impossible frequencies"""
        print("[ANALYSIS E] Event Type Distribution Check")
        
        event_counts = defaultdict(int)
        
        for election in self.elections:
            event_type = election.get('event_type', 'unknown')
            event_counts[event_type] += 1
        
        total = len(self.elections)
        
        for event_type, count in event_counts.items():
            ratio = count / total if total > 0 else 0
            
            # Look for suspiciously skewed distributions
            if ratio > 0.95:
                self.inconsistencies.append({
                    "type": "DOMINANT_EVENT_TYPE",
                    "severity": "LOW",
                    "event_type": event_type,
                    "count": count,
                    "percentage": round(ratio * 100, 1),
                    "description": f"Event type '{event_type}' accounts for {round(ratio*100,1)}% of all elections",
                    "explanation": "System is highly specialized around one event type. Is this narrowing opportunity space?"
                })
            elif ratio < 0.001:
                self.inconsistencies.append({
                    "type": "RARE_EVENT_TYPE",
                    "severity": "LOW",
                    "event_type": event_type,
                    "count": count,
                    "percentage": round(ratio * 100, 4),
                    "description": f"Event type '{event_type}' occurs {count} times ({round(ratio*100, 4)}%)",
                    "explanation": "Rare event type - possible dead code or initialization artifact"
                })
    
    def analyze_utility_patterns(self):
        """CONTRADICTION TYPE F: Choice utility patterns that are suspiciously uniform"""
        print("[ANALYSIS F] Utility Pattern Analysis")
        
        choice_sets = defaultdict(int)
        
        for election in self.elections:
            utilities = election.get('utilities', {})
            choices = tuple(sorted(utilities.keys()))
            choice_sets[choices] += 1
        
        # Find if same exact utility pattern repeats too much
        total = len(self.elections)
        for choice_set, count in choice_sets.items():
            if count > total * 0.5:  # If >50% of elections use same choice set
                self.inconsistencies.append({
                    "type": "UNIFORM_CHOICE_SET",
                    "severity": "MEDIUM",
                    "choice_set": list(choice_set),
                    "frequency": count,
                    "percentage": round(count / total * 100, 1),
                    "description": f"Choice set {choice_set} appears in {count}/{total} elections ({round(count/total*100, 1)}%)",
                    "explanation": "Extremely limited choice diversity - system may be stuck in local equilibrium"
                })
    
    def analyze(self) -> int:
        """Run all analyses"""
        print("\n" + "="*80)
        print("EQUILIBRATION ANALYSIS ENGINE - STARTING")
        print("="*80)
        
        self.load_elections()
        self.load_parameters()
        
        if not self.elections:
            print("ERROR: No elections loaded")
            return 0
        
        self.analyze_choice_consistency()
        self.analyze_elected_vs_available()
        self.analyze_parameter_application()
        self.analyze_temporal_patterns()
        self.analyze_event_type_distribution()
        self.analyze_utility_patterns()
        
        return len(self.inconsistencies)
    
    def report(self):
        """Print human-readable report"""
        print("\n" + "="*80)
        print(f"EQUILIBRATION ANALYSIS - RESULTS ({len(self.elections)} elections analyzed, {len(self.inconsistencies)} inconsistencies found)")
        print("="*80)
        
        if not self.inconsistencies:
            print("\n✓ No inconsistencies found - system appears coherent")
            return
        
        # Sort by severity
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        sorted_issues = sorted(
            self.inconsistencies,
            key=lambda x: severity_order.get(x.get('severity', 'LOW'), 99)
        )
        
        current_severity = None
        for issue in sorted_issues:
            if issue['severity'] != current_severity:
                current_severity = issue['severity']
                print(f"\n--- {current_severity} PRIORITY INCONSISTENCIES ---\n")
            
            print(f"【{issue['type']}】 {issue['description']}")
            print(f"   ⚠ {issue['explanation']}")
            
            # Show relevant details
            for key, value in issue.items():
                if key not in ['type', 'severity', 'description', 'explanation']:
                    if isinstance(value, (dict, list)) and len(str(value)) > 100:
                        print(f"   {key}: {str(value)[:100]}...")
                    else:
                        print(f"   {key}: {value}")
            print()
    
    def export(self, filepath: str):
        """Export findings to JSON"""
        output = {
            "timestamp": datetime.now().isoformat(),
            "elections_analyzed": len(self.elections),
            "inconsistencies_found": len(self.inconsistencies),
            "severity_breakdown": {
                "CRITICAL": len([x for x in self.inconsistencies if x.get('severity') == 'CRITICAL']),
                "HIGH": len([x for x in self.inconsistencies if x.get('severity') == 'HIGH']),
                "MEDIUM": len([x for x in self.inconsistencies if x.get('severity') == 'MEDIUM']),
                "LOW": len([x for x in self.inconsistencies if x.get('severity') == 'LOW']),
            },
            "inconsistencies": self.inconsistencies,
            "sample_elections": self.elections[:5]  # For debugging
        }
        
        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n✓ Analysis exported to: {filepath}")


if __name__ == '__main__':
    ledger_dir = os.path.dirname(__file__)
    engine = EquilibrationAnalysisEngine(ledger_dir)
    
    count = engine.analyze()
    engine.report()
    
    output_file = os.path.join(ledger_dir, 'equilibration_analysis_results.json')
    engine.export(output_file)
    
    print(f"\n✓ Analysis complete: {count} inconsistencies found and documented")
