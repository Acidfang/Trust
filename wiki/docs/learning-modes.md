---
layout: page
title: Learning Modes
permalink: /learning-modes/
description: Choose your learning path - visual, interactive, narrative, mathematical, or kinesthetic
---

# Choose Your Learning Path

**Everyone understands differently.** This wiki offers multiple ways to learn each concept.

<style>
.mode-selector {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.mode-card {
  background: white;
  border: 2px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
  color: inherit;
}

.mode-card:hover {
  border-color: #2196F3;
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.2);
  transform: translateY(-3px);
}

.mode-card h3 {
  margin-top: 0;
  color: #2196F3;
  font-size: 1.3rem;
}

.mode-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.mode-description {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.5;
}

.mode-use-case {
  font-size: 0.8rem;
  color: #999;
  margin-top: 1rem;
  font-style: italic;
}

.interactive-toggle {
  background: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 1rem;
  margin: 1rem 0;
  cursor: pointer;
}

.interactive-toggle h4 {
  margin: 0;
  color: #2196F3;
}

.form-inline {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
  flex-wrap: wrap;
}

.form-inline select,
.form-inline button {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
}

.form-inline select:focus,
.form-inline button:focus {
  outline: none;
  border-color: #2196F3;
  box-shadow: 0 0 4px rgba(33, 150, 243, 0.3);
}

.concept-explorer {
  background: #f9f9f9;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  margin: 2rem 0;
}

.concept-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin: 1rem 0;
}

.concept-button {
  background: white;
  border: 2px solid #e0e0e0;
  padding: 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
  font-weight: 500;
  color: #333;
}

.concept-button:hover {
  border-color: #2196F3;
  background: #f0f8ff;
}

.concept-button.active {
  border-color: #2196F3;
  background: #2196F3;
  color: white;
}

.depth-slider {
  margin: 1rem 0;
}

.depth-slider input[type="range"] {
  width: 100%;
  max-width: 300px;
}

.depth-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #666;
  max-width: 300px;
  margin-top: 0.5rem;
}

.quick-reference {
  background: #e8f5e9;
  border-left: 4px solid #4CAF50;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 4px;
}

.detailed-explanation {
  background: #e3f2fd;
  border-left: 4px solid #2196F3;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 4px;
  display: none;
}

.detailed-explanation.active {
  display: block;
}

.technical-view {
  background: #f3e5f5;
  border-left: 4px solid #9C27B0;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.9rem;
  display: none;
}

.technical-view.active {
  display: block;
}
</style>

## Your Learning Preferences

<div class="form-inline">
  <label for="preferred-mode">Show me:</label>
  <select id="preferred-mode" onchange="updateMode(this.value)">
    <option value="all">Everything (all modes)</option>
    <option value="visual">Visual explanations</option>
    <option value="interactive">Interactive explorations</option>
    <option value="narrative">Stories & examples</option>
    <option value="technical">Mathematical rigor</option>
    <option value="quick">Quick summaries</option>
  </select>
</div>

<div class="form-inline">
  <label for="complexity-level">Learning depth:</label>
  <div class="depth-slider">
    <input type="range" id="complexity-level" min="1" max="5" value="3" onchange="updateComplexity(this.value)">
    <div class="depth-labels">
      <span>Beginner</span>
      <span>Intermediate</span>
      <span>Advanced</span>
    </div>
  </div>
</div>

---

## Five Ways to Learn

<div class="mode-selector">

<a href="#visual-learning" class="mode-card">
<div class="mode-icon">🎨</div>
<h3>Visual</h3>
<div class="mode-description">
Diagrams, timelines, maps, and interactive visualizations that show how things connect.
</div>
<div class="mode-use-case">
Best for: Understanding structure and relationships
</div>
</a>

<a href="#interactive-learning" class="mode-card">
<div class="mode-icon">🎮</div>
<h3>Interactive</h3>
<div class="mode-description">
Click to explore, drag to manipulate, adjust sliders to see effects. Learn by experimenting.
</div>
<div class="mode-use-case">
Best for: Discovery and intuition-building
</div>
</a>

<a href="#narrative-learning" class="mode-card">
<div class="mode-icon">📖</div>
<h3>Narrative</h3>
<div class="mode-description">
Stories, examples, case studies. Understanding through real-world contexts.
</div>
<div class="mode-use-case">
Best for: Motivation and application
</div>
</a>

<a href="#technical-learning" class="mode-card">
<div class="mode-icon">⚙️</div>
<h3>Technical</h3>
<div class="mode-description">
Mathematics, equations, proofs, algorithms. Complete technical rigor.
</div>
<div class="mode-use-case">
Best for: Deep understanding and implementation
</div>
</a>

<a href="#kinesthetic-learning" class="mode-card">
<div class="mode-icon">🧩</div>
<h3>Kinesthetic</h3>
<div class="mode-description">
Build models, simulate systems, create comparisons. Learning by doing.
</div>
<div class="mode-use-case">
Best for: Retention and practical skill
</div>
</a>

</div>

---

<h2 id="visual-learning">🎨 Visual Learning</h2>

**What it is**: Diagrams, maps, timelines, and interactive visualizations

**When to use it**: When you want to see how things connect, what the big picture is, or how something is structured

**In this wiki:**
- [Framework Visualization Map]({{ site.baseurl }}/framework-map/) - See how all systems connect
- [Interactive Timeline]({{ site.baseurl }}/timeline-navigator/) - Explore each cosmic era visually
- [The Great Unfolding]({{ site.baseurl }}/cosmic-unfolding/) - Visual progression through stages

**Quick visual guide:**
- **Red lines** = Universal principle connections
- **Green nodes** = Foundational frameworks
- **Blue nodes** = Applied frameworks
- **Color gradients** = Time or complexity progression

---

<h2 id="interactive-learning">🎮 Interactive Learning</h2>

**What it is**: Click, drag, adjust, and see what happens instantly

**When to use it**: When you want to explore, experiment, and build intuition

**In this wiki:**
- Click timeline stages to see details
- Adjust sliders to control complexity level
- Toggle between explanations to compare perspectives
- Explore domain examples interactively

**Example - Universal Law Explorer** (coming soon)

<div class="interactive-toggle" onclick="toggleContent(this, 'explorer1')">
  <h4>▶ Try: Adjust the potential landscape</h4>
  <div class="form-inline" id="explorer1" style="display: none;">
    <label>Potential shape:</label>
    <select onchange="updatePotential(this.value)">
      <option value="quadratic">Harmonic</option>
      <option value="cubic">Cubic</option>
      <option value="double-well">Double-well</option>
      <option value="custom">Custom</option>
    </select>
    <canvas id="potential-canvas" width="300" height="150" style="border: 1px solid #ddd; margin-left: 1rem;"></canvas>
  </div>
</div>

---

<h2 id="narrative-learning">📖 Narrative Learning</h2>

**What it is**: Stories, examples, real-world applications, and case studies

**When to use it**: When you want to understand WHY something matters and WHERE it applies

**In this wiki:**
- [Why This Matters]({{ site.baseurl }}/why-this-matters/) - The stakes and consequences
- [Domain Examples]({{ site.baseurl }}/domain-examples/) - How the principle appears everywhere
- [Help Systems Cards]({{ site.baseurl }}/help-systems-cards/) - Real patterns in education, parenting, therapy

**Learn through context:**
- Start with a problem you care about
- See how the framework explains it
- Understand the principle through recognition, not memorization

---

<h2 id="technical-learning">⚙️ Technical Learning</h2>

**What it is**: Mathematics, equations, algorithms, and complete rigor

**When to use it**: When you need to implement something, prove something, or understand deeply

**In this wiki:**
- [Universal Foundation]({{ site.baseurl }}/universal-foundation/) - Full mathematical basis
- Framework code and documentation
- Verification proofs and implementations


**Toggle technical view:**

<div class="interactive-toggle" onclick="toggleContent(this, 'technical1')">
  <h4>▶ Show me: Mathematical formulation</h4>
  <div class="technical-view" id="technical1">
    <strong>Definition</strong>: A coherent system evolves via<br>
    dℹ/dt = -∇Φ(x,t)<br><br>
    <strong>Where:</strong><br>
    ℹ = system state (position, momentum, etc.)<br>
    Φ = potential energy landscape<br>
    ∇Φ = gradient of potential<br>
    -∇Φ = direction downhill in potential<br><br>
    <strong>Interpretation</strong>: System flows downhill in potential space. Minimum-energy configurations are stable. Gradients drive transition rates.
  </div>
</div>

---

<h2 id="kinesthetic-learning">🧩 Kinesthetic Learning</h2>

**What it is**: Build models, create comparisons, simulate systems. Learning by doing.

**When to use it**: When you want to really understand something and remember it long-term

**In this wiki:**
- [Discovery Game]({{ site.baseurl }}/game/) - Learn through consequences and discovery
- Framework builders (create your own system following the law)
- Comparative analyses (how does this principle apply in different domains?)

**Build something yourself:**

<div class="interactive-toggle" onclick="toggleContent(this, 'builder1')">
  <h4>▶ Try: Design your own system</h4>
  <div id="builder1" style="display: none;">
    <div class="form-inline">
      <label>System type:</label>
      <select onchange="updateBuilder(this.value)">
        <option>-- Choose --</option>
        <option value="particle">Physical particle</option>
        <option value="molecule">Chemical molecule</option>
        <option value="institution">Social institution</option>
        <option value="learning">Learning system</option>
      </select>
    </div>
    <div id="builder-output" style="background: #f5f5f5; padding: 1rem; margin-top: 1rem; border-radius: 4px; display: none;">
      <strong>Your system follows:</strong><br>
      dℹ/dt = -∇Φ<br><br>
      Now define Φ (the potential) for your system:
      <textarea placeholder="What's the energy landscape? What makes states stable or unstable?" style="width: 100%; height: 100px; margin-top: 0.5rem; padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px;"></textarea>
    </div>
  </div>
</div>

---

## Combining Modes for Mastery

The most effective learning combines multiple modes:

1. **Start Visual** - See the big picture on the Timeline
2. **Then Interactive** - Click stages to explore details
3. **Then Narrative** - Read why it matters in Domain Examples
4. **Then Technical** - Study the mathematics
5. **Then Kinesthetic** - Build something yourself

### Suggested Learning Paths

**For Quick Understanding** (15 minutes):
1. Interactive Timeline
2. Visual Framework Map
3. Quick summary on topic page

**For Intermediate Knowledge** (1 hour):
1. Interactive Timeline
2. Read Narrative section
3. View Technical formulation
4. Explore related domains

**For Mastery** (3+ hours):
1. Read The Great Unfolding
2. Study Universal Foundation
3. Review Framework code
4. Build your own system
5. Teach someone else

---

## Accessibility Features

All content is available in multiple formats:

- **Text** - For all content
- **Audio descriptions** (coming) - For diagrams
- **High contrast mode** - Available via browser settings
- **Mobile responsive** - All interactive elements work on phone/tablet
- **Keyboard accessible** - All interactive elements work without mouse

---

<script>
function toggleContent(element, contentId) {
  const content = document.getElementById(contentId);
  if (content.style.display === 'none') {
    content.style.display = 'block';
    element.innerHTML = element.innerHTML.replace('▶', '▼');
  } else {
    content.style.display = 'none';
    element.innerHTML = element.innerHTML.replace('▼', '▶');
  }
}

function updateMode(mode) {
  // Store preference
  localStorage.setItem('learningMode', mode);
  // In future, filter all content by mode
  console.log('Learning mode set to:', mode);
}

function updateComplexity(level) {
  // Store preference
  localStorage.setItem('complexityLevel', level);
  // In future, show/hide content based on complexity
  console.log('Complexity level set to:', level);
}

function updatePotential(type) {
  console.log('Potential type:', type);
  // In future, update canvas visualization
}

function updateBuilder(type) {
  const output = document.getElementById('builder-output');
  if (type === '-- Choose --') {
    output.style.display = 'none';
  } else {
    output.style.display = 'block';
  }
}

// Load user preferences on page load
window.addEventListener('load', function() {
  const mode = localStorage.getItem('learningMode');
  const complexity = localStorage.getItem('complexityLevel');
  
  if (mode) document.getElementById('preferred-mode').value = mode;
  if (complexity) document.getElementById('complexity-level').value = complexity;
});
</script>
