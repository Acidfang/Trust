"""
INTEGRATION GUIDE - How to Use Weighted Container System in Your Project

This guide shows practical examples for integrating the system into:
  - Animation pipelines
  - State management
  - Effect composition
  - Decision automation

All examples are runnable code.
"""

# ============================================================================
# EXAMPLE 1: ANIMATION EFFECT PIPELINE
# ============================================================================

"""
USE CASE: Automate animation effect selection

Scenario:
  - UI element needs to appear
  - Different animations available
  - Some work better with others
  - Need to pick the best combination

Solution: Let the weighted container system decide!
"""

from weighted_container_system import (
    WeightedItem, ContainerManager, QueryEngine, 
    ScoringEngine, FeasibilityValidator, CompositionAnalyzer
)


def setup_animation_system() -> tuple:
    """Setup animation effect system."""
    
    manager = ContainerManager()
    
    # Create animation effect container
    animations = manager.create_container(
        "animations",
        "Animation Effects",
        "animation"
    )
    
    # Define animation effects
    
    # Entrance effects (positive: good for first appearance)
    fade_in = WeightedItem(
        item_id="anim_fade_in",
        name="Fade In",
        category="entrance",
        weight=0.9,  # Very positive for appearing
        properties={"duration": 0.3, "easing": "ease_in"},
        compatibility_tags={"entrance", "smooth", "subtle"}
    )
    
    slide_in = WeightedItem(
        item_id="anim_slide_in",
        name="Slide In",
        category="entrance",
        weight=0.8,
        properties={"duration": 0.4, "direction": "left"},
        compatibility_tags={"entrance", "dynamic", "attention"}
    )
    
    bounce_in = WeightedItem(
        item_id="anim_bounce_in",
        name="Bounce In",
        category="entrance",
        weight=0.7,  # Good but maybe too much
        properties={"duration": 0.5, "strength": "medium"},
        compatibility_tags={"entrance", "playful", "attention"}
    )
    
    # Enhancement effects (positive: amplify appearance)
    glow_up = WeightedItem(
        item_id="anim_glow",
        name="Glow Up",
        category="enhancement",
        weight=0.6,
        properties={"intensity": 0.8, "color": "gold"},
        compatibility_tags={"enhancement", "emphasis", "entrance"}
    )
    
    scale_up = WeightedItem(
        item_id="anim_scale",
        name="Scale Up",
        category="enhancement",
        weight=0.5,
        properties={"from": 0.8, "to": 1.0},
        compatibility_tags={"enhancement", "dynamic", "entrance"}
    )
    
    # Interaction effects (positive: respond to user)
    hover_glow = WeightedItem(
        item_id="anim_hover",
        name="Hover Glow",
        category="interaction",
        weight=0.4,
        properties={"trigger": "hover", "intensity": "low"},
        compatibility_tags={"interaction", "feedback", "subtle"}
    )
    
    # Negative effects (should avoid)
    shake = WeightedItem(
        item_id="anim_shake",
        name="Shake",
        category="distraction",
        weight=-0.5,  # Negative: annoying
        properties={"intensity": "high"},
        compatibility_tags={"distraction", "warning"}
    )
    
    # Add to container
    for effect in [fade_in, slide_in, bounce_in, glow_up, scale_up, hover_glow, shake]:
        animations.add_item(effect)
    
    # Setup subsystems
    query = QueryEngine(manager)
    scorer = ScoringEngine()
    validator = FeasibilityValidator(manager, scorer)
    analyzer = CompositionAnalyzer(manager, query, scorer, validator)
    
    return manager, animations, query, scorer, validator, analyzer


def recommend_animation(use_case: str):
    """
    Example: Get recommended animation for a use case.
    
    Args:
        use_case: "appearance", "emphasis", "feedback"
    """
    
    manager, animations, query, scorer, validator, analyzer = setup_animation_system()
    
    print(f"\n{'='*60}")
    print(f"ANIMATION RECOMMENDATION: {use_case.upper()}")
    print('='*60)
    
    if use_case == "appearance":
        print("\nFinding smooth entrance animations...")
        
        # Find entrance effects
        entrances = query.find_by_category("entrance")
        print(f"✓ Found {len(entrances)} entrance effects")
        
        # Find smooth (not too aggressive)
        smooth = query.find_by_weight_range(min_weight=0.7)
        print(f"✓ Found {len(smooth)} smooth effects (weight >= 0.7)")
        
        # Find best smooth entrance
        from weighted_container_system import WeightedItem
        entrance_items = [item for _, item in entrances]
        smooth_items = [item for _, item in smooth]
        
        best = None
        best_score = -999
        
        for item in entrance_items:
            if item in smooth_items:
                score = item.weight
                if score > best_score:
                    best_score = score
                    best = item
        
        print(f"\n✓ RECOMMENDED: {best.name}")
        print(f"  Weight: {best_score:+.1f}")
        print(f"  Tags: {', '.join(list(best.compatibility_tags)[:3])}")
    
    elif use_case == "emphasis":
        print("\nFinding emphasis combinations...")
        
        # Find good effects to combine
        high_value = query.find_by_weight_range(min_weight=0.6)
        print(f"✓ Found {len(high_value)} high-value effects")
        
        # Get best combination
        best_combos = analyzer.find_best_combinations(max_combinations=3)
        
        if best_combos:
            combo = best_combos[0]
            print(f"\n✓ RECOMMENDED COMBINATION:")
            print(f"  Score: {combo['score']:+.2f}")
            for item_name in combo['items']:
                print(f"  - {item_name}")
    
    elif use_case == "feedback":
        print("\nFinding interaction feedback effects...")
        
        # Find interaction effects
        interactions = query.find_by_category("interaction")
        print(f"✓ Found {len(interactions)} interaction effects")
        
        if interactions:
            _, item = interactions[0]
            print(f"\n✓ RECOMMENDED: {item.name}")
            print(f"  Weight: {item.weight:+.1f}")


# Run recommendation examples
if __name__ == "__main__":
    
    print("\n" + "="*80)
    print("ANIMATION EFFECT PIPELINE EXAMPLE")
    print("="*80)
    
    recommend_animation("appearance")
    recommend_animation("emphasis")
    recommend_animation("feedback")
    
    print("\n" + "="*80)
    print("RESULT: Animation system ready for automation ✓")
    print("="*80)


# ============================================================================
# EXAMPLE 2: STATE-BASED VISUAL FEEDBACK
# ============================================================================

"""
USE CASE: Select visual indicator for application state

Scenario:
  - App can be in states: loading, success, error, warning
  - Each state needs visual indicator
  - Indicators have effects + colors + animations
  - Find best combination for each state
"""


def setup_state_indicator_system():
    """Setup state indicator system."""
    
    manager = ContainerManager()
    
    # Container for states
    states = manager.create_container("states", "App States", "state")
    
    # Define states with weights
    idle = WeightedItem("state_idle", "Idle", "state", weight=0.0, 
                       compatibility_tags={"neutral", "ready"})
    loading = WeightedItem("state_loading", "Loading", "state", weight=0.3,
                          compatibility_tags={"progress", "active"})
    success = WeightedItem("state_success", "Success", "state", weight=0.9,
                          compatibility_tags={"positive", "complete"})
    error = WeightedItem("state_error", "Error", "state", weight=-0.8,
                        compatibility_tags={"negative", "alert"})
    
    states.add_item(idle)
    states.add_item(loading)
    states.add_item(success)
    states.add_item(error)
    
    # Container for indicators
    indicators = manager.create_container("indicators", "Indicators", "indicator")
    
    spinner = WeightedItem("ind_spinner", "Spinner", "indicator", weight=0.5,
                          compatibility_tags={"progress", "active"})
    checkmark = WeightedItem("ind_checkmark", "Checkmark", "indicator", weight=0.9,
                            compatibility_tags={"positive", "complete"})
    xmark = WeightedItem("ind_xmark", "X Mark", "indicator", weight=-0.8,
                        compatibility_tags={"negative", "alert"})
    pulse = WeightedItem("ind_pulse", "Pulse", "indicator", weight=0.6,
                        compatibility_tags={"progress", "active"})
    
    indicators.add_item(spinner)
    indicators.add_item(checkmark)
    indicators.add_item(xmark)
    indicators.add_item(pulse)
    
    # Container for colors
    colors = manager.create_container("colors", "Colors", "color")
    
    gray = WeightedItem("col_gray", "Gray", "color", weight=0.1,
                       compatibility_tags={"neutral"})
    blue = WeightedItem("col_blue", "Blue", "color", weight=0.5,
                       compatibility_tags={"progress", "neutral"})
    green = WeightedItem("col_green", "Green", "color", weight=0.9,
                        compatibility_tags={"positive", "success"})
    red = WeightedItem("col_red", "Red", "color", weight=-0.8,
                      compatibility_tags={"negative", "error"})
    yellow = WeightedItem("col_yellow", "Yellow", "color", weight=0.3,
                         compatibility_tags={"warning", "alert"})
    
    colors.add_item(gray)
    colors.add_item(blue)
    colors.add_item(green)
    colors.add_item(red)
    colors.add_item(yellow)
    
    # Setup subsystems
    query = QueryEngine(manager)
    scorer = ScoringEngine()
    validator = FeasibilityValidator(manager, scorer)
    analyzer = CompositionAnalyzer(manager, query, scorer, validator)
    
    return manager, states, indicators, colors, query, scorer, validator, analyzer


def get_indicator_for_state(state_name: str):
    """Get best indicator combination for application state."""
    
    manager, states, indicators, colors, query, scorer, validator, analyzer = \
        setup_state_indicator_system()
    
    # Find the state
    state_items = [item for _, item in query.find_by_name(state_name, "states")]
    
    if not state_items:
        print(f"✗ State '{state_name}' not found")
        return
    
    state = state_items[0]
    print(f"\n{'='*60}")
    print(f"State: {state.name} (weight={state.weight:+.1f})")
    print('='*60)
    
    # Find matching indicators by tag
    state_tags = state.compatibility_tags
    all_indicators = [item for _, item in query.find_item_across_containers(
        lambda i: i.category == "indicator"
    )]
    
    print(f"\nMatching indicators for tags {state_tags}:")
    
    # Score each indicator with the state
    scored = []
    for indicator in all_indicators:
        score = scorer.score_pair(state, indicator)
        scored.append((indicator, score))
        print(f"  - {indicator.name}: {score['total_score']:+.2f}")
    
    # Find best
    best_indicator = max(scored, key=lambda x: x[1]['total_score'])[0]
    
    # Find matching color
    color_tags = state.compatibility_tags
    all_colors = [item for _, item in query.find_item_across_containers(
        lambda i: i.category == "color"
    )]
    
    print(f"\nMatching colors for tags {color_tags}:")
    
    scored_colors = []
    for color in all_colors:
        score = scorer.score_pair(state, color)
        scored_colors.append((color, score))
        print(f"  - {color.name}: {score['total_score']:+.2f}")
    
    best_color = max(scored_colors, key=lambda x: x[1]['total_score'])[0]
    
    # Final recommendation
    final_combo_score = scorer.score_combination([state, best_indicator, best_color])
    
    print(f"\n{'RECOMMENDATION':=^60}")
    print(f"Indicator: {best_indicator.name}")
    print(f"Color: {best_color.name}")
    print(f"Combined Score: {final_combo_score['total_score']:+.2f}")
    print(f"Overall: {'✓ POSITIVE' if final_combo_score['is_positive'] else '✗ NEGATIVE'}")
    print('='*60)


# Run examples
if __name__ == "__main__":
    
    print("\n" + "="*80)
    print("STATE-BASED INDICATOR EXAMPLE")
    print("="*80)
    
    get_indicator_for_state("Loading")
    get_indicator_for_state("Success")
    get_indicator_for_state("Error")


# ============================================================================
# EXAMPLE 3: COMPOSITE ELEMENT FEASIBILITY
# ============================================================================

"""
USE CASE: Check if composite UI element design is feasible

Scenario:
  - Designing complex UI element
  - Multiple sub-components (shadow, border, glow, etc.)
  - Need to verify they work together
  - Want to ensure optimal combination
"""


def check_composite_design():
    """Check if a composite design is feasible."""
    
    manager = ContainerManager()
    
    # Create styling container
    styles = manager.create_container("styles", "Styling Systems", "style")
    
    # Define styling elements
    shadow = WeightedItem("style_shadow", "Box Shadow", "style", weight=0.6,
                         compatibility_tags={"depth", "detail"})
    border = WeightedItem("style_border", "Border", "style", weight=0.5,
                         compatibility_tags={"definition", "clarity"})
    glow = WeightedItem("style_glow", "Inner Glow", "style", weight=0.7,
                       compatibility_tags={"luminosity", "depth"})
    high_contrast = WeightedItem("style_contrast", "High Contrast", "style", 
                                weight=0.8, compatibility_tags={"clarity"})
    blur = WeightedItem("style_blur", "Blur", "style", weight=-0.3,
                       compatibility_tags={"reduction"})
    
    for item in [shadow, border, glow, high_contrast, blur]:
        styles.add_item(item)
    
    # Setup
    query = QueryEngine(manager)
    scorer = ScoringEngine()
    validator = FeasibilityValidator(manager, scorer)
    
    # Test design 1: Good composition
    design1 = [shadow, border, glow, high_contrast]
    
    print(f"\n{'='*60}")
    print("COMPOSITE DESIGN FEASIBILITY CHECK")
    print('='*60)
    
    print(f"\nDesign 1: Shadow + Border + Glow + High Contrast")
    
    feasibility1 = validator.check_combination_feasibility(design1)
    score1 = scorer.score_combination(design1)
    
    print(f"  Items: {len(design1)}")
    print(f"  Sum weights: {score1['sum_weights']:+.2f}")
    print(f"  Synergy: {score1['synergy_bonus']:+.2f}")
    print(f"  Total score: {score1['total_score']:+.2f}")
    print(f"  Constraint violations: {score1['constraint_violations']}")
    print(f"  Status: {'✓ FEASIBLE' if feasibility1['feasible'] else '✗ NOT FEASIBLE'}")
    
    # Test design 2: With blur (problematic)
    design2 = [shadow, blur, border]
    
    print(f"\nDesign 2: Shadow + Blur + Border")
    
    feasibility2 = validator.check_combination_feasibility(design2)
    score2 = scorer.score_combination(design2)
    
    print(f"  Items: {len(design2)}")
    print(f"  Sum weights: {score2['sum_weights']:+.2f}")
    print(f"  Synergy: {score2['synergy_bonus']:+.2f}")
    print(f"  Total score: {score2['total_score']:+.2f}")
    print(f"  Status: {'✓ FEASIBLE' if feasibility2['feasible'] else '✗ NOT FEASIBLE'}")
    
    # Recommendation
    print(f"\n{'RECOMMENDATION':=^60}")
    if feasibility1['feasible'] and feasibility1['is_positive']:
        print("✓ Design 1 is recommended (score={:+.2f})".format(score1['total_score']))
    if feasibility2['feasible']:
        print("✓ Design 2 is also feasible")
    else:
        print("✗ Design 2 has issues - reconsider blur element")
    
    print('='*60)


if __name__ == "__main__":
    
    print("\n" + "="*80)
    print("COMPOSITE ELEMENT FEASIBILITY CHECK")
    print("="*80)
    
    check_composite_design()


# ============================================================================
# SUMMARY - INTEGRATION CHECKLIST
# ============================================================================

"""
INTEGRATION CHECKLIST:

For Animation Pipeline:
  ☐ Create "animations" container
  ☐ Define animation effects with weights
  ☐ Add compatibility tags
  ☐ Use QueryEngine to find by category
  ☐ Use ScoringEngine to rank combinations
  ☐ Use CompositionAnalyzer for automation

For State-Based UI:
  ☐ Create "states" container
  ☐ Create "indicators" container
  ☐ Create "colors" container
  ☐ Define state/indicator/color combinations
  ☐ Use QueryEngine to filter by state tags
  ☐ Use ScoringEngine to find best visual combo
  ☐ Use validator to ensure consistency

For Composite Design:
  ☐ Create container for styling elements
  ☐ Define each element with weight
  ☐ Set compatibility constraints
  ☐ Use validator to pre-flight check
  ☐ Report issues before implementation

General Best Practices:
  ☐ Weight ranges: positive for good, negative for bad
  ☐ Use tags for logical grouping
  ☐ Set constraints for hard rules
  ☐ Always validate before deployment
  ☐ Use analyzer to find optimal combinations
  ☐ Generate explanations for decisions

Available Resources:
  ✓ weighted_container_system.py - Core implementation
  ✓ WEIGHTED_CONTAINER_USER_GUIDE.md - API reference
  ✓ FEASIBILITY_ANALYSIS_COMPLETE.md - Technical analysis
  ✓ INTEGRATION_EXAMPLES.md - This file
"""
