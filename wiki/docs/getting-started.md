---
layout: default
title: "Getting Started - Find Your Learning Path"
permalink: /getting-started/
toc: false
description: "Diagnostic quiz to personalize your wiki journey"
status: published
difficulty: "Beginner"
reading_time: "5 minutes"
entry_point: "All users - starts here for personalization"
---

<style>
.quiz-container {
  max-width: 800px;
  margin: 40px auto;
}

.question-section {
  background: #f8f9fa;
  padding: 30px;
  margin: 30px 0;
  border-radius: 12px;
  border-left: 4px solid #667eea;
  display: none;
}

.question-section.active {
  display: block;
}

.question-section h2 {
  color: #667eea;
  margin-top: 0;
  font-size: 1.5em;
}

.question-section p {
  color: #666;
  font-size: 1.1em;
  margin: 20px 0;
  line-height: 1.6;
}

.option-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
  margin: 25px 0;
}

.option-button {
  padding: 20px;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  font-size: 1em;
}

.option-button:hover {
  border-color: #667eea;
  background: #f0f4ff;
  transform: translateX(5px);
}

.option-button.selected {
  border-color: #667eea;
  background: #667eea;
  color: white;
}

.option-button strong {
  display: block;
  font-size: 1.1em;
  margin-bottom: 5px;
}

.option-button small {
  display: block;
  opacity: 0.8;
  font-size: 0.9em;
  margin-top: 8px;
}

.nav-buttons {
  display: flex;
  gap: 15px;
  margin: 40px 0;
  justify-content: space-between;
}

.btn {
  padding: 12px 25px;
  border: 2px solid #667eea;
  background: white;
  color: #667eea;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
}

.btn:hover {
  background: #667eea;
  color: white;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.progress-bar {
  height: 6px;
  background: #e0e0e0;
  border-radius: 3px;
  margin: 20px 0;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  width: 0%;
  transition: width 0.3s ease;
}

.results-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px;
  border-radius: 12px;
  margin: 40px 0;
  text-align: center;
  display: none;
}

.results-section.active {
  display: block;
}

.results-section h2 {
  margin-top: 0;
  font-size: 2em;
}

.result-path {
  background: rgba(255,255,255,0.1);
  padding: 25px;
  border-radius: 8px;
  margin: 20px 0;
  text-align: left;
  border-left: 4px solid white;
}

.result-path h3 {
  margin-top: 0;
  font-size: 1.3em;
}

.result-path p {
  font-size: 0.95em;
  line-height: 1.6;
  margin: 10px 0;
}

.result-path a {
  display: inline-block;
  margin-top: 15px;
  padding: 10px 20px;
  background: rgba(255,255,255,0.2);
  color: white;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s ease;
}

.result-path a:hover {
  background: rgba(255,255,255,0.3);
  transform: translateY(-2px);
}

.restart-button {
  display: inline-block;
  margin-top: 20px;
  padding: 12px 25px;
  background: rgba(255,255,255,0.2);
  color: white;
  border: 2px solid white;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
}

.restart-button:hover {
  background: rgba(255,255,255,0.3);
}

.intro-section {
  background: #f0f4ff;
  border-left: 4px solid #667eea;
  padding: 30px;
  margin: 30px 0;
  border-radius: 8px;
  display: block;
}

.intro-section.hidden {
  display: none;
}

.intro-section h2 {
  color: #667eea;
  margin-top: 0;
}

.start-quiz-btn {
  display: inline-block;
  margin-top: 20px;
  padding: 15px 30px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1em;
  transition: all 0.2s ease;
}

.start-quiz-btn:hover {
  background: #764ba2;
  transform: translateY(-2px);
}

@media (max-width: 600px) {
  .option-grid {
    grid-template-columns: 1fr;
  }
  
  .nav-buttons {
    flex-direction: column;
  }
  
  .nav-buttons .btn {
    width: 100%;
  }
}
</style>

<div class="quiz-container">

<div class="intro-section" id="intro">
  <h2>✦ Welcome to the Wiki</h2>
  <p>This is a quick diagnostic to personalize your learning path. We'll ask you 3 questions and recommend where to start based on your interests, time available, and learning style.</p>
  <p><strong>This takes 2 minutes.</strong> Your answers help us recommend the best entry point for you.</p>
  <button class="start-quiz-btn" onclick="startQuiz()">Start the Quiz →</button>
</div>

<div id="quiz" style="display: none;">
  <div class="progress-bar">
    <div class="progress-fill" id="progressFill"></div>
  </div>

  <!-- Question 1: What Interests You? -->
  <div class="question-section active" id="q1">
    <h2>Question 1 of 3: What Interests You Most?</h2>
    <p>Choose the topic that resonates most with you right now.</p>
    
    <div class="option-grid">
      <button class="option-button" data-value="human" onclick="selectOption('q1', 'human', 'Human Development')">
        <strong>🎯 Human Development</strong>
        <small>How people actually develop genuine competence and internal coherence</small>
      </button>
      
      <button class="option-button" data-value="zero-error" onclick="selectOption('q1', 'zero-error', 'Zero-Error Computing')">
        <strong>⚙️ Zero-Error Computing</strong>
        <small>How to verify logic while thinking about it—catch bugs before they matter</small>
      </button>
      
      <button class="option-button" data-value="physics" onclick="selectOption('q1', 'physics', 'Physics & Universe')">
        <strong>🌌 Physics & Universe</strong>
        <small>How the same patterns appear everywhere, from particles to civilization</small>
      </button>
      
      <button class="option-button" data-value="complete" onclick="selectOption('q1', 'complete', 'All Three Integrated')">
        <strong>🔮 All Three Integrated</strong>
        <small>See how all three systems connect and teach the same structure</small>
      </button>
      
      <button class="option-button" data-value="unsure" onclick="selectOption('q1', 'unsure', 'Not Sure Yet')">
        <strong>❓ Not Sure Yet</strong>
        <small>I want a guided overview first</small>
      </button>
    </div>
  </div>

  <!-- Question 2: How Much Time? -->
  <div class="question-section" id="q2">
    <h2>Question 2 of 3: How Much Time Do You Have?</h2>
    <p>Choose roughly how much time you want to invest in learning right now.</p>
    
    <div class="option-grid">
      <button class="option-button" data-value="15min" onclick="selectOption('q2', '15min', '15 minutes')">
        <strong>⏱️ 15 Minutes</strong>
        <small>Quick overview - understand the core concept</small>
      </button>
      
      <button class="option-button" data-value="1hour" onclick="selectOption('q2', '1hour', '1 hour')">
        <strong>⏰ 1 Hour</strong>
        <small>Solid foundation - core concepts with examples</small>
      </button>
      
      <button class="option-button" data-value="1day" onclick="selectOption('q2', '1day', '1 day (6-8 hours)')">
        <strong>📅 1 Day</strong>
        <small>Deep dive - multiple systems and applications</small>
      </button>
      
      <button class="option-button" data-value="1week" onclick="selectOption('q2', '1week', '1 week (40-50 hours)')">
        <strong>📆 1 Week+</strong>
        <small>Mastery - complete integration and expertise</small>
      </button>
      
      <button class="option-button" data-value="flexible" onclick="selectOption('q2', 'flexible', 'Flexible')">
        <strong>🔄 Flexible</strong>
        <small>Mix of short reads and deep dives over time</small>
      </button>
    </div>
  </div>

  <!-- Question 3: Learning Style -->
  <div class="question-section" id="q3">
    <h2>Question 3 of 3: How Do You Like to Learn?</h2>
    <p>Choose the learning style that works best for you.</p>
    
    <div class="option-grid">
      <button class="option-button" data-value="read" onclick="selectOption('q3', 'read', 'Read-First')">
        <strong>📖 Read-First</strong>
        <small>Deep text, examples, complete explanations</small>
      </button>
      
      <button class="option-button" data-value="visual" onclick="selectOption('q3', 'visual', 'Visual')">
        <strong>🗺️ Visual</strong>
        <small>Maps, diagrams, structure visualizations</small>
      </button>
      
      <button class="option-button" data-value="interactive" onclick="selectOption('q3', 'interactive', 'Interactive')">
        <strong>🎬 Interactive</strong>
        <small>Animations, visualizations you can interact with</small>
      </button>
      
      <button class="option-button" data-value="hands-on" onclick="selectOption('q3', 'hands-on', 'Hands-On')">
        <strong>🛠️ Hands-On</strong>
        <small>Tutorials, templates, things I can apply immediately</small>
      </button>
    </div>
  </div>

  <div class="nav-buttons">
    <button class="btn" onclick="previousQuestion()" id="prevBtn" disabled>← Back</button>
    <span style="text-align: center; flex: 1; color: #667eea; font-weight: 600;" id="stepCounter">Question 1 of 3</span>
    <button class="btn" onclick="nextQuestion()" id="nextBtn">Next →</button>
  </div>
</div>

<!-- Results -->
<div class="results-section" id="results">
  <h2>Your Personalized Learning Path</h2>
  <p id="resultIntro"></p>
  <div id="resultPath"></div>
  <button class="restart-button" onclick="restartQuiz()">Take Quiz Again</button>
</div>

</div>

<script>
let currentQuestion = 1;
const totalQuestions = 3;
let answers = {
  q1: null,
  q2: null,
  q3: null
};

const results = {
  // Topic-focused paths
  human: {
    title: "🎯 Human Development Path",
    intro: "You want to understand how people actually develop genuine competence.",
    paths: {
      "15min": {
        title: "Quick Foundation (15 minutes)",
        description: "Get the core insight in minimal time.",
        steps: [
          "Read: <a href='/goal-blindness/'>Goal-Blindness</a> (5 min) - The root cause",
          "Read: <a href='/internal-coherence/'>Internal Coherence</a> (5 min) - How development works",
          "Explore: <a href='/universal-foundation/'>10 Gates</a> (5 min) - The framework"
        ]
      },
      "1hour": {
        title: "Solid Foundation (1 hour)",
        description: "Complete foundation with examples and applications.",
        steps: [
          "Start: <a href='/for-humans/'>For Humans</a> (30 min) - Complete introduction",
          "Explore: <a href='/help-systems/'>Help Systems</a> (15 min) - See the paradox",
          "Reference: <a href='/universal-foundation/'>10 Gates</a> (15 min) - Deep dive"
        ]
      },
      "1day": {
        title: "Deep Dive (1 day)",
        description: "Complete system with 3 domain applications.",
        steps: [
          "Follow: <a href='/reference/learning-paths/introduction/'>Introduction Path</a> (8 hours) - Guided day-long learning",
          "Includes: All 10 gates, 3 domain applications, complete examples",
          "Result: Expert-level understanding of System 1"
        ]
      },
      "1week": {
        title: "Mastery Program (1+ weeks)",
        description: "Complete integration with all applications and implications.",
        steps: [
          "Follow: <a href='/reference/learning-paths/mastery/'>Mastery Learning Path</a> (40+ hours) - Month-long program",
          "Learn: All 10 gates in depth, all 10 domain applications, complete examples",
          "Integrate: Connection to Systems 2 and 3"
        ]
      },
      "flexible": {
        title: "Flexible Learning",
        description: "Mix of quick reads and deeper exploration.",
        steps: [
          "Start: <a href='/for-humans/'>For Humans</a> (as much time as you have)",
          "Then: Pick any gate from <a href='/universal-foundation/'>10 Gates</a> that interests you",
          "Explore: <a href='/universal-foundation/'>Domain Applications</a> in your field"
        ]
      }
    }
  },
  
  "zero-error": {
    title: "⚙️ Zero-Error Computing Path",
    intro: "You want to learn how to catch errors before they matter.",
    paths: {
      "15min": {
        title: "Quick Overview (15 minutes)",
        description: "Understand the core concept.",
        steps: [
          "Read: <a href='/zero-error-mandate/'>Zero-Error Mandate</a> (5 min) - The principle",
          "Skim: <a href='/zero-error-quick-ref/'>Quick Reference</a> (5 min) - Tools overview",
          "Watch: <a href='/zero-error-validator/'>Validator Tool</a> (5 min) - How it works"
        ]
      },
      "1hour": {
        title: "Solid Foundation (1 hour)",
        description: "Understand and start implementing.",
        steps: [
          "Read: <a href='/zero-error-mandate/'>Mandate</a> (15 min) - Philosophy and approach",
          "Read: <a href='/zero-error-task-template/'>Task Template</a> (20 min) - 8-phase workflow",
          "Explore: <a href='/zero-error-quick-ref/'>Quick Reference</a> (15 min) - All tools",
          "Plan: <a href='/zero-error-integration/'>Integration Guide</a> (10 min) - How to start"
        ]
      },
      "1day": {
        title: "Full Implementation (1 day)",
        description: "Complete setup and first project.",
        steps: [
          "Follow: <a href='/zero-error-integration/'>Integration Guide</a> - Complete setup",
          "Study: <a href='/zero-error-task-template/'>Task Template</a> - Understand workflow",
          "Do: Set up in your repo and run your first verification"
        ]
      },
      "1week": {
        title: "Mastery (1+ weeks)",
        description: "Complete system integration and optimization.",
        steps: [
          "Implement: Full System 2 with all tools",
          "Explore: <a href='/zero-error-git-hooks/'>Git Hooks</a> for team setup",
          "Study: <a href='/human-development/gates/'>Gates applications</a> for your thinking",
          "Optimize: Custom rules and workflows"
        ]
      },
      "flexible": {
        title: "Flexible Learning",
        description: "Learn at your own pace.",
        steps: [
          "Start: <a href='/zero-error-mandate/'>Mandate</a> when you want",
          "Explore: <a href='/zero-error-task-template/'>Task Template</a> when implementing",
          "Reference: <a href='/zero-error-quick-ref/'>Quick Reference</a> as needed"
        ]
      }
    }
  },
  
  physics: {
    title: "🌌 Physics & Universe Path",
    intro: "You want to see how these patterns appear at every scale.",
    paths: {
      "15min": {
        title: "Quick Overview (15 minutes)",
        description: "See the big picture.",
        steps: [
          "Read: <a href='/elections-roadmap/'>Elections Roadmap</a> (5 min) - What you're seeing",
          "Watch: <a href='/election-1-distinction/'>Election 1</a> (5 min) - Distinction animation",
          "Explore: <a href='/whitepaper-unified-photon-field/'>Whitepaper</a> intro (5 min) - The model"
        ]
      },
      "1hour": {
        title: "Visual Tour (1 hour)",
        description: "See animations and understand the framework.",
        steps: [
          "Read: <a href='/elections-roadmap/'>Elections Roadmap</a> (10 min) - The journey",
          "Watch: <a href='/election-1-distinction/'>Elections 1-2</a> (20 min) - First animations",
          "Read: <a href='/whitepaper-unified-photon-field/'>Whitepaper</a> (20 min) - How it works",
          "Explore: <a href='/cosmic-unfolding/'>Cosmic Unfolding</a> (10 min) - Integration"
        ]
      },
      "1day": {
        title: "Complete System (1 day)",
        description: "See all 5 elections and understand the complete model.",
        steps: [
          "Follow: <a href='/elections-roadmap/'>Elections Roadmap</a> - Complete journey",
          "Watch: All 5 election animations",
          "Study: <a href='/whitepaper-unified-photon-field/'>Physics model</a> - Deep dive",
          "Connect: <a href='/cosmic-unfolding/'>How it appears</a> at every scale"
        ]
      },
      "1week": {
        title: "Mastery (1+ weeks)",
        description: "Complete understanding plus animation tutorial.",
        steps: [
          "Study: All 5 elections in detail",
          "Learn: <a href='/animation-tutorial/'>Animation tutorial</a> - Build your own",
          "Integrate: <a href='/cosmic-unfolding/'>Cosmic unfolding</a> with Systems 1 & 2",
          "Create: Your own visualizations"
        ]
      },
      "flexible": {
        title: "Flexible Exploration",
        description: "Explore elections as you want.",
        steps: [
          "Start: <a href='/elections-roadmap/'>Elections Roadmap</a> for orientation",
          "Then: Watch any election that interests you",
          "Reference: <a href='/whitepaper-unified-photon-field/'>Whitepaper</a> for deep dives"
        ]
      }
    }
  },
  
  complete: {
    title: "🔮 Integrated Systems Path",
    intro: "You want to see how all three systems connect.",
    paths: {
      "15min": {
        title: "Core Insight (15 minutes)",
        description: "Understand the unified pattern.",
        steps: [
          "Read: <a href='/why-this-matters/'>Why This Matters</a> (5 min) - The stakes",
          "Read: <a href='/goal-blindness/'>Goal-Blindness</a> (5 min) - Root cause",
          "See: <a href='/help-system-visual/'>Structure Maps</a> (5 min) - How they connect"
        ]
      },
      "1hour": {
        title: "Integration Overview (1 hour)",
        description: "See how all three systems teach the same thing.",
        steps: [
          "Read: <a href='/help-system-blueprint/'>Help System Blueprint</a> (15 min) - What's integrated",
          "Read: <a href='/for-humans/'>For Humans</a> section 1 (15 min) - System 1 foundation",
          "Skim: <a href='/zero-error-mandate/'>Zero-Error Mandate</a> (15 min) - System 2 principle",
          "Watch: <a href='/election-1-distinction/'>Election 1</a> (15 min) - System 3 visual"
        ]
      },
      "1day": {
        title: "Complete Integration (1 day)",
        description: "Learn all three systems and their connections.",
        steps: [
          "Follow: <a href='/reference/integration/binary-foundation/'>Binary Foundation</a> - Shows same structure",
          "Study: System 1 foundations",
          "Study: System 2 frameworks",
          "Study: System 3 physics",
          "See: How they mirror each other"
        ]
      },
      "1week": {
        title: "Mastery Integration (1+ weeks)",
        description: "Expert-level understanding across all three systems.",
        steps: [
          "Follow: <a href='/reference/learning-paths/mastery/'>Mastery Path</a> (40+ hours)",
          "Learn: All 10 gates and their computational parallels",
          "Learn: All physics elections and their applications",
          "Integrate: Build your own unified understanding"
        ]
      },
      "flexible": {
        title: "Flexible Integration",
        description: "Explore connections as you discover them.",
        steps: [
          "Start: <a href='/help-system-blueprint/'>Blueprint</a> for overview",
          "Then: Pick any system and explore it",
          "Connect: <a href='/reference/integration/'>Integration pages</a> show connections"
        ]
      }
    }
  },
  
  unsure: {
    title: "❓ Guided Overview Path",
    intro: "You're not sure yet. Let's start with an overview that helps you understand what this wiki contains.",
    paths: {
      "15min": {
        title: "5-Minute Overview",
        description: "Understand what you're looking at.",
        steps: [
          "Read this page again - you're on it",
          "Read: <a href='/help-system-blueprint/'>Help System Blueprint</a> (5 min) - What's here",
          "Check: <a href='/reference/faq/'>FAQ</a> - Quick answers"
        ]
      },
      "1hour": {
        title: "1-Hour Overview",
        description: "See all three systems at a glance.",
        steps: [
          "Read: <a href='/help-system-blueprint/'>Blueprint</a> (15 min) - Complete picture",
          "Skim: <a href='/help-system-architecture/'>Architecture</a> (20 min) - Content structure",
          "Explore: <a href='/help-system-visual/'>Visual maps</a> (15 min) - How it's organized",
          "Decide: Which system interests you most"
        ]
      },
      "1day": {
        title: "Exploration Day",
        description: "Try different parts and see what resonates.",
        steps: [
          "Spend 2 hours: System 1 - Read <a href='/for-humans/'>For Humans</a>",
          "Spend 2 hours: System 2 - Explore <a href='/zero-error-mandate/'>Zero-Error</a>",
          "Spend 2 hours: System 3 - Watch <a href='/elections-roadmap/'>Elections</a>",
          "Reflect: Which resonated most? Go deeper in that system"
        ]
      },
      "1week": {
        title: "Comprehensive Overview (1 week)",
        description: "Get full exposure to all three systems.",
        steps: [
          "Follow: <a href='/reference/learning-paths/introduction/'>Introduction Path</a> (8 hours)",
          "Then: Pick one system to go deeper",
          "Explore: How other systems connect"
        ]
      },
      "flexible": {
        title: "Organic Exploration",
        description: "Follow your curiosity.",
        steps: [
          "Start: <a href='/why-this-matters/'>Why This Matters</a> (no time commitment)",
          "Then: Click anything that interests you",
          "Let: The connections emerge naturally"
        ]
      }
    }
  }
};

function startQuiz() {
  document.getElementById('intro').classList.add('hidden');
  document.getElementById('quiz').style.display = 'block';
  updateProgress();
}

function selectOption(question, value, label) {
  answers[question] = value;
  
  // Update button styling
  const buttons = document.querySelectorAll(`#${question} .option-button`);
  buttons.forEach(btn => btn.classList.remove('selected'));
  event.target.closest('.option-button').classList.add('selected');
  
  // Enable next button
  document.getElementById('nextBtn').disabled = false;
}

function nextQuestion() {
  if (currentQuestion < totalQuestions) {
    document.getElementById(`q${currentQuestion}`).classList.remove('active');
    currentQuestion++;
    document.getElementById(`q${currentQuestion}`).classList.add('active');
    updateProgress();
    document.getElementById('nextBtn').disabled = false;
    
    if (currentQuestion === totalQuestions) {
      document.getElementById('nextBtn').textContent = 'See Results →';
    }
  } else {
    showResults();
  }
  
  if (currentQuestion > 1) {
    document.getElementById('prevBtn').disabled = false;
  }
}

function previousQuestion() {
  if (currentQuestion > 1) {
    document.getElementById(`q${currentQuestion}`).classList.remove('active');
    currentQuestion--;
    document.getElementById(`q${currentQuestion}`).classList.add('active');
    updateProgress();
    document.getElementById('nextBtn').disabled = false;
    document.getElementById('nextBtn').textContent = currentQuestion === totalQuestions ? 'See Results →' : 'Next →';
  }
  
  if (currentQuestion === 1) {
    document.getElementById('prevBtn').disabled = true;
  }
}

function updateProgress() {
  const progress = (currentQuestion / totalQuestions) * 100;
  document.getElementById('progressFill').style.width = progress + '%';
  document.getElementById('stepCounter').textContent = `Question ${currentQuestion} of ${totalQuestions}`;
}

function showResults() {
  // Determine which result set to show
  const topic = answers.q1;
  const time = answers.q2;
  const style = answers.q3;
  
  const resultSet = results[topic];
  
  // Build result HTML
  let html = `<div class="result-path">
    <h3>${resultSet.title}</h3>
    <p>${resultSet.intro}</p>`;
  
  if (resultSet.paths[time]) {
    const path = resultSet.paths[time];
    html += `<h4>${path.title}</h4>
    <p>${path.description}</p>
    <ul>`;
    path.steps.forEach(step => {
      html += `<li>${step}</li>`;
    });
    html += `</ul>
    </div>`;
  }
  
  // Add learning style note
  const styleInfo = {
    'read': 'You prefer deep text. Read the complete articles.',
    'visual': 'You learn visually. Check out the maps and diagrams.',
    'interactive': 'You like interactive content. Watch the animations.',
    'hands-on': 'You learn by doing. Use the templates and tutorials.'
  };
  
  html += `<div class="result-path" style="background: rgba(255,255,255,0.05);">
    <p><strong>Learning Style Note:</strong> ${styleInfo[style]}</p>
  </div>`;
  
  document.getElementById('resultPath').innerHTML = html;
  
  // Show results section
  document.getElementById('quiz').style.display = 'none';
  document.getElementById('results').classList.add('active');
}

function restartQuiz() {
  currentQuestion = 1;
  answers = { q1: null, q2: null, q3: null };
  
  // Reset UI
  document.querySelectorAll('.option-button').forEach(btn => btn.classList.remove('selected'));
  document.getElementById('intro').classList.remove('hidden');
  document.getElementById('quiz').style.display = 'none';
  document.getElementById('results').classList.remove('active');
  document.getElementById('q1').classList.add('active');
  document.getElementById('q2').classList.remove('active');
  document.getElementById('q3').classList.remove('active');
  document.getElementById('prevBtn').disabled = true;
  document.getElementById('nextBtn').disabled = true;
  document.getElementById('nextBtn').textContent = 'Next →';
  updateProgress();
}
</script>
