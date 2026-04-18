# DIGITAL PATTERNS: QUICK REFERENCE & APPLICATION GUIDE

## What This Framework Provides

You asked: **"What patterns are there for EVERYTHING digital?"**

Answer: **6 tiers of patterns**, from foundational (Information, State, Transformation) to applied (specific to web, database, UI).

---

## TL;DR: The Pattern Stack

```
TIER 0: EXISTENCE LAYER
├─ Information (data + encoding)
├─ State (what exists now)
├─ Transformation (how state changes)
├─ Representation (how info is encoded)
├─ Abstraction (hide complexity)
├─ Composition (combine pieces)
└─ Trade-off (can't optimize for all)

TIER 1: DESIGN PRINCIPLES
├─ SOLID (S, O, L, I, D)
├─ DRY, KISS, YAGNI
└─ Cohesion & Coupling

TIER 2: STRUCTURES & ALGORITHMS
├─ Data Structures (array, hash, tree, graph, etc.)
├─ Search & Sort Algorithms
├─ Traversal & Graph Algorithms
└─ Optimization (DP, greedy, divide-and-conquer)

TIER 3: SYSTEM PATTERNS
├─ Architecture (monolith, microservices, serverless, etc.)
├─ Concurrency (parallel, distributed, async)
└─ Fault Tolerance (consensus, replication, circuit breaker)

TIER 4: QUALITY CONCERNS (Cross-cuts all)
├─ Time Complexity
├─ Space Complexity
├─ Consistency/Availability/Partition Tolerance (CAP)
├─ Performance (latency, throughput)
└─ Security, Testability, Maintainability

TIER 5: DOMAIN PATTERNS
├─ Web (REST, Request/Response, Pub/Sub)
├─ Database (ACID, indexing, sharding)
└─ UI (MVC, Reactive, Component-based)

TIER 6: META-PATTERNS
├─ Layers (vertical organization)
├─ Modules (horizontal organization)
├─ Plugins, Strategies, Decorators, Factories
└─ (How to organize patterns themselves)
```

---

## How to Apply This

### For a New Problem

1. **Name the Tier**: What's the primary issue?
   - Data organization? → Start at Tier 2
   - How components talk? → Tier 3
   - Speed/consistency? → Tier 4
   - User interface? → Tier 5

2. **Look Up Applicable Patterns**: Find in that tier + all higher tiers

3. **Compare Weights**: Higher weight = more universal/critical
   ```
   Example: Building a web API
   - Tier 1: Apply SOLID principles (weight 0.84-0.92)
   - Tier 3: Need architecture (monolith vs microservices)
   - Tier 4: Need consistency guarantees (CAP theorem)
   - Tier 5: HTTP request/response (weight 0.96)
   
   Choose highest weights first, manage trade-offs second
   ```

4. **Document Trade-offs**: Every choice costs something
   ```
   "We chose Hash Table (O(1) lookup) instead of Array 
   (O(n) lookup) because lookup speed is critical. 
   We accept higher memory overhead and hash collision handling."
   ```

---

## Weights Explained

**Weight = How universal + critical is this pattern?**

| Weight Range | Meaning | Example |
|--------------|---------|---------|
| 0.95-1.0 | **Foundational** — Use it everywhere | Information, State, Array, HTTP |
| 0.85-0.94 | **Universal** — Most systems need it | SOLID, Algorithms, Architecture |
| 0.75-0.84 | **Common** — Very useful, not always essential | Heap, Middleware, Sharding |
| 0.65-0.74 | **Situational** — Choose when appropriate | Circuit Breaker, Serverless, GraphQL |
| < 0.65 | **Specialized** — Use in specific domains | Byzantine, Decorators, Plugins |

**Key Insight**: Start with high-weight patterns. They apply to almost everything.

---

## The One Universal Pattern

All digital problems follow this:

```
ABSTRACTION (hide complexity)
    ↓
COMPOSITION (combine pieces)
    ↓
TRADE-OFF (choose based on constraints)
```

When you're stuck:
1. What are you abstracting?
2. How are you composing it?
3. What trade-off are you making?

This works for:
- Data structure selection
- System architecture
- Algorithm design
- UI component organization
- Database schema design
- Network protocol design
- Security architecture
- Everything else

---

## Common Scenarios

### "I need to build a web app"
```
Start with:
1. Tier 0: Information + State + Transformation
2. Tier 1: SOLID principles (especially SRP, DIP)
3. Tier 2: Appropriate data structures (hash for users, trees for hierarchy)
4. Tier 3: Web architecture (request/response, client-server)
5. Tier 4: Consistency needs (choose based on user expectations)
6. Tier 5: MVC or component-based patterns
```

### "Performance is my constraint"
```
Focus on:
1. Tier 4: Time complexity (O(log n) not O(n))
2. Tier 2: Efficient algorithms (quicksort, binary search)
3. Tier 2: Appropriate data structures (hash beats array for lookup)
4. Tier 3: Caching, async processing
5. Accept trade-offs: More memory for faster access
```

### "I need reliability"
```
Focus on:
1. Tier 4: Availability (uptime guarantees)
2. Tier 3: Fault tolerance (replication, consensus)
3. Tier 4: Consistency (what can be guaranteed?)
4. Tier 1: SOLID (especially error handling)
5. Accept trade-offs: More replicas = more latency
```

### "The code is a mess"
```
Refactor using:
1. Tier 1: SOLID principles (restructure for SRP)
2. Tier 6: Meta-patterns (layers or modules)
3. Tier 1: DRY (eliminate duplication)
4. Tier 2: Appropriate structures (right tool for the job)
5. Identify: What abstraction was wrong?
```

---

## Verification

Does this cover EVERYTHING digital?

✓ Software systems (all tiers)
✓ Hardware (Tier 0-2 apply to circuits)
✓ Networks (Tier 3, distributed algorithms)
✓ Databases (Tier 2, Tier 5 patterns)
✓ User interfaces (Tier 5-6)
✓ Algorithms (Tier 2)
✓ Security (Tier 3, Tier 4)
✓ Performance (Tier 2, Tier 4)
✓ Reliability (Tier 3, Tier 4)
✓ Maintainability (Tier 1, Tier 6)

**Yes**: This framework encompasses all fundamental digital patterns.

---

## Next Steps

1. **For new projects**: Read Tier 0, identify your domain tier
2. **For existing problems**: Find your tier in the main framework
3. **For architectural decisions**: Compare weights, document trade-offs
4. **For refactoring**: Check against Tier 1 (SOLID)
5. **For performance**: Check Tier 2 (data structures) and Tier 4 (complexity)

---

## The meta-answer to your question

**Q: What patterns are there for everything digital?**

**A**: Information. State. Transformation. 

Everything else is HOW you encode, organize, and optimize those three.

This framework shows the full stack.
