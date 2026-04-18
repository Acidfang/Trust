---
layout: page
title: Quick Reference Cards
permalink: /quick-reference/
description: Printable one-page guides for key concepts - laminate and carry them
---

# Quick Reference Cards

**One-page summaries of essential concepts. Print them out, laminate them, carry them in your pocket.**

<style>
.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.reference-card {
  background: white;
  border: 2px solid #333;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  font-family: 'Courier New', monospace;
  position: relative;
  page-break-inside: avoid;
  break-inside: avoid;
}

.reference-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 8px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 6px 6px 0 0;
}

.card-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #333;
  margin: 0.5rem 0 1rem 0;
  padding-top: 0.5rem;
  border-bottom: 2px solid #ddd;
  padding-bottom: 0.75rem;
}

.card-section {
  margin: 1rem 0;
  font-size: 0.95rem;
  line-height: 1.6;
}

.card-section-title {
  font-weight: 700;
  color: #333;
  margin: 0.75rem 0 0.5rem 0;
  font-size: 0.9rem;
  text-transform: uppercase;
  border-bottom: 1px solid #ddd;
  padding-bottom: 0.25rem;
}

.card-list {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0;
}

.card-list li {
  padding: 0.25rem 0;
  margin: 0.25rem 0;
  color: #555;
  font-size: 0.9rem;
}

.card-list li::before {
  content: '→ ';
  color: #2196F3;
  font-weight: 700;
  margin-right: 0.5rem;
}

.equation {
  background: #f0f8ff;
  border-left: 3px solid #2196F3;
  padding: 0.75rem;
  margin: 0.5rem 0;
  border-radius: 3px;
  font-size: 0.85rem;
}

.example-box {
  background: #e8f5e9;
  border-left: 3px solid #4CAF50;
  padding: 0.75rem;
  margin: 0.5rem 0;
  border-radius: 3px;
  font-size: 0.85rem;
}

.key-point {
  background: #fff3e0;
  border-left: 3px solid #ff9800;
  padding: 0.75rem;
  margin: 0.5rem 0;
  border-radius: 3px;
  font-size: 0.85rem;
  font-weight: 600;
}

.print-button {
  text-align: center;
  margin: 2rem 0;
}

.print-btn {
  background: #333;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: background 0.2s;
}

.print-btn:hover {
  background: #555;
}

@media print {
  .print-button,
  .intro-section,
  h1,
  h2 {
    display: none;
  }
  
  .card-container {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .reference-card {
    page-break-inside: avoid;
    box-shadow: none;
    border: 1px solid #ccc;
    padding: 1.5rem;
  }
}

.intro-section {
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.copy-note {
  text-align: center;
  color: #999;
  font-size: 0.9rem;
  margin: 1rem 0;
}
</style>

<div class="intro-section">
  <h3 style="margin-top: 0;">📋 How to Use These Cards</h3>
  <p><strong>Print & Laminate:</strong> Click "Print These Cards" → Print on cardstock → Laminate → Carry with you</p>
  <p><strong>Quick Reference:</strong> Use when explaining concepts, teaching, or when you need a fast reminder of the essential points</p>
  <p><strong>Personalize:</strong> Print a set, use a pen to add your own notes and examples</p>
</div>

<div class="print-button">
  <button class="print-btn" onclick="window.print()">📥 Print These Cards</button>
</div>

<div class="card-container">

<!-- Card 1: Universal Foundation -->
<div class="reference-card">
  <div class="card-title">Universal Foundation</div>
  
  <div class="card-section">
    <div class="card-section-title">The Law</div>
    <div class="equation">dℹ/dt = -∇Φ</div>
    <p style="margin-top: 0.5rem; color: #666;">Every coherent system flows downhill in potential energy.</p>
  </div>

  <div class="card-section">
    <div class="card-section-title">What It Means</div>
    <ul class="card-list">
      <li>ℹ = system state (position, momentum, weights, price)</li>
      <li>Φ = potential energy landscape</li>
      <li>∇Φ = gradient (points uphill)</li>
      <li>-∇Φ = flow direction (downhill)</li>
    </ul>
  </div>

  <div class="card-section">
    <div class="card-section-title">In Different Domains</div>
    <ul class="card-list">
      <li>Physics: Ball rolling downhill</li>
      <li>Chemistry: Molecules forming bonds</li>
      <li>Biology: Proteins folding</li>
      <li>AI: Neural network training (backprop)</li>
      <li>Economy: Market price discovery</li>
      <li>Psychology: Learning via error reduction</li>
    </ul>
  </div>

  <div class="card-section">
    <div class="card-section-title">Key Insight</div>
    <div class="key-point">Same law governs electrons, molecules, brains, markets, and AI. No unified theory needed—already exists.</div>
  </div>
</div>

<!-- Card 2: Help Systems -->
<div class="reference-card">
  <div class="card-title">Help Systems Framework</div>
  
  <div class="card-section">
    <div class="card-section-title">The Four Levels</div>
    <div style="margin: 0.75rem 0;">
      <div style="font-weight: 700; color: #f44336;">GUIDED (High support)</div>
      <p style="margin: 0.25rem 0; font-size: 0.85rem; color: #666;">Professional directs: explains, demonstrates, decides</p>
    </div>
    <div style="margin: 0.75rem 0;">
      <div style="font-weight: 700; color: #ff9800;">SUPPORTED (Medium support)</div>
      <p style="margin: 0.25rem 0; font-size: 0.85rem; color: #666;">Collaborative: person leads, professional coaches</p>
    </div>
    <div style="margin: 0.75rem 0;">
      <div style="font-weight: 700; color: #4CAF50;">AUTONOMOUS (Low support)</div>
      <p style="margin: 0.25rem 0; font-size: 0.85rem; color: #666;">Person leads independently, professional available</p>
    </div>
  </div>

  <div class="card-section">
    <div class="card-section-title">Progression Blueprint</div>
    <ul class="card-list">
      <li>Start at person's current level</li>
      <li>Help them succeed at that level</li>
      <li>Gradually reduce support as competence grows</li>
      <li>Move toward autonomy, not away</li>
    </ul>
  </div>

  <div class="card-section">
    <div class="card-section-title">Applies To</div>
    <ul class="card-list">
      <li>Teaching & Education</li>
      <li>Therapy & Counseling</li>
      <li>Parenting & Development</li>
      <li>Coaching & Mentoring</li>
      <li>Management & Onboarding</li>
    </ul>
  </div>

  <div class="card-section">
    <div class="key-point">Match support level to person's competence. Mismatch = frustration or dependency.</div>
  </div>
</div>

<!-- Card 3: Cosmic Eras -->
<div class="reference-card">
  <div class="card-title">The Cosmic Eras</div>
  
  <div class="card-section">
    <div class="card-section-title">The Eight Eras</div>
    <ol style="margin: 0.5rem 0; padding-left: 1.2rem; color: #555; font-size: 0.85rem;">
      <li style="margin: 0.3rem 0;">Quantum Genesis (Big Bang)</li>
      <li style="margin: 0.3rem 0;">Atomic Formation (electrons+nuclei)</li>
      <li style="margin: 0.3rem 0;">Molecular Complexity (atoms→molecules)</li>
      <li style="margin: 0.3rem 0;">Protobiotic (chemistry→biology transition)</li>
      <li style="margin: 0.3rem 0;">Biological (single-celled life)</li>
      <li style="margin: 0.3rem 0;">Multicellular (tissues→organisms)</li>
      <li style="margin: 0.3rem 0;">Societal (groups→cultures→civilizations)</li>
      <li style="margin: 0.3rem 0;">Digital-Conscious (AI→future?)</li>
    </ol>
  </div>

  <div class="card-section">
    <div class="card-section-title">Pattern Within Eras</div>
    <ul class="card-list">
      <li>New organizational principle emerges</li>
      <li>New level of complexity appears</li>
      <li>Previous era's rules still apply (but not sufficient)</li>
      <li>Properties not predictable from parts</li>
    </ul>
  </div>

  <div class="card-section">
    <div class="example-box">Example: From neurons to thought. Know all neuron chemistry → still can't predict consciousness.</div>
  </div>

  <div class="card-section">
    <div class="key-point">Each era builds on previous, adding coordination principles. No return to simpler organization.</div>
  </div>
</div>

<!-- Card 4: Stability -->
<div class="reference-card">
  <div class="card-title">Stability & Equilibrium</div>
  
  <div class="card-section">
    <div class="card-section-title">Types of Equilibria</div>
    <div style="margin: 0.75rem 0;">
      <div style="font-weight: 700;">STABLE (Valley bottom)</div>
      <p style="margin: 0.25rem 0; font-size: 0.85rem; color: #666;">Small perturbation → returns to equilibrium</p>
    </div>
    <div style="margin: 0.75rem 0;">
      <div style="font-weight: 700;">UNSTABLE (Hill top)</div>
      <p style="margin: 0.25rem 0; font-size: 0.85rem; color: #666;">Small perturbation → system escapes</p>
    </div>
    <div style="margin: 0.75rem 0;">
      <div style="font-weight: 700;">METASTABLE (Local valley)</div>
      <p style="margin: 0.25rem 0; font-size: 0.85rem; color: #666;">Locally stable, but can escape with enough energy</p>
    </div>
  </div>

  <div class="card-section">
    <div class="card-section-title">Mathematical Test</div>
    <div class="equation">Stable if: ∂²E/∂x² > 0 (concave up)</div>
  </div>

  <div class="card-section">
    <div class="card-section-title">Real Examples</div>
    <ul class="card-list">
      <li>Habits: metastable, hard to break</li>
      <li>Monopolies: stable (entrench)</li>
      <li>Social norms: metastable</li>
      <li>Brain states: stable attractors</li>
    </ul>
  </div>
</div>

<!-- Card 5: Learning Curves -->
<div class="reference-card">
  <div class="card-title">Learning & Growth Curves</div>
  
  <div class="card-section">
    <div class="card-section-title">Standard Pattern</div>
    <div class="equation">Skill(t) = S_max × (1 - e^(-t/τ))</div>
    <p style="margin: 0.5rem 0; font-size: 0.8rem; color: #666;">Exponential approach to plateau</p>
  </div>

  <div class="card-section">
    <div class="card-section-title">What This Means</div>
    <ul class="card-list">
      <li>Slow start, then rapid improvement</li>
      <li>Eventually plateaus (diminishing returns)</li>
      <li>τ = time constant (bigger = slower learning)</li>
      <li>S_max = your ceiling (talent, effort, opportunity)</li>
    </ul>
  </div>

  <div class="card-section">
    <div class="card-section-title">To Accelerate Learning</div>
    <ul class="card-list">
      <li>Reduce τ (better instruction, practice)</li>
      <li>Increase S_max (remove barriers, add resources)</li>
      <li>Move plateau higher (deliberate practice)</li>
      <li>Spaced repetition reinforces minimum</li>
    </ul>
  </div>

  <div class="card-section">
    <div class="key-point">Consistent practice beats occasional intense effort. Compound growth is exponential, not linear.</div>
  </div>
</div>

<!-- Card 6: Domain Mapping -->
<div class="reference-card">
  <div class="card-title">See Patterns Across Domains</div>
  
  <div class="card-section">
    <div class="card-section-title">Same Concept, Different Domains</div>
    <p style="color: #666; font-size: 0.9rem; margin: 0.5rem 0;">Pick a concept → see it in all domains</p>
  </div>

  <div class="card-section">
    <div class="card-section-title">Example: Energy Minimization</div>
    <ul class="card-list">
      <li><strong>Physics:</strong> Electron falls into lowest orbital</li>
      <li><strong>Chemistry:</strong> Reaction products have lower energy</li>
      <li><strong>Biology:</strong> Protein folds to minimize free energy</li>
      <li><strong>AI:</strong> Neural network minimizes loss function</li>
      <li><strong>Market:</strong> Price settles at supply=demand</li>
      <li><strong>Psychology:</strong> Behavior reduces prediction error</li>
    </ul>
  </div>

  <div class="card-section">
    <div class="key-point">If you understand it in one domain, you understand it in all. Cross-domain thinking reveals universal principles.</div>
  </div>

  <div class="card-section">
    <div class="example-box">Usage: Struggling with AI concept? Learn the physics version first. Struggling with psych? Learn the physics. Same mathematics.</div>
  </div>
</div>

<!-- Card 7: Coherence Checklist -->
<div class="reference-card">
  <div class="card-title">Coherence Verification Checklist</div>
  
  <div class="card-section">
    <div class="card-section-title">For Any System or Concept</div>
    <div style="background: #f0f8ff; border-left: 3px solid #2196F3; padding: 0.75rem; border-radius: 3px; margin: 0.5rem 0;">
      <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.85rem; color: #555;">
        <li style="margin: 0.25rem 0;">□ States defined clearly (what are all possible states?)</li>
        <li style="margin: 0.25rem 0;">□ Transitions specified (how does each state change?)</li>
        <li style="margin: 0.25rem 0;">□ No contradictions (can two states exist simultaneously?)</li>
        <li style="margin: 0.25rem 0;">□ All paths valid (does every input lead somewhere?)</li>
        <li style="margin: 0.25rem 0;">□ No dead ends (can system get stuck permanently?)</li>
        <li style="margin: 0.25rem 0;">□ Stable endpoints (is there equilibrium?)</li>
        <li style="margin: 0.25rem 0;">□ Inputs handled (all possibilities covered?)</li>
      </ul>
    </div>
  </div>

  <div class="card-section">
    <div class="card-section-title">If Any Box Unchecked</div>
    <p style="margin: 0; font-size: 0.85rem; color: #555;">System has gaps or contradictions. Fix before relying on it.</p>
  </div>

  <div class="card-section">
    <div class="key-point">Coherent systems work. Contradictory ones fail. Check while thinking, before executing.</div>
  </div>
</div>

<!-- Card 8: Decision Tree -->
<div class="reference-card">
  <div class="card-title">Which Framework to Use?</div>
  
  <div class="card-section">
    <div class="card-section-title">Quick Decision Guide</div>
    <div style="font-size: 0.85rem; color: #555; line-height: 1.8; margin: 0.5rem 0;">
      <strong>Understanding WHY something changes?</strong><br/>
      → Universal Foundation<br/><br/>
      
      <strong>Helping someone learn/grow?</strong><br/>
      → Help Systems Framework<br/><br/>
      
      <strong>Understanding history/evolution?</strong><br/>
      → Cosmic Eras<br/><br/>
      
      <strong>Designing algorithms/computers?</strong><br/>
      → Binary Logic<br/><br/>
      
      <strong>Something doesn't make sense?</strong><br/>
      → Check Coherence Checklist<br/><br/>
      
      <strong>Unsure?</strong><br/>
      → Take Self-Assessment Quiz
    </div>
  </div>
</div>

</div>

<div class="print-button">
  <button class="print-btn" onclick="window.print()">📥 Print These Cards</button>
</div>

<div class="copy-note">
💡 Tip: Print on cardstock for durability. Laminate for weather resistance. Share with colleagues, students, or friends.
</div>
