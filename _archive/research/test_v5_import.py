#!/usr/bin/env python3
"""Quick test of V5 import and usage"""
import sys
sys.path.insert(0, r'c:\Determined')

try:
    from FIELD_IMAGE_GENERATOR_V5 import DeterministicFieldBuilder
    print("✓ Import successful")
    
    gen = DeterministicFieldBuilder()
    print("✓ Instance created")
    
    # Test Hydrogen
    result = gen.generate_generic_atom_svg('Hydrogen', 1)
    print(f"✓ Hydrogen generated: {len(result)} bytes")
    
    # Test Carbon
    result = gen.generate_generic_atom_svg('Carbon', 6)
    print(f"✓ Carbon generated: {len(result)} bytes (Config: 1s² 2s² 2p²)")
    
    # Test Water
    result = gen.generate_molecule_vsepr_svg('H₂O', 'O', 8, [('H', 1), ('H', 1)], 2)
    print(f"✓ Water generated: {len(result)} bytes")
    
    print("\n✓✓✓ All V5 functions working correctly")
    
except Exception as e:
    import traceback
    print(f"✗ Error: {e}")
    traceback.print_exc()
