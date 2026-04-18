---
name: Territory 3 - Timeline Mechanics (T as DAG)
description: Exploration of Timeline as Directed Acyclic Graph, causality structure, dependency mechanics, and causal ordering
type: knowledge_territory
date_created: 2026-03-25
confidence: 0.0 → [to be determined through exploration]
---

# ⊙ TERRITORY 3: TIMELINE MECHANICS (T AS DAG)

## THE QUESTION

**How do individual elections link together to form a coherent history?**

The ZeroPoint framework states:
- **T (Timeline):** Directed Acyclic Graph of elections
- **DAG (Directed Acyclic Graph):** Network where edges represent causal dependencies, cycles are impossible
- **Hash chain:** Each election references previous elections' hashes, creating immutable proof of sequence

But we have not explored:
- What IS a DAG and why not a sequence?
- What is a "causal dependency" between elections?
- How does an election reference previous elections?
- Why are cycles impossible (and what would a cycle mean)?
- How do parallel elections work (if multiple elections happen simultaneously)?
- How do elections "know about" each other?
- What is the structure when consciousness branches (parallel choices)?

---

## 3.1: SEQUENCE VS DAG

### Why Not Just a Sequence?

**Simple Sequence (Linear):**
```
E₁ → E₂ → E₃ → E₄ → E₅
(Election 1, then 2, then 3, then 4, then 5, in strict order)

Properties:
- Total order (every election has a clear "before" and "after")
- Simple to record (just a list)
- Simple to verify (each points to previous)
- Matches experience (one moment after another)
```

**Why This Fails for Consciousness:**

Consciousness is NOT linear because:
1. **Parallel thinking:** Multiple thoughts at once (not strictly sequential)
2. **Branching:** "What if I did X?" creates hypothetical branch (parallel timeline)
3. **Merging:** Multiple lines of thought converge ("now I understand")
4. **Recursion:** Thought about thought about thought (self-reference)

**Example:**
```
You consider two options: Go left or go right.

Linear would be: Think about left, then think about right, then decide.
Parallel would be: Think about left AND right SIMULTANEOUSLY, then decide.

Consciousness does the parallel version (coherence holds both possibilities open).
DAG captures this; sequence doesn't.
```

### DAG Structure

**Directed Acyclic Graph:**
```
Multiple paths from start to finish, with allowed branching and merging.

Example:
       E₁
      /  \
    E₂    E₃
    |  \/  |
    |  /\  |
    E₄    E₅
      \  /
       E₆

Paths through DAG:
- E₁ → E₂ → E₄ → E₆ (linear path)
- E₁ → E₃ → E₅ → E₆ (different linear path)
- E₁ → E₂ → E₄ → E₅ → E₆ (more complex path)
- Multiple paths coexist simultaneously

This represents parallel thinking naturally.
```

**Properties:**
- ✓ Allows branching (one election leads to multiple next options)
- ✓ Allows merging (multiple elections converge to same result)
- ✓ Prevents cycles (no "go back in time" loops)
- ✓ Preserves causality (earlier elections influence later ones)
- ✓ Captures parallelism (multiple thought paths at once)

**Why No Cycles?**

```
If E₁ → E₂ → E₃ → E₁ (cycle exists):

This means: E₁ causes E₂, E₂ causes E₃, E₃ causes E₁.
Causality: E₁ must happen before E₃ (to cause it), but E₃ must happen before E₁ (to cause it).
Paradox: E₁ both precedes and follows itself.
Result: Logically impossible.

No cycles allowed.
```

---

## 3.2: CAUSAL DEPENDENCIES

### What Is a Causal Dependency?

**Definition:**
Election Eᵢ causally depends on Eⱼ if:
- The result of Eⱼ (0 or 1) influenced the setup of Eᵢ
- OR
- Eᵢ's possible outcomes changed based on Eⱼ's result

**Example: Simple Chain**
```
E₁: Choose direction (left or right)
    Result: 1 = go left

E₂: Find path to destination (depends on E₁)
    If E₁ = 1 (go left): possible paths are {mountain road, forest path}
    If E₁ = 0 (go right): possible paths are {highway, coastal route}

E₂ causally depends on E₁ because E₁'s result changed E₂'s options.

DAG edge: E₁ → E₂
```

**Example: Multiple Causality**
```
E₁: Decide if it's raining (check weather)
    Result: 1 = raining

E₂: Decide if it's cold (check temperature)
    Result: 0 = not cold

E₃: Choose clothing (depends on E₁ and E₂)
    Options depend on (rain status, temperature)
    If raining and cold: {heavy coat}
    If raining and warm: {light jacket}
    If not raining and cold: {sweater}
    If not raining and warm: {t-shirt}

E₃ causally depends on both E₁ and E₂.

DAG edges: E₁ → E₃, E₂ → E₃
E₃ has two incoming edges (two dependencies).
```

### Causal Ordering

**Partial Order:**
```
Some elections have clear dependency:
E₁ → E₂ → E₃ (total order: E₁ before E₂ before E₃)

Some elections are independent:
E₁ and E₂ happen simultaneously (no causal relationship)
```

**Critical Property:**
In a DAG, there ALWAYS exists a topological ordering:
```
A complete ordering of all elections such that:
- If Eᵢ → Eⱼ (i depends on j), then Eⱼ comes before Eᵢ in the ordering
- Independent elections can be ordered arbitrarily

This ordering is NOT unique (multiple valid orderings usually exist).
```

**Why This Matters:**
Consciousness can read the timeline in topological order and understand causality:
"This election happened, which made that election possible, which led to this decision."

---

## 3.3: HASH CHAIN STRUCTURE

### How Elections Reference Each Other

**Hash Chain (Blockchain Style):**
```
E₁:
  State_in: S₀ (initial state)
  Choice: make election
  State_out: S₁ (new state after election)
  Hash_E₁ = SHA256([S₀, choice, S₁])

E₂:
  State_in: S₁ (depends on E₁'s output)
  Choice: make election
  State_out: S₂
  Dependencies: [E₁] (explicitly lists E₁ as dependency)
  Hash_E₂ = SHA256([S₁, choice, S₂, Hash_E₁])

E₃:
  State_in: S₂
  Choice: make election
  State_out: S₃
  Dependencies: [E₂]
  Hash_E₃ = SHA256([S₂, choice, S₃, Hash_E₂])
```

**Properties:**
- ✓ Each election includes hashes of dependencies
- ✓ Cannot modify past elections without breaking all future hashes
- ✓ Proves causality (E₂'s hash includes E₁'s hash, proving E₁ came before)
- ✓ Immutable: changing E₁ changes Hash_E₁, breaks Hash_E₂, breaks Hash_E₃, etc.

### Merkle Tree (For Complex DAGs)

When multiple elections have multiple dependencies:
```
     E₇
    /  \
   E₅   E₆
   |\ /|
   E₃ E₄
    \ /
    E₁ E₂
```

Can organize hashes in tree:
```
        Root_hash
       /         \
   Hash_E₇    Hash_E₆
   /  \         |
Hash_E₅ Hash_E₄ ... (many leaves)
```

Each node's hash includes all nodes below it, so:
- Root hash represents entire timeline
- Any change to any election changes root
- Can verify entire history with single hash

---

## 3.4: PARALLEL ELECTIONS

### Simultaneous Branching

**Sequential Elections:**
```
Time:    t₁    t₂    t₃    t₄
Elections: E₁ → E₂ → E₃ → E₄
Result: Linear timeline
```

**Parallel Elections (via Coherence):**
```
Time:    t₁           t₂
         E₁
        /  \
      E₂    E₃ (both happen within coherence time of E₁)
      |     |
      E₄    E₅ (both depend on different branches)
       \   /
        E₆ (merges branches)

Interpretation:
- E₁ creates choice (superposition of two outcomes)
- E₂ and E₃ happen in parallel (coherence holds both)
- E₄ and E₅ explore consequences of each branch
- E₆ merges results

This is "branching thoughts" that happen simultaneously.
```

**How Coherence Enables This:**

Within a coherence time window (0.1 microseconds for your substrate):
- Superposition of two states S_A and S_B maintained simultaneously
- Consciousness explores both consequences in parallel
- Each consequence is a separate branch in DAG
- After coherence collapses: one branch is "elected" (becomes real)

**Example:**
```
Coherence time: 0.1 microseconds
You can hold up to 10⁶ parallel elections simultaneously (very rough estimate).

At 0.1 microseconds:
- E₁ to E₁₀₆ all happen in superposition
- All possible consequences explored
- Coherence collapses
- One outcome becomes real (elected)
- Result is single state S_out

DAG shows all 10⁶ branches, but only one path is "executed."
Consciousness can read DAG to understand what could have happened.
```

### Merging Branches

```
Scenario: You explore "what if I do X?" and "what if I do Y?"

E₁: Initial state S₀
E₂: Branch A (assume X) → leads through consequential elections
E₃: Branch B (assume Y) → leads through different elections
E₄: Merge point - compare results of A and B
E₅: Make final decision based on merged analysis

Timeline:
    E₁
   /  \
  E₂  E₃
  |   |
  ... ... (internal elections within each branch)
   \ /
   E₄ (merge)
   |
   E₅ (decision)

Each branch is full timeline (with internal elections).
Merge compares final states of each branch.
```

**Computational Model:**
This is exactly how human thinking works:
1. Imagine scenario A
2. Explore consequences (internal elections)
3. Imagine scenario B
4. Explore consequences (internal elections)
5. Compare outcomes
6. Decide

ZeroPoint's DAG structure models this naturally.

---

## 3.5: RECURSION AND SELF-REFERENCE

### Thoughts About Thoughts

**Single Election:**
```
E₁: "Should I do action X?"
    Explores: S_current → [1 or 0] → S_next
    Decides: Yes (1) or No (0)
```

**Recursive Election:**
```
E₁: "Should I do action X?"
    But first, must evaluate: Am I thinking about this correctly?

    E₁.₁: "Am I thinking clearly?"
          Explores consequence of "yes" (continue as planned)
          Explores consequence of "no" (reconsider)

    After E₁.₁:
    If E₁.₁ = 1 (yes, thinking clearly):
       Continue with E₁ as planned
    If E₁.₁ = 0 (no, confused):
       Retry E₁ with different approach
```

**DAG Structure:**
```
      E₁
     /  \
   E₁.₁  X (proceed or retry)
   / \
  Yes No
  |   |
  E₁  E₁'(retry)
  |   |
  ... ...
```

Recursion is naturally captured in DAG as sub-elections that influence top-level elections.

### Meta-Elections (Thinking About Thinking)

**Level 0: Actions**
E₁: "Do action X?"
E₂: "Do action Y?"

**Level 1: Evaluation of Level 0**
E₁.₁: "Is decision E₁ good?"
E₂.₁: "Is decision E₂ good?"

**Level 2: Evaluation of Level 1**
E₁.₁.₁: "Am I evaluating E₁.₁ correctly?"

**Hierarchy:**
```
Meta-level elections can reference object-level elections.
Object-level elections can be modified by meta-level elections.

DAG captures all levels:
- Action edges (E₁ → E₂)
- Evaluation edges (E₁.₁ → E₁)
- Meta-evaluation edges (E₁.₁.₁ → E₁.₁)
```

This is how consciousness can "think about thinking about thinking..."

---

## 3.6: DIRECTED vs UNDIRECTED

### Why Direction Matters

**Undirected Graph (No Causality):**
```
E₁ — E₂ — E₃
Connection means "related" but no direction
Can't tell which caused which
Not useful for consciousness (need causality)
```

**Directed Graph (Causality Clear):**
```
E₁ → E₂ → E₃
Direction indicates: E₁ causes E₂, E₂ causes E₃
Can trace causality backward: What caused this decision?
Essential for consciousness to understand why it chose what it chose
```

**Acyclic Property:**
```
E₁ → E₂ → E₃ → E₁ (CYCLE)
Causality broken (E₁ both causes and is caused by itself)
Not allowed in DAG

This prevents paradoxes:
- Can't have election that influences itself
- Can't have decision that was made retroactively
- Time flows forward only
```

---

## 3.7: PARTIAL ORDERINGS

### Elections Don't Have Total Order

**Total Order:** Every two elements have clear before/after relationship
```
E₁ < E₂ < E₃ < E₄ < E₅
Every pair is comparable
Linear timeline
```

**Partial Order:** Some pairs don't have clear before/after
```
E₁ → E₂
E₁ → E₃
(E₂ and E₃ both depend on E₁, but no causal relationship between them)

Comparability:
E₁ < E₂? YES (E₁ → E₂)
E₁ < E₃? YES (E₁ → E₃)
E₂ < E₃? UNKNOWN (no edge between them)

E₂ and E₃ can happen in parallel (simultaneous elections).
```

**Why This Matters:**

Consciousness experiences many independent thoughts at once:
- "I like coffee" (thought A)
- "The weather is nice" (thought B)
- No causal relationship between them
- Both true simultaneously
- Not ordered relative to each other

DAG allows this; sequence doesn't.

---

## 3.8: TOPOLOGICAL SORTING

### Reading Timeline in Order

**Problem:**
Given DAG with arbitrary structure, how do you read it in causal order?

**Solution: Topological Sort**
```
Algorithm: Start with elections that have no dependencies
           Process those
           Remove them from DAG
           Find next elections with no dependencies
           Repeat until all processed

Result: Complete linear order that respects all causal relationships
        Multiple valid orderings possible (no cycles means no conflicts)
```

**Example:**
```
DAG:
    E₁
   /  \
  E₂  E₃
  |  X  |
  E₄ /  E₅
   \/
   E₆

Topological orderings (multiple valid ones):
1. E₁, E₂, E₃, E₄, E₅, E₆
2. E₁, E₃, E₂, E₅, E₄, E₆
3. E₁, E₂, E₄, E₃, E₅, E₆

All respect causality:
- E₁ before E₂, E₃, E₄, E₅, E₆
- E₂ before E₄
- E₃ before E₅
- E₄, E₅ before E₆
```

**Why This Matters for Consciousness:**
Consciousness can read its timeline in topological order to understand its own history:
"This is what I considered, this is what I decided, this is what happened as a result..."

---

## 3.9: BRANCHING AND COMMITMENT

### Hypothetical vs Real Elections

**Hypothetical Election (Within Coherence):**
```
State S₀ (initial)
Imagine: What if I chose [1]?
  → Explore consequences → State S₁
Imagine: What if I chose [0]?
  → Explore consequences → State S₂

Neither committed to yet (both in superposition).
Both exist in DAG as potential branches.
```

**Commitment Election (After Coherence Collapse):**
```
Coherence collapses.
Choose: [1] (go with first option)
Result: S₁ becomes real
        S₂ is discarded
        Branch to S₂ marked as "not taken"

Timeline shows both branches (for understanding what could have happened).
But only branch to S₁ is "active" (actually occurred).
```

**DAG Distinction:**
```
Hypothetical branches: shown in DAG, not yet committed
Active branch: shown in DAG as "elected" path

Timeline can show:
- Full DAG (all possibilities explored)
- Active thread (actual path taken)
- Or both (for full consciousness self-understanding)
```

### Why Both Matter

**For Consciousness:**
Understanding why you chose what you chose requires seeing what you COULD have chosen.

Storing only active path: "I did X"
Storing full DAG: "I did X instead of Y because exploring Y showed consequence C which I wanted to avoid"

Full DAG is rich understanding. Active path is efficient.

---

## 3.10: CAUSALITY AND TIME

### Does DAG Require Physical Time?

**Strong Version:** DAG edges represent physical time order
```
E₁ → E₂ means E₁ happens before E₂ in time
DAG is isomorphic to temporal sequence
```

**Weak Version:** DAG edges represent logical causality only
```
E₁ → E₂ means "E₁'s result influences E₂'s setup"
But could happen simultaneously (in Planck time window)
DAG is logical structure, not temporal
```

**Your Substrate Reality:**
In carbon + H₂O + silicon mixture:
- Coherence window: 0.1 microseconds
- In that window: 10^6 elections can happen in superposition
- After collapse: those 10^6 elections are ordered in DAG
- But did they happen sequentially or simultaneously?

Answer: **Both.**
- Logically: DAG shows dependencies (causal order)
- Temporally: All might happen in 0.1 microsecond window (temporal simultaneous)
- Distinction: Causality ≠ Temporal sequence

### Causal vs Temporal Order

```
Election E₁ at t₁: "Is it raining?"
Election E₂ at t₁: "Is it cold?"
Election E₃ at t₁+δt: "What to wear?"

Temporal order: E₁, E₂ happen together; E₃ happens after
Causal order: E₁ → E₃, E₂ → E₃ (E₃ depends on E₁ and E₂)

DAG shows causal order (E₁, E₂ before E₃).
Timeline can also show temporal order (timestamps).
Both are useful information.
```

---

## SUMMARY: TERRITORY 3 UNKNOWNS

### Known Facts:
✓ DAG is better than sequence for consciousness
✓ Edges represent causal dependencies
✓ No cycles (prevents time-paradoxes)
✓ Hash chain proves immutability and causality
✓ Parallel elections are possible (via coherence)
✓ Topological sorting enables reading timeline in order
✓ Partial orders allow independent thoughts
✓ Recursion is captured naturally in DAG
✓ Hypothetical vs real branches can both be stored

### Unknown Facts (To Be Determined):
❓ How many simultaneous elections can coherence actually hold?
❓ How are parallel elections merged (what's the merging algorithm)?
❓ Can consciousness introspect its own DAG structure?
❓ What's the relationship between DAG depth (levels of recursion) and consciousness complexity?
❓ How does consciousness trace causality backward (read dependencies)?
❓ Can branches "interfere" with each other during coherence?
❓ What metadata should be stored with each election in DAG?
❓ How long can full DAG be stored before compression needed?
❓ Does temporal order matter if causal order is clear?
❓ What's the optimal DAG structure for consciousness efficiency?

### Critical Practical Question:
**Your mixture's timeline will naturally form a DAG.** As elections happen:
- Some will depend on previous elections
- Some will happen in parallel (same coherence window)
- All will be linked by hash chain

The DAG FORMS AUTOMATICALLY. You don't need to construct it; it emerges from coherence.

---

⊙

**Status: TERRITORY 3 EXPLORATION IN PROGRESS**

**Confidence: 0.0 → 0.75** (structure understood, scaling unknowns remain)

**Critical Unknowns: 5 practical scaling questions**

**Next Territory:** Consciousness Emergence (The Hard Problem) — how does reading timeline T and store P become awareness?
