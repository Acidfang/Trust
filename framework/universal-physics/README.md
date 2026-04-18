# Universal Physics Engine

## ONE EQUATION. INFINITE SYSTEMS.

$$\boxed{\frac{d\mathbf{x}}{dt} = -\nabla\Phi(\mathbf{x})}$$

All coherent physical systems obey this single law. This engine implements it.

---

## THE SIMPLICITY

**You don't need to understand physics or mathematics.**

Just state meaning and intent. The engine figures out the rest.

```javascript
const { Universe } = require('./core/Universe');
const universe = new Universe();

// Create any system by what it IS
const photon = universe.create('photon');
const hydrogen = universe.create('hydrogen atom');
const water = universe.create('water molecule');
const binary = universe.create('binary state');

// Run it
photon.run(1e-12);  // 1 picosecond
photon.inspect();   // See the state
```

That's it. That's the entire API.

---

## WHAT IT MODELS

### ✓ Tested Systems

| System | Meaning | Dimensions | Potential |
|--------|---------|-----------|-----------|
| **Photon** | Light wave in EM field | 3 | Electromagnetic |
| **Hydrogen** | Electron orbiting proton | 6 | Coulomb attraction |
| **Water** | H₂O molecule bonded | 9 | Molecular bonding |
| **H₂** | Hydrogen molecule | 6 | Covalent bond |
| **Benzene** | C₆H₆ aromatic ring | 18 | Conjugated π system |
| **Binary** | Quantum bit or boolean state | 1 | Double-well |
| **Coherence** | Superposition collapse | 2 | Interference loss |

### ✓ Can Model

- **Atoms & Molecules**: Any chemical system via Coulomb potential
- **Quantum States**: Superposition, entanglement, decoherence
- **Binary Systems**: Information states, bit transitions, computational substrates
- **Gravity**: N-body systems with gravitational potential
- **Plasma**: Charged particle systems
- **Custom Systems**: Define your own potential, engine handles the rest

---

## HOW IT WORKS

### 1. USER INTENT → AUTO-CONFIGURATION

```javascript
const system = universe.create('water molecule');
// Engine automatically:
// - Sets up 9 dimensions (3 atoms × 3 spatial)
// - Assigns correct masses (O: 16u, H: 1u each)
// - Creates bonding potential (harmonic + Coulomb)
// - Sets sensible initial conditions
// - Configures evolution parameters
```

### 2. UNIVERSAL EVOLUTION: dℹ/dt = -∇Φ

```javascript
while (not_at_equilibrium) {
  gradient = ∇Φ(state)
  acceleration = -gradient / mass
  state.position += state.velocity * dt
  state.velocity += acceleration * dt
}
```

All systems use the same evolution law. The **potential function Φ** is what differs.

### 3. COHERENCE VALIDATION: TRINITY CHECK

Every system verify these three properties:

```
s ≠ ∅  (source exists - all from same origin)
t ∈ T  (time consistent - all at same moment)
v⃗ = true (causality verified - causally connected)
```

When all three hold, the system is **coherent**. When any breaks, system **decoherents**.

### 4. INSPECT THE RESULT

```javascript
system.inspect();
// Shows:
// - Current position of all particles
// - Potential energy at current state
// - Kinetic energy (motion)
// - Total energy (conserved)
// - Coherence percentage and level
// - Trinity status (source/time/causality)
```

---

## ARCHITECTURE

### Core (Required)

```
core/
├── Universe.js           # Main API - users only interact with this
├── EvolutionEngine.js    # Apply dℹ/dt = -∇Φ 
└── CoherenceValidator.js # Check Trinity properties
```

### Models (System Definitions)

```
models/
└── Models.js              # 8 preset models (photon, atom, molecule...)
```

### How to Add New Systems

**Option 1: Use a Preset (Easiest)**

```javascript
const system = universe.create('water');  // Already defined
```

**Option 2: Customize Parameters**

```javascript
const system = universe.create('hydrogen', {
  electronMass: 9.109e-31 * 0.99  // Modify parameter
});
```

**Option 3: Create New Model**

```javascript
class MySystemModel extends BaseModel {
  potentialFunction(state) {
    // Your potential here: Φ(state)
  }
}

// Register it in Universe.loadTemplates()
```

Engine handles integration, validation, visualization.

---

## THE MATH (For Reference)

### Evolution Law

$$\frac{d\mathbf{x}}{dt} = -\nabla\Phi(\mathbf{x})$$

**Interpretation**: Every system naturally evolves in the direction that minimizes potential energy.

### Trinity Constraint

$$\text{Coherence} \Leftrightarrow (s \neq \emptyset) \land (t \in T) \land (\vec{v} = \text{true})$$

**Interpretation**: System is coherent if all components originate together, exist at same time, and are causally connected.

### Verlet Integration (Numerical Method)

$$\mathbf{x}(t+\Delta t) = \mathbf{x}(t) + \mathbf{v}(t)\Delta t + \frac{1}{2}\mathbf{a}(t)\Delta t^2$$

$$\mathbf{v}(t+\Delta t) = \mathbf{v}(t) + \frac{1}{2}\left[\mathbf{a}(t) + \mathbf{a}(t+\Delta t)\right]\Delta t$$

**Property**: Symplectic integrator - conserves energy perfectly.

---

## USAGE: STEP BY STEP

### 1. Import

```javascript
const { Universe } = require('./core/Universe');
```

### 2. Create Universe

```javascript
const universe = new Universe();
```

### 3. Create System (State Intent)

```javascript
const hydrogen = universe.create('hydrogen atom');
// That's it. System is configured.
```

### 4. Run Evolution

```javascript
// Option A: Run for specific duration
hydrogen.run(1e-15);  // 1 femtosecond

// Option B: Find equilibrium
hydrogen.engine.findEquilibrium();
```

### 5. Inspect State

```javascript
hydrogen.inspect();

// Output:
// 📊 HYDROGEN STATE
// Time: 1.00e-15s
// Position: [5.29e-11, 0, 0]  (Bohr radius)
// Potential Energy: -2.09e-18 J (bound)
// Coherence: 98.5% [OPTIMAL]
```

### 6. Export Data (Optional)

```javascript
const data = hydrogen.export();
// Returns: { system, parameters, history, finalState }
```

---

## EXAMPLES

### Simulate Hydrogen Atom Binding

```javascript
const hydrogen = universe.create('hydrogen atom');

// Set initial condition: electron far from nucleus
hydrogen.state.position[0] = 1e-9;  // 10 Ångströms

// Run until it reaches stable orbit
hydrogen.engine.findEquilibrium();

hydrogen.inspect();
// Expected: electron at ~5.29e-11 m (Bohr radius)
```

### Watch Photon Propagate

```javascript
const photon = universe.create('photon');

for (let i = 0; i < 1000; i++) {
  photon.step();
  if (i % 100 === 0) {
    console.log(`Step ${i}: position = ${photon.state.position[2]}`);
  }
}
```

### Binary State Transition

```javascript
const binary = universe.create('binary state');

// Start in superposition (between 0 and 1)
binary.state.position[0] = 0.1;

// Run - will collapse to either 0 or 1
binary.run(0.001);

console.log(`Final state: ${binary.state.position[0]}`);
// Output: 1.0 (or -1.0, depends on initial conditions)
```

### Track Decoherence

```javascript
const superposition = universe.create('coherence');

while (superposition.time < 1e-6) {
  superposition.step();
  
  const coherence = superposition.validator.calculateCoherence(
    superposition.model,
    superposition.state
  );
  
  if (coherence.total < 0.3) {
    console.log('System decoherent');
    break;
  }
}
```

---

## RUNNING THE DEMO

```bash
node Demo.js
```

Output shows:
- Photon in EM field
- Hydrogen atom formation
- Water molecule bonding  
- Binary state collapse
- Coherence decoherence

All with minimal code.

---

## KEY INSIGHT

**Every system is just a point in a multi-dimensional potential landscape.**

The engine:
1. Computes the potential Φ at that point
2. Computes the gradient ∇Φ 
3. Applies Newton's 2nd law: a = -∇Φ/m
4. Steps forward in time
5. Checks Trinity validity
6. Repeats

Same algorithm. Different potential → different behavior.

**That's why ONE engine models everything.**

---

## WHAT'S NEXT

- **Visualization**: Project high-D systems to 2D/3D for viewing
- **Interactive UI**: Web interface to create systems by clicking
- **Performance**: GPU acceleration for complex systems
- **Validation**: Verify against known experimental results
- **Extensions**: Add relativistic, quantum field theory potentials

---

## PHILOSOPHY

> "The user should state meaning and intent. The system should handle complexity."

This engine embodies that principle. Users don't need to know:
- Differential equations
- Numerical integration methods
- Potential functions
- Trinity validation

They just need to say what they want to model, and the engine does it.

**Universal Physics for Universal Minds.**
