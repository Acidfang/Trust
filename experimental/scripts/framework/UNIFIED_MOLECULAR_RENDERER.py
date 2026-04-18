"""
UNIFIED MOLECULAR GIF GENERATOR

Integrates ALL primitives into a cohesive, holistic system.
Every decision considers geometry, field resolution, composition strategy, and invariance.
"""

import sys
sys.path.insert(0, r'c:\Determined')

from FIELD_VISUALIZATION_PRIMITIVES import (
    GeometryAnalyzer,
    GeometryMetrics,
    FieldResolutionRotation,
    FrameCompositionStrategy,
    FieldLayer,
    ProjectionPrimitive,
    RotationPrimitive,
    AtomicProperties,
)

from typing import List, Tuple, Dict
from dataclasses import dataclass
from PIL import Image, ImageDraw
import math
import os
import time

OUTPUT_DIR = r"c:\Determined\molecular_renders"


@dataclass
class Molecule:
    """Molecular structure."""
    name: str
    atoms: List[Tuple[str, float, float, float]]  # (element, x, y, z)
    bonds: List[Tuple[int, int, float]]  # (atom1_idx, atom2_idx, bond_order)


class UnifiedMolecularRenderer:
    """
    Comprehensive molecular visualization using ALL primitives.
    
    HOLISTIC ARCHITECTURE:
    1. GEOMETRY → Field resolution metrics
    2. METRICS → Optimal rotation strategy
    3. ROTATION → Frame-aligned angles
    4. PROJECTION → 2D coordinates with depth
    5. COMPOSITION → Painter's algorithm layers
    6. PROPERTIES → Atomic data lookups
    """
    
    def __init__(self):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        self.geometry_cache: Dict = {}  # Cache geometry analysis
        self.metrics = {
            "render_time": 0,
            "frames_generated": 0,
            "file_size_kb": 0,
        }
    
    def _get_geometry(self, molecule: Molecule) -> GeometryMetrics:
        """Cache geometry analysis (PRIMITIVE 1: GEOMETRY ANALYSIS)."""
        key = molecule.name
        if key not in self.geometry_cache:
            self.geometry_cache[key] = GeometryAnalyzer.compute(molecule.atoms)
        return self.geometry_cache[key]
    
    def _calculate_frame_rotation(self, molecule: Molecule, frame_idx: int, total_frames: int) -> FieldResolutionRotation:
        """
        Calculate frame rotation using field-aware strategy.
        PRIMITIVE 2: FIELD RESOLUTION ROTATION
        """
        geom = self._get_geometry(molecule)
        frame_norm = (frame_idx / total_frames) * 2 * math.pi
        
        # Create rotation object and apply frame normalization
        fr = FieldResolutionRotation(y_rotation=0, x_tilt=0, z_roll=0)
        return fr.apply_to_angles(frame_norm, geom)
    
    def render_molecule_to_gif(self, molecule: Molecule, output_filename: str = None, frames: int = 30) -> str:
        """Render with COMPOSITION STRATEGY (PRIMITIVE 3 & 4)."""
        
        start_time = time.time()
        
        if output_filename is None:
            output_filename = f"{molecule.name.replace(' ', '_').replace('(', '').replace(')', '')}.gif"
        
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # STAGE 1: RENDER (parallelism_principle)
        frame_images = []
        
        for frame_idx in range(frames):
            # Calculate field-resolution-based rotation with smooth easing
            rotation = self._calculate_frame_rotation(molecule, frame_idx, frames)
            
            # Create frame with ALL considerations
            img = self._create_comprehensive_frame(
                molecule, 
                rotation.y_rotation, 
                rotation.x_tilt, 
                rotation.z_roll,
                frame_idx,
                frames
            )
            frame_images.append(img)
            self.metrics["frames_generated"] += 1
        
        # STAGE 2: BATCH (amortization_principle)
        # All frames batched together
        
        # STAGE 3: TRANSFER (predictability_principle)
        duration_ms = 40
        
        # STAGE 4: ENCODE (fail_fast_principle)
        if not frame_images:
            raise ValueError("No frames generated")
        
        # STAGE 5: OPTIMIZE (simplicity_principle)
        frame_images[0].save(
            output_path,
            save_all=True,
            append_images=frame_images[1:],
            duration=duration_ms,
            loop=0,
            optimize=False
        )
        
        file_size_kb = os.path.getsize(output_path) / 1024
        self.metrics["file_size_kb"] = file_size_kb
        self.metrics["render_time"] = time.time() - start_time
        
        return output_path
    
    def _create_comprehensive_frame(self, molecule: Molecule, angle_y: float, angle_x: float, angle_z: float,
                                   frame_idx: int, total_frames: int) -> Image.Image:
        """
        Create frame considering EVERYTHING:
        - Geometry metrics for decisions
        - Optimal layer composition
        - Projection strategy
        - Rotation stability
        - Atomic properties
        """
        
        width, height = 500, 500  # Higher resolution for crispness
        img = Image.new('RGB', (width, height), color=(255, 255, 255))
        cx, cy = width // 2, height // 2
        scale = 100  # Larger scale for better visibility
        
        # Get geometry metrics (PRIMITIVE 1)
        geom = self._get_geometry(molecule)
        
        # ROTATE using stable primitive (PRIMITIVE 6: ROTATION)
        rotated_atoms = RotationPrimitive.rotate_euler(
            molecule.atoms, angle_x, angle_y, angle_z
        )
        
        # PROJECT using consistent strategy (PRIMITIVE 5: PROJECTION)
        projected = ProjectionPrimitive.perspective_project(
            [(a[1], a[2], a[3]) for a in rotated_atoms],
            scale, cx, cy, focal_distance=2.0
        )
        
        # COMPOSE using optimal layer order (PRIMITIVE 3 & 4)
        for layer in FrameCompositionStrategy.COMPOSITION_ORDER:
            blend = FrameCompositionStrategy.optimal_blend_mode(layer)
            
            if layer == FieldLayer.QUANTUM_FIELD:
                self._draw_quantum_field(img, projected, molecule, geom)
            
            elif layer == FieldLayer.ELECTROSTATIC:
                self._draw_electrostatic_field(img, projected, molecule)
            
            elif layer == FieldLayer.VDW_SURFACE:
                draw = ImageDraw.Draw(img)
                self._draw_vdw_surface(img, draw, projected, molecule)
            
            elif layer == FieldLayer.ORBITAL_REGIONS:
                draw = ImageDraw.Draw(img)
                self._draw_orbital_regions(img, draw, projected)
            
            elif layer == FieldLayer.BONDS:
                draw = ImageDraw.Draw(img)
                self._draw_bonds(img, draw, projected, molecule)
            
            elif layer == FieldLayer.ATOMS:
                draw = ImageDraw.Draw(img)
                self._draw_atoms(img, draw, projected, molecule)
            
            elif layer == FieldLayer.VALENCE_DOTS:
                draw = ImageDraw.Draw(img)
                self._draw_valence_dots(img, draw, projected, molecule)
            
            elif layer == FieldLayer.AROMATIC_INDICATORS:
                draw = ImageDraw.Draw(img)
                if "Benzene" in molecule.name:
                    self._draw_aromatic_rings(img, draw, projected, molecule, geom)
            
            elif layer == FieldLayer.DIPOLE_VECTORS:
                draw = ImageDraw.Draw(img)
                self._draw_dipole_moment(img, draw, projected, molecule, geom)
        
        # Add frame information
        draw = ImageDraw.Draw(img)
        self._draw_frame_info(img, draw, molecule, geom, frame_idx, total_frames)
        
        return img
    
    def _draw_quantum_field(self, img: Image.Image, projected: List, molecule: Molecule, geom: GeometryMetrics):
        """Quantum field based on geometry density with improved vibrancy."""
        field = Image.new('RGBA', img.size, (0, 0, 0, 0))
        field_draw = ImageDraw.Draw(field)
        
        for atom_idx, atom_proj in enumerate(projected):
            x, y, depth = atom_proj
            element = molecule.atoms[atom_idx][0]
            
            # Radius scales with density (PRIMITIVE 7: ATOMIC PROPERTIES)
            base_radius = AtomicProperties.get_size(element) + 5
            radius_scale = 1.0 + geom.atom_density * 0.5
            
            for layer in range(4):  # More layers for smoother gradient
                radius = base_radius * radius_scale + (layer * 2.5)
                alpha = int(80 * (1 - layer / 4))  # Stronger base opacity
                color = (120, 180, 255, alpha)  # More vibrant blue
                
                field_draw.ellipse(
                    [(x - radius, y - radius), (x + radius, y + radius)],
                    fill=color
                )
        
        field = field.convert('RGB')
        field_alpha = Image.new('L', field.size, 100)  # Higher opacity
        img.paste(field, (0, 0), field_alpha)
    
    def _draw_electrostatic_field(self, img: Image.Image, projected: List, molecule: Molecule):
        """Electrostatic potential field with improved vibrancy."""
        potential = Image.new('RGBA', img.size, (0, 0, 0, 0))
        potential_draw = ImageDraw.Draw(potential)
        
        for atom_idx, atom_proj in enumerate(projected):
            x, y, depth = atom_proj
            element = molecule.atoms[atom_idx][0]
            charge = AtomicProperties.get_charge(element)  # PRIMITIVE 7
            
            if charge < 0:
                color = (255, int(100 + 155 * abs(charge)), int(100 + 155 * abs(charge)), 90)
            elif charge > 0:
                color = (int(100 + 155 * charge), int(100 + 155 * charge), 255, 90)
            else:
                color = (100, 200, 100, 70)
            
            for layer in range(3):
                r = 25 + (layer * 8)
                potential_draw.ellipse(
                    [(x - r, y - r), (x + r, y + r)],
                    fill=color
                )
        
        potential = potential.convert('RGB')
        potential_alpha = Image.new('L', potential.size, 90)  # Slightly higher opacity
        img.paste(potential, (0, 0), potential_alpha)
    
    def _draw_vdw_surface(self, img: Image.Image, draw: ImageDraw.ImageDraw, projected: List, molecule: Molecule):
        """Van der Waals surface visualization."""
        for atom_idx, atom_proj in enumerate(projected):
            x, y, depth = atom_proj
            element = molecule.atoms[atom_idx][0]
            
            vdw = (AtomicProperties.VDW_RADII.get(element, 1.5) * 8)  # PRIMITIVE 7
            
            steps = 24
            points = []
            for i in range(steps):
                angle = (i / steps) * 2 * math.pi
                px = x + vdw * math.cos(angle)
                py = y + vdw * math.sin(angle)
                points.append((px, py))
            
            for i in range(0, len(points), 2):
                if i + 1 < len(points):
                    draw.line([points[i], points[i + 1]], fill=(200, 200, 100), width=1)
    
    def _draw_orbital_regions(self, img: Image.Image, draw: ImageDraw.ImageDraw, projected: List):
        """Bonding orbital visualization."""
        if len(projected) >= 2:
            for i in range(len(projected) - 1):
                x1, y1, _ = projected[i]
                x2, y2, _ = projected[i + 1]
                
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                dx, dy = x2 - x1, y2 - y1
                dist = math.sqrt(dx**2 + dy**2)
                
                if dist > 0:
                    for offset in [-8, 8]:
                        angle = math.atan2(dy, dx)
                        ox = mx + offset * math.cos(angle + math.pi/2)
                        oy = my + offset * math.sin(angle + math.pi/2)
                        
                        draw.ellipse(
                            [(ox - 10, oy - 6), (ox + 10, oy + 6)],
                            fill=(150, 200, 255),
                            outline=(100, 150, 200)
                        )
    
    def _draw_bonds(self, img: Image.Image, draw: ImageDraw.ImageDraw, projected: List, molecule: Molecule):
        """Draw bonds with better clarity and contrast."""
        for bond_idx in molecule.bonds:
            atom1_idx, atom2_idx, bond_order = bond_idx
            
            x1, y1 = projected[atom1_idx][:2]
            x2, y2 = projected[atom2_idx][:2]
            
            # Better bond colors based on type
            bond_colors = {1.0: (80, 80, 80), 2.0: (100, 100, 120), 3.0: (120, 100, 140)}
            color = bond_colors.get(bond_order, (80, 80, 80))
            thickness = max(2, int(bond_order * 1.5))  # Thicker bonds
            
            # Glow effect for better visibility
            draw.line([(x1, y1), (x2, y2)], fill=(220, 220, 220), width=thickness + 2)
            draw.line([(x1, y1), (x2, y2)], fill=color, width=thickness)
    
    def _draw_atoms(self, img: Image.Image, draw: ImageDraw.ImageDraw, projected: List, molecule: Molecule):
        """Draw atoms with enhanced glow and better contrast."""
        for atom_idx, atom_proj in enumerate(projected):
            x, y, depth = atom_proj
            element = molecule.atoms[atom_idx][0]
            
            color = AtomicProperties.get_color(element)  # PRIMITIVE 7
            size = AtomicProperties.get_size(element)    # PRIMITIVE 7
            
            # Enhanced glow layers for better visual depth
            glow_color = tuple(int(c * 0.5) for c in color)  # Darker glow
            for glow_layer in range(3, 0, -1):
                glow_size = size + glow_layer * 2
                draw.ellipse(
                    [(x - glow_size, y - glow_size), (x + glow_size, y + glow_size)],
                    fill=glow_color
                )
            
            # Main atom with stronger outline for clarity
            draw.ellipse(
                [(x - size, y - size), (x + size, y + size)],
                fill=color,
                outline=(30, 30, 30),
                width=2
            )
            
            # Element text with better contrast
            draw.text((x - 4, y - 4), element, fill=(240, 240, 240))
    
    def _draw_valence_dots(self, img: Image.Image, draw: ImageDraw.ImageDraw, projected: List, molecule: Molecule):
        """Draw Lewis-style valence dots."""
        for atom_idx, atom_proj in enumerate(projected):
            x, y, depth = atom_proj
            element = molecule.atoms[atom_idx][0]
            num_valence = AtomicProperties.get_valence(element)  # PRIMITIVE 7
            
            dot_radius = AtomicProperties.get_size(element) + 6
            
            for dot_idx in range(num_valence):
                angle = (dot_idx / max(1, num_valence)) * 2 * math.pi
                dot_x = x + dot_radius * math.cos(angle)
                dot_y = y + dot_radius * math.sin(angle)
                
                draw.ellipse(
                    [(dot_x - 2, dot_y - 2), (dot_x + 2, dot_y + 2)],
                    fill=(255, 100, 100)
                )
    
    def _draw_aromatic_rings(self, img: Image.Image, draw: ImageDraw.ImageDraw, projected: List, 
                            molecule: Molecule, geom: GeometryMetrics):
        """Draw aromatic ring indicators."""
        if len(projected) >= 6:
            ring_indices = list(range(6))
            
            center_x = sum(projected[i][0] for i in ring_indices) / 6
            center_y = sum(projected[i][1] for i in ring_indices) / 6
            
            radius_inner = 45
            for circle_layer in range(2):
                r = radius_inner - (circle_layer * 8)
                draw.ellipse(
                    [(center_x - r, center_y - r), (center_x + r, center_y + r)],
                    outline=(200, 100, 50),
                    width=2
                )
            
            steps = 16
            points = []
            for i in range(steps):
                angle = (i / steps) * 2 * math.pi
                px = center_x + radius_inner * 0.6 * math.cos(angle)
                py = center_y + radius_inner * 0.6 * math.sin(angle)
                points.append((px, py))
            
            for i in range(0, len(points), 2):
                if i + 1 < len(points):
                    draw.line([points[i], points[i + 1]], fill=(255, 150, 50), width=2)
    
    def _draw_dipole_moment(self, img: Image.Image, draw: ImageDraw.ImageDraw, 
                           projected: List, molecule: Molecule, geom: GeometryMetrics):
        """Draw dipole moment vector."""
        charges = {
            "O": -1.0, "N": -0.5, "C": 0.2, "H": 0.1
        }
        
        total_x, total_y = 0, 0
        total_charge = 0
        
        for atom_idx, atom_proj in enumerate(projected):
            x, y, depth = atom_proj
            element = molecule.atoms[atom_idx][0]
            charge = charges.get(element, 0.0)
            
            total_x += x * charge
            total_y += y * charge
            total_charge += abs(charge)
        
        if total_charge > 0:
            dipole_x = total_x / total_charge
            dipole_y = total_y / total_charge
            
            center_x = sum(p[0] for p in projected) / len(projected)
            center_y = sum(p[1] for p in projected) / len(projected)
            
            arrow_x = center_x + dipole_x * 0.2
            arrow_y = center_y + dipole_y * 0.2
            
            if (dipole_x**2 + dipole_y**2) > 1:
                draw.line(
                    [(center_x, center_y), (arrow_x, arrow_y)],
                    fill=(255, 0, 0),
                    width=3
                )
                
                angle = math.atan2(arrow_y - center_y, arrow_x - center_x)
                for da in [-0.3, 0.3]:
                    ux = arrow_x - 8 * math.cos(angle + da)
                    uy = arrow_y - 8 * math.sin(angle + da)
                    draw.line([(arrow_x, arrow_y), (ux, uy)], fill=(255, 0, 0), width=2)
    
    def _draw_frame_info(self, img: Image.Image, draw: ImageDraw.ImageDraw, molecule: Molecule, 
                        geom: GeometryMetrics, frame_idx: int, total_frames: int):
        """Draw frame information."""
        draw.text((10, 10), f"{molecule.name}", fill=(0, 0, 0))
        draw.text((10, 30), f"Frame {frame_idx + 1}/{total_frames}", fill=(100, 100, 100))
        
        # Show geometry metrics
        draw.text((10, 50), f"Spread: {geom.spread_factor:.2f}", fill=(100, 100, 100))
        draw.text((10, 65), f"Density: {geom.atom_density:.2f}", fill=(100, 100, 100))
        draw.text((10, 80), f"Asymmetry: {geom.asymmetry:.2f}", fill=(100, 100, 100))
        
        # Field visualization legend
        legend_y = img.height - 80
        draw.text((10, legend_y), "Fields:", fill=(0, 0, 0))
        draw.line([(10, legend_y + 20), (50, legend_y + 20)], fill=(100, 150, 255), width=3)
        draw.text((55, legend_y + 15), "Quantum", fill=(50, 50, 50))
        
        draw.line([(10, legend_y + 40), (50, legend_y + 40)], fill=(255, 0, 0), width=2)
        draw.text((55, legend_y + 35), "Dipole", fill=(50, 50, 50))


def create_test_molecules() -> List[Molecule]:
    """Create all test molecules."""
    return [
        Molecule(
            name="Water (H2O)",
            atoms=[("O", 0.0, 0.0, 0.0), ("H", 0.96, 0.0, 0.0), ("H", -0.24, 0.93, 0.0)],
            bonds=[(0, 1, 1.0), (0, 2, 1.0)]
        ),
        Molecule(
            name="Methane (CH4)",
            atoms=[
                ("C", 0.0, 0.0, 0.0),
                ("H", 0.63, 0.63, 0.63),
                ("H", -0.63, -0.63, 0.63),
                ("H", -0.63, 0.63, -0.63),
                ("H", 0.63, -0.63, -0.63),
            ],
            bonds=[(0,1,1.0), (0,2,1.0), (0,3,1.0), (0,4,1.0)]
        ),
        Molecule(
            name="Benzene (C6H6)",
            atoms=[
                ("C", 1.0, 0.0, 0.0), ("C", 0.5, 0.866, 0.0), ("C", -0.5, 0.866, 0.0),
                ("C", -1.0, 0.0, 0.0), ("C", -0.5, -0.866, 0.0), ("C", 0.5, -0.866, 0.0),
                ("H", 1.9, 0.0, 0.0), ("H", 0.95, 1.64, 0.0), ("H", -0.95, 1.64, 0.0),
                ("H", -1.9, 0.0, 0.0), ("H", -0.95, -1.64, 0.0), ("H", 0.95, -1.64, 0.0),
            ],
            bonds=[(0,1,1.5), (1,2,1.5), (2,3,1.5), (3,4,1.5), (4,5,1.5), (5,0,1.5),
                   (0,6,1.0), (1,7,1.0), (2,8,1.0), (3,9,1.0), (4,10,1.0), (5,11,1.0)]
        ),
        Molecule(
            name="Ammonia (NH3)",
            atoms=[("N", 0.0, 0.0, 0.0), ("H", 0.94, 0.0, 0.0), ("H", -0.47, 0.81, 0.0), ("H", -0.47, -0.81, 0.0)],
            bonds=[(0, 1, 1.0), (0, 2, 1.0), (0, 3, 1.0)]
        ),
        Molecule(
            name="Carbon Dioxide (CO2)",
            atoms=[("C", 0.0, 0.0, 0.0), ("O", 1.16, 0.0, 0.0), ("O", -1.16, 0.0, 0.0)],
            bonds=[(0, 1, 2.0), (0, 2, 2.0)]
        ),
        Molecule(
            name="Ethane (C2H6)",
            atoms=[
                ("C", 0.75, 0.0, 0.0), ("C", -0.75, 0.0, 0.0),
                ("H", 1.1, 0.9, 0.0), ("H", 1.1, -0.45, 0.78), ("H", 1.1, -0.45, -0.78),
                ("H", -1.1, 0.9, 0.0), ("H", -1.1, -0.45, 0.78), ("H", -1.1, -0.45, -0.78),
            ],
            bonds=[(0, 1, 1.0), (0, 2, 1.0), (0, 3, 1.0), (0, 4, 1.0), (1, 5, 1.0), (1, 6, 1.0), (1, 7, 1.0)]
        ),
        Molecule(
            name="Ethene (C2H4)",
            atoms=[
                ("C", 0.66, 0.0, 0.0), ("C", -0.66, 0.0, 0.0),
                ("H", 1.1, 0.9, 0.0), ("H", 1.1, -0.9, 0.0),
                ("H", -1.1, 0.9, 0.0), ("H", -1.1, -0.9, 0.0),
            ],
            bonds=[(0, 1, 2.0), (0, 2, 1.0), (0, 3, 1.0), (1, 4, 1.0), (1, 5, 1.0)]
        ),
        Molecule(
            name="Acetylene (C2H2)",
            atoms=[
                ("C", 0.6, 0.0, 0.0), ("C", -0.6, 0.0, 0.0),
                ("H", 1.35, 0.0, 0.0), ("H", -1.35, 0.0, 0.0),
            ],
            bonds=[(0, 1, 3.0), (0, 2, 1.0), (1, 3, 1.0)]
        ),
        Molecule(
            name="Formaldehyde (CH2O)",
            atoms=[("C", 0.0, 0.0, 0.0), ("O", 1.2, 0.0, 0.0), ("H", -0.6, 0.9, 0.0), ("H", -0.6, -0.9, 0.0)],
            bonds=[(0, 1, 2.0), (0, 2, 1.0), (0, 3, 1.0)]
        ),
    ]


if __name__ == "__main__":
    print("=" * 140)
    print("UNIFIED MOLECULAR RENDERER - COMPREHENSIVE FIELD VISUALIZATION")
    print("=" * 140)
    
    renderer = UnifiedMolecularRenderer()
    molecules = create_test_molecules()
    
    print(f"\nUsing primitives from FIELD_VISUALIZATION_PRIMITIVES")
    print(f"Molecules to render: {len(molecules)}\n")
    
    start_total = time.time()
    
    for i, mol in enumerate(molecules, 1):
        print(f"{i}. Rendering {mol.name}...", end=" ", flush=True)
        
        try:
            output_path = renderer.render_molecule_to_gif(mol, frames=30)
            
            print(f"✓ DONE")
            print(f"   Location: {output_path}")
            print(f"   File size: {renderer.metrics['file_size_kb']:.1f} KB")
            print(f"   Render time: {renderer.metrics['render_time']*1000:.2f} ms\n")
        
        except Exception as e:
            print(f"✗ ERROR: {e}\n")
    
    total_time = time.time() - start_total
    
    print("=" * 140)
    print(f"Total render time: {total_time:.2f}s - All molecules with comprehensive field visualization")
    print("=" * 140)
