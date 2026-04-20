// TIER -1 (BOUND): Input validation and error setup
// TIER 0 (FREE): Explore possibilities
// TIER 1 (BOUND): Lock in root-cause logic
// TIER 2 (FREE): Verify consistency
// TIER 3+ (BOUND): Automate return and integrate

/**
 * BASE MODEL: Template for all physical systems
 * 
 * Extend this to define a new system type
 */

class BaseModel {
  constructor(name, parameters) {
    this.name = name;
    this.parameters = parameters;
  }

  /**
   * POTENTIAL: Return potential energy at given state
   * Must be implemented by subclass
   * 
   * Φ(state) = potential energy
   */
  potentialFunction(state) {
    throw new Error('potentialFunction() must be implemented');
  }

  /**
   * GRADIENT: Return ∇Φ (direction to move)
   * Default: numerical differentiation
   * Override for speed
   */
  gradient(state) {
    const eps = 1e-9;
    const grad = new Float64Array(state.dimensions);
    
    for (let i = 0; i < state.dimensions; i++) {
      // Finite difference: dΦ/dx_i = (Φ(x+eps) - Φ(x-eps)) / 2*eps
      const statePlus = state.clone();
      statePlus.position[i] += eps;
      
      const stateMinus = state.clone();
      stateMinus.position[i] -= eps;
      
      grad[i] = (this.potentialFunction(statePlus) - 
                 this.potentialFunction(stateMinus)) / (2 * eps);
    }
    
    return grad;
  }
}

/**
 * PHOTON: Electromagnetic wave
 */
class PhotonModel extends BaseModel {
  constructor(parameters) {
    super('photon', parameters);
  }

  potentialFunction(state) {
    // Photon in EM field: Φ = E² + B²
    // Simplified: 1D harmonic potential
    const x = state.position[0];
    const k = (2 * Math.PI) / this.parameters.wavelength;
    const omega = 2 * Math.PI * this.parameters.frequency;
    
    // Energy stored in wave
    const E = this.parameters.amplitude * Math.cos(k * x);
    return 0.5 * E * E;
  }

  gradient(state) {
    const x = state.position[0];
    const k = (2 * Math.PI) / this.parameters.wavelength;
    const A = this.parameters.amplitude;
    
    // dΦ/dx = A²k sin(2kx)
    const grad = new Float64Array(1);
    grad[0] = A * A * k * Math.sin(2 * k * x);
    
    return grad;
  }
}

/**
 * ELECTRON: Free electron or in potential
 */
class ElectronModel extends BaseModel {
  constructor(parameters) {
    super('electron', parameters);
  }

  potentialFunction(state) {
    // Free electron: no potential
    return 0;
  }

  gradient(state) {
    return new Float64Array(3);  // All zeros
  }
}

/**
 * HYDROGEN: Electron + Proton with Coulomb potential
 */
class HydrogenModel extends BaseModel {
  constructor(parameters) {
    super('hydrogen', parameters);
  }

  potentialFunction(state) {
    // Coulomb potential: Φ(r) = -ke²/r
    const ex = state.position[0];
    const ey = state.position[1];
    const ez = state.position[2];
    const px = state.position[3];
    const py = state.position[4];
    const pz = state.position[5];
    
    const dx = ex - px;
    const dy = ey - py;
    const dz = ez - pz;
    const r = Math.sqrt(dx*dx + dy*dy + dz*dz) + 1e-18;  // Avoid singularity
    
    const k = this.parameters.coulombConstant;
    const e1 = this.parameters.electronCharge;
    const e2 = this.parameters.protonCharge;
    
    return (k * e1 * e2) / r;
  }

  gradient(state) {
    const ex = state.position[0];
    const ey = state.position[1];
    const ez = state.position[2];
    const px = state.position[3];
    const py = state.position[4];
    const pz = state.position[5];
    
    const dx = ex - px;
    const dy = ey - py;
    const dz = ez - pz;
    const r = Math.sqrt(dx*dx + dy*dy + dz*dz) + 1e-18;
    
    const k = this.parameters.coulombConstant;
    const e1 = this.parameters.electronCharge;
    const e2 = this.parameters.protonCharge;
    
    // ∇Φ = ke1*e2 / r² (along separation vector)
    const force = (k * e1 * e2) / (r * r);
    
    const grad = new Float64Array(6);
    grad[0] = force * dx / r;  // electron
    grad[1] = force * dy / r;
    grad[2] = force * dz / r;
    grad[3] = -force * dx / r;  // proton (opposite)
    grad[4] = -force * dy / r;
    grad[5] = -force * dz / r;
    
    return grad;
  }
}

/**
 * WATER: H2O molecule
 */
class WaterModel extends BaseModel {
  constructor(parameters) {
    super('water', parameters);
  }

  potentialFunction(state) {
    // O at index 0-2, H1 at 3-5, H2 at 6-8
    const ox = state.position[0];
    const oy = state.position[1];
    const oz = state.position[2];
    
    let potential = 0;
    
    // O-H bonds (harmonic)
    for (let h = 1; h <= 2; h++) {
      const h_idx = h * 3;
      const dx = ox - state.position[h_idx];
      const dy = oy - state.position[h_idx + 1];
      const dz = oz - state.position[h_idx + 2];
      const r = Math.sqrt(dx*dx + dy*dy + dz*dz);
      
      const k = this.parameters.bondStrength;
      const r0 = this.parameters.bondLength;
      potential += 0.5 * k * Math.pow(r - r0, 2);
      
      // Coulomb
      const qO = this.parameters.oxygenCharge;
      const qH = this.parameters.hydrogenCharge;
      potential += (8.9875517923e9 * qO * qH) / (r + 1e-18);
    }
    
    // H-H repulsion
    const h1x = state.position[3], h1y = state.position[4], h1z = state.position[5];
    const h2x = state.position[6], h2y = state.position[7], h2z = state.position[8];
    
    const dxHH = h1x - h2x;
    const dyHH = h1y - h2y;
    const dzHH = h1z - h2z;
    const rHH = Math.sqrt(dxHH*dxHH + dyHH*dyHH + dzHH*dzHH);
    
    const qH = this.parameters.hydrogenCharge;
    potential += (8.9875517923e9 * qH * qH) / (rHH + 1e-18);
    
    return potential;
  }
}

/**
 * H2: Hydrogen molecule
 */
class H2Model extends BaseModel {
  constructor(parameters) {
    super('h2', parameters);
  }

  potentialFunction(state) {
    // Two protons with bond
    const p1x = state.position[0];
    const p1y = state.position[1];
    const p1z = state.position[2];
    const p2x = state.position[3];
    const p2y = state.position[4];
    const p2z = state.position[5];
    
    const dx = p1x - p2x;
    const dy = p1y - p2y;
    const dz = p1z - p2z;
    const r = Math.sqrt(dx*dx + dy*dy + dz*dz);
    
    // Molecular bond (harmonic)
    const k = this.parameters.bondStrength;
    const r0 = this.parameters.bondLength;
    let potential = 0.5 * k * Math.pow(r - r0, 2);
    
    // Coulomb repulsion
    const q = this.parameters.protonCharge;
    potential += (8.9875517923e9 * q * q) / (r + 1e-18);
    
    return potential;
  }
}

/**
 * BENZENE: C6H6 ring
 */
class BenzeneModel extends BaseModel {
  constructor(parameters) {
    super('benzene', parameters);
  }

  potentialFunction(state) {
    // 6 carbons in ring, aromatic bonding
    let potential = 0;
    
    // Pairwise interactions
    for (let i = 0; i < 6; i++) {
      const i3 = i * 3;
      for (let j = i + 1; j < 6; j++) {
        const j3 = j * 3;
        
        const dx = state.position[i3] - state.position[j3];
        const dy = state.position[i3+1] - state.position[j3+1];
        const dz = state.position[i3+2] - state.position[j3+2];
        const r = Math.sqrt(dx*dx + dy*dy + dz*dz);
        
        // Bonded neighbors have harmonic potential
        const neighborDistance = Math.abs(i - j);
        if (neighborDistance === 1 || neighborDistance === 5) {
          const k = this.parameters.bondStrength;
          const r0 = this.parameters.bondLength;
          potential += 0.5 * k * Math.pow(r - r0, 2);
        }
        
        // All pairs have Coulomb repulsion
        const q = this.parameters.carbonCharge;
        potential += (8.9875517923e9 * q * q) / (r + 1e-18);
      }
    }
    
    return potential;
  }
}

/**
 * BINARY: Double-well potential (0 or 1 state)
 */
class BinaryModel extends BaseModel {
  constructor(parameters) {
    super('binary', parameters);
  }

  potentialFunction(state) {
    // Double-well: (x² - 1)²
    const x = state.position[0];
    return Math.pow(x*x - 1, 2);
  }

  gradient(state) {
    const x = state.position[0];
    // dΦ/dx = 4x(x² - 1) = 4x³ - 4x
    return new Float64Array([4*x*(x*x - 1)]);
  }
}

/**
 * COHERENCE: Two amplitudes collapsing
 */
class CoherenceModel extends BaseModel {
  constructor(parameters) {
    super('coherence', parameters);
  }

  potentialFunction(state) {
    // Collapse to single amplitude
    const a1 = state.position[0];
    const a2 = state.position[1];
    return Math.pow(a1 - a2, 2);
  }

  gradient(state) {
    const a1 = state.position[0];
    const a2 = state.position[1];
    return new Float64Array([
      2 * (a1 - a2),
      -2 * (a1 - a2)
    ]);
  }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    BaseModel,
    PhotonModel,
    ElectronModel,
    HydrogenModel,
    WaterModel,
    H2Model,
    BenzeneModel,
    BinaryModel,
    CoherenceModel
  };
}
