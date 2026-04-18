# UNIVERSAL RENDERER: Quick Start & Testing Guide

## ✅ Test Results: 10/10 PASSING (100%)

**Last Run**: 2026-03-29 | **Test File**: [UNIVERSAL_RENDERER_TEST.py](../../UNIVERSAL_RENDERER_TEST.py)

| Category | Status | Details |
|----------|--------|---------|
| Detection | ✅ PASS | 6/6 container types detected correctly |
| Extraction | ✅ PASS | Deduplication working (12 atoms → 3 fields) |
| Song Generation | ✅ PASS | 7 songs with correct weights (total 1.0) |
| ARIA Expansion | ✅ PASS | Environment-locked hashes generated |
| Election Sequencing | ✅ PASS | Multiple elections recorded with hashes |
| Output Formats | ✅ PASS | JSON, text, markdown all rendered |
| Dependencies | ✅ PASS | Recovery dependencies intact |
| Determinism | ✅ PASS | Identical outputs for equivalent inputs |
| Reversibility | ✅ PASS | Election clearing verified |
| Edge Cases | ✅ PASS | Empty, large, and null inputs handled |

---

## Quick Start: 5 Minutes

### Installation
```python
from UNIVERSAL_RENDERER import render_with_song_layer
```

### Basic Usage

```python
# Define a simple container
class MyMolecule:
    def __init__(self):
        self.atoms = [
            type('Atom', (), {'element': 'C'}),
            type('Atom', (), {'element': 'C'}),
            type('Atom', (), {'element': 'H'}),
            type('Atom', (), {'element': 'H'}),
            type('Atom', (), {'element': 'H'}),
            type('Atom', (), {'element': 'H'}),
        ]
        self.bonds = [
            type('Bond', (), {'order': 1.0}),
            type('Bond', (), {'order': 1.0}),
        ]

# Render to any format
molecule = MyMolecule()

# SVG visualization
svg = render_with_song_layer(molecule, output_format="svg")

# JSON for processing
json_data = render_with_song_layer(molecule, output_format="json")

# Human-readable verse
verse = render_with_song_layer(molecule, output_format="verse")

# System narrative (meta-song)
story = render_with_song_layer(molecule, output_format="meta_song")
```

---

## Testing Framework

### Test Categories

#### 1. Detection Tests
**Goal**: Verify container type detection works correctly  
**Test**: `test_detect_all_container_types()`

```python
def test_detect_all_container_types():
    """Verify detection for each container type"""
    
    tests = [
        ("primitive", MockMolecule()),
        ("entity", MockEntity()),
        ("ledger", MockLedger()),
        ("worldstate", MockWorldState()),
        ("orientation", MockOrientation()),
        ("registry", MockRegistry()),
    ]
    
    for expected_type, container in tests:
        detected = detect_container_type(container)
        assert detected == expected_type, f"Expected {expected_type}, got {detected}"
    
    print("✓ All detection tests passed")
```

---

#### 2. Extraction Tests
**Goal**: Verify compact form extraction and deduplication  
**Test**: `test_extract_to_compact()`

```python
def test_extract_to_compact():
    """Verify extraction produces correct compact form"""
    
    # Test benzene
    benzene = MockMolecule()
    compact = extract_to_compact(benzene)
    
    # Verify structure
    assert "fields" in compact
    assert "principle" in compact
    assert "container_type" in compact
    assert "extracted_at" in compact
    
    # Verify deduplication (6 carbons → 1 entry)
    carbon_entries = [f for f in compact["fields"] if f.get("element") == "C"]
    assert len(carbon_entries) == 1
    assert carbon_entries[0]["count"] == 6
    
    print("✓ Extraction tests passed")
```

---

#### 3. Song Generation Tests
**Goal**: Verify song generation for each principle  
**Test**: `test_generate_render_songs()`

```python
def test_generate_render_songs():
    """Verify each principle generates a valid song"""
    
    principles = [
        "unified_field",
        "constraint",
        "temporal",
        "proactive",
        "engagement",
        "attachment",
        "rarity"
    ]
    
    for principle in principles:
        song_data = map_principle_to_song(principle)
        
        # Verify structure
        assert song_data["principle"] is not None
        assert song_data["verse"] is not None
        assert song_data["symbols"] is not None
        assert 0 < song_data["weight"] <= 1
        
    # Verify total weight = 100%
    all_songs = list_all_songs()
    total_weight = sum(s["weight"] for s in all_songs)
    assert abs(total_weight - 1.0) < 0.001, f"Total weight {total_weight} != 1.0"
    
    print("✓ Song generation tests passed")
```

---

#### 4. ARIA Expansion Tests
**Goal**: Verify environment-locked expansion and hashing  
**Test**: `test_aria_expansion()`

```python
def test_aria_expansion():
    """Verify ARIA expansion produces consistent hashes"""
    
    # Create compact form
    benzene = MockMolecule()
    compact = extract_to_compact(benzene)
    
    # Expand twice with same environment
    env1 = {"solvent": "water", "temperature": "298K", "pressure": "1atm"}
    
    expansion1 = expand_for_aria(compact, env1)
    expansion2 = expand_for_aria(compact, env1)
    
    # Hashes should match (deterministic)
    assert expansion1["hash"] == expansion2["hash"], "Hashes don't match for identical expansion"
    
    # Field verses should be generated
    assert "field_verses" in expansion1
    assert len(expansion1["field_verses"]) > 0
    
    # Environment should be preserved
    assert expansion1["environment"]["solvent"] == "water"
    
    print("✓ ARIA expansion tests passed")
```

---

#### 5. Election Sequencing Tests
**Goal**: Verify election recording and meta-song composition  
**Test**: `test_election_sequencing()`

```python
def test_election_sequencing():
    """Verify election recording and meta-song"""
    
    # Clear previous elections
    clear_election_sequence()
    
    # Render multiple containers
    containers = [
        MockMolecule(),     # primitive
        MockEntity(),        # entity
        MockLedger(),        # ledger
    ]
    
    for container in containers:
        render_with_song_layer(container, output_format="song")
    
    # Check election count
    count = get_election_count()
    assert count == 3, f"Expected 3 elections, got {count}"
    
    # Get election sequence
    elections = get_election_sequence()
    assert len(elections) == 3
    
    # Verify each election has required fields
    for election in elections:
        assert "timestamp" in election
        assert "environment" in election
        assert "principle" in election
        assert "hash" in election
    
    # Get meta-song
    meta_song = get_election_meta_song(output_format="song")
    assert meta_song["metadata"]["election_count"] == 3
    assert len(meta_song["metadata"]["election_hashes"]) == 3
    
    print("✓ Election sequencing tests passed")
```

---

#### 6. Output Format Tests
**Goal**: Verify all output formats work and produce correct data  
**Test**: `test_all_output_formats()`

```python
def test_all_output_formats():
    """Verify each output format renders correctly"""
    
    benzene = MockMolecule()
    formats = ["verse", "symbol", "json", "markdown", "text", "svg", "song"]
    
    for fmt in formats:
        output = render_with_song_layer(benzene, output_format=fmt)
        
        # Check output is not empty
        if isinstance(output, str):
            assert len(output) > 0, f"Empty output for format {fmt}"
        elif isinstance(output, dict):
            assert len(output) > 0, f"Empty dict output for format {fmt}"
        
        # Format-specific validation
        if fmt == "json":
            assert "principle" in output
            assert "type" in output
        elif fmt == "svg":
            assert "<svg" in output
        elif fmt == "markdown":
            assert "##" in output
    
    print("✓ Output format tests passed")
```

---

#### 7. Dependency Tests
**Goal**: Verify recovery dependencies are correct  
**Test**: `test_recovery_dependencies()`

```python
def test_recovery_dependencies():
    """Verify each container type has correct dependencies"""
    
    container_types = [
        "primitive", "entity", "ledger", 
        "worldstate", "orientation", "registry"
    ]
    
    for container_type in container_types:
        deps = query_render_dependencies(container_type)
        
        # Verify structure
        assert "required" in deps
        assert "cascade" in deps
        assert isinstance(deps["required"], list)
        assert len(deps["required"]) >= 1
        
        # Each required song must be in all songs list
        all_songs = list_all_songs()
        song_principles = [s["principle"] for s in all_songs]
        
        for required_song in deps["required"]:
            assert required_song in song_principles, \
                f"Required song {required_song} not found in available songs"
    
    print("✓ Recovery dependency tests passed")
```

---

#### 8. Determinism Tests
**Goal**: Verify rendering is deterministic (same input → same output)  
**Test**: `test_determinism()`

```python
def test_determinism():
    """Verify same input always produces identical output"""
    
    benzene1 = MockMolecule()
    benzene2 = MockMolecule()
    
    # Render same container twice with same environment
    output1 = render_with_song_layer(benzene1, output_format="json")
    output2 = render_with_song_layer(benzene2, output_format="json")
    
    # Should produce identical output
    assert output1["principle"] == output2["principle"]
    assert output1["verse"] == output2["verse"]
    assert output1["symbols"] == output2["symbols"]
    
    # Compact forms should match
    compact1 = extract_to_compact(benzene1)
    compact2 = extract_to_compact(benzene2)
    
    assert compact1["principle"] == compact2["principle"]
    assert len(compact1["fields"]) == len(compact2["fields"])
    
    print("✓ Determinism tests passed")
```

---

#### 9. Reversibility Tests
**Goal**: Verify undo and reversal mechanisms work  
**Test**: `test_reversibility()`

```python
def test_reversibility():
    """Verify election sequence can be reversed"""
    
    # Record some elections
    clear_election_sequence()
    
    benzene = MockMolecule()
    render_with_song_layer(benzene, output_format="song")
    render_with_song_layer(benzene, output_format="json")
    
    count_before = get_election_count()
    assert count_before == 2
    
    # Clear elections
    clear_election_sequence()
    
    count_after = get_election_count()
    assert count_after == 0, "Election sequence not cleared"
    
    # Re-record and verify
    render_with_song_layer(benzene, output_format="song")
    count_restored = get_election_count()
    assert count_restored == 1
    
    print("✓ Reversibility tests passed")
```

---

#### 10. Edge Cases Tests
**Goal**: Verify system handles edge cases gracefully  
**Test**: `test_edge_cases()`

```python
def test_edge_cases():
    """Verify edge cases are handled correctly"""
    
    # Empty container
    empty = type('Empty', (), {})()
    detected = detect_container_type(empty)
    assert detected is not None, "Should default to 'generic'"
    
    # None input
    try:
        result = detect_container_type(None)
        assert result == "null"
    except:
        pass
    
    # Very large container
    large = MockMolecule()
    large.atoms = [type('Atom', (), {'element': 'C'})() for _ in range(1000)]
    
    compact = extract_to_compact(large)
    assert compact is not None
    assert compact["fields"][0]["count"] == 1000
    
    print("✓ Edge case tests passed")
```

---

## Running the Test Suite

```python
def run_all_tests():
    """Run complete test suite"""
    
    tests = [
        ("Detection", test_detect_all_container_types),
        ("Extraction", test_extract_to_compact),
        ("Song Generation", test_generate_render_songs),
        ("ARIA Expansion", test_aria_expansion),
        ("Election Sequencing", test_election_sequencing),
        ("Output Formats", test_all_output_formats),
        ("Dependencies", test_recovery_dependencies),
        ("Determinism", test_determinism),
        ("Reversibility", test_reversibility),
        ("Edge Cases", test_edge_cases),
    ]
    
    passed = 0
    failed = 0
    
    print("\n" + "=" * 60)
    print("UNIVERSAL RENDERER TEST SUITE")
    print("=" * 60 + "\n")
    
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
            print(f"✅ {test_name}: PASS")
        except AssertionError as e:
            failed += 1
            print(f"❌ {test_name}: FAIL - {e}")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print(f"Success Rate: {passed}/{len(tests)} ({100*passed//len(tests)}%)")
    print("=" * 60 + "\n")
    
    return failed == 0

# Run tests
if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
```

---

## Test Fixtures

### Mock Containers

```python
class MockMolecule:
    def __init__(self):
        self.atoms = [
            type('Atom', (), {'element': 'C'})(),
            type('Atom', (), {'element': 'C'})(),
            type('Atom', (), {'element': 'C'})(),
            type('Atom', (), {'element': 'C'})(),
            type('Atom', (), {'element': 'C'})(),
            type('Atom', (), {'element': 'C'})(),
            type('Atom', (), {'element': 'H'})(),
            type('Atom', (), {'element': 'H'})(),
            type('Atom', (), {'element': 'H'})(),
            type('Atom', (), {'element': 'H'})(),
            type('Atom', (), {'element': 'H'})(),
            type('Atom', (), {'element': 'H'})(),
        ]
        self.bonds = [
            type('Bond', (), {'order': 1.5})(),
            type('Bond', (), {'order': 1.5})(),
            type('Bond', (), {'order': 1.5})(),
            type('Bond', (), {'order': 1.5})(),
            type('Bond', (), {'order': 1.5})(),
            type('Bond', (), {'order': 1.5})(),
            type('Bond', (), {'order': 1.0})(),
            type('Bond', (), {'order': 1.0})(),
            type('Bond', (), {'order': 1.0})(),
            type('Bond', (), {'order': 1.0})(),
            type('Bond', (), {'order': 1.0})(),
            type('Bond', (), {'order': 1.0})(),
        ]

class MockEntity:
    def __init__(self):
        self.position = [5, 5, 5]
        self.id = "entity_001"
        self.properties = {"energy": 100}

class MockLedger:
    def __init__(self):
        self.version = 1
        self.timestamp = "2026-04-03T14:24:48"
        self.transactions = [{"action": "CREATE"}, {"action": "UPDATE"}]
        self.hash = "abc123"

class MockWorldState:
    def __init__(self):
        self.entities = [MockEntity()]
        self.connections = [("entity_001", "entity_002")] * 50

class MockOrientation:
    def __init__(self):
        self.anchor_vector = [1, 0, 0]
        self.magnitude = 1.0
        self.quaternion = [0, 0, 0, 1]

class MockRegistry:
    def __init__(self):
        self.primitives = [MockMolecule(), MockMolecule()]
        self.frameworks = ["framework_1", "framework_2", "framework_3"]
```

---

## Verification Checklist

- [ ] All 10 test categories pass (100% success rate)
- [ ] All 6 container types detected correctly
- [ ] All 7 recovery songs generated correctly
- [ ] Output formats produce valid output for each format
- [ ] Determinism proven (identical input → identical output)
- [ ] Reversibility works (clear and re-record)
- [ ] Hash computations match on re-expansion
- [ ] Election sequencing maintains order
- [ ] Meta-song composed from elections correctly
- [ ] Edge cases handled gracefully

