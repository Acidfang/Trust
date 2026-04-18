---
layout: page
title: Framework Comparison Matrix
permalink: /frameworks-comparison/
description: See which frameworks apply to which domains, and which one to use for your situation
---

# Framework Comparison Matrix

**Not all frameworks fit all situations. This matrix shows which frameworks best explain which domains.**

<style>
.comparison-container {
  margin: 2rem 0;
  overflow-x: auto;
}

.matrix-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-radius: 8px;
  overflow: hidden;
}

.matrix-table th,
.matrix-table td {
  padding: 1.25rem;
  text-align: center;
  border: 1px solid #e0e0e0;
}

.matrix-table th {
  background: #f5f5f5;
  font-weight: 600;
  color: #333;
}

.matrix-table th:first-child {
  text-align: left;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.matrix-table td {
  position: relative;
}

.matrix-table tr:hover {
  background: #f9f9f9;
}

.fit-indicator {
  display: inline-block;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  cursor: help;
  position: relative;
}

.fit-excellent {
  background: #e8f5e9;
  color: #2e7d32;
  border: 2px solid #4CAF50;
}

.fit-good {
  background: #fff3e0;
  color: #e65100;
  border: 2px solid #ff9800;
}

.fit-moderate {
  background: #e3f2fd;
  color: #1565C0;
  border: 2px solid #2196F3;
}

.fit-poor {
  background: #ffebee;
  color: #c62828;
  border: 2px solid #f44336;
}

.fit-tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: #333;
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
  z-index: 10;
  margin-bottom: 5px;
}

.fit-indicator:hover .fit-tooltip {
  opacity: 1;
}

.legend {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f9f9f9;
  border-radius: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.legend-dot {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.8rem;
}

.legend-text {
  font-size: 0.9rem;
  color: #666;
}

.framework-selector {
  margin: 2rem 0;
  padding: 1.5rem;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.framework-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin: 1rem 0;
}

.framework-btn {
  padding: 1rem;
  border: 2px solid #ddd;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
  text-align: center;
}

.framework-btn:hover {
  border-color: #2196F3;
  background: #e3f2fd;
}

.framework-btn.active {
  border-color: #2196F3;
  background: #2196F3;
  color: white;
}

.detailed-analysis {
  margin-top: 2rem;
  padding: 2rem;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.analysis-section {
  margin-bottom: 2rem;
}

.analysis-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.75rem;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 0.5rem;
}

.domain-list {
  list-style: none;
  padding: 0;
}

.domain-list li {
  padding: 0.5rem 0;
  color: #666;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.domain-list li:before {
  content: '✓';
  color: #2196F3;
  font-weight: 600;
}

.when-to-use {
  background: #e8f5e9;
  border-left: 4px solid #4CAF50;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 4px;
}

.when-not-to-use {
  background: #ffebee;
  border-left: 4px solid #f44336;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 4px;
}

.prerequisites {
  background: #fff3e0;
  border-left: 4px solid #ff9800;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 4px;
}

@media (max-width: 900px) {
  .matrix-table {
    font-size: 0.85rem;
  }
  
  .matrix-table th,
  .matrix-table td {
    padding: 0.75rem;
  }
  
  .fit-indicator {
    width: 30px;
    height: 30px;
    font-size: 0.7rem;
  }
}
</style>

<h2>Which Framework for Which Domain?</h2>

<div style="background: #fff3e0; border: 2px solid #ff9800; border-radius: 8px; padding: 1.5rem; margin-bottom: 2rem;">
  <strong style="color: #e65100; font-size: 1.1rem;">⚠️ CRITICAL: Goal-Blindness is the Root Cause</strong>
  <p style="margin: 0.75rem 0 0 0; color: #333;">
    All other frameworks attempt to solve problems created by goal-blindness. Goal-Blindness is the structural limitation that prevents humans from seeing consequences beyond their own goals.
  </p>
  <p style="margin: 0.5rem 0 0 0; color: #555; font-size: 0.95rem;">
    <strong>Every domain with human decision-makers has this problem.</strong> The column on the left shows the root cause. Other columns show how various systems try (usually ineffectively) to operate despite this blindness.
  </p>
</div>

<div class="legend">
  <div class="legend-item">
    <div class="legend-dot fit-excellent">★</div>
    <div class="legend-text">Excellent fit (95-100%)</div>
  </div>
  <div class="legend-item">
    <div class="legend-dot fit-good">✓</div>
    <div class="legend-text">Good fit (75-94%)</div>
  </div>
  <div class="legend-item">
    <div class="legend-dot fit-moderate">◐</div>
    <div class="legend-text">Moderate fit (50-74%)</div>
  </div>
  <div class="legend-item">
    <div class="legend-dot fit-poor">✗</div>
    <div class="legend-text">Poor fit (&lt;50%)</div>
  </div>
</div>

<div class="comparison-container">
  <table class="matrix-table">
    <thead>
      <tr>
        <th>Domain</th>
        <th title="Root cause: structural cognitive blindness to consequences for others">🔴 Goal-Blindness<br/><small>Root Cause</small></th>
        <th title="Energy minimization, potential gradients, evolution">Universal Foundation<br/><small>dℹ/dt = -∇Φ</small></th>
        <th title="Learning, growth, autonomy, support">Help Systems<br/><small>Scaffolding</small></th>
        <th title="History, emergence, cosmic evolution">Cosmic Eras<br/><small>Evolution</small></th>
        <th title="Computation, logic, verification">Binary Logic<br/><small>Computing</small></th>
      </tr>
    </thead>
    <tbody>
      <!-- Physics -->
      <tr>
        <td><strong>Physics</strong><br/><small>(Particles, atoms, fields)</small></td>
        <td><div class="fit-indicator fit-poor" title="Not human decision-making"><span>✗</span><div class="fit-tooltip">Particles don't have goals</div></div></td>
        <td><div class="fit-indicator fit-excellent" title="Fundamental law of physics"><span>★</span><div class="fit-tooltip">Describes all motion and interactions</div></div></td>
        <td><div class="fit-indicator fit-poor" title="Not applicable"><span>✗</span><div class="fit-tooltip">Help systems don't apply to particles</div></div></td>
        <td><div class="fit-indicator fit-moderate" title="Somewhat relevant"><span>◐</span><div class="fit-tooltip">History of universe interesting context</div></div></td>
        <td><div class="fit-indicator fit-moderate" title="Quantum mechanics"><span>◐</span><div class="fit-tooltip">Quantum computing uses binary logic</div></div></td>
      </tr>
      
      <!-- Chemistry -->
      <tr>
        <td><strong>Chemistry</strong><br/><small>(Reactions, bonding, kinetics)</small></td>
        <td><div class="fit-indicator fit-poor"><span>✗</span><div class="fit-tooltip">Molecular reactions lack intent</div></div></td>
        <td><div class="fit-indicator fit-excellent" title="Central principle"><span>★</span><div class="fit-tooltip">Explains molecule formation, reactions</div></div></td>
        <td><div class="fit-indicator fit-poor"><span>✗</span><div class="fit-tooltip">Not applicable</div></div></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Chemical evolution interesting</div></div></td>
        <td><div class="fit-indicator fit-moderate"><span>◐</span><div class="fit-tooltip">Quantum chemistry uses computation</div></div></td>
      </tr>
      
      <!-- Biology (Molecular) -->
      <tr>
        <td><strong>Biology: Molecular</strong><br/><small>(Protein folding, genetics)</small></td>
        <td><div class="fit-indicator fit-poor"><span>✗</span><div class="fit-tooltip">Molecular mechanisms lack agency</div></div></td>
        <td><div class="fit-indicator fit-excellent"><span>★</span><div class="fit-tooltip">Protein folding, RNA structure</div></div></td>
        <td><div class="fit-indicator fit-moderate"><span>◐</span><div class="fit-tooltip">Relevant to development</div></div></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Evolution of life mechanisms</div></div></td>
        <td><div class="fit-indicator fit-moderate"><span>◐</span><div class="fit-tooltip">Bioinformatics uses computing</div></div></td>
      </tr>
      
      <!-- Biology (Organismal) -->
      <tr>
        <td><strong>Biology: Organismal</strong><br/><small>(Anatomy, physiology, homeostasis)</small></td>
        <td><div class="fit-indicator fit-poor"><span>✗</span><div class="fit-tooltip">Organisms follow instinct, not goals</div></div></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Homeostasis as equilibrium</div></div></td>
        <td><div class="fit-indicator fit-moderate"><span>◐</span><div class="fit-tooltip">Development uses scaffolding</div></div></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Evolution shaped current forms</div></div></td>
        <td><div class="fit-indicator fit-moderate"><span>◐</span><div class="fit-tooltip">Simulation of systems</div></div></td>
      </tr>
      
      <!-- Ecology -->
      <tr>
        <td><strong>Ecology</strong><br/><small>(Ecosystems, succession, evolution)</small></td>
        <td><div class="fit-indicator fit-moderate"><span>◐</span><div class="fit-tooltip">Species pursue survival, but no institutions</div></div></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Ecosystem stability, energy flow</div></div></td>
        <td><div class="fit-indicator fit-poor"><span>✗</span><div class="fit-tooltip">Not applicable</div></div></td>
        <td><div class="fit-indicator fit-excellent"><span>★</span><div class="fit-tooltip">Succession as evolutionary process</div></div></td>
        <td><div class="fit-indicator fit-moderate"><span>◐</span><div class="fit-tooltip">Modeling ecosystems</div></div></td>
      </tr>
      
      <!-- Neuroscience -->
      <tr>
        <td><strong>Neuroscience</strong><br/><small>(Brain, learning, consciousness)</small></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Brain limitations cause cognitive blindness</div></div></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Synaptic plasticity follows gradients</div></div></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Scaffolding in skill learning</div></div></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Evolution of brain</div></div></td>
        <td><div class="fit-indicator fit-excellent"><span>★</span><div class="fit-tooltip">Neural circuits, neural computation</div></div></td>
      </tr>
      
      <!-- Psychology -->
      <tr>
        <td><strong>Psychology</strong><br/><small>(Behavior, learning, emotion)</small></td>
        <td><div class="fit-indicator fit-excellent"><span>★</span><div class="fit-tooltip">Core mechanism: cannot see beyond own goals/feelings</div></div></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Motivation as gradient, habit formation</div></div></td>
        <td><div class="fit-indicator fit-excellent"><span>★</span><div class="fit-tooltip">Central to learning and behavioral change</div></div></td>
        <td><div class="fit-indicator fit-moderate"><span>◐</span><div class="fit-tooltip">Psychological development stages</div></div></td>
        <td><div class="fit-indicator fit-moderate"><span>◐</span><div class="fit-tooltip">Decision-making algorithms</div></div></td>
      </tr>
      
      <!-- Education -->
      <tr>
        <td><strong>Education</strong><br/><small>(Teaching, learning, instruction)</small></td>
        <td><div class="fit-indicator fit-excellent"><span>★</span><div class="fit-tooltip">Teachers' helping-goal blinds to gate-prevention</div></div></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Learning curves as energy minimization</div></div></td>
        <td><div class="fit-indicator fit-excellent"><span>★</span><div class="fit-tooltip">Scaffolding, gradual release of responsibility</div></div></td>
        <td><div class="fit-indicator fit-moderate"><span>◐</span><div class="fit-tooltip">Historical context of knowledge</div></div></td>
        <td><div class="fit-indicator fit-moderate"><span>◐</span><div class="fit-tooltip">Educational technology, AI tutoring</div></div></td>
      </tr>
      
      <!-- Economics -->
      <tr>
        <td><strong>Economics</strong><br/><small>(Markets, pricing, incentives)</small></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Actors blind to externalities outside their goals</div></div></td>
        <td><div class="fit-indicator fit-excellent"><span>★</span><div class="fit-tooltip">Price discovery, equilibrium, optimization</div></div></td>
        <td><div class="fit-indicator fit-moderate"><span>◐</span><div class="fit-tooltip">Human development relevant</div></div></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Economic history, institutional evolution</div></div></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Algorithmic trading, ML in finance</div></div></td>
      </tr>
      
      <!-- Sociology -->
      <tr>
        <td><strong>Sociology</strong><br/><small>(Culture, institutions, social dynamics)</small></td>
        <td><div class="fit-indicator fit-excellent"><span>★</span><div class="fit-tooltip">Goal-blind institutions perpetuate blockage mechanisms</div></div></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Social equilibrium, polarization dynamics</div></div></td>
        <td><div class="fit-indicator fit-moderate"><span>◐</span><div class="fit-tooltip">Cultural transmission has scaffolding</div></div></td>
        <td><div class="fit-indicator fit-excellent"><span>★</span><div class="fit-tooltip">Evolution of institutions and culture</div></div></td>
        <td><div class="fit-indicator fit-moderate"><span>◐</span><div class="fit-tooltip">Agent-based modeling of social dynamics</div></div></td>
      </tr>
      
      <!-- Technology / AI -->
      <tr>
        <td><strong>Technology & AI</strong><br/><small>(Algorithms, neural networks, software)</small></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Tech companies blind to society-scale consequences</div></div></td>
        <td><div class="fit-indicator fit-excellent"><span>★</span><div class="fit-tooltip">Gradient descent in all ML, optimization</div></div></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Curriculum learning, Socratic methods</div></div></td>
        <td><div class="fit-indicator fit-moderate"><span>◐</span><div class="fit-tooltip">Evolution of technology, novelty</div></div></td>
        <td><div class="fit-indicator fit-excellent"><span>★</span><div class="fit-tooltip">Foundation of all computing</div></div></td>
      </tr>
      
      <!-- Medicine -->
      <tr>
        <td><strong>Medicine</strong><br/><small>(Disease, treatment, health)</small></td>
        <td><div class="fit-indicator fit-excellent"><span>★</span><div class="fit-tooltip">Regulators' safety-goal blinds to delay-deaths</div></div></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Physiological equilibrium, disease as dysregulation</div></div></td>
        <td><div class="fit-indicator fit-good"><span>✓</span><div class="fit-tooltip">Patient education, behavior change</div></div></td>
        <td><div class="fit-indicator fit-moderate"><span>◐</span><div class="fit-tooltip">Evolution of disease resistance</div></div></td>
        <td><div class="fit-indicator fit-moderate"><span>◐</span><div class="fit-tooltip">Diagnostic AI, treatment algorithms</div></div></td>
      </tr>
    </tbody>
  </table>
</div>

<h2>Deep-Dive Analysis</h2>

<div class="framework-selector">
  <strong>Select a framework for detailed analysis:</strong>
  <div class="framework-buttons">
    <button class="framework-btn" onclick="showFrameworkDetail('goalblindness')">Goal-Blindness (Root)</button>
    <button class="framework-btn" onclick="showFrameworkDetail('universal')">Universal Foundation</button>
    <button class="framework-btn" onclick="showFrameworkDetail('help')">Help Systems</button>
    <button class="framework-btn" onclick="showFrameworkDetail('eras')">Cosmic Eras</button>
    <button class="framework-btn" onclick="showFrameworkDetail('binary')">Binary Logic</button>
  </div>
</div>

<div id="detail-content"></div>

<script>
const frameworkDetails = {
  goalblindness: {
    title: 'Goal-Blindness: The Root Cause',
    bestFor: ['Psychology', 'Education', 'Medicine', 'Sociology', 'Economics', 'Parenting', 'Management'],
    whenToUse: 'When you need to understand WHY help systems prevent development, WHY institutions block advancement, WHY people perpetuate harm they don\'t see. When you need to design systems that measure what people are blind to.',
    whenNotToUse: 'Goal-blindness applies to all human decision-making, so it ALWAYS applies when humans are involved.',
    prerequisites: 'No technical background. Just the ability to recognize: "I can\'t think past my own goals and see consequences to others."',
    relatedFrameworks: ['Help Systems (manifestation of goal-blindness at individual scale)', 'Institutional blockage mechanisms (manifestation of goal-blindness at institutional scale)', 'Universal Foundation (what happens when blindness prevents optimization)'],
    keywords: ['blindness', 'goals', 'consequences', 'measurement', 'externalities', 'feedback', 'accountability']
  },
  
  universal: {
    title: 'Universal Foundation: dℹ/dt = -∇Φ',
    bestFor: ['Physics', 'Chemistry', 'AI & Machine Learning', 'Economics', 'Neuroscience'],
    whenToUse: 'When you need to understand why systems change, reach equilibrium, or optimize. Best for understanding the deep mechanism of change across all domains.',
    whenNotToUse: 'When you need practical guidance on teaching/coaching (use Help Systems). When you care about historical context more than mechanisms (use Cosmic Eras).',
    prerequisites: 'Comfortable with calculus and differential equations recommended, but physics intuition works without math.',
    relatedFrameworks: ['Help Systems (what drives change in learning)', 'Cosmic Eras (evolution of systems)', 'Binary Logic (discrete version of gradient descent)'],
    keywords: ['gradient descent', 'optimization', 'energy minimization', 'equilibrium', 'stability', 'evolution', 'change']
  },
  
  help: {
    title: 'Help Systems Framework',
    bestFor: ['Education', 'Psychology', 'Coaching', 'Management', 'Parenting', 'Therapy'],
    whenToUse: 'When you\'re helping someone grow or learn. When you need to decide what level of support/autonomy to offer at each stage.',
    whenNotToUse: 'When dealing with physical systems (use Universal Foundation). When focus is historical evolution (use Cosmic Eras). For implementing algorithms (use Binary Logic).',
    prerequisites: 'No technical background needed. Based on observing how teachers, coaches, therapists actually help.',
    relatedFrameworks: ['Universal Foundation (why people improve through learning)', 'Cosmic Eras (development stages)', 'Psychology research (empirical foundation)'],
    keywords: ['autonomy', 'scaffolding', 'support', 'guided', 'coaching', 'teaching', 'growth']
  },
  
  eras: {
    title: 'Cosmic Eras Framework',
    bestFor: ['Cosmology', 'Evolutionary Biology', 'History', 'Sociology', 'Technology Evolution', 'Anthropology'],
    whenToUse: 'When you want to understand how complex things evolved from simpler precursors. When tracing the "why" of current state through history.',
    whenNotToUse: 'When you need to understand mechanisms of current systems (use Universal Foundation). When helping someone learn/change (use Help Systems).',
    prerequisites: 'Broad knowledge helpful but narrative thinking is primary tool. Works without technical background.',
    relatedFrameworks: ['Universal Foundation (mechanism of change within each era)', 'Emergence (how new properties arise)'],
    keywords: ['evolution', 'emergence', 'history', 'progression', 'eras', 'stages', 'novelty']
  },
  
  binary: {
    title: 'Binary Computing Logic & Self-Verification',
    bestFor: ['Computer Science', 'AI & Machine Learning', 'Formal Verification', 'Logic', 'Algorithm Design'],
    whenToUse: 'When designing systems (state machines, circuits, protocols). When verifying correctness of computational systems. When working with discrete systems.',
    whenNotToUse: 'When dealing with continuous physical systems (use Universal Foundation). When helping people (use Help Systems). When tracing history (use Cosmic Eras).',
    prerequisites: 'Computer science or programming background helpful. Boolean logic fundamentals required.',
    relatedFrameworks: ['Universal Foundation (continuous version)', 'Physics (quantum computing bridge)'],
    keywords: ['state machine', 'logic gates', 'verification', 'computation', 'algorithm', 'discrete', 'binary']
  }
};

function showFrameworkDetail(framework) {
  const detail = frameworkDetails[framework];
  if (!detail) return;
  
  const html = `
    <div class="detailed-analysis">
      <h3>${detail.title}</h3>
      
      <div class="analysis-section">
        <div class="analysis-title">✓ Best For</div>
        <ul class="domain-list">
          ${detail.bestFor.map(d => `<li>${d}</li>`).join('')}
        </ul>
      </div>
      
      <div class="analysis-section">
        <div class="when-to-use">
          <div class="analysis-title" style="border: none; margin: 0; padding: 0; color: #2e7d32;">When To Use</div>
          <p style="margin: 0.5rem 0 0 0; color: #2e7d32;">${detail.whenToUse}</p>
        </div>
      </div>
      
      <div class="analysis-section">
        <div class="when-not-to-use">
          <div class="analysis-title" style="border: none; margin: 0; padding: 0; color: #c62828;">When NOT To Use</div>
          <p style="margin: 0.5rem 0 0 0; color: #c62828;">${detail.whenNotToUse}</p>
        </div>
      </div>
      
      <div class="analysis-section">
        <div class="prerequisites">
          <div class="analysis-title" style="border: none; margin: 0; padding: 0; color: #e65100;">Prerequisites / Background Helpful For</div>
          <p style="margin: 0.5rem 0 0 0; color: #e65100;">${detail.prerequisites}</p>
        </div>
      </div>
      
      <div class="analysis-section">
        <div class="analysis-title">Related Frameworks</div>
        <ul class="domain-list">
          ${detail.relatedFrameworks.map(f => `<li>${f}</li>`).join('')}
        </ul>
      </div>
      
      <div class="analysis-section">
        <div class="analysis-title">Key Concepts</div>
        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
          ${detail.keywords.map(k => `<span style="background: #e3f2fd; color: #1976D2; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.85rem;">${k}</span>`).join('')}
        </div>
      </div>
    </div>
  `;
  
  const buttons = document.querySelectorAll('.framework-btn');
  buttons.forEach(b => {
    b.classList.remove('active');
    if (b.textContent.includes(detail.title.split(':')[0])) {
      b.classList.add('active');
    }
  });
  
  document.getElementById('detail-content').innerHTML = html;
  document.getElementById('detail-content').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Initialize
window.addEventListener('load', () => {
  showFrameworkDetail('universal');
});
</script>
