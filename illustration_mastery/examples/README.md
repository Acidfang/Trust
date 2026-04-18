# ILLUSTRATION EXAMPLES: Learning by Studying Meaning

This directory contains examples of meaningful illustrations—ones where every visual element encodes conceptual meaning.

## Generated Examples

### 1. decision_consequence_paths.svg
**Type**: State diagram with choice paths  
**Core principle**: Different choices (A/B/C) lead to fundamentally different consequences

**What the illustration encodes**:
- **Node size**: Severity of tension/unresolved state
- **Node color**: Whether state is resolved (green) or unresolved (red)
- **Node darkness**: Intensity of tension (darker = more unresolved)
- **Line color**: Type of consequence (red A-paths, green B-paths, orange C-paths)
- **Line style**: Solid = direct consequence, dashed = deferred consequence
- **Curved lines**: Paths that loop back (showing cyclical tension increase)
- **Straight down**: Path that leads to resolution

**What you can learn from this**:
- First glance: "There are three different paths from the same starting point"
- Closer look: "Path A and C look easier but get harder; path B is harder but resolves"
- Deep understanding: "The visual form teaches that avoidance and continuation are equivalent in their failure to resolve"

---

## Types of Meaningful Illustrations to Study

### Type 1: State Diagram (Decision Consequences)
Shows how systems progress through states and what choices are available at each.

**Examples to create**:
- [ ] TCHT Tier progression (each tier as a layer with states)
- [ ] Full decision tree (all 31 states in single visualization)
- [ ] Entry marker persistence (how markers carry through tiers)

### Type 2: Hierarchical Structure (System Architecture)
Shows how components relate and what hierarchy/containment exists.

**Examples to create**:
- [ ] System Rules (top level) → applies in each Tier → affects each State
- [ ] Tiers nested in layers (visual metaphor: foundation tiers at bottom)
- [ ] Entry markers hierarchy (how they originate, persist, resolve)

### Type 3: Conceptual Diagram (Abstract Principles)
Shows relationships between concepts using visual metaphor.

**Examples to create**:
- [ ] Coherence as continuous field (not binary on/off)
- [ ] Tension as potential energy (accumulation over time)
- [ ] Resolution as energy release (moving from high to low potential)

### Type 4: Timeline/Process Diagram (Sequence and Duration)
Shows how things unfold and relative importance of each phase.

**Examples to create**:
- [ ] A choice consequence timeline (tension builds, then either loops or resolves)
- [ ] Tier progression (duration relative to depth/complexity)
- [ ] Entry marker lifecycle (origin → growth → resolution)

### Type 5: Matrix Visualization (Relationships Across Dimensions)
Shows patterns across multiple variables.

**Examples to create**:
- [ ] Entry markers across states (which markers appear where)
- [ ] Consequences across choice types (what happens with A/B/C)
- [ ] States across tiers (visual map of all 31 states organized by tier)

### Type 6: Interactive Diagram (User-Driven Exploration)
Shows how interaction reveals meaning.

**Examples to create**:
- [ ] Hover state markers → show where they appear in next tier
- [ ] Click a state → highlight all paths in/out of it
- [ ] Toggle entry marker → see how weight changes through system

---

## How to Read These Illustrations

### Level 1: Casual Viewing (30 seconds)
What's the main idea? Look at:
- Overall shape and structure
- Which elements are largest/most prominent
- Color patterns

### Level 2: Engaged Study (3-5 minutes)
What relationships exist? Look at:
- How elements connect
- What patterns repeat
- Which elements are similar

### Level 3: Expert Analysis (15+ minutes)
What mental model does this teach? Ask:
- Why is this shaped this way?
- What does each visual choice communicate?
- What would be different if design variables were changed?
- What would you learn differently if colors were swapped?

---

## Building Your Own Meaningful Illustration

### Process:

1. **START**: Choose ONE core principle you want to teach
   - Bad: "I want to show the entire TCHT system"
   - Good: "I want to show that A-path choices increase tension cyclically"

2. **IDENTIFY**: What's the visual form that naturally shows this principle?
   - Principle: "Things accumulate and get heavier"
   - Form: Progressive darkening or size increase
   - Not: Random colors/sizes

3. **MAP**: For each concept, pick a visual variable
   - Concept: "Severity of tension"
   - Visual variable: Node size or color darkness
   - Consistent: Always use the same variable for the same concept

4. **BUILD**: Create the illustration using your mappings
   - Use SVG, Canvas, ASCII, or whatever fits
   - Make sure 70% is understandable without labels

5. **VERIFY**: Does every element teach?
   - If you removed that element, is the core message unclear?
   - If not, remove it (non-essential decoration)

6. **TEST**: Can someone understand at all 3 levels?
   - Casual: Main idea clear?
   - Engaged: Relationships visible?
   - Expert: Mental model sound?

---

## Tools Available

### SVG (Scalable Vector Graphics)
```python
from illustration_generator import MeaningfulIllustrationBuilder

builder = MeaningfulIllustrationBuilder(width=800, height=600)
builder.set_color_scheme('default')
builder.add_state_node(x=400, y=300, state_id='T1.1', severity=2, is_resolved=False)
builder.save_svg('my_illustration.svg')
```

**When to use**:
- Technical diagrams
- Scalable (works at any size)
- Editable in any text editor
- Embeds in web and documents

### ASCII Art (Text-based)
```
    [Unresolved]
       |
   A / | \ B
    /  |  \
    V  V   V
[Cycle][Resolved]
       |
       C → [Deferred]
```

**When to use**:
- Documentation
- Terminal/CLI
- Accessibility
- Maximum portability

### Interactive (HTML Canvas / JavaScript)
```html
<canvas id="diagram"></canvas>
<script>
  // Draw with meaning encoding
  // Canvas coordinates map to concepts
  // Events reveal deeper relationships
</script>
```

**When to use**:
- Interactive exploration
- Real-time updates
- Animations showing change over time

---

## Design Principles Checklist

For every illustration, verify:

- [ ] **One core principle**: Single clear idea being taught
- [ ] **Visual form matches concept**: Shape/style naturally shows the principle
- [ ] **No arbitrary choices**: Every color/size/position has meaning
- [ ] **Consistent language**: Same visual variable always means same thing
- [ ] **Multi-level understanding**: Works at casual, engaged, and expert levels
- [ ] **70% readable without labels**: Could someone understand without words?
- [ ] **Essential elements only**: Everything present teaches something
- [ ] **Right mental model**: Visual form teaches the correct understanding

---

## Example: Studying an Illustration

Take any completed illustration and ask:

**What is the core principle?**
"This illustration teaches that avoidance defers costs rather than eliminating them"

**How does the visual form show this?**
"The C-path (avoidance) curves sideways and downward to a future tier at higher severity than the original issue"

**What would change if design was different?**
- If C-path went straight up instead of sideways → teaches "avoidance prevents progress"
- If C-path ended at same severity → teaches "avoidance maintains status quo"
- If C-path disappeared → teaches "avoidance is impossible"

**What does this teach implicitly?**
- The C-path design teaches "the cost reappears later" more effectively than a label

---

## Next Steps

1. **Study** the generated examples and identify what each visual choice means
2. **Modify** an example and notice how changing design variables changes what's taught
3. **Create** your first meaningful illustration using the generator
4. **Build** illustrations for your own domain using the framework
5. **Teach** others by having them read your illustrations

The goal: Master creating illustrations where the visual form is the teacher, not the labels.

---

**Status**: [Illustration Examples Generated ✓]

Every illustration in this directory demonstrates the principle: visual form encodes meaning.

Study them. Understand why every element is where it is. Then create your own.
