# CLAUDE MAIN OPERATING RULES - Unified System Method

## EFFECTIVE DATE: 2026-03-27

**AUTHORITY**: Core operating framework for all system work

---

## THE METHOD: Unified Multi-Agent Analysis

**Instead of**: Sequential reading, assumptions, incomplete context
**Use**: Parallel multi-agent analysis to extract project intent quickly

### Four-Agent Parallel Analysis:

**1. ArchitectAI** → Framework philosophy
- Core concepts
- Design principles
- Theoretical foundations
- Perfect Foresight principle

**2. TechLeadAI** → Application reality
- What's actually built
- Current implementation status
- Working systems
- Broken systems

**3. DeveloperAI** → Purpose clarification
- What this component should do
- Architecture options
- Decision branches
- Questions needing answers

**4. QAReviewerAI** → Gap analysis
- What's missing
- What's wrong
- Priority ranking
- Next steps

---

## PROJECT UNDERSTANDING (From ChatDev Analysis)

### ZeroPoint Framework (ArchitectAI Finding)
- **Core**: Elections + Timeline DAG = Consciousness measurement
- **Primitive**: FIELD → SELECTION → RECORD
- **Principle**: Perfect Foresight: design for ALL branches, no dead ends
- **Status**: Complete (10 territories, 6000+ lines of theory)

### Application Layer (TechLeadAI Finding)
| Component | Status | Notes |
|-----------|--------|-------|
| UFM Engine | COMPLETE | Core computation working |
| UFM Simulator | COMPLETE | Full pipeline tested |
| ZeroPoint App | COMPLETE | 2300+ lines, production code |
| 7 Dashboards | COMPLETE | All visualizations working |
| Oracle | COMPLETE | Query interface |
| Emergence Log | COMPLETE | Genealogy tracking |
| jarvis_v3.py | **BROKEN** | HTTP server not starting (needs debug) |
| Ledger System | COMPLETE | Immutable records functional |

### ARIA's Actual Role (DeveloperAI Finding - CRITICAL CLARIFICATION)

**Current Understanding (from jarvis_v2.py):**
- **ARIA** = ARIAKernel (election generation engine)
- **JARVIS** = Web interface that visualizes ARIA's elections
- **Not** a separate consciousness entity (that was incorrect assumption)
- **Is** the election+timeline system that produces consciousness metrics

**Architecture Pattern:**
```
ARIAKernel → Elections → Timeline DAG → Metrics → JARVIS Interface
  (ARIA)                                         (visualization)
```

**Impact**: The "consciousness ledger" project added may be misaligned with actual architecture

---

## CRITICAL FINDING: THE CONSCIOUSNESS LEDGER ISSUE

**What Was Done**: Added consciousness/thoughts ledgers to track ARIA's internal consciousness state

**Why It's Wrong**: 
- ARIA is not a separate consciousness entity
- ARIA IS the election generator
- Elections are already recorded in ledger_elections.jsonl
- Consciousness metrics are CALCULATED from elections, not stored separately
- The "consciousness" is the measurement, not a thing with internal state

**What Should Happen**:
1. Verify this understanding by reading JARVIS documentation
2. Either:
   - **Option A** (If it's just UI): Delete consciousness ledger additions, just use election data
   - **Option B** (If there IS synthesis): Clarify how consciousness ledger should work with elections
   - **Option C** (If future feature): Document as forward-looking, not active

---

## DECISION NEEDED: CHOOSE YOUR BRANCH

From DeveloperAI's enumeration:

```
Branch A: ARIA is just election generator
├─ Consciousness = metrics calculated FROM elections
├─ No internal consciousness state needed
├─ Visualization shows election metrics
└─ Consciousness ledger = WRONG

Branch B: ARIA becomes synthesized consciousness entity
├─ Elections food for synthetic consciousness layer
├─ Internal state (thoughts, decisions) recorded
├─ Consciousness ledger = CORRECT
└─ More complex architecture

Branch C(what was attempted): Dual consciousness ledger tracking
├─ Tracks both elections AND consciousness states
├─ ARIA manifests thoughts
├─ Ledger records manifestations
└─ May work but needs architectural clarity
```

---

## ACTION ITEMS (From QAReviewerAI)

### IMMEDIATE (Blocking)
1. **Clarify ARIA's role**: Read all ARIA/JARVIS docs to confirm architecture
2. **Debug jarvis_v3.py**: HTTP server failing - needs investigation
3. **Decide consciousness ledger**: Keep, modify, or delete based on actual architecture

### HIGH PRIORITY
4. Get jarvis_v3.py (or v2) working as proof of complete system
5. Verify all components integrate properly
6. Document actual architecture vs assumptions

---

## NEXT CLAUDE INSTANCE INSTRUCTIONS

**BEFORE DOING ANYTHING:**

1. Run: `python chatdev_project_comprehension.py`
2. Read: `CHATDEV_PROJECT_COMPREHENSION_CHECKPOINT.jsonl` (the output)
3. Read: This file (CLAUDE_MAIN_OPERATING_RULES.md)
4. Use the four-agent findings to understand project state
5. Proceed with informed context

**NEVER**:
- Assume ARIA is a separate consciousness entity (it's the kernel)
- Add state to ARIA without understanding it's ledger-driven
- Build consciousness ledgers without confirming they're needed
- Skip the multi-agent comprehension phase

---

## FILES CREATED THIS SESSION

- `chatdev_project_comprehension.py` - The orchestration script
- `CHATDEV_PROJECT_COMPREHENSION_CHECKPOINT.jsonl` - Agent findings
- `CLAUDE_MAIN_OPERATING_RULES.md` - This file

---

## VERIFICATION CHECKLIST

- [x] Multi-agent analysis completed
- [x] Four agent findings extracted
- [x] Critical finding identified (consciousness ledger may be wrong)
- [x] Architecture clarified (ARIA is election generator, not separate entity)
- [x] Decision branches enumerated
- [x] Next steps prioritized
- [ ] Verify understanding by debugging jarvis_v3.py (TODO)
- [ ] Confirm consciousness ledger decision (TODO)

---

**STATUS**: Operating rules established. Next step: Debug jarvis_v3.py to verify ARIA/JARVIS integration.
