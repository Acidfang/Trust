#!/usr/bin/env python3
"""
MINIMAL TEST API SERVER — Deterministic Field Visualization

Pure test to verify V5 generator works via API.
"""

from flask import Flask, Response, jsonify
import sys

sys.path.insert(0, r"c:\Determined")
from FIELD_IMAGE_GENERATOR_V5 import DeterministicFieldBuilder

app = Flask(__name__)

@app.route('/api/image/<entity_name>')
def generate_image(entity_name):
    """Generate deterministic field visualization."""
    builder = DeterministicFieldBuilder()
    
    # Map entities to generation
    if entity_name == 'Electron':
        svg = builder._generate_electron_measured()
    elif entity_name == 'Hydrogen':
        svg = builder.generate_generic_atom_svg('Hydrogen', 1)
    elif entity_name == 'Carbon':
        svg = builder.generate_generic_atom_svg('Carbon', 6)
    elif entity_name == 'Oxygen':
        svg = builder.generate_generic_atom_svg('Oxygen', 8)
    elif entity_name == 'Nitrogen':
        svg = builder.generate_generic_atom_svg('Nitrogen', 7)
    elif entity_name == 'Water':
        svg = builder.generate_molecule_vsepr_svg('H₂O', 'O', 8, [('H', 1), ('H', 1)], 2)
    elif entity_name == 'Methane':
        svg = builder.generate_molecule_vsepr_svg('CH₄', 'C', 6, [('H', 1), ('H', 1), ('H', 1), ('H', 1)], 4)
    else:
        return jsonify({"error": f"Unknown entity: {entity_name}"}), 404
    
    return Response(svg, mimetype='image/svg+xml')

@app.route('/test')
def test():
    """Quick test endpoint."""
    return jsonify({
        "status": "working",
        "deterministic_builder": "V5 Loaded",
        "try": "/api/image/Carbon or /api/image/Water"
    })

if __name__ == "__main__":
    print("=" * 70)
    print("MINIMAL DETERMINISTIC FIELD API - Testing V5")
    print("=" * 70)
    print("\n✓ DeterministicFieldBuilder imported successfully\n")
    print("Endpoints:")
    print("  GET /api/image/Electron")
    print("  GET /api/image/Hydrogen, Carbon, Oxygen, Nitrogen")
    print("  GET /api/image/Water, Methane")
    print("  GET /test")
    print("\nStarting on http://localhost:5000\n")
    
    app.run(debug=False, port=5000)
