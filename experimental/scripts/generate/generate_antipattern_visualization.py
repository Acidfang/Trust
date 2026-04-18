"""
Generate visual representation of antipattern chains.
Shows structural corruption: signal degradation, cascading failures, converging pathways.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np
from matplotlib.collections import LineCollection
import matplotlib.lines as mlines

# Create figure with high DPI
fig, ax = plt.subplots(figsize=(16, 10), dpi=150)
fig.patch.set_facecolor('#0a0e27')
ax.set_facecolor('#0a0e27')

# Set limits
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# ========== LAYER 1: PRESSURE AT SOURCE ==========
pressure_circle = Circle((10, 50), 3, color='#ff4444', alpha=0.8, zorder=10)
ax.add_patch(pressure_circle)
ax.text(10, 43, 'PRESSURE', ha='center', fontsize=9, color='#ff4444', weight='bold')

# Pressure rays
for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
    x_end = 10 + 4 * np.cos(angle)
    y_end = 50 + 4 * np.sin(angle)
    ax.plot([10, x_end], [50, y_end], color='#ff4444', alpha=0.3, linewidth=1)

# ========== LAYER 2: CHOICE FORK ==========
# Left path (short-term, local optimization) - LEADS TO FAILURE
ax.annotate('', xy=(18, 65), xytext=(12, 55),
            arrowprops=dict(arrowstyle='->', lw=2, color='#ff6666', alpha=0.7))
ax.text(15, 62, 'FAST\n(local)', ha='center', fontsize=8, color='#ff6666', style='italic')

# Right path (long-term, structural) - LEADS TO SUCCESS
ax.annotate('', xy=(18, 35), xytext=(12, 45),
            arrowprops=dict(arrowstyle='->', lw=2, color='#44ff44', alpha=0.7))
ax.text(15, 38, 'RIGHT\n(structural)', ha='center', fontsize=8, color='#44ff44', style='italic')

# ========== LAYER 3: SIGNAL DEGRADATION THROUGH LAYERS (top path) ==========
# Show signal getting corrupted through multiple layers
layer_x_positions = [20, 30, 40, 50, 60, 70, 80]
layer_colors = ['#ffff00', '#ffaa00', '#ff6600', '#ff3300', '#dd0000', '#880000', '#000000']
layer_alphas = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.2]

# Clean signal enters on left
signal_y = 65
ax.plot([18, 20], [signal_y, signal_y], color='#00ff00', linewidth=3, label='Original Signal')
ax.text(18.5, 68, 'CLEAR', fontsize=7, color='#00ff00', weight='bold')

# Signal passes through layers, degrading
for i, (x, color, alpha) in enumerate(zip(layer_x_positions, layer_colors, layer_alphas)):
    # Draw layer as vertical band
    layer_rect = FancyBboxPatch((x-0.8, 50), 1.6, 30, 
                                boxstyle="round,pad=0.1", 
                                edgecolor=color, facecolor=color, 
                                alpha=alpha*0.3, linewidth=2)
    ax.add_patch(layer_rect)
    
    # Draw signal passing through (increasingly noisy)
    if i < len(layer_x_positions) - 1:
        next_x = layer_x_positions[i+1]
        # Add noise to signal path
        noise = np.random.randn() * (i * 2)
        ax.plot([x, next_x], [signal_y + noise, signal_y + np.random.randn() * (i+1) * 2], 
               color=color, linewidth=2-i*0.2, alpha=alpha)
    
    ax.text(x, 48, f'L{i+1}', ha='center', fontsize=7, color=color, weight='bold')

# Signal ends as noise
ax.text(82, 65, 'CORRUPTED\n↓\nNOISE', fontsize=8, color='#000000', weight='bold', 
        bbox=dict(boxstyle='round', facecolor='#ff0000', alpha=0.3))

# ========== LAYER 4: CASCADING FAILURES (middle section) ==========
# Show 12 chains converging
cascade_y_start = 50
chains_data = [
    (25, 75, 'Abstraction'),
    (28, 72, 'Coupling'),
    (31, 69, 'Deferred'),
    (34, 66, 'Cargo'),
    (37, 63, 'Local Opt'),
    (40, 60, 'Context'),
    (43, 57, 'Argument'),
    (46, 54, 'Survivorship'),
    (49, 51, 'All-or-Nothing'),
    (52, 48, 'Correlation'),
    (55, 45, 'Externalized'),
    (58, 42, 'Ignored Signal'),
]

# Draw each chain as a path to center
center_x, center_y = 75, 50
for start_x, start_y, label in chains_data:
    # Draw curved path to center (convergence point)
    x_curve = np.linspace(start_x, center_x, 50)
    y_curve = np.linspace(start_y, center_y, 50) + np.sin(np.linspace(0, np.pi, 50)) * 3
    ax.plot(x_curve, y_curve, color='#ff6600', linewidth=1.5, alpha=0.4)
    
    # Label each chain
    ax.text(start_x-2, start_y, label, fontsize=6, color='#ffccaa', rotation=0, alpha=0.7)

# ========== LAYER 5: CONVERGENCE POINT (FAILURE) ==========
failure_circle = Circle((center_x, center_y), 4, color='#000000', alpha=0.9, ec='#ff0000', linewidth=3, zorder=20)
ax.add_patch(failure_circle)
ax.text(center_x, center_y, 'X', ha='center', va='center', fontsize=24, color='#ff0000', 
        weight='bold', zorder=21)
ax.text(center_x, center_y-7, 'SYSTEM\nFAILURE', ha='center', fontsize=9, color='#ff0000', 
        weight='bold', style='italic')

# Add corruption markers radiating from center
for angle in np.linspace(0, 2*np.pi, 16, endpoint=False):
    x_end = center_x + 8 * np.cos(angle)
    y_end = center_y + 8 * np.sin(angle)
    ax.plot([center_x, x_end], [center_y, y_end], color='#ff0000', alpha=0.2, linewidth=1)

# ========== LAYER 6: RIGHTEOUS PATH (bottom) ==========
# Show the structural approach succeeding
success_y = 35
ax.plot([18, 80], [success_y, success_y], color='#00ff00', linewidth=3, linestyle='--', 
        label='Structural Path', alpha=0.8)
ax.text(20, 30, 'Remove layers → Direct signal', fontsize=9, color='#00ff00', weight='bold')
ax.text(20, 27, 'Measure at each stage → Catch corruption', fontsize=9, color='#00ff00', weight='bold')
ax.text(20, 24, 'Independence not interdependence → Resilience', fontsize=9, color='#00ff00', weight='bold')

# Success endpoint
success_circle = Circle((80, success_y), 3, color='#00ff00', alpha=0.8, zorder=10)
ax.add_patch(success_circle)
ax.text(80, 20, 'COHERENT\nSYSTEM', ha='center', fontsize=9, color='#00ff00', weight='bold')

# ========== TITLE & LEGEND ==========
ax.text(50, 95, 'ANTIPATTERN CHAINS: ALL PATHS LEAD TO SYSTEM FAILURE', 
        ha='center', fontsize=14, color='#ffffff', weight='bold', 
        bbox=dict(boxstyle='round', facecolor='#1a1f3a', alpha=0.8))

ax.text(50, 10, 'Pressure → Choose Short-term → Add Layers → Corruption Compounds → Cascading Failures → System Dies', 
        ha='center', fontsize=9, color='#ffaa00', style='italic', weight='bold',
        bbox=dict(boxstyle='round', facecolor='#1a1f3a', alpha=0.6))

# Add legend
legend_elements = [
    mlines.Line2D([0], [0], color='#ff0000', lw=3, label='Failure Path (12 chains converge)'),
    mlines.Line2D([0], [0], color='#00ff00', lw=3, linestyle='--', label='Success Path (structural integrity)'),
    mlines.Line2D([0], [0], color='#ffff00', lw=2, label='Signal Degradation Through Layers'),
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=8, 
         framealpha=0.8, facecolor='#1a1f3a', edgecolor='#666666')

# ========== SAVE ==========
plt.tight_layout()
plt.savefig('c:\\Determined\\src\\applications\\ANTIPATTERN_CHAINS_VISUALIZATION.png', 
            bbox_inches='tight', facecolor='#0a0e27', dpi=150)
print("✓ Image generated: ANTIPATTERN_CHAINS_VISUALIZATION.png")

# Also save high-res version
plt.savefig('c:\\Determined\\src\\applications\\ANTIPATTERN_CHAINS_VISUALIZATION_HD.png', 
            bbox_inches='tight', facecolor='#0a0e27', dpi=300)
print("✓ High-res image generated: ANTIPATTERN_CHAINS_VISUALIZATION_HD.png")

plt.close()
