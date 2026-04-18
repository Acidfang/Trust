---
layout: page
title: Learning Pathways
permalink: /pathways/
description: Choose your own adventure through the wiki
---

# Learning Pathways: Choose Your Own Adventure

**Every person learns differently. Pick the path that matches YOU.**

<style>
.pathways-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.intro-box {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 3rem;
  text-align: center;
}

.intro-box h2 {
  margin: 0 0 1rem 0;
  font-size: 2rem;
}

.intro-box p {
  margin: 0.5rem 0;
  font-size: 1.1rem;
  opacity: 0.95;
}

.pathways-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.pathway-card {
  background: white;
  border: 2px solid #ddd;
  border-top: 5px solid;
  border-radius: 8px;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pathway-card:hover {
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  transform: translateY(-4px);
}

.pathway-card.visual {
  border-top-color: #ff6b6b;
  background: linear-gradient(135deg, #fff5f5 0%, #ffe0e0 100%);
}

.pathway-card.interactive {
  border-top-color: #4ecdc4;
  background: linear-gradient(135deg, #f0fffe 0%, #e0f9f7 100%);
}

.pathway-card.narrative {
  border-top-color: #ffd93d;
  background: linear-gradient(135deg, #fffdf5 0%, #fff9e6 100%);
}

.pathway-card.technical {
  border-top-color: #6c5ce7;
  background: linear-gradient(135deg, #f5f3ff 0%, #ede7ff 100%);
}

.pathway-card.kinesthetic {
  border-top-color: #a29bfe;
  background: linear-gradient(135deg, #faf8ff 0%, #f0ebff 100%);
}

.pathway-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.pathway-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #333;
}

.pathway-description {
  font-size: 0.95rem;
  color: #666;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.pathway-steps {
  background: white;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.pathway-steps h4 {
  margin: 0 0 0.75rem 0;
  font-size: 0.9rem;
  text-transform: uppercase;
  color: #999;
}

.step-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.step-list li {
  padding: 0.5rem 0;
  font-size: 0.9rem;
  color: #555;
  display: flex;
  align-items: center;
}

.step-list li::before {
  content: '→';
  margin-right: 0.75rem;
  font-weight: 700;
  color: #2196F3;
  min-width: 20px;
}

.pathway-links {
  display: grid;
  gap: 0.75rem;
}

.pathway-link {
  display: block;
  padding: 0.75rem 1rem;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-decoration: none;
  color: #333;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s;
  text-align: center;
}

.pathway-link:hover {
  background: #f5f5f5;
  border-color: #999;
  color: #000;
}

.time-estimate {
  font-size: 0.75rem;
  color: #999;
  margin-top: 0.5rem;
  font-style: italic;
}

/* Horizontal flow diagram */
.flow-container {
  background: white;
  border: 2px dashed #ddd;
  border-radius: 12px;
  padding: 2rem;
  margin: 3rem 0;
  overflow-x: auto;
}

.flow-title {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  text-align: center;
  color: #333;
}

.flow-diagram {
  display: flex;
  align-items: center;
  gap: 1rem;
  min-width: 900px;
  justify-content: center;
}

.flow-box {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 6px;
  text-align: center;
  font-weight: 600;
  font-size: 0.9rem;
  min-width: 150px;
  flex-shrink: 0;
}

.flow-arrow {
  font-size: 1.5rem;
  color: #667eea;
  flex-shrink: 0;
}

/* Decision trees */
.decision-section {
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 2rem;
  margin: 2rem 0;
}

.decision-section h3 {
  margin-top: 0;
  font-size: 1.3rem;
  color: #333;
}

.scenario-box {
  background: white;
  border-left: 4px solid #2196F3;
  padding: 1.5rem;
  margin: 1rem 0;
  border-radius: 4px;
}

.scenario-question {
  font-weight: 700;
  color: #333;
  margin-bottom: 0.75rem;
  font-size: 1rem;
}

.scenario-answer {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0.75rem 0;
}

.scenario-answer strong {
  color: #2196F3;
}

/* Progress tracker */
.progress-section {
  background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
  border-radius: 8px;
  padding: 2rem;
  color: white;
  text-align: center;
  margin: 2rem 0;
}

.progress-section h3 {
  margin-top: 0;
  font-size: 1.3rem;
}

.progress-bar {
  background: rgba(255,255,255,0.3);
  border-radius: 20px;
  height: 30px;
  margin: 1.5rem 0;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  background: white;
  height: 100%;
  width: 0%;
  border-radius: 20px;
  transition: width 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #667eea;
  font-weight: 700;
  font-size: 0.9rem;
}

/* FAQ/Tips */
.tips-section {
  background: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: 8px;
  padding: 1.5rem;
  margin: 2rem 0;
}

.tips-section h3 {
  margin-top: 0;
  color: #856404;
}

.tips-section ul {
  margin: 0;
  padding-left: 1.5rem;
  color: #856404;
}

.tips-section li {
  margin: 0.5rem 0;
}

@media (max-width: 768px) {
  .pathways-grid {
    grid-template-columns: 1fr;
  }
  
  .flow-diagram {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .flow-arrow {
    transform: rotate(90deg);
  }
}
</style>

<div class="pathways-container">

<!-- Intro Section -->
<div class="intro-box">
  <h2>🧭 Find Your Path</h2>
  <p>The wiki has many entry points. We've mapped them all out.</p>
  <p>Pick the learning style that matches how YOUR brain works best.</p>
</div>

<!-- Main Pathways -->
<div class="pathways-grid">

<!-- Visual Pathway -->
<div class="pathway-card visual">
  <div class="pathway-icon">🎨</div>
  <div class="pathway-title">Visual Learner</div>
  <div class="pathway-description">You understand through diagrams, maps, and spatial relationships. You prefer seeing the big picture first.</div>
  
  <div class="pathway-steps">
    <h4>Your Path (30-45 min)</h4>
    <ul class="step-list">
      <li>Domain Mapper (see concepts across domains)</li>
      <li>Framework Comparison Matrix (visual fit levels)</li>
      <li>Case Studies (pick one that matches your domain)</li>
      <li>Concept Explorer (deep dive the concept visually)</li>
    </ul>
  </div>
  
  <div class="pathway-links">
    <a href="/domain-mapper/" class="pathway-link">🗺️ Domain Mapper</a>
    <a href="/frameworks-comparison/" class="pathway-link">📊 Framework Comparison</a>
    <a href="/case-studies/" class="pathway-link">📚 Case Studies</a>
    <a href="/concept-explorer/" class="pathway-link">🔍 Concept Explorer</a>
  </div>
  
  <div class="time-estimate">⏱️ ~30-45 minutes to get oriented</div>
</div>

<!-- Interactive Pathway -->
<div class="pathway-card interactive">
  <div class="pathway-icon">🎮</div>
  <div class="pathway-title">Interactive Learner</div>
  <div class="pathway-description">You learn by doing, clicking, experimenting, and adjusting. You like to manipulate things directly.</div>
  
  <div class="pathway-steps">
    <h4>Your Path (20-30 min)</h4>
    <ul class="step-list">
      <li>Self-Assessment Quiz (get personalized recommendations)</li>
      <li>Framework Comparison (click through deep dives)</li>
      <li>Domain Mapper (select concepts, filter domains)</li>
      <li>Case Studies (explore related cases via modal nav)</li>
    </ul>
  </div>
  
  <div class="pathway-links">
    <a href="/self-assessment/" class="pathway-link">❓ Take the Quiz</a>
    <a href="/frameworks-comparison/" class="pathway-link">⚙️ Compare Frameworks</a>
    <a href="/domain-mapper/" class="pathway-link">🔄 Explore Domains</a>
    <a href="/case-studies/" class="pathway-link">📘 Browse Cases</a>
  </div>
  
  <div class="time-estimate">⏱️ ~20-30 minutes (quiz + exploration)</div>
</div>

<!-- Narrative Pathway -->
<div class="pathway-card narrative">
  <div class="pathway-icon">📖</div>
  <div class="pathway-title">Narrative Learner</div>
  <div class="pathway-description">You understand through stories, examples, and context. You like to see how concepts show up in real situations.</div>
  
  <div class="pathway-steps">
    <h4>Your Path (45-60 min)</h4>
    <ul class="step-list">
      <li>Case Studies (read real-world examples end-to-end)</li>
      <li>Concept Explorer (read narrative view for each)</li>
      <li>Help Systems Guide (learn through teaching stories)</li>
      <li>Learning Modes (read the context for each mode)</li>
    </ul>
  </div>
  
  <div class="pathway-links">
    <a href="/case-studies/" class="pathway-link">📚 Read Case Studies</a>
    <a href="/concept-explorer/" class="pathway-link">📝 Read Concepts</a>
    <a href="/quick-reference/" class="pathway-link">📋 Read Reference Cards</a>
    <a href="/learning-modes/" class="pathway-link">🎓 Read Learning Modes</a>
  </div>
  
  <div class="time-estimate">⏱️ ~45-60 minutes (deep reading)</div>
</div>

<!-- Technical Pathway -->
<div class="pathway-card technical">
  <div class="pathway-icon">🧮</div>
  <div class="pathway-title">Technical Learner</div>
  <div class="pathway-description">You understand through mathematics, equations, and formal systems. You want rigor and precision.</div>
  
  <div class="pathway-steps">
    <h4>Your Path (30-45 min)</h4>
    <ul class="step-list">
      <li>Concept Explorer (switch to "Technical" view)</li>
      <li>Case Studies (read equation + mechanics sections)</li>
      <li>Quick Reference (equations on laminate cards)</li>
      <li>Domain Mapper (equations for each domain)</li>
    </ul>
  </div>
  
  <div class="pathway-links">
    <a href="/concept-explorer/" class="pathway-link">📐 Technical Views</a>
    <a href="/case-studies/" class="pathway-link">🔬 Cases with Equations</a>
    <a href="/quick-reference/" class="pathway-link">📏 Reference Equations</a>
    <a href="/domain-mapper/" class="pathway-link">🧬 Domain Equations</a>
  </div>
  
  <div class="time-estimate">⏱️ ~30-45 minutes (equations + mechanics)</div>
</div>

<!-- Kinesthetic Pathway -->
<div class="pathway-card kinesthetic">
  <div class="pathway-icon">🛠️</div>
  <div class="pathway-title">Kinesthetic Learner</div>
  <div class="pathway-description">You understand through doing, building, simulating. You want to implement and see things work.</div>
  
  <div class="pathway-steps">
    <h4>Your Path (60+ min)</h4>
    <ul class="step-list">
      <li>Learning Modes (explore interactive toggles)</li>
      <li>Case Studies (try to apply improvements yourself)</li>
      <li>Domain Mapper (pick a domain, design improvements)</li>
      <li>Build something (create your own example)</li>
    </ul>
  </div>
  
  <div class="pathway-links">
    <a href="/learning-modes/" class="pathway-link">⚡ Interactive Modes</a>
    <a href="/case-studies/" class="pathway-link">🔧 Apply Cases</a>
    <a href="/domain-mapper/" class="pathway-link">🏗️ Design for Domain</a>
    <a href="/verification-tracker/" class="pathway-link">✅ Track Your Work</a>
  </div>
  
  <div class="time-estimate">⏱️ 60+ minutes (hands-on exploration)</div>
</div>

</div>

<!-- Flow Diagram -->
<div class="flow-container">
  <div class="flow-title">The Wiki's Internal Flow (How pages connect)</div>
  <div class="flow-diagram">
    <div class="flow-box">📍 Start Here</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">Pick Learning Mode</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">Explore Pathways</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">Deep Dive Content</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">Apply & Share</div>
  </div>
</div>

<!-- Scenario-Based Decision Guide -->
<div class="decision-section">
  <h3>🤔 I'm In This Situation... Where Should I Go?</h3>
  
  <div class="scenario-box">
    <div class="scenario-question">"I don't know where to start"</div>
    <div class="scenario-answer">
      Start with <strong>Learning Modes</strong> → Then take <strong>Self-Assessment Quiz</strong> → Get personalized recommendations
    </div>
  </div>
  
  <div class="scenario-box">
    <div class="scenario-question">"I'm confused by one concept"</div>
    <div class="scenario-answer">
      Go to <strong>Concept Explorer</strong> → Search the concept → Try "Visual" or "Narrative" view to understand it from multiple angles
    </div>
  </div>
  
  <div class="scenario-box">
    <div class="scenario-question">"I want quick reference without reading"</div>
    <div class="scenario-answer">
      Print <strong>Quick Reference Cards</strong> → Laminate them → Keep in pocket for instant reminders
    </div>
  </div>
  
  <div class="scenario-box">
    <div class="scenario-question">"I want to see how this applies to MY domain"</div>
    <div class="scenario-answer">
      Go to <strong>Domain Mapper</strong> → Pick your domain → See the pattern expressed in your field → Check <strong>Case Studies</strong> for real examples
    </div>
  </div>
  
  <div class="scenario-box">
    <div class="scenario-question">"I need to explain this to someone else"</div>
    <div class="scenario-answer">
      Pick a <strong>Case Study</strong> from their domain → Use the "Baseline → Principle → Improvement" structure to teach → Print QR cards as handouts
    </div>
  </div>
  
  <div class="scenario-box">
    <div class="scenario-question">"I want to go deep into the mathematics"</div>
    <div class="scenario-answer">
      Open <strong>Concept Explorer</strong> → Switch to "Technical" view for each concept → Check <strong>Case Studies</strong> "Equation" section → Compare across <strong>Domain Mapper</strong> equations
    </div>
  </div>
  
  <div class="scenario-box">
    <div class="scenario-question">"I'm comparing frameworks to pick the best one"</div>
    <div class="scenario-answer">
      Go to <strong>Framework Comparison Matrix</strong> → Match your domain → Click "deep dive" for details → Cross-reference with <strong>Self-Assessment</strong> recommendations
    </div>
  </div>
  
  <div class="scenario-box">
    <div class="scenario-question">"I'm building something and want to verify it's coherent"</div>
    <div class="scenario-answer">
      Use the <strong>Coherence Checklist</strong> from Quick Reference → Open <strong>Verification Tracker</strong> → Log your thinking as you check each item
    </div>
  </div>
</div>

<!-- Tips Section -->
<div class="tips-section">
  <h3>💡 Pro Tips for Getting the Most Out of the Wiki</h3>
  <ul>
    <li><strong>Mix pathways:</strong> Start with your natural learning style, but try others—cross-fertilization helps retention</li>
    <li><strong>Use "Save" buttons:</strong> Bookmark concepts and cases you want to revisit—they persist in your browser</li>
    <li><strong>Print reference cards:</strong> Laminated cards make great desk references or teaching materials</li>
    <li><strong>Compare across domains:</strong> The power isn't in one example, but seeing the same pattern in 5+ domains</li>
    <li><strong>Read baseline first:</strong> In case studies, always read the baseline before the improvement—contrast is how learning sticks</li>
    <li><strong>Check your understanding:</strong> After each page, can you explain the concept to a friend?</li>
    <li><strong>Look for equations:</strong> If you found it meaningful on one page, find the equation that describes it</li>
    <li><strong>Apply it:</strong> Don't just read—think of a problem in your own work. How would this framework help?</li>
  </ul>
</div>

<!-- Progress Tracker -->
<div class="progress-section">
  <h3>📊 Track Your Progress</h3>
  <p>How much of the wiki have you explored?</p>
  <div class="progress-bar">
    <div class="progress-fill" id="progressFill" style="width: 0%">0%</div>
  </div>
  <p id="progressText">0 pages explored • <a href="/verification-tracker/" style="color: white; text-decoration: underline;">Track your exploration →</a></p>
</div>

</div>

<script>
// Simple progress tracker
function updateProgress() {
  const visited = localStorage.getItem('visitedPages') ? JSON.parse(localStorage.getItem('visitedPages')) : [];
  const totalPages = 9; // total wiki pages
  const progress = Math.round((visited.length / totalPages) * 100);
  
  const progressFill = document.getElementById('progressFill');
  const progressText = document.getElementById('progressText');
  
  if (progressFill) {
    progressFill.style.width = progress + '%';
    if (progress > 10) {
      progressFill.textContent = progress + '%';
    }
  }
  
  if (progressText) {
    progressText.textContent = visited.length + ' pages explored • Track your exploration →';
  }
}

// Track page visits
function trackPageVisit(pageName) {
  const visited = localStorage.getItem('visitedPages') ? JSON.parse(localStorage.getItem('visitedPages')) : [];
  if (!visited.includes(pageName)) {
    visited.push(pageName);
    localStorage.setItem('visitedPages', JSON.stringify(visited));
  }
}

// Run on page load
updateProgress();
trackPageVisit('Learning Pathways');
</script>
