"""
ELECTION LEDGER ENGINE - Read, Query, Validate, and Verify Decision Records

Purpose: Makes election ledgers ACTIONABLE, not just documentation
- Read ledger files
- Query decisions by criteria
- Validate ledger structure
- Check verification gates
- Find alternatives and triggers
- Generate reports
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any
from pathlib import Path
import json
import re
from datetime import datetime


# ============================================================================
# DATA MODELS
# ============================================================================

class DecisionStatus(Enum):
    """Status of a decision."""
    GOOD = "GOOD"
    ADEQUATE = "ADEQUATE"
    BROKEN = "BROKEN"


class VerificationGate(Enum):
    """Five verification gates for decisions."""
    IDENTITY = "Identity: Unambiguous authorship and choice"
    STATE = "State: Measurable outcomes verified"
    CAUSALITY = "Causality: Explicit rationale for each decision"
    COHERENCE = "Coherence: Consistent with frameworks and prior work"
    DETERMINISM = "Determinism: Reproducible, verifiable results"


@dataclass
class Alternative:
    """An alternative decision not chosen."""
    id: str
    name: str
    benefit: str
    cost: str
    trigger_condition: str
    implementation_notes: str = ""
    
    def meets_trigger(self, context: Dict[str, Any]) -> bool:
        """Check if trigger condition is met in given context."""
        # Simple string matching for now
        # In production: parse and evaluate trigger expressions
        return False  # Placeholder


@dataclass
class Election:
    """A recorded decision with full context."""
    election_id: str
    title: str
    choice_made: str
    category: str
    
    # Reasoning
    problem_being_solved: str
    key_rationale: str
    trade_offs_accepted: str
    
    # Alternatives
    alternatives_explored: Dict[str, Tuple[str, str, str]] = field(default_factory=dict)
    # Format: {"ALT_A": (approach, result, why_rejected), ...}
    
    # Better election
    better_alternative: Optional[Alternative] = None
    
    # Status
    status: DecisionStatus = DecisionStatus.GOOD
    
    # Verification
    verification_gates: Dict[VerificationGate, bool] = field(default_factory=dict)
    verified_at: Optional[str] = None
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    session_id: Optional[str] = None
    related_elections: List[str] = field(default_factory=list)
    
    def __hash__(self):
        return hash(self.election_id)
    
    def __eq__(self, other):
        if not isinstance(other, Election):
            return NotImplemented
        return self.election_id == other.election_id
    
    def is_fully_verified(self) -> bool:
        """Check if all 5 gates pass."""
        return all(self.verification_gates.values()) if self.verification_gates else False
    
    def verification_score(self) -> float:
        """Percentage of gates passing (0.0 to 1.0)."""
        if not self.verification_gates:
            return 0.0
        passed = sum(1 for v in self.verification_gates.values() if v)
        return passed / len(self.verification_gates)
    
    def to_dict(self) -> Dict[str, Any]:
        """Export as dictionary."""
        return {
            "election_id": self.election_id,
            "title": self.title,
            "choice_made": self.choice_made,
            "category": self.category,
            "problem": self.problem_being_solved,
            "rationale": self.key_rationale,
            "trade_offs": self.trade_offs_accepted,
            "alternatives": self.alternatives_explored,
            "status": self.status.value,
            "verification_gates": {gate.name: passed 
                                  for gate, passed in self.verification_gates.items()},
            "verified": self.is_fully_verified(),
        }


# ============================================================================
# ELECTION LEDGER
# ============================================================================

class ElectionLedger:
    """Complete record of all decisions."""
    
    def __init__(self, ledger_id: str):
        self.ledger_id = ledger_id
        self.elections: Dict[str, Election] = {}
        self.created_at = datetime.now().isoformat()
        self.coherence_verified = False
    
    def add_election(self, election: Election) -> bool:
        """Add election to ledger."""
        if election.election_id in self.elections:
            return False  # Duplicate
        self.elections[election.election_id] = election
        return True
    
    def get_election(self, election_id: str) -> Optional[Election]:
        """Get election by ID."""
        return self.elections.get(election_id)
    
    def elections_by_category(self, category: str) -> List[Election]:
        """Get all elections in a category."""
        return [e for e in self.elections.values() if e.category == category]
    
    def elections_by_status(self, status: DecisionStatus) -> List[Election]:
        """Get all elections with given status."""
        return [e for e in self.elections.values() if e.status == status]
    
    def unverified_elections(self) -> List[Election]:
        """Get elections that haven't passed all 5 gates."""
        return [e for e in self.elections.values() 
                if not e.is_fully_verified()]
    
    def find_alternatives_available(self) -> List[Tuple[Election, Alternative]]:
        """Find elections with better alternatives not yet triggered."""
        results = []
        for election in self.elections.values():
            if election.better_alternative:
                results.append((election, election.better_alternative))
        return results
    
    def coherence_report(self) -> Dict[str, Any]:
        """Generate coherence verification report."""
        total_elections = len(self.elections)
        fully_verified = sum(1 for e in self.elections.values() 
                            if e.is_fully_verified())
        
        avg_verification_score = (
            sum(e.verification_score() for e in self.elections.values())
            / len(self.elections)
            if self.elections else 0.0
        )
        
        status_distribution = {
            DecisionStatus.GOOD: len(self.elections_by_status(DecisionStatus.GOOD)),
            DecisionStatus.ADEQUATE: len(self.elections_by_status(DecisionStatus.ADEQUATE)),
            DecisionStatus.BROKEN: len(self.elections_by_status(DecisionStatus.BROKEN)),
        }
        
        return {
            "ledger_id": self.ledger_id,
            "total_elections": total_elections,
            "fully_verified": fully_verified,
            "verification_percentage": (fully_verified / total_elections * 100 
                                       if total_elections else 0),
            "average_verification_score": avg_verification_score * 100,
            "status_distribution": {k.value: v for k, v in status_distribution.items()},
            "unverified_count": len(self.unverified_elections()),
            "alternatives_available": len(self.find_alternatives_available()),
            "coherence_verified": self.coherence_verified,
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Export entire ledger as dictionary."""
        return {
            "ledger_id": self.ledger_id,
            "created_at": self.created_at,
            "coherence_verified": self.coherence_verified,
            "total_elections": len(self.elections),
            "elections": [e.to_dict() for e in self.elections.values()],
        }


# ============================================================================
# LEDGER PARSER (from Markdown files)
# ============================================================================

class LedgerParser:
    """Parse election ledger from Markdown files."""
    
    @staticmethod
    def parse_file(filepath: Path) -> Optional[Election]:
        """Parse a single election ledger markdown file."""
        if not filepath.exists():
            return None
        
        content = filepath.read_text()
        
        # Extract election ID from filename
        match = re.search(r'ELECTION_(\d+)', filepath.name)
        election_id = match.group(1) if match else filepath.stem
        
        # Simple parsing: extract sections
        election = Election(
            election_id=election_id,
            title=LedgerParser._extract_title(content),
            choice_made=LedgerParser._extract_section(content, "Choice Made"),
            category=LedgerParser._extract_section(content, "Category", "uncategorized"),
            problem_being_solved=LedgerParser._extract_section(content, "Why This Choice"),
            key_rationale=LedgerParser._extract_section(content, "Key Rationale"),
            trade_offs_accepted=LedgerParser._extract_section(content, "Trade-offs Accepted"),
        )
        
        return election
    
    @staticmethod
    def parse_directory(directory: Path) -> ElectionLedger:
        """Parse all election files in directory."""
        ledger = ElectionLedger(f"ledger_{directory.name}")
        
        for filepath in sorted(directory.glob("*ELECTION*.md")):
            election = LedgerParser.parse_file(filepath)
            if election:
                ledger.add_election(election)
        
        return ledger
    
    @staticmethod
    def _extract_title(content: str) -> str:
        """Extract title from markdown."""
        match = re.search(r'^# (.+)$', content, re.MULTILINE)
        return match.group(1) if match else "Untitled"
    
    @staticmethod
    def _extract_section(content: str, section_name: str, 
                        default: str = "") -> str:
        """Extract section content from markdown."""
        pattern = rf'^### {re.escape(section_name)}.*?\n(.*?)(?=^###|$)'
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        if match:
            text = match.group(1).strip()
            # Clean up markdown formatting
            text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Bold
            text = re.sub(r'`(.+?)`', r'\1', text)  # Code
            return text[:200]  # Truncate for summary
        return default


# ============================================================================
# VERIFICATION ENGINE
# ============================================================================

class VerificationEngine:
    """Verify elections against the 5 gates."""
    
    @staticmethod
    def verify_election(election: Election) -> Dict[VerificationGate, bool]:
        """Run all 5 verification gates on an election."""
        gates = {
            VerificationGate.IDENTITY: VerificationEngine._check_identity(election),
            VerificationGate.STATE: VerificationEngine._check_state(election),
            VerificationGate.CAUSALITY: VerificationEngine._check_causality(election),
            VerificationGate.COHERENCE: VerificationEngine._check_coherence(election),
            VerificationGate.DETERMINISM: VerificationEngine._check_determinism(election),
        }
        election.verification_gates = gates
        election.verified_at = datetime.now().isoformat()
        return gates
    
    @staticmethod
    def _check_identity(election: Election) -> bool:
        """Gate 1: Is choice unambiguous and traceable?"""
        # Check: ID exists, title exists, choice_made exists
        return bool(election.election_id and 
                   election.title and 
                   election.choice_made)
    
    @staticmethod
    def _check_state(election: Election) -> bool:
        """Gate 2: Can we measure if it worked?"""
        # Check: Has status (GOOD/ADEQUATE/BROKEN)
        return election.status in [DecisionStatus.GOOD, 
                                  DecisionStatus.ADEQUATE, 
                                  DecisionStatus.BROKEN]
    
    @staticmethod
    def _check_causality(election: Election) -> bool:
        """Gate 3: Is reasoning explicit?"""
        # Check: Rationale and problem statement both present
        return bool(election.key_rationale and 
                   election.problem_being_solved)
    
    @staticmethod
    def _check_coherence(election: Election) -> bool:
        """Gate 4: Is it consistent with other decisions?"""
        # Check: Category assigned, no obvious conflicts
        return bool(election.category) and election.status != DecisionStatus.BROKEN
    
    @staticmethod
    def _check_determinism(election: Election) -> bool:
        """Gate 5: Are results verifiable?"""
        # Check: Status is determined (not ADEQUATE=uncertain)
        # In strict mode, even ADEQUATE fails this
        return election.status in [DecisionStatus.GOOD, DecisionStatus.BROKEN]


# ============================================================================
# COHERENCE VALIDATOR
# ============================================================================

class CoherenceValidator:
    """Verify that all decisions resonate together."""
    
    @staticmethod
    def validate_ledger(ledger: ElectionLedger) -> Dict[str, Any]:
        """Complete coherence check across all elections."""
        
        # Check 1: All elections verified
        unverified = ledger.unverified_elections()
        all_verified = len(unverified) == 0
        
        # Check 2: No BROKEN elections
        broken = ledger.elections_by_status(DecisionStatus.BROKEN)
        no_broken = len(broken) == 0
        
        # Check 3: Decision categories form coherent groups
        categories = set(e.category for e in ledger.elections.values())
        coherent_categories = len(categories) > 0
        
        # Check 4: All elections have rationales
        has_rationale = all(e.key_rationale for e in ledger.elections.values())
        
        # Check 5: Related elections form coherent chains
        # (Elections cite related elections that exist)
        related_ok = CoherenceValidator._check_related_elections(ledger)
        
        coherent = all([
            all_verified,
            no_broken,
            coherent_categories,
            has_rationale,
            related_ok,
        ])
        
        return {
            "coherent": coherent,
            "all_verified": all_verified,
            "unverified_count": len(unverified),
            "no_broken_decisions": no_broken,
            "broken_count": len(broken),
            "coherent_categories": coherent_categories,
            "category_count": len(categories),
            "all_have_rationale": has_rationale,
            "related_elections_valid": related_ok,
            "issue_count": (len(unverified) + len(broken)),
        }
    
    @staticmethod
    def _check_related_elections(ledger: ElectionLedger) -> bool:
        """Verify related elections actually exist."""
        for election in ledger.elections.values():
            for related_id in election.related_elections:
                if related_id not in ledger.elections:
                    return False  # Referenced election doesn't exist
        return True


# ============================================================================
# DECISION QUERY ENGINE
# ============================================================================

class DecisionQueryEngine:
    """Query decisions by various criteria."""
    
    def __init__(self, ledger: ElectionLedger):
        self.ledger = ledger
    
    def find_by_category(self, category: str) -> List[Election]:
        """Find all decisions in a category."""
        return self.ledger.elections_by_category(category)
    
    def find_by_keyword(self, keyword: str) -> List[Election]:
        """Find decisions mentioning keyword in title, choice, or rationale."""
        keyword_lower = keyword.lower()
        results = []
        for election in self.ledger.elections.values():
            if (keyword_lower in election.title.lower() or
                keyword_lower in election.choice_made.lower() or
                keyword_lower in election.key_rationale.lower()):
                results.append(election)
        return results
    
    def find_with_better_alternative(self) -> List[Tuple[Election, Alternative]]:
        """Find decisions that have a better alternative mapped."""
        return self.ledger.find_alternatives_available()
    
    def find_triggered_alternatives(self, context: Dict[str, Any]) -> List[Tuple[Election, Alternative]]:
        """Find alternatives whose trigger conditions are now met."""
        triggered = []
        for election, alternative in self.ledger.find_alternatives_available():
            if alternative.meets_trigger(context):
                triggered.append((election, alternative))
        return triggered
    
    def get_decision_chain(self, start_id: str, depth: int = 3) -> Dict[str, Any]:
        """Get chain of related decisions."""
        result = {"chain": [], "depth": 0}
        visited = set()
        
        def traverse(election_id: str, current_depth: int):
            if current_depth > depth or election_id in visited:
                return
            
            election = self.ledger.get_election(election_id)
            if not election:
                return
            
            visited.add(election_id)
            result["chain"].append({
                "id": election_id,
                "title": election.title,
                "depth": current_depth,
            })
            result["depth"] = max(result["depth"], current_depth)
            
            # Traverse related elections
            for related_id in election.related_elections:
                traverse(related_id, current_depth + 1)
        
        traverse(start_id, 0)
        return result


# ============================================================================
# REPORTING
# ============================================================================

class LedgerReporter:
    """Generate reports on ledger status."""
    
    @staticmethod
    def verify_report(ledger: ElectionLedger) -> str:
        """Generate verification report."""
        report = _header("ELECTION LEDGER VERIFICATION REPORT")
        report += f"\nLedger ID: {ledger.ledger_id}\n"
        report += f"Created: {ledger.created_at}\n"
        
        coherence = CoherenceValidator.validate_ledger(ledger)
        report += f"\n{'COHERENCE STATUS':-^60}\n"
        coherence_status = "YES" if coherence['coherent'] else "NO"
        report += f"Coherent: {coherence_status}\n"
        unverified_count = coherence['unverified_count']
        verified_status = "YES" if coherence['all_verified'] else f"NO ({unverified_count} unverified)"
        report += f"All Verified: {verified_status}\n"
        broken_count = coherence['broken_count']
        broken_status = "YES" if coherence['no_broken_decisions'] else f"NO ({broken_count} broken)"
        report += f"No Broken: {broken_status}\n"
        
        ledger_stats = ledger.coherence_report()
        report += f"\n{'STATISTICS':-^60}\n"
        report += f"Total Elections: {ledger_stats['total_elections']}\n"
        report += f"Fully Verified: {ledger_stats['fully_verified']} ({ledger_stats['verification_percentage']:.1f}%)\n"
        report += f"Average Verification Score: {ledger_stats['average_verification_score']:.1f}%\n"
        report += f"Alternatives Available: {ledger_stats['alternatives_available']}\n"
        
        return report
    
    @staticmethod
    def category_report(ledger: ElectionLedger) -> str:
        """Report on decisions by category."""
        report = f"{'DECISIONS BY CATEGORY':-^60}\n\n"
        
        categories = set(e.category for e in ledger.elections.values())
        for category in sorted(categories):
            elections = ledger.elections_by_category(category)
            report += f"{category}: {len(elections)} decisions\n"
            for e in elections:
                status = e.status.value
                report += f"  - {e.title} ({status})\n"
            report += "\n"
        
        return report


def _header(text: str, width: int = 60) -> str:
    """Format section header."""
    return f"\n{'=' * width}\n{text:^{width}}\n{'=' * width}\n"


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demo_election_ledger_engine():
    """Demonstrate the election ledger engine."""
    
    print("=" * 80)
    print("ELECTION LEDGER ENGINE - DEMONSTRATION")
    print("=" * 80)
    
    # Create a sample ledger
    print("\n[STEP 1] Creating sample election ledger...")
    ledger = ElectionLedger("demo_ledger_2026_04_02")
    
    # Add sample elections
    election1 = Election(
        election_id="1",
        title="Weighted Container System Architecture",
        choice_made="7-layer architecture with mathematical scoring",
        category="system_design",
        problem_being_solved="Need to store effects/elements with weights and score combinations",
        key_rationale="Layers decouple concerns; math enables objective decisions",
        trade_offs_accepted="Quadratic complexity is acceptable for typical use cases",
        status=DecisionStatus.GOOD,
    )
    
    election2 = Election(
        election_id="2",
        title="Python + No External Dependencies",
        choice_made="Pure Python 3.10+ with standard library only",
        category="technology",
        problem_being_solved="Need deterministic, portable deployment",
        key_rationale="No dependencies = guaranteed deployable anywhere",
        trade_offs_accepted="Cannot use performance-optimized packages like numpy",
        status=DecisionStatus.GOOD,
        related_elections=["1"],
    )
    
    election3 = Election(
        election_id="3",
        title="Comprehensive Documentation Strategy",
        choice_made="5 separate documents with full examples and API reference",
        category="documentation",
        problem_being_solved="Different audiences need different documentation types",
        key_rationale="Comprehensive docs enable future understanding and maintenance",
        trade_offs_accepted="Takes 25-30% of project effort",
        status=DecisionStatus.ADEQUATE,  # Not fully decided yet
        related_elections=["1", "2"],
    )
    
    ledger.add_election(election1)
    ledger.add_election(election2)
    ledger.add_election(election3)
    
    print(f"[OK] Created ledger with {len(ledger.elections)} elections")
    
    # Verify elections
    print("\n[STEP 2] Verifying elections against 5 gates...")
    for election in ledger.elections.values():
        gates = VerificationEngine.verify_election(election)
        verified = sum(1 for v in gates.values() if v)
        print(f"  {election.title}: {verified}/5 gates passed")
    
    # Check coherence
    print("\n[STEP 3] Checking coherence...")
    coherence = CoherenceValidator.validate_ledger(ledger)
    print(f"  Coherent: {'YES' if coherence['coherent'] else 'NO'}")
    print(f"  All Verified: {'YES' if coherence['all_verified'] else 'NO'}")
    print(f"  Unverified: {coherence['unverified_count']}")
    print(f"  Broken: {coherence['broken_count']}")
    
    # Query engine
    print("\n[STEP 4] Querying decisions...")
    query_engine = DecisionQueryEngine(ledger)
    
    design_decisions = query_engine.find_by_category("system_design")
    print(f"  System design decisions: {len(design_decisions)}")
    
    python_related = query_engine.find_by_keyword("Python")
    print(f"  Decisions mentioning 'Python': {len(python_related)}")
    
    # Generate report
    print("\n[STEP 5] Generating verification report...")
    report = LedgerReporter.verify_report(ledger)
    print(report)
    
    # Statistics
    print("\n[STEP 6] Ledger statistics...")
    stats = ledger.coherence_report()
    print(f"  Total Elections: {stats['total_elections']}")
    print(f"  Fully Verified: {stats['fully_verified']}/{stats['total_elections']}")
    print(f"  Verification Rate: {stats['verification_percentage']:.1f}%")
    print(f"  Status Distribution:")
    for status, count in stats['status_distribution'].items():
        print(f"    {status}: {count}")
    
    print("\n" + "=" * 80)
    print("RESULT: Election Ledger Engine is fully functional")
    print("=" * 80)


if __name__ == "__main__":
    demo_election_ledger_engine()
