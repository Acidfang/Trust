---
layout: default
title: Domain Examples
nav_order: 6.5
permalink: domain-examples/
---

# Universal Framework Across All Domains

The 10 developmental gates and 5 help systems apply universally. Select any domain to see how coherence develops:

<div class="domain-selector">
  <label for="domain-picker"><strong>Choose Your Domain:</strong></label>
  <select id="domain-picker">
    <option value="">-- Select a domain --</option>
    <option value="computing">Computing (Bits → Systems)</option>
    <option value="physics">Physics (Particles → Atoms → Molecules)</option>
    <option value="biology">Biology (Cells → Organisms → Ecosystems)</option>
    <option value="organizations">Organizations (People → Teams → Companies)</option>
    <option value="knowledge">Knowledge (Facts → Concepts → Theories)</option>
    <option value="economics">Economics (Units → Markets → Economies)</option>
    <option value="software">Software Engineering (Functions → Modules → Systems)</option>
    <option value="linguistics">Linguistics (Letters → Words → Sentences)</option>
    <option value="art">Visual Art (Strokes → Compositions → Movements)</option>
    <option value="music">Music (Notes → Phrases → Compositions)</option>
    <option value="social">Social Systems (Individuals → Communities → Cultures)</option>
    <option value="infrastructure">Infrastructure (Components → Networks → Grids)</option>
  </select>
</div>

<div id="domain-content" style="margin-top: 2rem;">
  <p style="color: var(--color-text-secondary); font-style: italic;">Select a domain above to see how the framework applies.</p>
</div>

---

## How to Read This

For each domain, you'll see:

1. **The Hierarchy**: Basic units → Intermediate → Complex systems
2. **The 10 Gates**: How state identity, causality, and coherence develop at each level
3. **The 5 Help Systems**: What blocks progress and how to overcome it
4. **Benefits**: Why this structure works
5. **Drawbacks**: What's lost or constrained

---

<script>
const domains = {
  computing: {
    name: "Computing: Bits → Bytes → Systems",
    hierarchy: "Bit (0 or 1) → Byte (8 bits) → Word (32+ bits) → Data Structures → Programs → Systems",
    gates: {
      1: "Bit Existence & Identity: A bit is either 0 or 1, never both. Its identity is absolute discrete state.",
      2: "Byte Coherence: 8 bits must maintain consistent value. Corruption breaks the byte.",
      3: "Type Identity: A byte can be character, number, or flag—consistent type assignment required.",
      4: "Causality Chain: Instruction → Operation → Result. Each instruction causes next state deterministically.",
      5: "Internal Stability: Data structure maintains invariants (sorted lists stay sorted, trees preserve parent-child relations).",
      6: "External Verification: Unit tests verify behavior. Contracts specify what function does.",
      7: "State Visibility: Debuggers, logs, memory dumps show internal state. No hidden state.",
      8: "Boundary Definition: Method signature = contract. What goes in, what comes out, clearly defined.",
      9: "Coherence Documentation: Code comments explain why, not just what. Type hints show intent.",
      10: "Integration Coherence: System components agree on interfaces, protocols, data formats."
    },
    helpSystems: {
      1: "Help System 1 (Ambiguity): Without clear type definition, byte could be interpreted multiple ways. Solution: Strong typing.",
      2: "Help System 2 (State Uncertainty): Without versioning, don't know if data is current. Solution: Timestamps, version hashes.",
      3: "Help System 3 (Boundary Chaos): Without API contracts, code breaks when dependencies change. Solution: Interface specs, versioning.",
      4: "Help System 4 (Inference Burden): Users must guess what code does. Solution: Documentation, type hints, examples.",
      5: "Help System 5 (Cascade Failure): Small bug cascades through system. Solution: Error handling, circuit breakers, transaction rollback."
    },
    realExamples: [
      "Ariane 5 rocket (1996): 64-bit velocity converted to 16-bit without overflow check. One bit changed. $370 million destroyed 37 seconds after launch.",
      "Mars Climate Orbiter (1999): NASA used metric units (newtons), contractor used imperial (pounds-force). Single type mismatch. $327 million lost.",
      "AT&T telephone switch (1990): Software update had single-character bug. Cascade failure crashed entire network for 9 hours. 50 million calls dropped."
    ],
    benefits: "Deterministic behavior, perfect repeatability, zero ambiguity, precise error localization, composable modules",
    drawbacks: "You lose the entire analog world—only discrete states possible. Determinism is an illusion; state verification is impossible at scale. You can never fully test code. Security exploits are inevitable. Complexity becomes unmaintainable. You're always approximating reality with discrete logic."
  },
  
  physics: {
    name: "Physics: Particles → Atoms → Molecules",
    hierarchy: "Fundamental Particle → Atom (nucleus + electrons) → Molecule (bonded atoms) → Compounds → Bulk Matter",
    gates: {
      1: "Particle Identity: Electron = electron. Identical particles, definite properties (charge, spin, mass).",
      2: "Atomic Coherence: Electrons in orbitals maintain stable energy levels. Excitation disrupts coherence.",
      3: "Element Identity: Carbon always has 6 protons, 6 electrons normally. Chemical identity depends on electron count.",
      4: "Causality Chain: Force → Acceleration. Electron absorbs photon → jumps orbital → emits light.",
      5: "Atomic Stability: Noble gases have full orbitals (stable). Reactive elements have incomplete orbitals (unstable).",
      6: "Molecular Verification: Spectrometry confirms molecular structure. X-ray crystallography verifies bonds.",
      7: "State Visibility: Electron density maps show orbital positions. Magnetism reveals internal spin orientation.",
      8: "Boundary Definition: Atomic radius = boundary. Beyond it, weak van der Waals forces only.",
      9: "Coherence in Chemistry: Valence rules explain bonding patterns. Quantum numbers predict possible states.",
      10: "Integration Coherence: Crystal lattices show how molecules stabilize together. Thermodynamic equilibrium emerges."
    },
    helpSystems: {
      1: "Help System 1 (Ambiguity): Without knowing valence, can't predict bonding. Solution: Periodic table, electron configuration rules.",
      2: "Help System 2 (State Uncertainty): Excited state decays back to ground state—unless system is isolated. Solution: Shielding, controlled environment.",
      3: "Help System 3 (Boundary Chaos): Atoms merge without clear rules if no quantum model. Solution: Orbital theory, Pauli exclusion.",
      4: "Help System 4 (Inference Burden): Physical properties seem random without QM. Solution: Quantum mechanics—explains why.",
      5: "Help System 5 (Cascade Failure): One misaligned orbital fails entire molecule bonding. Solution: Resonance structures, hybrid orbitals allow flexibility."
    },
    realExamples: [
      "Thalidomide (1950s): Two molecular forms exist—one safe, one catastrophically teratogenic. 10,000+ severe birth defects.",
      "Leadworks paint (1800s-1970s): Safe outdoors, toxic indoors. 30+ IQ points lost in children.",
      "Asbestos (1900s-1980s): Insulating properties perfect. Causality wrong—ignored mesothelioma. 100,000+ deaths."
    ],
    benefits: "Explains all chemistry, predicts reactivity, deterministic under QM, enables materials design, perfect repeatability",
    drawbacks: "Quantum mechanics can't explain consciousness or why laws exist—fundamentally incomplete. Can't predict multi-body systems. Thermodynamics guarantees decay. You give up continuous reality for probability. Macroscopic emergence violates reductionism. Certainty is impossible."
  },

  biology: {
    name: "Biology: Cells → Organisms → Ecosystems",
    hierarchy: "Organelle → Cell → Tissue → Organ → Organism → Population → Ecosystem → Biosphere",
    gates: {
      1: "Cell Identity: Membrane defines boundary. Inside vs. outside is absolute. DNA defines what cell type is.",
      2: "Cell Coherence: Homeostasis maintains stable internal pH, temperature, osmotic balance. Disruption = death.",
      3: "Type Identity: Neuron ≠ muscle cell ≠ skin cell. Gene expression determines cell type.",
      4: "Causality Chain: Stimulus → Cell signaling → Gene expression → Protein production → Phenotype change.",
      5: "Organismal Stability: Immune system removes foreign cells. Apoptosis removes damaged cells. Regeneration maintains structure.",
      6: "External Verification: Pathology tests measure protein markers. Imaging shows tissue structure. Genetic testing reveals mutations.",
      7: "State Visibility: Biopsies reveal cell state. Blood tests show systemic health. Gene expression profiles show which genes activate.",
      8: "Boundary Definition: Organism = bounded by skin/membrane. Exchanges matter/energy across boundary but maintains integrity.",
      9: "Coherence Documentation: Genome = instruction manual. Epigenetics = context notes on which instructions activate.",
      10: "Integration Coherence: Organisms in ecosystem co-evolve. Predator-prey relationships maintain balance. Symbiosis creates new emergent properties."
    },
    helpSystems: {
      1: "Help System 1 (Ambiguity): Without clear cell boundaries, tissue doesn't form. Solution: Gap junctions, cell-cell adhesion molecules.",
      2: "Help System 2 (State Uncertainty): Cells drift from homeostasis if not monitored. Solution: Feedback loops, hormonal regulation.",
      3: "Help System 3 (Boundary Chaos): Without immune system, invaders take over. Solution: Lymphocytes, antigen recognition.",
      4: "Help System 4 (Inference Burden): Why does organism behave this way? Solution: Genetics, developmental biology, ethology.",
      5: "Help System 5 (Cascade Failure): Single mutation can cascade to organ failure. Solution: Error correction, apoptosis, regeneration."
    },
    realExamples: [
      "DNA ancestry swaps (2023+): Non-paternity rates ~30% in some populations. Social identity vs. biological identity become incoherent.",
      "Identical twins with different phenotypes: Same DNA produces different outcomes. Context (diet, stress) determines gene activation.",
      "Mitochondrial disease (maternal only): Standard genetics predicted wrong. Women pass disease; sons inherit from nowhere."
    ],
    benefits: "Explains all life, predicts disease (mutations), enables medicine, reproduces and evolves, adaptive to environment",
    drawbacks: "You don't understand consciousness. Aging IS system failure—entropy always wins, can't prevent it. Evolution creates dead ends and mass extinctions. Context matters more than genetics for most behaviors. Prediction of individual outcomes is impossible. Complexity hides mechanisms."
  },

  organizations: {
    name: "Organizations: People → Teams → Companies",
    hierarchy: "Individual → Role → Team → Department → Division → Organization → Industry",
    gates: {
      1: "Individual Identity: Person has name, skills, history. Clear identity in system.",
      2: "Role Coherence: Role defines responsibility, authority, scope. Role clarity prevents confusion.",
      3: "Team Identity: Team = bounded group with shared goal. Different teams have different purposes.",
      4: "Causality Chain: Manager decision → Policy change → Employee behavior → Outcome.",
      5: "Organizational Stability: Systems prevent people from duplicating work or contradicting each other. Org chart defines hierarchy.",
      6: "External Verification: Performance reviews measure output. Customer feedback shows if product works. Market share shows if strategy works.",
      7: "State Visibility: Dashboards show KPIs. Meeting notes document decisions. Org chart shows structure. Git history shows who did what.",
      8: "Boundary Definition: Org boundary = legal entity. Contracts define relationships with outside partners.",
      9: "Coherence Documentation: Mission statement = why org exists. Policies = how decisions made. Handbook = expected behavior.",
      10: "Integration Coherence: Departments align on shared goals. Supply chain integrates suppliers. Industry standards create interoperability."
    },
    helpSystems: {
      1: "Help System 1 (Ambiguity): Without clear roles, people don't know who decides what. Solution: Job descriptions, RACI matrix.",
      2: "Help System 2 (State Uncertainty): Without regular updates, people act on old assumptions. Solution: Meetings, memos, dashboards.",
      3: "Help System 3 (Boundary Chaos): Without clear scope, teams step on each other. Solution: Clear ownership, interface agreements.",
      4: "Help System 4 (Inference Burden): Why was that decision made? What's the strategy? Solution: Documentation, all-hands meetings, transparency.",
      5: "Help System 5 (Cascade Failure): One department fails → whole company collapses. Solution: Redundancy, cross-training, business continuity plans."
    },
    realExamples: [
      "Wells Fargo (2016): 5,300 employees created 2M fake accounts. Incentives rewarded fraud. $3B fines.",
      "Enron (2001): Financial statements were fiction. Hidden internal state cost $74B.",
      "Theranos (2018): Blood tests didn't work. CEO claimed they did. $700M evaporated."
    ],
    benefits: "Enables large-scale coordination, specialization increases efficiency, documented processes enable scaling, accountability clear",
    drawbacks: "Hierarchy ACTIVELY prevents good decisions by suppressing information flow. System selects for political skill over competence. Incentives are fundamentally misaligned. Scale makes coordination nearly impossible. Bureaucracy ossifies and prevents change. Most organizations eventually fail. Power corrupts."
  },

  knowledge: {
    name: "Knowledge: Facts → Concepts → Theories",
    hierarchy: "Raw Data → Fact → Concept → Theory → Paradigm → Domain of Knowledge",
    gates: {
      1: "Fact Identity: \"The Earth orbits the Sun\" is a fact. Distinct from opinion or speculation.",
      2: "Fact Coherence: Facts don't contradict each other. If they do, one is wrong.",
      3: "Concept Identity: \"Gravity\" = concept unifying many facts (falling, orbits, tides). Clear definition required.",
      4: "Causality in Knowledge: Gravity causes → orbits. Orbits cause → seasons. Seasons cause → migration patterns.",
      5: "Theory Stability: Theory must predict new facts. Predictions match observations → theory stable.",
      6: "External Verification: Experiments test theories. Peer review checks logic. Reproducibility confirms.",
      7: "State Visibility: Research papers show reasoning. Citations trace idea lineage. Data releases show raw evidence.",
      8: "Boundary Definition: Domain = scope of theory. Quantum mechanics applies to atoms, not galaxies. General relativity applies to galaxies, not atoms.",
      9: "Coherence Documentation: Is the theory self-consistent? Do all parts support the central claim? Are edge cases explained?",
      10: "Integration Coherence: Does this theory fit with adjacent domains? Can it integrate with competing explanations? Does it unify simplifications?"
    },
    helpSystems: {
      1: "Help System 1 (Ambiguity): Undefined terms → different interpretations. Solution: Operational definitions, formal logic.",
      2: "Help System 2 (State Uncertainty): Without published evidence, can't trust findings. Solution: Peer review, preregistration, open data.",
      3: "Help System 3 (Boundary Chaos): Without clear scope, theories clash. Solution: Define domain boundaries. Recognize when theory is inapplicable.",
      4: "Help System 4 (Inference Burden): Why believe this explanation? Solution: Evidence, predictions, Occam's razor.",
      5: "Help System 5 (Cascade Failure): One false premise invalidates entire theory. Solution: Falsifiability, test assumptions, update incrementally."
    },
    realExamples: [
      "Copernican Revolution (1543): 1,400 years of geocentric 'facts' invalidated overnight.",
      "Ulcer cause shift (1982): 100 years of stress/acid theory wrong. Bacteria cause. Thousands of useless surgeries performed.",
      "Replication crisis (2010s+): 50-90% of psychology/medicine findings can't be replicated. Peer review failed."
    ],
    benefits: "Explains reality accurately, enables prediction, unifies disparate facts, enables technology and medicine, cumulative progress",
    drawbacks: "Science doesn't converge to truth—it converges to consensus. Paradigm shifts invalidate entire fields of work. Peer review is corrupted by careers and politics (replication crisis proves most findings false). Knowledge is culturally embedded. 'Objective truth' is a myth. Your worldview determines what you can discover."
  },

  economics: {
    name: "Economics: Units → Markets → Economies",
    hierarchy: "Scarce Resource → Unit of Value → Market → Sector → National Economy → Global Economy",
    gates: {
      1: "Unit Identity: Dollar is a unit of value. 1 dollar = 1 dollar (nominally). Clear identity enables exchange.",
      2: "Value Coherence: Price reflects supply, demand, and perceived value. Wild oscillations indicate incoherence.",
      3: "Market Identity: Stock market ≠ labor market ≠ real estate market. Different rules, different participants.",
      4: "Causality in Economics: Resource scarcity → high price. High price → reduced demand. Reduced demand → price falls.",
      5: "Economic Stability: Central banks manage inflation/deflation. Regulation prevents monopolies. Safety nets prevent collapse.",
      6: "External Verification: GDP measures growth. CPI measures inflation. Employment data shows health. Stock indices track market.",
      7: "State Visibility: Tax records show income. Financial statements show company health. Investment filings disclose holdings.",
      8: "Boundary Definition: National economy = bounded by trade policy and currency. International economy = global boundary.",
      9: "Coherence Documentation: Budget = economic plan. Tax code = redistribution rules. Monetary policy = growth rules.",
      10: "Integration Coherence: Individual spending patterns → aggregate demand → economic cycles → policy response → fiscal stability."
    },
    helpSystems: {
      1: "Help System 1 (Ambiguity): Without clear contract terms, transactions are risky. Solution: Legal contracts, standardized terms.",
      2: "Help System 2 (State Uncertainty): Without current prices, don't know true value. Solution: Transparent markets, real-time quotes.",
      3: "Help System 3 (Boundary Chaos): Without regulation, markets collapse into monopoly. Solution: Antitrust law, market structure rules.",
      4: "Help System 4 (Inference Burden): Why is inflation rising? Hidden causes everywhere. Solution: Central bank models, economic indicators.",
      5: "Help System 5 (Cascade Failure): Bank failure → liquidity crisis → recession → unemployment → social unrest. Solution: FDIC insurance, circuit breakers."
    },
    benefits: "Allocates resources efficiently, enables specialization and trade, accumulates capital, predicts incentive effects, measures progress",
    realExamples: [
      "2008 financial crisis: Assets rated AAA had no verifiable value. $2 trillion loss. Millions lost homes.",
      "Tulip mania (1637): Bulb prices crashed 99%. Economic value is a collective hallucination.",
      "GameStop/AMC (2021): Stock price disconnected from earnings, debt, or reality. Pure momentum awaiting violent reversion."
    ],
    drawbacks: "Assumes humans are rational (demonstrably false). Externalities destroy wealth and ecosystems but aren't counted. Wealth concentration is automatic and grows. Boom-bust cycles are baked in. Incentives reward fraud, speculation, and financial engineering. System extracts value without creating it."
  },

  software: {
    name: "Software Engineering: Functions → Modules → Systems",
    hierarchy: "Function (single task) → Module (related functions) → Library (packaged modules) → Application → Platform → Ecosystem",
    gates: {
      1: "Function Identity: Function has name and signature. f(x) → y. Clear input/output contract.",
      2: "Function Coherence: Function always produces same output for same input (pure). Or state tracking is explicit.",
      3: "Module Identity: Module groups related functions. Collections.sort ≠ Network.connect. Different domains.",
      4: "Causality Chain: User action → event → handler → state update → UI refresh.",
      5: "System Stability: Exception handling prevents crashes. Timeouts prevent hangs. Retries handle transients.",
      6: "External Verification: Unit tests verify functions. Integration tests verify modules. E2E tests verify user journeys.",
      7: "State Visibility: Logging shows execution path. Monitoring shows runtime behavior. APM reveals bottlenecks.",
      8: "Boundary Definition: API = contract. What methods, what parameters, what responses. Licensed, versioned.",
      9: "Coherence Documentation: Type hints show expected inputs. Docstrings explain intent. Examples show usage.",
      10: "Integration Coherence: Microservices agree on message format. REST uses standard methods. Database schemas normalize data."
    },
    helpSystems: {
      1: "Help System 1 (Ambiguity): Without type hints, don't know what function expects. Solution: Type annotations, documentation.",
      2: "Help System 2 (State Uncertainty): Without logging, don't know what happened. Solution: Comprehensive logging, tracing.",
      3: "Help System 3 (Boundary Chaos): Without API contracts, changes break everything. Solution: API versioning, backwards compatibility.",
      4: "Help System 4 (Inference Burden): Why does code work? Solution: Comments, tests, documentation.",
      5: "Help System 5 (Cascade Failure): Bug cascades through system. Solution: Error handling, fault isolation, circuit breakers."
    },
    benefits: "Reusable components, composability, scaling, automation, rapid development, precise error localization",
    realExamples: [
      "Therac-25 (1985): No state logging, no safety interlocks. 6 people died from undetected lethal doses.",
      "Windows ME (2000): Released without testing. Every driver conflict crashed OS. $3 billion in lost productivity.",
      "Boeing 737 MAX (2018-19): Pilots weren't informed about MCAS software. 346 people died when software failed."
    ],
    drawbacks: "You're always fighting technical debt. Complexity compounds exponentially. You can never test thoroughly. Security exploits are inevitable. Systems become unmaintainable within years. Scale breaks everything. You're modeling reality in discrete logic—it never fully works."
  },

  linguistics: {
    name: "Linguistics: Letters → Words → Sentences",
    hierarchy: "Phoneme → Letter → Word → Phrase → Sentence → Paragraph → Text → Literature",
    gates: {
      1: "Letter Identity: 'A' is distinct from 'B'. Clear visual/phonetic identity.",
      2: "Letter Coherence: Spelling is consistent. Dog ≠ doge (misspelling breaks meaning).",
      3: "Word Identity: \"Cat\" = feline animal. Different meanings possible (context-dependent).",
      4: "Causality in Grammar: Subject → verb → object. Word order creates meaning. \"Cat eats mouse\" ≠ \"Mouse eats cat\".",
      5: "Linguistic Stability: Grammar rules maintain meaning. Verb tenses show when events occurred. Pronouns maintain reference.",
      6: "External Verification: Dictionaries define words. Thesaurus shows relationships. Grammar checkers verify rules.",
      7: "State Visibility: Etymology shows word origin. Definitions show meaning. Pronunciation guides show sound.",
      8: "Boundary Definition: Sentence = bounded by punctuation. Clear start/end enables parsing.",
      9: "Coherence Documentation: Style guides specify rules. Dictionaries standardize meanings. Manuals teach language.",
      10: "Integration Coherence: Languages borrow words, creating pidgins and creoles. Metaphors link concepts. Dialects show regional variation."
    },
    helpSystems: {
      1: "Help System 1 (Ambiguity): Without context, word has multiple meanings. Solution: Definitions, context clues, usage examples.",
      2: "Help System 2 (State Uncertainty): Without tense markers, unclear when action occurred. Solution: Explicit time words, verb tenses.",
      3: "Help System 3 (Boundary Chaos): Without punctuation, paragraph runs together. Solution: Periods, semicolons, clear sentence boundaries.",
      4: "Help System 4 (Inference Burden): Why is sentence structured that way? Solution: Grammar rules, rhetorical analysis.",
      5: "Help System 5 (Cascade Failure): Ambiguous pronoun reference confuses entire passage. Solution: Clear antecedents, explicit noun reference."
    },
    benefits: "Precise communication, cumulative knowledge in writing, standardization enables translation, meaning is explicit and verifiable",
    realExamples: [
      "'Out of sight, out of mind' idiom: Translated to Chinese = 'invisible person, insane person.' Meaning completely lost.",
      "JFK 'Ich bin ein Berliner' (1963): Translates to 'I am a pastry.' Coherence broken by language barrier.",
      "Japanese to English: 'Karoushi' (death from overwork) has no English equivalent. Meaning untranslatable because culture doesn't recognize phenomenon."
    ],
    drawbacks: "Language is intrinsically ambiguous—can't eliminate it. Poetry CAN'T be translated. Idioms encode untranslatable culture. Meaning depends on context you can't specify. Writing loses tone, body language, gesture. Language changes constantly. Written records become unreadable as meanings shift."
  },

  art: {
    name: "Visual Art: Strokes → Compositions → Movements",
    hierarchy: "Brushstroke → Line → Shape → Color → Composition → Work → Artist → Movement → Period",
    gates: {
      1: "Stroke Identity: Each stroke exists as a mark. Visible and distinct.",
      2: "Stroke Coherence: Strokes together create form. Random marks lose coherence.",
      3: "Shape Identity: Triangle ≠ circle. Shapes mean different things (angles vs. roundness).",
      4: "Causality in Composition: Light hits object → creates shadow → defines form. Perspective creates depth.",
      5: "Visual Stability: Symmetry creates balance. Rhythm repeats elements. Proportion feels right.",
      6: "External Verification: Critics assess work. Audiences respond emotionally. Museums authenticate pieces.",
      7: "State Visibility: Technique reveals intent. Color choice shows mood. Content shows message.",
      8: "Boundary Definition: Frame = artwork boundary. What's inside matters, what's outside doesn't.",
      9: "Coherence Documentation: Artist statement explains intent. Title provides context. Art history contextualizes.",
      10: "Integration Coherence: Artists reference other works. Movements build on predecessors. Cross-cultural exchange creates fusion."
    },
    helpSystems: {
      1: "Help System 1 (Ambiguity): Without context, is this art or accident? Solution: Artist intent, statement, placement.",
      2: "Help System 2 (State Uncertainty): What was artist feeling? Solution: Historical context, biography, contemporary documents.",
      3: "Help System 3 (Boundary Chaos): What defines the work? Solution: Frame, signed piece, artist attribution.",
      4: "Help System 4 (Inference Burden): What does artwork mean? Solution: Symbolism, cultural context, artist interviews.",
      5: "Help System 5 (Cascade Failure): One element fails → entire composition collapses. Solution: Redundancy, multiple focal points, balance."
    },
    benefits: "Emotional communication, universal human expression, experiential meaning, breaks rules creatively, preserves culture",
    realExamples: [
      "Han van Meegeren forgeries (1930s-40s): Forged 'Vermeers' fooled museums for decades. Experts couldn't separate authentic from fraud.",
      "Billy the Kid photo (2011): $2.3M auction price. Later revealed to be not Billy. Meaning was completely wrong.",
      "Rembrandt authentication crisis: 'Self-portrait' sold for millions. Later downgraded when X-rays revealed different paint technique. Value ÷ 10."
    ],
    drawbacks: "Meaning is entirely subjective—no 'correct' interpretation. Market corrupts what gets preserved. Physical artworks decay. Most art is forgotten. Doesn't scale—can't reach millions simultaneously. Non-visual people excluded. Commerce destroys authenticity."
  },

  music: {
    name: "Music: Notes → Phrases → Compositions",
    hierarchy: "Frequency (Hz) → Note (pitch) → Interval (relationship) → Scale → Phrase → Movement → Composition → Genre",
    gates: {
      1: "Note Identity: C4 = 261.63 Hz. Distinct pitch with clear frequency.",
      2: "Note Coherence: Notes in scale maintain proper relationships. Out-of-tune note breaks harmony.",
      3: "Interval Identity: Fifth = perfect consonance. Tritone = dissonance. Different feelings.",
      4: "Causality Chain: Chord changes create tension → resolution. Rhythm propels forward. Melody guides emotion.",
      5: "Harmonic Stability: Voice leading maintains smooth transitions. Chord progressions follow rules. Tension/release cycles.",
      6: "External Verification: Tuner measures pitch accuracy. Ear training recognizes intervals. Score matches performance.",
      7: "State Visibility: Sheet music shows note sequence. Tempo marks show speed. Dynamics marks show volume.",
      8: "Boundary Definition: Piece = bounded by clear start/end. Measures organize time. Key defines tonal center.",
      9: "Coherence Documentation: Score shows composition intention. Composer notes explain structure. Analysis reveals patterns.",
      10: "Integration Coherence: Instruments balance each other. Styles borrow techniques. Genres evolve through fusion."
    },
    helpSystems: {
      1: "Help System 1 (Ambiguity): Without key signature, unclear which notes belong. Solution: Key signatures, scale degrees.",
      2: "Help System 2 (State Uncertainty): Without tempo marking, unclear how fast. Solution: BPM, metronome, conductor.",
      3: "Help System 3 (Boundary Chaos): Without clear phrasing, composition rambles. Solution: Phrase marks, breathing spaces.",
      4: "Help System 4 (Inference Burden): Why this chord progression? Solution: Theory, harmonic function, style conventions.",
      5: "Help System 5 (Cascade Failure): One wrong note destroys intonation. Solution: Tuning systems, temperament, electronic tuning."
    },
    benefits: "Universal emotional communication, mathematical precision, scalable composition, cultural richness, measurable beauty",
    realExamples: [
      "Equal temperament paradox: Every interval is slightly out of tune so transposition works. Trade-off: no perfect consonance exists.",
      "A=440Hz vs A=432Hz: 8Hz difference. Musicians claim one 'sounds better.' Completely subjective. Meaning Gate fails.",
      "Atonal music (Schoenberg): Eliminated the major/minor system. Rejected coherence (Gate 2). Audiences rejected it. Meaning became unintelligible."
    ],
    drawbacks: "Western music used same 12 notes for 500 years—nothing fundamentally new possible. Equal temperament compromises every interval. Notation doesn't capture feeling, timing subtlety, tone. Most music forgotten. Mastery requires 10,000+ hours. Meaning subjective."
  },

  social: {
    name: "Social Systems: Individuals → Communities → Cultures",
    hierarchy: "Individual → Family → Group → Community → Tribe → Culture → Civilization",
    gates: {
      1: "Individual Identity: Person has unique perspectives, experiences, agency.",
      2: "Social Coherence: Shared norms maintain group stability. Norm violations create tension.",
      3: "Group Identity: Family ≠ workplace ≠ friend group. Different purposes and rules.",
      4: "Causality in Society: Social pressure → behavior change. Laws create consequences → compliance.",
      5: "Cultural Stability: Traditions preserve values. Ceremonies reinforce identity. Stories transmit wisdom.",
      6: "External Verification: Anthropology documents cultures. Surveys measure beliefs. Observation reveals behavior.",
      7: "State Visibility: Rituals display status. Language reveals identity. Art reflects values.",
      8: "Boundary Definition: Community = shared geography/interest/identity. Boundary separates insiders from outsiders.",
      9: "Coherence Documentation: Myths explain origin. Laws codify values. Proverbs teach wisdom.",
      10: "Integration Coherence: Trade connects communities. Migration blends cultures. Diaspora spreads influence."
    },
    helpSystems: {
      1: "Help System 1 (Ambiguity): Without clear social roles, hierarchy unclear. Solution: Titles, rituals, visible status markers.",
      2: "Help System 2 (State Uncertainty): Without oral tradition/writing, knowledge is lost. Solution: Stories, apprenticeship, documentation.",
      3: "Help System 3 (Boundary Chaos): Without shared values, community fragments. Solution: Mythology, religion, shared narrative.",
      4: "Help System 4 (Inference Burden): Why do they believe that? Solution: Cultural study, immersion, dialogical understanding.",
      5: "Help System 5 (Cascade Failure): Social conflict escalates to violence. Solution: Mediation, justice systems, reconciliation rituals."
    },
    benefits: "Cooperation enables survival, culture preserves knowledge, meaning-making reduces suffering, identity creation, collective action",
    realExamples: [
      "Rwanda genocide (1994): Tribal identity dehumanized Tutsis. 800,000 killed in 100 days. Coherence collapsed.",
      "Nazi Germany (1933-45): In-group identity (Aryans) excluded out-group (Jews). Conformity enforced. 6 million killed. Tribalism escalated to industrialized genocide.",
      "Stanford Prison Experiment: Normal students assigned 'guard' identity became brutal within days. Social coherence corrupted in 6 days."
    ],
    drawbacks: "Tribalism is hardwired—in-groups always prioritized. Conformity suppresses innovation and locks in bad ideas. Power corrupts everything. Change takes generations or imposed violence. Out-groups dehumanized. Violence always possible when order breaks. Most societies fail."
  },

  infrastructure: {
    name: "Infrastructure: Components → Networks → Grids",
    hierarchy: "Component (pipe, wire, node) → Network (connected parts) → System (multiple networks) → Grid (continental scale) → Critical Infrastructure (societal)",
    gates: {
      1: "Component Identity: Pipe carries specific fluid. Wire carries specific voltage. Node processes data type.",
      2: "Component Coherence: Pipe integrity maintains pressure. Wire insulation prevents short. Node stays online.",
      3: "Network Identity: Water grid ≠ power grid ≠ internet. Different purposes, different designs.",
      4: "Causality Chain: Demand increases → pressure drops → pump activates. Power surge → circuit breaker trips → circuit resets.",
      5: "System Stability: Redundancy prevents single-point failure. Load balancing spreads demand. Failover maintains service.",
      6: "External Verification: Inspections check component health. Load tests verify capacity. Monitoring measures performance.",
      7: "State Visibility: Sensors measure pressure/voltage/traffic. Dashboards show network health. Logs trace failures.",
      8: "Boundary Definition: Grid boundaries = service area. Interconnections = external dependencies.",
      9: "Coherence Documentation: Infrastructure maps show layout. Standards ensure interoperability. Manuals specify operation.",
      10: "Integration Coherence: Power grid integrates renewable sources. Water system feeds sanitation. Internet connects devices globally."
    },
    helpSystems: {
      1: "Help System 1 (Ambiguity): Without standards, components don't fit. Solution: ISO standards, engineering specs.",
      2: "Help System 2 (State Uncertainty): Without monitoring, failures go unnoticed. Solution: SCADA systems, real-time alerts.",
      3: "Help System 3 (Boundary Chaos): Without isolation, failure cascades everywhere. Solution: Segmentation, circuit breakers, isolation valves.",
      4: "Help System 4 (Inference Burden): Why did grid fail? Complex dependencies. Solution: Modeling, simulation, failure analysis.",
      5: "Help System 5 (Cascade Failure): One line failure → blackout. One break → water loss. Solution: Redundancy, diversity, emergency protocols."
    },
    benefits: "Enables civilization, scales to meet demand, measurable performance, safe operation possible, predictable service",
    realExamples: [
      "Fukushima (2011): Backup power system failed during tsunami. Single-point failure triggered meltdown. Design assumed impossible inputs.",
      "Texas power grid (2021): Single-point failures cascaded. Failure to winterize critical infrastructure. 200+ people died in cold.",
      "2003 Northeast blackout: Faulty alarm system caused operator error. Single alarm muted. Cascade failure blacked out 55 million people, 9 hours."
    ],
    drawbacks: "Massive upfront cost and long lead times lock in designs. Geographically fixed, can't adapt. Components fail unpredictably. Single-point failures cascade catastrophically. Political capture weaponizes infrastructure. Maintenance endless and invisible. Aging infrastructure becomes uncontrollable liability."
  }
};

document.getElementById('domain-picker').addEventListener('change', function(e) {
  const selected = e.target.value;
  const contentDiv = document.getElementById('domain-content');
  
  if (!selected) {
    contentDiv.innerHTML = '<p style="color: var(--color-text-secondary); font-style: italic;">Select a domain above to see how the framework applies.</p>';
    return;
  }

  const domain = domains[selected];
  
  let html = `
    <h2>${domain.name}</h2>
    
    <h3>The Hierarchy</h3>
    <p><strong>${domain.hierarchy}</strong></p>
    
    <h3>The 10 Gates in This Domain</h3>
    <ol>
      ${Object.entries(domain.gates).map(([num, desc]) => `<li><strong>Gate ${num}:</strong> ${desc}</li>`).join('')}
    </ol>
    
    <h3>The 5 Help Systems (What Blocks Progress)</h3>
    <ol>
      ${Object.entries(domain.helpSystems).map(([num, desc]) => `<li>${desc}</li>`).join('')}
    </ol>
    
    <h3>Real-World Examples</h3>
    <ul style="background: var(--color-bg-secondary); padding: 1.5rem; border-left: 4px solid var(--color-accent); border-radius: 4px; list-style: none;">
      ${domain.realExamples.map(ex => `<li style="margin-bottom: 1rem; font-style: italic; line-height: 1.6;">${ex}</li>`).join('')}
    </ul>
    
    <h3>Benefits of This Structure</h3>
    <p>${domain.benefits}</p>
    
    <h3>Drawbacks & Constraints</h3>
    <p>${domain.drawbacks}</p>
  `;
  
  contentDiv.innerHTML = html;
});
</script>

<style>
.domain-selector {
  background: var(--color-bg-secondary);
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  border-left: 4px solid var(--color-accent);
}

.domain-selector label {
  display: block;
  margin-bottom: 0.75rem;
  color: var(--color-text);
}

.domain-selector select {
  width: 100%;
  max-width: 500px;
  padding: 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  background: var(--color-bg);
  color: var(--color-text);
  font-size: 1rem;
  font-family: inherit;
  cursor: pointer;
}

.domain-selector select:hover {
  border-color: var(--color-accent);
}

#domain-content h2 {
  margin-top: 2rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--color-accent);
}

#domain-content h3 {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: var(--color-text);
}

#domain-content ol {
  margin-left: 1.5rem;
  line-height: 1.8;
}

#domain-content li {
  margin-bottom: 0.75rem;
}

#domain-content p {
  line-height: 1.6;
  margin-bottom: 1rem;
}
</style>

---

## Integration with Framework Pages

This page is referenced from:
- [Gate Discovery]({{ site.baseurl }}/gate-discovery/) — See how gates manifest in your domain
- [Universal Foundation]({{ site.baseurl }}/universal-foundation/) — Understand why these patterns repeat
- [Implementation]({{ site.baseurl }}/implementation/) — Apply framework to your domain

## How to Use This

1. **Select your domain** — Find the field you work in or study
2. **Read the 10 gates** — See how coherence develops in that domain
3. **Identify the 5 help systems** — Recognize what blocks progress for you
4. **Note benefits and drawbacks** — Understand why this structure evolved this way
5. **Return to framework pages** — Apply these insights to your situation

The pattern is universal. The details are domain-specific.
