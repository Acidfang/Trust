#!/usr/bin/env python3
"""
Visualize potential functions to verify they look correct
before deploying to JavaScript
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

def electron_spiral(x, y, fe=12, re=0.15):
    """Electron spiral potential"""
    r = np.sqrt(x**2 + y**2) + 0.01
    theta = np.arctan2(y, x)
    spiral = fe * theta - 8 * r
    confinement = 3 * np.exp(-r / re)
    return np.sin(spiral) + confinement

def photon_propagating(x, y, f=8, direction=0.5, decay=0.1):
    """Photon propagating potential"""
    kx = f * np.cos(direction)
    ky = f * np.sin(direction)
    wave = np.sin(kx * x + ky * y)
    envelope = np.exp(-decay * (x**2 + y**2))
    return wave * envelope

def proton_resonance(x, y, harmonics=[1,2,3], binding=2.0):
    """Proton resonance potential"""
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    
    potential = np.zeros_like(x)
    for h in harmonics:
        potential += np.cos(h * theta)
    
    potential += binding * r**2
    return potential

def gravity_well(x, y, mass=1.0, scale=1.0):
    """Gravity well potential"""
    r = np.sqrt(x**2 + y**2) + 0.01
    return -(mass / r) * scale

def galaxy_spiral(x, y, M=10, arms=2, rotation=2):
    """Galaxy spiral potential"""
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    
    gravity = -(M / (r + 0.1))
    spiral_pattern = np.cos(arms * (theta - rotation * np.log(r + 1)))
    
    return gravity + 0.5 * spiral_pattern

def consciousness_network(x, y, nodes=7, coupling=1.5, frequency=3.0):
    """Consciousness network potential"""
    potential = np.zeros_like(x)
    
    for n in range(nodes):
        angle = (2 * np.pi * n) / nodes
        cx = np.cos(angle)
        cy = np.sin(angle)
        dist = np.sqrt((x - cx)**2 + (y - cy)**2)
        
        potential += coupling * np.exp(-dist * dist)
        potential += frequency * np.sin(n * np.arctan2(y - cy, x - cx))
    
    return potential

# Create grid
size = 256
x = np.linspace(-2, 2, size)
y = np.linspace(-2, 2, size)
X, Y = np.meshgrid(x, y)

# Create potentials
potentials = {
    'Electron Spiral': electron_spiral(X, Y),
    'Photon Propagating': photon_propagating(X, Y),
    'Proton Resonance': proton_resonance(X, Y),
    'Gravity Well': gravity_well(X, Y),
    'Galaxy Spiral': galaxy_spiral(X, Y),
    'Consciousness Network': consciousness_network(X, Y),
}

# Plot them
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('UPFM Potential Functions', fontsize=16, fontweight='bold')

for (name, potential), ax in zip(potentials.items(), axes.flat):
    # Clip extreme values for better visualization
    vmin = np.percentile(potential, 5)
    vmax = np.percentile(potential, 95)
    
    im = ax.imshow(potential, extent=[-2, 2, -2, 2], origin='lower', 
                   cmap='hsv', vmin=vmin, vmax=vmax)
    ax.set_title(name, fontweight='bold')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_aspect('equal')
    plt.colorbar(im, ax=ax, label='Φ(x,y)')

plt.tight_layout()
plt.savefig('c:/Determined/potential_visualization.png', dpi=150, bbox_inches='tight')
print("✓ Saved: potential_visualization.png")

# Print statistics
print("\nPotential Statistics:")
print("-" * 60)
for name, potential in potentials.items():
    print(f"\n{name}:")
    print(f"  Min: {np.min(potential):.4f}")
    print(f"  Max: {np.max(potential):.4f}")
    print(f"  Mean: {np.mean(potential):.4f}")
    print(f"  Std: {np.std(potential):.4f}")
    
    # Check if it looks like a spiral (has rotational symmetry pattern)
    center = size // 2
    radii = np.array([20, 40, 60, 80])
    print(f"  Center value: {potential[center, center]:.4f}")
    for r in radii:
        # Sample at cardinal directions
        if center + r < size:
            vals = [
                potential[center, center + r],
                potential[center + r, center],
                potential[center, center - r],
                potential[center - r, center]
            ]
            print(f"    At r={r}: {vals}")
