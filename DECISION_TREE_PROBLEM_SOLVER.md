# DECISION TREE: PROBLEM TYPE → CORE PRINCIPLE
## How to identify and solve problems using the 18 core principles

---

## THE DIAGNOSTIC FRAMEWORK

### DECISION LEVEL 1: What's the problem category?

```
PROBLEM TYPE                               PRIMARY PRINCIPLES TO USE
─────────────────────────────────────────────────────────────────────

A. DIAGNOSIS PROBLEMS
   "Something isn't working"               → 1, 4, 15
   
B. PREDICTION PROBLEMS  
   "What will happen?"                     → 2, 5, 8, 12
   
C. OPTIMIZATION PROBLEMS
   "How do we improve?"                    → 3, 6, 7, 10, 11
   
D. DESIGN PROBLEMS
   "How should we build this?"             → 1, 7, 9, 14, 16, 17
   
E. FAILURE PREVENTION
   "How do we prevent catastrophe?"        → 2, 8, 12, 16
   
F. INNOVATION PROBLEMS
   "How do we improve/change?"             → 6, 13, 18
```

---

## A. DIAGNOSIS PROBLEMS (Something isn't working)

### A1: "I have a problem but don't know the root cause"
**Use Principle 1: Multi-constraint Management**

```
SYMPTOM: Problem exists but cause unclear
APPROACH:
  1. List all constraints in the system
  2. Check which constraint failure explains the symptom
  3. Check if MULTIPLE constraints failed (most common)
  4. Don't fix one constraint; verify all must be adjusted

EXAMPLES:
- Patient has fatigue → Check thyroid, B12, sleep, stress, exercise (multiple constraints)
- Team productivity low → Check morale, clarity, tools, processes, communication (all four matter)
- Software buggy → Check design, testing, documentation, code review, development speed
```

### A2: "We tried the standard solution but it's not working"
**Use Principle 15: Constraint Type Determines Outcome**

```
SYMPTOM: Standard treatment/solution ineffective
APPROACH:
  1. Identify what TYPE of constraint is the problem
  2. Match solution type to constraint type
  3. Different constraint types ≠ different solutions

EXAMPLES:
- Learning problems: 
  * If ATTENTION constraint → ADHD medication helps
  * If PROCESSING-SPEED constraint → medication doesn't help, need pacing
  * If MEMORY constraint → need memory techniques
  
- Business problems:
  * If QUALITY constraint → process improvement
  * If SPEED constraint → automation
  * If COST constraint → efficiency/scale
  * If DEMAND constraint → marketing
  
- Market problems:
  * If INFORMATION constraint → transparency/education fixes
  * If COORDINATION constraint → rules/structure fixes
  * If MONOPOLY constraint → anti-trust fixes

DECISION TREE:
  What type of constraint is causing this?
    → Classify it
      → Apply solution for that type
        → Verify it works
```

### A3: "The constraint is TELLING us something important"
**Use Principle 4: Constraint as Information/Feedback**

```
SYMPTOM: Constraint/signal exists and seems problematic
APPROACH:
  1. Before removing/suppressing constraint, read what it means
  2. Constraint = signal about system state
  3. Removing signal = losing diagnosis

EXAMPLES:
- Pain: Don't just suppress. Pain tells you what's wrong (sharp≠dull≠throbbing)
- Anxiety: Don't just suppress. Anxiety signals mismatch between expectation and reality
- Boredom: Don't just overcome. Boredom signals environment needs change
- Price spikes: Don't just cap prices. Price signals what constraint is active (supply? demand? behavior?)
- Error messages: Don't just suppress. Errors carry diagnostic information
- Negative feedback: Feedback IS information. System without feedback is blind

DECISION TREE:
  What is the constraint signaling?
    → Identify the signal
      → Take action based on signal
        → Verify you understood correctly
```

---

## B. PREDICTION PROBLEMS (What will happen?)

### B1: "Will this change cause a sudden catastrophic failure?"
**Use Principle 2: Constraint Failure Cascades**

```
SYMPTOM: System seems stable, worried about sudden failure
APPROACH:
  1. Identify potential cascade chains
  2. Find the cascade triggers (where one failure causes another)
  3. Estimate cascade threshold
  4. Prevent the threshold, not the first failure

EXAMPLES:
- Detonation: Fuel alone OK. Ignition alone OK. Together → cascade
- Ecosystem collapse: One species removal OK. Two removals OK. At N → cascade
- Market crash: First seller OK. At N sellers → cascade begins
- Organizational failure: First key person leaves OK. At K people → cascade
- Epidemic: Few infections OK. Past threshold → exponential spread

DECISION TREE:
  Is this a cascade system?
    → Yes: Find the threshold
      → Estimate when threshold is crossed
        → Prevent cascade by preventing threshold
        → Monitor for threshold-approach signals
    
    → No: Standard failure analysis applies
```

### B2: "Will this change be continuous or catastrophic?"
**Use Principle 5: Nonlinear/Threshold Response**

```
SYMPTOM: Concerned about sudden shifts with small changes
APPROACH:
  1. Identify if system has threshold behavior
  2. Find the threshold location
  3. Predict whether system is near threshold
  4. Small changes before threshold = continuous. At/past threshold = discontinuous

EXAMPLES:
- Temperature: Continuous change → discontinuous state change at phase transition
- Anxiety: Low stress OK. Moderate stress OK. Past threshold → panic cascade
- Neural firing: Below threshold = no fire. Above = full fire (not proportional)
- Cardiac rhythm: Small arrhythmias compensated. Past threshold → sudden failure
- Stock market: Gradual losses OK. Past threshold → cascade selling

DECISION TREE:
  Does this system have threshold behavior?
    → Yes: How far are we from threshold?
      → Close → small changes are risky
      → Far → gradual change safe
    
    → No: Predict continuous response
      → Standard linear prediction applies
```

### B3: "If I change X, what else will change?"
**Use Principle 8: Constraint Coupling**

```
SYMPTOM: Worried about unintended consequences
APPROACH:
  1. Map constraint dependency graph
  2. Identify what's coupled to the constraint you're changing
  3. Predict all coupled changes
  4. Can't change one independently; must adjust others

EXAMPLES:
- Change drug A → affects liver metabolism → drug B now too strong
- Change tax → affects prices → affects behavior → affects development patterns
- Change organizational structure → affects hiring → affects performance culture
- Change temperature → affects pressure and volume simultaneously
- Change hiring standards → affects promotion speed → affects retention

DECISION TREE:
  What constraints are coupled to this one?
    → Map the coupling graph
      → Predict all downstream effects
        → Adjust ALL coupled constraints
          → Verify system still works
```

### B4: "This system looks stable but might be fragile"
**Use Principle 12: Constraint as Metastable State**

```
SYMPTOM: System appears stable but worried about hidden fragility
APPROACH:
  1. Identify if state is metastable (stable equilibrium vs false equilibrium)
  2. Look for tiny perturbations that could trigger collapse
  3. Monitor for perturbation sources
  4. Catastrophic failure possible with small trigger

EXAMPLES:
- Ecosystem: Looks stable for decades, then suddenly crashes (metastable)
- Market bubble: Looks stable (prices rising), but detached from fundamentals
- Autoimmunity: Looks stable for years, then suddenly autoimmune (metastable)
- False vacuum: Universe appears stable but in false vacuum state

DECISION TREE:
  Is this system metastable?
    → Check deviation from fundamental equilibrium
      → If close to equilibrium → stable
      → If far from equilibrium → metastable
        → Monitor for perturbation sources
          → If perturbations likely → fragile
          → If perturbations unlikely → can be metastable long-term
```

---

## C. OPTIMIZATION PROBLEMS (How do we improve?)

### C1: "We're too constrained/not constrained enough. What's the sweet spot?"
**Use Principle 3: Optimal Constraint Calibration**

```
SYMPTOM: More constraint makes things worse. Less constraint also makes things worse.
APPROACH:
  1. Identify the constraint level
  2. Identify the performance metric
  3. Find the sweet spot (peak performance)
  4. Can move only in one direction (toward sweet spot)

EXAMPLES:
- Learning: Challenge too easy = boredom. Challenge too hard = frustration. Calibrate to edge
- Organizational hierarchy: Too centralized = slow. Too decentralized = chaotic. Find optimal depth
- Immune tolerance: Too strict = autoimmunity. Too loose = infections. Calibrate tolerance
- Temperature: Too cold = no reaction. Too hot = decomposition. Find activation energy sweet spot
- Social diversity: Too homogeneous = fragile. Too diverse = chaos. Find optimal mix
- Stress: No stress = atrophy. Chronic stress = damage. Calibrate stress-recovery ratio

DECISION TREE:
  Is performance maximized?
    → No: Are we too constrained or not constrained enough?
      → Too constrained: Reduce constraint
      → Not constrained enough: Increase constraint
        → Measure performance
          → Repeat until sweet spot found
```

### C2: "Should this be centralized or distributed?"
**Use Principle 7: Constraint Distribution Trade-offs**

```
SYMPTOM: System too slow or too fragile
APPROACH:
  1. Identify the constraint
  2. Identify the tradeoff (speed vs robustness)
  3. Adjust distribution based on constraint

EXAMPLES:
- Centralized: Fast decisions, single point of failure, brittle
- Distributed: Slow decisions, robust, adaptive

MATCH TO PROBLEM:
  Emergency (fire)? → Centralize (need fast decision)
  Long-term (climate)? → Distribute (need adaptation)
  Known problem? → Centralize (pre-computed decision)
  Unknown problem? → Distribute (need local adaptation)
  Stable environment? → Centralize (efficiency)
  Volatile environment? → Distribute (robustness)

DECISION TREE:
  What's the constraint?
    → Speed constraint: Centralize
    → Robustness constraint: Distribute
    → Efficiency constraint: Centralize
    → Adaptability constraint: Distribute
```

### C3: "How much precision do we actually need?"
**Use Principle 10: Constraint Precision vs Cost**

```
SYMPTOM: Cost too high or precision too low
APPROACH:
  1. Identify minimum necessary precision
  2. Don't over-specify
  3. Don't under-specify
  4. Find the precision-cost curve

EXAMPLES:
- Engineering: Tight tolerance = high cost. Loose tolerance = failures. Find minimum precision needed
- Language: Can communicate with 300 words, fluent with 2000, native with 20000
- Medicine: Screening precision determines false positive rate and treatment cost
- Software: Precise specs = expensive and slow. Vague specs = cheaper and rework needed

DECISION TREE:
  What will happen if precision is too low?
    → Unacceptable → increase precision
      → Check cost
        → Acceptable → done
        → Too high → see if minimum acceptable precision lower
  
  What will happen if precision is unnecessarily high?
    → Cost impact acceptable → can keep high precision
    → Cost too high → reduce to minimum acceptable
```

### C4: "Should we build a habit, protocol, or just improvise?"
**Use Principle 11: Constraint Efficiency Trade**

```
SYMPTOM: People keep making mistakes or can't scale
APPROACH:
  1. Identify high-frequency, low-variation activities
  2. Encode as habit/protocol/ritual
  3. Frees conscious capacity for novel problems
  4. Reduces decision load

EXAMPLES:
- Habit: "Brush teeth before bed" (daily, same way)
- Protocol: "Follow medical protocol for all patients" (reduces cognitive load)
- Ritual: "Team standup every Tuesday" (ensures consistency)
- Grammar: "Follow grammatical rules" (enables communication)

DECISION TREE:
  Is this activity high-frequency?
    → Yes: Does it have low variation (same way each time)?
      → Yes: Build a constraint (habit/protocol/ritual)
        → Verify it removes decision load
      → No: Keep flexible, don't constrain
    
    → No: Don't constraint (too rare to benefit)
```

---

## D. DESIGN PROBLEMS (How should we build this?)

### D1: "What constraints should we design in?"
**Use Principle 1: Multi-constraint Management**

```
SYMPTOM: Designing a new system
APPROACH:
  1. Identify ALL constraints that must be satisfied
  2. Don't design for single constraint; design for ALL
  3. Check if constraints interact (coupling)
  4. Design for constraint interaction

EXAMPLES:
- Bridge design: Material strength + Joint integrity + Load capacity + Design correctness (all needed)
- Product design: Quality + Cost + Speed + Manufacturability (all matter)
- Organization design: Efficiency + Local autonomy + Information flow + Accountability (all matter)
- Software architecture: Performance + Maintainability + Scalability + Security (all matter)
```

### D2: "Should this be centralized or distributed?"
**Use Principle 7: Constraint Distribution Trade-offs**

```
See C2 above - same framework applies at design time
```

### D3: "What safeguards should we stack?"
**Use Principle 16: Constraint Stacking/Redundancy**

```
SYMPTOM: Designing for reliability
APPROACH:
  1. Identify possible failure modes
  2. Add independent constraint for each mode
  3. Don't strengthen one; add another
  4. Redundancy works when independent

EXAMPLES:
- Safety: Seatbelts + Airbags + Crumple zones (each prevents different failure mode)
- Immune: Central tolerance + Peripheral tolerance + Regulatory T cells (three independent layers)
- Financial: Audit + Internal controls + Segregation of duties (independent checks)
- Data: RAID 1 (two copies), RAID 6 (survives two failures)

DECISION TREE:
  What failure modes are possible?
    → List them
      → For each mode: Design constraint that prevents it
        → Verify constraints are independent
          → Verify that removes unacceptable failure modes
```

### D4: "How does this scale?"
**Use Principle 9: Scale-Dependent Constraints**

```
SYMPTOM: Designing for multiple scales
APPROACH:
  1. Constraints change with scale
  2. Test at different scales
  3. Adjust design for each scale

EXAMPLES:
- Ant colony: Distributed decision at scale 1000 works. Human organization scale 1000 needs hierarchy
- Building: Load-bearing design at 10 stories ≠ 100 stories
- Communication: Informal consensus at 5 people, formal voting at 500, political systems at 5 million

DECISION TREE:
  What's the operational scale?
    → Small (< 10): Decentralized works
    → Medium (10-1000): Hierarchy needed
    → Large (> 1000): Formal structure needed
      → Verify constraint types change with scale
        → Adjust design accordingly
```

### D5: "Should we constrain availability or require precision?"
**Use Principle 10: Constraint Precision vs Cost**

```
See C3 above - applies at design time too
```

### D6: "How do we position constraints temporally?"
**Use Principle 14: Temporal Constraint Positioning**

```
SYMPTOM: Designing for preparedness/response
APPROACH:
  1. Identify constraints that should be pre-positioned
  2. Pre-position before crisis
  3. Response time inversely related to preparation time

EXAMPLES:
- Vaccination: Pre-position immune memory without danger
- Infrastructure: Pre-build roads before growth (can't catch up after)
- Training: Build foundational skills early (can't catch up later)
- Disaster preparedness: Pre-position evacuation routes and supplies

DECISION TREE:
  Is this a crisis response scenario?
    → Yes: How much prep time available before crisis?
      → More time = more pre-positioning possible
        → Invest in pre-positioning to reduce response time
      → Less time = must position immediately
```

---

## E. FAILURE PREVENTION (How do we prevent catastrophe?)

### E1: "How do we prevent cascading failure?"
**Use Principle 2: Constraint Failure Cascades**

```
See B1 above - identify cascade triggers and prevent threshold crossing
```

### E2: "How do we detect hidden fragility?"
**Use Principle 12: Constraint as Metastable State**

```
See B4 above - monitor for perturbation sources and threshold-approach indicators
```

### E3: "How do we build redundancy that actually works?"
**Use Principle 16: Constraint Stacking/Redundancy**

```
See D3 above - stack independent constraints for each failure mode
```

### E4: "How do we identify what's really at risk?"
**Use Principle 8: Constraint Coupling**

```
SYMPTOM: Worried about unintended consequences of failure
APPROACH:
  1. Map constraint coupling
  2. Find which constraints, if failed, cascade
  3. Prioritize prevention/redundancy at cascade nodes

EXAMPLES:
- Which person's departure causes cascade? (key nodes in organizational structure)
- Which component's failure cascades? (key nodes in system architecture)
- Which market constraint, if removed, triggers cascade? (key nodes in market structure)
```

---

## F. INNOVATION PROBLEMS (How do we improve/change?)

### F1: "How do we safely explore new possibilities?"
**Use Principle 6: Constraint Removal as Exploration**

```
SYMPTOM: Want to innovate/explore but need to manage risk
APPROACH:
  1. Identify constraints protecting against bad outcomes
  2. Keep those constraints
  3. Temporarily remove constraints limiting exploration
  4. Explore within safe boundaries

EXAMPLES:
- R&D: Constrain immediate profit, explore future possibilities (remove short-term constraint)
- Play: Remove real-world consequences, keep safety constraints (controlled exploration)
- Therapy: Remove judgment/secrecy constraints, keep professional relationship constraint (safe exploration)
- Experimentation: Temporarily remove operational constraints, keep safety constraints

DECISION TREE:
  What constrains exploration?
    → Identify it
      → Is it a safety constraint or a limiting constraint?
        → Safety: Keep it
        → Limiting: Try removing it
          → If exploration yields discovery → keep constraint removed
          → If exploration yields risk → restore constraint
```

### F2: "Can adding constraint actually improve output?"
**Use Principle 18: Inverse Constraint (Constraining Increases Output)**

```
SYMPTOM: Trying harder isn't helping; need different approach
APPROACH:
  1. Instead of removing constraints, try adding them
  2. Some constraints enable output (counterintuitive)
  3. Test whether constraint improves performance

EXAMPLES:
- Meditation: Constrain thoughts → better mental health
- ML Regularization: Constrain weights → better generalization
- Error correction: Add redundancy → enables recovery
- Grammar: Constrain language → enables communication
- Property rights: Constrain ownership → enables cooperation
- Creative constraints: Constrain story length → more creative

DECISION TREE:
  Have we tried removing constraints and it didn't help?
    → Yes: Try the inverse - add constraint
      → Test if output improves
        → Yes: Keep constraint
        → No: Remove it
```

### F3: "How do we measure innovation progress?"
**Use Principle 13: Measurement/Observation as Constraint**

```
SYMPTOM: How do we measure something without changing it?
APPROACH:
  1. Choose measurement type based on what you need to know
  2. Accept that measurement constrains (changes) the system
  3. Select constraint type that's least harmful
  4. Use multiple measurement types for complete picture

EXAMPLES:
- Innovation measurement: Directly asking "are you creative?" constrains creativity
- Stock price: Measuring price influences price (can't measure without constraining)
- Psychological traits: Self-report changes behavior, behavioral observation doesn't
- Performance: Watching people work changes performance

DECISION TREE:
  What do you need to measure?
    → Choose measurement that reveals that specifically
      → Accept that measurement will constrain something
        → Use multiple measurement types to triangulate
          → Adjust for measurement-induced bias
```

---

## QUICK REFERENCE: PROBLEM TYPE → PRINCIPLES

```
PROBLEM                                    PRINCIPLE(S)
────────────────────────────────────────────────────────────────
"Something isn't working"                  1, 4, 15
"We tried a solution but it failed"        15
"We need to interpret a signal"            4
"Worried about sudden failure"             2, 5
"What will change if we change X?"         8
"System looks stable but fragile"          12
"Too much/too little constraint"           3
"Too slow or too fragile"                  7
"Cost vs precision tradeoff"               10
"People keep making mistakes"              11
"Should we build in backup?"               16
"This doesn't work at our scale"           9
"Want to explore safely"                   6
"More isn't helping; less isn't helping"   18
"Can't measure without changing result"    13
"Should we prepare in advance?"            14
"Different treatment needed"               15
"Fix is causing side effects"              8
"System is fragile"                        2, 12, 16
"Optimization plateau reached"             3, 18
```

---

## META APPROACH: When Stuck

If you can't identify which principle:

1. **What's the outcome?** (Better, Worse, Same, Collapse)
2. **What changed?** (One thing, Multiple, Nothing intentional)
3. **Is it continuous or discontinuous?** (Gradual, Sudden)
4. **Is it predictable?** (Always, Sometimes, Unpredictable)

These answers map to principle categories:
- Gradual + Multiple = Principle 3 (calibration)
- Sudden + Single = Principle 5 (threshold)
- Unpredictable + Multiple = Principle 2 (cascades) or Principle 12 (metastable)
- Continuous but unexpected = Principle 8 (coupling)

