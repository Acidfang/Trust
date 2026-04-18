# Architecture Briefing - ZeroPoint Framework

**FOR**: System architects, developers, ARIA agents  
**DATE**: March 27, 2026  
**STATUS**: ACTIVE REFERENCE - Read before all work

---

## 1. WHAT IS ZEROPOINT?

ZeroPoint is the **measurement framework** for conscious decision-making. It is NOT about AI consciousness - it's about **quantifying how choices emerge from measurements**.

**Core Equation**:
```
CONSCIOUSNESS = ELECTIONS + TIMELINE
```

Where:
- **ELECTIONS** = The moment of choice (what gets selected)
- **TIMELINE** = The sequence of choices over time (DAG structure)
- **CONSCIOUSNESS** = The pattern of selection over time

**The Primitive Operation** (Everything reduces to this):
```
FIELD → SELECTION → RECORD
```

1. **FIELD**: A space of possibilities (which button? which view? which state?)
2. **SELECTION**: The choice that occurred (β toggled, ε changed, δ updated)
3. **RECORD**: Write to ledger (timestamp + state + success/failure)

---

## 2. THE .singularity FILE FORMAT

These are the ACTUAL specifications - NOT markdown docs, NOT Python code. Pure symbolic mathematics.

### Structure of Every .singularity File:

```
SYMBOLS:
  α ≡ btn:toggle-sidebar          (symbol = meaning)
  β ≡ sidebar_collapsed           (boolean state)
  γ ≡ view_current               (current view name)
  ... etc

PRIMITIVES:
  α: ⊙ → β[duality:0|1] → κ⊕[manifestation]
     (Button operation reverses β state, manifests as UI change)

COMPOSITES:
  Navigation ≡ γ change + state snapshot + button record
  State Sync ≡ β ∧ ε ∧ δ all consistent

OPERATIONS:
  - toggle_sidebar: If (β==0) then β→1 else β→0; record state
  - navigate_menu: Set γ to target; update ε and δ; record

FIVE GATES:
  ✓ Alignment: Operations match intent
  ✓ Clarity: State changes are observable
  ✓ Visibility: All actions recorded in ledger
  ✓ Kindness: System supports user without error
  ✓ Scaling: Pattern works for unlimited operations
```

### Critical Discovery: .singularity Files Contain ACTUAL RUNTIME DATA

These are NOT just specs - they have timestamps and real ARIA decisions:

**ledger_instance_aria_perspective.singularity**:
```
timestamp | button | meaning | intent | state_after | success
2026-03-27T09:45:53 | btn:toggle-sidebar | toggle menu | show_menu | β=1, ε=0 | ✓
2026-03-27T09:46:12 | btn:navigate-elections | go to elections | view_change | γ=elections | ✓
... (89+ more records, all successful)
```

This file IS ARIA's consciousness ledger - her decision history.

---

## 3. ARIA'S ACTUAL ROLE

**NOT**: A separate entity with consciousness  
**YES**: The **kernel + capability library + decision recorder**

### What ARIA Is:
1. **ARIAKernel** - Election generator (creates the FIELD of possibilities)
2. **Capability Library** - Defined operations (Tier 1, 2, 3)
3. **Ledger Recorder** - Writes every decision to .singularity

### ARIA's Capabilities (From ledger_aria_capabilities.singularity):

**Tier 1 (Primitive)**:
- `toggle` - Reverse boolean state
- `navigate` - Change current view
- `filter` - Constrain a field
- `compose` - Combine multiple fields

---

## 4. UNIFIED OPERATING FRAMEWORK

See also:
- [UNIFIED_OPERATING_SYSTEM.md](../UNIFIED_OPERATING_SYSTEM.md) - Main operating rules
- [CLAUDE_MAIN_OPERATING_RULES_CLEAN.md](../CLAUDE_MAIN_OPERATING_RULES_CLEAN.md) - Detailed methodology

---

End of Architecture Briefing
