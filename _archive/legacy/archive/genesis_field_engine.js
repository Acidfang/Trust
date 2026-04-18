/**
 * GENESIS FIELD ENGINE — The Core Physics of Choice
 * 
 * Logic based on the protocol: 
 * - Absence = High Potential
 * - n=1 = Single Electron Sea (Universal Field)
 * - n>=2 = Presence (Election)
 * - Gravity = Apex Return
 */

class GenesisField {
    constructor() {
        this.electrons = []; // Presence points (n>=2)
        this.potentialSea = 1.0; // The n=1 baseline (0 to 1)
        this.c = 299792458; // The Truth Constraint (normalized in view)
        this.fieldAttributes = {
            coherence: 1.0,
            density: 0,
            gravityGradient: 0
        };
    }

    /**
     * Add an "Election" to the field
     */
    addElectron(x, y, z = 0) {
        const id = `e_${Date.now()}_${Math.floor(Math.random() * 1000)}`;
        const electron = {
            id,
            origin: { x, y, z },
            state: 1, // Start at state 1 (Election)
            radius: 30, // Initial presence
            maxRadius: 150 + Math.random() * 50, // Point of Apex
            phase: 0, // For spiral rotation
            isReturning: false, // Becomes true at Apex
            energy: 1.0 // Normalized energy
        };
        this.electrons.push(electron);
        this.calculateFieldImpact();
        
        // Trigger a field modulation effect across the sea
        this.fieldAttributes.ripple = 1.0;
        
        return id;
    }

    /**
     * Calculate field attributes based on the current set of elections
     * Every addition modifies the baseline attributes of the universal field
     */
    calculateFieldImpact() {
        const n = this.electrons.length + 1; // n=1 is sea base
        
        // The "Absence" (Pure Potential) decreases as Density increases
        // More electrons = more "Mass-like" behavior, less "Void-like" energy
        this.potentialSea = Math.max(0.05, 1.0 / Math.sqrt(n));
        
        // Coherence decreases with complexity (Entropy equivalent)
        this.fieldAttributes.coherence = Math.max(0.1, 1.0 / (1 + Math.log10(n)));
        
        // Density is the literal presence count
        this.fieldAttributes.density = n;
        
        // Gravity Gradient is the cumulative pull of all return-leg signals
        // High n = Deep Gravity Well
        this.fieldAttributes.gravityGradient = this.electrons.filter(e => e.isReturning).length * (n * 0.05);
    }

    /**
     * Update physics for one tick
     */
    update(dt) {
        this.electrons.forEach(e => {
            // Speed of truth (c) is constant
            const baseVelocity = 3.0; 
            
            // Logarithmic Spiral Constant (b in r = a * e^(b*theta))
            const b = 0.30635; // Golden spiral approximate

            if (!e.isReturning) {
                // Outward Expansion (Presence Push)
                e.radius += baseVelocity;
                
                // θ = ln(r/a) / b
                // We derive phase (θ) from radius to lock the dot to the path
                e.phase = Math.log(Math.max(1, e.radius) / 5) / b;

                if (e.radius >= e.maxRadius) {
                    e.isReturning = true; // REACHED APEX
                }
            } else {
                // Inward Flow (Gravity Pull) - Returning to source
                e.radius -= baseVelocity;
                
                // Same geometric lock for return
                e.phase = Math.log(Math.max(1, e.radius) / 5) / b;

                if (e.radius <= 0) {
                    // ELECTRON EXTINGUISHED - Return to Sea (n=1)
                    this.electrons = this.electrons.filter(ele => ele.id !== e.id);
                    this.calculateFieldImpact();
                }
            }
        });
    }

    /**
     * Get UI-ready data
     */
    getStats() {
        return {
            potential: (this.potentialSea * 100).toFixed(2) + '%',
            density: this.fieldAttributes.density,
            coherence: this.fieldAttributes.coherence.toFixed(4),
            returnFlow: this.fieldAttributes.gravityGradient.toFixed(2),
            stateN: `n=${this.electrons.length + 1}`
        };
    }
}

// Global instance for the viewer
window.GenesisPhysics = new GenesisField();
