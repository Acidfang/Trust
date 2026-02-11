# Invariant Identity Engine v2

A history-independent structural identity primitive implementing formal LCT (Linear and Non-Linear Canonical Transform) specification.

## Features

### Core Components

1. **StructuralIdentityEngine** - Implements the formal identity definition:
   - `ID(B) = HASH(C(B))` where `C(B) = MIN_? { T_i(B) | T_i ? T and reversible }`
   - History-independent canonicalization
   - Bounded transform grammar
   - Entropy guardrail (Black Brick Protocol)

2. **InvariantLedger** - Deterministic ledger architecture:
   - Order-independent storage
   - Trie-based brick management
   - Asymptotic storage stillness
   - Collision-resistant structural IDs

3. **OverlayWindow** - Click-through overlay with interception:
   - Transparent overlay across entire screen
   - F9 hotkey to toggle interception mode
   - F10 to show/hide Timeline Inspection Panel
   - Click-through when not intercepting
   - Visual feedback during active interception
   - Real-time pattern analysis and optimization

4. **TimelineInspectionPanel** - Interactive analysis dashboard (NEW):
   - Real-time event visualization
   - Dynamic entropy threshold adjustment
   - Auto-optimization detection
   - Transform effectiveness filtering
   - Export analysis capabilities
   - Stillness metrics tracking

4. **ExecutionEngine** - Processes intercepted data through ledger:
   - Real-time structural ID computation
   - Ledger ingest with deduplication
   - Statistics tracking
   - Simulation capabilities

### Admissible Transform Grammar (LCT Set)

The system implements a bounded, deterministic transform set:

1. **Bit Rotations** (0-7 positions)
2. **Endianness Swaps** (16-bit, 32-bit, 64-bit)
3. **Base64 Encoding** (bijective bit mapping)
4. **Padding Removal** (trailing null bytes)

All transforms are:
- Reversible
- Verifiable from bitstream alone
- Polynomially bounded

### Entropy Guardrail

- **Threshold**: 7.8 bits per byte
- High-entropy data classified as "Black Brick"
- Prevents false convergence
- Preserves compressed/encrypted data integrity

## Usage

### Running the Application

1. Launch the application
2. Click "Show Overlay" to activate the transparent overlay
3. Press F9 or click "Start Intercept" to begin capturing interactions
4. Click anywhere on screen - data will be processed through the identity engine
5. Press F9 or ESC to stop interception

### Keyboard Shortcuts

- **F9**: Toggle interception mode
- **F10**: Toggle Timeline Inspection Panel
- **F11**: Trigger optimization analysis
- **ESC**: Stop interception (when active)

### Testing

Click "Run Test" to execute the adversarial test suite:
- Original data test
- Base64 encoded variant (should produce same ID)
- Padded version test
- High entropy (Black Brick) test

## Architectural Principles

### History Independence

The system guarantees:
- Structural IDs identical regardless of ingest order
- Ledger structure independent of timing
- Canonical form selection deterministic and bounded
- No optimization against ledger contents

### Formal Verification

Two independent implementations using this grammar must produce:
- Identical canonical outputs
- Identical structural IDs
- Identical ledger topologies

### Breakthrough Criteria

The system qualifies as a deterministic identity primitive if:
- ? Canonicalization is grammar-bounded and history-independent
- ? Structural IDs identical across implementations
- ? False convergence rate near zero
- ? Ledger structure identical across ingest orders
- ? Brick growth plateaus asymptotically
- ? Compute scaling bounded polynomially
- ? Energy efficiency superior to baseline CAS

## Implementation Notes

### Click-Through Overlay

The overlay uses Win32 API to achieve:
- `WS_EX_TRANSPARENT`: Click-through capability
- `WS_EX_LAYERED`: Transparency support
- `WS_EX_NOACTIVATE`: Prevents focus stealing

When interception is active, the transparent flag is removed, allowing the overlay to capture mouse events.

### Canonicalization Algorithm

```csharp
def Canonicalize(bitstream):
    candidates = [(bitstream, "IDENTITY")]
    
    for transform in LCT_SET:
        if transform.IsReversible(bitstream):
            candidate = transform.Apply(bitstream)
            candidates.Add((candidate, transform.TransformId))
    
    return Min(candidates) // Lexicographic ordering
```

### Ledger Storage

Uses `ConcurrentDictionary` for:
- Thread-safe brick storage
- O(1) lookup by structural ID
- Atomic reference counting
- Order-independent insertion

## Performance Characteristics

- **Brick Growth**: Asymptotic plateau under redundancy saturation
- **Compute Cost**: Polynomial bounded (O(n × |T|) where |T| is transform set size)
- **Memory**: O(k) where k is unique brick count
- **Lookup**: O(1) for existing bricks

## Future Enhancements

1. **Stillness Metrics Dashboard**: Real-time brick count vs ingest volume curves
2. **Transform Ambiguity Detection**: Alert when multiple transforms produce identical canonical forms
3. **Adversarial Corpus Generator**: Automated generation of test variants
4. **Energy Profiling**: Joules per byte measurement
5. **Distributed Ledger**: Multi-node history-independent synchronization

## License

This implementation follows the formal specification in `brief.md` for third-party reproducibility and breakthrough verification.

## References

- See `brief.md` for complete formal specification
- LCT grammar is versioned and immutable
- Entropy threshold (7.8) is formally published
- All transform operations are deterministic and reversible
