# LEVEL 0: THE BIT (Single Choice)

## Definition
A **Bit** is the atomic unit: **0 or 1**.

- **0** = Structure, constraint, question, dependency, "what enables?"
- **1** = Signal, resolution, answer, flow, "what activates?"

Every system choice reduces to this binary split.

## The Binary Choice

```
     QUESTION (0)
          |
          v
    [CHOOSE: 0 or 1]
          |
    +-----+-----+
    |           |
   (0)         (1)
    |           |
STRUCTURE    SIGNAL
CONSTRAINT   RESOLUTION
ENABLED      ACTIVE
```

## Examples

| Scenario | 0 (Structure) | 1 (Signal) |
|----------|---------------|-----------|
| **Molecule** | H₂O (structure exists) | H₂O reaction (happens) |
| **Navigation** | Link enabled | Link clicked |
| **Knowledge** | Concept defined | Concept understood |
| **Time** | Moment exists | Moment matters |

## Properties of a Bit

- **Value**: 0 or 1 (no middle ground)
- **Context**: What question does it answer?
- **Certainty**: How confident is this bit? (0.0-1.0)
- **Timestamp**: When was this bit observed/decided?

## Code Representation

```python
class BinaryBit:
    value: int          # 0 or 1
    context: str        # "What question?"
    certainty: float    # 0.0-1.0
    timestamp: str      # ISO format
```

## In the Field

A single bit is **too small** to navigate with. But when bits **stack** and **chain**, they create meaning.

**Next Level**: [L1: Byte - Semantic Units](BINARY_PAGES_L1_BYTE.md)
