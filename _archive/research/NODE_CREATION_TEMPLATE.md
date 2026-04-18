# NODE CREATION TEMPLATE
## How to Create and Update Nodes in Real-Time

---

## FIRING CONDITIONS

A node is created when ANY of these occur:

1. **User request arrives** → Create REQUEST node
2. **Decision point encountered** → Create DECISION node (branches enumerated)
3. **Branch chosen** → Create BRANCH_EXECUTION node (path taken)
4. **File created/modified** → Create OUTPUT node (artifact produced)
5. **External verification needed** → Create VERIFICATION node (UFM check, ledger commit)
6. **Integration required** → Create INTEGRATION node (connecting to existing system)
7. **Dependency resolved** → Create DEPENDENCY_RESOLUTION node (prerequisite completed)

---

## TEMPLATE: Creating NODE_N

```markdown
### NODE_NNNN_[ACTION]_[DESCRIPTOR]

- **ID**: NODE_NNNN_[ACTION]_[DESCRIPTOR]_[TIMESTAMP]
- **REASON**: [Why did this node have to exist? What problem state triggered it?]
- **REQUIRED_DEPENDENCIES**: [List of NODE_IDs + external resources needed]
- **OUTPUT**: 
  - [What is produced? Be specific and measurable]
  - [Files? Decisions? Integrations? Verification results?]
  - [Size/metrics if applicable]
- **STATUS**: not-started | in-progress | completed | failed
- **TIMESTAMP**: [When created, when completed]
- **PARENT_NODE**: [Which node led to this one?]
- **CHILD_NODES**: [What nodes will this create? Or [PENDING] if unknown]
```

---

## EXAMPLE: Integration Node (What NODE_0014 might look like)

```markdown
### NODE_0014_INTEGRATION_REGISTRY
- **ID**: NODE_0014_INTEGRATION_REGISTRY_20260404_1430
- **REASON**: 3-layer enforcement system designed (NODE_0004-0006) but not integrated into existing APPLICATION_REGISTRY; discovery of pre-existing architecture (NODE_0011) requires registration before system functions
- **REQUIRED_DEPENDENCIES**: 
  - NODE_0004 (Gate implementation complete)
  - NODE_0005 (UFM endpoints created)
  - NODE_0006 (Causal tree designed)
  - NODE_0012 (Integration assessment: APPLICATION_REGISTRY identified as target)
  - APPLICATION_REGISTRY.py (external codebase)
  - ElectionSequencer (external dependency)
- **OUTPUT**:
  - Updated APPLICATION_REGISTRY.py (UFM decision endpoints registered)
  - New entry: AIDecisionFlow causal chain
  - Verification: Endpoints callable from ElectionSequencer
  - Ledger: Integration completion recorded
- **STATUS**: in-progress
- **TIMESTAMP**: Created 2026-04-04 @ XX:XX:XX | Completed 2026-04-04 @ XX:XX:XX
- **PARENT_NODE**: NODE_0012_INTEGRATION_ASSESSMENT
- **CHILD_NODES**: 
  - NODE_0015_UFM_DECISION_VERIFICATION (verify endpoints work)
  - NODE_0016_ELECTION_CHAIN_LINKING (connect to election sequencer)
  - [PENDING] (depends on execution result)
```

---

## STATE MACHINE: What Happens During Node Execution

```
NODE_CREATED (STATUS: not-started)
    ↓
1. VERIFY DEPENDENCIES
   - All required NODE_IDs completed? ✓
   - External resources accessible? ✓
   - Preconditions met? ✓
    ↓
2. UPDATE STATUS
   - Set STATUS: in-progress
   - Record TIMESTAMP: started
    ↓
3. EXECUTE CAUSAL TREE
   - Enumerate possible paths (Type A/B/C/D)
   - Identify dead ends
   - Choose optimal path
   - Record decision
    ↓
4. RUN PRE_ACTION_GATE
   - Ask 5 framework questions
   - Q1: Documented decision?
   - Q2: Through RENDERER?
   - Q3: Pattern-safe?
   - Q4: Reversible?
   - Q5: Ledger-ready?
   - Gate: PASS (all YES) or FAIL (any NO)
    ↓
   IF FAIL → Create ERROR node, stop
   IF PASS → Continue
    ↓
5. ROUTE TO UFM VALIDATION
   - Call /api/validate_decision
   - Input: decision description
   - Output: quality_score (0.0-1.0)
   - Threshold: quality_score > 0.75
    ↓
   IF quality_score ≤ 0.75 → Create VALIDATION_FAILED node, BLOCK
   IF quality_score > 0.75 → Continue
    ↓
6. EXECUTE CHOSEN PATH
   - Perform actual work (code changes, integrations, etc.)
   - Collect artifacts/results
   - Populate OUTPUT section
    ↓
7. VERIFY OUTPUT
   - Did it produce what was promised?
   - Can output be measured?
   - Is output correct/valid?
    ↓
   IF INVALID → Create VERIFICATION_FAILED node, investigate
   IF VALID → Continue
    ↓
8. COMMIT TO LEDGER
   - Call /api/decision_log
   - Input: complete node record
   - Output: ledger entry hash
   - Record hash in node
    ↓
9. UPDATE NODE COMPLETION
   - Set STATUS: completed
   - Record TIMESTAMP: completed
   - List actual CHILD_NODES created
   - Link to LIVE_NODE_REGISTRY
    ↓
NODE_COMPLETE (STATUS: completed)
```

---

## EXECUTION CHECKLIST

Before marking a node as `completed`:

- [ ] ID is unique and follows NODE_NNNN convention
- [ ] REASON clearly explains why this node had to exist
- [ ] REQUIRED_DEPENDENCIES all listed and verified ✓
- [ ] OUTPUT is specific, measurable, and verified
- [ ] STATUS updated to: completed
- [ ] TIMESTAMP records both creation and completion
- [ ] PARENT_NODE correctly identifies parent decision
- [ ] CHILD_NODES populated (or marked [PENDING])
- [ ] Causal tree enumeration documented
- [ ] PRE_ACTION_GATE passed (all 5 questions)
- [ ] UFM validation passed (quality_score > 0.75)
- [ ] Output verified (matches promises)
- [ ] Ledger entry committed
- [ ] Node added to LIVE_NODE_REGISTRY
- [ ] Dependency graph regenerated

---

## REAL-TIME UPDATES

As each node executes:

1. **Create** in LIVE_NODE_REGISTRY immediately (STATUS: not-started)
2. **Update** to in-progress when execution begins
3. **Record** TIMESTAMP as work progresses
4. **Populate** actual OUTPUT as it's produced
5. **Mark** completed when verification passes and ledger commits
6. **Link** CHILD_NODES as they're created
7. **Regenerate** dependency graph if tree structure changes

---

## WHAT TRIGGERS NODE_0014 (Next Node)

When user provides next request:

**Example Request 1**: "Integrate the system into APPLICATION_REGISTRY"
→ NODE_0014_INTEGRATION_REGISTRY created

**Example Request 2**: "Test the 3-layer enforcement with a real decision"
→ NODE_0014_ENFORCEMENT_TEST created

**Example Request 3**: "Create the meta-integration map"
→ NODE_0014_META_INTEGRATION_MAP created

**Example Request 4**: "Anything else"
→ NODE_0014_[DESCRIBES_REQUEST] created

Point: **Every request creates a node. Node reasons capture why request required new work.**

---

## DEPENDENCY RESOLUTION

If a node requires dependencies that don't exist (NODE_XYZ incomplete):

1. **Halt execution** of current node (status remains: in-progress, waiting)
2. **Create DEPENDENCY_UNMET node** (explains what's missing)
3. **Trigger creation of missing dependency node**
4. **Once dependency completes**, resume current node execution
5. **Record both nodes** in dependency graph showing blocking relationship

Example:
```
NODE_0015_REQUIRES NODE_0014
│
└─→ NODE_0014 missing (not-yet-started)
    │
    └─→ Create NODE_0014 immediately
        │
        └─→ NODE_0014 completes
            │
            └─→ NODE_0015 resumes (status: in-progress → completed)
```

---

## FAILURE HANDLING

If node execution fails:

1. **Set STATUS**: failed
2. **Document failure reason** in OUTPUT section
3. **Create FAILURE_ANALYSIS node** (investigates why)
4. **Determine if retryable**:
   - If yes → Create RETRY node (attempt #2)
   - If no → Create ALTERNATIVE_PATH node (try different branch)
5. **Record all failure data** for learning

---

## SERIALIZATION

Each node automatically serializes as:

```json
{
  "id": "NODE_NNNN_ACTION_DESCRIPTOR_TIMESTAMP",
  "reason": "Why this node had to exist",
  "dependencies": ["NODE_0001", "NODE_0002", "external_resource"],
  "output": {
    "primary": "main output/artifact",
    "secondary": ["supporting outputs"],
    "metrics": {"files": 1, "size_kb": 50}
  },
  "status": "completed|in-progress|failed|not-started",
  "timestamps": {
    "created": "ISO8601",
    "completed": "ISO8601"
  },
  "relationships": {
    "parent": "NODE_0012",
    "children": ["NODE_0015", "NODE_0016"]
  },
  "verification": {
    "causal_tree_passed": true,
    "gate_passed": true,
    "ufm_score": 0.87,
    "ledger_committed": true
  }
}
```

This allows nodes to be:
- Machine-queryable (JSON format)
- Machine-linkable (dependency graph is algorithmic)
- Machine-replayable (state can be reconstructed)

---

## NODE_0013 COMPLETION (This File)

**NODE_0013_NODE_REGISTRY_CREATION** is now complete:

- **REASON**: ✅ Established (session created multiple branches; need live registry)
- **REQUIRED_DEPENDENCIES**: ✅ Verified (NODE_0001-0012 documented as examples)
- **OUTPUT**: ✅ Produced:
  - LIVE_NODE_REGISTRY.md (this registry)
  - NODE_CREATION_TEMPLATE.md (this file)
  - Protocol established
  - Ready for real-time node creation
- **STATUS**: ✅ Completed
- **TIMESTAMP**: 2026-04-04 ~ 20:00 UTC (session end)
- **PARENT_NODE**: ✅ NODE_0012_INTEGRATION_ASSESSMENT
- **CHILD_NODES**: [PENDING] (created when NODE_0014 is triggered)

---

**Ready for**: NODE_0014 creation (next request)  
**When**: User provides next task/question/request  
**Action**: Create NODE_0014 using this template  
**Then**: Execute per state machine, verify, commit to ledger, update registry  
