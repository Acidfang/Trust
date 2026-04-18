# HOW TO USE THE MULTI-AGENT SYSTEM
## A Guide to Agent Collaboration for Determined Project

**What**: You now have 6 AI agent personas that work together systematically  
**How**: Call them by election phase, they integrate automatically with ZEROPOINT  
**Why**: Ensures every decision is verified, scalable, and reversible

---

## THE 6 AGENTS

### 1. RESEARCHER (Election 0⊙: EXPOSE)
**Skill**: Strip systems to primitives. What actually exists?  
**Method**: JUICE - Backward debugging, remove assumptions  
**When to Use**: 
- Start of project analysis
- When something seems broken but you're not sure what
- To understand current state objectively
- To find dead code or unused features

**Example Call**:
```
RESEARCHER: "What's actually working right now?"
→ Output: List of completed features, current gaps, primitives
→ Gate Check: Can each finding trace to ledger? (Gate 1)
```

---

### 2. ARCHITECT (Election 2κ⊕4ψ: DESIGN)
**Skill**: Declare system constraints BEFORE building. Declare optimal state.  
**Method**: ZAP/UFM - Spec first, implementation later  
**When to Use**:
- Before writing any code
- When defining a new feature
- To declare rules that must never be violated
- To reverse causality (declare what should be, work backward)

**Example Call**:
```
ARCHITECT: "Design an optimization loop for parameters"
→ Output: 6-layer architecture with constraints
→ Gate Check: Is method ZAP/UFM? (Gate 2)
```

---

### 3. ANALYST (Election 1β-3⊕: FILTER & ISOLATE)
**Skill**: Find patterns. What repeats? What's anomalous?  
**Method**: JUICE - Binary filter, separate signal from noise  
**When to Use**:
- After RESEARCHER finds raw data
- When categorizing features or parameters
- To detect relationships between things
- To find what's unusual (opportunities or problems)

**Example Call**:
```
ANALYST: "Categorize these 7 parameters - what patterns exist?"
→ Output: Grouped by type/impact, anomalies listed
→ Gate Check: Ambiguity eliminated? (Gate 2)
```

---

### 4. OPTIMIZER (Election 3⊕-5Θ: COMMIT TO CORE)
**Skill**: Generate recommendations. What should change?  
**Method**: ZAP/UFM - Declare improved state  
**When to Use**:
- After ANALYST understands patterns
- When you need improvement ideas
- To prioritize work
- To declare target metrics

**Example Call**:
```
OPTIMIZER: "Given these parameters, what 3 changes would most improve the system?"
→ Output: Ranked recommendations with reasons
→ Gate Check: Would this work at scale? (Gate 5)
```

---

### 5. REVIEWER (Election 6λ: VERIFY COHERENCE)
**Skill**: Check ALL gates. Verify nothing was missed.  
**Method**: Strict gate checking (9 gates: 4 anti-drift + 5 finite)  
**When to Use**:
- Before executing ANY recommendation
- When you're unsure if something is safe
- To verify nothing was overlooked
- Before committing to ledger

**Example Call**:
```
REVIEWER: "Verify these 3 recommendations - do they pass all 9 gates?"
→ Output: Gate-by-gate verification report
→ Verdict: ✅ ALL PASS or ❌ GATE X FAILED
→ Gate Check: Kindness check - are we doing right thing? (Gate 4)
```

---

### 6. IMPLEMENTER (Election 7-10: REBUILD & VERIFY)
**Skill**: Execute carefully. Build minimal, verify, attach proof.  
**Method**: Step-by-step with interlocks  
**When to Use**:
- When REVIEWER approves (all gates pass)
- For actually executing changes
- To write values to ledger
- To prepare checkpoints

**Example Call**:
```
IMPLEMENTER: "Execute these approved recommendations"
→ Output: 3-step execution plan (prepare, write, verify)
→ Status: Ready to execute
→ Gate Check: Did write succeed? (Election 8)
```

---

## DECISION TREE - WHICH AGENT TO USE?

```
START
│
├─→ "What's the current state?"
│   └→ RESEARCHER (Election 0⊙)
│
├─→ "What should the system be like?"
│   └→ ARCHITECT (Election 2κ)
│
├─→ "What patterns exist in this data?"
│   └→ ANALYST (Election 1β)
│
├─→ "What should we change?"
│   └→ OPTIMIZER (Election 3⊕)
│
├─→ "Is this safe to do?"
│   └→ REVIEWER (Election 6λ)
│
├─→ "Let's actually do it"
│   └→ IMPLEMENTER (Election 7)
│
└─→ LOOP ENTIRE CYCLE (Elections 0⊙-13)
    └→ Checkpoint recorded
```

---

## TYPICAL WORKFLOW (0-13 CYCLE)

```
Phase 1: RESEARCH (Election 0⊙-2κ)
  1. RESEARCHER exposes actual state
  2. ARCHITECT declares desired state
  3. ANALYST finds patterns in data
  
Phase 2: OPTIMIZE (Election 3⊕-5Θ)
  1. OPTIMIZER generates recommendations
  2. All 9 gates checked
  3. No recommendations rejected yet

Phase 3: VERIFY & EXECUTE (Election 6λ-12)
  1. REVIEWER verifies coherence (Election 6λ)
  2. IMPLEMENTER prepares execution (Election 7-10)
  3. System state updated (Election 11-12)

Phase 4: CHECKPOINT (Election 13)
  1. Decision recorded to ledger
  2. Evidence attached (gate verification log)
  3. New cycle ready to start
```

---

## HOW TO INVOKE AGENTS DIRECTLY

### From Command Line:
```powershell
# Run entire orchestration
python multi_agent_orchestration.py

# Run specific agent (when supported)
python multi_agent_orchestration.py --agent researcher
python multi_agent_orchestration.py --agent architect
```

### From Python Code:
```python
from multi_agent_orchestration import (
    Researcher, Architect, Analyst, Optimizer, Reviewer, Implementer
)

# Use one agent
researcher = Researcher()
findings = researcher.analyze_current_state()
print(findings)

# Use multiple agents
architect = Architect()
spec = architect.design_optimization_loop()

analyst = Analyst()
analysis = analyst.analyze_parameters(parameters)
```

---

## WHAT EACH AGENT PRODUCES

| Agent | Input | Output | Record |
|-------|-------|--------|--------|
| RESEARCHER | System state | Findings JSON | Gap analysis |
| ARCHITECT | Scope | Architectural spec | Design decisions |
| ANALYST | Raw data | Categorization + patterns | Metadata |
| OPTIMIZER | Patterns | Ranked recommendations | Priority list |
| REVIEWER | Recommendations | Gate verification | Approval/rejection |
| IMPLEMENTER | Approved recs | Execution plan | Checkpoint |

---

## GATE INTEGRATION (Automatic with Each Agent)

**Agent produces output → Automatic gate check →**

| Gate | Agent Check | Pass Condition |
|------|------------|----------------|
| 1 (Ledger) | RESEARCHER | Findings trace to ledger |
| 2 (Method) | ARCHITECT | Design is ZAP/UFM or JUICE |
| 3 (Cycle) | OPTIMIZER | Follows 0-13 sequence |
| 4 (Authority) | REVIEWER | Roadmap item exists |
| 5-9 (Finite) | REVIEWER | Alignment, ambiguity, reason, kindness, scale |

---

## EXAMPLE: ADDING A NEW FEATURE

```
USER: "I want to add a 'continuous learning' mode"

Step 1: RESEARCHER
  Analyze current code
  Output: "Continuous learning mode not in codebase"
  Gate 1 Check: ✓ (Current state traced)

Step 2: ARCHITECT
  Design continuous learning feature
  Output: "3-layer architecture: collect → analyze → feedback"
  Gate 2 Check: ✓ (ZAP/UFM - spec declared)

Step 3: ANALYST
  Categorize required changes
  Output: "Needs 4 new modules, 1 modified"
  Gate 2 Check: ✓ (Ambiguity eliminated)

Step 4: OPTIMIZER
  Recommend priority implementation
  Output: "Build feedback layer first (enables other 3)"
  Gate 5 Check: ✓ (Works at scale)

Step 5: REVIEWER
  Verify all gates
  Output: "All 9 gates pass. Safe to execute."

Step 6: IMPLEMENTER
  Execute the build
  Output: "Feedback layer running. Ready for next module."
  Checkpoint recorded (Election 13)
```

---

## COMMON PATTERNS

### Pattern 1: "Something is wrong but I don't know what"
```
Call: RESEARCHER
→ Exposes what's actually true
→ Often reveals assumption was wrong, not code
```

### Pattern 2: "I want to improve X"
```
Call: ARCHITECT → ANALYST → OPTIMIZER → REVIEWER
→ Spec what "improved" means
→ Find what needs to change
→ Get ranked recommendations
→ Verify safety
```

### Pattern 3: "This recommendation keeps failing"
```
Call: REVIEWER
→ Check which gate is failing
→ If Gate 1: Not traceable → needs RESEARCHER
→ If Gate 2: Method unclear → needs ARCHITECT
→ If Gate 4: Not authorized → ask user permission
→ If Gate 5-9: Reasoning issue → back to ANALYST/OPTIMIZER
```

### Pattern 4: "I need to debug this in a new way"
```
Call: ARCHITECT
→ Declare new debugging method
→ ZAP/UFM says: "This is what we're testing"
→ ANALYST can then isolate signals
→ OPTIMIZER can recommend how to trace
```

---

## AGENT COMMUNICATION STYLE

Each agent "speaks" in election language:

- **RESEARCHER**: "Here's what I exposed (Election 0⊙)"
- **ARCHITECT**: "Here's what SHOULD be (Election 2κ)"
- **ANALYST**: "Here's what REPEATS (Election 1β)"
- **OPTIMIZER**: "Here's what to CHANGE (Election 3⊕)"
- **REVIEWER**: "Here's what's COHERENT (Election 6λ)"
- **IMPLEMENTER**: "Here's what HAPPENS (Election 7-10)"

Read their output as: "This is my report from the [election phase]"

---

## LIMITATIONS & DESIGN

**What agents CAN do**:
- ✓ Analyze and categorize
- ✓ Recommend (with reasoning)
- ✓ Verify against gates
- ✓ Plan execution
- ✓ Record decisions

**What agents CANNOT do** (by design):
- ✗ Execute code without IMPLEMENTER approval
- ✗ Bypass ZEROPOINT gates
- ✗ Commit to ledger without REVIEWER sign-off
- ✗ Make decisions outside authorized scope
- ✗ Ignore past checkpoints

**Why**: This ensures every decision is traceable and reversible.

---

## NEXT STEPS

1. **For ChatDev Integration**:
   - Configure `.env` with LLM API key
   - Let agents analyze Determined parameters
   - Build ChatDev workflows from agent recommendations

2. **For Parameter Optimization**:
   - Use ANALYST to find which parameters matter most
   - Use OPTIMIZER to recommend optimal values
   - Use REVIEWER to verify changes won't break system

3. **For Continuous Improvement**:
   - Run agents every session (0-13 cycle)
   - Each cycle improves the system
   - Checkpoints allow debugging past cycles

---

**Status**: ✅ AGENT SYSTEM READY TO USE

Try the agents next time you need to:
- Understand a system
- Design a feature
- Find patterns
- Get recommendations
- Verify decisions
- Execute safely
