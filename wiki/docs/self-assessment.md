---
layout: page
title: Self-Assessment & Framework Selector
permalink: /self-assessment/
description: Discover which frameworks best explain your situation, and assess your understanding
---

# Self-Assessment & Framework Selector

**Confused about which framework to learn? Struggling to understand a concept? This tool guides you.**

<style>
.assessment-container {
  max-width: 900px;
  margin: 2rem auto;
}

.assessment-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.question-block {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f9f9f9;
  border-radius: 6px;
}

.question-text {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1rem;
}

.option-group {
  display: grid;
  gap: 1rem;
}

.option {
  background: white;
  border: 2px solid #ddd;
  padding: 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.option:hover {
  border-color: #2196F3;
  background: #f0f8ff;
}

.option input[type="radio"],
.option input[type="checkbox"] {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.option input:checked + label {
  color: #2196F3;
  font-weight: 600;
}

.option input:checked ~ .option-label::before {
  content: '✓ ';
  color: #2196F3;
  font-weight: 600;
}

.option-label {
  display: block;
  cursor: pointer;
  margin: 0;
  padding: 0;
}

.option-description {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.5rem;
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin: 2rem 0;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.btn-primary {
  background: #2196F3;
  color: white;
}

.btn-primary:hover {
  background: #1976D2;
}

.btn-secondary {
  background: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.results-section {
  display: none;
  margin-top: 2rem;
}

.results-section.active {
  display: block;
}

.result-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  margin: 1rem 0;
  transition: all 0.3s;
}

.result-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.result-framework {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.result-description {
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  opacity: 0.95;
}

.result-action {
  background: rgba(255,255,255,0.2);
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  display: inline-block;
  cursor: pointer;
  transition: background 0.2s;
  text-decoration: none;
}

.result-action:hover {
  background: rgba(255,255,255,0.3);
}

.match-bar {
  background: rgba(255,255,255,0.3);
  height: 4px;
  border-radius: 2px;
  margin: 0.5rem 0;
  overflow: hidden;
}

.match-fill {
  background: rgba(255,255,255,0.9);
  height: 100%;
  border-radius: 2px;
  transition: width 0.3s;
}

.assessment-progress {
  margin-bottom: 2rem;
}

.progress-bar {
  background: #e0e0e0;
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  background: #2196F3;
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s;
}

.progress-label {
  font-size: 0.9rem;
  color: #666;
  text-align: center;
}

.understanding-tracker {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin: 2rem 0;
}

@media (max-width: 600px) {
  .understanding-tracker {
    grid-template-columns: 1fr;
  }
  
  .button-group {
    flex-direction: column;
  }
}

.concept-card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.concept-card:hover {
  border-color: #2196F3;
  box-shadow: 0 4px 12px rgba(33, 150, 243, 0.15);
}

.concept-name {
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.concept-status {
  font-size: 0.85rem;
  color: #999;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  margin-top: 0.5rem;
}

.badge-novice {
  background: #ffebee;
  color: #c62828;
}

.badge-intermediate {
  background: #fff3e0;
  color: #e65100;
}

.badge-proficient {
  background: #e8f5e9;
  color: #2e7d32;
}

.recommendation-box {
  background: #e3f2fd;
  border-left: 4px solid #2196F3;
  padding: 1.5rem;
  border-radius: 4px;
  margin: 1.5rem 0;
}

.recommendation-title {
  font-weight: 600;
  color: #1565C0;
  margin-bottom: 0.75rem;
}

.recommendation-text {
  color: #333;
  line-height: 1.6;
}

.skip-section {
  text-align: center;
  padding: 1rem;
}

.skip-link {
  color: #2196F3;
  text-decoration: none;
  cursor: pointer;
  font-size: 0.9rem;
}

.skip-link:hover {
  text-decoration: underline;
}
</style>

<div class="assessment-container">

<h1>Discover Your Learning Path</h1>

<div id="intro-section" class="assessment-card">
  <h2>Quick Questions</h2>
  <p>Answer a few questions to discover which frameworks explain your situation best.</p>
  
  <div class="assessment-progress">
    <div class="progress-bar">
      <div class="progress-fill" id="progress-fill" style="width: 0%;"></div>
    </div>
    <div class="progress-label" id="progress-label">Question 1 of 6</div>
  </div>

  <!-- Question 1: What's your situation? -->
  <div class="question-block">
    <div class="question-text">1. What are you trying to understand?</div>
    <div class="option-group">
      <label class="option">
        <input type="radio" name="situation" value="physics-system" onchange="updateProgress()">
        <div class="option-label">
          <strong>A physical system</strong>
          <div class="option-description">How particles, atoms, molecules, or fields behave</div>
        </div>
      </label>
      
      <label class="option">
        <input type="radio" name="situation" value="biological-system" onchange="updateProgress()">
        <div class="option-label">
          <strong>A biological system</strong>
          <div class="option-description">How cells, organisms, or ecosystems work</div>
        </div>
      </label>
      
      <label class="option">
        <input type="radio" name="situation" value="learning-growth" onchange="updateProgress()">
        <div class="option-label">
          <strong>How people learn or change</strong>
          <div class="option-description">Psychology, education, habit formation, behavioral change</div>
        </div>
      </label>
      
      <label class="option">
        <input type="radio" name="situation" value="economic-social" onchange="updateProgress()">
        <div class="option-label">
          <strong>Economics or social dynamics</strong>
          <div class="option-description">Markets, organizations, cultures, communities</div>
        </div>
      </label>
      
      <label class="option">
        <input type="radio" name="situation" value="technology-ai" onchange="updateProgress()">
        <div class="option-label">
          <strong>Technology or AI</strong>
          <div class="option-description">How algorithms, neural networks, or computer systems work</div>
        </div>
      </label>
    </div>
  </div>

  <!-- Question 2: What's your main question? -->
  <div class="question-block">
    <div class="question-text">2. What's your main question?</div>
    <div class="option-group">
      <label class="option">
        <input type="radio" name="question" value="why-stable" onchange="updateProgress()">
        <div class="option-label">
          <strong>Why is something stable?</strong>
          <div class="option-description">Why does X stay this way? What keeps it from changing?</div>
        </div>
      </label>
      
      <label class="option">
        <input type="radio" name="question" value="how-change" onchange="updateProgress()">
        <div class="option-label">
          <strong>Why does something change?</strong>
          <div class="option-description">What drives change? How does it evolve? What's the direction?</div>
        </div>
      </label>
      
      <label class="option">
        <input type="radio" name="question" value="how-help" onchange="updateProgress()">
        <div class="option-label">
          <strong>How do I help someone improve?</strong>
          <div class="option-description">How do I teach, coach, or support growth effectively?</div>
        </div>
      </label>
      
      <label class="option">
        <input type="radio" name="question" value="understand-connection" onchange="updateProgress()">
        <div class="option-label">
          <strong>How are different things connected?</strong>
          <div class="option-description">What pattern appears in multiple domains?</div>
        </div>
      </label>
    </div>
  </div>

  <!-- Question 3: What time horizon? -->
  <div class="question-block">
    <div class="question-text">3. What time scale interests you?</div>
    <div class="option-group">
      <label class="option">
        <input type="radio" name="timescale" value="immediate" onchange="updateProgress()">
        <div class="option-label">
          <strong>Immediate/Short-term</strong>
          <div class="option-description">What's happening now? How does this work right now?</div>
        </div>
      </label>
      
      <label class="option">
        <input type="radio" name="timescale" value="medium" onchange="updateProgress()">
        <div class="option-label">
          <strong>Medium-term (days to years)</strong>
          <div class="option-description">How does it change over time? Learning curves? Relationships?</div>
        </div>
      </label>
      
      <label class="option">
        <input type="radio" name="timescale" value="long" onchange="updateProgress()">
        <div class="option-label">
          <strong>Long-term/cosmic (years to billions of years)</strong>
          <div class="option-description">How did this arise? Where is it heading? Deep history?</div>
        </div>
      </label>
    </div>
  </div>

  <!-- Question 4: What's your background? -->
  <div class="question-block">
    <div class="question-text">4. What's your background?</div>
    <div class="option-group">
      <label class="option">
        <input type="radio" name="background" value="technical" onchange="updateProgress()">
        <div class="option-label">
          <strong>Technical/Mathematical</strong>
          <div class="option-description">I'm comfortable with equations and formal reasoning</div>
        </div>
      </label>
      
      <label class="option">
        <input type="radio" name="background" value="practical" onchange="updateProgress()">
        <div class="option-label">
          <strong>Practical/Applied</strong>
          <div class="option-description">I care about real-world application and results</div>
        </div>
      </label>
      
      <label class="option">
        <input type="radio" name="background" value="holistic" onchange="updateProgress()">
        <div class="option-label">
          <strong>Holistic/Integrative</strong>
          <div class="option-description">I want to see how everything connects</div>
        </div>
      </label>
    </div>
  </div>

  <!-- Question 5: What's your goal? -->
  <div class="question-block">
    <div class="question-text">5. What do you want to do with this knowledge?</div>
    <div class="option-group">
      <label class="option">
        <input type="radio" name="goal" value="understand" onchange="updateProgress()">
        <div class="option-label">
          <strong>Understand deeply</strong>
          <div class="option-description">I want to grasp the principles fundamentally</div>
        </div>
      </label>
      
      <label class="option">
        <input type="radio" name="goal" value="apply" onchange="updateProgress()">
        <div class="option-label">
          <strong>Apply to my work</strong>
          <div class="option-description">I need to use this to solve problems</div>
        </div>
      </label>
      
      <label class="option">
        <input type="radio" name="goal" value="teach" onchange="updateProgress()">
        <div class="option-label">
          <strong>Teach others</strong>
          <div class="option-description">I want to explain this to students or colleagues</div>
        </div>
      </label>
      
      <label class="option">
        <input type="radio" name="goal" value="explore" onchange="updateProgress()">
        <div class="option-label">
          <strong>Explore for curiosity</strong>
          <div class="option-description">This fascinates me, I want to know more</div>
        </div>
      </label>
    </div>
  </div>

  <div class="button-group">
    <button class="btn btn-primary" onclick="calculateRecommendations()">Get Recommendations</button>
    <button class="btn btn-secondary" onclick="showAllFrameworks()">Skip to All Frameworks</button>
  </div>
</div>

<!-- Results Section -->
<div id="results-section" class="results-section assessment-card">
  <h2>Your Personalized Recommendations</h2>
  <p id="recommendations-intro"></p>
  <div id="results-container"></div>
</div>

<!-- Understanding Self-Assessment -->
<div id="understanding-section" class="assessment-card" style="display: none;">
  <h2>Your Understanding Level</h2>
  <p>Rate your current understanding of key concepts:</p>
  <div class="understanding-tracker" id="understanding-tracker"></div>
  <div class="button-group">
    <button class="btn btn-primary" onclick="saveUnderstanding()">Save My Progress</button>
  </div>
</div>

</div>

<script>
const frameworks = [
  {
    name: 'universal-foundation',
    title: 'Universal Foundation: dℹ/dt = -∇Φ',
    description: 'The single law governing all coherent systems',
    suited_for: {
      'physics-system': 100,
      'biological-system': 90,
      'learning-growth': 75,
      'economic-social': 80,
      'technology-ai': 95,
      'why-stable': 90,
      'how-change': 100,
      'how-help': 30,
      'understand-connection': 85,
      'understand': 95,
      'apply': 85,
      'teach': 80,
      'explore': 90,
      'technical': 95,
      'practical': 70,
      'holistic': 80
    },
    related_resources: [
      'domain-mapper',
      'case-studies',
      'concept-explorer'
    ]
  },
  
  {
    name: 'help-systems',
    title: 'Help Systems Framework',
    description: 'How systems help people learn and grow',
    suited_for: {
      'learning-growth': 100,
      'how-help': 100,
      'medium': 85,
      'practical': 100,
      'teach': 100,
      'apply': 90,
      'technical': 40,
      'holistic': 85,
      'biological-system': 60,
      'physics-system': 20
    },
    related_resources: [
      'case-studies',
      'learning-modes'
    ]
  },
  
  {
    name: 'cosmic-eras',
    title: 'The Cosmic Eras Framework',
    description: 'History as progressive sophistication',
    suited_for: {
      'understand-connection': 100,
      'long': 100,
      'holistic': 95,
      'explore': 100,
      'biological-system': 80,
      'learning-growth': 60,
      'understand': 85,
      'practical': 50,
      'technical': 70,
      'economic-social': 70
    },
    related_resources: [
      'case-studies',
      'domain-mapper'
    ]
  },
  
  {
    name: 'binary-computing',
    title: 'Binary Computing Logic',
    description: 'Pure computational logic and self-verification',
    suited_for: {
      'technology-ai': 100,
      'technical': 100,
      'understand': 90,
      'apply': 85,
      'immediate': 80,
      'physics-system': 40,
      'holistic': 50,
      'practical': 70,
      'teach': 80
    },
    related_resources: [
      'concept-explorer',
      'case-studies'
    ]
  }
];

function updateProgress() {
  const answers = {
    situation: document.querySelector('input[name="situation"]:checked'),
    question: document.querySelector('input[name="question"]:checked'),
    timescale: document.querySelector('input[name="timescale"]:checked'),
    background: document.querySelector('input[name="background"]:checked'),
    goal: document.querySelector('input[name="goal"]:checked')
  };
  
  let answered = 0;
  for (let key in answers) {
    if (answers[key]) answered++;
  }
  
  const total = 5;
  const percent = (answered / total) * 100;
  document.getElementById('progress-fill').style.width = percent + '%';
  document.getElementById('progress-label').textContent = `Question ${answered + 1} of ${total}`;
}

function calculateRecommendations() {
  const situation = document.querySelector('input[name="situation"]:checked')?.value;
  const question = document.querySelector('input[name="question"]:checked')?.value;
  const timescale = document.querySelector('input[name="timescale"]:checked')?.value;
  const background = document.querySelector('input[name="background"]:checked')?.value;
  const goal = document.querySelector('input[name="goal"]:checked')?.value;
  
  if (!situation || !question || !timescale || !background || !goal) {
    alert('Please answer all questions');
    return;
  }
  
  // Score each framework
  const scores = frameworks.map(fw => {
    let score = 0;
    const answers = { situation, question, timescale, background, goal };
    
    for (let answer in answers) {
      score += fw.suited_for[answers[answer]] || 0;
    }
    
    return {
      ...fw,
      score: Math.round(score / 5) // Average score
    };
  }).sort((a, b) => b.score - a.score);
  
  // Show results
  document.getElementById('intro-section').style.display = 'none';
  document.getElementById('results-section').classList.add('active');
  
  const intro = `Based on your answers, here are the frameworks that best match what you're trying to do:`;
  document.getElementById('recommendations-intro').textContent = intro;
  
  const resultsHTML = scores.slice(0, 3).map((fw, idx) => {
    const matchPercent = Math.min(100, fw.score);
    return `
      <div class="result-card" style="background: linear-gradient(135deg, hsl(${idx * 100}, 70%, 50%) 0%, hsl(${idx * 100 + 60}, 70%, 50%) 100%);">
        <div class="result-framework">#${idx + 1}: ${fw.title}</div>
        <div class="result-description">${fw.description}</div>
        <div class="match-bar">
          <div class="match-fill" style="width: ${matchPercent}%;"></div>
        </div>
        <div style="font-size: 0.9rem; margin: 0.75rem 0;">${matchPercent}% match for your needs</div>
        <a href="/wiki/${fw.name}/" class="result-action" onclick="event.stopPropagation();">Learn More →</a>
      </div>
    `;
  }).join('');
  
  document.getElementById('results-container').innerHTML = resultsHTML;
  
  // Show understanding section
  setTimeout(() => {
    document.getElementById('understanding-section').style.display = 'block';
    initializeUnderstandingTracker(scores);
    document.getElementById('understanding-section').scrollIntoView({ behavior: 'smooth' });
  }, 500);
}

function initializeUnderstandingTracker(recommendations) {
  const concepts = [
    'Universal Foundation (dℹ/dt = -∇Φ)',
    'Potential Landscapes & Stability',
    'Gradient Descent & Change',
    'Help Systems Framework',
    'Learning & Growth',
    'Cross-Domain Connections'
  ];
  
  const html = concepts.map(concept => `
    <div class="concept-card">
      <div class="concept-name">${concept}</div>
      <div style="margin-top: 1rem;">
        <label style="display: flex; gap: 0.5rem; margin: 0.5rem 0;">
          <input type="radio" name="concept-${concept}" value="0" checked>
          <span>🔴 Novice</span>
        </label>
        <label style="display: flex; gap: 0.5rem; margin: 0.5rem 0;">
          <input type="radio" name="concept-${concept}" value="1">
          <span>🟡 Intermediate</span>
        </label>
        <label style="display: flex; gap: 0.5rem; margin: 0.5rem 0;">
          <input type="radio" name="concept-${concept}" value="2">
          <span>🟢 Proficient</span>
        </label>
      </div>
    </div>
  `).join('');
  
  document.getElementById('understanding-tracker').innerHTML = html;
}

function saveUnderstanding() {
  alert('✓ Your understanding profile saved! Visit Verification Tracker to log your progress.');
}

function showAllFrameworks() {
  window.location.href = '/wiki/framework-explorer/';
}

// Initialize
window.addEventListener('load', updateProgress);
</script>
