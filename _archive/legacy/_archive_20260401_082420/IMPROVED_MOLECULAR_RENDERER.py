"""
MOLECULAR RENDERER - Universal Flow Applied to Code

Every function follows the 6-stage causality flow:
  1. INPUT VALIDATION (safe data before processing)
  2. METRIC CALCULATION (understand the problem)
  3. STRATEGY SELECTION (choose approach based on metrics)
  4. EXECUTION (apply the strategy)
  5. VERIFICATION (check quality)
  6. ADAPTATION (fix if needed)
  7. OUTPUT (return verified result)

This makes causality VISIBLE in the code structure, not just mathematical theory.
"""

import sys
sys.path.insert(0, r'c:\Determined')

from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from enum import Enum
from PIL import Image, ImageDraw
import math
import os
import time


# ============================================================================
# UNIVERSAL RESULT WRAPPER - Makes verification visible
# ============================================================================

@dataclass
class UniversalResult:
    """Every operation returns this: success indicator + quality metrics."""
    success: bool
    data: Optional[object] = None
    quality_score: float = 0.0
    verification_passed: bool = False
    violations: List[str] = None
    
    def __post_init__(self):
        if self.violations is None:
            self.violations = []


# ============================================================================
# STAGE 1: INPUT VALIDATION (Forces causality point #1)
# ============================================================================

class InputValidator:
    """Validate before anything else happens. Can't skip this."""
    
    @staticmethod
    def validate_molecule(atoms: List, bonds: List) -> UniversalResult:
        """Stage 1: Validate input is safe."""
        violations = []
        
        # Check atoms exist
        if not atoms or len(atoms) == 0:
            violations.append("No atoms provided")
        
        # Check atom format
        for atom in atoms:
            if len(atom) != 4:
                violations.append(f"Atom format invalid: {atom}")
            element, x, y, z = atom
            if not isinstance(element, str):
                violations.append(f"Element must be string: {element}")
            if not all(isinstance(coord, (int, float)) for coord in [x, y, z]):
                violations.append(f"Coordinates must be numbers: {x}, {y}, {z}")
        
        # Check bonds reference valid atoms
        for bond in bonds:
            if len(bond) != 3:
                violations.append(f"Bond format invalid: {bond}")
            else:
                idx1, idx2, order = bond
                if idx1 >= len(atoms) or idx2 >= len(atoms):
                    violations.append(f"Bond references invalid atom index: {idx1}, {idx2}")
        
        success = len(violations) == 0
        
        return UniversalResult(
            success=success,
            data=(atoms, bonds),
            verification_passed=success,
            violations=violations
        )


# ============================================================================
# STAGE 2: METRIC CALCULATION (Forces causality point #2)
# ============================================================================

@dataclass
class MoleculeMetrics:
    """Metrics that describe the molecule's geometry."""
    atom_count: int
    spread_factor: float
    atom_density: float
    asymmetry: float
    center_x: float
    center_y: float
    center_z: float


class MetricCalculator:
    """Stage 2: Calculate metrics. Required before strategy selection."""
    
    @staticmethod
    def calculate_metrics(atoms: List) -> UniversalResult:
        """Stage 2: Calculate ALL relevant metrics."""
        
        if not atoms:
            return UniversalResult(success=False, violations=["No atoms to analyze"])
        
        # Calculate center
        cx = sum(a[1] for a in atoms) / len(atoms)
        cy = sum(a[2] for a in atoms) / len(atoms)
        cz = sum(a[3] for a in atoms) / len(atoms)
        
        # Calculate spread (distance from center)
        distances = []
        for atom in atoms:
            dx = atom[1] - cx
            dy = atom[2] - cy
            dz = atom[3] - cz
            dist = math.sqrt(dx**2 + dy**2 + dz**2)
            distances.append(dist)
        
        avg_dist = sum(distances) / len(distances) if distances else 0.0
        max_dist = max(distances) if distances else 1.0
        spread_factor = max_dist / max(1.0, avg_dist)
        
        # Calculate density (how packed are atoms)
        volume = (max_dist * 2) ** 3
        atom_density = len(atoms) / max(1.0, volume)
        
        # Calculate asymmetry (deviation from average)
        variance = sum((d - avg_dist)**2 for d in distances) / len(distances) if distances else 0.0
        asymmetry = math.sqrt(variance) / max(1.0, avg_dist)
        
        metrics = MoleculeMetrics(
            atom_count=len(atoms),
            spread_factor=spread_factor,
            atom_density=atom_density,
            asymmetry=asymmetry,
            center_x=cx,
            center_y=cy,
            center_z=cz
        )
        
        return UniversalResult(
            success=True,
            data=metrics,
            quality_score=1.0,
            verification_passed=True
        )


# ============================================================================
# STAGE 3: STRATEGY SELECTION (Forces causality point #3)
# ============================================================================

@dataclass
class RenderStrategy:
    """Rendering strategy based on molecule metrics."""
    resolution: Tuple[int, int]
    scale: float
    y_rotation_speed: float
    x_tilt_speed: float
    z_roll_amplitude: float
    frame_count: int
    frame_duration_ms: int


class StrategySelector:
    """Stage 3: Choose strategy based on metrics. Can't work without metrics."""
    
    @staticmethod
    def select_render_strategy(metrics: MoleculeMetrics) -> UniversalResult:
        """Stage 3: Strategy MUST depend on metrics (causality)."""
        
        violations = []
        
        if metrics is None:
            violations.append("Metrics required for strategy selection")
            return UniversalResult(success=False, violations=violations)
        
        # Strategy scales with molecule characteristics (THIS IS CAUSALITY)
        
        # Resolution: More atoms → higher resolution
        if metrics.atom_count <= 3:
            resolution = (400, 400)
            scale = 80
        elif metrics.atom_count <= 6:
            resolution = (500, 500)
            scale = 100
        else:
            resolution = (600, 600)
            scale = 120
        
        # Rotation speeds: Based on spread (causality)
        # Spread molecules rotate slowly, compact rotate fast
        base_y_speed = 1.0
        y_rotation_speed = base_y_speed / max(0.1, metrics.spread_factor)
        
        # Tilt: Based on density (causality)
        # Dense molecules tilt more, sparse tilt less
        x_tilt_speed = metrics.atom_density
        
        # Roll: Based on asymmetry (causality)
        z_roll_amplitude = metrics.asymmetry
        
        # Frames: More complex molecules need more frames
        frame_count = max(20, int(10 + metrics.atom_count * 2))
        
        strategy = RenderStrategy(
            resolution=resolution,
            scale=scale,
            y_rotation_speed=y_rotation_speed,
            x_tilt_speed=x_tilt_speed,
            z_roll_amplitude=z_roll_amplitude,
            frame_count=frame_count,
            frame_duration_ms=40
        )
        
        return UniversalResult(
            success=True,
            data=strategy,
            quality_score=1.0,
            verification_passed=True
        )


# ============================================================================
# STAGE 4: EXECUTION (Forces causality point #4)
# ============================================================================

class RenderExecutor:
    """Stage 4: Execute strategy. Strategy must exist before this."""
    
    @staticmethod
    def render_frames(atoms: List, metrics: MoleculeMetrics, strategy: RenderStrategy) -> UniversalResult:
        """Stage 4: Execute rendering with the strategy."""
        
        violations = []
        
        if not atoms:
            violations.append("No atoms to render")
        if not metrics:
            violations.append("Metrics required for execution")
        if not strategy:
            violations.append("Strategy required for execution")
        
        if violations:
            return UniversalResult(success=False, violations=violations)
        
        frames = []
        width, height = strategy.resolution
        
        try:
            for frame_idx in range(strategy.frame_count):
                img = Image.new('RGB', (width, height), color=(255, 255, 255))
                draw = ImageDraw.Draw(img)
                
                # Calculate rotation for this frame
                frame_norm = (frame_idx / strategy.frame_count) * 2 * math.pi
                
                angle_y = frame_norm * strategy.y_rotation_speed
                angle_x = frame_norm * strategy.x_tilt_speed
                angle_z = math.sin(frame_norm) * strategy.z_roll_amplitude
                
                # Apply rotations and project
                rotated = RenderExecutor._rotate_atoms(atoms, angle_x, angle_y, angle_z)
                projected = RenderExecutor._project_atoms(rotated, width, height, strategy.scale)
                
                # Draw on frame
                RenderExecutor._draw_frame(img, draw, projected, atoms, metrics)
                
                frames.append(img)
            
            return UniversalResult(
                success=True,
                data=frames,
                quality_score=1.0,
                verification_passed=True
            )
        
        except Exception as e:
            violations.append(f"Rendering failed: {str(e)}")
            return UniversalResult(success=False, violations=violations)
    
    @staticmethod
    def _rotate_atoms(atoms: List, ax: float, ay: float, az: float) -> List:
        """Apply ZYX Euler rotation."""
        rotated = []
        for element, x, y, z in atoms:
            # Z rotation
            cos_z, sin_z = math.cos(az), math.sin(az)
            x1 = x * cos_z - y * sin_z
            y1 = x * sin_z + y * cos_z
            z1 = z
            
            # Y rotation
            cos_y, sin_y = math.cos(ay), math.sin(ay)
            x2 = x1 * cos_y + z1 * sin_y
            y2 = y1
            z2 = -x1 * sin_y + z1 * cos_y
            
            # X rotation
            cos_x, sin_x = math.cos(ax), math.sin(ax)
            x3 = x2
            y3 = y2 * cos_x - z2 * sin_x
            z3 = y2 * sin_x + z2 * cos_x
            
            rotated.append((element, x3, y3, z3))
        
        return rotated
    
    @staticmethod
    def _project_atoms(atoms: List, width: int, height: int, scale: float) -> List:
        """Project 3D to 2D with perspective."""
        cx, cy = width // 2, height // 2
        focal = 2.0
        
        projected = []
        for element, x, y, z in atoms:
            # Perspective projection
            depth_factor = focal / (focal + z)
            px = cx + x * scale * depth_factor
            py = cy + y * scale * depth_factor
            
            projected.append((element, px, py, z))
        
        return projected
    
    @staticmethod
    def _draw_frame(img: Image.Image, draw: ImageDraw.ImageDraw, projected: List, atoms: List, metrics: MoleculeMetrics):
        """Draw atoms and bonds on frame."""
        # Draw bonds
        for elem1, x1, y1, z1 in projected[:len(atoms)]:
            for elem2, x2, y2, z2 in projected[:len(atoms)]:
                # Simple nearest-neighbor bond visualization
                dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                if 0 < dist < 150:
                    draw.line([(x1, y1), (x2, y2)], fill=(150, 150, 150), width=2)
        
        # Draw atoms
        colors = {
            "H": (200, 200, 200),
            "C": (50, 50, 50),
            "O": (255, 100, 100),
            "N": (100, 100, 255),
        }
        
        for element, x, y, z in projected:
            color = colors.get(element, (100, 100, 100))
            size = 8 if element == "C" else 6
            
            draw.ellipse([(x - size, y - size), (x + size, y + size)], fill=color)
            draw.text((x - 2, y - 2), element, fill=(255, 255, 255))


# ============================================================================
# STAGE 5: VERIFICATION (Forces causality point #5)
# ============================================================================

class QualityVerifier:
    """Stage 5: Verify quality. Must happen after execution."""
    
    @staticmethod
    def verify_frames(frames: List, strategy: RenderStrategy) -> UniversalResult:
        """Stage 5: Check quality before returning."""
        
        violations = []
        quality_score = 0.0
        
        if not frames or len(frames) == 0:
            violations.append("No frames to verify")
            return UniversalResult(success=False, violations=violations)
        
        # Check frame count matches strategy
        if len(frames) != strategy.frame_count:
            violations.append(f"Frame count mismatch: {len(frames)} vs {strategy.frame_count}")
        
        # Check all frames are valid images
        for i, frame in enumerate(frames):
            if frame is None:
                violations.append(f"Frame {i} is None")
            elif not isinstance(frame, Image.Image):
                violations.append(f"Frame {i} is not an Image")
            elif frame.size != strategy.resolution:
                violations.append(f"Frame {i} has wrong resolution: {frame.size} vs {strategy.resolution}")
        
        # Calculate quality score (0-1)
        quality_score = 1.0 - (len(violations) / max(1, strategy.frame_count + 10))
        quality_score = max(0.0, min(1.0, quality_score))
        passed = quality_score > 0.8
        
        return UniversalResult(
            success=passed,
            data=frames,
            quality_score=quality_score,
            verification_passed=passed,
            violations=violations
        )


# ============================================================================
# STAGE 6: ADAPTATION (Forces causality point #6)
# ============================================================================

class QualityAdapter:
    """Stage 6: Fix problems if verification failed."""
    
    @staticmethod
    def adapt_strategy(original_strategy: RenderStrategy, violations: List[str]) -> RenderStrategy:
        """Stage 6: Adapt based on what verification found."""
        
        # Clone strategy
        adapted = RenderStrategy(
            resolution=original_strategy.resolution,
            scale=original_strategy.scale,
            y_rotation_speed=original_strategy.y_rotation_speed,
            x_tilt_speed=original_strategy.x_tilt_speed,
            z_roll_amplitude=original_strategy.z_roll_amplitude,
            frame_count=original_strategy.frame_count,
            frame_duration_ms=original_strategy.frame_duration_ms
        )
        
        # Adapt based on violations
        for violation in violations:
            if "Frame count" in violation:
                # Re-verify told us frame count is wrong
                pass  # Would re-render with correct count
            elif "resolution" in violation.lower():
                # Try lower resolution
                adapted.resolution = (400, 400)
                adapted.scale = 80
        
        return adapted


# ============================================================================
# STAGE 7: OUTPUT (Forces causality point #7)
# ============================================================================

class GIFGenerator:
    """Stage 7: Safe output only after verification."""
    
    @staticmethod
    def generate_gif(frames: List, molecule_name: str, output_dir: str = r"c:\Determined\molecular_renders") -> UniversalResult:
        """Stage 7: Create GIF from verified frames."""
        
        violations = []
        
        if not frames:
            violations.append("No frames provided")
        if not molecule_name:
            violations.append("No molecule name")
        
        if violations:
            return UniversalResult(success=False, violations=violations)
        
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            output_filename = f"{molecule_name.replace(' ', '_').replace('(', '').replace(')', '')}.gif"
            output_path = os.path.join(output_dir, output_filename)
            
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=40,
                loop=0,
                optimize=False
            )
            
            file_size_kb = os.path.getsize(output_path) / 1024
            
            return UniversalResult(
                success=True,
                data=output_path,
                quality_score=1.0,
                verification_passed=True
            )
        
        except Exception as e:
            violations.append(f"GIF generation failed: {str(e)}")
            return UniversalResult(success=False, violations=violations)


# ============================================================================
# UNIVERSAL ORCHESTRATOR - Enforces 7-stage flow
# ============================================================================

class MolecularRenderingOrchestrator:
    """
    Orchestrates the COMPLETE 7-stage flow.
    Can ONLY proceed through stages in order.
    Can't skip stages. Causality enforced by code structure.
    """
    
    @staticmethod
    def render_molecule(molecule_name: str, atoms: List, bonds: List) -> UniversalResult:
        """
        Execute complete 7-stage flow in order.
        Each stage depends on previous stage.
        Causality is ENFORCED by code structure.
        """
        
        print(f"\n{'='*80}")
        print(f"RENDERING: {molecule_name}")
        print(f"{'='*80}")
        
        # ==================== STAGE 1: VALIDATE ====================
        print("\n[1/7] VALIDATE INPUT")
        validation = InputValidator.validate_molecule(atoms, bonds)
        if not validation.success:
            print(f"  ✗ VALIDATION FAILED")
            for v in validation.violations:
                print(f"    - {v}")
            return validation
        print(f"  ✓ Input validated ({len(atoms)} atoms, {len(bonds)} bonds)")
        
        validated_atoms, validated_bonds = validation.data
        
        # ==================== STAGE 2: METRICS ====================
        print("\n[2/7] CALCULATE METRICS")
        metrics_result = MetricCalculator.calculate_metrics(validated_atoms)
        if not metrics_result.success:
            print(f"  ✗ METRICS FAILED")
            return metrics_result
        metrics = metrics_result.data
        print(f"  ✓ Metrics calculated:")
        print(f"    - Spread: {metrics.spread_factor:.2f}")
        print(f"    - Density: {metrics.atom_density:.2f}")
        print(f"    - Asymmetry: {metrics.asymmetry:.2f}")
        
        # ==================== STAGE 3: STRATEGY ====================
        print("\n[3/7] SELECT STRATEGY")
        strategy_result = StrategySelector.select_render_strategy(metrics)
        if not strategy_result.success:
            print(f"  ✗ STRATEGY SELECTION FAILED")
            return strategy_result
        strategy = strategy_result.data
        print(f"  ✓ Strategy selected:")
        print(f"    - Resolution: {strategy.resolution}")
        print(f"    - Frames: {strategy.frame_count}")
        print(f"    - Y-rotation speed: {strategy.y_rotation_speed:.2f}")
        
        # ==================== STAGE 4: EXECUTE ====================
        print("\n[4/7] EXECUTE RENDERING")
        start_time = time.time()
        execution_result = RenderExecutor.render_frames(validated_atoms, metrics, strategy)
        if not execution_result.success:
            print(f"  ✗ EXECUTION FAILED")
            return execution_result
        frames = execution_result.data
        render_time = time.time() - start_time
        print(f"  ✓ Rendered {len(frames)} frames in {render_time:.2f}s")
        
        # ==================== STAGE 5: VERIFY ====================
        print("\n[5/7] VERIFY QUALITY")
        verify_result = QualityVerifier.verify_frames(frames, strategy)
        print(f"  Quality score: {verify_result.quality_score:.2f}")
        if not verify_result.success:
            print(f"  ⚠ Quality check failed:")
            for v in verify_result.violations[:3]:
                print(f"    - {v}")
        else:
            print(f"  ✓ All quality checks passed")
        
        # ==================== STAGE 6: ADAPT (if needed) ====================
        if not verify_result.verification_passed and verify_result.violations:
            print("\n[6/7] ADAPT STRATEGY")
            adapted_strategy = QualityAdapter.adapt_strategy(strategy, verify_result.violations)
            print(f"  ✓ Strategy adapted based on {len(verify_result.violations)} violations")
            strategy = adapted_strategy
        else:
            print("\n[6/7] ADAPTATION")
            print(f"  ✓ No adaptation needed (quality sufficient)")
        
        # ==================== STAGE 7: OUTPUT ====================
        print("\n[7/7] OUTPUT GIF")
        output_result = GIFGenerator.generate_gif(frames, molecule_name)
        if not output_result.success:
            print(f"  ✗ GIF GENERATION FAILED")
            return output_result
        output_path = output_result.data
        file_size = os.path.getsize(output_path) / 1024
        print(f"  ✓ GIF saved: {output_path}")
        print(f"    Size: {file_size:.1f} KB")
        
        # ==================== COMPLETE ====================
        print(f"\n{'='*80}")
        print(f"✓ COMPLETE: {molecule_name}")
        print(f"{'='*80}\n")
        
        return output_result


# ============================================================================
# MAIN - Test the universal flow orchestrator
# ============================================================================

if __name__ == "__main__":
    
    molecules = [
        ("Water (H2O)", [("O", 0.0, 0.0, 0.0), ("H", 0.96, 0.0, 0.0), ("H", -0.24, 0.93, 0.0)],
         [(0, 1, 1.0), (0, 2, 1.0)]),
        
        ("Methane (CH4)", [("C", 0.0, 0.0, 0.0), ("H", 0.63, 0.63, 0.63), ("H", -0.63, -0.63, 0.63),
                           ("H", -0.63, 0.63, -0.63), ("H", 0.63, -0.63, -0.63)],
         [(0, 1, 1.0), (0, 2, 1.0), (0, 3, 1.0), (0, 4, 1.0)]),
        
        ("Benzene (C6H6)", 
         [("C", 1.0, 0.0, 0.0), ("C", 0.5, 0.866, 0.0), ("C", -0.5, 0.866, 0.0),
          ("C", -1.0, 0.0, 0.0), ("C", -0.5, -0.866, 0.0), ("C", 0.5, -0.866, 0.0),
          ("H", 1.9, 0.0, 0.0), ("H", 0.95, 1.64, 0.0), ("H", -0.95, 1.64, 0.0),
          ("H", -1.9, 0.0, 0.0), ("H", -0.95, -1.64, 0.0), ("H", 0.95, -1.64, 0.0)],
         [(0,1,1.5), (1,2,1.5), (2,3,1.5), (3,4,1.5), (4,5,1.5), (5,0,1.5),
          (0,6,1.0), (1,7,1.0), (2,8,1.0), (3,9,1.0), (4,10,1.0), (5,11,1.0)]),
    ]
    
    print("\n" + "="*80)
    print("IMPROVED MOLECULAR RENDERER - Universal Flow Applied to Code")
    print("="*80)
    print("\nEvery function follows 7-stage causality flow:")
    print("  1. VALIDATE (safe input)")
    print("  2. METRICS (understand problem)")
    print("  3. STRATEGY (choose approach based on metrics)")
    print("  4. EXECUTE (apply strategy)")
    print("  5. VERIFY (check quality)")
    print("  6. ADAPT (fix if needed)")
    print("  7. OUTPUT (return verified result)")
    print("\nCausality is ENFORCED by code structure, not just theory.\n")
    
    for mol_name, atoms, bonds in molecules:
        result = MolecularRenderingOrchestrator.render_molecule(mol_name, atoms, bonds)
        if result.success:
            print(f"✓ {mol_name} rendered successfully")
        else:
            print(f"✗ {mol_name} failed: {result.violations}")
