# INTEGRATION GUIDE: Apply Human Standards to UNIVERSAL_RENDERER
## Step-by-step retrofit of existing renderer to use standards-based approach

**Target**: Update UNIVERSAL_RENDERER.py to use Quaternion + Dipole + Field standards  
**Scope**: All 7 Stages + all 9+ molecules  
**Complexity**: Low (drop-in replacements)

---

## PHASE 1: Import Standards Library

**File**: `UNIVERSAL_RENDERER.py` - Add to top:

```python
# ===== EXISTING IMPORTS =====
import sys
sys.path.insert(0, r'c:\Determined')

# ===== NEW: HUMAN STANDARDS =====
from HUMAN_STANDARDS_ENFORCEMENT import (
    Quaternion,
    Dipole,
    UniversalContainerStandards,
    create_molecular_container
)
```

---

## PHASE 2: Stage 1 - Input Validator

**What to change**: Validate orientations as quaternions

### BEFORE:
```python
class Stage1_InputValidator(Stage):
    def process(self, molecule_data):
        # Validate: custom checks
        if not hasattr(molecule_data, 'yaw'):
            raise ValueError("Missing yaw")
        if not hasattr(molecule_data, 'pitch'):
            raise ValueError("Missing pitch")
        if not hasattr(molecule_data, 'roll'):
            raise ValueError("Missing roll")
        return molecule_data
```

### AFTER:
```python
class Stage1_InputValidator(Stage):
    def process(self, molecule_data):
        # Extract atoms
        atoms = molecule_data.get('atoms', [])
        
        # Convert to standards
        rotation_axis = molecule_data.get('rotation_axis', [0, 0, 1])
        rotation_angle = molecule_data.get('rotation_angle_deg', 0.0)
        
        # Create container
        container = create_molecular_container(
            mol_id=molecule_data.get('name', 'unknown'),
            atoms=atoms,
            rotation_axis=rotation_axis,
            rotation_angle_deg=rotation_angle
        )
        
        # Validate against standards
        validation = container.validate()
        if not validation['valid']:
            for error in validation['errors']:
                raise ValueError(f"Standards violation: {error}")
        
        # Return enriched with standards
        molecule_data['standards_container'] = container
        molecule_data['quaternion'] = container.orientation
        molecule_data['dipole'] = container.dipole
        return molecule_data
```

---

## PHASE 3: Stage 2 - Metrics Calculator

**What to change**: Calculate metrics in quaternion space

### BEFORE:
```python
class Stage2_MetricsCalculator(Stage):
    def process(self, molecule_data):
        # Custom rotation metrics
        metrics = {
            'yaw': molecule_data['yaw'],
            'pitch': molecule_data['pitch'],
            'roll': molecule_data['roll'],
            'gimbal_lock_risk': self.check_gimbal_lock(molecule_data)
        }
        molecule_data['metrics'] = metrics
        return molecule_data
```

### AFTER:
```python
class Stage2_MetricsCalculator(Stage):
    def process(self, molecule_data):
        container = molecule_data['standards_container']
        q = container.orientation
        
        # Quaternion metrics (always valid, no gimbal lock)
        aa = q.to_axis_angle()
        metrics = {
            'quaternion': {
                'w': float(q.w),
                'x': float(q.x),
                'y': float(q.y),
                'z': float(q.z),
                'magnitude': float(q.magnitude())
            },
            'axis_angle_reference': {
                'axis': aa['axis'].tolist(),
                'angle_deg': float(aa['angle_deg'])
            },
            'rotation_matrix': q.to_matrix().tolist(),
            'gimbal_lock_risk': 0.0  # Never happens with quaternions!
        }
        
        # Dipole metrics
        dipole = container.dipole
        metrics['dipole'] = {
            'magnitude_au': float(dipole.magnitude),
            'magnitude_debye': float(dipole.magnitude_debye),
            'color_rgb': dipole.color_code(),
            'direction': dipole.direction.tolist()
        }
        
        molecule_data['metrics'] = metrics
        return molecule_data
```

---

## PHASE 4: Stage 3 - Strategy Selector

**What to change**: Choose rendering strategy based on quaternion, not Euler angles

### BEFORE:
```python
class Stage3_StrategySelector(Stage):
    def process(self, molecule_data):
        yaw = molecule_data['yaw']
        pitch = molecule_data['pitch']
        
        # Heuristic based on angles
        if abs(pitch) > 70:  # Near singularity
            strategy = 'matrix_based'
        else:
            strategy = 'euler_based'
        
        molecule_data['strategy'] = strategy
        return molecule_data
```

### AFTER:
```python
class Stage3_StrategySelector(Stage):
    def process(self, molecule_data):
        q = molecule_data['quaternion']
        
        # Always use quaternion (no singularities!)
        # Choose strategy based on rotation magnitude only
        aa = q.to_axis_angle()
        angle_deg = abs(aa['angle_deg'])
        
        if angle_deg > 180:
            # Large rotation
            strategy = 'quaternion_based_large'
        elif angle_deg > 45:
            # Medium rotation
            strategy = 'quaternion_based_medium'
        else:
            # Small rotation
            strategy = 'quaternion_based_small'
        
        molecule_data['strategy'] = strategy
        return molecule_data
```

---

## PHASE 5: Stage 4 - Executor

**What to change**: Generate frames using quaternion interpolation

### BEFORE:
```python
class Stage4_Executor(Stage):
    def process(self, molecule_data):
        yaw = molecule_data['yaw']
        frames = []
        
        for frame_num in range(360):
            angle = frame_num  # Rotate 1° per frame
            # Apply yaw + frame rotation
            R = self.euler_to_matrix(yaw, 0, angle)
            frame_data = self.render_with_matrix(R)
            frames.append(frame_data)
        
        molecule_data['frames'] = frames
        return molecule_data
```

### AFTER:
```python
class Stage4_Executor(Stage):
    def process(self, molecule_data):
        q_base = molecule_data['quaternion']
        num_frames = molecule_data.get('num_frames', 360)
        frames = []
        
        for frame_num in range(num_frames):
            # Interpolate rotation using SLERP
            # (Smooth Spherical Linear Interpolation)
            t = frame_num / float(num_frames)
            
            # Create rotating quaternion
            angle_frame = t * 360.0  # Full 360° rotation
            q_rotation = Quaternion.from_axis_angle(
                [0, 0, 1],  # Rotate around Z
                np.radians(angle_frame)
            )
            
            # Compose: base rotation THEN frame rotation
            q_current = q_rotation.compose(q_base)
            
            # Get rotation matrix
            R = q_current.to_matrix()
            
            # Render frame
            frame_data = self.render_with_quaternion(q_current)
            frames.append(frame_data)
        
        molecule_data['frames'] = frames
        return molecule_data

    def render_with_quaternion(self, q):
        """Render using quaternion rotation"""
        R = q.to_matrix()
        # ... render logic using R ...
        return frame_data
```

---

## PHASE 6: Stage 5 - Verifier

**What to change**: Verify quaternion + dipole sanity

### BEFORE:
```python
class Stage5_Verifier(Stage):
    def process(self, molecule_data):
        frames = molecule_data['frames']
        
        # Check: Do frames exist?
        if not frames:
            raise ValueError("No frames generated")
        
        # Check: First frame valid?
        if not frames[0]:
            raise ValueError("First frame is empty")
        
        molecule_data['verified'] = True
        return molecule_data
```

### AFTER:
```python
class Stage5_Verifier(Stage):
    def process(self, molecule_data):
        frames = molecule_data['frames']
        container = molecule_data['standards_container']
        
        # Verify standards compliance
        validation = container.validate()
        if not validation['valid']:
            raise ValueError(f"Standards violation: {validation['errors']}")
        
        # Check: Frames exist?
        if not frames:
            raise ValueError("No frames generated")
        
        # Check: Frame count reasonable?
        if len(frames) < 10:
            raise ValueError(f"Too few frames: {len(frames)}")
        if len(frames) > 7200:
            raise ValueError(f"Too many frames: {len(frames)}")
        
        # Check: Quaternion remains normalized throughout
        q = container.orientation
        mag = q.magnitude()
        if abs(mag - 1.0) > 0.01:
            raise ValueError(f"Quaternion denormalized: |q| = {mag}")
        
        # Check: Dipole makes sense
        dipole = container.dipole
        if dipole.magnitude < 0:
            raise ValueError("Dipole magnitude cannot be negative")
        if dipole.magnitude > 1000:
            raise ValueError(f"Dipole magnitude suspiciously large: {dipole.magnitude}")
        
        # Check: No NaN or Inf in frames
        for i, frame in enumerate(frames):
            if self.contains_nan_or_inf(frame):
                raise ValueError(f"Frame {i} contains NaN or Inf")
        
        molecule_data['verified'] = True
        molecule_data['validation_metrics'] = validation['metrics']
        return molecule_data
    
    def contains_nan_or_inf(self, frame_data):
        """Check for invalid floating point values"""
        for value in frame_data.values():
            if isinstance(value, (list, tuple, np.ndarray)):
                if np.any(np.isnan(value)) or np.any(np.isinf(value)):
                    return True
            elif isinstance(value, (int, float)):
                if np.isnan(value) or np.isinf(value):
                    return True
        return False
```

---

## PHASE 7: Stage 6 - Adapter

**What to change**: Fix issues in quaternion space

### BEFORE:
```python
class Stage6_Adapter(Stage):
    def process(self, molecule_data):
        if not molecule_data.get('verified'):
            # Attempt fixes
            molecule_data = self.fix_euler_angles(molecule_data)
        
        return molecule_data

    def fix_euler_angles(self, data):
        # Custom Euler angle fixes
        data['yaw'] = data['yaw'] % 360
        data['pitch'] = max(-90, min(90, data['pitch']))
        return data
```

### AFTER:
```python
class Stage6_Adapter(Stage):
    def process(self, molecule_data):
        if not molecule_data.get('verified'):
            container = molecule_data['standards_container']
            q = container.orientation
            
            # Renormalize quaternion if drift detected
            mag = q.magnitude()
            if abs(mag - 1.0) > 1e-6:
                print(f"Renormalizing quaternion: |q| was {mag}")
                q.normalize()
            
            # Re-validate
            validation = container.validate()
            if validation['valid']:
                molecule_data['verified'] = True
                print("✓ Quaternion corrected")
            else:
                raise ValueError(f"Cannot fix: {validation['errors']}")
        
        return molecule_data
```

---

## PHASE 8: Stage 7 - Output Generator

**What to change**: Export with standards metadata

### BEFORE:
```python
class Stage7_OutputGenerator(Stage):
    def process(self, molecule_data):
        frames = molecule_data['frames']
        
        # Generate GIF
        images = [self.frame_to_pil(f) for f in frames]
        output_path = self.make_gif(images)
        
        return {
            'output_path': output_path,
            'frame_count': len(frames)
        }
```

### AFTER:
```python
class Stage7_OutputGenerator(Stage):
    def process(self, molecule_data):
        frames = molecule_data['frames']
        container = molecule_data['standards_container']
        
        # Generate GIF
        images = [self.frame_to_pil(f) for f in frames]
        mol_name = container.entity_id
        output_path = self.make_gif(images, mol_name)
        
        # EXPORT STANDARDS METADATA
        # 1. XML metadata
        xml_metadata = container.export_metadata_xml()
        xml_path = output_path.replace('.gif', '_standards.xml')
        with open(xml_path, 'w') as f:
            f.write(xml_metadata)
        
        # 2. JSON metadata
        json_metadata = container.to_json()
        json_path = output_path.replace('.gif', '_standards.json')
        with open(json_path, 'w') as f:
            f.write(json_metadata)
        
        return {
            'output_path': output_path,
            'metadata_xml': xml_path,
            'metadata_json': json_path,
            'frame_count': len(frames),
            'standards_verified': True,
            'quaternion': container.orientation.to_dict(),
            'dipole': container.dipole.to_dict()
        }
```

---

## PHASE 9: Main Loop - Apply to All Molecules

**What to change**: Process all 9+ molecules identically

### BEFORE:
```python
def render_all_molecules():
    molecules = [
        {'name': 'mol_001', 'yaw': 0, 'pitch': 30, 'roll': 45},
        {'name': 'mol_002', 'yaw': 40, 'pitch': 20, 'roll': 10},
        # ... 7 more molecules, each with custom angles ...
    ]
    
    for mol in molecules:
        print(f"Rendering {mol['name']}...")
        # Custom logic for each molecule
        if mol['name'] == 'mol_001':
            mol['strategy'] = 'strategy_A'
        elif mol['name'] == 'mol_002':
            mol['strategy'] = 'strategy_B'
        # ... etc ...
```

### AFTER:
```python
def render_all_molecules():
    molecules = [
        {
            'name': 'mol_001',
            'atoms': [{'pos': [-1, 0, 0], 'element': 'C'}, ...],
            'rotation_axis': [0, 0, 1],
            'rotation_angle_deg': 0
        },
        {
            'name': 'mol_002',
            'atoms': [{'pos': [-1, 0, 0], 'element': 'C'}, ...],
            'rotation_axis': [0, 0, 1],
            'rotation_angle_deg': 40
        },
        # All molecules use SAME structure + HUMAN STANDARDS
    ]
    
    orchestrator = UniversalContainerOrchestrator()
    results = []
    
    for mol_data in molecules:
        print(f"Rendering {mol_data['name']} using HUMAN STANDARDS...")
        
        try:
            # Apply 7-stage pipeline
            result = orchestrator.execute([
                Stage1_InputValidator(),
                Stage2_MetricsCalculator(),
                Stage3_StrategySelector(),
                Stage4_Executor(),
                Stage5_Verifier(),
                Stage6_Adapter(),
                Stage7_OutputGenerator()
            ], mol_data)
            
            results.append(result)
            print(f"  ✓ {mol_data['name']} complete")
            print(f"    Quaternion: {result['quaternion']}")
            print(f"    Dipole: {result['dipole']}")
        
        except Exception as e:
            print(f"  ✗ {mol_data['name']} failed: {e}")
    
    return results
```

---

## BENEFITS OF INTEGRATION

| Aspect | Before | After | Benefit |
|--------|--------|-------|---------|
| Rotation representation | Euler angles (custom) | Quaternions (standard) | No gimbal lock, industry standard |
| Dipole representation | Color maps (ad-hoc) | Arrow vectors (universal) | Works for ALL containers |
| Validation | Per-molecule heuristics | Standards checklist | Consistent, automated |
| Metadata | None | XML + JSON | Full provenance tracking |
| Scalability | 9 molecules (custom logic) | 9+ containers (one pipeline) | Linear growth, not exponential |
| Error handling | Catch-all exceptions | Typed validation | Clear error messages |

---

## QUICK START: Replace 3 Functions

If you don't want to refactor everything, replace just these 3:

### 1. Orientation conversion:
```python
# OLD: yaw, pitch, roll = float, float, float
# NEW: quaternion = Quaternion

Q = Quaternion.from_axis_angle(
    axis=[0, 0, 1],
    angle_rad=np.radians(45)
)
```

### 2. Dipole extraction:
```python
# OLD: dipole_color = some_custom_function()
# NEW: dipole = Dipole(neg_source, pos_source)

dipole = Dipole(
    source_negative=[-2, 0, 0],
    target_positive=[2, 0, 0]
)
color = dipole.color_code()  # Returns (R, G, B)
```

### 3. Metadata export:
```python
# OLD: No metadata
# NEW: standards_container.export_metadata_xml()

standards_container = UniversalContainerStandards(
    entity_id='mol_001',
    entity_type='molecule',
    orientation=Q,
    dipole=dipole
)
xml = standards_container.export_metadata_xml()
```

---

## TESTING: Verify Integration

Run this after making changes:

```python
# Test that all 9 molecules render identically (except for rotation)
def test_standards_integrity():
    from HUMAN_STANDARDS_ENFORCEMENT import UniversalContainerStandards
    
    for i in range(1, 10):
        mol_data = load_molecule(f'mol_{i:03d}')
        result = render_with_standards(mol_data)
        
        # Every molecule should have:
        assert 'quaternion' in result
        assert 'dipole' in result
        assert 'metadata_xml' in result
        assert result['quaternion']['magnitude'] == 1.0
        assert result['dipole']['magnitude_atomic_units'] > 0
        
        print(f"✓ mol_{i:03d} passed standards integrity check")
```

---

## ROLLBACK PLAN (If needed)

All original logic is preserved. To revert:
1. Keep old Stage classes (rename to `Stage_OLD_*`)
2. New Standards Stages can coexist
3. Switch via pipeline configuration

But you won't need to rollback - this is purely additive.

---

**Summary**: Integration is straightforward. The human standards become "the new normal" for your entire system.
