# Invariant Identity Engine - User Guide

## Quick Start

### 1. Launch Application
Run `Trust.exe` to start the Invariant Identity Engine control panel.

### 2. Activate Overlay
Click **"Show Overlay"** to enable the transparent overlay across your entire screen. The overlay starts in click-through mode, allowing normal interaction with other applications.

### 3. Start Interception
Press **F9** (or click **"Start Intercept"**) to activate interception mode. The overlay will:
- Change to a semi-transparent red tint
- Display status message at top of screen
- Begin capturing click events

### 4. Intercept Interactions
With interception active:
- Click anywhere on screen
- Each click is captured and processed
- Data is converted to structural ID
- Results appear in control panel log

### 5. Stop Interception
- Press **F9** again to toggle back to click-through mode
- Press **ESC** to stop interception
- Click **"Hide Overlay"** to close overlay completely

## Features

### Overlay Window

**Click-Through Mode** (Default)
- Transparent overlay
- No interference with other applications
- Background monitoring ready

**Interception Mode** (F9 to toggle)
- Semi-transparent red overlay
- Captures all mouse clicks
- Processes data through identity engine
- Returns to click-through with F9 or ESC

### Control Panel

**Buttons:**
- **Show/Hide Overlay**: Toggle overlay visibility
- **Start/Stop Intercept**: Toggle interception mode (also F9)
- **Run Test**: Execute adversarial test suite
- **Validate Spec**: Run formal specification validation
- **Clear Log**: Clear output window

**Status Bar:**
- **Status**: Current system state
- **Bricks**: Unique structural patterns stored
- **Compression**: Deduplication ratio achieved

### Testing Suite

Click **"Run Test"** to execute:

1. **Original Data Test**
   - Process baseline text data
   - Generate structural ID

2. **Base64 Equivalence Test**
   - Encode same data as Base64
   - Verify same structural ID produced
   - Validates transform recognition

3. **Padding Test**
   - Add null byte padding
   - Should produce similar structural ID
   - Tests padding removal transform

4. **Black Brick Test**
   - Generate high-entropy random data
   - Should classify as BLACK_BRICK
   - Validates entropy guardrail

### Specification Validation

Click **"Validate Spec"** to verify compliance with formal specification:

**Tests Performed:**
- Core Identity Test (Section 7.1)
- History Independence (Section 6.1)
- Transform Reversibility (Section 3)
- Entropy Guardrail (Section 5)
- Collision Resistance (Section 7.2)
- Transform Ambiguity (Section 8)

Results show:
- ? PASS: Test meets specification
- ? FAIL: Non-compliance detected

## Understanding Results

### Structural ID Format
```
A1B2C3D4E5F6... (64-character hex string)
```
SHA256 hash of canonical form.

### Black Brick Format
```
BLACK_BRICK:A1B2C3D4E5F6...
```
High-entropy data exceeding 7.8 bits/byte threshold.

### Result Fields

**Structural ID**: Unique identity for canonical form
**Status**: NEW BRICK or EXISTING BRICK
**Transform**: Which LCT transform produced canonical form
  - IDENTITY: No transform needed
  - BITROT_N: Bit rotation by N positions
  - ENDIAN_16/32/64: Endianness swap
  - BASE64: Base64 encoding detected
  - PADDING_REMOVE: Trailing nulls removed
**Entropy**: Shannon entropy in bits per byte
**Total Bricks**: Unique patterns in ledger
**Total Ingests**: Total data processed
**Compression Ratio**: Deduplication percentage

## Advanced Usage

### Interpreting Stillness

**Low Brick Growth**: System achieving stillness
- Many ingests with few new bricks
- High compression ratio
- Structural equivalence detected

**High Brick Growth**: Unique data
- Most ingests create new bricks
- Low compression ratio
- Diverse structural patterns

### Black Brick Classification

Data classified as BLACK_BRICK when:
- Shannon entropy > 7.8 bits/byte
- Typically encrypted data
- Compressed archives
- Random noise
- Prevents false convergence

### Transform Selection

System automatically selects canonical form:
- Tries all LCT transforms
- Selects lexicographically smallest
- Deterministic and repeatable
- Independent of ledger state

## Keyboard Shortcuts

- **F9**: Toggle interception mode
- **ESC**: Stop interception (when active)

## Troubleshooting

### Overlay Not Visible
- Check if hidden behind other windows
- Click "Show Overlay" again
- Overlay may be in click-through mode (semi-transparent)

### Clicks Not Intercepting
- Verify interception mode active (red tint)
- Check status message at top of screen
- Press F9 to toggle mode

### Application Not Responding
- Close overlay window
- Restart application
- Check system permissions

### Low Compression Ratio
- Normal for diverse, unique data
- Black Bricks don't compress
- Stillness achieved with redundant data patterns

## Performance Considerations

### Compute Cost
- O(n × |T|) where n = data size, |T| = transform count
- Bounded by LCT grammar size (12 transforms)
- Linear scaling with data volume

### Memory Usage
- O(k) where k = unique brick count
- Minimal growth under redundancy
- Asymptotic stillness under saturation

### Best Practices
- Process similar data patterns for best compression
- Monitor brick count vs ingest volume
- Black Bricks indicate unique/encrypted data
- Stillness demonstrates structural convergence

## API Integration

### Basic Usage
```csharp
var engine = new StructuralIdentityEngine();
var result = engine.ComputeStructuralId(dataBytes);

Console.WriteLine($"ID: {result.StructuralId}");
Console.WriteLine($"Transform: {result.TransformApplied}");
Console.WriteLine($"Entropy: {result.Entropy:F2}");
```

### Ledger Integration
```csharp
var ledger = new InvariantLedger();
var ingestResult = ledger.Ingest(dataBytes);

if (ingestResult.IsNewBrick)
    Console.WriteLine("New pattern discovered");
else
    Console.WriteLine("Known pattern - ledger still");
```

### Execution Optimization
```csharp
var optimizer = new ExecutionOptimizer(ledger);
var prediction = optimizer.PredictBrickCreation(dataBytes);

if (!prediction.WillCreateNewBrick)
    Console.WriteLine("Structural duplicate detected");
```

## Theory of Operation

### Structural Identity
```
ID(B) = HASH(C(B))
where C(B) = MIN { T_i(B) | T_i ? LCT }
```

### History Independence
- Ledger structure independent of ingest order
- Canonical form selection deterministic
- Same data always produces same ID
- No optimization against ledger contents

### Asymptotic Stillness
- Brick count plateaus under redundancy
- Storage growth bounded
- Compute cost remains polynomial
- Energy efficiency superior to baseline CAS

## References

- See `brief.md` for formal specification
- See `README.md` for architectural details
- LCT grammar formally defined and versioned
- All transforms reversible and verifiable

## Support

For issues or questions:
1. Check specification compliance with "Validate Spec"
2. Review formal specification in `brief.md`
3. Verify LCT grammar implementation
4. Test with adversarial corpus

This system implements a deterministic identity primitive, not a compression system.
