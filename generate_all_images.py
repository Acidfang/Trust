"""
UPFM Image Generation - All 20 Wiki Images

Generates complete set of images for UPFM wiki.
Runs on GitHub Actions via workflow trigger.
"""

import sys
import os
import numpy as np
from pathlib import Path

# Add current directory to path
sys.path.insert(0, 'c:\\Determined')

from upfm_field_solver import FieldSolver
from upfm_field_renderer import FieldRenderer
from upfm_potential_library import PotentialLibrary


class BatchImageGenerator:
    """Generate all wiki images in one batch."""
    
    def __init__(self, output_dir='wiki/images/upfm'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.potlib = PotentialLibrary()
        self.renderer = FieldRenderer(verbose=False)
        self.results = {}
    
    def generate_image(self, name, concept, potential_func, params, 
                      grid_size=512, domain=(-3, 3), render_style='magnitude_phase'):
        """Generate single image."""
        try:
            solver = FieldSolver(grid_size=grid_size, domain=domain, verbose=False)
            
            field, potential = solver.solve(
                lambda x, y: potential_func(x, y, **params),
                t_max=400,
                dt=0.01,
                epsilon=1e-5,
                init_scale=0.1
            )
            
            output_path = f'{self.output_dir}/{name}.png'
            
            if render_style == 'magnitude_phase':
                self.renderer.render_magnitude_phase(field, output_path=output_path)
            elif render_style == 'frequency':
                self.renderer.render_frequency_map(field, output_path=output_path)
            else:
                self.renderer.render_magnitude_only(field, output_path=output_path)
            
            self.results[name] = {
                'status': 'success',
                'file': output_path,
                'concept': concept
            }
            print(f"✓ {name}")
            
        except Exception as e:
            self.results[name] = {
                'status': 'error',
                'error': str(e),
                'concept': concept
            }
            print(f"✗ {name}: {e}")
    
    def generate_all(self):
        """Generate all 20 images."""
        
        print("\n" + "="*70)
        print("UPFM IMAGE GENERATION - ALL 20 WIKI IMAGES")
        print("="*70 + "\n")
        
        # Image specifications
        images = {
            # FOUNDATION & THEORY (4 images)
            '01_electron_spiral': {
                'concept': 'Electron',
                'potential': self.potlib.electron_spiral,
                'params': {'f_e': 12, 'r_e': 0.15, 'barrier_height': 5.0},
                'domain': (-3, 3),
                'style': 'magnitude_phase'
            },
            '02_photon_propagating': {
                'concept': 'Photon',
                'potential': self.potlib.photon_propagating,
                'params': {'f': 8, 'direction': [1, 0], 'decay': 0.1},
                'domain': (-3, 3),
                'style': 'magnitude_phase'
            },
            '03_proton_resonance': {
                'concept': 'Proton',
                'potential': self.potlib.proton_resonance,
                'params': {'harmonics': [1, 2, 3], 'binding_strength': 2.0},
                'domain': (-3, 3),
                'style': 'magnitude_phase'
            },
            '04_generic_spiral': {
                'concept': 'Generic Spiral',
                'potential': self.potlib.gaussian,
                'params': {'sigma': 0.5},
                'domain': (-3, 3),
                'style': 'magnitude_phase'
            },
            
            # FORCES (4 images)
            '05_gravity_well': {
                'concept': 'Gravity',
                'potential': self.potlib.gravity_well,
                'params': {'mass': 1.0, 'scale': 1.0},
                'domain': (-3, 3),
                'style': 'magnitude_phase'
            },
            '06_four_forces_gravity': {
                'concept': 'Gravity (Large Scale)',
                'potential': self.potlib.gravity_well,
                'params': {'mass': 5.0, 'scale': 0.3},
                'domain': (-4, 4),
                'style': 'magnitude_phase'
            },
            '07_electron_confined': {
                'concept': 'Electron Tighter',
                'potential': self.potlib.electron_spiral,
                'params': {'f_e': 20, 'r_e': 0.1, 'barrier_height': 8.0},
                'domain': (-2, 2),
                'style': 'magnitude_phase'
            },
            '08_photon_free_space': {
                'concept': 'Photon Free',
                'potential': self.potlib.photon_propagating,
                'params': {'f': 12, 'direction': [1, 1], 'decay': 0.05},
                'domain': (-4, 4),
                'style': 'frequency'
            },
            
            # COSMIC STRUCTURES (4 images)
            '09_galaxy_spiral': {
                'concept': 'Galaxy',
                'potential': self.potlib.galaxy_spiral,
                'params': {'M_center': 10.0, 'a_core': 0.5, 'spiral_arms': 2.0, 'rotation_rate': 2.0},
                'domain': (-5, 5),
                'style': 'magnitude_phase'
            },
            '10_galaxy_dense': {
                'concept': 'Galaxy Dense',
                'potential': self.potlib.galaxy_spiral,
                'params': {'M_center': 20.0, 'a_core': 0.2, 'spiral_arms': 3.0, 'rotation_rate': 3.0},
                'domain': (-5, 5),
                'style': 'frequency'
            },
            '11_black_hole_reversal': {
                'concept': 'Black Hole Reversal',
                'potential': self.potlib.black_hole_reversal,
                'params': {'inversion_radius': 0.5, 'strength': 5.0},
                'domain': (-3, 3),
                'style': 'magnitude_phase'
            },
            '12_information_entropy': {
                'concept': 'Information Entropy',
                'potential': self.potlib.information_entropy_landscape,
                'params': {'ordered_regions': 2, 'temperature': 1.0},
                'domain': (-4, 4),
                'style': 'magnitude_phase'
            },
            
            # INFORMATION & CONSCIOUSNESS (4 images)
            '13_consciousness_7node': {
                'concept': 'Consciousness (7 nodes)',
                'potential': self.potlib.consciousness_network,
                'params': {'nodes': 7, 'coupling_strength': 1.5, 'frequency_base': 3.0},
                'domain': (-4, 4),
                'style': 'magnitude_phase'
            },
            '14_consciousness_5node': {
                'concept': 'Consciousness (5 nodes)',
                'potential': self.potlib.consciousness_network,
                'params': {'nodes': 5, 'coupling_strength': 2.0, 'frequency_base': 4.0},
                'domain': (-4, 4),
                'style': 'frequency'
            },
            '15_consciousness_3node': {
                'concept': 'Consciousness (3 nodes)',
                'potential': self.potlib.consciousness_network,
                'params': {'nodes': 3, 'coupling_strength': 1.0, 'frequency_base': 2.0},
                'domain': (-3, 3),
                'style': 'magnitude_phase'
            },
            '16_consciousness_network_large': {
                'concept': 'Consciousness (Large)',
                'potential': self.potlib.consciousness_network,
                'params': {'nodes': 12, 'coupling_strength': 1.2, 'frequency_base': 2.5},
                'domain': (-6, 6),
                'style': 'magnitude_phase'
            },
            
            # SPECIAL CASES & VARIATIONS (4 images)
            '17_resonance_tight': {
                'concept': 'Resonance Tight',
                'potential': self.potlib.proton_resonance,
                'params': {'harmonics': [1, 3, 5], 'binding_strength': 3.0},
                'domain': (-2, 2),
                'style': 'magnitude_phase'
            },
            '18_resonance_loose': {
                'concept': 'Resonance Loose',
                'potential': self.potlib.proton_resonance,
                'params': {'harmonics': [1, 2], 'binding_strength': 1.0},
                'domain': (-4, 4),
                'style': 'frequency'
            },
            '19_inward_convergence': {
                'concept': 'Inward Convergence',
                'potential': self.potlib.gravity_well,
                'params': {'mass': 10.0, 'scale': 0.1},
                'domain': (-2, 2),
                'style': 'magnitude_phase'
            },
            '20_outward_propagation': {
                'concept': 'Outward Propagation',
                'potential': self.potlib.photon_propagating,
                'params': {'f': 5, 'direction': [1, 0], 'decay': 0.02},
                'domain': (-5, 5),
                'style': 'frequency'
            },
        }
        
        # Generate all images
        total = len(images)
        for idx, (name, spec) in enumerate(images.items(), 1):
            print(f"[{idx:2d}/{total}] {name:<30s} ", end='', flush=True)
            self.generate_image(
                name,
                spec['concept'],
                spec['potential'],
                spec['params'],
                domain=spec['domain'],
                render_style=spec['style']
            )
        
        # Summary
        print("\n" + "="*70)
        success = sum(1 for r in self.results.values() if r['status'] == 'success')
        failed = sum(1 for r in self.results.values() if r['status'] == 'error')
        
        print(f"GENERATION COMPLETE: {success} succeeded, {failed} failed")
        print("="*70)
        
        # List outputs
        print("\nGenerated images:")
        for name, result in self.results.items():
            if result['status'] == 'success':
                print(f"  ✓ {name:<30s} → {result['concept']}")
        
        if failed > 0:
            print("\nFailed images:")
            for name, result in self.results.items():
                if result['status'] == 'error':
                    print(f"  ✗ {name:<30s} → {result['error']}")
        
        print(f"\nAll images saved to: {self.output_dir}/")
        
        return failed == 0


def main():
    generator = BatchImageGenerator()
    success = generator.generate_all()
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
