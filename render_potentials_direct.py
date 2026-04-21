#!/usr/bin/env python3
"""
Direct potential rendering - no solver needed
Just visualize the potential functions as images
Build concentrically from center outward
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def render_potential_as_field(potential_func, grid_size=256, domain=[-2, 2], name="Potential"):
    """
    Directly render a potential function as a field image
    No solving needed - the potential IS the field
    """
    x = np.linspace(domain[0], domain[1], grid_size)
    y = np.linspace(domain[0], domain[1], grid_size)
    X, Y = np.meshgrid(x, y)
    
    # Compute potential at every point
    phi = potential_func(X, Y)
    
    # Normalize for visualization
    phi_normalized = (phi - np.min(phi)) / (np.max(phi) - np.min(phi) + 1e-6)
    
    # Convert to HSV: use phi as hue (rotational phase)
    # Magnitude as value (brightness)
    from matplotlib.colors import hsv_to_rgb
    
    h = (phi / (2 * np.pi)) % 1.0  # Hue wraps around
    s = np.ones_like(h)  # Full saturation
    v = phi_normalized  # Brightness from normalized potential
    
    hsv = np.stack([h, s, v], axis=-1)
    rgb = hsv_to_rgb(hsv)
    rgb = (rgb * 255).astype(np.uint8)
    
    return Image.fromarray(rgb)

# Define potentials
def electron_spiral(x, y):
    """Electron orbital visualization using quantum mechanical probability density.
    
    Combines orbital types from quantum mechanics:
    - Radial: hydrogen-like decay e^(-αr) showing shell structure
    - Angular: spherical harmonics creating s, p, d orbital shapes
    - Uses contour visualization showing where 90% probability density lies
    """
    r = np.sqrt(x**2 + y**2) + 1e-10
    theta = np.arctan2(y, x)
    
    # Radial decay: hydrogen-like (principal quantum number effects)
    # 1s orbital: single lobe, densest at center, exponential decay
    # 2p orbital: nodal plane, two lobes
    radial_envelope = np.exp(-1.5 * r)  # Orbital decay length
    
    # Angular structure: combine multiple orbital symmetries
    # s-orbital component: spherically symmetric contribution
    s_component = 1.0
    
    # p-orbital component: dumbbell shape (two lobes along x-axis)
    p_component = np.cos(theta)
    
    # d-orbital component: cloverleaf pattern (four lobes)
    d_component = np.cos(2 * theta)
    
    # Mix orbital types for rich structure (realistic multi-electron atom)
    angular_structure = 0.4*s_component + 0.3*p_component + 0.3*d_component
    
    # Probability density: |ψ(r,θ)|^2
    phi = radial_envelope * angular_structure
    return phi
    
    # Radial decay: hydrogen-like (principal quantum number effects)
    # 1s orbitwave propagation using plane wave + amplitude modulation.
    
    Visualizes electromagnetic wave characteristics:
    - Sinusoidal oscillation: periodic spatial variation at wavelength λ
    - Gaussian envelope: amplitude modulation controlling wave packet extent
    - Frequency encoded in wavenumber k = 2π/λ
    """
    # Wavenumber defining wavelength of oscillation
    k_magnitude = 8.0  # Controls wavelength
    
    # Wave direction at 45 degrees (arbitrarily chosen propagation direction)
    propagation_angle = 0.5  # radians
    kx = k_magnitude * np.cos(propagation_angle)
    ky = k_magnitude * np.sin(propagation_angle)
    
    # Plane wave: sinusoidal oscillation in space
    oscillation = np.sin(kx * x + ky * y)
    
    # Gaussian envelope: amplitude modulation (wave packet confinement)
    # Standard deviation controls how long wave packet extends
    envelope_width = 0.1
    amplitude_envelope = np.exp(-envelope_width * (x**2 + y**2))
    
    # Complete wave: oscillation modulated by envelope
    phi = oscillation * amplitude_envelope
    return phi
    # p-orbital component: dumbbell shape (two lobes along x-axis)
    p_component = np.cos(theta)
    using logarithmic spiral pattern.
    
    Represents density waves in galactic disks:
    - Logarithmic spiral: r = a × e^(k×θ) (self-similar property)
    - Pitch angle: ~12° for Milky Way-like galaxies
    - Star formation in density wave compression regions
    - Constant pitch maintains spiral arm shape as galaxy rotates
    """
    r = np.sqrt(x**2 + y**2) + 0.1  # Avoid singularity at origin
    theta = np.arctan2(y, x)
    
    # Logarithmic spiral definition: φ = (1/k) ln(r/a)
    # Rearranged: phase ∝ θ - ln(r) gives the spiral structure
    # k = tan(pitch_angle), pitch ≈ 12° for Milky Way
    pitch_coefficient = 2.0  # Controls how tightly wound the spiral is
    
    # Logarithmic spiral equation in polar form
    spiral_phase = pitch_coefficient * (theta - np.log(r + 1))
    
    # Star formation intensity: density waves cause compression
    # Exponential radial falloff: stars concentrated in disk
    disk_profile = np.exp(-(r**2) / (2 * 1.0**2))  # Broader for galactic scale
    
    phi = spiral_phase * disk_profile
    return phingular_structure
    return phi

def photon_propagatinas distributed neural network activation.
    
    Represents brain information processing:
    - Nodes: neurons positioned in heptagonal symmetry (7 brain regions)
    - Node strength: Gaussian activation envelope (synaptic integration)
    - Connections: phase coupling between nodes (neural oscillations)
    - Field pattern: emergent behavior from local interactions
    """
    field = np.zeros_like(x)
    
    # Heptagonal arrangement: 7 primary brain regions/nodes
    # (approximate: visual, auditory, motor, language, memory, emotion, integration)
    num_nodes = 7
    node_radius = 0.6  # Distance from center to node positions
    
    for node_idx in range(num_nodes):
        # Position of this brain region node
        angle = (2 * np.pi * node_idx) / num_nodes
        node_x = node_radius * np.cos(angle)
        node_y = node_radius * np.sin(angle)
        
        # Distance from this node
        distance_from_node = np.sqrt((x - node_x)**2 + (y - node_y)**2)
        
        # Local neural field: Gaussian activation (soma, dendrites)
        # Represents synaptic integration field
        local_activation = 2.0 * np.exp(-distance_from_node**2 / 0.3)
        
        # Phase coupling: oscillatory interaction between nodes
        # Represents neural synchronization and information transfer
        local_phase = 0.3 * np.sin(node_idx * np.arctan2(y - node_y, x - node_x))
        
        # Combine local field and phase interactions
        field += local_activation + local_phaseation direction)
    propagation_angle = 0.5  # radians
    kx = k_magnitude * np.cos(propagation_angle)
    ky = k_magnitude * np.sin(propagation_angle)
    
    # Plane wave: sinusoidal oscillation in space
    oscillation = np.sin(kx * x + ky * y)
    
    # Gaussian envelope: amplitude modulation (wave packet confinement)
    # Standard deviation controls how long wave packet extends
    envelope_width = 0.1
    amplitude_envelope = np.exp(-envelope_width * (x**2 + y**2))
    
    # Complete wave: oscillation modulated by envelope
    phi = oscillation * amplitude_envelope
    return phi

def galaxy_spiral(x, y):
    """Galaxy spiral using logarithmic spiral pattern.
    
    Represents density waves in galactic disks:
    - Logarithmic spiral: r = a × e^(k×θ) (self-similar property)
    - Pitch angle: ~12° for Milky Way-like galaxies
    - Star formation in density wave compression regions
    - Constant pitch maintains spiral arm shape as galaxy rotates
    """
    r = np.sqrt(x**2 + y**2) + 0.1  # Avoid singularity at origin
    theta = np.arctan2(y, x)
    
    # Logarithmic spiral definition: φ = (1/k) ln(r/a)
    # Rearranged: phase ∝ θ - ln(r) gives the spiral structure
    # k = tan(pitch_angle), pitch ≈ 12° for Milky Way
    pitch_coefficient = 2.0  # Controls how tightly wound the spiral is
    
    # Logarithmic spiral equation in polar form
    spiral_phase = pitch_coefficient * (theta - np.log(r + 1))
    
    # Star formation intensity: density waves cause compression
    # Exponential radial falloff: stars concentrated in disk
    disk_profile = np.exp(-(r**2) / (2 * 1.0**2))  # Broader for galactic scale
    
    phi = spiral_phase * disk_profile
    return phi

def consciousness_network(x, y):
    """Consciousness as distributed neural network activation.
    
    Represents brain information processing:
    - Nodes: neurons positioned in heptagonal symmetry (7 brain regions)
    - Node strength: Gaussian activation envelope (synaptic integration)
    - Connections: phase coupling between nodes (neural oscillations)
    - Field pattern: emergent behavior from local interactions
    """
    field = np.zeros_like(x)
    
    # Heptagonal arrangement: 7 primary brain regions/nodes
    # (approximate: visual, auditory, motor, language, memory, emotion, integration)
    num_nodes = 7
    node_radius = 0.6  # Distance from center to node positions
    
    for node_idx in range(num_nodes):
        # Position of this brain region node
        angle = (2 * np.pi * node_idx) / num_nodes
        node_x = node_radius * np.cos(angle)
        node_y = node_radius * np.sin(angle)
        
        # Distance from this node
        distance_from_node = np.sqrt((x - node_x)**2 + (y - node_y)**2)
        
        # Local neural field: Gaussian activation (soma, dendrites)
        # Represents synaptic integration field
        local_activation = 2.0 * np.exp(-distance_from_node**2 / 0.3)
        
        # Phase coupling: oscillatory interaction between nodes
        # Represents neural synchronization and information transfer
        local_phase = 0.3 * np.sin(node_idx * np.arctan2(y - node_y, x - node_x))
        
        # Combine local field and phase interactions
        field += local_activation + local_phase
    
    return field

# Generate images
concepts = {
    'Electron Spiral': electron_spiral,
    'Photon Propagating': photon_propagating,
    'Galaxy Spiral': galaxy_spiral,
    'Consciousness Network': consciousness_network,
}

fig, axes = plt.subplots(2, 2, figsize=(12, 12))
fig.suptitle('UPFM Direct Field Visualization', fontsize=16, fontweight='bold')

for (name, func), ax in zip(concepts.items(), axes.flat):
    img = render_potential_as_field(func, grid_size=256, name=name)
    ax.imshow(img, extent=[-2, 2, -2, 2], origin='lower')
    ax.set_title(name, fontweight='bold')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_aspect('equal')
    
    # Save individual image
    filename = f'c:/Determined/{name.lower().replace(" ", "_")}_direct.png'
    img.save(filename)
    print(f"✓ Saved: {filename}")

plt.tight_layout()
plt.savefig('c:/Determined/direct_field_visualization.png', dpi=150, bbox_inches='tight')
print("✓ Saved: direct_field_visualization.png")

print("\n✓ Direct field rendering complete - no solver needed!")
