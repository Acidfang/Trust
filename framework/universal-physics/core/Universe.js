// TIER -1 (BOUND): Input validation and error setup
// TIER 0 (FREE): Explore possibilities
// TIER 1 (BOUND): Lock in root-cause logic
// TIER 2 (FREE): Verify consistency
// TIER 3+ (BOUND): Automate return and integrate

/**
 * UNIVERSE: The simplest possible interface
 * 
 * User just states meaning and intent. Everything else is auto-generated.
 * 
 * USAGE:
 *   const universe = new Universe();
 *   const photon = universe.create('photon');
 *   const hydrogen = universe.create('hydrogen atom');
 *   const water = universe.create('water molecule');
 *   const binary = universe.create('binary state');
 *   
 *   photon.run(1e-12);  // Run for 1 picosecond
 *   hydrogen.inspect(); // See what's happening
 */

class Universe {
  constructor() {
    this.systems = new Map();
    this.templates = this.loadTemplates();
    this.time = 0;
  }

  /**
   * CREATE: One method to create any system
   * Parse user intent, auto-generate model
   */
  create(intent, customParameters = {}) {
    const normalized = this.normalizeIntent(intent);
    const template = this.findTemplate(normalized);
    
    if (!template) {
      throw new Error(`Cannot recognize system intent: "${intent}". 
        Try: photon, electron, hydrogen atom, water molecule, 
        benzene, binary state, coherence, etc.`);
    }

    // Create the system from template
    const system = new CoherentSystem(normalized, template, customParameters);
    this.systems.set(normalized, system);
    
    return system;
  }

  normalizeIntent(intent) {
    // "photon" -> "photon"
    // "hydrogen atom" -> "hydrogen"
    // "H2O" -> "water"
    // "water molecule" -> "water"
    // "binary" -> "binary"
    // "0 and 1" -> "binary"
    
    const lower = intent.toLowerCase().trim();
    
    const aliases = {
      'electromagnetic wave': 'photon',
      'light': 'photon',
      'em wave': 'photon',
      'electron': 'electron',
      'e-': 'electron',
      'proton': 'proton',
      'p+': 'proton',
      'hydrogen': 'hydrogen',
      'h atom': 'hydrogen',
      'hydrogen atom': 'hydrogen',
      'h2o': 'water',
      'water molecule': 'water',
      'water': 'water',
      'h2': 'h2',
      'hydrogen molecule': 'h2',
      'benzene': 'benzene',
      'c6h6': 'benzene',
      'binary': 'binary',
      'bit': 'binary',
      '0 and 1': 'binary',
      'boolean': 'binary',
      'coherence': 'coherence',
      'superposition': 'coherence'
    };
    
    return aliases[lower] || lower;
  }

  loadTemplates() {
    return {
      'photon': {
        type: 'photon',
        dimensions: 3,
        meaning: 'EM wave traveling through space',
        parameters: {
          frequency: 1e15,                    // Hz
          wavelength: 3e-7,                   // meters
          speed: 3e8,                         // m/s
          amplitude: 1.0
        },
        initial: {
          position: [0, 0, 0],
          velocity: [0, 0, 3e8],
          mass: [1, 1, 1]                     // Photons have effective mass
        },
        potential: 'electromagnetic-wave'
      },

      'electron': {
        type: 'electron',
        dimensions: 3,
        meaning: 'Free electron moving in space',
        parameters: {
          mass: 9.109e-31,                    // kg
          charge: -1.602e-19,                 // Coulombs
          spin: 0.5
        },
        initial: {
          position: [0, 0, 0],
          velocity: [1e6, 0, 0],              // 1 million m/s
          mass: [9.109e-31, 9.109e-31, 9.109e-31]
        },
        potential: 'free-particle'
      },

      'hydrogen': {
        type: 'hydrogen',
        dimensions: 6,                        // electron (x,y,z), proton (x,y,z)
        meaning: 'Electron orbiting proton nucleus',
        parameters: {
          electronMass: 9.109e-31,
          protonMass: 1.673e-27,
          electronCharge: -1.602e-19,
          protonCharge: 1.602e-19,
          coulombConstant: 8.9875517923e9
        },
        initial: {
          position: [1e-10, 0, 0, 0, 0, 0],   // electron 1Å away, proton at origin
          velocity: [0, 2.2e6, 0, 0, 0, 0],   // electron moving tangentially
          mass: [
            9.109e-31, 9.109e-31, 9.109e-31,
            1.673e-27, 1.673e-27, 1.673e-27
          ]
        },
        potential: 'coulomb'
      },

      'water': {
        type: 'water',
        dimensions: 9,                        // 3 atoms × 3 coords
        meaning: 'Water molecule with bent geometry',
        parameters: {
          oxygenMass: 15.999 * 1.66054e-27,
          hydrogenMass: 1.008 * 1.66054e-27,
          oxygenCharge: -0.8 * 1.602e-19,
          hydrogenCharge: 0.4 * 1.602e-19,
          bondStrength: 500,
          bondLength: 9.6e-11
        },
        initial: {
          position: [0, 0, 0, 9.6e-11, 0, 0, -9.6e-11*Math.cos(104.5*Math.PI/180), 0, 9.6e-11*Math.sin(104.5*Math.PI/180)],
          velocity: new Array(9).fill(0),
          mass: [
            15.999 * 1.66054e-27, 15.999 * 1.66054e-27, 15.999 * 1.66054e-27,
            1.008 * 1.66054e-27, 1.008 * 1.66054e-27, 1.008 * 1.66054e-27,
            1.008 * 1.66054e-27, 1.008 * 1.66054e-27, 1.008 * 1.66054e-27
          ]
        },
        potential: 'molecular-bonding'
      },

      'h2': {
        type: 'h2',
        dimensions: 6,                        // 2 atoms × 3 coords
        meaning: 'Hydrogen molecule (two protons bonded)',
        parameters: {
          protonMass: 1.673e-27,
          protonCharge: 1.602e-19,
          bondStrength: 574,                  // eV
          bondLength: 7.4e-11
        },
        initial: {
          position: [0, 0, 0, 7.4e-11, 0, 0],
          velocity: [0, 0, 0, 0, 0, 0],
          mass: [
            1.673e-27, 1.673e-27, 1.673e-27,
            1.673e-27, 1.673e-27, 1.673e-27
          ]
        },
        potential: 'hydrogen-molecule'
      },

      'benzene': {
        type: 'benzene',
        dimensions: 18,                       // 6 carbon atoms × 3 coords
        meaning: 'Benzene ring with delocalized electrons',
        parameters: {
          carbonMass: 12.011 * 1.66054e-27,
          carbonCharge: -0.2 * 1.602e-19,
          bondStrength: 940,                  // eV (aromatic)
          bondLength: 1.4e-10,
          ringRadius: 0.7e-10
        },
        initial: {
          position: this.generateBenzeneRing(),
          velocity: new Array(18).fill(0),
          mass: new Array(18).fill(12.011 * 1.66054e-27)
        },
        potential: 'aromatic-bonding'
      },

      'binary': {
        type: 'binary',
        dimensions: 1,                        // 1D: position between 0 and 1
        meaning: 'Quantum bit or boolean state in double-well potential',
        parameters: {
          wellDepth: 1.0,
          barierHeight: 10.0
        },
        initial: {
          position: [0.1],                    // Start near false (0)
          velocity: [0],
          mass: [1.0]
        },
        potential: 'double-well'              // (x² - 1)²
      },

      'coherence': {
        type: 'coherence',
        dimensions: 2,                        // amplitude1, amplitude2
        meaning: 'Two-component system collapsing via decoherence',
        parameters: {
          coupling: 1.0
        },
        initial: {
          position: [1.0, 0.5],               // Start in superposition
          velocity: [0, 0],
          mass: [1.0, 1.0]
        },
        potential: 'coherence-loss'
      }
    };
  }

  generateBenzeneRing() {
    const ring = [];
    for (let i = 0; i < 6; i++) {
      const angle = (i * 2 * Math.PI) / 6;
      const x = 0.7e-10 * Math.cos(angle);
      const y = 0.7e-10 * Math.sin(angle);
      const z = 0;
      ring.push(x, y, z);
    }
    return ring;
  }

  findTemplate(normalized) {
    return this.templates[normalized];
  }
}

/**
 * COHERENT SYSTEM: A specific instance in the universe
 * User interacts with this object
 */
class CoherentSystem {
  constructor(name, template, customParameters = {}) {
    this.name = name;
    this.template = template;
    this.parameters = Object.assign({}, template.parameters, customParameters);
    this.dimensions = template.dimensions;
    
    // Initialize state
    this.state = new FieldState(
      template.dimensions,
      template.initial.position,
      template.initial.velocity,
      template.initial.mass
    );
    
    // Get the right model
    this.model = this.instantiateModel(template, this.parameters);
    
    // Setup evolution
    this.engine = new EvolutionEngine(this.model, this.state);
    this.validator = new CoherenceValidator();
    
    // History
    this.history = [];
    this.time = 0;
  }

  instantiateModel(template, parameters) {
    // Load the right model for this system type
    const models = {
      'photon': () => new PhotonModel(parameters),
      'electron': () => new ElectronModel(parameters),
      'hydrogen': () => new HydrogenModel(parameters),
      'water': () => new WaterModel(parameters),
      'h2': () => new H2Model(parameters),
      'benzene': () => new BenzeneModel(parameters),
      'binary': () => new BinaryModel(parameters),
      'coherence': () => new CoherenceModel(parameters)
    };

    const constructor = models[template.type];
    if (!constructor) {
      throw new Error(`No model for type: ${template.type}`);
    }
    return constructor();
  }

  /**
   * RUN: Execute the simulation for specified duration
   */
  run(durationSeconds) {
    console.log(`\n▶ Running ${this.name} for ${durationSeconds}s`);
    this.engine.run(durationSeconds);
    this.recordSnapshot();
    return this;
  }

  /**
   * STEP: Single evolution step
   */
  step() {
    this.engine.step();
    this.recordSnapshot();
    return this;
  }

  /**
   * INSPECT: Show current state of the system
   */
  inspect() {
    const coherence = this.validator.calculateCoherence(this.model, this.state);
    const observable = this.calculateObservables();
    
    console.log(`\n📊 ${this.name.toUpperCase()} STATE`);
    console.log(`Time: ${this.time.toExponential(2)}s`);
    console.log(`Position: ${this.state.position.slice(0, 3).map(x => x.toExponential(2)).join(', ')}`);
    console.log(`Velocity: ${this.state.velocity.slice(0, 3).map(v => v.toExponential(2)).join(', ')}`);
    console.log(`Potential Energy: ${observable.potential.toExponential(2)} J`);
    console.log(`Kinetic Energy: ${observable.kinetic.toExponential(2)} J`);
    console.log(`Total Energy: ${(observable.potential + observable.kinetic).toExponential(2)} J`);
    console.log(`Coherence: ${(coherence.total * 100).toFixed(1)}% [${coherence.level}]`);
    console.log(`Trinity Status:`, {
      source_unified: coherence.trinity.source_unified,
      time_synchronized: coherence.trinity.time_synchronized,
      causality_verified: coherence.trinity.causality_verified
    });
    
    return this;
  }

  recordSnapshot() {
    this.history.push({
      time: this.time,
      position: this.state.position.slice(),
      velocity: this.state.velocity.slice(),
      potential: this.model.potentialFunction(this.state),
      coherence: this.validator.calculateCoherence(this.model, this.state)
    });
    this.time = this.engine.time;
  }

  calculateObservables() {
    const mass = this.state.mass;
    const velocity = this.state.velocity;
    
    let kinetic = 0;
    for (let i = 0; i < mass.length; i++) {
      kinetic += 0.5 * mass[i] * velocity[i] * velocity[i];
    }
    
    return {
      potential: this.model.potentialFunction(this.state),
      kinetic: kinetic,
      totalEnergy: kinetic + this.model.potentialFunction(this.state)
    };
  }

  /**
   * EXPORT: Get simulation data
   */
  export() {
    return {
      system: this.name,
      parameters: this.parameters,
      history: this.history,
      finalState: {
        position: this.state.position,
        velocity: this.state.velocity,
        potential: this.model.potentialFunction(this.state),
        coherence: this.validator.calculateCoherence(this.model, this.state)
      }
    };
  }
}

/**
 * FIELD STATE: Universal state vector for any system
 */
class FieldState {
  constructor(dimensions, position, velocity, mass) {
    this.dimensions = dimensions;
    this.position = new Float64Array(position);
    this.velocity = new Float64Array(velocity);
    this.mass = new Float64Array(mass);
    this.acceleration = new Float64Array(dimensions);
  }

  clone() {
    const cloned = new FieldState(
      this.dimensions,
      Array.from(this.position),
      Array.from(this.velocity),
      Array.from(this.mass)
    );
    cloned.acceleration = new Float64Array(this.acceleration);
    return cloned;
  }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { Universe, CoherentSystem, FieldState };
}
