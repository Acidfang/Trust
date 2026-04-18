"""
Universal Renderer API Server
Serves universal narratives for any entity type using pattern completion
(electrons, particles, organisms, systems, abstract concepts - scale and domain agnostic)
"""

from flask import Flask, request, jsonify
import json
import sys
sys.path.insert(0, r'c:\Determined')

from UNIVERSAL_RENDERER import render_with_song_layer, generate_field_narratives
from PATTERN_COMPLETION_BASELINE import BaselineKnowledgeGenerator
from UFM_CLIENT import get_ufm_client

app = Flask(__name__)

# Try to enable CORS, but don't fail if unavailable
try:
    from flask_cors import CORS
    CORS(app)
    cors_enabled = True
except ImportError:
    cors_enabled = False
    print("⚠ Flask-CORS not installed, proceeding without CORS headers")

baseline_gen = BaselineKnowledgeGenerator()
ufm_client = get_ufm_client()

# API PRINCIPLE: Universally agnostic format
# Works for ANY entity type at ANY scale: electrons → cosmic systems
# Works across ANY domain: physical, biological, social, abstract, emergent


@app.route('/api/entity/<entity_name>', methods=['GET'])
def get_entity(entity_name):
    """Get complete narrative for any entity using pattern completion.
    
    UNIVERSAL: Works for any entity type at any scale:
    - Physical: electrons, atoms, molecules, particles, forces
    - Biological: cells, organisms, ecosystems, species
    - Social: individuals, families, groups, societies, civilizations
    - Abstract: concepts, systems, ideas, patterns, information structures
    - Emergent: phenomena, behaviors, networks, organizations
    """
    try:
        # Generate baseline from patterns (no web search needed)
        baseline = baseline_gen.generate_baseline_for_organism(entity_name)
        
        # Build entity object for renderer
        class PatternEntity:
            def __init__(self, baseline_data):
                self.name = baseline_data['organism']  # 'organism' key is universal label
                self.attributes = baseline_data['core_attributes']
                self.principles = baseline_data['principles']
                self.coherence = 0.95
                self.confidence = baseline_data['confidence']
                
                # Create attribute access (works for any entity type)
                for attr, value in baseline_data['core_attributes'].items():
                    setattr(self, attr, value)
                for attr, value in baseline_data['derived_attributes'].items():
                    setattr(self, attr, value)
        
        entity = PatternEntity(baseline)
        
        # Generate field narratives
        field_narratives = baseline['narratives']
        
        return jsonify({
            "entity": entity_name,
            "entity_type": "universal",  # Works for any scale/domain
            "principles": baseline['principles'],
            "attributes": baseline['core_attributes'],
            "derived_attributes": baseline['derived_attributes'],
            "field_narratives": field_narratives,
            "confidence": baseline['confidence'],
            "source": "pattern_completion",
            "scale_agnostic": True
        })
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e), "scale_agnostic": False}), 500


@app.route('/api/entities', methods=['GET'])
def list_entities():
    """List example entities across all scales and domains.
    
    UNIVERSAL: Examples span from microscopic to macroscopic,
    from physical to social to abstract.
    """
    entities = [
        {"name": "Electron", "scale": "sub-atomic", "domain": "physics", "description": "Fundamental particle"},
        {"name": "Water Molecule", "scale": "molecular", "domain": "chemistry", "description": "H2O compound"},
        {"name": "E. coli Bacteria", "scale": "cellular", "domain": "biology", "description": "Simple adaptive organism"},
        {"name": "Human", "scale": "macroscopic", "domain": "biology", "description": "Complex reasoning entity"},
        {"name": "Peregrine Falcon", "scale": "macroscopic", "domain": "biology", "description": "Fastest animal on Earth"},
        {"name": "Gray Wolf", "scale": "macroscopic", "domain": "biology", "description": "Apex pack predator"},
        {"name": "Wolf Pack", "scale": "social", "domain": "sociology", "description": "Emergent social structure"},
        {"name": "Human Civilization", "scale": "macro-social", "domain": "sociology", "description": "Complex emergent system"},
        {"name": "Internet Protocol", "scale": "abstract", "domain": "information", "description": "Emergent communication system"},
        {"name": "Constraint", "scale": "abstract", "domain": "philosophy", "description": "Abstract universal principle"}
    ]
    return jsonify({
        "entities": entities,
        "principle": "Universally agnostic - works at ANY scale and in ANY domain"
    })


@app.route('/api/organism/<organism_name>', methods=['GET'])
@app.route('/api/entity/<organism_name>', methods=['GET'])
def get_organism_legacy(organism_name):
    """Backward compatibility: redirect to universal entity endpoint"""
    return get_entity(organism_name)


@app.route('/api/organisms', methods=['GET'])
def list_organisms_legacy():
    """Backward compatibility: redirect to universal entities endpoint"""
    return list_entities()


@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "online",
        "service": "Universal Renderer API",
        "principle": "Universally agnostic - works at any scale/domain"
    })


@app.route('/api/ufm/process', methods=['POST'])
def process_with_ufm():
    """Process data through UFM's 7-stage universal pipeline.
    
    Request body:
    {
        "entity_name": "string",  # Entity name or description
        "data": "string" or byte data
    }
    
    Returns UFM analysis with:
    - quality_score (0.0-1.0)
    - 7 causal principles per stage
    - stage results
    - replay seed for deterministic reproduction
    """
    try:
        payload = request.get_json()
        entity_name = payload.get('entity_name', 'Unknown')
        data = payload.get('data', entity_name).encode('utf-8')
        
        # Process through UFM's universal pipeline
        ufm_result = ufm_client.process_universal(data, verify=True)
        
        if ufm_result.get('error'):
            return jsonify({
                "status": "error",
                "error": ufm_result['error'],
                "entity_name": entity_name
            }), 500
        
        # Return UFM analysis
        return jsonify({
            "entity_name": entity_name,
            "ufm_analysis": {
                "success": ufm_result.get('success'),
                "quality_score": ufm_result.get('quality_score'),
                "seed": ufm_result.get('seed'),
                "replay_valid": ufm_result.get('replay_valid'),
                "stages": ufm_result.get('stages_completed', []),
                "principles": ufm_result.get('principles', [])
            },
            "source": "UFM Engine v3.0-rust",
            "scale_agnostic": True
        })
    
    except Exception as e:
        return jsonify({"error": str(e), "scale_agnostic": False}), 500


@app.route('/api/ufm/health', methods=['GET'])
def ufm_health():
    """Check UFM Engine connectivity"""
    try:
        health = ufm_client.health()
        return jsonify({
            "ufm_engine": health.get('status'),
            "engine_version": health.get('engine_version'),
            "renderer_status": "online",
            "integration": "active"
        })
    except Exception as e:
        return jsonify({
            "ufm_engine": "error",
            "error": str(e),
            "renderer_status": "online",
            "integration": "error"
        }), 500


if __name__ == '__main__':
    print("Starting Universal Renderer API Server...")
    print("Visit: http://localhost:5000")
    print("\nAPI PRINCIPLE: Universally Agnostic Format")
    print("  Works for ANY entity at ANY scale")
    print("  From electrons to cosmic systems")
    print("  Across all domains: physical, biological, social, abstract\n")
    print("API endpoints:")
    print("  GET /api/entities - List example entities across all scales")
    print("  GET /api/entity/<name> - Get universal narrative for any entity")
    print("  POST /api/ufm/process - Process through UFM's 7-stage pipeline")
    print("  GET /api/ufm/health - Check UFM Engine connectivity")
    print("  GET /api/health - Health check\n")
    app.run(debug=True, port=5000)
