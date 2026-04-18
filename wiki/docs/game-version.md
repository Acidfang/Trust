---
layout: default
title: "The Discovery Game - Full Comprehension Learning"
permalink: /game/
---

# 🎮 The Discovery Game: Gates of Understanding

**Start at Tier -1. Everything you skip has consequences.**

---

## How This Works

You're not reading about gates. You're **discovering** them through scenarios, quizzes, and outcomes.

- **Answer correctly?** Pattern unlocks. You move deeper.
- **Answer wrong?** See why that thinking fails. Learn the hard way.
- **Skip the quiz?** Fine—but you'll hit a wall later. The consequence shows up.

Your transparent thinking will compound. Your gaps will compound harder.

---

<div id="game-container" style="min-height: 100vh; background: var(--color-bg-secondary); padding: 3rem 2rem; border-radius: 8px; margin: 2rem 0;">

## Starting the Game...

<button id="start-game-btn" style="padding: 1rem 2rem; font-size: 1.2rem; background: var(--color-accent); color: white; border: none; border-radius: 4px; cursor: pointer; margin: 2rem 0;">
🚀 Begin at Tier -1
</button>

<div id="game-ui" style="display: none; margin-top: 3rem;">
  <!-- Game UI will render here -->
</div>

</div>

---

## The Three Phases

### Phase 1: Tier -1 (Self-Awareness)
**Answer three quick questions about how you actually work.**

The most important stat: **Transparency**
- 🎯 100% = Completely honest, even shameful answers
- 😐 70% = Mostly honest, might soften some answers  
- 😷 30% = Answering how I want to be seen
- 😵 0% = Not thinking about it

If transparency is low, descriptions will be **foggy** (literally blurred) until you're honest with yourself.

**Why?** You can't discover gates if you're hiding from yourself.

---

### Phase 2: Tier 0 (Domain Selection)

**Choose a domain to explore**: Business, Biology, History, Technology, Art, Ethics

Some domains unlock based on your comprehension level. You can't jump straight to "Ethics" if you don't understand "Agency" yet.

The game respects the gate progression.

---

### Phase 3: Tier 1-3 (Learn Through Consequence)

**Quiz encounters in each domain.**

Each gate appears across multiple domains—same pattern, different context.

✅ **Correct answer**: "You understand Gate 3 at 'Recognizing' level"
- Unlocks visualization for that gate
- You start seeing it in other domains
- Your pattern recognition map fills in

❌ **Wrong answer**: "This thinking means... [consequence shown]"
- Not punishment. Just physics.
- Shows what your answer implies in the real world
- You can retry to understand better

⏭️ **Skip quiz**: "Coherence Debt: +8"
- Can't see the pattern across that domain
- Those connections stay foggy
- Debt accumulates; harder to make sense of things

---

## The Dashboard: Your Discovery Map

As you play, you'll see:

```
🎯 COMPREHENSION LEVELS
├─ Gate 1: Consequentialist ████████░░ 80%
├─ Gate 2: Denier ███░░░░░░░ 30% ⚠️
├─ Gate 3: Locked 🔒
└─ [More gates as you progress...]

📊 PATTERN RECOGNITION
├─ Gate 1 found in: Business, Biology, —
├─ Gate 2 found in: —
└─ [Map fills as you connect patterns...]

💔 COHERENCE DEBT: 0 (Perfect clarity)
   └─ Or if you've skipped: 23 (Heavy fog in 3 areas)

📈 TRANSPARENCY SCORE: 85%
   └─ How honest you're being changes everything

🏆 JOURNEY STAGE: Awakening
   └─ Progresses as you integrate learning
```

---

## Why This Is Actually Harder Than Reading

Reading pages = passive. You might understand.

This game = **active consequence**.

When you skip a quiz, you'll encounter a situation later where you need that knowledge. Wall hits hard.

When you answer wrong, you don't just see "that's wrong." You see the real-world failure that thinking causes.

When you're not being transparent, the _whole system shows you fog_. Literally fuzzy descriptions until you answer honestly.

**This is way faster to learn from, but way less comfortable.**

---

## The Rules

1. **You cannot break the gates.** They're ordered for a reason. You can't jump to Gate 8 without Gate 1.
2. **You cannot hide consequences.** Skip a quiz, it shows as debt. Debt blocks pattern recognition.
3. **You cannot fake transparency.** System detects inconsistent answers. Fog increases.
4. **You can always retry.** Wrong answers aren't failures—they're discoveries of what you don't understand yet.
5. **Skipping is allowed.** But the game remembers, and consequences compound.

---

## The Endgame

Complete comprehension = all 10 gates understood across 3+ domains each = you see the pattern everywhere.

You'll understand why civilizations collapse the same way organisms fail. Why business failures mirror physics symmetries. Why the same gap appears in art and ethics.

That's integration. That's depth. That's the game won.

---

<script src="{{ '/assets/js/civilization-models.js' | relative_url }}"></script>
<script src="{{ '/assets/js/civilization-renderer.js' | relative_url }}"></script>
<script src="{{ '/assets/js/game-engine.js' | relative_url }}"></script>

<script>
// Wait for game engine to initialize, then set up event handlers
function initializeGameUI() {
  const startBtn = document.getElementById('start-game-btn');
  const gameUI = document.getElementById('game-ui');

  if (!startBtn) return; // Game container not on this page

  startBtn.addEventListener('click', function(e) {
    e.preventDefault();
    startBtn.style.display = 'none';
    
    // Get diagnostic from game engine
    const diagnostic = window.game.getTier0Diagnostic();
    renderDiagnosticUI(diagnostic);
  });
}

function renderDiagnosticUI(diagnostic) {
  const gameUI = document.getElementById('game-ui');
  let html = '<h2>Tier -1: Who Are You Actually?</h2>';
  html += '<p style="font-style: italic; color: #666;">Three questions. Complete honesty. Your transparency score depends on it.</p>';
  
  diagnostic.questions.forEach((q, idx) => {
    html += `<div style="margin: 2rem 0; padding: 1.5rem; background: var(--color-bg); border-left: 4px solid var(--color-accent); border-radius: 4px;">`;
    html += `<h3>Q${idx + 1}: ${q.prompt}</h3>`;
    html += '<div style="margin-top: 1rem;">';
    
    q.answers.forEach((answer, ansIdx) => {
      html += `<label style="display: block; margin: 0.8rem 0; padding: 0.8rem; cursor: pointer; background: var(--color-bg-secondary); border-radius: 4px; transition: all 0.2s;">
        <input type="radio" name="diagnostic_q${idx}" value="${ansIdx}" style="margin-right: 0.5rem;">
        ${answer.text}
      </label>`;
    });
    
    html += '</div></div>';
  });
  
  html += `<button id="submit-diagnostic" style="padding: 1rem 2rem; font-size: 1.1rem; background: var(--color-accent); color: white; border: none; border-radius: 4px; cursor: pointer; margin: 2rem 0;">
    ✓ I'm Being Honest - Continue
  </button>`;
  
  gameUI.innerHTML = html;
  gameUI.style.display = 'block';
  
  // Set up submit handler
  document.getElementById('submit-diagnostic').addEventListener('click', function() {
    submitDiagnostic(diagnostic);
  });
}

function submitDiagnostic(diagnostic) {
  const answers = [];
  
  diagnostic.questions.forEach((q, idx) => {
    const selected = document.querySelector(`input[name="diagnostic_q${idx}"]:checked`);
    if (selected) {
      const answerValue = parseInt(selected.value);
      const answerObj = q.answers[answerValue];
      answers.push(answerObj);
    }
  });

  if (answers.length !== diagnostic.questions.length) {
    alert('Please answer all questions');
    return;
  }

  // Process diagnostic and show domain selection
  window.game.processDiagnostic(answers);
  const domainData = window.game.showDomainSelection();
  renderDomainSelection(domainData);
}

function renderDomainSelection(domainData) {
  const gameUI = document.getElementById('game-ui');
  let html = '<h2>Tier 0: Choose Your Path</h2>';
  html += '<p>Pick a domain to explore. Some unlock as you understand deeper gates.</p>';
  html += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin: 2rem 0;">';
  
  domainData.domains.forEach((domain, idx) => {
    const locked = !domain.unlocked;
    const style = locked 
      ? 'opacity: 0.6; pointer-events: none; cursor: not-allowed;' 
      : 'cursor: pointer; transition: transform 0.2s ease, box-shadow 0.2s ease;';
    
    html += `<div id="domain_${idx}" style="padding: 1.5rem; background: var(--color-bg); border: 2px solid var(--color-accent); border-radius: 8px; ${style}" ${!locked ? `onclick="exploreDomain('${domain.name}', ${idx})"` : ''}>
      <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">${domain.icon}</div>
      <h3 style="margin: 0.5rem 0;">${domain.name}</h3>
      <p style="color: #666; margin: 0.5rem 0; font-size: 0.95rem;">${domain.description}</p>
      ${locked ? `<p style="color: #ff9800; font-size: 0.9rem; margin-top: 1rem;">🔒 Unlocks at Tier ${Math.ceil(domain.gatesUsed[0] / 2)}</p>` : '<p style="color: #4caf50; font-size: 0.9rem; margin-top: 1rem;">✓ Available</p>'}
    </div>`;
  });
  
  html += '</div>';
  gameUI.innerHTML = html;
}

function exploreDomain(domainName, idx) {
  const gameUI = document.getElementById('game-ui');
  const quizzes = window.game.quizData[domainName.toLowerCase().replace(/ /g, '')] || [];
  
  if (quizzes.length === 0) {
    gameUI.innerHTML = `<h2>Loading ${domainName}...</h2><p>Quiz system initializing...</p>`;
    return;
  }
  
  renderQuizUI(quizzes[0], domainName);
}

function renderQuizUI(quiz, domain) {
  const gameUI = document.getElementById('game-ui');
  let html = `<h2>Gate ${quiz.gate}: ${domain}</h2>`;
  html += `<p style="font-size: 1.1rem; margin: 1rem 0;">${quiz.question}</p>`;
  html += '<div style="display: grid; grid-template-columns: 1fr; gap: 1rem; margin: 2rem 0;">';
  
  quiz.answers.forEach((answer, idx) => {
    html += `<label style="padding: 1rem; background: var(--color-bg-secondary); border: 2px solid transparent; border-radius: 4px; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.borderColor='var(--color-accent)'" onmouseout="this.style.borderColor='transparent'">
      <input type="radio" name="quiz_answer" value="${idx}" style="margin-right: 0.5rem;">
      ${answer.text}
    </label>`;
  });
  
  html += '</div>';
  html += `<button id="submit-answer" style="padding: 1rem 2rem; font-size: 1.1rem; background: var(--color-accent); color: white; border: none; border-radius: 4px; cursor: pointer; margin: 1rem 0 1rem 0;">
    Submit Answer
  </button>
  <button id="skip-answer" style="padding: 1rem 2rem; font-size: 1.1rem; background: #ff9800; color: white; border: none; border-radius: 4px; cursor: pointer; margin: 1rem 0 1rem 1rem;">
    Skip Quiz
  </button>`;
  
  gameUI.innerHTML = html;
  
  document.getElementById('submit-answer').addEventListener('click', function() {
    const selected = document.querySelector('input[name="quiz_answer"]:checked');
    if (!selected) {
      alert('Please select an answer');
      return;
    }
    const answerIdx = parseInt(selected.value);
    const answer = quiz.answers[answerIdx];
    
    const result = window.game.processQuizAnswer(answer, quiz, domain);
    renderQuizResult(result, quiz, domain);
  });
  
  document.getElementById('skip-answer').addEventListener('click', function() {
    const result = window.game.processSkip(quiz, domain);
    renderSkipResult(result, quiz, domain);
  });
}

function renderQuizResult(result, quiz, domain) {
  const gameUI = document.getElementById('game-ui');
  let html = '';
  
  if (result.type === 'correct') {
    html += '<div style="background: #c8e6c9; border-left: 5px solid #4caf50; padding: 1.5rem; border-radius: 4px; margin: 2rem 0;">';
    html += '<h2 style="color: #2e7d32; margin-top: 0;">✓ Correct!</h2>';
    html += '<p>' + result.message + '</p>';
    html += '</div>';
    
    // SHOW TIER ADVANCEMENT IF PLAYER ADVANCED (CAUSAL CHAIN)
    if (result.tierAdvancement && result.tierAdvancement.advanced) {
      html += '<div style="background: #fff8e1; border-left: 5px solid #ffd700; padding: 2rem; border-radius: 4px; margin: 2rem 0; text-align: center;">';
      html += '<h2 style="color: #f57f17; margin: 0 0 1rem 0;">🎓 TIER ADVANCEMENT!</h2>';
      html += `<p style="font-size: 1.1rem; margin: 0.5rem 0;"><strong>You advanced from Tier ${result.tierAdvancement.oldTier} to Tier ${result.tierAdvancement.newTier}</strong></p>`;
      html += `<p style="margin: 0.5rem 0; font-style: italic;">${result.tierAdvancement.description}</p>`;
      
      if (result.tierAdvancement.newDomainsUnlocked && result.tierAdvancement.newDomainsUnlocked.length > 0) {
        html += '<p style="margin: 1rem 0; color: #f57f17;"><strong>🔓 New Domains Unlocked:</strong></p>';
        html += '<p style="margin: 0;">' + result.tierAdvancement.newDomainsUnlocked.join(', ') + '</p>';
      }
      html += '</div>';
    }
  } else {
    html += '<div style="background: #ffccbc; border-left: 5px solid #ff5722; padding: 1.5rem; border-radius: 4px; margin: 2rem 0;">';
    html += '<h2 style="color: #d84315; margin-top: 0;">✗ Not Quite</h2>';
    html += '<p><strong>You chose:</strong> ' + result.message.replace(/You chose: "/, '').replace(/"$/, '') + '</p>';
    html += '<p><strong>What this means:</strong> ' + result.whatThisMeans + '</p>';
    html += '<p><strong>In reality:</strong> ' + result.realOutcome + '</p>';
    html += '</div>';
  }
  
  // Show civilization outcome if available
  if (result.civilization) {
    html += '<h3 style="margin-top: 2rem;">What This Choice Produces</h3>';
    html += '<div style="background: white; padding: 1.5rem; border-radius: 4px; border: 1px solid #ddd;">';
    html += renderCivilizationOutcomeCard(result.civilization);
    html += '</div>';
  }
  
  // Show progress toward next tier if not advanced
  if (!result.tierAdvancement?.advanced && result.tierAdvancement?.gatesProgress) {
    html += '<div style="background: #e3f2fd; border-left: 5px solid #2196f3; padding: 1rem; border-radius: 4px; margin: 1.5rem 0;">';
    html += '<p style="margin: 0;"><strong>Progress to Next Tier:</strong><br>';
    html += `Gates: ${result.tierAdvancement.gatesProgress} | Domains: ${result.tierAdvancement.domainsProgress}</p>`;
    html += '</div>';
  }
  
  html += `<div style="margin-top: 2rem;">
    <button onclick="location.reload()" style="padding: 1rem 2rem; background: var(--color-accent); color: white; border: none; border-radius: 4px; cursor: pointer;">
      Continue
    </button>
  </div>`;
  
  gameUI.innerHTML = html;
}

function renderCivilizationOutcomeCard(civ) {
  let html = `<h4>${civ.title}</h4>`;
  html += `<p><em>${civ.timespan}</em></p>`;
  html += `<p><strong>Cities healthy:</strong> ${civ.cities_healthy} / ${civ.population}</p>`;
  if (civ.cities_struggling) html += `<p><strong>Cities struggling:</strong> ${civ.cities_struggling}</p>`;
  if (civ.cities_collapsed) html += `<p><strong>Cities collapsed:</strong> ${civ.cities_collapsed}</p>`;
  
  return html;
}

function renderSkipResult(result, quiz, domain) {
  const gameUI = document.getElementById('game-ui');
  let html = '';
  
  html += '<div style="background: #fff3e0; border-left: 5px solid #ff9800; padding: 1.5rem; border-radius: 4px; margin: 2rem 0;">';
  html += '<h2 style="color: #e65100; margin-top: 0;">⏭️ Skipped</h2>';
  html += '<p>' + result.message + '</p>';
  html += '<p><strong>💔 Coherence Debt: +' + result.debt + '</strong></p>';
  html += '<p style="color: #666;">' + result.consequence.meaning + '</p>';
  html += '</div>';
  
  html += `<div style="margin-top: 2rem;">
    <button onclick="location.reload()" style="padding: 1rem 2rem; background: var(--color-accent); color: white; border: none; border-radius: 4px; cursor: pointer;">
      Continue
    </button>
  </div>`;
  
  gameUI.innerHTML = html;
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeGameUI);
} else {
  // DOM already loaded
  initializeGameUI();
}
</script>

<style>
#game-container {
  font-family: inherit;
}

#game-container h2 {
  color: var(--color-accent);
  margin-bottom: 1rem;
}

#game-container h3 {
  margin-bottom: 0.5rem;
}

#game-container input[type="radio"] {
  appearance: none;
  -webkit-appearance: none;
  width: 1.2rem;
  height: 1.2rem;
  border: 2px solid var(--color-accent);
  border-radius: 50%;
  cursor: pointer;
  vertical-align: middle;
}

#game-container input[type="radio"]:checked {
  background: var(--color-accent);
}

#game-container label {
  transition: all 0.2s;
}

#game-container label:hover {
  background: var(--color-accent) !important;
  color: white;
}
</style>
