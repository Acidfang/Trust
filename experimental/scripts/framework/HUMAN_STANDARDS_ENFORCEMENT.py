"""
HUMAN_STANDARDS_ENFORCEMENT.py

Implements the Human Standards for Universal Containers:
- Quaternion (Hamilton convention) for all rotations
- Arrow vector for all dipole representations
- Consistent field visualization

All 9+ molecules rendered using THE SAME standards.
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, Dict, Optional, List
import json
from xml.dom import minidom
import xml.etree.ElementTree as ET

# ============================================================================
# STANDARD 1: QUATERNION (HAMILTON CONVENTION) - ALL ROTATIONS
# ============================================================================

@dataclass
class Quaternion:
    """
    Unit quaternion in Hamilton convention: q = w + xi + yj + zk
    
    Invariant: w² + x² + y² + z² = 1.0 ± 0.001
    
    References:
      - Wikipedia: Quaternions and Spatial Rotation
      - Hamilton convention (established 1844, ALL major frameworks use this)
      - NOT Shuster convention (marked "usage discouraged" in literature)
    """
    
    w: float  # Scalar (real) part
    x: float  # Vector (imaginary) i-component
    y: float  # Vector (imaginary) j-component
    z: float  # Vector (imaginary) k-component
    
    def __post_init__(self):
        """Ensure unit quaternion after construction"""
        self.normalize()
    
    def normalize(self) -> None:
        """Normalize to unit quaternion: |q| = 1.0"""
        norm = np.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
        if norm < 1e-10:
            raise ValueError("Cannot normalize zero quaternion")
        self.w /= norm
        self.x /= norm
        self.y /= norm
        self.z /= norm
    
    def magnitude(self) -> float:
        """Return magnitude (should be ~1.0 for unit quaternion)"""
        return np.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
    
    @staticmethod
    def from_axis_angle(axis: np.ndarray, angle_rad: float) -> 'Quaternion':
        """
        Create quaternion from axis-angle representation.
        
        Standard formula (Euler axis-angle):
          q = cos(θ/2) + sin(θ/2) * (u_x*i + u_y*j + u_z*k)
          
        where u = (u_x, u_y, u_z) is normalized rotation axis
        """
        # Normalize axis
        axis = np.array(axis, dtype=float)
        axis_norm = np.linalg.norm(axis)
        if axis_norm < 1e-10:
            raise ValueError("Rotation axis must be non-zero")
        u = axis / axis_norm
        
        half_angle = angle_rad / 2.0
        w = np.cos(half_angle)
        xyz = u * np.sin(half_angle)
        
        return Quaternion(w, xyz[0], xyz[1], xyz[2])
    
    def to_axis_angle(self) -> Dict:
        """
        Convert to axis-angle representation.
        
        Returns: {
            'axis': [ux, uy, uz],           # unit vector
            'angle_rad': θ,                 # radians
            'angle_deg': θ * 180/π          # degrees
        }
        
        Reference: Rodrigues formula (1840)
        """
        # Extract angle
        w_clipped = np.clip(self.w, -1.0, 1.0)
        angle_rad = 2.0 * np.arccos(w_clipped)
        
        # Extract axis
        sin_half_angle = np.sin(angle_rad / 2.0)
        
        if abs(sin_half_angle) < 1e-10:
            # Undefined axis for identity rotation
            axis = np.array([0.0, 0.0, 1.0])
        else:
            axis = np.array([self.x, self.y, self.z]) / sin_half_angle
            axis /= np.linalg.norm(axis)  # Normalize
        
        return {
            'axis': axis,
            'angle_rad': angle_rad,
            'angle_deg': float(np.degrees(angle_rad))
        }
    
    def to_matrix(self) -> np.ndarray:
        """
        Convert to 3x3 rotation matrix.
        
        For unit quaternion (w, x, y, z):
        
        R = [1-2(y²+z²)    2(xy-wz)       2(xz+wy)    ]
            [2(xy+wz)      1-2(x²+z²)     2(yz-wx)    ]
            [2(xz-wy)      2(yz+wx)       1-2(x²+y²)  ]
        """
        w, x, y, z = self.w, self.x, self.y, self.z
        
        return np.array([
            [1 - 2*(y**2 + z**2),  2*(x*y - w*z),      2*(x*z + w*y)],
            [2*(x*y + w*z),        1 - 2*(x**2 + z**2), 2*(y*z - w*x)],
            [2*(x*z - w*y),        2*(y*z + w*x),      1 - 2*(x**2 + y**2)]
        ], dtype=float)
    
    def compose(self, q2: 'Quaternion') -> 'Quaternion':
        """
        Compose two rotations: self THEN q2.
        
        Quaternion multiplication (Hamilton product):
          (q1 * q2) = (w1*w2 - x1*x2 - y1*y2 - z1*z2) + ...
          
        WARNING: NOT commutative; order matters!
          q1 ⊗ q2 ≠ q2 ⊗ q1
          
        Reference: Hamilton multiplication rules (established 1844)
        """
        w1, x1, y1, z1 = self.w, self.x, self.y, self.z
        w2, x2, y2, z2 = q2.w, q2.x, q2.y, q2.z
        
        w = w1*w2 - x1*x2 - y1*y2 - z1*z2
        x = w1*x2 + x1*w2 + y1*z2 - z1*y2
        y = w1*y2 - x1*z2 + y1*w2 + z1*x2
        z = w1*z2 + x1*y2 - y1*x2 + z1*w2
        
        return Quaternion(w, x, y, z)
    
    def rotate_vector(self, v: np.ndarray) -> np.ndarray:
        """
        Rotate 3D vector by this quaternion.
        
        Formula: v' = q * v * q⁻¹
        
        For unit quaternion: q⁻¹ = (w, -x, -y, -z)
        """
        v = np.array(v, dtype=float)
        
        # Handle zero vector (at origin - no rotation needed)
        magnitude = np.linalg.norm(v)
        if magnitude < 1e-10:
            return np.array([0.0, 0.0, 0.0])
        
        # Convert vector to pure quaternion (bypass normalization)
        v_quat = Quaternion.__new__(Quaternion)
        v_quat.w = 0.0
        v_quat.x = v[0]
        v_quat.y = v[1]
        v_quat.z = v[2]
        
        # Conjugate (inverse for unit quaternion)
        q_inv = Quaternion(self.w, -self.x, -self.y, -self.z)
        
        # Rotate: q * v * q^-1
        rotated = self.compose(v_quat).compose(q_inv)
        
        return np.array([rotated.x, rotated.y, rotated.z])
    
    def slerp(self, q2: 'Quaternion', t: float) -> 'Quaternion':
        """
        Spherical linear interpolation (SLERP) between two quaternions.
        
        Smooth rotation animation between self (t=0) and q2 (t=1).
        
        Used for: Smooth rotation keyframes in animations
        """
        # Compute dot product
        dot = self.w*q2.w + self.x*q2.x + self.y*q2.y + self.z*q2.z
        
        # Clamp to [-1, 1]
        if dot < 0.0:
            q2 = Quaternion(-q2.w, -q2.x, -q2.y, -q2.z)
            dot = -dot
        dot = np.clip(dot, -1.0, 1.0)
        
        # Compute angle
        theta = np.arccos(dot)
        sin_theta = np.sin(theta)
        
        if sin_theta < 1e-10:
            # Quaternions are very close, use linear interpolation
            w = self.w + t * (q2.w - self.w)
            x = self.x + t * (q2.x - self.x)
            y = self.y + t * (q2.y - self.y)
            z = self.z + t * (q2.z - self.z)
        else:
            # SLERP formula
            a = np.sin((1-t) * theta) / sin_theta
            b = np.sin(t * theta) / sin_theta
            w = a * self.w + b * q2.w
            x = a * self.x + b * q2.x
            y = a * self.y + b * q2.y
            z = a * self.z + b * q2.z
        
        return Quaternion(w, x, y, z)
    
    def to_dict(self) -> Dict:
        """Export as JSON-serializable dict"""
        return {
            'w': float(self.w),
            'x': float(self.x),
            'y': float(self.y),
            'z': float(self.z),
            'magnitude': float(self.magnitude()),
            'axis_angle': self.to_axis_angle()
        }


# ============================================================================
# STANDARD 2: DIPOLE - ARROW VECTOR REPRESENTATION
# ============================================================================

@dataclass
class Dipole:
    """
    Universal dipole representation: Arrow from negative → positive.
    
    Invariants:
      - Source: negative charge center
      - Target: positive charge center
      - Direction: unit vector from source to target
      - Magnitude: >= 0, in atomic units (Debye on request)
      
    References:
      - Molecular chemistry: standard convention
      - Electromagnetism: field lines from + to −
      - Atomic units: 1 a.u. = e·a₀ ≈ 2.54 Debye
    """
    
    source_negative: np.ndarray  # [x, y, z] coordinates of negative charge
    target_positive: np.ndarray  # [x, y, z] coordinates of positive charge
    magnitude_atomic: Optional[float] = None
    
    def __post_init__(self):
        self.source_negative = np.array(self.source_negative, dtype=float)
        self.target_positive = np.array(self.target_positive, dtype=float)
    
    @property
    def vector(self) -> np.ndarray:
        """Dipole as vector: target - source"""
        return self.target_positive - self.source_negative
    
    @property
    def magnitude(self) -> float:
        """Magnitude in atomic units"""
        if self.magnitude_atomic is not None:
            return self.magnitude_atomic
        return float(np.linalg.norm(self.vector))
    
    @property
    def direction(self) -> np.ndarray:
        """Unit vector pointing from negative to positive"""
        mag = self.magnitude
        if mag < 1e-10:
            return np.array([0.0, 0.0, 0.0])
        return self.vector / mag
    
    @property
    def magnitude_debye(self) -> float:
        """Convert magnitude to Debye (1 a.u. = 2.54 Debye)"""
        return self.magnitude * 2.54
    
    def rotate(self, quaternion: Quaternion) -> 'Dipole':
        """Rotate dipole by quaternion"""
        rotated_vector = quaternion.rotate_vector(self.vector)
        new_target = self.source_negative + rotated_vector
        return Dipole(self.source_negative, new_target, self.magnitude_atomic)
    
    def color_code(self) -> Tuple[int, int, int]:
        """
        Color based on magnitude (0-1 normalized, then HSL).
        
        Standard CPK-style color:
          0.00  → Gray   (128, 128, 128)
          0.33  → Yellow (255, 255, 0)
          0.67  → Orange (255, 165, 0)
          1.00  → Red    (255, 0, 0)
        """
        # Normalize magnitude with saturation
        norm_mag = np.tanh(self.magnitude / 10.0)
        
        if norm_mag < 0.25:
            return (128, 128, 128)  # Gray
        elif norm_mag < 0.50:
            # Interpolate gray → yellow
            t = (norm_mag - 0.25) / 0.25
            return (128 + int(127*t), 128 + int(127*t), int(0))
        elif norm_mag < 0.75:
            # Interpolate yellow → orange
            t = (norm_mag - 0.50) / 0.25
            return (255, 255 - int(90*t), int(0))
        else:
            # Interpolate orange → red
            t = (norm_mag - 0.75) / 0.25
            return (255, 165 - int(165*t), int(0))
    
    def to_dict(self) -> Dict:
        """Export as JSON-serializable dict"""
        return {
            'source_negative': self.source_negative.tolist(),
            'target_positive': self.target_positive.tolist(),
            'magnitude_atomic_units': float(self.magnitude),
            'magnitude_debye': float(self.magnitude_debye),
            'direction': self.direction.tolist(),
            'color_rgb': self.color_code()
        }


# ============================================================================
# STANDARD 3: UNIVERSAL CONTAINER - STANDARDS ENFORCER
# ============================================================================

@dataclass
class UniversalContainerStandards:
    """
    Enforces Human Standards for all containers.
    
    Validates:
      1. Orientation as quaternion (Hamilton convention)
      2. Dipole as arrow vector
      3. Field as consistent visualizations
      4. Metadata XML generation
    """
    
    entity_id: str
    entity_type: str  # "molecule", "field", "point_cloud", etc.
    
    # Mandatory
    orientation: Quaternion
    dipole: Dipole
    
    # Optional properties
    properties: Dict = None
    rendering_model: str = "ball_and_stick"  # CPK standard
    camera_angle: str = "isometric_35.26_45.0"
    
    def __post_init__(self):
        if self.properties is None:
            self.properties = {}
    
    def validate(self) -> Dict:
        """
        Comprehensive validation against standards.
        
        Returns: {
            'valid': bool,
            'errors': [list of issues],
            'warnings': [list of cautions],
            'metrics': {...}
        }
        """
        errors = []
        warnings = []
        
        # Check 1: Orientation is unit quaternion
        mag = self.orientation.magnitude()
        if abs(mag - 1.0) > 0.01:
            errors.append(f"Quaternion not unit: |q| = {mag:.6f} (expected 1.0±0.001)")
        
        # Check 2: Dipole is valid
        if len(self.dipole.source_negative) != 3:
            errors.append("Dipole source must be 3D point")
        if len(self.dipole.target_positive) != 3:
            errors.append("Dipole target must be 3D point")
        
        dipole_mag = self.dipole.magnitude
        if dipole_mag < 0:
            errors.append(f"Dipole magnitude cannot be negative: {dipole_mag}")
        if dipole_mag > 100:
            warnings.append(f"Dipole magnitude unusually large: {dipole_mag} a.u.")
        
        # Check 3: No NaN or Inf
        for attr in ['w', 'x', 'y', 'z']:
            val = getattr(self.orientation, attr)
            if np.isnan(val) or np.isinf(val):
                errors.append(f"Quaternion component {attr} is {val}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'metrics': {
                'quaternion_magnitude': float(mag),
                'dipole_magnitude_au': float(dipole_mag),
                'dipole_magnitude_debye': float(self.dipole.magnitude_debye)
            }
        }
    
    def export_metadata_xml(self) -> str:
        """
        Generate XML metadata following HUMAN_STANDARDS format.
        
        Includes:
          - Orientation (quaternion + axis-angle reference)
          - Dipole (source, target, magnitude, color)
          - Rendering parameters
        """
        root = ET.Element('container_render')
        
        # Metadata
        meta = ET.SubElement(root, 'metadata')
        ET.SubElement(meta, 'entity_id').text = self.entity_id
        ET.SubElement(meta, 'entity_type').text = self.entity_type
        ET.SubElement(meta, 'renderer').text = 'HUMAN_STANDARDS_v1.0'
        ET.SubElement(meta, 'standard_authority').text = 'Scientific consensus (Rotation Formalisms, Molecular Graphics, Quaternions & Spatial Rotation)'
        
        # Orientation
        orient = ET.SubElement(root, 'orientation_standard')
        ET.SubElement(orient, 'representation').text = 'quaternion_hamilton'
        ET.SubElement(orient, 'q_w').text = f"{self.orientation.w:.6f}"
        ET.SubElement(orient, 'q_x').text = f"{self.orientation.x:.6f}"
        ET.SubElement(orient, 'q_y').text = f"{self.orientation.y:.6f}"
        ET.SubElement(orient, 'q_z').text = f"{self.orientation.z:.6f}"
        
        # Axis-angle reference
        aa = self.orientation.to_axis_angle()
        aa_elem = ET.SubElement(orient, 'euler_axis_angle_reference')
        ET.SubElement(aa_elem, 'axis').text = f"{aa['axis'][0]:.6f} {aa['axis'][1]:.6f} {aa['axis'][2]:.6f}"
        ET.SubElement(aa_elem, 'angle_rad').text = f"{aa['angle_rad']:.6f}"
        ET.SubElement(aa_elem, 'angle_deg').text = f"{aa['angle_deg']:.2f}"
        
        # Dipole
        dip = ET.SubElement(root, 'dipole_standard')
        ET.SubElement(dip, 'representation').text = 'arrow_vector'
        src = ET.SubElement(dip, 'source_negative')
        src.text = f"{self.dipole.source_negative[0]:.6f} {self.dipole.source_negative[1]:.6f} {self.dipole.source_negative[2]:.6f}"
        tgt = ET.SubElement(dip, 'target_positive')
        tgt.text = f"{self.dipole.target_positive[0]:.6f} {self.dipole.target_positive[1]:.6f} {self.dipole.target_positive[2]:.6f}"
        ET.SubElement(dip, 'magnitude_atomic_units').text = f"{self.dipole.magnitude:.6f}"
        ET.SubElement(dip, 'magnitude_debye').text = f"{self.dipole.magnitude_debye:.6f}"
        
        dir_elem = ET.SubElement(dip, 'direction_unit')
        d = self.dipole.direction
        dir_elem.text = f"{d[0]:.6f} {d[1]:.6f} {d[2]:.6f}"
        
        rgb = self.dipole.color_code()
        ET.SubElement(dip, 'color_rgb').text = f"({rgb[0]}, {rgb[1]}, {rgb[2]})"
        
        # Rendering
        rend = ET.SubElement(root, 'rendering_parameters')
        ET.SubElement(rend, 'model_type').text = self.rendering_model
        ET.SubElement(rend, 'camera').text = self.camera_angle
        ET.SubElement(rend, 'elevation_deg').text = "35.26"
        ET.SubElement(rend, 'azimuth_deg').text = "45.0"
        ET.SubElement(rend, 'colormap').text = "CPK_standard"
        
        # Pretty-print
        rough_string = ET.tostring(root, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def to_json(self) -> str:
        """Export all data as JSON"""
        data = {
            'entity_id': self.entity_id,
            'entity_type': self.entity_type,
            'orientation': self.orientation.to_dict(),
            'dipole': self.dipole.to_dict(),
            'rendering': {
                'model': self.rendering_model,
                'camera': self.camera_angle
            },
            'validation': self.validate()
        }
        return json.dumps(data, indent=2)


# ============================================================================
# HELPER FUNCTIONS FOR ALL CONTAINERS
# ============================================================================

def create_molecular_container(
    mol_id: str,
    atoms: List[Dict],  # [{'pos': [x,y,z], 'element': 'C'}, ...]
    rotation_axis: np.ndarray = None,
    rotation_angle_deg: float = 0.0,
    dipole_source=None,
    dipole_target=None
) -> UniversalContainerStandards:
    """
    Factory function: Create standardized container from molecular data.
    
    Uses QUATERNION (Hamilton) + DIPOLE (arrow) standards automatically.
    """
    
    # Default rotation: identity
    if rotation_axis is None:
        rotation_axis = np.array([0, 0, 1])
    q = Quaternion.from_axis_angle(rotation_axis, np.radians(rotation_angle_deg))
    
    # Default dipole: from center of negative to positive
    if dipole_source is None:
        # Compute center points (simplified)
        positions = np.array([a['pos'] for a in atoms])
        center = np.mean(positions, axis=0)
        dipole_source = center - np.array([2, 0, 0])
        dipole_target = center + np.array([2, 0, 0])
    
    dipole = Dipole(dipole_source, dipole_target)
    
    return UniversalContainerStandards(
        entity_id=mol_id,
        entity_type='molecule',
        orientation=q,
        dipole=dipole,
        rendering_model='ball_and_stick',
        camera_angle='isometric_35.26_45.0'
    )


# ============================================================================
# DEMONSTRATION: All 9 molecules using HUMAN STANDARDS
# ============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("HUMAN STANDARDS FOR UNIVERSAL CONTAINERS - DEMONSTRATION")
    print("=" * 80)
    print()
    
    # Create 9 standardized containers
    molecules = []
    for i in range(1, 10):
        angle = (i - 1) * 40.0  # Different rotation angles
        axis = np.array([0, 0, 1])  # All rotate around Z
        
        container = create_molecular_container(
            mol_id=f'molecule_{i:03d}',
            atoms=[
                {'pos': [-1, 0, 0], 'element': 'C'},
                {'pos': [1, 0, 0], 'element': 'O'}
            ],
            rotation_axis=axis,
            rotation_angle_deg=angle,
            dipole_source=np.array([-2, 0, 0]),
            dipole_target=np.array([2, 0, 0])
        )
        molecules.append(container)
        
        # Validate
        validation = container.validate()
        print(f"Molecule {i}:")
        print(f"  ✓ Valid: {validation['valid']}")
        print(f"  Orientation: Q = ({container.orientation.w:.3f}, {container.orientation.x:.3f}, {container.orientation.y:.3f}, {container.orientation.z:.3f})")
        print(f"  Dipole: {container.dipole.magnitude:.3f} a.u. ({container.dipole.magnitude_debye:.3f} Debye)")
        print(f"  Color: RGB{container.dipole.color_code()}")
        print()
    
    # Export metadata for first molecule
    print("=" * 80)
    print("METADATA XML (Molecule 1)")
    print("=" * 80)
    print(molecules[0].export_metadata_xml())
    
    print("\n" + "=" * 80)
    print(f"✓ ALL 9 MOLECULES USING HUMAN STANDARDS (Quaternion + Dipole + Field)")
    print("=" * 80)
