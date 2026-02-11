# Invariant Identity Engine - Quick Reference

## Hotkeys
| Key | Action |
|-----|--------|
| F9 | Toggle interception mode |
| ESC | Stop interception |

## UI Buttons
| Button | Function |
|--------|----------|
| Show Overlay | Activate transparent overlay |
| Hide Overlay | Deactivate overlay |
| Start Intercept | Begin capturing clicks |
| Stop Intercept | Return to click-through |
| Run Test | Execute adversarial suite |
| Validate Spec | Run compliance tests |
| Clear Log | Clear output window |

## Overlay States
| State | Visual | Behavior |
|-------|--------|----------|
| Click-Through | Light blue tint (10% opacity) | Passes clicks through |
| Interception | Red tint (50% opacity) | Captures all clicks |
| Hidden | Not visible | Overlay closed |

## Status Indicators
| Indicator | Meaning |
|-----------|---------|
| Ready | System initialized |
| Overlay Active | Overlay in click-through mode |
| INTERCEPTING | Capturing interactions |
| Spec Compliant | Validation passed |
| Non-Compliant | Validation failed |

## Result Types
| Type | Format | Description |
|------|--------|-------------|
| Structural ID | 64-char hex | SHA256 of canonical form |
| Black Brick | BLACK_BRICK:... | High entropy (>7.8 bits/byte) |
| NEW BRICK | Status indicator | First time pattern seen |
| EXISTING BRICK | Status indicator | Pattern already in ledger |

## Transforms
| ID | Description | Reversible |
|----|-------------|-----------|
| IDENTITY | No transform | ? |
| BITROT_0..7 | Bit rotation | ? |
| ENDIAN_16 | 16-bit endian swap | ? |
| ENDIAN_32 | 32-bit endian swap | ? |
| ENDIAN_64 | 64-bit endian swap | ? |
| BASE64 | Base64 encoding | ? |
| PADDING_REMOVE | Null byte removal | ? |

## Metrics
| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Total Bricks | Count of unique IDs | Structural diversity |
| Total Ingests | Count of all data processed | Volume throughput |
| Compression Ratio | 1 - (Bricks/Ingests) | Deduplication rate |
| Entropy | Shannon entropy | Randomness measure |
| Stillness Ratio | 1 - Compression | Storage efficiency |

## Test Suite
| Test | Validates | Pass Criteria |
|------|-----------|--------------|
| Original Data | Baseline processing | ID generated |
| Base64 | Transform equivalence | Same ID as original |
| Padded | Padding removal | Handles null bytes |
| Black Brick | Entropy guardrail | Classifies high entropy |

## Validation Tests
| Test | Specification Section | Criteria |
|------|----------------------|----------|
| Core Identity | 7.1 | ID(raw) == ID(b64) |
| History Independence | 6.1 | Order-independent |
| Transform Reversibility | 3 | T(Reverse(T(B))) == B |
| Entropy Guardrail | 5 | E > 7.8 ? Black Brick |
| Collision Resistance | 7.2 | Different data ? Different ID |
| Transform Ambiguity | 8 | Unique canonical form |

## Performance
| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Canonicalization | O(n × 12) | 12 transforms in LCT |
| Hash Computation | O(n) | SHA256 |
| Ledger Lookup | O(1) | Hash table |
| Ledger Insert | O(1) | Concurrent dictionary |

## Troubleshooting
| Issue | Solution |
|-------|----------|
| Overlay not visible | Click Show Overlay |
| Clicks not intercepting | Press F9 |
| Low compression | Normal for unique data |
| High Black Brick count | Encrypted/compressed input |

## Formal Specification
```
ID(B) = HASH(C(B))
C(B) = MIN { T_i(B) | T_i ? LCT and reversible }
```

## Key Properties
- ? History-independent
- ? Deterministic
- ? Order-independent
- ? Collision-resistant
- ? Entropy-aware
- ? Asymptotically still

## Files
| File | Purpose |
|------|---------|
| brief.md | Formal specification |
| README.md | Architecture details |
| USERGUIDE.md | Complete user manual |
| IMPLEMENTATION.md | Technical summary |

## Quick Start
1. Launch Trust.exe
2. Click "Show Overlay"
3. Press F9 to intercept
4. Click anywhere
5. View results in log

## Sample Output
```
--- Click Intercepted at (1024, 768) ---
Structural ID: A1B2C3D4E5F6...
Status: NEW BRICK
Transform: IDENTITY
Entropy: 4.23 bits/byte
Total Bricks: 42
Compression: 87.50%
```

## Contact/Support
- Review brief.md for formal specification
- Run "Validate Spec" for compliance check
- Check USERGUIDE.md for detailed help
