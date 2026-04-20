// TIER -1 (BOUND): Input validation and error setup
// TIER 0 (FREE): Explore possibilities
// TIER 1 (BOUND): Lock in root-cause logic
// TIER 2 (FREE): Verify consistency
// TIER 3+ (BOUND): Automate return and integrate

/**
 * EVOLUTION ENGINE: Apply dℹ/dt = -∇Φ
 * 
 * The universal law that drives all coherent systems forward in time
 */

class EvolutionEngine {
  constructor(model, state) {
    this.model = model;
    this.state = state;
    this.time = 0;
    this.dt = 1e-6;                    // Default: 1 microsecond
    this.autoAdjustTimestep = true;
    this.energyHistory = [];
  }

  /**
   * STEP: One time increment
   * 
   * Uses Verlet integration (symplectic, energy-conserving)
   * x(t+dt) = x(t) + v(t)*dt + 0.5*a(t)*dt²
   * v(t+dt) = v(t) + 0.5*(a(t) + a(t+dt))*dt
   */
  step() {
    // Calculate gradient at current position
    const gradient = this.model.gradient(this.state);
    
    // Update accelerations: a = -∇Φ/m
    for (let i = 0; i < this.state.dimensions; i++) {
      this.state.acceleration[i] = -gradient[i] / this.state.mass[i];
    }
    
    // Verlet: Update positions
    for (let i = 0; i < this.state.dimensions; i++) {
      const pos = this.state.position[i];
      const vel = this.state.velocity[i];
      const acc = this.state.acceleration[i];
      
      this.state.position[i] = pos + vel * this.dt + 0.5 * acc * this.dt * this.dt;
    }
    
    // Recalculate gradient at new position
    const gradientNew = this.model.gradient(this.state);
    
    // Verlet: Update velocities
    for (let i = 0; i < this.state.dimensions; i++) {
      const accNew = -gradientNew[i] / this.state.mass[i];
      this.state.velocity[i] += 0.5 * (this.state.acceleration[i] + accNew) * this.dt;
    }
    
    this.time += this.dt;
    
    // Adaptive timestep (optional)
    if (this.autoAdjustTimestep) {
      this.adjustTimestep();
    }
  }

  /**
   * RUN: Evolve system for specified duration
   */
  run(durationSeconds, logInterval = 100) {
    const startTime = this.time;
    const targetTime = this.time + durationSeconds;
    let stepCount = 0;
    
    while (this.time < targetTime) {
      this.step();
      stepCount++;
      
      if (stepCount % logInterval === 0) {
        const progress = ((this.time - startTime) / durationSeconds) * 100;
        process.stdout.write(`\rProgress: ${progress.toFixed(1)}%`);
      }
    }
    
    console.log('\n✓ Simulation complete');
  }

  /**
   * FIND EQUILIBRIUM: Run until gradient is zero
   */
  findEquilibrium(maxSteps = 100000, gradientThreshold = 1e-10) {
    let stepCount = 0;
    
    while (stepCount < maxSteps) {
      const gradient = this.model.gradient(this.state);
      const gradMagnitude = Math.sqrt(gradient.reduce((sum, g) => sum + g*g, 0));
      
      if (gradMagnitude < gradientThreshold) {
        console.log(`✓ Equilibrium found at step ${stepCount}`);
        return true;
      }
      
      this.step();
      stepCount++;
      
      if (stepCount % 1000 === 0) {
        process.stdout.write(`\rSearching equilibrium... step ${stepCount}, gradient ${gradMagnitude.toExponential(2)}`);
      }
    }
    
    console.log('\n⚠ Did not converge to equilibrium');
    return false;
  }

  /**
   * ADJUST TIMESTEP: Automatic step size control
   */
  adjustTimestep() {
    const energy = this.calculateTotalEnergy();
    this.energyHistory.push(energy);
    
    if (this.energyHistory.length > 10) {
      const recent = this.energyHistory.slice(-10);
      const variance = this.calculateVariance(recent);
      
      // If energy is oscillating too much, reduce timestep
      if (variance > 0.01) {
        this.dt *= 0.95;  // Reduce by 5%
      } else if (variance < 0.001) {
        this.dt *= 1.02;  // Increase by 2%
      }
      
      // Keep within reasonable bounds
      this.dt = Math.max(1e-9, Math.min(1e-4, this.dt));
    }
  }

  calculateTotalEnergy() {
    const potential = this.model.potentialFunction(this.state);
    let kinetic = 0;
    
    for (let i = 0; i < this.state.dimensions; i++) {
      kinetic += 0.5 * this.state.mass[i] * this.state.velocity[i] * this.state.velocity[i];
    }
    
    return potential + kinetic;
  }

  calculateVariance(values) {
    const mean = values.reduce((a, b) => a + b, 0) / values.length;
    const squaredDiffs = values.map(v => (v - mean) * (v - mean));
    return squaredDiffs.reduce((a, b) => a + b, 0) / values.length;
  }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { EvolutionEngine };
}
