"""
UPFM Potential Function Library
Defines potential functions Φ(x,y) for different concepts.

Each potential encodes the physical/conceptual structure in its landscape.
"""

import numpy as np
from scipy import special


class PotentialLibrary:
    """Library of potential functions for UPFM image generation."""
    
    @staticmethod
    def gaussian(x, y, sigma=0.5):
        """Simple 2D Gaussian potential (generic smooth potential)."""
        return np.exp(-(x**2 + y**2) / (2 * sigma**2))
    
    @staticmethod
    def electron_spiral(x, y, f_e=12, r_e=0.15, barrier_height=5.0):
        """
        Electron potential: High-frequency confined spiral pattern.
        
        Structure:
        - Central confinement (harmonic potential)
        - High frequency modulation (creates spiral)
        - Barrier to keep field bound
        
        Args:
            f_e: Frequency of spiral (higher = tighter coils)
            r_e: Characteristic radius of confinement
            barrier_height: Height of confinement potential
        """
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        
        # Harmonic confinement + angular frequency modulation
        confinement = barrier_height * (r_e**2 / (r**2 + r_e**2))
        spiral = f_e * np.sin(f_e * theta)
        
        # Combine: creates tight spiral confined to central region
        phi = confinement + spiral
        
        return phi
    
    @staticmethod
    def photon_propagating(x, y, f=8, direction=None, decay=0.1):
        """
        Photon potential: Free-space propagating spiral.
        
        Structure:
        - Plane wave oscillation (no confinement)
        - Gaussian envelope (natural decay)
        - Extends outward freely
        
        Args:
            f: Frequency of oscillation
            direction: Direction of propagation [dx, dy]
            decay: Envelope decay rate
        """
        if direction is None:
            direction = [1, 0]
        
        # Propagation direction
        k = f * np.array(direction) / np.linalg.norm(direction)
        
        # Plane wave
        r_vec = np.stack([x, y], axis=-1)
        phase = k[0] * x + k[1] * y
        wave = np.sin(phase)
        
        # Gaussian envelope (free-space decay)
        r_mag = np.sqrt(x**2 + y**2)
        envelope = np.exp(-decay * r_mag)
        
        return wave * envelope
    
    @staticmethod
    def proton_resonance(x, y, harmonics=None, binding_strength=2.0):
        """
        Proton potential: Multiple harmonically-locked resonances.
        
        Structure:
        - Multiple frequency components
        - Each confined to center
        - Phase-locked together
        
        Args:
            harmonics: List of harmonic ratios [1, 2, 3] for triad
            binding_strength: How strongly bound the resonances are
        """
        if harmonics is None:
            harmonics = [1, 2, 3]
        
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        
        phi = np.zeros_like(x)
        
        # Sum harmonic potentials
        for h in harmonics:
            # Angular modulation at harmonic frequency
            angular = np.cos(h * theta)
            
            # Radial confinement (tighter for higher harmonics)
            radial = binding_strength / (h * (r + 0.1))
            
            phi += angular * radial
        
        return phi
    
    @staticmethod
    def gravity_well(x, y, mass=1.0, scale=1.0):
        """
        Gravity potential: Large-scale inward convergence.
        
        Structure:
        - 1/r form (like gravitational potential)
        - Extended spatial scale
        - Simple, smooth convergence
        
        Args:
            mass: Strength of gravitational attraction
            scale: Softening parameter (prevents singularity)
        """
        r = np.sqrt(x**2 + y**2 + scale**2)
        
        # Gravitational potential
        phi = -mass / r
        
        return phi
    
    @staticmethod
    def galaxy_spiral(x, y, M_center=10.0, a_core=0.5, spiral_arms=2.0, 
                     rotation_rate=2.0):
        """
        Galaxy potential: Spiral galaxy rotation with central mass.
        
        Structure:
        - Central gravitational well (supermassive black hole)
        - Rotational perturbation (creates spiral arms)
        - Balance of inward (gravity) and circular (rotation)
        
        Args:
            M_center: Central mass strength
            a_core: Core size (prevents singularity)
            spiral_arms: Number of spiral arms
            rotation_rate: How fast the spiral pattern rotates
        """
        r = np.sqrt(x**2 + y**2 + 0.1)
        theta = np.arctan2(y, x)
        
        # Central gravitational potential
        gravity = -M_center / (r + a_core)
        
        # Spiral arm perturbation
        spiral = spiral_arms * np.sin(spiral_arms * theta - rotation_rate * np.log(r + 0.1))
        spiral = spiral / (r + 0.5)  # Decay with radius
        
        phi = gravity + spiral
        
        return phi
    
    @staticmethod
    def consciousness_network(x, y, nodes=7, coupling_strength=1.0, 
                            frequency_base=3.0):
        """
        Consciousness potential: Network of information processing nodes.
        
        Structure:
        - Multiple nodes arranged in circle
        - Harmonic coupling between nodes
        - Creates interference patterns (information integration)
        
        Args:
            nodes: Number of processing nodes
            coupling_strength: How strongly nodes interact
            frequency_base: Base frequency of oscillation
        """
        phi = np.zeros_like(x)
        
        # Arrange nodes in circle
        angles = np.linspace(0, 2*np.pi, nodes, endpoint=False)
        node_positions = [(2.0 * np.cos(a), 2.0 * np.sin(a)) for a in angles]
        
        # Create potential from superposition of harmonic sources
        for node_x, node_y in node_positions:
            # Distance from node
            r_to_node = np.sqrt((x - node_x)**2 + (y - node_y)**2)
            
            # Harmonic potential centered at node
            # (like interference pattern from oscillating source)
            potential_from_node = coupling_strength * np.cos(frequency_base * r_to_node) / (r_to_node + 0.3)
            phi += potential_from_node
        
        return phi
    
    @staticmethod
    def black_hole_reversal(x, y, inversion_radius=0.5, strength=5.0):
        """
        Black hole reversal cycle potential.
        
        Structure:
        - Extreme inward convergence toward singularity
        - Sharp reversal at Planck scale
        - Outward ejection afterward
        
        Args:
            inversion_radius: Where inversion occurs
            strength: How strong the convergence is
        """
        r = np.sqrt(x**2 + y**2)
        
        # Inward convergence
        inward = -strength / (r + inversion_radius)
        
        # Reversal at small scale (sharp change in sign)
        reversal = strength * np.sin(np.pi * r / inversion_radius) * (r < inversion_radius)
        
        phi = inward + reversal
        
        return phi
    
    @staticmethod
    def information_entropy_landscape(x, y, ordered_regions=2, temperature=1.0):
        """
        Information/Entropy landscape: Learning and compression.
        
        Structure:
        - High entropy (flat, disordered) regions
        - Low entropy (deep minima, ordered) regions
        - Shows learning as entropy reduction
        
        Args:
            ordered_regions: Number of ordered minima
            temperature: Thermal noise level
        """
        phi = np.zeros_like(x)
        
        # Create multiple minima (ordered states)
        angles = np.linspace(0, 2*np.pi, ordered_regions, endpoint=False)
        for angle in angles:
            min_x = 2.0 * np.cos(angle)
            min_y = 2.0 * np.sin(angle)
            
            # Deep well at each minimum
            r_to_min = np.sqrt((x - min_x)**2 + (y - min_y)**2)
            phi -= 10.0 / (r_to_min + 0.2)
        
        # Add thermal noise (temperature)
        phi += temperature * np.sin(10*x) * np.cos(10*y)
        
        return phi


# Validation and testing
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    lib = PotentialLibrary()
    
    # Create test grid
    x = np.linspace(-3, 3, 256)
    y = np.linspace(-3, 3, 256)
    X, Y = np.meshgrid(x, y)
    
    # Test a few potentials
    potentials = {
        'electron_spiral': lib.electron_spiral(X, Y),
        'photon_propagating': lib.photon_propagating(X, Y),
        'gravity_well': lib.gravity_well(X, Y),
        'galaxy_spiral': lib.galaxy_spiral(X, Y),
        'consciousness_network': lib.consciousness_network(X, Y),
    }
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for idx, (name, phi) in enumerate(potentials.items()):
        axes[idx].imshow(phi, extent=[-3, 3, -3, 3], cmap='RdBu_r', origin='lower')
        axes[idx].set_title(f'{name}')
        axes[idx].set_xlabel('x')
        axes[idx].set_ylabel('y')
    
    axes[-1].axis('off')
    
    plt.tight_layout()
    plt.savefig('c:\\Determined\\potentials_test.png', dpi=150, bbox_inches='tight')
    print("✓ Potential library test figure saved: potentials_test.png")
