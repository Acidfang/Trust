/**
 * UPFM Field Solver - JavaScript Implementation
 * Solves: ∂i/∂t = -∇Φ(x,y) via gradient descent
 * Returns complex field (magnitude + phase)
 */

class FieldSolver {
  constructor(gridSize = 128, domain = [-2, 2]) {  // Reduced to 128
    this.gridSize = gridSize;
    this.domain = domain;
    this.dx = (domain[1] - domain[0]) / gridSize;
    this.dt = 0.05;  // Increased from 0.01 for faster convergence
    this.size = gridSize * gridSize;
    
    // Pre-compute coordinate grid
    this.coordGrid = new Float32Array(this.size * 2);
    const domainMin = domain[0];
    for (let i = 0; i < this.size; i++) {
      const y = Math.floor(i / gridSize);
      const x = i % gridSize;
      this.coordGrid[i * 2] = domainMin + x * this.dx;      // x
      this.coordGrid[i * 2 + 1] = domainMin + y * this.dx;  // y
    }
  }

  /**
   * Compute gradient of potential via finite differences
   */
  computeGradient(field, potential) {
    const grad = new Float32Array(this.size * 2);  // Real/Imag pairs
    const eps = this.dx;
    const eps2inv = 1 / (2 * eps);
    
    for (let i = 0; i < this.size; i++) {
      const x = this.coordGrid[i * 2];
      const y = this.coordGrid[i * 2 + 1];
      
      // Central differences - 4 evaluations
      const fxp = potential(x + eps, y);
      const fxm = potential(x - eps, y);
      const fyp = potential(x, y + eps);
      const fym = potential(x, y - eps);
      
      grad[i * 2] = (fxp - fxm) * eps2inv;      // dfdx
      grad[i * 2 + 1] = (fyp - fym) * eps2inv; // dfdy
    }
    return grad;
  }

  /**
   * Get x,y coordinates from flat index
   */
  getCoordinates(idx, domainMin) {
    const gs = this.gridSize;
    const y = Math.floor(idx / gs);
    const x = idx % gs;
    return [
      domainMin + x * this.dx,
      domainMin + y * this.dx
    ];
  }

  /**
   * Get flat index from x,y coordinates
   */
  getIndex(x, y, domainMin) {
    const ix = Math.round((x - domainMin) / this.dx);
    const iy = Math.round((y - domainMin) / this.dx);
    return iy * this.gridSize + ix;
  }

  /**
   * Main solver: gradient descent until convergence
   * Async version to avoid blocking UI
   */
  async solve(potentialFunc, params = {}) {
    const tMax = params.tMax || 100;  // Reduced iterations
    const epsilon = params.epsilon || 1e-3;  // Very relaxed convergence
    const initScale = params.initScale || 0.1;
    
    // Initialize field as flat typed array [real0, imag0, real1, imag1, ...]
    let field = new Float32Array(this.size * 2);
    for (let i = 0; i < this.size * 2; i++) {
      field[i] = (Math.random() - 0.5) * initScale;
    }
    
    let t = 0;
    let converged = false;
    
    while (t < tMax && !converged) {
      const potential = (x, y) => potentialFunc(x, y, params);
      const grad = this.computeGradient(field, potential);
      
      // Update field & check convergence
      let maxGrad = 0;
      for (let i = 0; i < this.size * 2; i += 2) {
        field[i] -= this.dt * grad[i];           // real
        field[i + 1] -= this.dt * grad[i + 1];   // imag
        
        const gradMag = Math.sqrt(grad[i] ** 2 + grad[i + 1] ** 2);
        maxGrad = Math.max(maxGrad, gradMag);
      }
      
      // Only check convergence every 10 iterations (faster)
      if (t % 10 === 0 && maxGrad < epsilon) {
        converged = true;
      }
      
      t++;
      
      // Yield to UI every 10 iterations
      if (t % 10 === 0) {
        await new Promise(resolve => setTimeout(resolve, 0));
      }
    }
    
    return { field, converged, iterations: t };
  }
}

/**
 * Potential Functions - parameterized Φ(x,y)
 */
const Potentials = {
  electronSpiral: (x, y, params = {}) => {
    const fe = params.frequency || 12;
    const sigma = params.sigma || 0.5;  // Gaussian width
    const r = Math.sqrt(x ** 2 + y ** 2);
    const theta = Math.atan2(y, x);
    
    // Spiral: angular oscillation modulated by radial decay
    const spiral = fe * theta;
    const radial_decay = Math.exp(-(r ** 2) / (2 * sigma ** 2));  // Smooth gaussian
    
    return radial_decay * Math.sin(spiral) + 0.5 * r ** 2;  // Add gentle quartic confinement
  },

  photonPropagating: (x, y, params = {}) => {
    const f = params.frequency || 8;
    const dir = params.direction || 0;
    const decay = params.decay || 0.1;
    
    const kx = f * Math.cos(dir);
    const ky = f * Math.sin(dir);
    const wave = Math.sin(kx * x + ky * y);
    const envelope = Math.exp(-decay * (x ** 2 + y ** 2));
    
    return wave * envelope;
  },

  protonResonance: (x, y, params = {}) => {
    const harmonics = params.harmonics || [1, 2, 3];
    const binding = params.binding || 1.0;  // Reduced
    const r = Math.sqrt(x ** 2 + y ** 2);
    
    let potential = 0;
    for (const h of harmonics) {
      const theta = Math.atan2(y, x);
      potential += 0.5 * Math.cos(h * theta);  // Reduced amplitude
    }
    
    potential += 0.5 * binding * r ** 2;  // Gentler
    return potential;
  },

  gravityWell: (x, y, params = {}) => {
    const mass = params.mass || 1.0;
    const scale = params.scale || 1.0;
    const r = Math.sqrt(x ** 2 + y ** 2) + 0.2;  // Larger offset to avoid singularity
    
    return -(mass / (r + 1)) * scale;  // Softer falloff
  },

  galaxySpiral: (x, y, params = {}) => {
    const M = params.mass || 5;  // Reduced from 10
    const arms = params.arms || 2;
    const rotation = params.rotation || 1;  // Reduced rotation
    const r = Math.sqrt(x ** 2 + y ** 2) + 0.1;
    const theta = Math.atan2(y, x);
    
    const gravity = -(M / (r + 2));  // Softer
    const spiralPattern = 0.3 * Math.cos(arms * (theta - rotation * Math.log(r + 1)));  // Reduced amplitude
    
    return gravity + spiralPattern;
  },

  consciousnessNetwork: (x, y, params = {}) => {
    const nodes = params.nodes || 7;
    const coupling = params.coupling || 0.8;  // Reduced
    const baseFreq = params.frequency || 2.0;
    
    let potential = 0;
    for (let n = 0; n < nodes; n++) {
      const angle = (2 * Math.PI * n) / nodes;
      const cx = 0.6 * Math.cos(angle);  // Nodes on circle at r=0.6
      const cy = 0.6 * Math.sin(angle);
      const dist = Math.sqrt((x - cx) ** 2 + (y - cy) ** 2);
      
      potential += coupling * Math.exp(-dist * dist / 0.3);  // Broader gaussians
      potential += 0.2 * baseFreq * Math.sin(n * Math.atan2(y - cy, x - cx));  // Reduced
    }
    
    return potential;
  },

  blackHoleReversal: (x, y, params = {}) => {
    const invRadius = params.inversionRadius || 0.8;
    const strength = params.strength || 2;  // Reduced
    const r = Math.sqrt(x ** 2 + y ** 2) + 0.1;
    
    // Smooth transition instead of sharp inversion
    const ratio = r / invRadius;
    return strength * Math.tanh(2 * (ratio - 1));  // Smooth step function
  },

  informationEntropy: (x, y, params = {}) => {
    const regions = params.regions || 2;
    const temp = params.temperature || 1.0;
    
    const oscillation = Math.sin(regions * Math.PI * x) * Math.sin(regions * Math.PI * y);
    const noise = Math.sin(temp * (x * x + y * y));
    
    return oscillation + 0.3 * noise;
  },

  gaussian: (x, y, params = {}) => {
    const sigma = params.sigma || 0.5;
    return Math.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2));
  }
};
