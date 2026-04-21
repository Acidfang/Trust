#!/usr/bin/env python3
"""
Test the field solver on electron spiral to verify it converges correctly
"""

import numpy as np
import matplotlib.pyplot as plt
from upfm_field_solver import FieldSolver
from upfm_field_renderer import FieldRenderer
from upfm_potential_library import PotentialLibrary

# Solve electron spiral
solver = FieldSolver(grid_size=256, domain=[-2, 2])
print("Solving electron spiral...")
result = solver.solve(
    PotentialLibrary.electron_spiral,
    t_max=200,
    dt=0.05,
    epsilon=1e-3,
    init_scale=0.1
)

print(f"Converged: {result['converged']}")
print(f"Iterations: {result['iterations']}")

field = result['field']

# Analyze the field
mags = np.abs(field)
phases = np.angle(field)

print(f"\nField magnitude stats:")
print(f"  Min: {np.min(mags):.6f}")
print(f"  Max: {np.max(mags):.6f}")
print(f"  Mean: {np.mean(mags):.6f}")
print(f"  Std: {np.std(mags):.6f}")

print(f"\nField phase stats:")
print(f"  Min: {np.min(phases):.6f}")
print(f"  Max: {np.max(phases):.6f}")
print(f"  Mean: {np.mean(phases):.6f}")
print(f"  Std: {np.std(phases):.6f}")

# Render with different methods
renderer = FieldRenderer(grid_size=256)

fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle('Electron Spiral Field Solution Analysis', fontsize=16, fontweight='bold')

# Magnitude
ax = axes[0, 0]
im = ax.imshow(mags, extent=[-2, 2, -2, 2], origin='lower', cmap='hot')
ax.set_title('Field Magnitude |i|')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.colorbar(im, ax=ax)

# Phase
ax = axes[0, 1]
im = ax.imshow(phases, extent=[-2, 2, -2, 2], origin='lower', cmap='hsv')
ax.set_title('Field Phase arg(i)')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.colorbar(im, ax=ax, label='Phase (radians)')

# Magnitude-Phase rendering (HSV)
ax = axes[1, 0]
hsv_image = renderer.render_magnitude_phase(field)
ax.imshow(hsv_image, extent=[-2, 2, -2, 2], origin='lower')
ax.set_title('HSV Rendering (Magnitude-Phase)')
ax.set_xlabel('x')
ax.set_ylabel('y')

# Frequency map
ax = axes[1, 1]
freq_image = renderer.render_frequency_map(field)
ax.imshow(freq_image, extent=[-2, 2, -2, 2], origin='lower', cmap='turbo')
ax.set_title('Frequency Map (Phase Gradient)')
ax.set_xlabel('x')
ax.set_ylabel('y')

plt.tight_layout()
plt.savefig('c:/Determined/electron_field_test.png', dpi=150, bbox_inches='tight')
print("\n✓ Saved: electron_field_test.png")

# Check if spiral pattern exists in the phase
print("\nPhase patterns at different radii:")
center = 128
for r in [10, 20, 40, 60]:
    angles = np.linspace(0, 2*np.pi, 16, endpoint=False)
    phase_vals = []
    for angle in angles:
        x = int(center + r * np.cos(angle))
        y = int(center + r * np.sin(angle))
        if 0 <= x < 256 and 0 <= y < 256:
            phase_vals.append(phases[y, x])
    
    phase_diffs = np.diff(np.array(phase_vals + [phase_vals[0]]))
    print(f"  r={r:2d}: phase_diffs mean={np.mean(phase_diffs):.4f} (should be consistent for spiral)")
