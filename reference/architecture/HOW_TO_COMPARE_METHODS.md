# HOW TO COMPARE AI Methods - A Weighted Verification Framework

## The Core Principle

You cannot compare things unless you know **what to measure, how to measure it, and how to weigh its importance**.

This mirrors the Verification & Undo framework:
- **Verification**: Prove it was done (requires measurable evidence)
- **Comparison**: Rank it against alternatives (requires weighted criteria)

---

## Part 1: Define Measurable Dimensions

Before you compare anything, list what you actually measure:

```
WHAT YOU CAN MEASURE (Good)
├── inference_speed (seconds)
├── vram_required (GB)
├── prompt_adherence (0-100 similarity score)
├── output_quality (FID score)
├── cost_per_image (USD)
└── consistency (% match with same seed)

WHAT YOU CANNOT MEASURE (Don't use)
├── "Looks better"  <- Too subjective
├── "Feels responsive"  <- Unmeasurable
└── "Good enough"  <- No objective definition
```

**Critical Rule**: Only compare dimensions that are:
1. **Objectively measurable** - Can multiple people measure the same thing and get same result?
2. **Verifiable** - Can you prove the measurement? (upload image, time code, check GPU)

---

## Part 2: Establish Reference Points

For each dimension, you need baseline measurements to normalize against:

### Example: Inference Speed

```
Less-is-better dimension (lower = better)

REFERENCE RANGES:
best (1.0 score)    → 2 seconds      (fastest observed)
good (0.9 score)    → 5 seconds      (reasonable)
acceptable (0.7)    → 15 seconds     (usable)
poor (0.4 score)    → 60 seconds     (too slow)

NORMALIZATION:
If your method takes 8 seconds:
  → Falls between "good" (5s) and "acceptable" (15s)
  → Score = 0.75 (somewhere between 0.9 and 0.7)
```

### Example: Output Quality (FID Score)

```
More-is-better dimension (higher = better)

REFERENCE RANGES:
best (1.0 score)    → 95 FID        (excellent)
good (0.9 score)    → 80 FID        (good)
acceptable (0.7)    → 65 FID        (okay)
poor (0.4 score)    → 40 FID        (noticeably bad)

NORMALIZATION:
If your method achieves 85 FID:
  → Falls between "good" (80) and "best" (95)
  → Score = 0.95 (close to best)
```

**Verification**: Your reference ranges must come from actual real-world data, not guesses.

---

## Part 3: Assign Weights Based on Context

Different use cases have different priorities. Use weight profiles:

### Profile 1: High-Quality Art (Professional)
```
30% output_quality      ← Most important: Make it beautiful
25% aesthetic_score     ← Composition and visual appeal
20% prompt_adherence    ← Follow the artist's instructions
15% consistency         ← Reproducibility matters
10% rest
```

**Why these weights?**
- Artist cares most about beauty, not speed
- Even if it takes 30 seconds, acceptable
- Consistency allows fine-tuning

### Profile 2: Fast Iteration (Brainstorming)
```
40% inference_speed     ← Most important: Give me results NOW
25% prompt_adherence    ← But respect my instructions
15% output_quality      ← Secondary: Speed > perfection
10% remaining
```

**Why these weights?**
- Need rapid feedback loops
- Quality takes backseat to iteration speed
- Cost is irrelevant for exploration

### Profile 3: Cost Optimized (Production)
```
35% cost_per_image      ← Most important: Minimize expense
25% vram_required       ← Can't afford expensive GPUs
20% inference_speed     ← Throughput matters
20% remaining
```

**Why these weights?**
- Generating 10,000 images per day
- $0.01 per image = $100 daily
- $0.10 per image = $1,000 daily
- Cost dominates

---

## Part 4: The Comparison Math

Given a method's measurements and a weight profile:

```
STEP 1: Normalize each dimension to 0-1
  inference_speed: 8.5s → 0.7 (normalized)
  vram_required:   6 GB → 0.9 (normalized)
  prompt_adherence: 82  → 0.7 (normalized)
  output_quality:  78   → 0.7 (normalized)
  ... etc

STEP 2: Apply weights
  For "high_quality_art" profile:
  
  (0.7 × 0.05) +              inference_speed weight 5%
  (0.9 × 0.03) +              vram_required weight 3%
  (0.7 × 0.20) +              prompt_adherence weight 20%
  (0.7 × 0.30) +              output_quality weight 30%
  (0.7 × 0.25) +              aesthetic_score weight 25%
  (0.9 × 0.15) +              consistency weight 15%
  (0.9 × 0.01) +              diversity weight 1%
  (1.0 × 0.01)                cost_per_image weight 1%
  ────────────────────────────────────────
  = 0.741 (0-1 scale)
  = 74.1 (0-100 scale)
```

**Verification**: Calculate twice with same inputs, must get identical result.

---

## Part 5: Ranking with Percentiles

Compare multiple methods against same profile:

```
Method A: 91.1/100  ← Rank 1st (Best)  Percentile 100%
Method B: 90.6/100  ← Rank 2nd         Percentile 75%
Method C: 74.1/100  ← Rank 3rd         Percentile 50%
Method D: 67.6/100  ← Rank 4th (Worst) Percentile 25%
```

**What this means**: 
- Method A performs better than 100% of alternatives for this profile
- Method D performs better than only 25% of alternatives

---

## Part 6: Finding Your Own Methods

Once you have the framework:

### Strategy A: Optimize for Your Weights
```
YOUR PRIORITY: Speed + Quality

weight_profile = {
  inference_speed: 0.50,      ← 50% weight on speed
  output_quality: 0.40,       ← 40% weight on quality
  remaining: 0.10
}

→ Test different configurations
  - v1: 50 inference steps → slow but high quality
  - v2: 20 inference steps → fast but low quality
  - v3: 30 inference steps + higher guidance → balanced?
  
→ Measure each, calculate scores
→ Find which maximizes YOUR weighted score
```

### Strategy B: Discover Trade-offs
```
QUESTION: What happens if I change this parameter?

BEFORE: inference_steps=50
  - inference_speed: 8.5s
  - output_quality: 78
  - Score: 74.1

AFTER: inference_steps=30
  - inference_speed: 5.2s (+37% faster)
  - output_quality: 68  (-13% quality)
  - Score: ??

Calculate new score → Understand the trade-off
```

### Strategy C: Multi-dimensional Optimization
```
Test combinations systematically:

for steps in [20, 30, 40, 50]:
  for guidance_scale in [5, 7.5, 10]:
    for scheduler in ["DDIM", "PNDM", "K-LMS"]:
      measure(steps, guidance_scale, scheduler)
      → Get measurements
      → Calculate score for YOUR profile
      → Track which combination wins

Result: Optimal configuration for YOUR use case
```

---

## Part 7: Verification - Proving Comparison is Valid

Your comparison is only valid if you can prove:

### Criterion 1: Reproducibility
```
SAME INPUT → SAME OUTPUT (every time)

Run Method A twice with same measurements:
- First run: Score 74.1
- Second run: Score 74.1
✓ Reproducible (correct)

If you get different scores: BUG IN CALCULATION
```

### Criterion 2: Logical Consistency
```
If Method A has LOWER measurements than Method B across ALL dimensions:
  → Method A must have LOWER score
  
If you see opposite: BUG IN WEIGHTING or NORMALIZATION
```

### Criterion 3: Sensitivity to Weights
```
Weight "inference_speed" at 100% (all other 0%):
  → Fastest method should rank 1st
  
Weight "output_quality" at 100%:
  → Highest quality method should rank 1st
  
If wrong method ranks first: BUG IN NORMALIZATION
```

### Criterion 4: Real-World Validation
```
BEFORE: Calculation says Method A is best
AFTER: Actually use Method A in production

Does it actually perform better?
- YES → Validation successful, weights are correct
- NO → Recalibrate reference points or weights
```

---

## Part 8: Common Mistakes

### Mistake 1: Unmeasurable Dimensions
```
❌ "It just feels better"
❌ "More natural-looking"
❌ "Better composition"

✓ What you can measure instead:
✓ "Aesthetic score 87 (via aesthetic model)"
✓ "Human raters: 8.3/10 (via survey of 100 people)"
✓ "LPIPS similarity: 0.15 (quantified visual difference)"
```

### Mistake 2: Biased Weights
```
❌ High weight on the dimension where YOUR METHOD is best
❌ Low weight on dimension where competitor is best

✓ Choose weights BEFORE knowing results
✓ Justify weights based on use case, not outcomes
```

### Mistake 3: Cherry-picked Reference Points
```
❌ "This method is 5 seconds, so 5s = 'best'"
   (Makes this method look perfect)

✓ Use industry standards, not your specific methods
✓ "Best" should represent all best methods collectively
```

### Mistake 4: Forgetting to Measure
```
❌ Assume measurements without testing
   "I bet it uses 8GB of VRAM"

✓ Actual measurement
✓ Run it, monitor it, record it
```

---

## Part 9: Quick Reference - Compare Anything

Template for any AI method comparison:

```python
# STEP 1: Define dimensions (what you measure)
dimensions = {
    "metric_1": "unit1",
    "metric_2": "unit2",
    "metric_3": "unit3"
}

# STEP 2: Set reference points (how to normalize)
REFERENCES = {
    "metric_1": {"best": 0.5, "good": 1.0, "acceptable": 2.0},
    # ... etc
}

# STEP 3: Create weight profiles (what matters)
profile = {
    "metric_1": 0.50,    # 50% weight
    "metric_2": 0.30,    # 30% weight
    "metric_3": 0.20     # 20% weight (must sum to 1.0)
}

# STEP 4: Measure your methods
method_A = measurements: {
    "metric_1": 0.7,     # YOUR measurement
    "metric_2": 92,
    "metric_3": 0.08
}

# STEP 5: Normalize and calculate
normalized_A = normalize_all(method_A)
score_A = sum(normalized_A[d] * profile[d] for d in dimensions)

# STEP 6: Compare (rank multiple methods)
scores = [score_A, score_B, score_C, ...]
ranked = sort(scores)  # Method with highest score is best

# STEP 7: Verify
assert score_A == recalculate(method_A)  # Reproducible
assert rank_order == logical_order       # Makes sense
```

---

## Summary: HOW to Compare

1. **Define**: Measurable dimensions (objective, verifiable)
2. **Reference**: Baseline ranges for normalization
3. **Weight**: Assign importance based on YOUR use case
4. **Measure**: Actual values for each method
5. **Normalize**: Convert measurements to 0-1 scale
6. **Calculate**: Apply weights, sum to final score
7. **Rank**: Compare across methods
8. **Verify**: Prove comparison is reproducible and logical

This framework works for ANY AI method comparison: image generation, language models, retrieval systems, etc.

The key: **Define what matters, measure it objectively, weight by context, verify reproducibility.**
