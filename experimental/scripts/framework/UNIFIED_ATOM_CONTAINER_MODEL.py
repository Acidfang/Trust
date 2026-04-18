"""
UNIFIED ATOM CONTAINER MODEL
=============================

Combines ALL atom container patterns from codebase:
  1. electron_visualization.py → Electrons in orbital shells
  2. molecule_visualization.py → Atoms with bonds and bond angles
  3. optimized_molecule_animation_generator.py → Simple position-based dictionaries
  4. container_library.py → Generic container with items and primitives
  5. electron_tree_generator.py → Periodic table configurations
  6. UNIVERSAL_ENTITY_CONNECTION_FRAMEWORK.py → Versioned dataclass structures
  7. field_gradient_visualization_system.py → Field grids and Gaussian concentrations
  8. STANDARDS_RENDERER_IMAGES.py → Atom3D/Atom2D projections
  9. FIELD_VISUALIZATION_PRIMITIVES.py → Atomic property tables
  10. universal_field_gradient_system.py → Field regions and overlaps

STRATEGY: Unified Container Architecture
  Layer 1: ATOM CORE (element, position, properties, state)
  Layer 2: ELECTRON SHELL (orbitals, electrons, configurations)
  Layer 3: FIELD REPRESENTATION (Gaussian grid, concentration)
  Layer 4: CONNECTIVITY (bonds, relationships, angles)
  Layer 5: VERSIONING (history, modifications, causality)
  Layer 6: VISUAL PROPERTIES (color, size, representation mode)
  Layer 7: 4-PRIMITIVES (Spatial, Color, Temporal, Structure)

Key Insight: ALL containers share same 4-PRIMITIVE framework
  - SPATIAL: Where is it? (position, grid, coordinates)
  - COLOR: What color? (element-based, orbital-based, intensity)
  - TEMPORAL: How does it change? (animation frames, shells fill)
  - STRUCTURE: What is it? (bonds, electrons, configuration)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any, Set
from enum import Enum
import numpy as np
import math
import time
import hashlib
from abc import ABC, abstractmethod


# ============================================================================
# LAYER 1: ELEMENT & ATOMIC PROPERTIES (from FIELD_VISUALIZATION_PRIMITIVES.py)
# ============================================================================

@dataclass
class AtomicProperties:
    """Invariant atomic property lookup - element-specific constants"""
    
    COLORS = {
        "H": (200, 200, 200),
        "C": (50, 50, 50),
        "N": (50, 100, 200),
        "O": (200, 50, 50),
    }
    
    SIZES = {
        "H": 8,
        "C": 12,
        "N": 11,
        "O": 11,
    }
    
    VALENCE = {
        "H": 1, "C": 4, "N": 5, "O": 6
    }
    
    CHARGES = {
        "O": -0.5, "N": -0.3, "C": 0.0, "H": 0.1
    }
    
    VDW_RADII = {
        "H": 1.20, "C": 1.70, "N": 1.55, "O": 1.52
    }
    
    ELECTRONEGATIVITIES = {
        "H": 2.1, "C": 2.55, "N": 3.04, "O": 3.44, "S": 2.58, "P": 2.19
    }
    
    @classmethod
    def get_properties(cls, element: str) -> Dict[str, Any]:
        """Get all properties for element"""
        return {
            "color": cls.COLORS.get(element, (100, 100, 100)),
            "size": cls.SIZES.get(element, 10),
            "valence": cls.VALENCE.get(element, 0),
            "charge": cls.CHARGES.get(element, 0.0),
            "vdw_radius": cls.VDW_RADII.get(element, 1.5),
            "electronegativity": cls.ELECTRONEGATIVITIES.get(element, 2.5),
        }


# ============================================================================
# LAYER 2: ELECTRON CONFIGURATION (from electron_tree_generator.py + atom_visualization.py)
# ============================================================================

class OrbitalType(Enum):
    S = "s"
    P = "p"
    D = "d"
    F = "f"


@dataclass
class ElectronOrbital:
    """Single orbital with electrons - container for electrons"""
    orbital_name: str  # "1s", "2p", etc.
    shell: int  # n quantum number
    orbital_type: OrbitalType  # s, p, d, f
    max_electrons: int  # 2, 6, 10, 14
    electrons_present: int  # Actual count
    
    def color(self) -> Tuple[int, int, int]:
        """Color based on orbital type"""
        colors = {
            OrbitalType.S: (255, 107, 107),  # Red
            OrbitalType.P: (78, 205, 196),   # Teal
            OrbitalType.D: (69, 183, 209),   # Blue
            OrbitalType.F: (255, 160, 122),  # Light Salmon
        }
        return colors.get(self.orbital_type, (136, 136, 136))
    
    def is_full(self) -> bool:
        """Is this orbital fully occupied?"""
        return self.electrons_present == self.max_electrons


@dataclass
class ElectronShell:
    """Full electron shell (n=1,2,3...) - container for orbitals"""
    shell_number: int  # Principal quantum number n
    orbitals: List[ElectronOrbital] = field(default_factory=list)
    
    def add_orbital(self, orbital: ElectronOrbital) -> None:
        self.orbitals.append(orbital)
    
    def total_electrons(self) -> int:
        return sum(o.electrons_present for o in self.orbitals)
    
    def max_capacity(self) -> int:
        return sum(o.max_electrons for o in self.orbitals)
    
    def orbital_radius(self) -> float:
        """Bohr radius scaling with shell number"""
        return 0.53 * self.shell_number  # Angstroms


@dataclass
class ElectronConfiguration:
    """Complete electron configuration for an atom (from periodic table)"""
    atomic_number: int
    element_symbol: str
    shells: List[ElectronShell] = field(default_factory=list)
    
    @staticmethod
    def generate_configuration(z: int) -> 'ElectronConfiguration':
        """Generate electron configuration using aufbau principle"""
        element = ['', 'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne'][min(z, 10)]
        
        orbital_sequence = [
            (1, OrbitalType.S, 2),
            (2, OrbitalType.S, 2), (2, OrbitalType.P, 6),
            (3, OrbitalType.S, 2), (3, OrbitalType.P, 6),
            (4, OrbitalType.S, 2), (3, OrbitalType.D, 10), (4, OrbitalType.P, 6),
            (5, OrbitalType.S, 2), (4, OrbitalType.D, 10), (5, OrbitalType.P, 6),
        ]
        
        config = ElectronConfiguration(z, element)
        electrons_left = z
        shell_map = {}
        
        for shell_n, orbital_type, max_e in orbital_sequence:
            if electrons_left <= 0:
                break
            
            electrons_in_orbital = min(electrons_left, max_e)
            orbital_name = f"{shell_n}{orbital_type.value}"
            
            if shell_n not in shell_map:
                shell_map[shell_n] = ElectronShell(shell_n)
                config.shells.append(shell_map[shell_n])
            
            orbital = ElectronOrbital(
                orbital_name=orbital_name,
                shell=shell_n,
                orbital_type=orbital_type,
                max_electrons=max_e,
                electrons_present=electrons_in_orbital
            )
            shell_map[shell_n].add_orbital(orbital)
            electrons_left -= electrons_in_orbital
        
        return config


# ============================================================================
# LAYER 3: FIELD REPRESENTATION (from field_gradient_visualization_system.py)
# ============================================================================

@dataclass
class GaussianFieldRegion:
    """Single Gaussian field contribution - container for field intensity"""
    element: str
    position: Tuple[float, float]  # 2D center
    concentration: float  # 0-1, strength
    sigma: float  # Gaussian spread
    
    def intensity_at(self, x: float, y: float) -> float:
        """Gaussian intensity at point (x, y)"""
        dx = x - self.position[0]
        dy = y - self.position[1]
        dist_sq = dx*dx + dy*dy
        return self.concentration * math.exp(-dist_sq / (2 * self.sigma**2))


@dataclass
class FieldGrid:
    """Continuous field representation - container for field regions"""
    width: int
    height: int
    regions: List[GaussianFieldRegion] = field(default_factory=list)
    grid: Optional[np.ndarray] = None  # Cached grid
    
    def add_region(self, region: GaussianFieldRegion) -> None:
        self.regions.append(region)
        self.grid = None  # Invalidate cache
    
    def compute_grid(self, interpolate=True) -> np.ndarray:
        """Compute field grid from regions"""
        if self.grid is not None:
            return self.grid
        
        grid = np.zeros((self.height, self.width))
        
        for region in self.regions:
            for y in range(self.height):
                for x in range(self.width):
                    grid[y, x] += region.intensity_at(float(x), float(y))
        
        self.grid = grid
        return grid


# ============================================================================
# LAYER 4: BONDING & CONNECTIVITY (from molecule_visualization.py)
# ============================================================================

@dataclass
class Bond:
    """Chemical bond between two atoms"""
    atom1_id: str
    atom2_id: str
    bond_order: float = 1.0  # 1.0=single, 2.0=double, 3.0=triple
    length: float = 1.0  # Angstroms
    angle_to_third: Optional[float] = None  # Bond angle if part of triplet
    created_time: float = field(default_factory=time.time)
    
    def is_valid(self) -> bool:
        return self.bond_order > 0 and self.bond_order <= 3


# ============================================================================
# LAYER 5: UNIFIED ATOM CONTAINER (combines all above layers)
# ============================================================================

class AtomRepresentationMode(Enum):
    """Different ways to represent atom - from various visualization files"""
    POINT = "point"  # Simple point (optimized_molecule_animation_generator.py)
    CIRCLE_2D = "circle_2d"  # 2D circle (molecule_visualization.py)
    SHELL_VISUALIZATION = "shell_visualization"  # Electron shells (atom_visualization.py)
    FIELD_GAUSSIAN = "field_gaussian"  # Gaussian field (field_gradient_visualization_system.py)
    ATOM_3D = "atom_3d"  # 3D projection (STANDARDS_RENDERER_IMAGES.py)
    ATOM_2D = "atom_2d"  # 2D projected (STANDARDS_RENDERER_IMAGES.py)


@dataclass
class UnifiedAtomContainer:
    """
    UNIFIED ATOM CONTAINER
    
    Combines all container patterns:
    - Storage: dictionary-based (simple, flexible)
    - Hierarchy: shell → orbital → electron (from electron_visualization)
    - Spatial: 3D position + field grid (from field_gradient_visualization_system)
    - Visual: 4 PRIMITIVES (Spatial, Color, Temporal, Structure)
    - Versioning: History tracking (from UNIVERSAL_ENTITY_CONNECTION_FRAMEWORK)
    - Connectivity: Bonds and relationships (from molecule_visualization)
    
    KEY INSIGHT: This atom can be rendered in multiple ways simultaneously
                 and composed into molecules without reimplementation
    """
    
    # ===== LAYER 1: ATOM CORE =====
    atom_id: str
    element: str
    position_3d: Tuple[float, float, float]  # Spatial primitive
    
    # ===== LAYER 2: ELECTRON CONFIGURATION =====
    electron_config: Optional[ElectronConfiguration] = None
    
    # ===== LAYER 3: FIELD REPRESENTATION =====
    field_regions: List[GaussianFieldRegion] = field(default_factory=list)
    field_grid: Optional[FieldGrid] = None
    
    # ===== LAYER 4: CONNECTIVITY =====
    bonds: List[Bond] = field(default_factory=list)
    bond_angles: Dict[str, float] = field(default_factory=dict)
    
    # ===== LAYER 5: PROPERTIES =====
    properties: Dict[str, Any] = field(default_factory=dict)
    charge: float = 0.0
    formal_charge: int = 0
    
    # ===== LAYER 6: VISUAL PROPERTIES (Color Primitive) =====
    color_rgb: Optional[Tuple[int, int, int]] = None
    size_pixels: int = 10
    representation_mode: AtomRepresentationMode = AtomRepresentationMode.POINT
    
    # ===== LAYER 7: VERSIONING & HISTORY =====
    version: int = 1
    created_time: float = field(default_factory=time.time)
    modified_time: float = field(default_factory=time.time)
    modification_history: List[Dict] = field(default_factory=list)
    
    # ===== LAYER 8: TEMPORAL INFO (Temporal Primitive) =====
    animation_frames: Optional[List['UnifiedAtomContainer']] = None
    frame_index: int = 0
    
    # ===== 4 PRIMITIVES TRACKING =====
    primitives_verified: Dict[str, bool] = field(default_factory=lambda: {
        "spatial": False,
        "color": False,
        "temporal": False,
        "structure": False
    })
    
    def __post_init__(self):
        """Initialize from element properties if needed"""
        if self.color_rgb is None:
            props = AtomicProperties.get_properties(self.element)
            self.color_rgb = props["color"]
            self.size_pixels = props["size"]
        
        if not self.properties:
            self.properties = AtomicProperties.get_properties(self.element)
    
    # ===== SPATIAL PRIMITIVE =====
    def get_position_2d(self, projection="isometric") -> Tuple[float, float]:
        """Project 3D position to 2D screen space"""
        if projection == "isometric":
            x = self.position_3d[0] - self.position_3d[2]
            y = self.position_3d[1] - self.position_3d[2] / 2
            return (x, y)
        elif projection == "orthographic_xy":
            return (self.position_3d[0], self.position_3d[1])
        else:
            return (self.position_3d[0], self.position_3d[1])
    
    def get_radius(self) -> float:
        """VdW radius from atomic properties"""
        return self.properties.get("vdw_radius", 1.5)
    
    def distance_to(self, other: 'UnifiedAtomContainer') -> float:
        """Euclidean distance to another atom"""
        dx = self.position_3d[0] - other.position_3d[0]
        dy = self.position_3d[1] - other.position_3d[1]
        dz = self.position_3d[2] - other.position_3d[2]
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    # ===== COLOR PRIMITIVE =====
    def get_color(self) -> Tuple[int, int, int]:
        """Get color (might vary by orbital occupancy for electron shells)"""
        return self.color_rgb
    
    def get_color_by_orbital_type(self, orbital: ElectronOrbital) -> Tuple[int, int, int]:
        """Color electron shell by orbital type"""
        if self.electron_config:
            return orbital.color()
        return self.color_rgb
    
    # ===== STRUCTURE PRIMITIVE =====
    def get_configuration_string(self) -> str:
        """Get electron configuration as string"""
        if not self.electron_config:
            return ""
        
        config_str = ""
        for orbital in self.electron_config.shells:
            for o in orbital.orbitals:
                config_str += f"{o.orbital_name}{o.electrons_present}"
        return config_str
    
    def get_valence_electrons(self) -> int:
        """Count valence electrons"""
        if not self.electron_config or not self.electron_config.shells:
            return self.properties.get("valence", 0)
        
        # Last shell is valence
        last_shell = self.electron_config.shells[-1]
        return last_shell.total_electrons()
    
    # ===== TEMPORAL PRIMITIVE =====
    def add_frame(self, frame: 'UnifiedAtomContainer') -> None:
        """Add animation frame"""
        if self.animation_frames is None:
            self.animation_frames = []
        self.animation_frames.append(frame)
    
    def get_frame(self, index: int) -> Optional['UnifiedAtomContainer']:
        """Get animation frame by index"""
        if self.animation_frames and 0 <= index < len(self.animation_frames):
            frame = self.animation_frames[index]
            frame.frame_index = index
            return frame
        return None
    
    # ===== FIELD REPRESENTATION =====
    def add_field_region(self, element: str, position_2d: Tuple[float, float],
                         concentration: float = 1.0, sigma: float = 30) -> None:
        """Add Gaussian field contribution"""
        region = GaussianFieldRegion(element, position_2d, concentration, sigma)
        self.field_regions.append(region)
        if self.field_grid:
            self.field_grid.add_region(region)
    
    def get_field_grid(self, width: int = 1200, height: int = 1200) -> FieldGrid:
        """Get or create field grid"""
        if self.field_grid is None:
            self.field_grid = FieldGrid(width, height)
            for region in self.field_regions:
                self.field_grid.add_region(region)
        return self.field_grid
    
    # ===== BONDING =====
    def add_bond(self, target_atom_id: str, bond_order: float = 1.0, length: float = 1.0) -> None:
        """Add bond to another atom"""
        bond = Bond(self.atom_id, target_atom_id, bond_order, length)
        self.bonds.append(bond)
    
    def get_bonds(self) -> List[Bond]:
        """Get all bonds from this atom"""
        return self.bonds
    
    # ===== VERSIONING =====
    def record_modification(self, key: str, old_value: Any, new_value: Any) -> None:
        """Track modification history"""
        self.modification_history.append({
            "time": time.time(),
            "version": self.version,
            "key": key,
            "old_value": old_value,
            "new_value": new_value
        })
        self.modified_time = time.time()
        self.version += 1
    
    def get_hash(self) -> str:
        """Compute SHA256 hash of atom state"""
        state_str = f"{self.atom_id}{self.element}{self.position_3d}{self.version}"
        return hashlib.sha256(state_str.encode()).hexdigest()
    
    # ===== 4-PRIMITIVE VERIFICATION =====
    def verify_spatial_primitive(self) -> Tuple[bool, str]:
        """Verify: Position is valid 3D coordinate"""
        if not self.position_3d or len(self.position_3d) != 3:
            return False, "Invalid 3D position"
        if any(math.isnan(v) or math.isinf(v) for v in self.position_3d):
            return False, "Position contains NaN or Inf"
        self.primitives_verified["spatial"] = True
        return True, "Spatial primitive verified"
    
    def verify_color_primitive(self) -> Tuple[bool, str]:
        """Verify: Color is valid RGB tuple"""
        if not self.color_rgb or len(self.color_rgb) != 3:
            return False, "Invalid RGB color"
        if not all(0 <= v <= 255 for v in self.color_rgb):
            return False, "Color values out of range [0-255]"
        self.primitives_verified["color"] = True
        return True, "Color primitive verified"
    
    def verify_temporal_primitive(self) -> Tuple[bool, str]:
        """Verify: Temporal info is consistent"""
        if self.created_time > self.modified_time:
            return False, "Created time after modified time"
        if self.animation_frames and not all(isinstance(f, UnifiedAtomContainer) for f in self.animation_frames):
            return False, "Invalid animation frames"
        self.primitives_verified["temporal"] = True
        return True, "Temporal primitive verified"
    
    def verify_structure_primitive(self) -> Tuple[bool, str]:
        """Verify: Bonds and config are consistent"""
        for bond in self.bonds:
            if not bond.is_valid():
                return False, f"Invalid bond: {bond}"
        if self.electron_config:
            total_e = sum(s.total_electrons() for s in self.electron_config.shells)
            if total_e != self.electron_config.atomic_number:
                return False, f"Electron count mismatch: {total_e} vs {self.electron_config.atomic_number}"
        self.primitives_verified["structure"] = True
        return True, "Structure primitive verified"
    
    def verify_all_primitives(self) -> Tuple[bool, Dict[str, str]]:
        """Verify all 4 primitives"""
        results = {}
        
        results["spatial"] = self.verify_spatial_primitive()[1]
        results["color"] = self.verify_color_primitive()[1]
        results["temporal"] = self.verify_temporal_primitive()[1]
        results["structure"] = self.verify_structure_primitive()[1]
        
        all_passed = all(self.primitives_verified.values())
        return all_passed, results


# ============================================================================
# MOLECULE CONTAINER (combines unified atoms)
# ============================================================================

@dataclass
class UnifiedMoleculeContainer:
    """Molecule as container of unified atoms"""
    molecule_id: str
    molecule_name: str
    atoms: Dict[str, UnifiedAtomContainer] = field(default_factory=dict)
    bonds: List[Bond] = field(default_factory=list)
    
    # Metadata
    version: int = 1
    created_time: float = field(default_factory=time.time)
    
    def add_atom(self, atom: UnifiedAtomContainer) -> None:
        """Add unified atom to molecule"""
        self.atoms[atom.atom_id] = atom
    
    def add_bond(self, atom1_id: str, atom2_id: str, bond_order: float = 1.0) -> None:
        """Add bond between atoms"""
        distance = self.atoms[atom1_id].distance_to(self.atoms[atom2_id])
        bond = Bond(atom1_id, atom2_id, bond_order, distance)
        self.bonds.append(bond)
        
        # Add to atoms' internal bond lists too
        self.atoms[atom1_id].add_bond(atom2_id, bond_order, distance)
        self.atoms[atom2_id].add_bond(atom1_id, bond_order, distance)
    
    def get_formula(self) -> str:
        """Get molecular formula"""
        element_counts = {}
        for atom in self.atoms.values():
            element_counts[atom.element] = element_counts.get(atom.element, 0) + 1
        
        formula = ""
        for element in sorted(element_counts.keys()):
            count = element_counts[element]
            formula += element + (str(count) if count > 1 else "")
        return formula
    
    def get_all_field_regions(self) -> List[GaussianFieldRegion]:
        """Combine field regions from all atoms"""
        all_regions = []
        for atom in self.atoms.values():
            all_regions.extend(atom.field_regions)
        return all_regions
    
    def verify_all_atoms(self) -> bool:
        """Verify all atoms pass 4-primitive check"""
        return all(atom.verify_all_primitives()[0] for atom in self.atoms.values())


# ============================================================================
# RENDERING ENGINE (uses all representation modes)
# ============================================================================

class AtomRenderer(ABC):
    """Abstract renderer for unified atoms"""
    
    @abstractmethod
    def render(self, atom: UnifiedAtomContainer) -> Any:
        pass


class PointRenderer(AtomRenderer):
    """Simple point renderer (optimized_molecule_animation_generator.py style)"""
    
    def render(self, atom: UnifiedAtomContainer) -> Dict:
        return {
            "type": "point",
            "position": atom.position_3d,
            "element": atom.element,
            "color": atom.get_color(),
            "size": atom.size_pixels
        }


class CircleRenderer(AtomRenderer):
    """Circle renderer (molecule_visualization.py style)"""
    
    def render(self, atom: UnifiedAtomContainer) -> Dict:
        pos_2d = atom.get_position_2d()
        return {
            "type": "circle",
            "position_2d": pos_2d,
            "radius": atom.get_radius(),
            "color": atom.get_color(),
            "element": atom.element
        }


class ShellVisualizationRenderer(AtomRenderer):
    """Electron shell renderer (atom_visualization.py style)"""
    
    def render(self, atom: UnifiedAtomContainer) -> Dict:
        if not atom.electron_config:
            return {"type": "shell_visualization", "shells": []}
        
        shells_data = []
        for shell in atom.electron_config.shells:
            orbitals_data = []
            for orbital in shell.orbitals:
                orbitals_data.append({
                    "name": orbital.orbital_name,
                    "electrons": orbital.electrons_present,
                    "color": orbital.color()
                })
            shells_data.append({
                "shell_number": shell.shell_number,
                "radius": shell.orbital_radius(),
                "orbitals": orbitals_data
            })
        
        return {
            "type": "shell_visualization",
            "element": atom.element,
            "atomic_number": atom.electron_config.atomic_number,
            "shells": shells_data
        }


class FieldGaussianRenderer(AtomRenderer):
    """Field Gaussian renderer (field_gradient_visualization_system.py style)"""
    
    def render(self, atom: UnifiedAtomContainer) -> Dict:
        field_grid = atom.get_field_grid()
        return {
            "type": "field_gaussian",
            "grid": field_grid.compute_grid(),
            "regions": len(atom.field_regions),
            "element": atom.element,
            "position": atom.position_3d
        }


# ============================================================================
# FACTORY: Create unified atoms in various ways
# ============================================================================

class UnifiedAtomFactory:
    """Factory for creating unified atoms from different sources"""
    
    @staticmethod
    def from_simple_dict(atom_dict: Dict[str, Any]) -> UnifiedAtomContainer:
        """From simple optimized_molecule_animation_generator.py format"""
        return UnifiedAtomContainer(
            atom_id=f"{atom_dict['element']}_0",
            element=atom_dict['element'],
            position_3d=atom_dict['position']
        )
    
    @staticmethod
    def from_molecule_visualization(element: str, x: float, y: float, z: float = 0) -> UnifiedAtomContainer:
        """From molecule_visualization.py format"""
        return UnifiedAtomContainer(
            atom_id=f"{element}_{hash((x, y, z))}",
            element=element,
            position_3d=(x, y, z)
        )
    
    @staticmethod
    def with_electron_config(element: str, atomic_number: int, 
                             position: Tuple[float, float, float]) -> UnifiedAtomContainer:
        """With full electron configuration"""
        atom = UnifiedAtomContainer(
            atom_id=f"{element}_{atomic_number}",
            element=element,
            position_3d=position,
            electron_config=ElectronConfiguration.generate_configuration(atomic_number)
        )
        return atom
    
    @staticmethod
    def with_field_regions(atom: UnifiedAtomContainer, num_regions: int = 1,
                           sigma: float = 30) -> UnifiedAtomContainer:
        """Add Gaussian field regions"""
        pos_2d = atom.get_position_2d()
        for i in range(num_regions):
            angle = (i / num_regions) * 2 * math.pi
            offset_x = math.cos(angle) * 20
            offset_y = math.sin(angle) * 20
            atom.add_field_region(
                atom.element,
                (pos_2d[0] + offset_x, pos_2d[1] + offset_y),
                concentration=1.0 / num_regions,
                sigma=sigma
            )
        return atom


# ============================================================================
# EXAMPLE USAGE & TESTING
# ============================================================================

def create_water_molecule_unified() -> UnifiedMoleculeContainer:
    """Create H₂O using unified container model"""
    molecule = UnifiedMoleculeContainer("water_1", "Water (H₂O)")
    
    # Create atoms with full electron configurations and field regions
    oxygen = UnifiedAtomFactory.with_electron_config("O", 8, (0.0, 0.0, 0.0))
    UnifiedAtomFactory.with_field_regions(oxygen, num_regions=3)
    
    h1 = UnifiedAtomFactory.with_electron_config("H", 1, (0.96, 0.0, 0.0))
    UnifiedAtomFactory.with_field_regions(h1, num_regions=1)
    
    h2 = UnifiedAtomFactory.with_electron_config("H", 1, (-0.24, 0.93, 0.0))
    UnifiedAtomFactory.with_field_regions(h2, num_regions=1)
    
    # Add to molecule
    molecule.add_atom(oxygen)
    molecule.add_atom(h1)
    molecule.add_atom(h2)
    
    # Add bonds
    molecule.add_bond(oxygen.atom_id, h1.atom_id, 1.0)
    molecule.add_bond(oxygen.atom_id, h2.atom_id, 1.0)
    
    # Verify all primitives
    print(f"Unified Water Molecule: {molecule.get_formula()}")
    print(f"All atoms verified: {molecule.verify_all_atoms()}")
    
    for atom_id, atom in molecule.atoms.items():
        primitives_ok, results = atom.verify_all_primitives()
        print(f"  {atom.element}: {primitives_ok} → {results}")
    
    return molecule


if __name__ == "__main__":
    print("="*80)
    print("UNIFIED ATOM CONTAINER MODEL")
    print("="*80)
    
    # Test unified model
    water = create_water_molecule_unified()
    print(f"\nFormula: {water.get_formula()}")
    print(f"Atoms: {len(water.atoms)}")
    print(f"Bonds: {len(water.bonds)}")
    
    # Test different renderers
    print("\n" + "="*80)
    print("RENDERING EXAMPLES")
    print("="*80)
    
    for atom_id, atom in water.atoms.items():
        print(f"\n{atom.element} ({atom_id}):")
        
        # Point renderer
        point_render = PointRenderer()
        print(f"  Point: {point_render.render(atom)}")
        
        # Circle renderer
        circle_render = CircleRenderer()
        print(f"  Circle: {circle_render.render(atom)}")
        
        # Shell renderer
        if atom.electron_config:
            shell_render = ShellVisualizationRenderer()
            shell_data = shell_render.render(atom)
            print(f"  Shells: {len(shell_data['shells'])} shells")
        
        # Field renderer
        if atom.field_regions:
            field_render = FieldGaussianRenderer()
            field_data = field_render.render(atom)
            print(f"  Field: {field_data['regions']} regions")
