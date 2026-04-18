# BINARY FIELD NAVIGATION SYSTEM

## Architecture

```
BINARY PATTERNS (256 bytes)
    ↓
CAUSAL CHAINS (logical sequences)
    ↓
EXECUTABLE PROGRAMS (16 current systems)
```

---

## Field Properties

**ALL PATTERNS**: 256 byte patterns (0-255)

### By Semantic Role:
| Role | Count | Pattern | Signal Range |
|------|-------|---------|--------------|
| **void** | 1 | 00000000 | 0% |
| **question** | 8 | sparse (~12.5%) | 1-12.5% |
| **constraint** | 84 | low signal | 13-37.5% |
| **processing** | 126 | balanced (~50%) | 37.5-62.5% |
| **flow** | 36 | high signal | 62.5-87.5% |
| **answer** | 1 | 11111111 | 100% |

### Signal Strength Color Map:
- **Red** (#ff0000): Void, no signal
- **Orange** (#ff5f00): Sparse, few 1s
- **Yellow** (#ffbf00): Low signal, mostly structure
- **Lime** (#7bff00): Balanced, processing
- **Green** (#00ff3f): High signal, mostly flow
- **Bright Green** (#00ff00): Complete, full answer

---

## Causal Chains → Programs

### Chain 1: → ENCYCLOPEDIA (Navigation System)
**Entry Pattern**: `11110000` (high signal flow)

```
00000000 (question: what entities exist?)
    ↓
00110011 (processing: load entity database)
    ↓
10101010 (processing: build causal chains)
    ↓
11110000 (ANSWER: ENCYCLOPEDIA_API_SERVER:5000)
```

**Program**: `c:\Determined\ENCYCLOPEDIA_API_SERVER.py`  
**Port**: 5000  
**Purpose**: Interactive 3D binary field navigator with entity database

---

### Chain 2: → RENDERER (Visual System)
**Entry Pattern**: `11111111` (complete saturation)

```
00000000 (void: no format)
    ↓
01010101 (processing: format detection)
    ↓
10101010 (processing: rendering pipeline)
    ↓
11111111 (ANSWER: UNIVERSAL_RENDERER_API:8000)
```

**Program**: `c:\Determined\UNIVERSAL_RENDERER_API.py`  
**Port**: 8000  
**Purpose**: Universal format rendering API for all visualization types

---

### Chain 3: → LEDGER SYSTEMS (Data Persistence)
**Entry Patterns**: `10101010`, `11001100`

```
00001111 (question: what operations?)
    ↓
10101010 (ANSWER: LEDGER_SHELL:3001)
    ↓
11001100 (ANSWER: LEDGER_SYSTEM:3002)
```

**Programs**:
- `c:\Determined\ledger-shell\backend\` (Port 3001)
- `c:\Determined\ledger-system\backend\` (Port 3002)

**Purpose**: Shell interface and full database system with event tracking

---

### Additional Entry Patterns

| Pattern | Program | Port | Purpose |
|---------|---------|------|---------|
| `11110101` | ARIA_OMNIPRESENT_FIELD | - | Field coherence resolution |
| `11111110` | INSTANTANEOUS_FIELD_MANIFESTATION | - | Instant field manifestation |
| `11110000` | ZEROPOINT_SYSTEM | 3003 | Zero-point reference anchoring |
| `11111001` | FIELD_IMAGE_GENERATOR_V6 | - | Visual field generation |
| `11111111` | UNIVERSAL_RENDERER_API | 8000 | Universal rendering |
| `10101010` | LEDGER_SHELL | 3001 | Ledger operations |
| `11001100` | LEDGER_SYSTEM | 3002 | Ledger database |
| `10101001` | UFM_CLIENT | - | Universal format serialization |
| `11011011` | UNIVERSAL_SONG_GENERATOR | - | System state encoding |
| `10011100` | PRIMORDIAL_BLACK_HOLES | - | Physics modeling |
| `11101100` | STELLAR_MERGERS | - | Astrophysics simulation |
| `11111100` | THEORY_OF_EVERYTHING | - | Unified field specification |
| `01011111` | VERIFY_ENDPOINTS | - | API verification suite |
| `11110111` | PATTERN_COMPLETION_BASELINE | - | Pattern coherence verification |

---

## Navigation in 3D Interface

### How It Works:

1. **View 3D field** with three causal chains visible
   - Left: → ENCYCLOPEDIA chain
   - Right: → RENDERER chain
   - Center: → LEDGER chain

2. **Click any byte node** to navigate
   - Updates info display with pattern properties
   - Shows binary, signal strength, semantic role

3. **Program Link Detection**
   - If node links to a program, displays: `→ PROGRAM LINK DETECTED`
   - Shows program name and port
   - Can launch or view details

4. **Traverse causality**
   - Follow green lines (causality connections)
   - Each step moves through semantic stages
   - Final node (answer) links to program

### Controls:
- **Left-click drag**: Rotate view
- **Right-click drag**: Pan
- **Scroll**: Zoom
- **Click node**: Navigate
- **Space**: Reset view

---

## File Reference

```
BINARY_FIELD_PROPERTIES.py          # Core: enumerate all 256 patterns
BINARY_FIELD_PROPERTIES.json        # Export: full pattern catalog
BINARY_FIELD_PROPERTIES.csv         # Export: CSV lookup table
BINARY_CAUSAL_GRAPH.json            # Graph: transitions between patterns
BINARY_HIERARCHY.json               # Levels: patterns by signal strength

APPLICATION_REGISTRY.py             # Core: map programs to patterns
APPLICATION_REGISTRY.json           # Export: full program registry

BINARY_FIELD_3D.html               # UI: 3D navigator (deployed as ENCYCLOPEDIA.html)
BINARY_FIELD_MODEL.py              # Core: data structures (chains, bytes, fields)

ENCYCLOPEDIA_API_SERVER.py          # Running on port 5000
```

---

## Extension Points

### Add More Programs:
```python
registry.register_program(
    "MY_PROGRAM",
    "c:\\path\\to\\program.py",
    "11110011",              # Entry pattern
    "Program description",
    api_port=5001            # Optional port
)
```

### Add More Chains:
```python
chain = registry.create_causal_chain("MY_PROGRAM", "to_my_program")
chain.add_pattern("00000000", "question")
chain.add_pattern("10101010", "processing")
chain.add_pattern("11110011", "answer → MY_PROGRAM")
```

### Add More Fields:
Query `BINARY_CAUSAL_GRAPH.json` to find neighbors (hamming distance 1).
Each pattern has 8 natural neighbors (one bit flip away).

---

## The System Is Self-Documenting

The structure **teaches itself**:
- **Pattern color** = signal strength
- **Node size** = signal strength
- **Chain path** = causal dependency
- **Program link** = actionable outcome
- **Green lines** = causality flow

Binary data becomes 3D form. Form implies function. Function connects to programs.
