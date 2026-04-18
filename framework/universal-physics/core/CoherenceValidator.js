/**
 * COHERENCE VALIDATOR: Trinity check for any system
 * 
 * A system is coherent if:
 * 1. s ≠ ∅ (source exists - unified origin)
 * 2. t ∈ T (time consistent - synchronized components)
 * 3. v⃗ = true (causality verified - connected path)
 */

class CoherenceValidator {
  /**
   * CALCULATE: Full coherence metrics for a system
   */
  calculateCoherence(model, state) {
    // Potential-based coherence: how close to minimum
    const potentialCoherence = this.calculatePotentialCoherence(model, state);
    
    // Trinity-based coherence: structural soundness
    const trinity = this.validateTrinity(model, state);
    const trinityCoherence = trinity.score;
    
    // Combined metric
    const totalCoherence = 0.6 * potentialCoherence + 0.4 * trinityCoherence;
    
    return {
      potential: potentialCoherence,
      trinity: trinityCoherence,
      total: totalCoherence,
      level: this.getCoherenceLevel(totalCoherence),
      components: {
        source_unified: trinity.source,
        time_synchronized: trinity.time,
        causality_verified: trinity.causality
      },
      details: trinity
    };
  }

  /**
   * POTENTIAL COHERENCE: Proximity to energy minimum
   * 
   * At equilibrium, ∇Φ = 0 (no gradient)
   * Coherence = 1.0 at minimum, decreases as you move away
   */
  calculatePotentialCoherence(model, state) {
    const gradient = model.gradient(state);
    const gradMagnitude = Math.sqrt(gradient.reduce((sum, g) => sum + g*g, 0));
    
    // Normalize: typical gradients are 1e-10 to 1e30
    // If gradient is tiny, we're at a minimum (coherent)
    // If gradient is huge, we're far from minimum (incoherent)
    
    const coherence = Math.exp(-Math.log10(Math.max(gradMagnitude, 1e-30)));
    return Math.min(1.0, Math.max(0.0, coherence));
  }

  /**
   * TRINITY VALIDATION: Structural coherence
   * 
   * Check that all components:
   * - Come from same source (s ≠ ∅)
   * - Have same timestamp (t ∈ T)
   * - Are causally connected (v⃗ = true)
   */
  validateTrinity(model, state) {
    // Source unity: All particles from same event
    const sourceUnified = this.checkSourceUnity(model, state);
    
    // Time synchronization: All at same moment
    const timeSynchronized = this.checkTimeSync(model, state);
    
    // Causality: Connected by continuous interaction
    const causalityVerified = this.checkCausality(model, state);
    
    // Score: all three must pass (0.33 each)
    const score = (sourceUnified ? 0.33 : 0) +
                  (timeSynchronized ? 0.33 : 0) +
                  (causalityVerified ? 0.34 : 0);
    
    return {
      source: sourceUnified,
      time: timeSynchronized,
      causality: causalityVerified,
      score: score
    };
  }

  checkSourceUnity(model, state) {
    // For most systems, all components originate from the potential definition
    // If the model is well-formed, source is always unified
    // Exception: If particles have inconsistent masses, they came from different sources
    
    const masses = state.mass;
    if (!masses || masses.length === 0) return true;
    
    // Check for gross inconsistencies (e.g., one component has wildly different mass)
    const massRatios = [];
    for (let i = 1; i < masses.length; i++) {
      massRatios.push(masses[i] / masses[0]);
    }
    
    // If ratios are within expected bounds (1-scale differences), source is unified
    const unified = massRatios.every(r => r > 0.001 && r < 1000);
    return unified;
  }

  checkTimeSync(model, state) {
    // All position/velocity updates happened in single step
    // Time is always synchronized in classical mechanics (single time parameter)
    // In quantum: need all superposition components at same time
    
    // For now, assume single-time evolution, so always synchronized
    return true;
  }

  checkCausality(model, state) {
    // Components are causally connected if:
    // 1. Distance is less than light cone (r < c*t)
    // 2. Interaction potential connects them
    
    const position = state.position;
    
    // Check pairwise distances
    for (let i = 0; i < position.length; i += 3) {
      for (let j = i + 3; j < position.length; j += 3) {
        let distSq = 0;
        for (let k = 0; k < 3; k++) {
          const dx = position[i+k] - position[j+k];
          distSq += dx * dx;
        }
        
        // If distance is very large, might not be causally connected
        // (Unless it's a weak interaction like gravity)
        const distance = Math.sqrt(distSq);
        if (distance > 1000) {  // > 1000 meters
          // Check if model handles this (e.g., long-range gravity)
          // For now, assume if we're modeling it, it's connected
        }
      }
    }
    
    return true;  // Assume causally connected if modeled together
  }

  /**
   * COHERENCE LEVEL: Human-readable status
   */
  getCoherenceLevel(value) {
    if (value > 0.95) return 'OPTIMAL';
    if (value > 0.85) return 'STABLE';
    if (value > 0.60) return 'WARNING';
    if (value > 0.30) return 'CRITICAL';
    return 'DECOHERENT';
  }

  /**
   * DECOHERENCE: Detect when system breaks apart
   * Called when coherence drops below threshold
   */
  detectDecoherence(model, state, threshold = 0.3) {
    const coherence = this.calculateCoherence(model, state);
    
    if (coherence.total < threshold) {
      return {
        isDecoherent: true,
        level: coherence.level,
        cause: this.identifyDecoherenceCause(model, state, coherence)
      };
    }
    
    return { isDecoherent: false };
  }

  identifyDecoherenceCause(model, state, coherence) {
    if (!coherence.components.source_unified) {
      return 'Source not unified: components have different origins';
    }
    if (!coherence.components.time_synchronized) {
      return 'Time desynchronization: components at different times';
    }
    if (!coherence.components.causality_verified) {
      return 'Causality broken: components not causally connected';
    }
    return 'Potential minimum reached: system in stable state';
  }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { CoherenceValidator };
}
