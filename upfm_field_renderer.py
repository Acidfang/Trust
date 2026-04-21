"""
UPFM Image Renderer
Converts converged field states to beautiful visualizations.

Rendering philosophy:
- Magnitude → Brightness/Value (how strong the field is)
- Phase → Hue (rotational orientation, 0-2π → Red-Violet)
- Frequency (local) → Saturation (information content)
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import colormaps


class FieldRenderer:
    """Render complex field to beautiful images."""
    
    def __init__(self, verbose=True):
        self.verbose = verbose
    
    @staticmethod
    def normalize(array, vmin=None, vmax=None):
        """Normalize array to [0, 1]."""
        if vmin is None:
            vmin = np.min(array)
        if vmax is None:
            vmax = np.max(array)
        
        if vmax == vmin:
            return np.zeros_like(array)
        
        return (array - vmin) / (vmax - vmin)
    
    def render_magnitude_phase(self, field, title="UPFM Field", 
                               output_path=None, dpi=150, enhance=True):
        """
        Render field using HSV color space.
        
        H (Hue): Phase (arg(field))
        S (Saturation): Frequency content (local gradient)
        V (Value): Magnitude (|field|)
        
        This is the primary rendering mode for UPFM images.
        """
        if self.verbose:
            print(f"Rendering: {title}")
        
        magnitude = np.abs(field)
        phase = np.angle(field)
        
        # Normalize components
        mag_norm = self.normalize(magnitude)
        phase_norm = (phase + np.pi) / (2 * np.pi)
        
        # Compute local frequency (gradient of phase)
        phase_grad_y, phase_grad_x = np.gradient(phase)
        freq_local = np.sqrt(phase_grad_x**2 + phase_grad_y**2)
        sat_norm = self.normalize(freq_local)
        
        # Build HSV image
        hsv = np.dstack([phase_norm, sat_norm, mag_norm])
        
        # Convert HSV to RGB
        from matplotlib.colors import hsv_to_rgb
        rgb = hsv_to_rgb(hsv)
        
        # Optional enhancement
        if enhance:
            # Boost contrast slightly
            rgb = np.clip(rgb ** 0.9, 0, 1)
        
        # Convert to uint8
        img_uint8 = (rgb * 255).astype(np.uint8)
        img_pil = Image.fromarray(img_uint8, mode='RGB')
        
        if output_path:
            img_pil.save(output_path, quality=95)
            if self.verbose:
                print(f"✓ Saved: {output_path}")
        
        return img_pil, rgb
    
    def render_frequency_map(self, field, title="Frequency Map",
                            output_path=None, colormap='turbo', enhance=True):
        """
        Render local frequency content of field.
        
        Useful for showing oscillation patterns and resonances.
        """
        if self.verbose:
            print(f"Rendering: {title} (frequency map)")
        
        phase = np.angle(field)
        
        # Compute phase gradient (proportional to local frequency)
        phase_grad_y, phase_grad_x = np.gradient(phase)
        freq_local = np.sqrt(phase_grad_x**2 + phase_grad_y**2)
        
        # Smooth slightly to reduce noise
        from scipy import ndimage
        freq_local = ndimage.gaussian_filter(freq_local, sigma=1.0)
        
        freq_norm = self.normalize(freq_local)
        
        # Apply colormap
        cmap = plt.get_cmap(colormap)
        rgb = cmap(freq_norm)[:, :, :3]
        
        if enhance:
            # Boost contrast
            rgb = np.clip(rgb ** 0.95, 0, 1)
        
        img_uint8 = (rgb * 255).astype(np.uint8)
        img_pil = Image.fromarray(img_uint8, mode='RGB')
        
        if output_path:
            img_pil.save(output_path, quality=95)
            if self.verbose:
                print(f"✓ Saved: {output_path}")
        
        return img_pil, rgb
    
    def render_magnitude_only(self, field, title="Field Magnitude",
                             output_path=None, colormap='hot', enhance=True):
        """Render magnitude only using single colormap."""
        if self.verbose:
            print(f"Rendering: {title} (magnitude)")
        
        magnitude = np.abs(field)
        mag_norm = self.normalize(magnitude)
        
        if enhance:
            # Power law to enhance contrast
            mag_norm = mag_norm ** 0.85
        
        cmap = plt.get_cmap(colormap)
        rgb = cmap(mag_norm)[:, :, :3]
        
        img_uint8 = (rgb * 255).astype(np.uint8)
        img_pil = Image.fromarray(img_uint8, mode='RGB')
        
        if output_path:
            img_pil.save(output_path, quality=95)
            if self.verbose:
                print(f"✓ Saved: {output_path}")
        
        return img_pil, rgb
    
    def render_with_flow(self, field, potential=None, title="Field with Flow",
                        output_path=None, flow_scale=0.15):
        """
        Render field magnitude with gradient flow vectors overlaid.
        
        Shows which direction the field is "flowing" to minimize potential.
        """
        if self.verbose:
            print(f"Rendering: {title} (with flow)")
        
        magnitude = np.abs(field)
        mag_norm = self.normalize(magnitude)
        
        # Base image
        cmap = plt.get_cmap('hot')
        rgb = cmap(mag_norm ** 0.9)[:, :, :3]
        
        # Draw gradient flow if potential provided
        if potential is not None:
            h, w = magnitude.shape
            
            # Subsample gradient for visibility
            step = 16
            y_idx, x_idx = np.mgrid[0:h:step, 0:w:step]
            
            # Compute potential gradient
            gy, gx = np.gradient(potential)
            gy_sub = gy[y_idx, x_idx]
            gx_sub = gx[y_idx, x_idx]
            
            # Normalize and scale for visualization
            g_mag = np.sqrt(gx_sub**2 + gy_sub**2)
            g_mag[g_mag == 0] = 1
            gx_sub = gx_sub / g_mag * flow_scale
            gy_sub = gy_sub / g_mag * flow_scale
            
            # Draw vectors on RGB image (in-place)
            for i, (y, x) in enumerate(zip(y_idx.flat, x_idx.flat)):
                dx, dy = int(gx_sub.flat[i] * 20), int(gy_sub.flat[i] * 20)
                x_end = max(0, min(w-1, x + dx))
                y_end = max(0, min(h-1, y + dy))
                
                # Simple line drawing
                if dx != 0 or dy != 0:
                    rgb[y, x] = [1, 1, 1]  # White markers
        
        img_uint8 = (rgb * 255).astype(np.uint8)
        img_pil = Image.fromarray(img_uint8, mode='RGB')
        
        if output_path:
            img_pil.save(output_path, quality=95)
            if self.verbose:
                print(f"✓ Saved: {output_path}")
        
        return img_pil, rgb
    
    def create_comparison_figure(self, field, potential, title, 
                                 output_path=None, figsize=(15, 5)):
        """Create multi-panel comparison figure (3 rendering styles)."""
        if self.verbose:
            print(f"Creating comparison figure: {title}")
        
        fig, axes = plt.subplots(1, 3, figsize=figsize)
        fig.suptitle(title, fontsize=16, fontweight='bold')
        
        # Panel 1: Magnitude-Phase (HSV)
        magnitude = np.abs(field)
        phase = np.angle(field)
        
        mag_norm = self.normalize(magnitude)
        phase_norm = (phase + np.pi) / (2 * np.pi)
        phase_grad_y, phase_grad_x = np.gradient(phase)
        freq_local = np.sqrt(phase_grad_x**2 + phase_grad_y**2)
        sat_norm = self.normalize(freq_local)
        
        hsv = np.dstack([phase_norm, sat_norm, mag_norm])
        from matplotlib.colors import hsv_to_rgb
        rgb_hsv = hsv_to_rgb(hsv)
        
        axes[0].imshow(rgb_hsv)
        axes[0].set_title('Magnitude-Phase (HSV)', fontweight='bold')
        axes[0].axis('off')
        
        # Panel 2: Frequency map
        cmap = plt.get_cmap('turbo')
        freq_norm = self.normalize(freq_local)
        rgb_freq = cmap(freq_norm)[:, :, :3]
        
        axes[1].imshow(rgb_freq)
        axes[1].set_title('Local Frequency', fontweight='bold')
        axes[1].axis('off')
        
        # Panel 3: Potential landscape
        pot_norm = self.normalize(potential)
        cmap_pot = plt.get_cmap('RdBu_r')
        rgb_pot = cmap_pot(pot_norm)[:, :, :3]
        
        axes[2].imshow(rgb_pot)
        axes[2].set_title('Potential Φ(x,y)', fontweight='bold')
        axes[2].axis('off')
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            if self.verbose:
                print(f"✓ Saved comparison: {output_path}")
        
        return fig
    
    def metadata_string(self, field, potential, concept_name, parameters):
        """Generate metadata string for image documentation."""
        mag_mean = np.mean(np.abs(field))
        mag_max = np.max(np.abs(field))
        phase_range = 2 * np.pi
        
        meta = f"""
{concept_name}
================
Parameters: {parameters}
Field magnitude: [{np.min(np.abs(field)):.4f}, {mag_max:.4f}]
Field magnitude (mean): {mag_mean:.4f}
Phase range: [0, {phase_range:.4f}]
Potential range: [{np.min(potential):.4f}, {np.max(potential):.4f}]

Generated via: ∂i/∂t = -∇Φ(x,y) [gradient descent]
Rendering: HSV color space (Phase→Hue, Frequency→Saturation, Magnitude→Value)
"""
        return meta


if __name__ == "__main__":
    # Test renderer (requires a field from solver)
    print("Renderer module loaded. Use with FieldSolver to render images.")
