---
layout: page
title: Domain Mapper - See Patterns Everywhere
permalink: /domain-mapper/
description: Pick a concept, see how it appears in physics, biology, psychology, economics, AI, and more
---

# Domain Mapper

**One principle. Infinite domains. See it everywhere.**

The deepest learning comes from recognizing the SAME pattern appearing in completely different domains.

<style>
.domain-mapper-container {
  margin: 2rem 0;
}

.concept-selector {
  background: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.concept-search {
  margin-bottom: 1.5rem;
}

.concept-search input {
  width: 100%;
  max-width: 500px;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border: 2px solid #ddd;
  border-radius: 4px;
}

.concept-search input:focus {
  outline: none;
  border-color: #2196F3;
  box-shadow: 0 0 4px rgba(33, 150, 243, 0.3);
}

.concept-chips {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}

.chip {
  background: white;
  border: 2px solid #ddd;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.chip:hover {
  border-color: #2196F3;
  background: #e3f2fd;
}

.chip.active {
  background: #2196F3;
  color: white;
  border-color: #2196F3;
}

.domain-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.domain-card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.3s;
  cursor: pointer;
}

.domain-card:hover {
  border-color: #2196F3;
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.15);
  transform: translateY(-3px);
}

.domain-card.active {
  border-color: #2196F3;
  background: #f0f8ff;
}

.domain-icon {
  font-size: 2rem;
  margin-bottom: 0.75rem;
}

.domain-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.domain-description {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.domain-example {
  background: #f9f9f9;
  border-left: 3px solid #2196F3;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.domain-example strong {
  color: #2196F3;
}

.example-label {
  font-size: 0.8rem;
  color: #999;
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: 0.25rem;
}

.comparison-view {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 2rem;
  margin: 2rem 0;
}

.comparison-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #eee;
}

.comparison-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.comparison-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1rem;
}

.equation-block {
  background: #f3e5f5;
  border-left: 4px solid #9C27B0;
  padding: 1.5rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.95rem;
  margin: 1rem 0;
}

.universal-equation {
  background: #e8f5e9;
  border-left: 4px solid #4CAF50;
  padding: 1.5rem;
  border-radius: 4px;
  font-size: 1rem;
  margin: 1rem 0;
  font-weight: 600;
}

.domain-equations {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 1.5rem 0;
}

.equation-card {
  background: #f9f9f9;
  border: 1px solid #ddd;
  padding: 1rem;
  border-radius: 6px;
}

.equation-domain {
  font-weight: 600;
  color: #2196F3;
  font-size: 0.9rem;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.equation-text {
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  color: #333;
  line-height: 1.6;
}

.insights-section {
  background: #fff3e0;
  border-left: 4px solid #ff9800;
  padding: 1.5rem;
  border-radius: 4px;
  margin: 1.5rem 0;
}

.insights-title {
  font-weight: 600;
  color: #e65100;
  margin-bottom: 0.75rem;
}

.insights-list {
  list-style: none;
  padding: 0;
}

.insights-list li {
  padding: 0.5rem 0;
  color: #333;
}

.insights-list li:before {
  content: "💡 ";
  margin-right: 0.5rem;
}

.export-comparison {
  text-align: center;
  margin-top: 2rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 4px;
}

.export-btn {
  background: #2196F3;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.export-btn:hover {
  background: #1976D2;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #999;
}

.empty-state p {
  font-size: 1.1rem;
  margin: 0.5rem 0;
}
</style>

<div class="domain-mapper-container">

<div class="concept-selector">
  <h3 style="margin-top: 0;">What concept do you want to trace?</h3>
  
  <div class="concept-search">
    <input type="text" id="concept-search" placeholder="Search: gradient, energy, stability, learning, equilibrium..." onkeyup="updateConceptSearch(this.value)">
  </div>

  <div class="concept-chips" id="concept-chips">
    <!-- Populated by JavaScript -->
  </div>
</div>

<div class="comparison-view" id="comparison-container">
  <div class="empty-state">
    <p>👆 Select a concept above to see how it appears in different domains</p>
    <p style="font-size: 0.95rem; color: #bbb;">Try: "energy minimization", "stability", "growth", "descent", "convergence"</p>
  </div>
</div>

</div>

<script>
// Comprehensive mapping of concepts across domains
const conceptMapping = {
  "energy-minimization": {
    title: "Energy Minimization (Potential Flow)",
    universal: "dℹ/dt = -∇Φ — all systems flow downhill in potential",
    domains: {
      physics: {
        icon: "⚛️",
        name: "Physics",
        description: "Particles and waves",
        example: "Electron falls into lowest-energy orbital around nucleus",
        equation: "Electron potential energy: E = -13.6 eV / n²",
        insight: "Lower energy = more stable, naturally preferred"
      },
      chemistry: {
        icon: "🧪",
        name: "Chemistry",
        description: "Molecular bonds and reactions",
        example: "Reactants spontaneously form products with lower enthalpy",
        equation: "ΔG = ΔH - TΔS < 0 (thermodynamically favorable)",
        insight: "Reactions proceed toward lower free energy state"
      },
      biology: {
        icon: "🧬",
        name: "Biology",
        description: "Cells and proteins",
        example: "Protein folds into 3D structure minimizing free energy",
        equation: "Folding: ΔG_fold < 0 (native state is minimum)",
        insight: "Misfolded proteins are unstable and marked for degradation"
      },
      psychology: {
        icon: "🧠",
        name: "Psychology",
        description: "Behavior and learning",
        example: "Neural synapses strengthen via Hebbian learning, reducing prediction error",
        equation: "Learning error: E = (predicted - actual)², minimize by gradient descent",
        insight: "Brain naturally optimizes synapse weights to better predict reality"
      },
      economics: {
        icon: "💰",
        name: "Economics",
        description: "Markets and incentives",
        example: "Market price settles where supply equals demand (equilibrium)",
        equation: "Equilibrium: Supply(P) = Demand(P), ∇price = 0",
        insight: "At equilibrium, no incentive for price to change further"
      },
      ai: {
        icon: "🤖",
        name: "AI & Machine Learning",
        description: "Neural networks and algorithms",
        example: "Neural network minimizes loss function during training",
        equation: "Loss(w) → min via backprop: dLoss/dw = -η∇Loss",
        insight: "Gradient descent is the same algorithm across all ML domains"
      }
    }
  },
  
  "stability-equilibrium": {
    title: "Stability & Equilibrium",
    universal: "Stable configurations are local minima in potential landscape",
    domains: {
      physics: {
        icon: "⚛️",
        name: "Physics",
        description: "Static and dynamic systems",
        example: "Ball in valley stays put (stable) vs ball on hill rolls away (unstable)",
        equation: "Stability: ∂²E/∂x² > 0 (second derivative positive)",
        insight: "Curvature determines whether perturbation is restored or amplified"
      },
      biology: {
        icon: "🧬",
        name: "Biology",
        description: "Organism homeostasis",
        example: "Body temperature stable around 37°C, returns to this if perturbed",
        equation: "Homeostasis: Set point maintained by negative feedback",
        insight: "Biological systems are stable equilibria under perturbation"
      },
      psychology: {
        icon: "🧠",
        name: "Psychology",
        description: "Mental health and habits",
        example: "Habit is stable attractor state; breaking requires energy",
        equation: "Habit strength ~ entrenchment in neural weight space",
        insight: "Strong habits resist change (high stability), weak ones are fragile"
      },
      economics: {
        icon: "💰",
        name: "Economics",
        description: "Market and social dynamics",
        example: "Market monopoly is stable equilibrium; competition perturbs it",
        equation: "Market stability: Profit margin attracts/repels competitors",
        insight: "Equilibrium can be stable or unstable depending on feedback"
      },
      sociology: {
        icon: "👥",
        name: "Sociology",
        description: "Social systems and cultures",
        example: "Cultural traditions persist (stable), paradigm shifts are rare (barriers)",
        equation: "Culture stability: Barrier to change = cost of norm violation",
        insight: "Social systems have stability barriers like physical potentials"
      }
    }
  },

  "gradient-descent": {
    title: "Gradient Descent (Downhill Flow)",
    universal: "Every system naturally flows in direction of steepest descent",
    domains: {
      physics: {
        icon: "⚛️",
        name: "Physics",
        description: "Motion and forces",
        example: "Water always flows downhill, not uphill",
        equation: "Force = -∇Φ (force points opposite to potential gradient)",
        insight: "Gradient indicates direction of steepest change"
      },
      ai: {
        icon: "🤖",
        name: "AI & Machine Learning",
        description: "Model training",
        example: "Backpropagation computes loss gradient, updates weights opposite direction",
        equation: "w_new = w_old - η * ∇Loss(w)",
        insight: "Same algorithm used in all deep learning"
      },
      psychology: {
        icon: "🧠",
        name: "Psychology",
        description: "Decision making",
        example: "People naturally avoid pain (negative gradient) and seek pleasure",
        equation: "Behavior: Move toward reward, away from punishment",
        insight: "Behavioral gradient descent is visible in learning animals"
      },
      biology: {
        icon: "🧬",
        name: "Biology",
        description: "Evolution",
        example: "Natural selection is gradient descent on fitness landscape",
        equation: "Fitness gradient: dW/dt = selection pressure",
        insight: "Evolution approximates gradient descent in genetic space"
      }
    }
  },

  "learning-growth": {
    title: "Learning & Growth",
    universal: "Systems improve capability (reduce error) through repeated exposure",
    domains: {
      psychology: {
        icon: "🧠",
        name: "Psychology",
        description: "Behavioral learning",
        example: "Student gradually masters math through practice and feedback",
        equation: "Learning: Skill ∝ Practice, S(t) = S_max * (1 - e^(-t/τ))",
        insight: "Learning follows predictable S-curve: slow→fast→plateaus"
      },
      biology: {
        icon: "🧬",
        name: "Biology",
        description: "Adaptation",
        example: "Immune system learns to recognize pathogen, mounts faster response",
        equation: "Immune memory: Antibody affinity improves through selection",
        insight: "Immune system is learning system discovering optimal response"
      },
      education: {
        icon: "📚",
        name: "Education",
        description: "Knowledge acquisition",
        example: "Teacher guides student from confusion to mastery",
        equation: "Scaffolding: Support gradually reduced as competence grows",
        insight: "Help system mirrors learning curve: Guided → Autonomous"
      },
      ai: {
        icon: "🤖",
        name: "AI & Machine Learning",
        description: "Model improvement",
        example: "Neural network performance improves with more data and training",
        equation: "Validation loss: L(epoch) decreases toward minimum",
        insight: "Machine learning directly implements biological learning principles"
      }
    }
  },

  "complexity-emergence": {
    title: "Complexity & Emergence",
    universal: "Simple rules → complex patterns → novel properties (not predictable from parts)",
    domains: {
      physics: {
        icon: "⚛️",
        name: "Physics",
        description: "Phase transitions",
        example: "Simple H₂O molecules → ice crystal shows new properties (rigidity)",
        equation: "Phase transition: Collective behavior at critical point",
        insight: "Emergent properties arise from interaction symmetry-breaking"
      },
      biology: {
        icon: "🧬",
        name: "Biology",
        description: "Life itself",
        example: "Simple molecules → cells → consciousness (not predictable)",
        equation: "Cannot predict consciousness from biochemistry alone",
        insight: "Emergence explains why life is more than chemistry"
      },
      neuroscience: {
        icon: "🧠",
        name: "Neuroscience",
        description: "Consciousness and mind",
        example: "Single neurons ↔ thought, feeling, decision (emergence)",
        equation: "Thought: Emerges from neural activity pattern",
        insight: "No single neuron 'contains' thought, emerges from network"
      },
      economics: {
        icon: "💰",
        name: "Economics",
        description: "Market dynamics",
        example: "Individual traders → market crashes (emergent phenomenon)",
        equation: "Macro patterns not predictable from individual decisions",
        insight: "Market crashes emerge from individual rational choices"
      },
      sociology: {
        icon: "👥",
        name: "Sociology",
        description: "Culture and institutions",
        example: "Individual believers → organized religion with emergent properties",
        equation: "Culture emerges from individual interactions",
        insight: "Society exhibits properties no individual possesses"
      }
    }
  }
};

// Initialize
function initializeConceptChips() {
  const container = document.getElementById('concept-chips');
  container.innerHTML = '';
  
  Object.keys(conceptMapping).forEach(key => {
    const concept = conceptMapping[key];
    const chip = document.createElement('button');
    chip.className = 'chip';
    chip.textContent = concept.title;
    chip.onclick = () => selectConcept(key);
    container.appendChild(chip);
  });
}

function selectConcept(conceptKey) {
  const concept = conceptMapping[conceptKey];
  document.querySelectorAll('.chip').forEach(chip => chip.classList.remove('active'));
  event.target.classList.add('active');
  
  renderComparison(concept);
  scrollToComparison();
}

function renderComparison(concept) {
  const container = document.getElementById('comparison-container');
  
  let html = `
    <div class="comparison-section">
      <div class="comparison-title">${concept.title}</div>
      <div class="universal-equation">
        🌍 Universal Principle: ${concept.universal}
      </div>
    </div>
  `;
  
  // Render domain cards
  html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin: 2rem 0;">';
  
  Object.entries(concept.domains).forEach(([domainKey, domain]) => {
    html += `
      <div class="domain-card">
        <div class="domain-icon">${domain.icon}</div>
        <div class="domain-name">${domain.name}</div>
        <div class="domain-description">${domain.description}</div>
        
        <div class="domain-example">
          <div class="example-label">Real Example</div>
          <p style="margin: 0.5rem 0; color: #333;">${domain.example}</p>
          
          <div class="example-label" style="margin-top: 0.75rem;">How it works</div>
          <div class="equation-text">${domain.equation}</div>
          
          <div class="example-label" style="margin-top: 0.75rem;">Key insight</div>
          <p style="margin: 0.25rem 0; font-size: 0.85rem; color: #666;">${domain.insight}</p>
        </div>
      </div>
    `;
  });
  
  html += '</div>';
  
  // Add insights section
  html += `
    <div class="insights-section">
      <div class="insights-title">🔍 Cross-Domain Insights</div>
      <ul class="insights-list">
        <li><strong>Universal pattern:</strong> ${concept.universal}</li>
        <li><strong>Why it matters:</strong> Understanding in one domain helps predict in others</li>
        <li><strong>Practical use:</strong> If you understand the principle in physics, you understand it in AI training</li>
        <li><strong>Deep insight:</strong> Same mathematics describes ${Object.keys(concept.domains).length} completely different phenomena</li>
      </ul>
    </div>
  `;
  
  html += `
    <div class="export-comparison">
      <button class="export-btn" onclick="exportComparison('${Object.keys(conceptMapping).find(k => conceptMapping[k].title === concept.title)}')">
        📥 Export this comparison
      </button>
    </div>
  `;
  
  container.innerHTML = html;
}

function updateConceptSearch(term) {
  const chips = document.querySelectorAll('.chip');
  term = term.toLowerCase();
  
  chips.forEach(chip => {
    const text = chip.textContent.toLowerCase();
    if (text.includes(term) || term === '') {
      chip.style.display = 'inline-block';
    } else {
      chip.style.display = 'none';
    }
  });
}

function scrollToComparison() {
  document.getElementById('comparison-container').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function exportComparison(conceptKey) {
  const concept = conceptMapping[conceptKey];
  let text = `# ${concept.title}\n\n`;
  text += `Universal: ${concept.universal}\n\n`;
  
  Object.entries(concept.domains).forEach(([key, domain]) => {
    text += `## ${domain.name}\n`;
    text += `Example: ${domain.example}\n`;
    text += `Equation: ${domain.equation}\n`;
    text += `Insight: ${domain.insight}\n\n`;
  });
  
  const blob = new Blob([text], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${conceptKey}-domain-map.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// Initialize
window.addEventListener('load', initializeConceptChips);
</script>
