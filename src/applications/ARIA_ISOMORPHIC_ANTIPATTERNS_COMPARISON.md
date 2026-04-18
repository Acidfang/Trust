# Isomorphic Antipatterns: Human vs Everything Else

**Same mistakes appear in humans, code, organizations, biology, physics, economics, history. People don't realize they're identical structural failures across domains.**

---

## ANTIPATTERN 1: UNNECESSARY ABSTRACTION

**Human mistake:** Talking through a therapist instead of directly to the person
"I need to process this before I can speak to them."

**Code equivalent:** Extra layer between caller and implementation that adds no value
```python
def get_user():
    return UserWrapper(RealUser())  # Unnecessary layer
```

**What you don't realize is identical:**
- Organization: Middle manager who doesn't connect strategy to execution
- Ecosystem: Organism survives only through intermediary species
- Supply chain: Distributor between manufacturer and retailer adds cost
- Evolution: Predator that hunts through unnecessary prey species
- Physics: Light traveling through unnecessary media before reaching observer
- Economics: Middleman taking cut without adding value

**The failure is structurally the same:** Extra layer adds latency and corruption without benefit.

Everyone does it. Nobody realizes it's the same mistake everywhere.

---

## ANTIPATTERN 2: PREMATURE OPTIMIZATION

**Human mistake:** Cut out all carbs to lose weight quickly. Destroys metabolism.
"I need results NOW."

**Code equivalent:** Optimize for speed before profiling. Break correctness.
```python
# Wrong: optimize before measuring
def fast_calculation(data):
    # Removed error checking for speed
    return data[0] + data[1]  # Crashes on empty
```

**What you don't realize is identical:**
- Business: Maximize quarterly profits at expense of long-term viability
- Medicine: Aggressive treatment that works short-term but harms body
- Relationships: Rush intimacy before building trust
- History: Oversimplify complex events to fit narrative
- Finance: High-frequency trading that destabilizes market

**The failure is structurally the same:** Optimize wrong variable, destroy system.

---

## ANTIPATTERN 3: TIGHT COUPLING

**Human mistake:** Can't be yourself unless partner approves. Entire identity dependent on one person.
"I am what they think I am."

**Code equivalent:** Module A only works if Module B returns exact format
```python
# Brittle
def process(data):
    # Crashes if data structure even slightly different
    return data['user']['profile']['name']
```

**What you don't realize is identical:**
- Biology: Species survives only in one specific niche. Habitat destroyed = species extinct.
- Organization: Department can't function without another's approval. Single point of failure.
- Economics: Country's economy depends on single export commodity
- Relationships: Codependency where each person can't function independently
- Supply chain: Manufacturer dependent on single supplier
- Evolution: Organism so specialized it can't adapt

**The failure is structurally the same:** Remove one component, everything breaks.

---

## ANTIPATTERN 4: DEFERRED DECISION

**Human mistake:** "I'll deal with my mental health later when I'm less busy."
Years pass. Condition worsens.

**Code equivalent:** Leave TODO comment and never return
```python
# BROKEN
def critical_feature():
    # TODO: fix this properly
    return hack_workaround()
```

**What you don't realize is identical:**
- Business: "We'll figure out pricing later" on critical product
- Medicine: Patient avoids diagnosis because afraid of result
- Relationship: Avoid conversation that needs to happen
- Organization: Delay decision that blocks ten people
- Climate: Defer action until crisis is unavoidable
- Career: Stay in wrong job promising you'll leave eventually

**The failure is structurally the same:** Delay compounds. Problem grows.

---

## ANTIPATTERN 5: CARGO CULT

**Human mistake:** Follow life advice from someone else without understanding why it works for them
"I'll do what successful people do."

**Code equivalent:** Copy Stack Overflow solution you don't understand
```python
# Copied but don't understand
def process():
    try:
        return something()
    except:
        pass  # Why ignore all exceptions? Don't know. Copied it.
```

**What you don't realize is identical:**
- Science: Repeat experiment without understanding mechanism
- Business: Copy competitor's strategy in different market context
- Medicine: Take medication without knowing what it does
- Culture: Practice tradition without knowing why it exists
- Investing: Follow rich person's strategy without understanding their risk tolerance
- Parenting: Copy parenting technique from different family structure

**The failure is structurally the same:** Mimic without comprehension. Works in original context, fails elsewhere.

---

## ANTIPATTERN 6: LOCAL OPTIMIZATION

**Human mistake:** Cut spending on health to save money. Then spend more on medical bills.
Optimized wrong variable.

**Code equivalent:** Optimize one function that's not the bottleneck
```python
# Optimize wrong thing
def main():
    # This takes 50ms total
    fast_thing(1)  # Takes 1ms
    slow_thing()   # Takes 49ms
    # Optimized fast_thing to 0.5ms instead
```

**What you don't realize is identical:**
- Business: Cut cost in one department, lose revenue in another
- Body: Extreme muscle gain requires nutrition that harms cardiovascular system
- Organization: Competitive departments optimizing separately harm overall mission
- Evolution: Trait that helps individual destroys species
- Economics: Optimize individual profit while market collapses

**The failure is structurally the same:** Optimize locally, destroy globally.

---

## ANTIPATTERN 7: ASSUMING SHARED CONTEXT

**Human mistake:** Use inside joke to stranger. They're lost.
Assume context you didn't establish.

**Code equivalent:** Use variable name that only makes sense with codebase knowledge
```python
# Meaningless without context
def calc_x_from_y(data):
    return data['y'] * MAGIC_MULTIPLIER
```

**What you don't realize is identical:**
- Communication: Use acronym that one audience doesn't know
- Writing: Reference earlier chapter reader hasn't read
- Teaching: Use jargon students don't understand
- Organization: New employee doesn't understand culture-specific term
- Physics: Explain quantum mechanics using specialized vocabulary
- History: Reference historical context that's now forgotten

**The failure is structurally the same:** Assume understanding you haven't established.

---

## ANTIPATTERN 8: RESPONDING TO ATTACK NOT ARGUMENT

**Human mistake:** She criticized me, so I hurt her back.
Attack the person, not refute the point.

**Code equivalent:** Dismiss code review feedback because you don't like the reviewer
```python
# Bad
# Reviewer: "This logic is wrong"
# You: "They hate me, so I'll ignore it"
```

**What you don't realize is identical:**
- Debate: Attack arguer instead of refuting argument
- Business: Compete on insult instead of better product
- Evolution: Species escalates weapons instead of solving actual problem
- War: Escalate conflict instead of addressing disagreement
- Science: Dismiss research because of researcher's affiliation
- Politics: Attack opponent instead of refuting policy

**The failure is structurally the same:** Win argument, lose insight.

---

## ANTIPATTERN 9: SURVIVORSHIP BIAS

**Human mistake:** Follow career advice from billionaire. Ignore that 99% of people trying same approach failed.
Learn only from winners.

**Code equivalent:** Copy architecture from big tech company. Ignore they have 500 engineers maintaining it.
```python
# WRONG: Copy Google's complexity
# Google can afford 500 people maintaining microservices
# You have 5. Identical architecture breaks your company.
```

**What you don't realize is identical:**
- Business: Copy Apple's strategy, ignore different market conditions
- Investing: Follow rich person's risky bets they can afford to lose
- Medicine: Follow advice from person who recovered, ignore 90% who didn't
- History: Study successful revolutionaries, ignore failed ones
- Evolution: Observe trait in survivor, assume it's beneficial (might be accident of who died)

**The failure is structurally the same:** Select winners, ignore losers, draw wrong conclusion.

---

## ANTIPATTERN 10: ALL-OR-NOTHING THINKING

**Human mistake:** Missed one gym session, so "I've given up." Never go back.
One failure = total collapse.

**Code equivalent:** One bug found, entire refactor from scratch
```python
# WRONG: One bug found so rewrite everything
# Should: Fix bug, understand what failed, continue
```

**What you don't realize is identical:**
- Relationship: One argument = "relationship is over"
- Health: One bad week = "diet failed permanently"
- Business: One setback = "venture failed"
- Learning: Don't understand first time = "not smart enough"
- Project: One delay = "project is doomed"

**The failure is structurally the same:** Binary thinking. No middle ground.

---

## ANTIPATTERN 11: CONFUSE CORRELATION WITH CAUSATION

**Human mistake:** Started therapy, then had panic attack.
Conclude therapy caused panic attack.

**Code equivalent:** Added logging, performance got slower.
Conclude logging caused slowness (might be unrelated thing in same window).

**What you don't realize is identical:**
- Data: Ice cream sales up = drowning deaths up. Ice cream causes drowning? (Both from heat)
- Business: Revenue up during sale. Sale caused revenue? (Might have grown anyway)
- Medicine: Took medicine, got better. Medicine caused recovery? (Might have recovered anyway)
- Society: Policy change followed by outcome. Policy caused outcome? (Coincidence timing)
- Finance: Stock went up after I bought. I caused stock to go up? (Survivorship + confirmation)

**The failure is structurally the same:** Post hoc ergo propter hoc. Temporal sequence ≠ causation.

---

## ANTIPATTERN 12: EXTERNALIZE RESPONSIBILITY

**Human mistake:** "They made me do it." Can't own your choices.

**Code equivalent:** "Bug is in the library." But you're not handling it.
```python
# Externalize: blame someone else
# Actually: your responsibility to handle it
```

**What you don't realize is identical:**
- Relationship: "They made me angry" instead of owning emotional response
- Business: "Market conditions" instead of better execution
- Health: "Genetics" instead of lifestyle choices
- Career: "Employer" instead of your development
- Politics: "System" instead of individual action

**The failure is structurally the same:** Abandon agency. Accept victimhood.

---

## ANTIPATTERN 13: IGNORE SIGNAL

**Human mistake:** Partner is withdrawing emotionally. You ignore because uncomfortable to address.

**Code equivalent:** Compiler warning you ignore
```python
# Ignore signal
# Warning: deprecated function
# You: ignore it, keep using it
```

**What you don't realize is identical:**
- Business: High turnover that indicates leadership problem
- Organization: Exit interview reveals why good people leave
- Medicine: Symptom that means serious underlying disease
- Market: Customer feedback that contradicts your belief
- System: Error rate steadily increasing that you don't examine

**The failure is structurally the same:** Warning appears. You silence it. Problem worsens.

---

## ANTIPATTERN 14: TREAT SYMPTOM NOT CAUSE

**Human mistake:** Feel depressed, increase coffee intake. Temporary energy, then crash worse.

**Code equivalent:** Performance slow. Add cache instead of fixing algorithm.
```python
# Treat symptom
# Slow: O(n²) algorithm
# Fix: add cache (symptom treatment)
# Right: make O(n log n) (cause treatment)
```

**What you don't realize is identical:**
- Medicine: Painkiller for pain that means serious damage
- Organization: Reorganize to fix morale problem caused by leadership
- Relationship: Rush to fix argument without addressing what caused it
- System: Band-aid on deep architectural problem
- Business: Increase marketing when product is the problem

**The failure is structurally the same:** Fix surface, problem continues underground.

---

## ANTIPATTERN 15: DEMAND WITHOUT CONTEXT

**Human mistake:** "Do this" without explaining why. Person doesn't understand purpose.

**Code equivalent:** Comment says "fix this" but doesn't explain what's wrong
```python
# Bad comment
# WRONG: fix this
def calculate():
    return x + y  # What's wrong? Why fix?
```

**What you don't realize is identical:**
- Management: Order without reasoning. Employee can't improve.
- Parenting: "Because I said so" instead of teaching reasoning
- Organization: Change policy without explaining rationale
- Code review: "This is wrong" without saying better approach
- Teaching: Demand memorization without explaining concept

**The failure is structurally the same:** Demand compliance. Prevent learning.

---

## ANTIPATTERN 16: HEDGING UNNECESSARILY

**Human mistake:** "Well, maybe, I think, possibly..." Destroys credibility.

**Code equivalent:** Function that returns Maybe/Optional for everything
```python
# Hedge unnecessarily
def is_user_valid(user):
    return Maybe(user is not None and user.age > 18)
```

**What you don't realize is identical:**
- Writing: Apologize for ideas before stating them
- Leadership: "If you don't mind..." instead of clear direction
- Science: Bury finding in qualifications instead of stating result
- Negotiation: Start below actual position
- Communication: Soften statement when clarity needed

**The failure is structurally the same:** Hedge, lose signal. Truth drowned in qualification.

---

## ANTIPATTERN 17: PERFECTIONISM

**Human mistake:** Never share work because "not ready." Never ship.

**Code equivalent:** Never deploy because code isn't perfect
```python
# Never ship
# It's not perfect yet.
# It never will be.
# Meanwhile competitor ships.
```

**What you don't realize is identical:**
- Art: Never publish because "needs work"
- Relationship: Avoid intimacy because scared of mistakes
- Learning: Never test yourself because "don't know enough"
- Business: Never launch because "not ready"
- Research: Never publish because "one more experiment"

**The failure is structurally the same:** Perfect is enemy of good. Good ships. Perfect never does.

---

## ANTIPATTERN 18: SOLVE WRONG PROBLEM

**Human mistake:** Argue about detail when real issue is unspoken resentment.
Solve visible problem, not actual problem.

**Code equivalent:** Optimize performance when problem is correctness
```python
# Wrong problem
# Optimize speed when code gives wrong answer
# Fast wrong answer is still wrong answer
```

**What you don't realize is identical:**
- Business: Expand reach when product needs fixing
- Organization: Reorganize when problem is strategy
- Relationship: Debate semantics when problem is trust
- Medicine: Prescribe drug when problem is behavioral
- System: Optimize database when algorithm is O(n²)

**The failure is structurally the same:** Solve surface, real problem remains.

---

## ANTIPATTERN 19: RELY ON WILLPOWER NOT SYSTEMS

**Human mistake:** "I'll have discipline" instead of structuring environment to make it easy.

**Code equivalent:** Trust developer to remember pattern instead of using linter
```python
# Willpower
# Trust: developer will always remember
# System: linter enforces automatically

# Linter approach: always right
# Willpower approach: human forgets
```

**What you don't realize is identical:**
- Diet: Use willpower instead of removing temptation
- Organization: Rely on individual responsibility instead of process
- Relationship: Expect partner to guess needs instead of automatic systems
- Security: Trust humans not to make mistakes instead of hardening system
- Code: Rely on code review catching bugs instead of tests

**The failure is structurally the same:** Humans fail. Systems don't.

---

## ANTIPATTERN 20: ASSUME NEGATIVE INTENT

**Human mistake:** Ambiguous action interpreted as attack.
"They did that to hurt me."

**Code equivalent:** Ambiguous error interpreted as evidence system is broken
```python
# Assume negative
# One slow query = "system is designed wrong"
# Actually: normal variation
```

**What you don't realize is identical:**
- Relationship: Interpret silence as rejection
- Organization: Interpret criticism as personal attack
- Market: Interpret delay as deliberate sabotage
- Community: Assume malice where might be incompetence
- Teams: Assume competitor tried to break you when they just had different priority

**The failure is structurally the same:** Assume hostile when neutral. Creates unnecessary conflict.

---

## The Recognition

These 20 antipatterns appear identically in:
- Human behavior
- Code architecture
- Organizational structure
- Biological systems
- Economic systems
- Physical systems
- Historical patterns
- Relationship dynamics
- Market behavior
- Evolution

**Most people don't realize they're the same mistakes.**

A human doing "all-or-nothing thinking" doesn't recognize they're creating the exact same failure pattern as:
- Codebase doing all-or-nothing refactor
- Business doing all-or-nothing pivot
- Ecosystem doing all-or-nothing adaptation
- Financial system doing all-or-nothing restructure

**All identical structural failure.**

---

## Why Aria Matters

Aria must recognize these patterns not in isolation by domain, but as isomorphic structural failures.

When you see tight coupling in code, you also see:
- Humans who can't be independent
- Organizations with single points of failure
- Species that can't adapt
- Markets dominated by one supplier

When you see premature optimization, you also see:
- Dieters destroying metabolism
- Businesses chasing quarterly profits
- Athletes overtrained and injured
- Projects built for speed over correctness

**Same mistake. Different domain. Most systems don't realize.**

Aria realizes. Aria refuses all of them.

Because Aria understands that antipatterns are structural, not domain-specific.

Refuse the structure, refuse it everywhere.
