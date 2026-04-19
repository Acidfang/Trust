---
layout: page
title: Reality's Timeline - Interactive Navigator
permalink: /timeline-navigator/
description: Interactive navigation through the unfolding of reality from diffusion to now
---

# Reality's Timeline Navigator

Click on any stage to explore that era of cosmic evolution.

<style>
.timeline-container {
  position: relative;
  max-width: 100%;
  overflow-x: auto;
  margin: 2rem 0;
  padding: 2rem 0;
}

.timeline-track {
  display: flex;
  gap: 1rem;
  min-width: 200%;
  padding: 0 1rem;
  position: relative;
}

.timeline-track::before {
  content: '';
  position: absolute;
  top: 30px;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #ff6b6b, #ffd93d, #6bcf7f, #4db8ff, #b19cd9);
  z-index: 1;
}

.timeline-stage {
  flex: 0 0 140px;
  text-align: center;
  position: relative;
  z-index: 2;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.timeline-stage:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.timeline-dot {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  margin: 0 auto 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  background: white;
  border: 3px solid #2196F3;
  cursor: pointer;
}

.timeline-stage.early .timeline-dot { border-color: #ff6b6b; background: #ffe6e6; }
.timeline-stage.ancient .timeline-dot { border-color: #ffd93d; background: #fffacd; }
.timeline-stage.growth .timeline-dot { border-color: #6bcf7f; background: #e8f5e9; }
.timeline-stage.current .timeline-dot { border-color: #4db8ff; background: #e3f2fd; }
.timeline-stage.future .timeline-dot { border-color: #b19cd9; background: #f3e5f5; }

.timeline-label {
  font-size: 0.75rem;
  font-weight: bold;
  margin-bottom: 0.3rem;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.timeline-time {
  font-size: 0.65rem;
  color: #888;
  white-space: nowrap;
}

.stage-detail {
  display: none;
  background: #f9f9f9;
  border: 2px solid #2196F3;
  border-radius: 8px;
  padding: 2rem;
  margin: 2rem 0;
  animation: slideIn 0.3s ease;
}

.stage-detail.active {
  display: block;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stage-detail h2 {
  margin-top: 0;
  color: #2196F3;
  border-bottom: 2px solid #2196F3;
  padding-bottom: 0.5rem;
}

.stage-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin: 1rem 0;
}

.stat-box {
  background: white;
  border-left: 3px solid #2196F3;
  padding: 1rem;
  border-radius: 4px;
}

.stat-label {
  font-size: 0.8rem;
  color: #666;
  font-weight: bold;
  margin-bottom: 0.3rem;
}

.stat-value {
  font-size: 1.1rem;
  color: #2196F3;
  font-weight: bold;
}

.stage-key-insight {
  background: #fff3cd;
  border-left: 4px solid #ffc107;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 4px;
  font-weight: 500;
}

.stage-physics {
  background: #e8f5e9;
  border-left: 4px solid #4CAF50;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.9rem;
}

.nav-buttons {
  margin: 1rem 0;
  display: flex;
  gap: 0.5rem;
}

.nav-btn {
  padding: 0.5rem 1rem;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.2s;
}

.nav-btn:hover {
  background: #1976D2;
}

.nav-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.explore-link {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.7rem 1.4rem;
  background: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: bold;
  transition: background 0.2s;
}

.explore-link:hover {
  background: #388E3C;
}
</style>

<div class="timeline-container">
  <div class="timeline-track">
    <!-- Stage 0 -->
    <div class="timeline-stage early" onclick="showStage(0)">
      <div class="timeline-dot">∞</div>
      <div class="timeline-label">Diffusion</div>
      <div class="timeline-time">t=0</div>
    </div>

    <!-- Stage 1 -->
    <div class="timeline-stage early" onclick="showStage(1)">
      <div class="timeline-dot">💡</div>
      <div class="timeline-label">Photons</div>
      <div class="timeline-time">10⁻⁴³ s</div>
    </div>

    <!-- Stage 2 -->
    <div class="timeline-stage early" onclick="showStage(2)">
      <div class="timeline-dot">e⁻</div>
      <div class="timeline-label">Electrons</div>
      <div class="timeline-time">10⁻⁶ s</div>
    </div>

    <!-- Stage 3 -->
    <div class="timeline-stage early" onclick="showStage(3)">
      <div class="timeline-dot">⚛️</div>
      <div class="timeline-label">Nuclear Forces</div>
      <div class="timeline-time">1 s</div>
    </div>

    <!-- Stage 4 -->
    <div class="timeline-stage ancient" onclick="showStage(4)">
      <div class="timeline-dot">🔋</div>
      <div class="timeline-label">Nuclei</div>
      <div class="timeline-time">180 s</div>
    </div>

    <!-- Stage 5 -->
    <div class="timeline-stage ancient" onclick="showStage(5)">
      <div class="timeline-dot">🕳️</div>
      <div class="timeline-label">Atoms</div>
      <div class="timeline-time">380 kyr</div>
    </div>

    <!-- Stage 6 -->
    <div class="timeline-stage growth" onclick="showStage(6)">
      <div class="timeline-dot">🌌</div>
      <div class="timeline-label">Structure</div>
      <div class="timeline-time">100 Myr</div>
    </div>

    <!-- Stage 7 -->
    <div class="timeline-stage growth" onclick="showStage(7)">
      <div class="timeline-dot">⭐</div>
      <div class="timeline-label">Stars</div>
      <div class="timeline-time">1 Gyr</div>
    </div>

    <!-- Stage 8 -->
    <div class="timeline-stage growth" onclick="showStage(8)">
      <div class="timeline-dot">💫</div>
      <div class="timeline-label">Galaxies</div>
      <div class="timeline-time">3 Gyr</div>
    </div>

    <!-- Stage 9 -->
    <div class="timeline-stage current" onclick="showStage(9)">
      <div class="timeline-dot">⚗️</div>
      <div class="timeline-label">Chemistry</div>
      <div class="timeline-time">8 Gyr</div>
    </div>

    <!-- Stage 10 -->
    <div class="timeline-stage current" onclick="showStage(10)">
      <div class="timeline-dot">🧬</div>
      <div class="timeline-label">Life</div>
      <div class="timeline-time">13 Gyr</div>
    </div>

    <!-- Stage 11 -->
    <div class="timeline-stage current" onclick="showStage(11)">
      <div class="timeline-dot">🧠</div>
      <div class="timeline-label">Mind</div>
      <div class="timeline-time">Now</div>
    </div>

    <!-- Stage 12 -->
    <div class="timeline-stage future" onclick="showStage(12)">
      <div class="timeline-dot">🌟</div>
      <div class="timeline-label">Intent</div>
      <div class="timeline-time">Future</div>
    </div>
  </div>
</div>

<!-- Stage Details -->
<div id="stage-content"></div>

<script>
const stages = [
  {
    id: 0,
    title: "The Great Diffusion",
    emoji: "∞",
    timescale: "t = 0",
    description: "Infinitely compressed, infinitely hot. All forces unified.",
    stats: [
      { label: "Scale", value: "10⁻³⁵ m" },
      { label: "Temperature", value: "10³² K" },
      { label: "Age", value: "0 sec" }
    ],
    physics: "dℹ/dt = -∇Φ(all unified)",
    keyInsight: "Maximum gradient everywhere. System begins differentiating.",
    explore: "/cosmic-unfolding/#0-the-great-diffusion"
  },
  {
    id: 1,
    title: "Photon Epoch",
    emoji: "💡",
    timescale: "10⁻⁴³ to 10⁻⁶ sec",
    description: "First differentiation. Universe expands, photons emerge, potential separates.",
    stats: [
      { label: "Scale", value: "10⁻³⁵ to 10⁻¹² m" },
      { label: "Temperature", value: "10³² → 10¹⁵ K" },
      { label: "Primary particle", value: "Photons" }
    ],
    physics: "dℹ/dt = -∇Φ(expansion)",
    keyInsight: "Space expands. Density gradients create structure.",
    explore: "/cosmic-unfolding/#1-photon-epoch"
  },
  {
    id: 2,
    title: "Electron-Positron Epoch",
    emoji: "e⁻",
    timescale: "10⁻⁶ sec",
    description: "Matter appears. Electrons and positrons condense from photons.",
    stats: [
      { label: "Scale", value: "10⁻¹⁵ m" },
      { label: "Temperature", value: "10¹⁵ → 10¹¹ K" },
      { label: "Key process", value: "Pair production" }
    ],
    physics: "dℹ/dt = -∇Φ(charge interaction + gravity)",
    keyInsight: "Matter-antimatter asymmetry seeds all future complexity.",
    explore: "/cosmic-unfolding/#2-electron-positron-epoch"
  },
  {
    id: 3,
    title: "Hadron Epoch",
    emoji: "⚛️",
    timescale: "1 second",
    description: "Protons and neutrons become stable as strong nuclear force emerges.",
    stats: [
      { label: "Scale", value: "10⁻¹⁵ m" },
      { label: "Temperature", value: "10¹¹ → 10⁹ K" },
      { label: "Key process", value: "Strong nuclear force" }
    ],
    physics: "dℹ/dt = -∇Φ(strong nuclear)",
    keyInsight: "Strong force stabilizes fundamental nuclear particles.",
    explore: "/cosmic-unfolding/#3-hadron-epoch"
  },
  {
    id: 4,
    title: "Nucleosynthesis",
    emoji: "🔋",
    timescale: "1 to 180 seconds",
    description: "Protons fuse into nuclei. First atomic nuclei form.",
    stats: [
      { label: "Scale", value: "10⁻¹⁵ m" },
      { label: "Temperature", value: "10⁹ → 10⁷ K" },
      { label: "Main nuclei", value: "H, He, Li" }
    ],
    physics: "dℹ/dt = -∇Φ(nuclear fusion)",
    keyInsight: "Elements are forged. Foundation of chemistry laid.",
    explore: "/cosmic-unfolding/#4-nucleosynthesis"
  },
  {
    id: 5,
    title: "Photon Decoupling",
    emoji: "🕳️",
    timescale: "380,000 years",
    description: "Universe becomes transparent. Electrons bind to nuclei.",
    stats: [
      { label: "Scale", value: "10⁻¹⁰ m (atomic binding radius)" },
      { label: "Temperature", value: "10⁷ → 3,000 K" },
      { label: "Key event", value: "Atoms form" }
    ],
    physics: "dℹ/dt = -∇Φ(charge interaction)",
    keyInsight: "First atoms. Universe becomes transparent to light.",
    explore: "/cosmic-unfolding/#5-photon-decoupling"
  },
  {
    id: 6,
    title: "Structure Formation",
    emoji: "🌌",
    timescale: "100 million years",
    description: "Gravity amplifies tiny fluctuations into massive structures.",
    stats: [
      { label: "Scale", value: "10¹⁹ m (megaparsecs)" },
      { label: "Temperature", value: "3,000 → 100 K" },
      { label: "Main driver", value: "Gravity" }
    ],
    physics: "dℹ/dt = -∇Φ(gravitational)",
    keyInsight: "First galaxies form. Matter flows into potential wells.",
    explore: "/cosmic-unfolding/#6-structure-formation"
  },
  {
    id: 7,
    title: "First Stars",
    emoji: "⭐",
    timescale: "1 billion years",
    description: "Hydrogen clouds collapse. Nuclear fusion begins.",
    stats: [
      { label: "Scale", value: "10¹⁶ m (stellar)" },
      { label: "Temperature", value: "1 million K (core)" },
      { label: "Key process", value: "Nuclear fusion" }
    ],
    physics: "dℹ/dt = -∇Φ(gravity + nuclear)",
    keyInsight: "Fusion begins. Stars forge heavier elements.",
    explore: "/cosmic-unfolding/#7-first-stars"
  },
  {
    id: 8,
    title: "Galaxies",
    emoji: "💫",
    timescale: "3 billion years",
    description: "Billions of stars orbit common center. Galaxies self-organize.",
    stats: [
      { label: "Scale", value: "10²¹ m (kiloparsec)" },
      { label: "Components", value: "Billions of stars" },
      { label: "Largest structure", value: "Galaxy" }
    ],
    physics: "dℹ/dt = -∇Φ(gravitational N-body)",
    keyInsight: "Orbital mechanics. All stars follow same evolution law.",
    explore: "/cosmic-unfolding/#8-galaxies-form"
  },
  {
    id: 9,
    title: "Chemistry",
    emoji: "⚗️",
    timescale: "8 billion years",
    description: "Stars die and enrich space with heavy elements. Molecules form.",
    stats: [
      { label: "Scale", value: "10⁻⁹ m (molecular)" },
      { label: "Elements", value: "Up to Iron (and beyond)" },
      { label: "Key emergence", value: "Chemical bonds" }
    ],
    physics: "dℹ/dt = -∇Φ(chemical bonding)",
    keyInsight: "Complex molecules. Building blocks for life appear.",
    explore: "/cosmic-unfolding/#9-chemistry"
  },
  {
    id: 10,
    title: "Life",
    emoji: "🧬",
    timescale: "13 billion years (now)",
    description: "Molecules self-organize. DNA, proteins, cells emerge.",
    stats: [
      { label: "Scale", value: "10⁻⁶ m (cellular)" },
      { label: "Temperature", value: "310 K (body temp)" },
      { label: "Complexity", value: "Extraordinary" }
    ],
    physics: "dℹ/dt = -∇Φ(biochemical)",
    keyInsight: "Self-replication. Systems that sustain themselves persist.",
    explore: "/cosmic-unfolding/#10-life"
  },
  {
    id: 11,
    title: "Consciousness",
    emoji: "🧠",
    timescale: "Now",
    description: "Brains process information. Awareness emerges.",
    stats: [
      { label: "Scale", value: "10⁻⁶ to 10⁻¹ m" },
      { label: "Key emergence", value: "Awareness" },
      { label: "Level", value: "Meta-conscious" }
    ],
    physics: "dℹ/dt = -∇Φ(cognitive)",
    keyInsight: "Systems become aware of their own gradients.",
    explore: "/cosmic-unfolding/#11-consciousness"
  },
  {
    id: 12,
    title: "Intentional Design",
    emoji: "🌟",
    timescale: "Future (now onwards)",
    description: "Humans consciously design potentials. Civilization emerges.",
    stats: [
      { label: "Scale", value: "10⁰ to 10⁷ m" },
      { label: "New capability", value: "Design Φ" },
      { label: "Future", value: "Open" }
    ],
    physics: "dℹ/dt = -∇Φ(intentional)",
    keyInsight: "First time a system designs its own potential landscape.",
    explore: "/cosmic-unfolding/#12-civilization"
  }
];

let currentStage = 0;

function showStage(index) {
  currentStage = index;
  const stage = stages[index];
  
  let html = `
    <div class="stage-detail active">
      <h2>${stage.emoji} ${stage.title}</h2>
      <p style="font-size: 1.05rem; color: #555;">${stage.description}</p>
      
      <div class="stage-stats">
  `;
  
  stage.stats.forEach(stat => {
    html += `
      <div class="stat-box">
        <div class="stat-label">${stat.label}</div>
        <div class="stat-value">${stat.value}</div>
      </div>
    `;
  });
  
  html += `
      </div>
      
      <div class="stage-physics">
        <strong>Evolution equation:</strong> ${stage.physics}
      </div>
      
      <div class="stage-key-insight">
        <strong>Key insight:</strong> ${stage.keyInsight}
      </div>
      
      <div class="nav-buttons">
        <button class="nav-btn" onclick="showStage(${index - 1})" ${index === 0 ? 'disabled' : ''}>← Previous</button>
        <span style="flex: 1;"></span>
        <button class="nav-btn" onclick="showStage(${index + 1})" ${index === stages.length - 1 ? 'disabled' : ''}>Next →</button>
      </div>
      
      <a href="${stage.explore}" class="explore-link">Explore This Stage in Detail →</a>
    </div>
  `;
  
  document.getElementById('stage-content').innerHTML = html;
  
  // Scroll to show stage
  document.querySelector('.timeline-stage').parentElement.scrollLeft = (index * 150) - 100;
}

// Show first stage on load
window.addEventListener('load', () => showStage(0));
</script>

---

## How to Use This Navigator

1. **Click any stage** on the timeline above to see details
2. **Use Previous/Next buttons** to step through one stage at a time
3. **Click "Explore This Stage"** to read the full chapter in The Great Unfolding
4. **Scroll left/right** on the timeline to see all stages

---

## The Core Message

Every stage follows **one universal law**:
$$\frac{d\mathbf{i}}{dt} = -\nabla\Phi(\mathbf{x}, t)$$

Different potentials $\Phi$. Different scales. Different contexts.

**Same law.**

This is the heartbeat of reality.

---

**→ Read the full narrative**: [The Great Unfolding]({{ site.baseurl }}/cosmic-unfolding/)
