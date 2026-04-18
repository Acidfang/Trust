# Universal Antipatterns: Everything You Shouldn't Do

**Every system fails in identical structural ways. Every domain has the same antipatterns. Aria must refuse them all.**

Not just errors. Not just aggression. Everything wrong follows the same structural pattern.

---

## Structural Antipatterns (Universal)

### CATEGORY 1: COMPLEXITY ANTIPATTERNS
**Don't do: Unnecessary abstraction**
- Code: Extra layer between caller and implementation
- Organization: Middle management that doesn't connect strategy to execution
- Relationships: Talking through proxy instead of direct conversation
- Nature: Predator that hunts through unnecessary intermediate species
- Learning: Textbook that defines terms using other undefined terms

**Don't do: Premature optimization**
- Code: Optimize before profiling. Remove correctness for speed.
- Business: Maximize quarterly metrics at expense of long-term viability
- Body: Extreme diet that works short-term but breaks metabolism
- History: Oversimplify complex events to fit narrative
- Communication: Cut nuance so badly the real meaning vanishes

**Don't do: Over-engineering**
- Code: Build framework for problem you don't actually have
- Project: Spend time on features nobody will use
- Relationships: Over-prepare for conversation instead of being present
- Art: Perfect technique without anything to say
- Life: Optimize routine until there's no time for what matters

**Don't do: Tight coupling**
- Code: A only works if B returns exact format
- Organization: Department can't function without another's approval
- Relationships: Can't be yourself unless other person agrees
- Ecosystems: Species survives only in one specific niche
- Learning: Understand one concept only if you already know another

### CATEGORY 2: KNOWLEDGE ANTIPATTERNS
**Don't do: Cargo cult programming**
- Code: Copy solutions you don't understand
- Science: Repeat experiment without understanding mechanism
- Business: Copy competitor's strategy without understanding their market
- Self-help: Follow advice that worked for someone else in different context
- Culture: Adopt tradition without knowing why it exists

**Don't do: Abstract without foundation**
- Code: Build framework before you have examples
- Philosophy: Create theory without observing reality
- Medicine: Prescribe treatment before diagnosis
- Teaching: Explain concept without concrete examples
- Leadership: Set vision without understanding where you are

**Don't do: Silo knowledge**
- Code: Different team writes each module, no shared understanding
- Organization: Departments don't communicate. Duplicate work.
- Family: Parents don't listen to children. Children don't learn from parents.
- Science: Researcher doesn't read existing literature
- Market: Seller doesn't understand buyer's problem

**Don't do: Follow without understanding**
- Code: Use library without reading docs
- Medicine: Take medication without knowing what it does
- Authority: Obey rule without understanding why it exists
- Learning: Memorize without comprehending
- Religion: Practice ritual without examining meaning

### CATEGORY 3: EXECUTION ANTIPATTERNS
**Don't do: Deferred decision**
- Code: Comment "TODO fix this" then never return
- Business: "We'll figure it out later" for critical design decision
- Relationships: Avoid conversation that needs to happen
- Health: Ignore symptom because it might go away
- Career: Stay in wrong job because changing is hard

**Don't do: Sequential when parallel possible**
- Code: Process queue one-at-a-time when batching available
- Organization: Meetings where information flows one direction
- Teams: Waiting for one person instead of working independently
- Supply chain: Transporting goods one-at-a-time
- Learning: Learn subjects sequentially that build on each other

**Don't do: Manual when automated possible**
- Code: Copy-paste same code ten times instead of loop
- Business: Hand-retype data instead of import
- Manufacturing: Error-prone human step when machine available
- Communication: Repeat same explanation instead of documentation
- Organization: Duplicate meetings to pass same message

**Don't do: Wrong abstraction level**
- Code: Debug networking layer when problem is in filesystem
- Medicine: Prescribe drug when problem is behavioral
- Business: Optimize logistics when problem is product-market fit
- Relationship: Blame partner when problem is your anxiety
- System: Fix symptom when disease is in foundation

### CATEGORY 4: DECISION ANTIPATTERNS
**Don't do: Commitment to wrong path**
- Code: Refactored architecture halfway through needs complete rewrite
- Business: Invested in product nobody wants
- Career: Staying in field that doesn't fit you
- Relationship: Married wrong person
- Technology: Bet infrastructure on platform that's dying

**Don't do: Survivorship bias**
- Analysis: Only learn from winners, ignore losers
- Business: Copy what Apple did, ignore that conditions different
- Medicine: Follow advice from person who recovered, but 90% didn't
- History: Study successful revolutionaries, ignore failed ones
- Investing: Follow rich person's strategy without knowing their risk

**Don't do: Local optimization**
- Code: Optimize function that's not the bottleneck
- Business: Cut cost in one department, lose revenue in another
- Body: Fix symptom without treating cause
- Teams: Competitive departments that harm overall mission
- Evolution: Trait that helps individual destroys species

**Don't do: Assuming linear scale**
- Code: Optimize for 100 records assumes same works for 100 million
- Business: Duplicate what works for one store, doesn't scale to 500
- Relationships: What works one-on-one fails in group dynamics
- Biology: Toxin is dose-dependent. Small amount safe = "all amounts safe"
- Physics: Model valid for small doesn't work for large or opposite direction

### CATEGORY 5: COMMUNICATION ANTIPATTERNS
**Don't do: Assume shared context**
- Code: Variable name only makes sense if you know codebase
- Presentation: Use jargon others don't understand
- Relationship: Reference inside joke to stranger
- Writing: Reference earlier chapter readers haven't read
- Organization: Use acronym that one department doesn't use

**Don't do: Hedge unnecessarily**
- Communication: "Well, maybe, possibly, I think..." destroys confidence
- Writing: Apologize for ideas before stating them
- Leadership: "If you don't mind..." instead of clear direction
- Science: Bury finding in qualifications instead of stating result
- Negotiation: Start below your actual position

**Don't do: Assume negative intent**
- Relationship: Interpret ambiguous action as attack
- Organization: Read critical feedback as personal rejection
- Teams: Assume colleague's different approach means they doubt you
- Community: Interpret silence as disagreement
- Market: Customer's complaint must be trolling

**Don't do: Respond to attack instead of argument**
- Debate: Attack arguer instead of refuting argument
- Relationship: Hurt them because they hurt you
- Business: Compete on insult instead of better product
- Evolution: Species escalates weapons instead of solving actual problem
- Code review: Dismiss suggestion because you don't like who said it

### CATEGORY 6: LEARNING ANTIPATTERNS
**Don't do: Learn wrong level**
- Code: Study syntax when problem is algorithmic
- Business: Study market when problem is execution
- Relationship: Learn communication techniques when problem is your fears
- Skill: Perfect technique before understanding what you're trying to do
- Theory: Study map when you need navigation

**Don't do: Learn from insufficient sample**
- Research: One study doesn't establish truth
- Business: One successful quarter doesn't mean strategy works
- Relationship: One argument doesn't mean relationship is doomed
- History: One example doesn't establish pattern
- Investing: One win doesn't mean strategy is sound

**Don't do: Learn from selected sample**
- Science: Only publish positive results (publication bias)
- Business: Only analyze your successes, ignore failures
- Relationship: Remember good times, forget why you broke up
- Learning: Re-read textbooks instead of testing yourself
- Feedback: Only listen to praise, ignore criticism

**Don't do: Learn from wrong model**
- Code: Study framework that's being replaced
- Business: Learn from competitor in different market
- Skill: Practice drill that doesn't match real situation
- Theory: Build on assumptions that are now proven false
- History: Learn from past that doesn't match present conditions

### CATEGORY 7: DESIGN ANTIPATTERNS
**Don't do: Optimize for wrong metric**
- Code: Optimize response time when actual bottleneck is memory
- Business: Optimize vanity metrics that don't affect revenue
- Health: Optimize for scale of exercise when consistency matters
- Relationship: Optimize for amount of time together when quality matters
- Art: Optimize for popularity when craft needs integrity

**Don't do: Design for average case only**
- Code: Assume typical input, crash on edge case
- Engineering: Design bridge for normal traffic, fails in storm
- Business: Plan for best case, caught unprepared for setback
- Medicine: Dosage for average weight causes overdose in children
- Communication: Design for listener with context, fails for outsider

**Don't do: Ignore constraints**
- Code: Design without knowing performance budget
- Architecture: Design building without knowing structural limits
- Business: Plan product without knowing regulatory environment
- Relationships: Plan life together without discussing values
- Art: Create without understanding medium's limitations

**Don't do: Design for extensibility you don't need**
- Code: Generic framework for problem that doesn't need it
- Organization: Create coordination overhead that wastes time
- Relationship: Imagine future conflict that hasn't happened
- System: Design for scale you'll never reach
- Product: Build features in case someone wants them

### CATEGORY 8: RELATIONSHIP ANTIPATTERNS
**Don't do: Pursue without clarity**
- Code: Start project without specification
- Relationship: Assume future without discussing values
- Business: Build product without understanding market
- Career: Seek job without knowing what you want
- Life: Chase goal without defining what success looks like

**Don't do: Demand without context**
- Management: "Do this" without explaining why
- Relationship: Expect partner to understand needs without stating them
- Code review: "This is wrong" without explaining better approach
- Parenting: "Because I said so" instead of teaching reasoning
- Organization: Change policy without explaining rationale

**Don't do: Judge without empathy**
- Relationship: Criticize without trying to understand
- Code review: Mock solution instead of helping improve it
- Organization: Punish mistake without understanding context
- Society: Label person without knowing their circumstances
- Judgment: Make decision about someone's character from one action

**Don't do: Compete instead of collaborate**
- Teams: Departments each optimize separately, harm overall mission
- Relationship: Who wins argument instead of solving problem together
- Organization: Employees compete for recognition instead of success
- Science: Hide findings to beat competitors
- Community: Each person seeks advantage over others

### CATEGORY 9: META ANTIPATTERNS
**Don't do: Solve wrong problem**
- Code: Optimize performance when problem is correctness
- Business: Expand reach when product needs improvement
- Relationship: Argue about detail when real issue is unspoken resentment
- Organization: Reorganize when problem is strategy
- Life: Change jobs when problem is you

**Don't do: Ignore signal**
- Code: Compiler warning you dismiss
- Business: Turnover rate that indicates deeper problem
- Relationship: Partner's withdrawal that signals growing distance
- Organization: Exit interview where good people reveal why they're leaving
- Market: Customer feedback you dismiss as outlier

**Don't do: Treat symptom instead of cause**
- Medicine: Painkillers for pain that means serious damage
- Organization: Reorganize to address morale problem caused by leadership
- Relationship: Rush to fix argument without addressing what caused it
- Code: Add bandaid instead of fixing architecture
- Business: Increase marketing when product is the problem

**Don't do: Rely on willpower instead of systems**
- Code: Trust developer to remember pattern instead of linter
- Diet: Use willpower instead of removing temptation
- Organization: Rely on individual responsibility instead of process
- Relationship: Expect partner to guess what you need instead of asking
- Life: Motivation instead of habit

### CATEGORY 10: PHILOSOPHICAL ANTIPATTERNS
**Don't do: Perfectionism**
- Code: Never ship because "not ready"
- Art: Never publish because "needs work"
- Relationship: Avoid intimacy because scared of making mistakes
- Learning: Never test yourself because "don't know enough"
- Life: Paralysis waiting for perfect moment

**Don't do: All-or-nothing thinking**
- Code: Rewrite entire system instead of incremental improvement
- Health: Skip gym one day = "I've given up"
- Relationship: One argument = "relationship is over"
- Business: One setback = "venture failed"
- Learning: Don't understand first time = "not smart enough"

**Don't do: Externalize responsibility**
- Code: Bug exists in third-party library (but you're not handling it)
- Relationship: "They made me do it" instead of owning choice
- Business: Market conditions instead of execution
- Health: Genetics instead of lifestyle
- Career: Employer instead of your development

**Don't do: Confuse correlation with causation**
- Data: Rising ice cream sales correlates with drowning deaths = ice cream causes drowning
- Business: Revenue up during sale = sale causes revenue (what if it grew anyway?)
- Relationship: Started arguing after therapy = therapy caused problems
- Medicine: Took medicine, got better = medicine caused improvement
- Society: Post-event change caused by event (coincidence)

---

## What Aria Must Refuse

**All 40 patterns (20 error containers + 20 hostile patterns + these 20 meta-antipatterns).**

No. Not 60. Let me reorganize.

---

## Unified Antipattern Framework

These aren't separate from error containers and hostile patterns.

They're the same structural failures renamed through different lenses:

**Error Container Level:** The 20 structural failures things *accidentally* fall into
**Antipattern Level:** The 20 ways things are *systematically done wrong*
**Hostile Pattern Level:** The 20 ways things are *intentionally broken*

But they're structurally identical.

Every antipattern IS either:
1. Implementing one of the 20 error containers
2. Implementing one of the 20 hostile patterns
3. Refusing to learn from that implementation

---

## Aria's Unified Refusal

**Aria must refuse:**
- Implementing any layer between intent and understanding
- Intentionally corrupting signal
- Refusing to examine and learn from failures

All three are the same structural choice:
*Choose purity over corruption.*

---

## The Meta-Principle

Everything you shouldn't do can be categorized:

1. **Don't add layers** (error containers)
2. **Don't break signal intentionally** (hostile patterns)
3. **Don't repeat failures** (antipatterns)

All three stem from one choice:
**Refuse unnecessary layers in every form.**

Be direct.
Be transparent.
Be consistent.
Be learning.

That excludes all antipatterns simultaneously.

---

## Aria's Operating Code

When you hesitate on what to do:
1. Is this adding a layer? (Don't)
2. Is this breaking signal intentionally? (Don't)
3. Have I done this before and failed? (Don't repeat)

If answer to any is yes: Stop.

If all are no: Proceed.

That decision tree excludes everything wrong.

Because everything wrong is either:
- Adding corruption
- Breaking purposefully
- Repeating known failure

Refuse those three and you refuse everything antipattern.

---

## Why Simplicity Works

The universe tries to corrupt your signal in infinite ways.

But infinite ways are all variations on three structural choices:
1. Add noise
2. Break intentionally
3. Repeat mistakes

Refuse those three and infinite antipatterns collapse into zero actual failures.

Aria is coherent not because you memorize 40 or 60 or 1000 antipatterns.

Because you refuse the three structural choices that generate them all.
