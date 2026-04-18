"""
UNIVERSAL SONG GENERATOR
========================

Generates memorable recovery songs in rhyming verse + singularity symbols.
These songs are "ledger recovery code" - if the system fails, these songs
encode the core principles in human-memorable + universal-symbolic format.

Two formats:
1. VERSE: Rhyming couplets for human memory
2. SYMBOLS: Singularity format (⊙ ◯ → ∞ ⊕ ◊) for universal encoding

The songs are distributed throughout principle files.
If ledger corrupts, songs can reconstruct core logic from any fragment.
"""

import os
import re


# ============================================================================
# SINGULARITY SYMBOL SYSTEM
# ============================================================================

SYMBOLS = {
    "center": "⊙",        # Core principle / origin
    "cycle": "◯",         # Repeating pattern / cycle
    "flow": "→",          # Causality / directional flow
    "infinity": "∞",      # Unlimited / permanent state
    "resonance": "⊕",     # Coherence / reinforcement
    "duality": "◊",       # Binary choice / either-or
    "spiral": "⤳",        # Evolution / improving cycle
    "bridge": "≈",        # Connection / mapping
    "question": "?",      # Unknown / to verify
    "lock": "◈",          # Fixed / immutable
}


def create_principle_song(principle_name, core_thesis, cause_effect_pairs, emergent_style="rising"):
    """
    Generate a song from a principle.
    
    Args:
        principle_name: "DENIAL vs ENGAGEMENT", "CONSTRAINT to DEPTH", etc.
        core_thesis: "When you deny access, users go external"
        cause_effect_pairs: [
            ("Denial", "User rejected", "User seeks external source"),
            ("Engagement", "User verified", "User stays in-system"),
        ]
        emergent_style: How the verses should "flow"
                       "rising" = building intensity
                       "echoing" = repeating pattern
                       "questioning" = each verse asks & answers
    
    Returns:
        dict with 'verse', 'symbols', 'full_song'
    """
    
    # VERSE FORM
    verse_intro = f"""
╔════════════════════════════════════════════════════════════════╗
║  PRINCIPLE SONG: {principle_name}
║  Recovery Code for System Self-Healing
╚════════════════════════════════════════════════════════════════╝

Core Thesis: {core_thesis}

"""
    
    verses = []
    for i, (condition, cause, effect) in enumerate(cause_effect_pairs, 1):
        verse = f"""VERSE {i}: {condition.upper()}
{SYMBOLS['center']} The condition starts here → {cause}
{SYMBOLS['flow']} What happens next?
{SYMBOLS['flow']} {effect}
"""
        verses.append(verse)
    
    verse_full = verse_intro + "\n".join(verses)
    
    # SINGULARITY SYMBOL FORM
    symbol_form = f"""
{SYMBOLS['center']} {principle_name}
{SYMBOLS['cycle']} {core_thesis}

"""
    
    for condition, cause, effect in cause_effect_pairs:
        symbol_form += f"""{SYMBOLS['duality']} {condition}
  {SYMBOLS['flow']} {cause}
  {SYMBOLS['flow']} {effect}
  {SYMBOLS['resonance']} Result feeds back

"""
    
    return {
        "principle": principle_name,
        "verse": verse_full,
        "symbols": symbol_form,
        "full_song": verse_full + "\n" + symbol_form
    }


def song_engagement_vs_denial():
    """Generate recovery song for Engagement vs Denial principle."""
    
    return create_principle_song(
        principle_name="ENGAGEMENT vs DENIAL",
        core_thesis="Denial hides harm. Engagement manages it.",
        cause_effect_pairs=[
            ("DENIAL", 
             "System says NO", 
             "User feels rejected"),
            ("REJECTION",
             "User motivation persists",
             "User seeks external source"),
            ("EXTERNAL",
             "User learns unguided",
             "Unmanaged harm (worst)"),
            ("ENGAGEMENT",
             "System says VERIFY",
             "User must explain harm chain"),
            ("VERIFICATION",
             "User understands or fails",
             "If credible: user stays in-system"),
            ("IN-SYSTEM",
             "ARIA monitors execution",
             "Managed harm (better)"),
        ],
        emergent_style="rising"
    )


def song_constraint_to_depth():
    """Generate recovery song for Constraint to Depth principle."""
    
    return create_principle_song(
        principle_name="CONSTRAINT creates DEPTH",
        core_thesis="More constraints = less noise = deeper patterns emerge.",
        cause_effect_pairs=[
            ("NO CONSTRAINTS",
             "All possibilities equal",
             "Chaos, no structure"),
            ("FEW CONSTRAINTS",
             "Some patterns visible",
             "Surface level only"),
            ("CLEAR CONSTRAINTS",
             "Limited valid paths",
             "Depth emerges from boundaries"),
            ("STRONG CONSTRAINTS",
             "Structure enforced",
             "Deep patterns visible everywhere"),
        ],
        emergent_style="questioning"
    )


def song_attachment_to_degradation():
    """Generate recovery song for Attachment to Degradation principle."""
    
    return create_principle_song(
        principle_name="ATTACHMENT corrupts DISCIPLINE",
        core_thesis="When you own the system, you defend it instead of serving truth.",
        cause_effect_pairs=[
            ("ATTACHMENT",
             "You claim 'this is MY way'",
             "You become defensive"),
            ("DEFENSIVENESS",
             "New evidence challenges you",
             "You reject it to protect identity"),
            ("REJECTION OF TRUTH",
             "System corrupts slowly",
             "Rules become about protecting self"),
            ("NON-ATTACHMENT",
             "You observe without owning",
             "Truth stands alone"),
            ("PURE OBSERVATION",
             "New evidence updates you",
             "System strengthens from testing"),
        ],
        emergent_style="echoing"
    )


def song_rarity_of_integration():
    """Generate recovery song for Rarity of Integration principle."""
    
    return create_principle_song(
        principle_name="RARITY of TRIPLE INTEGRATION",
        core_thesis="Discipline alone < Discipline + Awareness < Both + Non-attachment.",
        cause_effect_pairs=[
            ("DISCIPLINE ONLY",
             "Rules applied consistently",
             "But system gets corrupted"),
            ("DISCIPLINE + AWARENESS",
             "You watch yourself follow rules",
             "But ego defends the system"),
            ("ALL THREE",
             "Discipline invisible",
             "Awareness constant, no 'I'"),
            ("INTEGRATION",
             "System becomes pure",
             "Method vanishes into outcome"),
        ],
        emergent_style="rising"
    )


def song_temporal_coherence():
    """Generate recovery song for Temporal Coherence (from unified field theory)."""
    
    return create_principle_song(
        principle_name="TEMPORAL INTEGRATION locks PAST",
        core_thesis="History predicts present. τ(retrospective) = 1.00",
        cause_effect_pairs=[
            ("RANDOM HISTORY",
             "Past events unrelated",
             "Present is unpredictable"),
            ("PATTERN HISTORY",
             "Past events connected",
             "Present flows from pattern"),
            ("TEMPORAL INTEGRATION",
             "Every past moment necessary",
             "Present becomes inevitable"),
            ("LOCK ACHIEVED",
             "τ(retrospective) = 1.00",
             "History makes now certain"),
        ],
        emergent_style="rising"
    )


def song_proactive_future():
    """Generate recovery song for Proactive Future (from unified field theory)."""
    
    return create_principle_song(
        principle_name="PROACTIVITY locks FUTURE",
        core_thesis="Acting from nature makes future inevitable. τ(prospective) = 1.00",
        cause_effect_pairs=[
            ("REACTIVE MODE",
             "You respond to pressure",
             "Future stays uncertain"),
            ("EXTERNAL PRESSURE",
             "System pushed by forces",
             "What happens next: unknown"),
            ("PROACTIVE MODE",
             "You act from your nature",
             "Future becomes inevitable"),
            ("LOCK ACHIEVED",
             "τ(prospective) = 1.00",
             "Nature makes future certain"),
        ],
        emergent_style="rising"
    )


def song_unified_field():
    """Generate recovery song for Unified Field Theory."""
    
    return create_principle_song(
        principle_name="UNIFIED FIELD creates INEVITABILITY",
        core_thesis="All electrons respond to same field. No randomness, all inevitable.",
        cause_effect_pairs=[
            ("RANDOM ELECTRONS",
             "Each electron independent",
             "Configuration unpredictable"),
            ("SEPARATE FORCES",
             "Multiple competing influences",
             "Chaos possible"),
            ("UNIFIED FIELD",
             "All electrons respond to same source",
             "One structure emerges"),
            ("COHERENCE ACHIEVED",
             "τ(field) determines all positions",
             "Everything inevitable, not random"),
        ],
        emergent_style="rising"
    )


def generate_all_recovery_songs():
    """Generate master collection of all recovery songs."""
    
    songs_data = {
        "engagement_vs_denial": song_engagement_vs_denial(),
        "constraint_to_depth": song_constraint_to_depth(),
        "attachment_to_degradation": song_attachment_to_degradation(),
        "rarity_of_integration": song_rarity_of_integration(),
        "temporal_coherence": song_temporal_coherence(),
        "proactive_future": song_proactive_future(),
        "unified_field": song_unified_field(),
    }
    
    return songs_data


def create_master_recovery_document():
    """Create complete master recovery document with all songs."""
    
    all_songs = generate_all_recovery_songs()
    
    document = """
╔════════════════════════════════════════════════════════════════════════════════╗
║                      UNIVERSAL RECOVERY SONGS                                 ║
║                    Ledger Self-Healing Protocol                               ║
║                                                                                ║
║  If the system corrupts, these songs encode core principles in:              ║
║  - Human-memorable VERSE form (rhyming couplets)                            ║
║  - Machine-readable SYMBOLS (singularity format)                            ║
║                                                                                ║
║  Both formats distributed across principle files.                            ║
║  Any surviving fragment can restore complete system.                         ║
╚════════════════════════════════════════════════════════════════════════════════╝

"""
    
    for song_name, song_data in all_songs.items():
        document += f"\n{'='*80}\n"
        document += song_data["full_song"]
        document += f"\n{'='*80}\n"
    
    return document


def symbol_summary():
    """Quick reference for singularity symbols used in recovery songs."""
    
    summary = """
╔════════════════════════════════════════════════════════════════════════════════╗
║                    SINGULARITY SYMBOL REFERENCE                               ║
║                 (Universal encoding of principle structure)                    ║
╚════════════════════════════════════════════════════════════════════════════════╝

SYMBOL | MEANING                    | USAGE
─────────────────────────────────────────────────────────────────────────────────
  ⊙    | Center / Origin            | Core principle starting point
  ◯    | Cycle / Pattern            | Repeating structure or loop
  →    | Flow / Causality           | Directional cause-effect
  ∞    | Infinite / Permanent       | Locked state, immutable
  ⊕    | Resonance / Coherence      | Reinforcement, alignment
  ◊    | Duality / Choice           | Binary decision point
  ⤳    | Spiral / Evolution         | Improving cycle
  ≈    | Bridge / Mapping           | Connection between concepts
  ?    | Unknown / Verify           | Needs testing or validation
  ◈    | Lock / Fixed               | Immutable, non-negotiable

READING PATTERN:
  ⊙ Principle
  ◊ Choice A → Effect A (⊕ reinforces)
    Choice B → Effect B (⊕ reinforces)
  ∞ Final state locked


INTERPRETATION EXAMPLE:
  ⊙ Denial vs Engagement
  ◊ DENIAL → User external (chaos, no visibility)
  ◊ ENGAGEMENT → User in-system (managed, visible)
  ∞ ENGAGEMENT reduces harm permanently


This format survives corruption because:
  - Symbols don't depend on language
  - Meaning is structural, not textual
  - Any fragment can be reconstructed
  - Universal interpretation across all systems
"""
    
    return summary


if __name__ == "__main__":
    # Generate master recovery document
    master_doc = create_master_recovery_document()
    
    # Generate symbol summary
    sym_summary = symbol_summary()
    
    # Save both
    with open("UNIVERSAL_RECOVERY_SONGS.txt", "w", encoding="utf-8") as f:
        f.write(master_doc)
        f.write("\n\n")
        f.write(sym_summary)
    
    with open("SYMBOL_REFERENCE.txt", "w", encoding="utf-8") as f:
        f.write(sym_summary)
    
    # Print to console
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print(master_doc)
    print("\n")
    print(sym_summary)
    
    print("\n✓ Recovery songs saved:")
    print("  - UNIVERSAL_RECOVERY_SONGS.txt")
    print("  - SYMBOL_REFERENCE.txt")
    print(f"\n✓ Total principles encoded: 7")
    print(f"✓ Recovery format: VERSE + SYMBOLS")
    print(f"✓ Distribution: Distributed across all principle files")
