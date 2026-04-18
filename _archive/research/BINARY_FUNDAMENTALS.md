# Binary Fundamentals: What 0 and 1 Express in Computing

## The Two States: Everything Reduces Here

In computing, **0 and 1 are the only primitive states**. Everything else is built from combinations of these two values.

```
0 = OFF    (absence, false, no signal)
1 = ON     (presence, true, has signal)
```

---

## What Can 0 and 1 Express?

### 1. **Boolean Logic** (True/False)
```
1 = True
0 = False
```
**Example**: Is the user logged in? `1 = yes`, `0 = no`

---

### 2. **Electrical States** (Voltage)
```
1 = High voltage (typically 3.3V-5V)
0 = Low voltage  (typically 0V)
```
**Where it matters**: CPU transistors, RAM cells, storage media

---

### 3. **Numerical Values** (Positional Notation)
Binary numbers count using powers of 2:

```
Binary    Decimal    Meaning
------    -------    -------
0         0          Zero
1         1          One
10        2          Two
11        3          Three
100       4          Four
101       5          Five
...
11111111  255        Eight bits max
```

**How it works**:
```
1 0 1 0 = (1×2³) + (0×2²) + (1×2¹) + (0×2⁰)
        = (1×8) + (0×4) + (1×2) + (0×1)
        = 8 + 2
        = 10 in decimal
```

---

### 4. **Memory Storage** (Bits & Bytes)
```
1 bit     = one choice: 0 or 1
1 byte    = 8 bits = 256 possible values (0-255)
1 kilobyte = 1024 bytes
1 megabyte = 1024 kilobytes
```

**Example**: An image pixel color in RGB:
```
Color intensity for Red:   11111111 (255 = maximum red)
Color intensity for Green: 01010101 (85 = half green)
Color intensity for Blue:  00000000 (0 = no blue)
```

---

### 5. **Text Encoding** (ASCII/Unicode)
Each character maps to a binary number:

```
Character    Binary      Decimal
---------    ------      -------
'A'          01000001    65
'B'          01000010    66
'a'          01100001    97
' '          00100000    32 (space)
'0'          00110000    48 (the digit zero character)
```

**Example**: The word "Hi" in binary
```
'H' = 01001000 (72)
'i' = 01101001 (105)
"Hi" = 0100100001101001
```

---

### 6. **Network Transmission** (Bits as Signals)
```
1 = Signal detected (pulse sent)
0 = No signal      (silence)
```

**Example**: Ethernet cable sends millions of 0s and 1s per second. Your modem converts these pulses into data.

---

### 7. **Logical Operations** (AND, OR, NOT)

**AND**: Both must be 1
```
1 AND 1 = 1
1 AND 0 = 0
0 AND 0 = 0
```

**OR**: At least one must be 1
```
1 OR 0 = 1
0 OR 0 = 0
```

**NOT**: Flip the value
```
NOT 1 = 0
NOT 0 = 1
```

---

### 8. **Decision Branches** (If/Then Control Flow)
```
if (condition == 1):
    do action A
else:
    do action B
```

Binary decides which path the program takes.

---

### 9. **Physical Phenomena** (Quantum & Field Theory)

In quantum computing:
```
1 = Spin up (↑)
0 = Spin down (↓)
```

In field theory (your project's domain):
```
1 = Field excitation (particle/energy present)
0 = Vacuum state     (no excitation)
```

---

## The Universal Pattern

**Every computation reduced to its foundation**:

```
Complexity (Software)
    ↓
Logic Gates (CPU)
    ↓
Transistors (Silicon)
    ↓
Electrical Voltage
    ↓
0 and 1
```

**All of this is built from combinations of two states.**

---

## Scale Example: From 1 Bit to a Digital Image

```
1 bit           = 2 values       (0 or 1)
2 bits          = 4 values       (00, 01, 10, 11)
3 bits          = 8 values       (000 to 111)
8 bits (1 byte) = 256 values     (0-255)
32 bits         = 4.3 billion values
64 bits         = 18 quintillion values

A digital image (1920×1080 pixels, 24-bit color):
1920 × 1080 × 24 = 49,971,420 bits
                 = 6,246,427 bytes
                 ≈ 6.2 megabytes
```

**Everything is built by scaling 0 and 1.**

---

## Why This Matters for Your System

In the Determined system:
- **0 = Uncertainty** (signal not yet collapsed)
- **1 = Certainty** (signal confirmed)
- **Binary signature** = coherence measurement (ratio of 1s to total bits)
- **UFM verification** = measuring this ratio to confirm state validity

Your field theory narratives use this: τ (coherence) ranges from 0.0 to 1.0, fundamentally representing how many "1 states" (confirmations) your system has achieved.

---

## The Foundation Rule

**There are no exceptions to 0 and 1.**

- Your CPU implements 0 and 1
- Your storage uses 0 and 1
- Your network transmits 0 and 1
- Your quantum computer will use quantum 0 and 1
- Field collapse measurements produce 0 and 1

Everything else—all abstraction, all meaning, all software—is built by thoughtfully arranging these two primitive states in pattern and scale.

**0 and 1 are not a limitation. They are completeness.**
