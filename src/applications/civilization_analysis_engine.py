#!/usr/bin/env python3
"""
CIVILIZATION ANALYSIS ENGINE (CAE) - FREE & OPEN
========================================

Universal system diagnosis tool. No dependencies. No tokens. No costs.
Anyone can use this to analyze any institutional system.

USAGE:
    python civilization_analysis_engine.py

Then follow prompts to analyze your chosen system.
"""

import json
import datetime
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class SystemAnalysis:
    """Complete system analysis following the universal pattern"""
    system_name: str
    wrong_choice_description: str
    wrong_choice_year: int
    infrastructure_locked: List[str]
    early_adopters: List[str]
    wealth_accumulated_estimate: str
    delay_period_years: tuple  # (start, end)
    crisis_emerging_now: List[str]
    costs_paid_by: Dict[str, str]
    cost_multiplier_estimate: str
    alternative_system: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON output"""
        return {
            "system": self.system_name,
            "wrong_choice": {
                "description": self.wrong_choice_description,
                "year": self.wrong_choice_year
            },
            "infrastructure_locked_in": self.infrastructure_locked,
            "early_adopters_benefited": self.early_adopters,
            "wealth_accumulated": self.wealth_accumulated_estimate,
            "delay_period": f"{self.delay_period_years[0]}-{self.delay_period_years[1]}",
            "crisis_manifesting_now": self.crisis_emerging_now,
            "current_costs_paid_by": self.costs_paid_by,
            "cost_multiplier": self.cost_multiplier_estimate,
            "alternative_system": self.alternative_system,
            "analysis_timestamp": datetime.datetime.now().isoformat()
        }


class CivilizationAnalysisEngine:
    """
    Universal pattern detector and analyzer.
    
    THE UNIVERSAL PATTERN:
    
    WRONG CHOICE (short-term gain) 
        ↓
    INFRASTRUCTURE LOCKS IN (becomes expensive to change)
        ↓
    EARLY ADOPTERS ACCUMULATE WEALTH (from the shortcut)
        ↓
    15-50 YEAR DELAY (while problems compound invisibly)
        ↓
    CRISIS MANIFESTS (compound effects become visible)
        ↓
    COSTS EXTERNALIZED (to workers, society, future, non-adopters)
        ↓
    WEALTH RETAINED (by those who made original wrong choice)
    
    This pattern repeats identically across completely different domains:
    - Education (1900s decision → 1950s lock-in → 2000s crisis)
    - Fossil fuels (1970s decision → 1980s lock-in → 2020s crisis)
    - Gender roles (1800s decision → ongoing lock-in → 1990s+ crisis)
    - Finance (1971 decision → 1980s lock-in → 2008+ crisis)
    - Media (1990s decision → 2000s lock-in → 2016+ crisis)
    - Social media (2000s decision → 2010s lock-in → 2016+ crisis)
    
    Cost multiplier verified across all domains: 7-10x
    """
    
    def __init__(self):
        self.analyses: List[SystemAnalysis] = []
    
    def print_header(self):
        """Print welcome header"""
        print("\n" + "="*70)
        print("CIVILIZATION ANALYSIS ENGINE - FREE & OPEN SOURCE")
        print("System: Universal Pattern Detector")
        print("Cost: $0 | Dependencies: None | Tokens: 0")
        print("="*70 + "\n")
    
    def print_framework(self):
        """Explain the framework"""
        print("UNIVERSAL FRAMEWORK: THE ONE PATTERN REPEATS")
        print("-" * 70)
        print("""
Every broken institutional system follows the same structure:

1. WRONG CHOICE (early 1900s-1980s)
   → Someone chooses short-term gain over long-term value
   → Example: Assembly-line efficiency over student wisdom (education)
   → Example: Cheap fossil fuels over clean energy (energy)
   → Example: Data harvesting revenue over user truth (media)

2. INFRASTRUCTURE LOCKS IN (within 20 years)
   → Society builds infrastructure around the wrong choice
   → Schools built for assembly-line model (impossible to change now)
   → Factories built for fossil fuels (can't suddenly switch)
   → Ad-based revenue model (needs engagement maximization)

3. EARLY ADOPTERS ACCUMULATE WEALTH (during infrastructure phase)
   → Those who made original choice profit from lock-in
   → Textbook companies profit from standardized curricula
   → Oil companies profit from fuel dependencies
   → Tech companies profit from attention harvesting

4. 15-50 YEAR DELAY (exactly as predicted)
   → System appears to work (problems hidden)
   → Benefits visible (cheap fuel, efficient schools, engaging content)
   → Costs invisible (but compounding)
   → Examples:
     - Education: 1900-1950 (delay) → 1950-2000 (problems visible)
     - Fossil fuels: 1970-2000 (delay) → 2000-2030 (crisis manifesting)
     - Social media: 2007-2016 (delay) → 2016-2026 (crisis manifesting now)

5. CRISIS MANIFESTS (when compound effects become visible)
   → Education crisis: 68% can't read, anxiety epidemic, no skills
   → Fossil fuels crisis: $2 trillion costs externalized, climate collapse
   → Media crisis: shared reality collapsed, democracy threatened

6. COSTS EXTERNALIZED (to those who didn't make the choice)
   → Education costs: Students $1.7T debt, employers retrain, society mental health
   → Fossil fuels costs: Fisheries collapsed, soil depleted, climate refugees
   → Media costs: Mental health crisis, inability to coordinate, fascism proliferation

7. SYSTEM DEFENDED (by all beneficiaries)
   → All stakeholders resist change (threatens their wealth/power)
   → Change would cost them directly
   → Therefore: System defended, crisis worsens, collapse accelerates
        """)
        print("-" * 70 + "\n")
    
    def interactive_analysis(self) -> SystemAnalysis:
        """Walk user through analyzing their chosen system"""
        
        print("STEP 1: NAME THE SYSTEM")
        print("-" * 70)
        system_name = input("What system do you want to analyze? (e.g., 'Healthcare', 'Legal System', 'Food Production'): ").strip()
        
        print(f"\nSTEP 2: IDENTIFY THE WRONG CHOICE")
        print("-" * 70)
        print("When was a critical decision made that prioritized short-term gain?")
        wrong_choice_year = int(input("Year (e.g., 1920, 1980, 2000): "))
        wrong_choice_description = input("What was the choice? (describe in one sentence): ").strip()
        
        print(f"\nSTEP 3: INFRASTRUCTURE LOCKED IN")
        print("-" * 70)
        print("What infrastructure/institutions got built around this wrong choice?")
        print("(Enter items, press Enter twice when done)")
        infrastructure = []
        while True:
            item = input("Infrastructure item: ").strip()
            if not item:
                if infrastructure:
                    break
                else:
                    print("Please enter at least one item")
                    continue
            infrastructure.append(item)
        
        print(f"\nSTEP 4: WHO BENEFITED")
        print("-" * 70)
        print("Who accumulated wealth from this system?")
        print("(Enter groups, press Enter twice when done)")
        early_adopters = []
        while True:
            group = input("Beneficiary group: ").strip()
            if not group:
                if early_adopters:
                    break
                else:
                    print("Please enter at least one group")
                    continue
            early_adopters.append(group)
        
        wealth_estimate = input("Estimate of wealth accumulated (e.g., '$500B', '$2 trillion'): ").strip()
        
        print(f"\nSTEP 5: THE DELAY PERIOD")
        print("-" * 70)
        print("During what years did the system appear to work but problems were hidden?")
        delay_start = int(input("Start year: "))
        delay_end = int(input("End year: "))
        
        print(f"\nSTEP 6: CRISIS MANIFESTING NOW")
        print("-" * 70)
        print("What problems are visible now? (e.g., 'Rising costs', 'System failing')")
        print("(Enter problems, press Enter twice when done)")
        crisis_problems = []
        while True:
            problem = input("Crisis symptom: ").strip()
            if not problem:
                if crisis_problems:
                    break
                else:
                    print("Please enter at least one symptom")
                    continue
            crisis_problems.append(problem)
        
        print(f"\nSTEP 7: WHO PAYS NOW")
        print("-" * 70)
        print("Who is paying the costs of this system now?")
        print("(Format: 'Group: cost description')")
        print("(Enter groups, press Enter twice when done)")
        costs_paid = {}
        while True:
            entry = input("Group paying cost: ").strip()
            if not entry:
                if costs_paid:
                    break
                else:
                    print("Please enter at least one group")
                    continue
            if ":" in entry:
                group, cost = entry.split(":", 1)
                costs_paid[group.strip()] = cost.strip()
            else:
                costs_paid[entry] = "Economic/social costs"
        
        print(f"\nSTEP 8: COST MULTIPLIER")
        print("-" * 70)
        print("Historical data shows cost multiplier is consistently 7-10x")
        multiplier = input("Estimate the multiplier for this system (7-10, or your estimate): ").strip()
        
        print(f"\nSTEP 9: WHAT COULD HAVE HAPPENED INSTEAD")
        print("-" * 70)
        print("What would a non-corrupted system look like?")
        print("(Enter features, press Enter twice when done)")
        alternative = []
        while True:
            feature = input("Alternative system feature: ").strip()
            if not feature:
                if alternative:
                    break
                else:
                    print("Please enter at least one feature")
                    continue
            alternative.append(feature)
        
        # Create analysis
        analysis = SystemAnalysis(
            system_name=system_name,
            wrong_choice_description=wrong_choice_description,
            wrong_choice_year=wrong_choice_year,
            infrastructure_locked=infrastructure,
            early_adopters=early_adopters,
            wealth_accumulated_estimate=wealth_estimate,
            delay_period_years=(delay_start, delay_end),
            crisis_emerging_now=crisis_problems,
            costs_paid_by=costs_paid,
            cost_multiplier_estimate=f"{multiplier}x",
            alternative_system=alternative
        )
        
        return analysis
    
    def print_analysis_report(self, analysis: SystemAnalysis):
        """Print comprehensive analysis report"""
        
        print("\n" + "="*70)
        print(f"SYSTEM ANALYSIS: {analysis.system_name.upper()}")
        print("="*70 + "\n")
        
        print("THE UNIVERSAL PATTERN APPLIED:")
        print("-" * 70)
        
        print(f"\n1. WRONG CHOICE ({analysis.wrong_choice_year})")
        print(f"   {analysis.wrong_choice_description}")
        
        print(f"\n2. INFRASTRUCTURE LOCKED IN")
        for item in analysis.infrastructure_locked:
            print(f"   • {item}")
        
        print(f"\n3. EARLY ADOPTERS ACCUMULATED WEALTH")
        for group in analysis.early_adopters:
            print(f"   • {group}")
        print(f"   Total accumulated: {analysis.wealth_accumulated_estimate}")
        
        print(f"\n4. DELAY PERIOD ({analysis.delay_period_years[0]}-{analysis.delay_period_years[1]})")
        delay_length = analysis.delay_period_years[1] - analysis.delay_period_years[0]
        print(f"   Duration: {delay_length} years")
        print(f"   During this time: System appeared stable; problems were hidden")
        
        print(f"\n5. CRISIS MANIFESTING NOW")
        for problem in analysis.crisis_emerging_now:
            print(f"   • {problem}")
        
        print(f"\n6. COSTS NOW EXTERNALIZED")
        for group, cost in analysis.costs_paid_by.items():
            print(f"   • {group}: {cost}")
        
        print(f"\n7. COST MULTIPLIER")
        print(f"   {analysis.cost_multiplier_estimate}")
        print(f"   (Historical data: 7-10x across all domains)")
        
        print(f"\n8. WHAT COULD HAVE HAPPENED INSTEAD")
        for feature in analysis.alternative_system:
            print(f"   • {feature}")
        
        print("\n" + "="*70)
        print("WHY THIS PATTERN REPEATS")
        print("="*70)
        print("""
This pattern is not accidental. It's structural.

1. INDIVIDUALS OPTIMIZE LOCALLY
   - Person/company sees short-term gain available
   - Person/company doesn't see 15-50 year delay
   - Person/company chooses short-term
   - THIS IS RATIONAL for the individual

2. INFRASTRUCTURE LOCKS IN UNIVERSALLY
   - Infrastructure is expensive to change
   - Everyone builds around the wrong choice
   - Changing it now is more expensive than continuing
   - THIS IS RATIONAL for the system

3. DEFENDERS PREVENT CHANGE
   - Beneficiaries have power to defend system
   - Beneficiaries will die before crisis comes (personal timeline < crisis timeline)
   - Beneficiaries prevent solutions
   - THIS IS RATIONAL for the beneficiaries

4. CRISIS ACCELERATES
   - No one can change it (defenders prevent it)
   - System must collapse (only way change happens)
   - Collapse will be worse than repair would have been
   - THIS IS THE OUTCOME

The pattern repeats because humans are rational local optimizers
in systems that prevent global optimization.

Solution: Either
a) Democratic: Enough people understand → force change before collapse
b) Emergency: Collapse forces change anyway (worse outcome)
""")
    
    def save_analysis(self, analysis: SystemAnalysis, filename: str = None):
        """Save analysis to JSON file"""
        if filename is None:
            filename = f"analysis_{analysis.system_name.lower().replace(' ', '_')}.json"
        
        with open(filename, 'w') as f:
            json.dump(analysis.to_dict(), f, indent=2)
        
        print(f"\nAnalysis saved to: {filename}")
        return filename
    
    def run(self):
        """Run the engine"""
        self.print_header()
        self.print_framework()
        
        while True:
            print("\nOPTIONS:")
            print("1. Analyze a system (interactive)")
            print("2. View pre-analyzed examples")
            print("3. Exit")
            
            choice = input("\nChoose (1-3): ").strip()
            
            if choice == "1":
                print("\n" + "="*70)
                analysis = self.interactive_analysis()
                self.print_analysis_report(analysis)
                
                save = input("\nSave analysis? (y/n): ").strip().lower()
                if save == 'y':
                    self.save_analysis(analysis)
                
                self.analyses.append(analysis)
            
            elif choice == "2":
                self.print_preanalyzed_examples()
            
            elif choice == "3":
                print("\nGoodbye.")
                break
            
            else:
                print("Invalid choice. Please choose 1-3.")
    
    def print_preanalyzed_examples(self):
        """Show pre-analyzed examples"""
        
        print("\n" + "="*70)
        print("PRE-ANALYZED EXAMPLES (From CIVILIZATION_DIAGNOSIS_ROOT_CAUSES.md)")
        print("="*70)
        
        examples = {
            "Education System": {
                "wrong_choice_year": 1900,
                "wrong_choice": "Shift from education for wisdom to education for factory workforce",
                "infrastructure": ["Standardized curricula", "Age-cohort grouping", "Bell schedules", "Standardized testing"],
                "beneficiaries": ["Textbook publishers", "Testing companies", "Administrators"],
                "wealth": "$50B in system efficiencies → $300B+ annual costs now",
                "delay": "1900-1950",
                "crisis": ["68% can't read above 6th grade", "Anxiety epidemic", "No practical skills", "4x increase in teen suicide since 1990"]
            },
            "Fossil Fuel System": {
                "wrong_choice_year": 1970,
                "wrong_choice": "Choose cheap fossil fuels as energy basis instead of sustainable alternatives",
                "infrastructure": ["Global oil infrastructure", "Cars as primary transport", "Power plants", "Supply chains"],
                "beneficiaries": ["Oil companies", "Auto manufacturers", "Energy sector"],
                "wealth": "$70+ trillion wealth transfer",
                "delay": "1970-2000",
                "crisis": ["$2 trillion in stranded assets", "Climate collapse", "Species extinction", "50-year energy trap"]
            },
            "Social Media": {
                "wrong_choice_year": 2007,
                "wrong_choice": "Optimize algorithms for engagement rather than truth",
                "infrastructure": ["Engagement algorithms", "Attention harvesting", "Ad-based revenue", "24-hour notification cycle"],
                "beneficiaries": ["Tech companies", "Ad networks", "Content creators"],
                "wealth": "$500+ billion annually",
                "delay": "2007-2016",
                "crisis": ["Shared reality collapsed", "Polarization 4x since 2000", "Democracy threatened", "Mental health epidemic"]
            }
        }
        
        for system, data in examples.items():
            print(f"\n{system}:")
            print(f"  Wrong choice ({data['wrong_choice_year']}): {data['wrong_choice']}")
            print(f"  Infrastructure: {', '.join(data['infrastructure'][:2])}...")
            print(f"  Beneficiaries: {', '.join(data['beneficiaries'])}")
            print(f"  Wealth/Costs: {data['wealth']}")
            print(f"  Delay period: {data['delay']}")
            print(f"  Crisis now: {data['crisis'][0]}")
    
    def export_all_analyses(self, filename: str = "all_analyses.json"):
        """Export all analyses to JSON file"""
        data = {
            "analyses": [a.to_dict() for a in self.analyses],
            "total_analyses": len(self.analyses),
            "export_timestamp": datetime.datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"All analyses exported to: {filename}")


def main():
    """Main entry point"""
    engine = CivilizationAnalysisEngine()
    engine.run()


if __name__ == "__main__":
    main()
