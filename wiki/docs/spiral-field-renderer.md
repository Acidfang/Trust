# Constraint-Determined Spiral Field Renderer: Full Bidirectional Reality

## The Bowling Ball Principle

You CAN choose an object's center—if you engineer the right constraints. This renderer demonstrates both directions:

1. **Forward (Analysis)**: Define constraints → system computes where center MUST be
2. **Backward (Design)**: Choose where you want center → system solves for required constraints

Like a bowling ball with offset weight distribution: you design the internal structure (constraints) to achieve external positioning (center location). Both perspectives are equally real.

<div id="constraintControls" style="background: #0a0e27; border: 2px solid #00d9ff; border-radius: 8px; padding: 20px; margin: 20px 0; color: #00ff88; font-family: monospace;">
  <div style="margin-bottom: 20px; padding: 10px; background: #1a1e37; border-left: 3px solid #ff6600;">
    <h3 style="color: #ff6600; margin-top: 0;">🎯 View Modes</h3>
    <div style="margin-bottom: 10px;">
      <button id="topDownView" style="padding: 6px 12px; margin-right: 8px; background: #00d9ff; color: #000; border: none; cursor: pointer; font-weight: bold; border-radius: 4px;">↓ Top-Down (External View)</button>
      <button id="fromCenterView" style="padding: 6px 12px; margin-right: 8px; background: #444; color: #00ff88; border: 2px solid #00ff88; cursor: pointer; border-radius: 4px;">⊙ From Center (Internal View)</button>
    </div>
    <p style="color: #888; margin: 8px 0; font-size: 12px;">Same spiral, same constraints—two completely different viewpoints</p>
  </div>

  <div style="margin-bottom: 20px; padding: 10px; background: #1a1e37; border-left: 3px solid #ff6600;">
    <h3 style="color: #ff6600; margin-top: 0;">🎯 Design Mode</h3>
    <label><input type="checkbox" id="designMode"> Enable Design Mode (click 3D view to set desired centers)</label>
    <p style="margin: 10px 0; color: #888;">In design mode: choose where you want centers → solver derives required constraints</p>
  </div>

  <div style="margin-bottom: 20px;">
    <h3 style="color: #00d9ff; margin-top: 0;">Object 1 - Cyan</h3>
    <div style="background: #0f1632; padding: 10px; border-radius: 4px;">
      <div style="margin-bottom: 8px;">
        <strong>Constraints (Interior Structure):</strong>
      </div>
      <label>Precession Axis X: <input type="range" id="obj1_precX" min="-1" max="1" step="0.1" value="0" style="width: 80px;"> <span id="obj1_precX_val">0</span></label><br>
      <label>Precession Axis Y: <input type="range" id="obj1_precY" min="-1" max="1" step="0.1" value="1" style="width: 80px;"> <span id="obj1_precY_val">1</span></label><br>
      <label>Precession Axis Z: <input type="range" id="obj1_precZ" min="-1" max="1" step="0.1" value="0" style="width: 80px;"> <span id="obj1_precZ_val">0</span></label><br>
      <label>Phase Offset: <input type="range" id="obj1_phase" min="0" max="6.28" step="0.1" value="0" style="width: 80px;"> <span id="obj1_phase_val">0</span></label><br>
      <label>Coupling Strength: <input type="range" id="obj1_coupling" min="0.1" max="1" step="0.1" value="0.7" style="width: 80px;"> <span id="obj1_coupling_val">0.7</span></label>
      <div style="margin-top: 8px; padding: 8px; background: #000; border-left: 2px solid #00d9ff;">
        <strong>Computed Center:</strong> <span id="obj1_center_display">loading...</span>
      </div>
    </div>
  </div>


</div>

<div id="spiralFieldContainer" style="width: 100%; height: 600px; background: #0a0e27; border-radius: 8px; overflow: hidden; position: relative; margin: 20px 0;"></div>

### System Architecture

Three core concepts working together:

1. **Object Centers** - Points in space to be understood
2. **Spiral Scans** - Precession-based detection paths around each center
3. **Coherence Detection** - Finding where multiple spirals resonate

<script src="https://unpkg.com/three@0.160.0/build/three.min.js"></script>
<script>
class ConstraintSolver {
    // FORWARD: Constraints → Center Position
    static solveCenter(constraints) {
        const {precessionAxis, phaseOffset, couplingStrength} = constraints;
        
        // Normalize precession axis
        const len = Math.sqrt(
            precessionAxis.x * precessionAxis.x + 
            precessionAxis.y * precessionAxis.y + 
            precessionAxis.z * precessionAxis.z
        );
        
        const normAxis = {
            x: precessionAxis.x / (len || 1),
            y: precessionAxis.y / (len || 1),
            z: precessionAxis.z / (len || 1)
        };
        
        // Center position along precession axis, distance = coupling strength
        const distance = 200 * couplingStrength;
        
        return new THREE.Vector3(
            normAxis.x * distance,
            normAxis.y * distance,
            normAxis.z * distance
        );
    }
    
    // BACKWARD: Desired Center → Required Constraints
    // This demonstrates the bowling ball principle: engineer the constraints to achieve desired geometry
    static solveConstraints(desiredCenter, currentConstraints = null) {
        // Calculate required precession axis direction
        const distance = desiredCenter.length(); // Distance from origin
        const couplingStrength = Math.min(1.0, distance / 200); // Scale back from 200 unit range
        
        // Normalize to get axis direction
        const axisLen = Math.max(0.1, distance);
        const precessionAxis = {
            x: desiredCenter.x / axisLen,
            y: desiredCenter.y / axisLen,
            z: desiredCenter.z / axisLen
        };
        
        // Keep phase offset stable (can interpolate from current if available)
        const phaseOffset = currentConstraints?.phaseOffset || Math.random() * 6.28;
        
        return {
            precessionAxis,
            phaseOffset,
            couplingStrength: Math.max(0.1, couplingStrength)
        };
    }
    
    // Compute reachability: what points can be reached with given constraints?
    static computeReachablePoints(constraints, sampleCount = 100) {
        const center = this.solveCenter(constraints);
        const coupling = constraints.couplingStrength;
        const maxRadius = 200 * coupling * 0.5; // Spiral scan radius is half of distance
        
        return {center, maxRadius};
    }
}

class SpiralScanGenerator {
    constructor(centerPos, constraints, scanRadius = 300, scanHeights = 8, pointsPerTurn = 100) {
        this.centerPos = centerPos;
        this.constraints = constraints;
        this.scanRadius = scanRadius;
        this.scanHeights = scanHeights;
        this.pointsPerTurn = pointsPerTurn;
        this.goldenAngle = 2.399963229728653;
    }
    
    generate() {
        const points = [];
        const totalTurns = this.scanHeights;
        const totalPoints = totalTurns * this.pointsPerTurn;
        
        for (let i = 0; i < totalPoints; i++) {
            const t = i / totalPoints;
            
            const y = (t * 2 - 1) * this.scanRadius;
            const radiusPhase = Math.sin(t * Math.PI);
            const r = this.scanRadius * radiusPhase;
            
            const angle = this.goldenAngle * i + this.constraints.phaseOffset;
            
            const x = Math.cos(angle) * r;
            const z = Math.sin(angle) * r;
            
            points.push(new THREE.Vector3(
                this.centerPos.x + x,
                this.centerPos.y + y,
                this.centerPos.z + z
            ));
        }
        
        return new Float32Array(points.flatMap(p => [p.x, p.y, p.z]));
    }
    
    generateCurve() {
        return this.generate();
    }
}

class CoherenceDetector {
    constructor(samplePoints = 1000) {
        this.samplePoints = samplePoints;
    }
    
    computeCoherence(point, spiralGenerators) {
        if (spiralGenerators.length === 0) return 0;
        if (spiralGenerators.length === 1) return 1;
        
        let phasesX = [];
        let phasesY = [];
        let phasesZ = [];
        
        for (let gen of spiralGenerators) {
            const dx = point.x - gen.centerPos.x;
            const dy = point.y - gen.centerPos.y;
            const dz = point.z - gen.centerPos.z;
            
            const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
            const angle = Math.atan2(dz, dx);
            
            const {precessionAxis} = gen.constraints;
            const axisInfluence = (
                precessionAxis.x * dx + 
                precessionAxis.y * dy + 
                precessionAxis.z * dz
            ) / (distance || 1);
            
            phasesX.push(Math.cos(angle) * (1 + axisInfluence * 0.5));
            phasesY.push(Math.cos(dy / gen.scanRadius * Math.PI));
            phasesZ.push(Math.sin(angle) * (1 + axisInfluence * 0.5));
        }
        
        let sumX = phasesX.reduce((a, b) => a + b, 0);
        let sumY = phasesY.reduce((a, b) => a + b, 0);
        let sumZ = phasesZ.reduce((a, b) => a + b, 0);
        
        const magnitude = Math.sqrt(sumX * sumX + sumY * sumY + sumZ * sumZ);
        const coherence = magnitude / spiralGenerators.length;
        
        return Math.max(0, Math.min(1, coherence));
    }
    
    generateCoherenceField(spiralGenerators, gridSize = 15) {
        const field = [];
        const spacing = 400 / gridSize;
        
        for (let x = -200; x < 200; x += spacing) {
            for (let y = -200; y < 200; y += spacing) {
                for (let z = -200; z < 200; z += spacing) {
                    const point = new THREE.Vector3(x, y, z);
                    const coherence = this.computeCoherence(point, spiralGenerators);
                    field.push({point, coherence});
                }
            }
        }
        
        return field;
    }
}

class BidirectionalConstraintApp {
    constructor() {
        this.container = document.getElementById('spiralFieldContainer');
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x0a0e27);
        
        this.camera = new THREE.PerspectiveCamera(
            75,
            this.container.clientWidth / this.container.clientHeight,
            0.1,
            10000
        );
        this.camera.position.set(400, 300, 400);
        this.camera.lookAt(0, 0, 0);
        
        this.renderer = new THREE.WebGLRenderer({antialias: true, alpha: false});
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.container.appendChild(this.renderer.domElement);
        
        const ambientLight = new THREE.AmbientLight(0x00ff88, 0.4);
        this.scene.add(ambientLight);
        
        const pointLight = new THREE.PointLight(0x00d9ff, 0.8);
        pointLight.position.set(300, 300, 300);
        this.scene.add(pointLight);
        
        this.objects = [
            {constraints: null, centerMesh: null, color: 0x00d9ff}
        ];
        
        this.designMode = false;
        this.designTargets = [null]; // Desired centers in design mode
        this.designIndicators = [null]; // Visual indicators for desired centers
        
        this.viewMode = 'topdown'; // 'topdown' or 'fromCenter'
        this.internalViewCenterIndex = 0; // Which center to look from in internal view
        
        this.spiralMeshes = [];
        this.coherenceParticles = null;
        this.coherenceDetector = new CoherenceDetector();
        
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();
        
        this.init();
        this.setupListeners();
        this.animate();
    }
    
    readConstraints() {
        return [
            {
                precessionAxis: {
                    x: parseFloat(document.getElementById('obj1_precX').value),
                    y: parseFloat(document.getElementById('obj1_precY').value),
                    z: parseFloat(document.getElementById('obj1_precZ').value)
                },
                phaseOffset: parseFloat(document.getElementById('obj1_phase').value),
                couplingStrength: parseFloat(document.getElementById('obj1_coupling').value)
            }
        ];
    }
    
    setConstraints(index, constraints) {
        // Update UI sliders from constraint values
        const prefix = `obj${index + 1}`;
        document.getElementById(`${prefix}_precX`).value = constraints.precessionAxis.x.toFixed(2);
        document.getElementById(`${prefix}_precY`).value = constraints.precessionAxis.y.toFixed(2);
        document.getElementById(`${prefix}_precZ`).value = constraints.precessionAxis.z.toFixed(2);
        document.getElementById(`${prefix}_phase`).value = constraints.phaseOffset.toFixed(2);
        document.getElementById(`${prefix}_coupling`).value = constraints.couplingStrength.toFixed(2);
        
        this.update();
    }
    
    init() {
        this.update();
    }
    
    update() {
        const constraintsList = this.readConstraints();
        
        // Update displays
        for (let i = 0; i < 1; i++) {
            const c = constraintsList[i];
            const objNum = i + 1;
            const prefix = `obj${objNum}`;
            
            document.getElementById(`${prefix}_precX_val`).textContent = c.precessionAxis.x.toFixed(2);
            document.getElementById(`${prefix}_precY_val`).textContent = c.precessionAxis.y.toFixed(2);
            document.getElementById(`${prefix}_precZ_val`).textContent = c.precessionAxis.z.toFixed(2);
            document.getElementById(`${prefix}_phase_val`).textContent = c.phaseOffset.toFixed(2);
            document.getElementById(`${prefix}_coupling_val`).textContent = c.couplingStrength.toFixed(2);
            
            this.objects[i].constraints = c;
            
            // Display computed center
            const center = ConstraintSolver.solveCenter(c);
            document.getElementById(`${prefix}_center_display`).textContent = 
                `(${center.x.toFixed(1)}, ${center.y.toFixed(1)}, ${center.z.toFixed(1)})`;
        }
        
        this.updateCenters();
        this.updateSpiralMeshes();
        this.updateCoherenceField();
    }
    
    updateCenters() {
        for (let obj of this.objects) {
            if (obj.centerMesh) this.scene.remove(obj.centerMesh);
        }
        
        for (let i = 0; i < this.objects.length; i++) {
            const obj = this.objects[i];
            const centerPos = ConstraintSolver.solveCenter(obj.constraints);
            
            const geom = new THREE.SphereGeometry(15, 16, 16);
            const mat = new THREE.MeshPhongMaterial({
                color: obj.color,
                emissive: obj.color
            });
            obj.centerMesh = new THREE.Mesh(geom, mat);
            obj.centerMesh.position.copy(centerPos);
            this.scene.add(obj.centerMesh);
        }
    }
    
    updateSpiralMeshes() {
        for (let mesh of this.spiralMeshes) {
            this.scene.remove(mesh);
        }
        this.spiralMeshes = [];
        
        for (let i = 0; i < this.objects.length; i++) {
            const obj = this.objects[i];
            const centerPos = ConstraintSolver.solveCenter(obj.constraints);
            const generator = new SpiralScanGenerator(centerPos, obj.constraints);
            
            const spiralPoints = generator.generateCurve();
            const geom = new THREE.BufferGeometry();
            geom.setAttribute('position', new THREE.BufferAttribute(
                new Float32Array(spiralPoints),
                3
            ));
            
            const mat = new THREE.LineBasicMaterial({
                color: obj.color,
                linewidth: 2,
                transparent: true,
                opacity: 0.7
            });
            
            const line = new THREE.Line(geom, mat);
            this.scene.add(line);
            this.spiralMeshes.push(line);
        }
    }
    
    updateCoherenceField() {
        // Disabled in simplified view - focus on single spiral clarity
    }
    
    hslToRgb(h, s, l) {
        h = h * 360;
        const c = (1 - Math.abs(2 * l - 1)) * s;
        const hp = h / 60;
        const x = c * (1 - Math.abs((hp % 2) - 1));
        
        let r, g, b;
        if (hp < 1) {r = c; g = x; b = 0;}
        else if (hp < 2) {r = x; g = c; b = 0;}
        else if (hp < 3) {r = 0; g = c; b = x;}
        else if (hp < 4) {r = 0; g = x; b = c;}
        else if (hp < 5) {r = x; g = 0; b = c;}
        else {r = c; g = 0; b = x;}
        
        const m = l - c / 2;
        return {r: (r + m), g: (g + m), b: (b + m)};
    }
    
    setupListeners() {
        // Constraint input listeners
        const inputIds = [
            'obj1_precX', 'obj1_precY', 'obj1_precZ', 'obj1_phase', 'obj1_coupling'
        ];
        
        for (let id of inputIds) {
            const elem = document.getElementById(id);
            if (elem) {
                elem.addEventListener('input', () => {
                    this.update();
                });
            }
        }
        
        // View mode buttons
        document.getElementById('topDownView').addEventListener('click', () => {
            this.viewMode = 'topdown';
            document.getElementById('topDownView').style.background = '#00d9ff';
            document.getElementById('topDownView').style.color = '#000';
            document.getElementById('topDownView').style.fontWeight = 'bold';
            document.getElementById('fromCenterView').style.background = '#444';
            document.getElementById('fromCenterView').style.color = '#00ff88';
            document.getElementById('fromCenterView').style.fontWeight = 'normal';
        });
        
        document.getElementById('fromCenterView').addEventListener('click', () => {
            this.viewMode = 'fromCenter';
            document.getElementById('topDownView').style.background = '#444';
            document.getElementById('topDownView').style.color = '#00ff88';
            document.getElementById('topDownView').style.fontWeight = 'normal';
            document.getElementById('fromCenterView').style.background = '#00d9ff';
            document.getElementById('fromCenterView').style.color = '#000';
            document.getElementById('fromCenterView').style.fontWeight = 'bold';
        });
        
        // Design mode toggle
        document.getElementById('designMode').addEventListener('change', (e) => {
            this.designMode = e.target.checked;
            if (this.designMode) {
                this.renderer.domElement.style.cursor = 'crosshair';
            } else {
                this.renderer.domElement.style.cursor = 'default';
            }
        });
        
        // Canvas click for design mode
        this.renderer.domElement.addEventListener('click', (event) => {
            if (!this.designMode) return;
            
            const rect = this.renderer.domElement.getBoundingClientRect();
            this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
            this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
            
            this.raycaster.setFromCamera(this.mouse, this.camera);
            
            // Intersect with a plane at z=0 to allow positioning anywhere
            const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
            const intersection = new THREE.Vector3();
            this.raycaster.ray.intersectPlane(plane, intersection);
            
            // Single object design mode
            const objIndex = 0;
            this.designTargets[objIndex] = intersection.clone();
            
            // Solve for required constraints
            const requiredConstraints = ConstraintSolver.solveConstraints(
                intersection,
                this.objects[objIndex].constraints
            );
            
            // Update the object's constraints
            this.setConstraints(objIndex, requiredConstraints);
        });
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        if (this.viewMode === 'topdown') {
            // External top-down view: bird's eye perspective
            const angle = Date.now() * 0.0001;
            const radius = 450;
            this.camera.position.set(
                Math.cos(angle) * radius * 0.7,
                350,
                Math.sin(angle) * radius * 0.7
            );
            this.camera.lookAt(0, 0, 0);
        } else {
            // Internal from-center view: observer at one of the centers looking outward
            const centerPos = ConstraintSolver.solveCenter(
                this.objects[this.internalViewCenterIndex].constraints
            );
            
            // Position camera at the center
            this.camera.position.copy(centerPos);
            
            // Look toward the other centers (or just rotate around)
            const angle = Date.now() * 0.0001;
            const lookDirection = new THREE.Vector3(
                Math.cos(angle) * 200,
                Math.sin(angle) * 150,
                Math.sin(angle * 0.7) * 200
            );
            this.camera.lookAt(
                centerPos.x + lookDirection.x,
                centerPos.y + lookDirection.y,
                centerPos.z + lookDirection.z
            );
        }
        
        this.renderer.render(this.scene, this.camera);
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new BidirectionalConstraintApp();
    });
} else {
    new BidirectionalConstraintApp();
}
</script>
        this.pointsPerTurn = pointsPerTurn;
        this.goldenAngle = 2.399963229728653;
    }
    
    generate() {
        // Generate spiral scan pattern around center
        // Moves in expanding spiral at multiple heights
        const points = [];
        const totalTurns = this.scanHeights;
        const totalPoints = totalTurns * this.pointsPerTurn;
        
        for (let i = 0; i < totalPoints; i++) {
            const t = i / totalPoints; // 0 to 1
            
            // Height varies from -scanRadius to +scanRadius
            const y = (t * 2 - 1) * this.scanRadius;
            
            // Radius expands then contracts (scanning pattern)
            const radiusPhase = Math.sin(t * Math.PI); // 0 to 1 to 0
            const r = this.scanRadius * radiusPhase;
            
            // Angle rotates by golden angle per point
            const angle = this.goldenAngle * i;
            
            const x = Math.cos(angle) * r;
            const z = Math.sin(angle) * r;
            
            points.push(new THREE.Vector3(
                this.centerPos.x + x,
                this.centerPos.y + y,
                this.centerPos.z + z
            ));
        }
        
        return new Float32Array(
            points.flatMap(p => [p.x, p.y, p.z])
        );
    }
    
    // Compute spiral curve as Float32Array [x, y, z, x, y, z, ...]
    generateCurve() {
        return this.generate();
    }
}

class CoherenceDetector {
    constructor(samplePoints = 1000) {
        this.samplePoints = samplePoints;
    }
    
    // Compute coherence value at point p from multiple spirals
    computeCoherence(point, spiralGenerators) {
        if (spiralGenerators.length === 0) return 0;
        if (spiralGenerators.length === 1) return 1; // Single spiral always coherent
        
        // Compute phase contribution from each spiral
        let coherenceSum = 0;
        let phasesX = [];
        let phasesY = [];
        let phasesZ = [];
        
        for (let gen of spiralGenerators) {
            const dx = point.x - gen.centerPos.x;
            const dy = point.y - gen.centerPos.y;
            const dz = point.z - gen.centerPos.z;
            
            // Distance determines phase along spiral
            const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
            const angle = Math.atan2(dz, dx);
            
            // Precession-like phase calculation
            phasesX.push(Math.cos(angle));
            phasesY.push(Math.cos(dy / gen.scanRadius * Math.PI));
            phasesZ.push(Math.sin(angle));
        }
        
        // Coherence = how aligned the phases are
        // High when all spirals point same direction, low when scattered
        let coherence = 0;
        
        // Vector sum of all contributions
        let sumX = phasesX.reduce((a, b) => a + b, 0);
        let sumY = phasesY.reduce((a, b) => a + b, 0);
        let sumZ = phasesZ.reduce((a, b) => a + b, 0);
        
        // Magnitude shows phase alignment
        const magnitude = Math.sqrt(sumX * sumX + sumY * sumY + sumZ * sumZ);
        coherence = magnitude / spiralGenerators.length;
        
        return Math.max(0, Math.min(1, coherence));
    }
    
    // Generate 3D coherence field for visualization
    generateCoherenceField(spiralGenerators, gridSize = 20) {
        const field = [];
        const spacing = 400 / gridSize;
        
        for (let x = -200; x < 200; x += spacing) {
            for (let y = -200; y < 200; y += spacing) {
                for (let z = -200; z < 200; z += spacing) {
                    const point = new THREE.Vector3(x, y, z);
                    const coherence = this.computeCoherence(point, spiralGenerators);
                    field.push({point, coherence});
                }
            }
        }
        
        return field;
    }
}

class MultiCenterSpiralApp {
    constructor() {
        this.container = document.getElementById('spiralFieldContainer');
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x0a0e27);
        
        this.camera = new THREE.PerspectiveCamera(
            75,
            this.container.clientWidth / this.container.clientHeight,
            0.1,
            10000
        );
        this.camera.position.set(400, 300, 400);
        this.camera.lookAt(0, 0, 0);
        
        this.renderer = new THREE.WebGLRenderer({antialias: true, alpha: false});
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.container.appendChild(this.renderer.domElement);
        
        // Lighting
        const ambientLight = new THREE.AmbientLight(0x00ff88, 0.4);
        this.scene.add(ambientLight);
        
        const pointLight = new THREE.PointLight(0x00d9ff, 0.8);
        pointLight.position.set(300, 300, 300);
        this.scene.add(pointLight);
        
        // Object centers (draggable)
        this.centers = [
            {pos: new THREE.Vector3(-150, 0, -150), gen: null, mesh: null},
            {pos: new THREE.Vector3(150, 0, -150), gen: null, mesh: null},
            {pos: new THREE.Vector3(0, 100, 150), gen: null, mesh: null}
        ];
        
        this.spiralMeshes = [];
        this.coherenceParticles = null;
        this.coherenceDetector = new CoherenceDetector();
        
        this.selectedCenter = null;
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();
        
        this.init();
        this.setupControls();
        this.animate();
    }
    
    init() {
        // Create centers and their spiral generators
        for (let centerData of this.centers) {
            centerData.gen = new SpiralScanGenerator(centerData.pos);
            
            // Visual representation of center
            const centerGeom = new THREE.SphereGeometry(15, 16, 16);
            const centerMat = new THREE.MeshPhongMaterial({color: 0x00ff88, emissive: 0x00ff88});
            centerData.mesh = new THREE.Mesh(centerGeom, centerMat);
            centerData.mesh.position.copy(centerData.pos);
            this.scene.add(centerData.mesh);
        }
        
        this.updateSpiralMeshes();
        this.updateCoherenceField();
    }
    
    updateSpiralMeshes() {
        // Remove old spiral meshes
        for (let mesh of this.spiralMeshes) {
            this.scene.remove(mesh);
        }
        this.spiralMeshes = [];
        
        // Create new spiral meshes for each center
        const colors = [0x00d9ff, 0xff00ff, 0x00ffff];
        
        for (let i = 0; i < this.centers.length; i++) {
            const centerData = this.centers[i];
            const spiralPoints = centerData.gen.generateCurve();
            
            const geom = new THREE.BufferGeometry();
            geom.setAttribute('position', new THREE.BufferAttribute(
                new Float32Array(spiralPoints),
                3
            ));
            
            const mat = new THREE.LineBasicMaterial({
                color: colors[i % colors.length],
                linewidth: 2,
                transparent: true,
                opacity: 0.7
            });
            
            const line = new THREE.Line(geom, mat);
            this.scene.add(line);
            this.spiralMeshes.push(line);
        }
    }
    
    updateCoherenceField() {
        // Remove old coherence visualization
        if (this.coherenceParticles) {
            this.scene.remove(this.coherenceParticles);
        }
        
        // Generate coherence field
        const field = this.coherenceDetector.generateCoherenceField(
            this.centers.map(c => c.gen),
            15
        );
        
        // PARADIGM: Only render observable geometry (coherence > threshold)
        // The visible shape IS the 3D model emerging from spiral coherence
        const coherenceThreshold = 0.25; // Only show 25%+ coherence
        
        const positions = [];
        const colors = [];
        
        for (let {point, coherence} of field) {
            // KEY CHANGE: Only render if observable (coherence above threshold)
            if (coherence < coherenceThreshold) {
                continue; // Don't render - unobservable
            }
            
            positions.push(point.x, point.y, point.z);
            
            // Coherence → color (low threshold=dark, high=bright cyan)
            // Brightness represents how clearly observable the point is
            const normalizedCoherence = (coherence - coherenceThreshold) / (1 - coherenceThreshold);
            
            const h = 0.5; // Cyan (constant hue)
            const s = normalizedCoherence; // Saturation based on coherence
            const l = normalizedCoherence * 0.6; // Lightness based on coherence
            
            const rgb = this.hslToRgb(h, s, l);
            colors.push(rgb.r, rgb.g, rgb.b);
        }
        
        // If no observable points, show nothing
        if (positions.length === 0) {
            return;
        }
        
        const geom = new THREE.BufferGeometry();
        geom.setAttribute('position', new THREE.BufferAttribute(
            new Float32Array(positions),
            3
        ));
        geom.setAttribute('color', new THREE.BufferAttribute(
            new Float32Array(colors),
            3
        ));
        
        const mat = new THREE.PointsMaterial({
            size: 12, // Larger particles since fewer of them
            vertexColors: true,
            transparent: true,
            opacity: 0.8,
            sizeAttenuation: true
        });
        
        this.coherenceParticles = new THREE.Points(geom, mat);
        this.scene.add(this.coherenceParticles);
    }
    
    hslToRgb(h, s, l) {
        h = h * 360; // Convert to degrees
        const c = (1 - Math.abs(2 * l - 1)) * s;
        const hp = h / 60;
        const x = c * (1 - Math.abs((hp % 2) - 1));
        
        let r, g, b;
        if (hp < 1) {r = c; g = x; b = 0;}
        else if (hp < 2) {r = x; g = c; b = 0;}
        else if (hp < 3) {r = 0; g = c; b = x;}
        else if (hp < 4) {r = 0; g = x; b = c;}
        else if (hp < 5) {r = x; g = 0; b = c;}
        else {r = c; g = 0; b = x;}
        
        const m = l - c / 2;
        return {
            r: (r + m),
            g: (g + m),
            b: (b + m)
        };
    }
    
    setupControls() {
        this.renderer.domElement.addEventListener('mousedown', (e) => {
            this.mouse.x = (e.clientX / this.container.clientWidth) * 2 - 1;
            this.mouse.y = -(e.clientY / this.container.clientHeight) * 2 + 1;
            
            this.raycaster.setFromCamera(this.mouse, this.camera);
            
            const centerMeshes = this.centers.map(c => c.mesh);
            const intersects = this.raycaster.intersectObjects(centerMeshes);
            
            if (intersects.length > 0) {
                this.selectedCenter = this.centers.find(c => c.mesh === intersects[0].object);
            }
        });
        
        this.renderer.domElement.addEventListener('mousemove', (e) => {
            if (!this.selectedCenter) return;
            
            this.mouse.x = (e.clientX / this.container.clientWidth) * 2 - 1;
            this.mouse.y = -(e.clientY / this.container.clientHeight) * 2 + 1;
            
            this.raycaster.setFromCamera(this.mouse, this.camera);
            
            // Intersect with ground plane (y = const)
            const planeY = this.selectedCenter.pos.y;
            const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), -planeY);
            const intersection = new THREE.Vector3();
            this.raycaster.ray.intersectPlane(plane, intersection);
            
            this.selectedCenter.pos.x = intersection.x;
            this.selectedCenter.pos.z = intersection.z;
            this.selectedCenter.mesh.position.copy(this.selectedCenter.pos);
            this.selectedCenter.gen.centerPos = this.selectedCenter.pos;
            
            this.updateSpiralMeshes();
            this.updateCoherenceField();
        });
        
        this.renderer.domElement.addEventListener('mouseup', () => {
            this.selectedCenter = null;
        });
        
        // Handle window resize
        window.addEventListener('resize', () => {
            const width = this.container.clientWidth;
            const height = this.container.clientHeight;
            this.camera.aspect = width / height;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(width, height);
        });
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        // Subtle auto-rotation if no interaction
        if (!this.selectedCenter) {
            this.camera.position.applyAxisAngle(new THREE.Vector3(0, 1, 0), 0.0005);
            this.camera.lookAt(0, 0, 0);
        }
        
        this.renderer.render(this.scene, this.camera);
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new MultiCenterSpiralApp();
    });
} else {
    new MultiCenterSpiralApp();
}
</script>

---

## How This Works: Constraints → Computed Centers → Emergent Geometry

### The Fundamental Principle

**You cannot choose where an object's center is in reality.** The center position is computed from the object's constraint specification. Change the constraints, the center moves. The geometry then emerges from the constraint-determined center position.

### Interactive Elements

**Adjust the constraint sliders** for each object:

1. **Precession Axis** (X, Y, Z)
   - Defines the orientation of the spiral rotation axis
   - The center position is computed along this direction
   - Different orientations = different center positions

2. **Phase Offset**
   - Shifts the spiral rotation phase
   - Affects how the spiral winds around the precession axis

3. **Coupling Strength** (0.1 to 1.0)
   - Controls how strongly this object couples with space
   - Distance from origin = 200 × coupling strength
   - Higher coupling = center farther from origin

**As you adjust any slider:**
- Center position is recomputed instantly
- Spirals emanate from new position
- Geometry reshapes based on new spiral configuration
- All changes are constraint-driven, never arbitrary

### What You're Seeing

**THIS IS HOW 3D MODELS SHOULD ACTUALLY BE COMPUTED.**

1. **Colored spheres** - Object centers (COMPUTED from constraints, not placed manually)
   - Cyan, magenta, light blue
   - Position is determined by precession axis and coupling strength
   - Move a constraint slider → center moves automatically

2. **Three spiral paths** - Scanning spirals emanating from computed centers
   - Follow golden angle precession pattern
   - Precession axis orientation determines spiral direction
   - Each spiral represents detection capability of that constraint-defined object

3. **Observable 3D geometry** - Only where spirals cohere
   - Shows ONLY points where coherence > 25% threshold
   - **The shape IS the spiral coherence pattern**
   - Completely determined by computed center positions
   - No manual modeling needed—emerges from constraint satisfaction

### The Paradigm: Objects Are Constraint-Determined Spirals

**Traditional 3D modeling:**
- Designer models object manually
- Stores fixed geometry
- Object is static

**Correct approach (what you see here):**
- Define object constraints (that's all you provide)
- System computes center position from constraints
- Spirals emanate from constraint-determined center
- **3D geometry emerges from spiral coherence**
- Change constraints → center updates → geometry reshapes automatically

**Key insight:** The entire 3D model is a consequence of constraint satisfaction. You're not creating geometry—you're specifying constraints, and the universe self-organizes the geometry from those constraints.

### What This Enables

1. **Verifiability** - Every object position can be proven from its constraints
2. **Consistency** - Impossible to create invalid configurations (all are constraint-derived)
3. **Adaptability** - Change one constraint → ripple through entire system
4. **Understanding** - See visually how constraints determine structure

### Mathematical Foundation

Each spiral is generated using:
- **Precession axis** (from constraints) determining spiral orientation
- **Golden angle** (2.399963229728653) for perfect angular coverage
- **Coupling strength** (from constraints) determining center distance
- **Coherence detection** = phase alignment of multiple spirals at each point

The system is completely self-determining: constraints → center → spirals → geometry.
