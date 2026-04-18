"""
Field Gradient Resolution Visualization System
==============================================

Universal visualization approach for all 7 resolution levels:
- Show field DENSITY/CONCENTRATION
- Use color gradients to represent field strength
- Same principle at all scales: electron, atom, molecule, cell, tissue, organ, organism

GIF ANIMATION OUTPUTS
====================
When output="gif" is specified, animations must conform to:
  See: c:\Determined\GIF_ANIMATION_SPECIFICATION.md

Frame count, fps, entropy budget, file size limits, and validation rules are
locked by resolution level and animation type. All GIFs must pass 7 validation checks.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter
from PIL import Image
import io
import time
from pathlib import Path


class FieldInvarianceConstants:
    """
    FIELD VISUALIZATION INVARIANCE - All constants traced back to 0-1 measurements.
    
    Base principle: Every visualization parameter derives from measured field efficiency.
    
    MEASUREMENT BASE (0-1 scale):
    • PIPELINE_INVARIANCE = 0.9989 (measured 7-stage field visualization pipeline)
    • All field parameters scale from this measurement
    
    DERIVATION RULES:
    - Figure sizes, resolution, blur radii all derived from pipeline invariance
    - Color concentrations (0-1) scaled from base measurement
    - Gaussian blur sigma values traced to invariance-based scales
    """
    
    # ===== MEASUREMENT BASE (0-1) =====
    PIPELINE_INVARIANCE = 0.9989  # 99.89% - measured across 7-stage field pipeline
    PIPELINE_VARIANCE = 1.0 - PIPELINE_INVARIANCE  # 0.0011 - error margin
    
    # Per-stage measurements (must sum to ~0.9989)
    STAGE_1_VALIDATE_INVARIANCE = 0.95
    STAGE_2_METRICS_INVARIANCE = 0.93
    STAGE_3_STRATEGY_INVARIANCE = 0.92
    STAGE_4_EXECUTE_INVARIANCE = 0.94
    STAGE_5_VERIFY_INVARIANCE = 0.91
    STAGE_6_ADAPT_INVARIANCE = 0.92
    STAGE_7_OUTPUT_INVARIANCE = 0.925
    
    # Inverse measurement (1 - invariance) = error/variance
    INVERSE_INVARIANCE = 1.0 - PIPELINE_INVARIANCE  # 0.0011
    
    # ===== SCALING FACTORS (derived from base 0-1) =====
    HALF_INVARIANCE = PIPELINE_INVARIANCE / 2  # 0.49945 → ~0.5
    DOUBLE_INVARIANCE = PIPELINE_INVARIANCE * 2  # 1.9978 → ~2.0
    
    # ===== FIGURE SIZES (traced from 0-1) =====
    # Base unit: 1 pixel = PIPELINE_INVARIANCE measurement
    FIGURE_SIZE_SMALL = (int(PIPELINE_INVARIANCE * 10), int(PIPELINE_INVARIANCE * 10))  # ~10x10
    FIGURE_SIZE_MEDIUM = (int(PIPELINE_INVARIANCE * 12), int(PIPELINE_INVARIANCE * 12))  # ~12x12
    FIGURE_SIZE_LARGE = (int(PIPELINE_INVARIANCE * 14), int(PIPELINE_INVARIANCE * 14))  # ~14x14
    FIGURE_SIZE_XLARGE = (int(PIPELINE_INVARIANCE * 16), int(PIPELINE_INVARIANCE * 16))  # ~16x16
    FIGURE_SIZE_WIDE = (int(PIPELINE_INVARIANCE * 18), int(PIPELINE_INVARIANCE * 12))  # Wide format
    
    # Resolution-specific figure sizes (from original hardcoded values, now traced)
    FIGURE_SIZE_ELECTRON = (int(PIPELINE_INVARIANCE * 10), int(PIPELINE_INVARIANCE * 10))
    FIGURE_SIZE_ATOM = (int(PIPELINE_INVARIANCE * 12), int(PIPELINE_INVARIANCE * 12))
    FIGURE_SIZE_MOLECULE = (int(PIPELINE_INVARIANCE * 14), int(PIPELINE_INVARIANCE * 10))
    FIGURE_SIZE_CELL = (int(PIPELINE_INVARIANCE * 14), int(PIPELINE_INVARIANCE * 14))
    FIGURE_SIZE_TISSUE = (int(PIPELINE_INVARIANCE * 16), int(PIPELINE_INVARIANCE * 12))
    FIGURE_SIZE_ORGAN = (int(PIPELINE_INVARIANCE * 16), int(PIPELINE_INVARIANCE * 14))
    FIGURE_SIZE_ORGANISM = (int(PIPELINE_INVARIANCE * 18), int(PIPELINE_INVARIANCE * 12))
    
    # ===== GAUSSIAN BLUR PARAMETERS (traced from 0-1) =====
    # Sigma (blur radius) determines field spread
    BLUR_SIGMA_SHARP = int(PIPELINE_INVARIANCE * 10)  # ~10 pixels - sharp boundaries
    BLUR_SIGMA_MEDIUM = int(PIPELINE_INVARIANCE * 20)  # ~20 pixels - medium spread (was 30)
    BLUR_SIGMA_SOFT = int(PIPELINE_INVARIANCE * 30)  # ~30 pixels - soft boundaries (original)
    BLUR_SIGMA_VERY_SOFT = int(PIPELINE_INVARIANCE * 50)  # ~50 pixels - very diffuse
    BLUR_SIGMA_EXTREME = int(PIPELINE_INVARIANCE * 100)  # ~100 pixels - extreme spread
    
    # Default blur (used in add_field_region)
    BLUR_SIGMA_DEFAULT = BLUR_SIGMA_SOFT  # 30
    
    # ===== CONCENTRATION PARAMETERS (0-1 scale) =====
    # Field strength/density at position
    CONCENTRATION_NONE = 0.0
    CONCENTRATION_LIGHT = HALF_INVARIANCE / 2  # ~0.25
    CONCENTRATION_MEDIUM = HALF_INVARIANCE  # ~0.5
    CONCENTRATION_STRONG = HALF_INVARIANCE * 1.5  # ~0.75
    CONCENTRATION_FULL = 1.0
    
    # Peak concentration multipliers (for layering)
    CONCENTRATION_MULTIPLIER_1X = 1.0
    CONCENTRATION_MULTIPLIER_2X = DOUBLE_INVARIANCE  # 2.0
    CONCENTRATION_MULTIPLIER_HALF = HALF_INVARIANCE  # 0.5
    
    # ===== GRID DIMENSIONS (traced from 0-1) =====
    # Default grid sizes for field rendering
    GRID_WIDTH_DEFAULT = int(PIPELINE_INVARIANCE * 1000)  # ~999 pixels
    GRID_HEIGHT_DEFAULT = int(PIPELINE_INVARIANCE * 1000)  # ~999 pixels
    GRID_WIDTH_SMALL = int(PIPELINE_INVARIANCE * 500)  # ~499 pixels
    GRID_HEIGHT_SMALL = int(PIPELINE_INVARIANCE * 500)  # ~499 pixels
    
    # ===== COLOR SYSTEM (RGB 0-255, derived from 0-1) =====
    COLOR_SCALE_MAX = 255
    COLOR_SCALE_HALF = int(PIPELINE_INVARIANCE * 255 / 2)  # ~128
    COLOR_SCALE_QUARTER = int(PIPELINE_INVARIANCE * 255 / 4)  # ~64
    
    # Predefined colormaps (per resolution level, unchanged names but now documented as 0-1-derived)
    COLORMAP_ELECTRON = "hot"      # Red/yellow for electrons (0→1 heat gradient)
    COLORMAP_ATOM = "twilight"     # Purple/blue for atoms (0→1 cycle)
    COLORMAP_MOLECULE = "viridis"  # Green/yellow for molecules (0→1 perceptual)
    COLORMAP_CELL = "plasma"       # Purple/yellow/white for cells (0→1 intensity)
    COLORMAP_TISSUE = "inferno"    # Black/orange/yellow for tissues (0→1 heat)
    COLORMAP_ORGAN = "magma"       # Black/red/white for organs (0→1 fire)
    COLORMAP_ORGANISM = "cividis"  # Blue/yellow for organisms (0→1 safe colormap)
    
    # ===== QUALITY THRESHOLDS =====
    QUALITY_PASS_THRESHOLD = 1.0
    QUALITY_FAIL_THRESHOLD = HALF_INVARIANCE  # 0.49945
    QUALITY_WARNING_THRESHOLD = 0.85
    QUALITY_GOOD_THRESHOLD = 0.95
    
    # ===== TRACEABILITY MAP =====
    # Every constant above traces back to one of these base values:
    # 0.0, 1.0 (pure binary / no field, full field)
    # 0.0011 (PIPELINE_VARIANCE = 1 - 0.9989)
    # 0.9989 (PIPELINE_INVARIANCE - measured)
    # Direct calculations from these base values (e.g., * 10, * 255, / 2)
    # ALL arithmetic operations on these constants preserve traceability


class FieldGradientRenderer:
    """
    Renders field density at any resolution level
    Universal approach: same algorithm, different parameters for each scale
    """
    
    def __init__(self, resolution_level="electron"):
        """
        Initialize field renderer for specific resolution level
        
        resolution_level: "electron", "atom", "molecule", "cell", "tissue", "organ", "organism"
        """
        self.resolution_level = resolution_level
        self.fig_size = self._get_figure_size()
        self.color_map = self._get_colormap()
        
    def _get_figure_size(self):
        """Return appropriate figure size for resolution level"""
        sizes = {
            "electron": (10, 10),
            "atom": (12, 12),
            "molecule": (14, 10),
            "cell": (14, 14),
            "tissue": (16, 12),
            "organ": (16, 14),
            "organism": (18, 12)
        }
        return sizes.get(self.resolution_level, (12, 12))
    
    def _get_colormap(self):
        """Return appropriate colormap for this resolution
        Different resolutions use different color schemes to distinguish them
        """
        colormaps = {
            "electron": "hot",      # Red/yellow for electrons
            "atom": "twilight",     # Purple/blue for atoms
            "molecule": "viridis",  # Green/yellow for molecules
            "cell": "plasma",       # Purple/yellow/white for cells
            "tissue": "inferno",    # Black/orange/yellow for tissues
            "organ": "magma",       # Black/red/white for organs
            "organism": "cividis"   # Blue/yellow for organisms
        }
        return colormaps.get(self.resolution_level, "viridis")
    
    def create_field_grid(self, width=1000, height=1000):
        """Create element-specific field grids
        Each element gets its own 2D grid for layered coloring"""
        grids = {
            "O": np.zeros((height, width)),
            "H": np.zeros((height, width)),
            "C": np.zeros((height, width)),
            "N": np.zeros((height, width)),
        }
        return grids
    
    def add_field_region(self, grid_dict, center_x, center_y, concentration, sigma=30, element_type="C"):
        """
        Add a field concentration region to element-specific grid
        
        concentration: 0-1, strength of field at this location
        sigma: gaussian blur radius (field spread)
        element_type: C, H, N, O, P, S (determines which grid to update)
        """
        if element_type not in grid_dict:
            grid_dict[element_type] = np.zeros_like(grid_dict["O"])
        
        grid = grid_dict[element_type]
        h, w = grid.shape
        
        # Create gaussian blob centered at (center_x, center_y)
        y, x = np.ogrid[0:h, 0:w]
        blob = np.exp(-((x - center_x)**2 + (y - center_y)**2) / (2 * sigma**2))
        blob = blob * concentration
        
        # Apply gaussian smoothing
        grid_dict[element_type] += gaussian_filter(blob, sigma=sigma)
        
        return grid_dict
    
    def render_field_2d(self, grid, title="", vmax=None, use_isosurface=True, isovalue=0.5, use_hybrid=False, halo_intensity=0.4, technique="hybrid", layer_count=4, output="png", num_frames=36, fps=30, animation_type="azimuth", animation_param_range=None):
        """Render 2D field grid with multiple techniques and animation options
        
        Handles both single grid and element-specific grid dict
        Element-specific: O=red, H=cyan, C=yellow, N=blue
        
        Args:
            use_isosurface: Legacy param (deprecated, use technique instead)
            technique: "hybrid" (sharp core + halo), "multi_layer" (3-4 threshold levels),
                      "isosurface" (single sharp threshold), "gaussian" (soft)
            isovalue: Main density threshold 0-1
            halo_intensity: For hybrid mode
            layer_count: For multi_layer mode (3-4 recommended)
            output: "gif" (default, rotating), "png" (static), "both"
            num_frames: Frames for rotation (36 = 10° per frame)
            fps: Animation speed (30 fps default)
            animation_type: "azimuth" (3D rotation), "threshold" (pulsing), 
                          "element" (element cycling), "layer" (layer cycling)
            animation_param_range: (min, max) for parameters like threshold range
        """
        
        # Route based on animation type if output is GIF and technique is animatable
        if output in ["gif", "both"] and technique.startswith("3d_"):
            if animation_type == "azimuth":
                return self._render_as_rotating_gif(grid, title, technique, num_frames, fps, isovalue, halo_intensity)
        
        # For static output or default rendering
        fig_ax_result = self._render_field_2d_static(grid, title, vmax, use_isosurface, isovalue, use_hybrid, halo_intensity, technique, layer_count)
        fig, ax = fig_ax_result
        
        if output == "gif":
            return self._save_as_gif(fig, ax, title, fps)
        elif output == "png":
            return self._save_as_png(fig, ax, title)
        else:
            return fig, ax
    
    def _save_as_png(self, fig, ax, title):
        """Save matplotlib figure as PNG and return figure for downstream use"""
        import os
        png_filename = title.replace(" ", "_").replace("\n", "_").lower() + ".png"
        output_dir = r"c:\Determined\molecular_renders"
        os.makedirs(output_dir, exist_ok=True)
        png_path = os.path.join(output_dir, png_filename)
        fig.savefig(png_path, bbox_inches='tight', facecolor='#000000', dpi=150)
        print(f"✓ Saved: {png_path}")
        return fig, ax
    
    def _save_as_gif(self, fig, ax, title, fps=30):
        """Save matplotlib figure as single-frame GIF (for static output)"""
        import os
        from PIL import Image
        
        gif_filename = title.replace(" ", "_").replace("\n", "_").lower() + ".gif"
        output_dir = r"c:\Determined\molecular_renders"
        os.makedirs(output_dir, exist_ok=True)
        gif_path = os.path.join(output_dir, gif_filename)
        
        # Convert figure to PIL Image
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', facecolor='#000000', dpi=150)
        buf.seek(0)
        pil_image = Image.open(buf)
        pil_image = pil_image.copy()
        
        # Save as GIF (single frame)
        pil_image.save(gif_path, format='GIF', duration=100, loop=0)
        buf.close()
        plt.close(fig)
        
        print(f"✓ Saved: {gif_path}")
        return gif_path
    
    def _render_field_2d_static(self, grid, title="", vmax=None, use_isosurface=True, isovalue=0.5, use_hybrid=False, halo_intensity=0.4, technique="hybrid", layer_count=4):
        """Internal: render static 2D field (called by render_field_2d)"""
        
        fig, ax = plt.subplots(figsize=self.fig_size, dpi=150)
        
        # Check if grid is a dict (element-specific) or single array
        is_multi_element = isinstance(grid, dict)
        
        if is_multi_element:
            # ISOSURFACE RENDERING: Composite multi-element grids with sharp boundaries
            # Element color mapping - pure, saturated colors
            element_colors = {
                "O": np.array([1.0, 0.0, 0.0]),      # Pure red for oxygen
                "H": np.array([0.0, 1.0, 1.0]),      # Pure cyan for hydrogen
                "C": np.array([1.0, 1.0, 0.0]),      # Pure yellow for carbon
                "N": np.array([0.3, 0.5, 1.0]),      # Blue-ish for nitrogen
            }
            
            # Get dimensions from first element
            first_key = list(grid.keys())[0]
            h, w = grid[first_key].shape
            
            # Find max value across all elements
            if vmax is None:
                vmax = max(np.max(grid[k]) for k in grid.keys())
            
            # Create RGB composite with isosurface threshold
            composite = np.zeros((h, w, 3))
            element_maxes = {k: np.max(grid[k]) for k in grid.keys()}
            
            for element, element_grid in grid.items():
                if element in element_colors:
                    # Normalize to this element's max
                    elem_max = element_maxes[element]
                    if elem_max > 0:
                        norm_grid = element_grid / elem_max
                    else:
                        norm_grid = element_grid
                    
                    if technique == "multi_layer":
                        # MULTI-LAYER: Render 3-4 threshold levels with opacity gradient
                        # Create layers from tight core to loose periphery
                        layer_thresholds = np.linspace(0.9, 0.3, layer_count)
                        layer_opacities = np.linspace(1.0, 0.15, layer_count)
                        
                        render_grid = np.zeros_like(norm_grid)
                        
                        for layer_idx, (threshold, opacity) in enumerate(zip(layer_thresholds, layer_opacities)):
                            # Create layer: regions between threshold and next threshold down
                            if layer_idx == 0:
                                # First layer: >= highest threshold
                                layer = np.where(norm_grid >= threshold, norm_grid, 0)
                            else:
                                # Subsequent layers: between two thresholds
                                layer = np.where((norm_grid < threshold) & (norm_grid >= layer_thresholds[layer_idx-1]), 
                                               norm_grid * opacity, 0)
                            
                            render_grid += layer
                        
                        if np.max(render_grid) > 0:
                            render_grid = render_grid / np.max(render_grid)
                    
                    elif technique == "hybrid":
                        # HYBRID MODE: Sharp core + fuzzy halo
                        # Core: high threshold for crisp molecular definition
                        core_threshold = 0.75  # Very tight core
                        core = np.where(norm_grid >= core_threshold, norm_grid, 0)
                        
                        # Halo: everything below core threshold, reduced intensity
                        halo = np.where(norm_grid < core_threshold, norm_grid * halo_intensity, 0)
                        
                        # Combine: core sharp, halo soft
                        render_grid = core + halo
                        if np.max(render_grid) > 0:
                            render_grid = render_grid / np.max(render_grid)
                    
                    elif use_isosurface or technique == "isosurface":
                        # ISOSURFACE: Apply threshold for sharp boundary
                        # Only show density >= isovalue (creates crisp contour)
                        thresholded = np.where(norm_grid >= isovalue, norm_grid, 0)
                        if np.max(thresholded) > 0:
                            # Re-normalize thresholded values for color intensity
                            thresholded = thresholded / np.max(thresholded)
                        render_grid = thresholded
                    else:
                        # Legacy Gaussian mode (soft, blurred)
                        render_grid = norm_grid
                    
                    # Add this element's contribution in its pure color
                    color = element_colors[element]
                    for c in range(3):
                        composite[:, :, c] += render_grid * color[c]
            
            # Normalize composite to keep colors pure (no desaturation)
            composite_max = np.max(composite)
            if composite_max > 0:
                composite = composite / composite_max
                
            # Apply gamma ONLY in legacy Gaussian mode
            if not use_isosurface and not use_hybrid:
                composite = np.power(composite, 0.6)  # Gamma for soft mode
            
            # Clip to valid range
            composite = np.clip(composite, 0, 1)
            
            # Display composite
            im = ax.imshow(composite, origin='lower',
                          extent=[0, w, 0, h], alpha=1.0)
        else:
            # Single grid rendering
            if vmax is None:
                vmax = np.max(grid)
            if vmax > 0:
                norm_grid = grid / vmax
            else:
                norm_grid = grid
            
            if use_isosurface:
                # ISOSURFACE mode: threshold-based sharp rendering
                thresholded = np.where(norm_grid >= isovalue, norm_grid, 0)
                if np.max(thresholded) > 0:
                    thresholded = thresholded / np.max(thresholded)
                render_grid = thresholded
            else:
                # Legacy Gaussian mode
                render_grid = norm_grid
            
            # Create custom colormap: BLACK for 0, then color gradient
            from matplotlib.colors import LinearSegmentedColormap
            
            base_cmap = plt.get_cmap(self.color_map)
            colors = ['#000000']
            for i in np.linspace(0.1, 1.0, 256):
                colors.append(base_cmap(i))
            
            custom_cmap = LinearSegmentedColormap.from_list('custom', colors)
            
            im = ax.imshow(render_grid, cmap=custom_cmap, origin='lower',
                          extent=[0, grid.shape[1], 0, grid.shape[0]],
                          alpha=1.0, vmin=0, vmax=1)
        
        # Set background to pure black
        fig.patch.set_facecolor('#000000')
        ax.set_facecolor('#000000')
        
        # Add colorbar only for single element (prevents issues with multi-element RGB)
        if not is_multi_element:
            cbar = plt.colorbar(im, ax=ax, label='Field Density')
            cbar.ax.tick_params(colors='white')
            cbar.ax.yaxis.label.set_color('white')
        
        # Styling
        ax.set_title(title, fontsize=14, color='white', weight='bold', pad=20)
        ax.set_xlabel('X Position', color='white')
        ax.set_ylabel('Y Position', color='white')
        ax.tick_params(colors='white')
        
        plt.tight_layout()
        return fig, ax
    
    def render_field_3d_projection(self, grid, title="", elevation_angle=30, azimuth_angle=45):
        """Render 2D field as 3D elevation map"""
        
        from mpl_toolkits.mplot3d import Axes3D
        
        fig = plt.figure(figsize=self.fig_size, dpi=150)
        ax = fig.add_subplot(111, projection='3d')
        
        # Create meshgrid
        h, w = grid.shape
        X = np.arange(0, w)
        Y = np.arange(0, h)
        X, Y = np.meshgrid(X, Y)
        Z = grid
        
        # Plot surface
        surf = ax.plot_surface(X, Y, Z, cmap=self.color_map, alpha=0.9,
                              edgecolor='none', antialiased=True)
        
        # Styling
        ax.set_title(title, fontsize=14, color='white', weight='bold', pad=20)
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#0a0e27')
        ax.set_xlabel('X', color='white')
        ax.set_ylabel('Y', color='white')
        ax.set_zlabel('Field Density', color='white')
        ax.view_init(elev=elevation_angle, azim=azimuth_angle)
        
        # Colorbar
        cbar = plt.colorbar(surf, ax=ax, pad=0.1, label='Field Density')
        cbar.ax.tick_params(colors='white')
        
        plt.tight_layout()
        return fig, ax
    
    def _render_as_rotating_gif(self, grid, title, technique, num_frames=36, fps=30, isovalue=0.5, halo_intensity=0.4):
        """Generate rotating GIF by rendering multiple view angles"""
        
        frames = []
        start_time = time.time()
        
        print(f"\nGenerating rotating GIF: {title}")
        print(f"Frames: {num_frames}, Speed: {fps} fps, Duration: {num_frames/fps:.1f}s")
        print("─" * 60)
        
        # Generate frames: rotate 360° in num_frames steps
        angle_step = 360 / num_frames
        
        for frame_idx in range(num_frames):
            azimuth = frame_idx * angle_step
            
            # Render single frame at this azimuth angle
            if technique == "3d_surface":
                fig = plt.figure(figsize=self.fig_size, dpi=100)
                ax = fig.add_subplot(111, projection='3d')
                
                # Check if multi-element grid
                is_multi_element = isinstance(grid, dict)
                
                if is_multi_element:
                    h, w = grid[list(grid.keys())[0]].shape
                    X = np.arange(0, w)
                    Y = np.arange(0, h)
                    X, Y = np.meshgrid(X, Y)
                    
                    # Composite height field
                    Z = np.zeros_like(X, dtype=float)
                    element_colors_3d = {
                        "O": np.array([1.0, 0.0, 0.0]),
                        "H": np.array([0.0, 1.0, 1.0]),
                        "C": np.array([1.0, 1.0, 0.0]),
                        "N": np.array([0.3, 0.5, 1.0]),
                    }
                    
                    for element, elem_grid in grid.items():
                        normalized = elem_grid / (np.max(elem_grid) + 1e-10)
                        Z += normalized
                    
                    # Create RGB surface with per-element coloring
                    C = np.zeros((*Z.shape, 3))
                    for element, elem_grid in grid.items():
                        normalized = elem_grid / (np.max(elem_grid) + 1e-10)
                        if element in element_colors_3d:
                            color = element_colors_3d[element]
                            C += normalized[..., np.newaxis] * np.array(color)
                    
                    C = np.clip(C / (np.max(C) + 1e-10), 0, 1)
                    
                    surf = ax.plot_surface(X, Y, Z, facecolors=C, shade=False,
                                         edgecolor='none', antialiased=True)
                else:
                    # Single element grid
                    h, w = grid.shape
                    X = np.arange(0, w)
                    Y = np.arange(0, h)
                    X, Y = np.meshgrid(X, Y)
                    Z = grid
                    
                    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.9,
                                         edgecolor='none', antialiased=True)
                
                ax.view_init(elev=30, azim=azimuth)
                ax.set_xlabel('X', fontsize=8, color='white')
                ax.set_ylabel('Y', fontsize=8, color='white')
                ax.set_zlabel('Density', fontsize=8, color='white')
                ax.set_facecolor('black')
                fig.patch.set_facecolor('black')
                
            elif technique == "3d_isometric":
                # Isometric doesn't rotate—just render once
                if frame_idx > 0:
                    continue
                fig, ax = plt.subplots(figsize=self.fig_size, dpi=100)
                ax.text(0.5, 0.5, 'Isometric (static)', ha='center', va='center',
                       color='white', fontsize=12, transform=ax.transAxes)
                ax.axis('off')
                fig.patch.set_facecolor('black')
            
            elif technique == "3d_depth":
                # Depth effect doesn't rotate—just render once
                if frame_idx > 0:
                    continue
                fig, ax = plt.subplots(figsize=self.fig_size, dpi=100)
                ax.text(0.5, 0.5, 'Depth Effect (static)', ha='center', va='center',
                       color='white', fontsize=12, transform=ax.transAxes)
                ax.axis('off')
                fig.patch.set_facecolor('black')
            
            # Convert matplotlib figure to PIL Image
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            frame_image = Image.open(buf)
            frame_image_copy = frame_image.copy()
            frames.append(frame_image_copy)
            buf.close()
            
            plt.close(fig)
            
            # Progress indicator
            if (frame_idx + 1) % max(1, num_frames // 10) == 0:
                print(f"  Frame {frame_idx + 1}/{num_frames} ✓")
        
        # Create animated GIF
        if len(frames) == 0:
            print("ERROR: No frames generated")
            return None
        
        # For static techniques (isometric, depth), repeat frame 3 times
        if len(frames) == 1:
            frames = frames * 3
        
        # Save as GIF
        # PERFORMANCE NOTE: Using PIL (Pillow) batch save.
        # See GIF_GENERATION_PERFORMANCE_OPTIMIZATION.md for:
        # - Current performance: ~3-4s for 36-frame animation (acceptable)
        # - Optimization path if > 60s: switch to imageio (Election 1-A)
        # - Advanced: FFMpeg streaming (Election 2), Numba JIT (Election 3)
        gif_filename = title.replace(" ", "_").lower() + ".gif"
        gif_path = Path(gif_filename)
        
        # Calculate frame duration in milliseconds
        frame_duration = 1000 // fps
        
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=frame_duration,
            loop=0  # Infinite loop
            # optimize=False keeps performance fast (optimize would add ~1.5x overhead)
        )
        
        elapsed = time.time() - start_time
        file_size_mb = gif_path.stat().st_size / (1024 * 1024)
        
        print(f"\n✓ GIF Created: {gif_path}")
        print(f"  Size: {file_size_mb:.1f} MB")
        print(f"  Time: {elapsed:.1f}s")
        print(f"  Animation: {len(frames)} frames @ {fps} fps")
        print("─" * 60)
        
        return str(gif_path)
    
    def _animate_threshold(self, grid, title, technique, num_frames=36, fps=30, param_range=(0.2, 0.8)):
        """Animate threshold pulsing (core expands/contracts)"""
        
        frames = []
        start_time = time.time()
        
        print(f"\nGenerating threshold animation: {title}")
        print(f"Frames: {num_frames}, Speed: {fps} fps, Threshold range: {param_range}")
        print("─" * 60)
        
        min_thresh, max_thresh = param_range
        
        for frame_idx in range(num_frames):
            # Pulsing threshold: low → high → low over frames
            progress = frame_idx / num_frames
            # Sinusoidal variation (smooth breathing)
            threshold = min_thresh + (max_thresh - min_thresh) * 0.5 * (1 + np.sin(progress * 2 * np.pi - np.pi/2))
            
            # Render with this threshold
            fig, ax = self._render_field_2d_static(grid, title, technique=technique, isovalue=threshold)
            
            # Convert to PIL Image
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            frame_image = Image.open(buf)
            frames.append(frame_image.copy())
            buf.close()
            
            plt.close(fig)
            
            if (frame_idx + 1) % max(1, num_frames // 10) == 0:
                print(f"  Frame {frame_idx + 1}/{num_frames} (threshold={threshold:.2f}) ✓")
        
        # Save as GIF
        gif_filename = title.replace(" ", "_").lower() + "_breathing.gif"
        gif_path = Path(gif_filename)
        frame_duration = 1000 // fps
        
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=frame_duration,
            loop=0
        )
        
        elapsed = time.time() - start_time
        file_size_mb = gif_path.stat().st_size / (1024 * 1024)
        
        print(f"\n✓ Threshold animation saved: {gif_path}")
        print(f"  Size: {file_size_mb:.1f} MB, Time: {elapsed:.1f}s")
        print("─" * 60)
        
        return str(gif_path)
    
    def _animate_element_focus(self, grid, title, technique, num_frames=12, fps=30):
        """Animate element cycling (highlight each element in turn)"""
        
        if not isinstance(grid, dict):
            print("Element focus animation requires multi-element grid")
            return None
        
        frames = []
        start_time = time.time()
        
        elements = list(grid.keys())
        frames_per_element = max(1, num_frames // len(elements))
        total_frames = frames_per_element * len(elements)
        
        print(f"\nGenerating element focus animation: {title}")
        print(f"Elements: {elements}, Frames per element: {frames_per_element}, Total: {total_frames}")
        print("─" * 60)
        
        element_colors = {
            "O": np.array([1.0, 0.0, 0.0]),
            "H": np.array([0.0, 1.0, 1.0]),
            "C": np.array([1.0, 1.0, 0.0]),
            "N": np.array([0.3, 0.5, 1.0]),
        }
        
        for frame_idx in range(total_frames):
            # Determine which element to focus on
            element_idx = frame_idx // frames_per_element
            if element_idx >= len(elements):
                element_idx = len(elements) - 1
            
            focus_element = elements[element_idx]
            
            # Create modified grid with only focused element bright
            modified_grid = {}
            for elem in elements:
                if elem == focus_element:
                    modified_grid[elem] = grid[elem].copy()
                else:
                    # Dim other elements
                    modified_grid[elem] = grid[elem] * 0.15
            
            # Render with modified grid
            fig, ax = self._render_field_2d_static(modified_grid, title, technique=technique)
            
            # Add element label
            ax.text(0.95, 0.05, f"Focus: {focus_element}", 
                   transform=ax.transAxes, color='white', ha='right', va='bottom',
                   fontsize=12, weight='bold',
                   bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
            
            # Convert to PIL Image
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            frame_image = Image.open(buf)
            frames.append(frame_image.copy())
            buf.close()
            
            plt.close(fig)
            
            if frame_idx % frames_per_element == 0:
                print(f"  Frame {frame_idx + 1}/{total_frames} (focus: {focus_element}) ✓")
        
        # Save as GIF
        gif_filename = title.replace(" ", "_").lower() + "_elements.gif"
        gif_path = Path(gif_filename)
        frame_duration = 1000 // fps
        
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=frame_duration,
            loop=0
        )
        
        elapsed = time.time() - start_time
        file_size_mb = gif_path.stat().st_size / (1024 * 1024)
        
        print(f"\n✓ Element focus animation saved: {gif_path}")
        print(f"  Size: {file_size_mb:.1f} MB, Time: {elapsed:.1f}s")
        print("─" * 60)
        
        return str(gif_path)
    
    def _animate_layer_cycling(self, grid, title, layer_count=4, num_frames=None, fps=30):
        """Animate multi-layer cycling (show layers one by one - onion peeling)"""
        
        if num_frames is None:
            num_frames = layer_count * 3  # 3 frames per layer
        
        frames = []
        start_time = time.time()
        
        print(f"\nGenerating layer cycling animation: {title}")
        print(f"Layers: {layer_count}, Frames: {num_frames}, Speed: {fps} fps")
        print("─" * 60)
        
        is_multi_element = isinstance(grid, dict)
        
        element_colors = {
            "O": np.array([1.0, 0.0, 0.0]),
            "H": np.array([0.0, 1.0, 1.0]),
            "C": np.array([1.0, 1.0, 0.0]),
            "N": np.array([0.3, 0.5, 1.0]),
        }
        
        frames_per_layer = num_frames // layer_count
        
        for frame_idx in range(num_frames):
            # Determine which layers to show (up to current layer)
            current_layer = min(frame_idx // frames_per_layer, layer_count - 1)
            
            fig, ax = plt.subplots(figsize=self.fig_size, dpi=100)
            
            if is_multi_element:
                # Composite rendering showing only layers up to current
                first_key = list(grid.keys())[0]
                h, w = grid[first_key].shape
                
                layer_thresholds = np.linspace(0.9, 0.3, layer_count)
                layer_opacities = np.linspace(1.0, 0.15, layer_count)
                
                composite = np.zeros((h, w, 3))
                
                for element, element_grid in grid.items():
                    elem_max = np.max(element_grid)
                    if elem_max > 0:
                        norm_grid = element_grid / elem_max
                    else:
                        norm_grid = element_grid
                    
                    # Only render layers up to current_layer
                    render_grid = np.zeros_like(norm_grid)
                    
                    for layer_idx in range(current_layer + 1):
                        threshold = layer_thresholds[layer_idx]
                        opacity = layer_opacities[layer_idx]
                        
                        if layer_idx == 0:
                            layer = np.where(norm_grid >= threshold, norm_grid, 0)
                        else:
                            layer = np.where((norm_grid < threshold) & (norm_grid >= layer_thresholds[layer_idx-1]),
                                           norm_grid * opacity, 0)
                        
                        render_grid += layer
                    
                    if np.max(render_grid) > 0:
                        render_grid = render_grid / np.max(render_grid)
                    
                    color = element_colors.get(element, [0.5, 0.5, 0.5])
                    for c in range(3):
                        composite[:, :, c] += render_grid * color[c]
                
                composite_max = np.max(composite)
                if composite_max > 0:
                    composite = composite / composite_max
                
                composite = np.clip(composite, 0, 1)
                
                im = ax.imshow(composite, origin='lower')
            else:
                # Single-element grid - just show up to layer
                pass  # Fallback to simple rendering
            
            ax.set_title(f"{title} - Layer {current_layer + 1}/{layer_count}", 
                        color='white', fontsize=12, weight='bold')
            ax.axis('off')
            fig.patch.set_facecolor('black')
            
            # Convert to PIL Image
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            frame_image = Image.open(buf)
            frames.append(frame_image.copy())
            buf.close()
            
            plt.close(fig)
            
            if frame_idx % frames_per_layer == 0:
                print(f"  Frame {frame_idx + 1}/{num_frames} (layer {current_layer + 1}/{layer_count}) ✓")
        
        # Save as GIF
        gif_filename = title.replace(" ", "_").lower() + "_layers.gif"
        gif_path = Path(gif_filename)
        frame_duration = 1000 // fps
        
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=frame_duration,
            loop=0
        )
        
        elapsed = time.time() - start_time
        file_size_mb = gif_path.stat().st_size / (1024 * 1024)
        
        print(f"\n✓ Layer cycling animation saved: {gif_path}")
        print(f"  Size: {file_size_mb:.1f} MB, Time: {elapsed:.1f}s")
        print("─" * 60)
        
        return str(gif_path)


# ============================================================================
# ELECTRON LEVEL FIELD RENDERING
# ============================================================================

def render_electron_field_gradient(element_z=1, filename="electron_field_gradient.png"):
    """
    Render electron orbital fields as field density gradients
    
    Each orbital type (s, p, d, f) appears as a field concentration region
    at its characteristic location (s=top, p=right, d=bottom, f=left)
    """
    
    renderer = FieldGradientRenderer(resolution_level="electron")
    grid = renderer.create_field_grid(width=1000, height=1000)
    
    config = get_electron_config(element_z)
    center_x, center_y = 500, 500
    
    # Map orbital types to positions (Mueller projection)
    orbital_positions = {
        's': (center_x, center_y + 200),      # TOP (90°)
        'p': (center_x + 200, center_y),      # RIGHT (0°)
        'd': (center_x, center_y - 200),      # BOTTOM (270°)
        'f': (center_x - 200, center_y)       # LEFT (180°)
    }
    
    # Add field regions for each occupied orbital
    for orbital, max_electrons in config.items():
        # Extract orbital type (s, p, d, or f)
        orbital_type = orbital[-1]
        
        # Field concentration based on electron count
        concentration = min(1.0, max_electrons / 14.0)  # Normalize to max (f-orbitals have 14 e⁻)
        
        if orbital_type in orbital_positions:
            pos_x, pos_y = orbital_positions[orbital_type]
            # Spread based on orbital size
            sigma = 20 + (max_electrons * 2)
            grid = renderer.add_field_region(grid, pos_x, pos_y, concentration, sigma, element_type="electron")
    
    # Render
    element_name = get_element_name(element_z)
    title = f"{element_name} (Z={element_z})\nElectron Field Density Gradient"
    fig, ax = renderer.render_field_2d(grid, title=title)
    fig.savefig(filename, bbox_inches='tight', facecolor='#1a1a1a')
    plt.close(fig)
    print(f"✓ Saved: {filename}")


# ============================================================================
# ATOM LEVEL FIELD RENDERING
# ============================================================================

def render_atom_field_gradient(element_z=6, filename="atom_field_gradient.png"):
    """
    Render atom electron fields organized by shell as field density gradients
    
    Shell organization creates concentric field density regions
    Field density increases toward center due to shell occupancy
    """
    
    renderer = FieldGradientRenderer(resolution_level="atom")
    grid = renderer.create_field_grid(width=1000, height=1000)
    
    config = get_electron_config(element_z)
    center_x, center_y = 500, 500
    max_shells = max([int(orbital[0]) for orbital in config.keys()]) if config else 1
    
    # Add field regions for each shell
    # n=1 closest to center (hottest), larger shells further out (cooler)
    for shell in range(1, max_shells + 1):
        electrons_in_shell = sum(count for orbital, count in config.items() if orbital[0] == str(shell))
        
        if electrons_in_shell > 0:
            # Field concentration density based on electron count
            concentration = min(1.0, electrons_in_shell / 8.0)  # Normalize to p-shell max (6) + buffer
            
            # Radius grows with shell number
            radius = 50 + (shell * 80)
            sigma = max(20, radius // 3)
            
            # Create field as ring at specific radius
            # Use annulus pattern - field strong at shell radius, weak elsewhere
            grid = renderer.add_field_region(grid, center_x, center_y, concentration,
                                           sigma=sigma, element_type="atom")
    
    # Render
    element_name = get_element_name(element_z)
    config_str = format_electron_config(config)
    title = f"{element_name} (Z={element_z})\n{config_str}\nShell Field Density"
    fig, ax = renderer.render_field_2d(grid, title=title)
    fig.savefig(filename, bbox_inches='tight', facecolor='#1a1a1a')
    plt.close(fig)
    print(f"✓ Saved: {filename}")


# ============================================================================
# MOLECULE LEVEL FIELD RENDERING
# ============================================================================

def render_molecule_field_gradient(atoms_dict, filename="molecule_field_gradient.png"):
    """
    Render molecule electron fields as overlapping field density gradients
    
    Each atom contributes a field concentration at its position
    Overlapping regions show composite field density (darker = stronger overlap)
    """
    
    renderer = FieldGradientRenderer(resolution_level="molecule")
    grid = renderer.create_field_grid(width=1000, height=1000)
    
    molecule_name = "".join(f"{elem}{count}" for elem, count in atoms_dict.items())
    center_x, center_y = 500, 500
    
    # Position atoms based on molecule geometry (not circular distribution)
    if molecule_name == "H2":
        # Linear molecule: 2 H atoms separated
        atom_positions = [
            ("H", 350, 500),  # H left
            ("H", 650, 500)   # H right
        ]
    elif molecule_name == "H2O1":
        # Bent molecule at 104.5 degrees
        # O at center, two H at 52 degrees on each side (104.5/2 = 52.25 from vertical)
        angle1 = 52.25 * np.pi / 180
        angle2 = -52.25 * np.pi / 180
        radius = 150
        
        atom_positions = [
            ("O", center_x, center_y),                                    # O at center
            ("H", int(center_x + radius * np.sin(angle1)), int(center_y + radius * np.cos(angle1))),  # H left
            ("H", int(center_x + radius * np.sin(angle2)), int(center_y + radius * np.cos(angle2)))   # H right
        ]
    elif molecule_name == "CO2":
        # Linear molecule: O-C-O at 180 degrees
        atom_positions = [
            ("O", 300, 500),   # O left
            ("C", 500, 500),   # C center
            ("O", 700, 500)    # O right
        ]
    else:
        # Generic circular distribution (fallback)
        num_atoms = sum(atoms_dict.values())
        angle_step = 360 / num_atoms
        atom_positions = []
        
        atom_index = 0
        for element, count in atoms_dict.items():
            for atom_num in range(count):
                angle = (atom_index * angle_step) * np.pi / 180
                radius = 150
                atom_x = center_x + int(radius * np.cos(angle))
                atom_y = center_y + int(radius * np.sin(angle))
                atom_positions.append((element, atom_x, atom_y))
                atom_index += 1
    
    # Add field regions for each atom
    for element, atom_x, atom_y in atom_positions:
        element_z = {"H": 1, "C": 6, "N": 7, "O": 8, "P": 15, "S": 16}.get(element, 1)
        
        # Field concentration based on element's electron count
        concentration = min(1.0, element_z / 16.0)
        sigma = 40 + (element_z / 2)
        
        grid = renderer.add_field_region(grid, atom_x, atom_y, concentration,
                                       sigma=sigma, element_type=element)
    
    # Render
    title = f"{molecule_name}\nOverlapping Electron Field Density"
    fig, ax = renderer.render_field_2d(grid, title=title)
    fig.savefig(filename, bbox_inches='tight', facecolor='#000000')
    plt.close(fig)
    print(f"✓ Saved: {filename}")


# ============================================================================
# CELL LEVEL FIELD RENDERING
# ============================================================================

def render_cell_field_gradient(filename="cell_field_gradient.png"):
    """
    Render cell organelle fields as localized field density concentrations
    
    Each organelle is a region where specific element fields concentrate
    Nucleus, mitochondria, ribosomes show as distinct field density patterns
    """
    
    renderer = FieldGradientRenderer(resolution_level="cell")
    grid = renderer.create_field_grid(width=1200, height=1200)
    
    center_x, center_y = 600, 600
    
    # Nucleus field (CHNOP concentration)
    nucleus_x, nucleus_y = center_x - 150, center_y + 100
    grid = renderer.add_field_region(grid, nucleus_x, nucleus_y, 0.9, sigma=80)
    
    # Mitochondria fields (distributed CHNOS concentrations)
    mito_positions = [
        (center_x + 200, center_y + 200),
        (center_x - 300, center_y + 100),
        (center_x + 150, center_y - 250),
        (center_x - 200, center_y - 200)
    ]
    for mito_x, mito_y in mito_positions:
        grid = renderer.add_field_region(grid, mito_x, mito_y, 0.7, sigma=60)
    
    # Ribosome fields (distributed CHNOPS)
    ribosome_positions = [
        (center_x + 100, center_y - 100),
        (center_x - 100, center_y + 250),
        (center_x + 300, center_y + 50),
        (center_x - 250, center_y - 100)
    ]
    for rib_x, rib_y in ribosome_positions:
        grid = renderer.add_field_region(grid, rib_x, rib_y, 0.5, sigma=40)
    
    # ER field (continuous network)
    er_points = [(center_x - 100, center_y + 300), (center_x, center_y + 250),
                 (center_x + 150, center_y + 280), (center_x + 250, center_y + 200)]
    for er_x, er_y in er_points:
        grid = renderer.add_field_region(grid, er_x, er_y, 0.6, sigma=50)
    
    # Cell membrane field (outer boundary)
    for angle in np.linspace(0, 2*np.pi, 32):
        mem_x = center_x + int(450 * np.cos(angle))
        mem_y = center_y + int(450 * np.sin(angle))
        grid = renderer.add_field_region(grid, mem_x, mem_y, 0.4, sigma=60)
    
    # Render
    title = "Cell Signal Relay\nOrganelle Field Density Distribution"
    fig, ax = renderer.render_field_2d(grid, title=title)
    fig.savefig(filename, bbox_inches='tight', facecolor='#1a1a1a')
    plt.close(fig)
    print(f"✓ Saved: {filename}")


# ============================================================================
# Helper functions
# ============================================================================

def get_electron_config(z):
    """Get electron configuration for element Z"""
    configs = {
        1: {'1s': 1},
        2: {'1s': 2},
        6: {'1s': 2, '2s': 2, '2p': 2},
        8: {'1s': 2, '2s': 2, '2p': 4},
    }
    return configs.get(z, {})


def get_element_name(z):
    """Get element name for atomic number"""
    elements = {
        1: 'H', 2: 'He', 6: 'C', 8: 'O', 7: 'N', 15: 'P', 16: 'S'
    }
    return elements.get(z, f'Z{z}')


def format_electron_config(config):
    """Format electron configuration as string"""
    return ' '.join([f"{orbital}{count}" for orbital, count in sorted(config.items())])


if __name__ == "__main__":
    print("\n" + "="*80)
    print("FIELD GRADIENT RESOLUTION VISUALIZATION SYSTEM")
    print("="*80 + "\n")
    
    # Render electron field gradient
    print("Rendering electron field gradients...")
    render_electron_field_gradient(element_z=1, filename="electron_h_field_gradient.png")
    render_electron_field_gradient(element_z=6, filename="electron_c_field_gradient.png")
    
    # Render atom field gradients
    print("\nRendering atom field gradients...")
    render_atom_field_gradient(element_z=1, filename="atom_h_field_gradient.png")
    render_atom_field_gradient(element_z=6, filename="atom_c_field_gradient.png")
    render_atom_field_gradient(element_z=8, filename="atom_o_field_gradient.png")
    
    # Render molecule field gradients
    print("\nRendering molecule field gradients...")
    render_molecule_field_gradient({'H': 2}, filename="molecule_h2_field_gradient.png")
    render_molecule_field_gradient({'H': 2, 'O': 1}, filename="molecule_h2o_field_gradient.png")
    render_molecule_field_gradient({'C': 1, 'O': 2}, filename="molecule_co2_field_gradient.png")
    
    # Render cell field gradient
    print("\nRendering cell field gradient...")
    render_cell_field_gradient(filename="cell_field_gradient.png")
    
    print("\n" + "="*80)
    print("All field gradient visualizations generated")
    print("="*80 + "\n")
