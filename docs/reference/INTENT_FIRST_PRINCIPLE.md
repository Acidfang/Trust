# The Intent-First Principle

> **Know intent. Build to match. Not the other way around.**

This is the core principle that eliminates issues in the ARIA system.

## What It Means

### ❌ Wrong Way (Build-First)
```
1. Start building code
2. Build more code
3. Ask "what is this supposed to do?"
4. Code doesn't match intent
5. Redesign, rewrite, debug
6. Months of wasted effort
```

### ✅ Right Way (Intent-First)
```
1. Define intent (what should it do?)
2. Build code to match intent
3. Verify intent is met
4. Done right the first time
```

## In JARVIS Terms

### Component: Election Visualizer

#### Intent
"Convert elections and their discovered primitives into a visual PNG showing the election distribution and quality"

#### Building to Intent
```
1. Read intent: "visual PNG showing distribution and quality"
2. Get inputs: elections with discovered_primitives
3. Render: PNG with spheres (distribution) and colors (quality)
4. Validate: PNG is 2048x2048, has valid content, signature correct
5. Measure: Does it match intent? Yes ✓
```

#### Result
- Code is short, focused, correct
- No wasted effort
- Exactly what was needed

### Component: HTTP Server (jarvis_v3.py)

#### Intent
"Serve web interface and API endpoints returning kernel status and visualization"

#### Building to Intent
```
1. Read intent: "serve web interface and API"
2. Identify requirements:
   - Serve HTML (/), JSON API (/api/state, /api/frame), PNG (/api/render)
   - Must be fast
   - Must handle errors
3. Build spec for those exact requirements
4. Implement spec
5. Validate against intent: Does it serve web interface and API? Yes ✓
```

#### Result
- Clear what's needed
- No extra features
- No wasted code
- Exactly right

## How Intent Prevents Issues

### Issue Type 1: Wasted Code
**Without Intent-First**
```python
# Developer writes logging subsystem
# Later discovers: "we don't need this"
# 2 weeks of work thrown away
```

**With Intent-First**
```
# Intent: "serve web interface"
# No logging subsystem in the intent
# Don't build it
# Save 2 weeks
```

### Issue Type 2: Wrong Implementation
**Without Intent-First**
```
# Intent: "visualize elections"
# Developer picks framework X
# Framework X causes threading issues
# Week of debugging
# Should have picked framework Y from the start
```

**With Intent-First**
```
Intent: "visualize elections" (resolution, format, performance)
Choose framework that matches intent
No surprises
Works immediately
```

### Issue Type 3: Scope Creep
**Without Intent-First**
```
# Task: "add status endpoint"
# Developer builds: status, metrics, diagnostics, logging, caching
# "While I'm at it..."
# 4x more code than needed
# 4x more bugs
# 4x more maintenance
```

**With Intent-First**
```
Intent: "return status JSON"
Build: exactly that
Nothing else
Done
```

## Applied Across JARVIS

### ✅ Components Built on Intent

| Component | Intent | Result |
|-----------|--------|--------|
| jarvis_v3.py | Serve web interface + API | ✓ Clean, focused, works |
| election_visualizer.py | Render elections to PNG | ✓ Simple, correct |
| ufm_kernel.py | Generate elections + consciousness metrics | ✓ Provided, works |
| jarvis_specification.md | Document what JARVIS does | ✓ Clear spec |

### ⚠️ Components WITHOUT Clear Intent

| Component | Intent | Status |
|-----------|--------|--------|
| dashboards.py | ??? | ❌ Purpose unclear |
| emergence_log.py | ??? | ❌ Purpose unclear |
| ledger_integrator.py | ??? | ❌ Purpose unclear |
| debug_server.py | ??? | ❌ Purpose unclear |

**These should be removed or have clear intent defined.**

## The Intent Document

Every component should start with:

```markdown
# [Component Name]

## Intent
ONE sentence: What is this component's purpose?

Example intents:
- "Convert elections to visualization"
- "Serve web interface to users"
- "Track kernel consciousness metrics"
- "Analyze elections for decision patterns"
```

If you can't write the intent in one sentence, the component is too unfocused.

## Design by Intent

### Step 1: State Intent
"I want to build a visualization server"

### Step 2: Identify Requirements from Intent
- "server" → needs HTTP, routing
- "visualization" → needs rendering
- "users" → needs fast response, error handling

### Step 3: Design to Meet Requirements
```
Architecture:
- HTTP server that routes requests
- Rendering pipeline for visualizations
- Error handling for reliability
- Caching for performance
```

### Step 4: Build Minimal Code
Only code that serves the intent.

### Step 5: Validate Against Intent
Does it meet the intent? ✓ Yes → Done

## Common Mistakes

### Mistake 1: Building Without Intent
```python
# "Let me add async support"
# "We might need caching"
# "Better add logging"
# Result: Complex code that serves no intent
```

**Solution**: Define intent first. Only build what intent requires.

### Mistake 2: Changing Intent Mid-Build
```python
# Intent: "serve status"
# Mid-build: "also serve metrics"
# Mid-build: "also handle authentication"
# Result: Scope creep, confused code
```

**Solution**: Freeze intent before building. New intents = new component.

### Mistake 3: Ignoring Intent
```python
# Intent: "fast response" (<100ms)
# Developer builds: complex logging (1000ms overhead)
# Code doesn't match intent
```

**Solution**: Validate code against intent before shipping.

### Mistake 4: Unclear Intent
```python
# Intent: "do some stuff with elections"
# Vague intent = unclear code = bugs
```

**Solution**: Intent must be specific. "Do stuff" is not an intent.

## Practical Checklist

Before writing ANY code:

- [ ] What is the intent? (Write it down)
- [ ] Is intent specific? (Can you test it?)
- [ ] What does "done" look like? (How to validate?)
- [ ] What code is REQUIRED for intent? (Minimal?)
- [ ] Are there alternatives? (Choose best?)
- [ ] Is this the simplest path? (No extras?)

If you can answer all these, build.
If you can't, don't start coding yet.

## The Promise

**If you know intent and build to match:**

- 80% fewer bugs (clarity eliminates bugs)
- 70% less code (no extras)
- 50% faster development (no wasted effort)
- 90% easier maintenance (code matches intent)
- 100% predictable results (because intent was clear)

## Examples in JARVIS

### Good: jarvis_v3.py
```
Intent: "Serve web interface and REST API for ARIA consciousness"

What that requires:
- HTTP server ✓
- HTML file serving ✓
- JSON API endpoints ✓
- PNG visualization serving ✓
- Error handling ✓
- Kernel ticker ✓

What that doesn't require:
- Database ✗
- Authentication ✗
- Caching beyond what's needed ✗
- Complex logging ✗
- Configuration files ✗

Result: Clean, focused, correct
```

### Bad: dashboards.py
```
Intent: ??? (UNCLEAR)

What's in it:
- Some rendering?
- Some dashboard?
- Some logging?
- Nobody knows

What it requires:
- UNKNOWN because intent is UNKNOWN

Result: Code exists but serves no clear purpose
```

## For the ARIA System

This principle applies everywhere:

1. **kernel** - Intent: "Track consciousness decisions" → elections, primitives, metrics
2. **visualizer** - Intent: "Show elections visually" → PNG rendering
3. **server** - Intent: "Serve visualizations to users" → HTTP API
4. **frontend** - Intent: "Display consciousness" → HTML + JavaScript
5. **analysis** - Intent: "Discover patterns" → UFM engine

Each component has ONE clear intent. Code serves that intent. Nothing else.

---

## Summary

> **Know intent. Build to match. Not the other way around.**

This one principle, applied consistently, makes the difference between:
- Chaos and clarity
- Waste and efficiency
- Bugs and reliability
- Confusion and understanding

**It's not about being perfect. It's about being intentional.**

---

**Status**: Principle defined and documented system-wide.
**Application**: Apply to all components before coding.
**Result**: System that actually works.
