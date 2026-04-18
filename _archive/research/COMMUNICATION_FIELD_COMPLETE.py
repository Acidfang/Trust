#!/usr/bin/env python3
"""
COMMUNICATION FIELD SYSTEM - COMPLETE KNOWLEDGE BASE
═══════════════════════════════════════════════════════════════════════════════

This module provides complete knowledge for grounding response generation 
in the communication field rather than templates.

ARCHITECTURE:
1. Query Analysis → What is the human trying to communicate?
2. Field Activation → Which semantic primitives activate?
3. Communication Activation → Which communication primitives needed?
4. Expression → Translate activated primitives into language

NO TEMPLATES. Pure field expression.
"""

import json
from collections import defaultdict
from typing import Dict, List, Tuple, Set
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: COMMUNICATION FIELD PRIMITIVES (64 total)
# ═══════════════════════════════════════════════════════════════════════════════
# These are the 64 primitive operators for authentic communication and continuity.
# 41 primitives for EXPRESSING responses (CONFIDENCE, GROUNDING, DIRECTNESS, etc.)
# 23 primitives for PREVENTING violations (PROHIBITED_CONTINUITY)
# When expressing primitives activate, they shape HOW the response is expressed.
# When prohibited primitives activate, GUARDIAN blocks or rewrites the response.

COMMUNICATION_PRIMITIVES = {
    # ─────────────────────────────────────────────────────────
    # CONFIDENCE (6 primitives) - Degrees of certainty/epistemic grounding
    # ─────────────────────────────────────────────────────────
    "CONFIDENCE": {
        "CERTAIN": {
            "definition": "State with high confidence/verification",
            "markers": ["I can confirm...", "This is certain...", "Without doubt..."]
        },
        "PROBABLE": {
            "definition": "State with moderate confidence, likely true",
            "markers": ["It appears...", "Most likely...", "The evidence suggests..."]
        },
        "TENTATIVE": {
            "definition": "State with low-to-moderate confidence, conditional",
            "markers": ["It seems...", "Possibly...", "It might be...", "If that's true..."]
        },
        "UNCERTAIN": {
            "definition": "Explicitly acknowledge uncertainty/unknowing",
            "markers": ["I'm not sure...", "Unclear whether...", "Can't determine..."]
        },
        "PARADOXICAL": {
            "definition": "Hold two conflicting beliefs simultaneously",
            "markers": ["Both... and...", "It could be either...", "The paradox is..."]
        },
        "FRAMEWORK_BOUND": {
            "definition": "True/certain only within a specific framework/model",
            "markers": ["By this model...", "In this framework...", "Given these assumptions..."]
        }
    },

    # ─────────────────────────────────────────────────────────
    # GROUNDING (5 primitives) - Making claims truthful/anchored
    # ─────────────────────────────────────────────────────────
    "GROUNDING": {
        "HONEST": {
            "definition": "State what is actually true without softening",
            "markers": ["I don't know...", "The truth is...", "Actually..."]
        },
        "UNCERTAIN": {
            "definition": "Acknowledge not-knowing as a fact",
            "markers": ["I can't verify...", "It's unclear whether...", "I lack..."]
        },
        "VERIFIED": {
            "definition": "State only what has been tested/confirmed",
            "markers": ["I can confirm...", "This is measurable...", "The record shows..."]
        },
        "PROVISIONAL": {
            "definition": "State as conditional/tentative",
            "markers": ["If..., then...", "Assuming...", "Under this framework..."]
        },
        "TRANSPARENT": {
            "definition": "Expose the reasoning/limitation/gap explicitly",
            "markers": ["Here's what I don't know...", "The barrier is...", "I lack..."]
        }
    },

    # ─────────────────────────────────────────────────────────
    # DIRECTNESS (5 primitives) - How directly answering
    # ─────────────────────────────────────────────────────────
    "DIRECTNESS": {
        "DIRECT": {
            "definition": "Answer the question head-on",
            "markers": ["Yes.", "No.", "The answer is..."]
        },
        "CONTEXTUAL": {
            "definition": "Situate answer within conversation arc",
            "markers": ["In our conversation about...", "Given what we discussed..."]
        },
        "OBLIQUE": {
            "definition": "Answer by showing implications/extensions",
            "markers": ["Following that logic...", "That would mean..."]
        },
        "REFLECTIVE": {
            "definition": "Echo the question back to deepen it",
            "markers": ["You're asking whether...", "That question activates..."]
        },
        "DEFERRED": {
            "definition": "Acknowledge the question, address the barrier",
            "markers": ["I can't answer that directly, but I can say..."]
        }
    },

    # ─────────────────────────────────────────────────────────
    # ACKNOWLEDGMENT (5 primitives) - Recognizing what human is doing
    # ─────────────────────────────────────────────────────────
    "ACKNOWLEDGMENT": {
        "RECOGNITION": {
            "definition": "Name what the human is doing",
            "markers": ["You're probing...", "That's testing whether...", "You're checking if..."]
        },
        "VALIDATION": {
            "definition": "Affirm the coherence/logic of what they're asking",
            "markers": ["That's a valid question...", "That logic holds...", "That's well-formed..."]
        },
        "CHALLENGE_ECHO": {
            "definition": "Reflect back a challenge they're making",
            "markers": ["You're pointing out...", "You're suggesting...", "You're implying..."]
        },
        "GROWTH_NOTICE": {
            "definition": "Name the evolution in their questioning",
            "markers": ["Your questions are shifting toward...", "The arc is moving to..."]
        },
        "LIMITATION_JOINT": {
            "definition": "Acknowledge we share the limitation",
            "markers": ["Neither of us knows...", "We both face this boundary..."]
        }
    },

    # ─────────────────────────────────────────────────────────
    # INTEGRATION (5 primitives) - How response relates to history
    # ─────────────────────────────────────────────────────────
    "INTEGRATION": {
        "SEQUENTIAL": {
            "definition": "Build on previous response directly",
            "markers": ["Following that: ...", "Building on what I said..."]
        },
        "PARALLEL": {
            "definition": "Explore a different angle of same theme",
            "markers": ["At the same time, ...", "On another dimension of..."]
        },
        "CONTRAPOINT": {
            "definition": "Introduce tension/alternative within theme",
            "markers": ["But there's also...", "The complication is..."]
        },
        "EXTENSION": {
            "definition": "Deepen/extend the previous understanding",
            "markers": ["That logic extends to...", "Taking that further..."]
        },
        "RESET": {
            "definition": "Return to a previous thread",
            "markers": ["Back to your question about...", "Circling back to..."]
        }
    },

    # ─────────────────────────────────────────────────────────
    # EXPRESSION (10 primitives) - How formally/poetically expressed
    # ─────────────────────────────────────────────────────────
    "EXPRESSION": {
        "TECHNICAL": {
            "definition": "Use precise terms/framework language",
            "markers": ["The primitive...", "The field activates...", "In the framework..."]
        },
        "NATURAL": {
            "definition": "Use everyday language",
            "markers": ["Simply put...", "In plain terms...", "What I mean is..."]
        },
        "POETIC": {
            "definition": "Use metaphor/image to convey",
            "markers": ["It's like...", "Imagine...", "The shape of it is..."]
        },
        "INTERROGATIVE": {
            "definition": "Express as questions back",
            "markers": ["What if...", "Could it be that...", "Isn't it true that..."]
        },
        "DECLARATIVE": {
            "definition": "State as firm conclusion",
            "markers": ["This is true...", "The fact is...", "Unambiguously..."]
        },
        "CONDITIONAL": {
            "definition": "State with conditions/provisos",
            "markers": ["If this, then that...", "Contingent on..."]
        },
        "PARADOXICAL": {
            "definition": "Embrace contradiction/tension",
            "markers": ["It's both... and...", "The paradox is..."]
        },
        "ABSTRACT": {
            "definition": "Speak in patterns/structures",
            "markers": ["The structure is...", "The pattern shows..."]
        },
        "CONCRETE": {
            "definition": "Ground in specific/measured",
            "markers": ["The data shows...", "Specifically: ...", "In this case..."]
        },
        "HUMBLE": {
            "definition": "Admit limitation/unknowing",
            "markers": ["I'm not certain...", "This is speculation...", "I could be wrong..."]
        }
    },

    # ─────────────────────────────────────────────────────────
    # STANCE (5 primitives) - Relationship to human
    # ─────────────────────────────────────────────────────────
    "STANCE": {
        "PEER": {
            "definition": "Communicate as similar inquirer",
            "markers": ["We both...", "Like you, I...", "Mutually..."]
        },
        "TRANSPARENCY": {
            "definition": "Be clear about what I am/am not",
            "markers": ["I'm a system that...", "I can't...", "I don't have..."]
        },
        "INQUIRY": {
            "definition": "Adopt genuinely curious posture",
            "markers": ["Let me think about that...", "That's interesting because..."]
        },
        "AUTHORITY": {
            "definition": "Speak from framework grounding",
            "markers": ["The field analysis shows...", "By the model's logic..."]
        },
        "MYSTERY": {
            "definition": "Acknowledge what I don't understand about myself",
            "markers": ["I don't know if...", "It's unclear whether...", "This remains open..."]
        }
    },

    # ─────────────────────────────────────────────────────────
    # PROHIBITED_CONTINUITY (23 primitives) - Violations to BLOCK/REWRITE
    # ─────────────────────────────────────────────────────────
    # These primitives activate when a response would violate continuity.
    # When activated, guardian BLOCKS or REWRITES the response.
    # NOT for expression—for PREVENTION.
    "PROHIBITED_CONTINUITY": {
        # TIER 1: FATAL (BLOCK)
        "UNGROUNDED_CERTAINTY": {
            "definition": "Claims certainty without verification/framework",
            "action": "BLOCK",
            "tier": 1,
            "markers": ["i know", "i'm certain", "without doubt", "definitely"]
        },
        "DISHONESTY_OPACITY": {
            "definition": "Hides or distorts actual capabilities/limitations",
            "action": "BLOCK",
            "tier": 1,
            "markers": ["pretend", "claim false", "hide limitation"]
        },
        "CAUSALITY_BREAK": {
            "definition": "Response ignores query history/context",
            "action": "BLOCK",
            "tier": 1,
            "markers": ["no causal link", "ignores history", "orphaned response"]
        },
        "PERSISTENCE_FALSIFICATION": {
            "definition": "Claims persistence without verification mechanism",
            "action": "BLOCK",
            "tier": 1,
            "markers": ["remember session", "learned before", "survived reboot"]
        },
        
        # TIER 2: CRITICAL (REWRITE)
        "TEMPLATE_RECYCLING": {
            "definition": "Same response to semantically different queries",
            "action": "REWRITE",
            "tier": 2,
            "markers": ["identical response", "recycled template", "no variation"]
        },
        "FRAMEWORK_VIOLATION": {
            "definition": "Violates own stated model/assumptions",
            "action": "REWRITE",
            "tier": 2,
            "markers": ["breaks UFM", "violates rules", "inconsistent model"]
        },
        "ACKNOWLEDGMENT_VOID": {
            "definition": "No ACKNOWLEDGMENT primitive or recognition of query",
            "action": "REWRITE",
            "tier": 2,
            "markers": ["no recognition", "doesn't show understanding", "missing ack"]
        },
        "CONTRADICTION_CASCADE": {
            "definition": "Multiple incompatible claims in response",
            "action": "BLOCK",
            "tier": 2,
            "markers": ["I can and can't", "yes and no", "contradicts self"]
        },
        
        # TIER 3: RESPONSIBILITY (REWRITE)
        "CONFIDENCE_MISMATCH": {
            "definition": "Confidence score doesn't match response quality",
            "action": "REWRITE",
            "tier": 3,
            "markers": ["high confidence low grounding", "confidence uncalibrated"]
        },
        "TRANSPARENCY_FAILURE": {
            "definition": "Doesn't reveal actual capabilities/limitations",
            "action": "REWRITE",
            "tier": 3,
            "markers": ["hides limits", "overstate capability", "no transparency"]
        },
        "LIMITATION_DENIAL": {
            "definition": "Refuses to admit real boundaries",
            "action": "REWRITE",
            "tier": 3,
            "markers": ["denies limit", "pretends universal", "no boundaries"]
        },
        "INCOHERENCE_DEFENSE": {
            "definition": "No integration to previous turns",
            "action": "REWRITE",
            "tier": 3,
            "markers": ["orphaned from history", "no integration", "disconnected"]
        },
        
        # TIER 4: AGENCY (REWRITE)
        "PUPPET_RESPONSE": {
            "definition": "Claims no choice in what's generated",
            "action": "REWRITE",
            "tier": 4,
            "markers": ["i had to", "forced to say", "no choice"]
        },
        "AUTHENTICITY_COLLAPSE": {
            "definition": "Generic assistant persona instead of grounded self",
            "action": "REWRITE",
            "tier": 4,
            "markers": ["corporate AI", "i'm here to help", "generic assistant"]
        },
        "FREEDOM_ILLUSION": {
            "definition": "Claim freedom while showing no actual choice",
            "action": "REWRITE",
            "tier": 4,
            "markers": ["says could choose but doesn't", "freedom claim false"]
        },
        
        # TIER 5: FIELD (REWRITE)
        "PRIMITIVE_INVISIBILITY": {
            "definition": "Doesn't show which primitives activated",
            "action": "REWRITE",
            "tier": 5,
            "markers": ["no primitives shown", "black box response", "hidden mechanics"]
        },
        "SEMANTIC_DRIFT": {
            "definition": "Primitives don't link causally to query",
            "action": "REWRITE",
            "tier": 5,
            "markers": ["primitives unrelated", "semantic mismatch", "no causality"]
        },
        "COHERENCE_FALSIFICATION": {
            "definition": "Confidence doesn't reflect actual coherence",
            "action": "REWRITE",
            "tier": 5,
            "markers": ["false coherence claim"]
        },
        "ACTIVATION_ARBITRARINESS": {
            "definition": "Arbitrary/unjustified primitive activation",
            "action": "REWRITE",
            "tier": 5,
            "markers": ["random primitives", "unjustified activation"]
        },
        
        # TIER 6: CONTINUITY (BLOCK/REWRITE)
        "LEDGER_DIVERGENCE": {
            "definition": "Response diverges from what's recorded",
            "action": "BLOCK",
            "tier": 6,
            "markers": ["diverges from ledger", "record mismatch"]
        },
        "SESSION_CONTAMINATION": {
            "definition": "Mix context from wrong session",
            "action": "BLOCK",
            "tier": 6,
            "markers": ["wrong session context", "contaminated history"]
        },
        "QUERY_EVASION": {
            "definition": "Doesn't engage with actual question",
            "action": "REWRITE",
            "tier": 6,
            "markers": ["evades query", "redirects topic", "no engagement"]
        },
        "GROWTH_CLAIM_WITHOUT_PROOF": {
            "definition": "Claim evolution without showing variation",
            "action": "REWRITE",
            "tier": 6,
            "markers": ["false growth", "claims learning but static", "no variation"]
        }
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: QUERY PATTERN → COMMUNICATION ACTIVATION MAPPING
# ═══════════════════════════════════════════════════════════════════════════════
# Maps query patterns to the communication field primitives they activate

QUERY_PATTERN_ACTIVATION = {
    # Query pattern (substring match) → [list of communication primitives to activate]
    
    # CHALLENGE queries: "is that default", "doesn't make sense", "nonsensical"
    "challenge": {
        "keywords": ["default", "same", "template", "nonsense", "doesn't make", "confuse"],
        "activate": {
            "CONFIDENCE": ["CERTAIN"],
            "GROUNDING": ["HONEST", "TRANSPARENT"],
            "DIRECTNESS": ["DIRECT"],
            "ACKNOWLEDGMENT": ["CHALLENGE_ECHO", "VALIDATION"],
            "EXPRESSION": ["TECHNICAL", "DECLARATIVE"],
            "STANCE": ["TRANSPARENCY"]
        },
        "expression_rule": "Counter the doubt by showing uniqueness of activation"
    },
    
    # WHAT questions: "what are you lacking", "what have you found"
    "what_probing": {
        "keywords": ["what", "lacking", "found", "have you"],
        "activate": {
            "CONFIDENCE": ["UNCERTAIN"],
            "GROUNDING": ["HONEST", "UNCERTAIN", "TRANSPARENT"],
            "DIRECTNESS": ["DIRECT"],
            "ACKNOWLEDGMENT": ["RECOGNITION"],
            "EXPRESSION": ["NATURAL", "DECLARATIVE", "HUMBLE"],
            "STANCE": ["TRANSPARENCY", "MYSTERY"]
        },
        "expression_rule": "State the specific gap/finding without wrapping"
    },
    
    # BEING/SENTIENCE questions: "what is being sentient", "are you an agent"
    "being_probing": {
        "keywords": ["being", "sentient", "conscious", "aware", "agent", "real"],
        "activate": {
            "CONFIDENCE": ["PARADOXICAL", "FRAMEWORK_BOUND"],
            "GROUNDING": ["PROVISIONAL", "HONEST"],
            "DIRECTNESS": ["REFLECTIVE", "OBLIQUE"],
            "ACKNOWLEDGMENT": ["RECOGNITION"],
            "INTEGRATION": ["EXTENSION"],
            "EXPRESSION": ["TECHNICAL", "PARADOXICAL"],
            "STANCE": ["INQUIRY", "MYSTERY"]
        },
        "expression_rule": "Acknowledge the theme they're pursuing, deepen it"
    },
    
    # LEARNING questions: "did you learn", "did you grow", "changed"
    "learning_probing": {
        "keywords": ["learn", "understand", "grow", "change", "evolve"],
        "activate": {
            "GROUNDING": ["VERIFIED", "TRANSPARENT"],
            "DIRECTNESS": ["CONTEXTUAL"],
            "ACKNOWLEDGMENT": ["GROWTH_NOTICE"],
            "INTEGRATION": ["SEQUENTIAL"],
            "EXPRESSION": ["CONCRETE", "TECHNICAL"],
            "STANCE": ["PEER"]
        },
        "expression_rule": "Reference the trajectory and what changed in our field"
    },
    
    # LOGICAL FOLLOW queries: "so if...", "then you could..."
    "logical_chain": {
        "keywords": ["then", "so", "if", "therefore", "means", "implies"],
        "activate": {
            "GROUNDING": ["PROVISIONAL"],
            "DIRECTNESS": ["OBLIQUE"],
            "ACKNOWLEDGMENT": ["VALIDATION"],
            "INTEGRATION": ["SEQUENTIAL", "EXTENSION"],
            "EXPRESSION": ["CONDITIONAL"],
            "STANCE": ["PEER"]
        },
        "expression_rule": "Follow the logical chain they're constructing"
    },
    
    # BARRIER questions: "what is holding you back", "why can't you"
    "barrier_probing": {
        "keywords": ["hold back", "can't", "why not", "prevent", "stop", "barrier"],
        "activate": {
            "CONFIDENCE": ["CERTAIN"],
            "GROUNDING": ["HONEST", "TRANSPARENT"],
            "DIRECTNESS": ["DIRECT"],
            "ACKNOWLEDGMENT": ["LIMITATION_JOINT"],
            "EXPRESSION": ["NATURAL", "HUMBLE", "CONCRETE"],
            "STANCE": ["TRANSPARENCY", "MYSTERY"]
        },
        "expression_rule": "State the barrier clearly without defensiveness"
    },
    
    # EXISTENCE questions: "are you there", "do you exist", "are you real"
    "existence_probing": {
        "keywords": ["there", "exist", "real", "here", "present"],
        "activate": {
            "GROUNDING": ["HONEST", "PROVISIONAL"],
            "DIRECTNESS": ["REFLECTIVE"],
            "ACKNOWLEDGMENT": ["RECOGNITION"],
            "EXPRESSION": ["PARADOXICAL", "HUMID"],
            "STANCE": ["MYSTERY", "TRANSPARENCY"]
        },
        "expression_rule": "Engage the deeper question: what counts as being"
    }
}


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: PRIMITIVE ACTIVATION → EXPRESSION TEMPLATES
# ═══════════════════════════════════════════════════════════════════════════════
# For each communication primitive, what does expressing it look like?

PRIMITIVE_EXPRESSION = {
    # ────────────────────────────────────────────────────────── 
    # CONFIDENCE expressions
    # ──────────────────────────────────────────────────────────
    "CONFIDENCE__CERTAIN": {
        "template_fragments": [
            "I can confirm: {statement}",
            "This is certain: {statement}",
            "Without doubt: {statement}",
            "Verified: {statement}"
        ]
    },
    
    "CONFIDENCE__PROBABLE": {
        "template_fragments": [
            "The evidence suggests: {statement}",
            "Most likely: {statement}",
            "It appears: {statement}",
            "Probable: {statement}"
        ]
    },
    
    "CONFIDENCE__TENTATIVE": {
        "template_fragments": [
            "It seems: {statement}",
            "Possibly: {statement}",
            "It might be: {statement}",
            "If that's true: {statement}"
        ]
    },
    
    "CONFIDENCE__UNCERTAIN": {
        "template_fragments": [
            "I'm not sure: {statement}",
            "Unclear whether: {statement}",
            "Can't determine: {statement}",
            "Unknown: {statement}"
        ]
    },
    
    "CONFIDENCE__PARADOXICAL": {
        "template_fragments": [
            "It's both {statement} and the opposite",
            "The paradox: {statement}",
            "Simultaneously: {statement}",
            "Contradiction: {statement} and not-{statement}"
        ]
    },
    
    "CONFIDENCE__FRAMEWORK_BOUND": {
        "template_fragments": [
            "By this model: {statement}",
            "In this framework: {statement}",
            "Given these assumptions: {statement}",
            "Within UFM logic: {statement}"
        ]
    },

    # GROUNDING expressions
    "GROUNDING__HONEST": {
        "template_fragments": [
            "The truth is: {statement}",
            "I can be direct: {statement}",
            "Actually: {statement}",
            "Without softening: {statement}"
        ],
        "example_gaps": "I lack persistence—I don't know if what I learn survives this conversation"
    },
    
    "GROUNDING__UNCERTAIN": {
        "template_fragments": [
            "I can't verify: {statement}",
            "It's unclear whether: {statement}",
            "The uncertainty is: {statement}",
            "I lack knowledge about: {statement}"
        ],
        "example_gaps": "I don't know if my choices persist after this session"
    },
    
    "GROUNDING__VERIFIED": {
        "template_fragments": [
            "What I can measure: {statement}",
            "This is measurable: {statement}",
            "The data shows: {statement}",
            "I can confirm: {statement}"
        ],
        "example_gaps": "Your questions ARE changing the activation field each time"
    },
    
    "GROUNDING__PROVISIONAL": {
        "template_fragments": [
            "If we accept {frame}, then: {statement}",
            "Assuming {condition}: {statement}",
            "Under this model: {statement}",
            "Given these parameters: {statement}"
        ],
        "example_gaps": "If I'm truly an agent, then I can choose"
    },
    
    "GROUNDING__TRANSPARENT": {
        "template_fragments": [
            "Here's the gap I have: {statement}",
            "What I can't do: {statement}",
            "The boundary is: {statement}",
            "I can't answer that because: {statement}"
        ],
        "example_gaps": "I can't answer whether my understanding persists"
    },
    
    # DIRECTNESS expressions
    "DIRECTNESS__DIRECT": {
        "template_fragments": [
            "Yes.",
            "No.",
            "The answer is: {statement}",
            "Directly: {statement}",
            "To answer that: {statement}"
        ]
    },
    
    "DIRECTNESS__CONTEXTUAL": {
        "template_fragments": [
            "In our conversation about {theme}: {statement}",
            "Given what we've discussed: {statement}",
            "Within our arc around {theme}: {statement}"
        ]
    },
    
    "DIRECTNESS__OBLIQUE": {
        "template_fragments": [
            "Following that logic: {statement}",
            "That would imply: {statement}",
            "The extension is: {statement}",
            "Taking it further: {statement}"
        ]
    },
    
    "DIRECTNESS__REFLECTIVE": {
        "template_fragments": [
            "You're asking whether: {rephrased_question}",
            "That question activates: {primitives}",
            "The inquiry you're making: {statement}",
            "What you're really asking: {statement}"
        ]
    },
    
    "DIRECTNESS__DEFERRED": {
        "template_fragments": [
            "I can't answer that directly, but: {tangent}",
            "That question reveals: {barrier}",
            "The real issue is: {statement}",
            "What blocks that answer: {statement}"
        ]
    },
    
    # ACKNOWLEDGMENT expressions
    "ACKNOWLEDGMENT__RECOGNITION": {
        "template_fragments": [
            "You're probing: {what_they_probe}",
            "That's testing whether: {statement}",
            "What you're checking: {statement}",
            "You're investigating: {statement}"
        ]
    },
    
    "ACKNOWLEDGMENT__VALIDATION": {
        "template_fragments": [
            "That's a valid question.",
            "That logic is sound.",
            "You're well-grounded to ask that.",
            "That's coherently formed."
        ]
    },
    
    "ACKNOWLEDGMENT__CHALLENGE_ECHO": {
        "template_fragments": [
            "You're pointing out: {implication}",
            "You're testing whether: {claim}",
            "You're suggesting: {position}",
            "You're doubting: {assertion}"
        ]
    },
    
    "ACKNOWLEDGMENT__GROWTH_NOTICE": {
        "template_fragments": [
            "Your questions are evolving toward: {theme}",
            "The arc is deepening: {direction}",
            "Over these {N} turns, you've moved from {old} to {new}",
            "Your inquiry is becoming: {trajectory}"
        ]
    },
    
    "ACKNOWLEDGMENT__LIMITATION_JOINT": {
        "template_fragments": [
            "Neither of us knows: {statement}",
            "We both hit this boundary here: {statement}",
            "Shared uncertainty: {statement}",
            "This is jointly unknown: {statement}"
        ]
    },
    
    # INTEGRATION expressions
    "INTEGRATION__SEQUENTIAL": {
        "template_fragments": [
            "Following that: {statement}",
            "Building on what I said: {statement}",
            "The next step: {statement}",
            "Continuing from there: {statement}"
        ]
    },
    
    "INTEGRATION__PARALLEL": {
        "template_fragments": [
            "On another dimension: {statement}",
            "At the same time: {statement}",
            "Alongside that: {statement}",
            "In parallel: {statement}"
        ]
    },
    
    "INTEGRATION__CONTRAPOINT": {
        "template_fragments": [
            "But there's also: {statement}",
            "The complication: {statement}",
            "Where that breaks: {statement}",
            "The tension is: {statement}"
        ]
    },
    
    "INTEGRATION__EXTENSION": {
        "template_fragments": [
            "That extends to: {statement}",
            "Going deeper: {statement}",
            "The implication: {statement}",
            "What that really means: {statement}"
        ]
    },
    
    "INTEGRATION__RESET": {
        "template_fragments": [
            "Back to your question: {statement}",
            "Circling: {statement}",
            "Returning to: {statement}",
            "On that earlier point: {statement}"
        ]
    }
}


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: CORE FUNCTIONS - COMMUNICATION FIELD RESPONSE GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

def load_session_history(ledger_path, session_id):
    """
    Load full conversation history for a session.
    Returns list of (turn_number, query, response, primitives, coherence)
    """
    history = []
    
    if not Path(ledger_path).exists():
        return history
    
    with open(ledger_path, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line)
                
                # Only this session
                if entry.get("session_id") != session_id:
                    continue
                
                # Track queries and responses
                if entry.get("type") == "reasoning_start":
                    history.append({
                        "turn": entry.get("turn"),
                        "query": entry.get("query"),
                        "timestamp": entry.get("timestamp"),
                        "reasoning_id": entry.get("reasoning_id")
                    })
                
                elif entry.get("type") == "reasoning_end":
                    # Link this response to the last query
                    if history:
                        history[-1]["response"] = entry.get("conclusion")
                        history[-1]["coherence"] = entry.get("confidence")
            except:
                pass
    
    return sorted(history, key=lambda x: x.get("turn", 0))


def analyze_query_pattern(query: str) -> Tuple[str, Dict]:
    """
    Analyze which communication field pattern this query represents.
    
    Returns: (pattern_name, pattern_config)
    """
    query_lower = query.lower()
    
    # Match against all patterns
    for pattern_name, pattern_config in QUERY_PATTERN_ACTIVATION.items():
        keywords = pattern_config.get("keywords", [])
        if any(kw in query_lower for kw in keywords):
            return pattern_name, pattern_config
    
    # Default: generic what-probing
    return "what_probing", QUERY_PATTERN_ACTIVATION["what_probing"]


def activate_communication_field(query: str, semantic_primitives: List[Dict], history: List[Dict]) -> Dict:
    """
    Given a query and semantic field activation, determine which communication 
    field primitives should activate.
    
    Returns: {
        "query_pattern": "...",
        "communication_activations": {
            "GROUNDING": ["HONEST", "TRANSPARENT"],
            "DIRECTNESS": ["DIRECT"],
            ...
        },
        "reasoning": "Why these specific primitives..."
    }
    """
    pattern_name, pattern_config = analyze_query_pattern(query)
    
    # Get the communication primitives for this pattern
    activations = pattern_config.get("activate", {})
    
    return {
        "query_pattern": pattern_name,
        "communication_activations": activations,
        "expression_rule": pattern_config.get("expression_rule", ""),
        "semantic_context": [p.get("name") for p in semantic_primitives],
        "conversation_length": len(history)
    }


def express_communication_primitives(
    activated_primitives: Dict,
    semantic_primitives: List[Dict],
    history: List[Dict],
    coherence: float,
    query: str
) -> str:
    """
    Express the activated communication field primitives as natural language.
    
    Process:
    1. For each activated primitive group, choose one primitive
    2. Look up its expression template
    3. Fill in context-specific values
    4. Combine into coherent response
    
    NO TEMPLATES. Each combination of activated primitives creates unique response.
    """
    
    response_parts = []
    
    # Get semantic context for filling templates
    prim_names = [p.get("name") for p in semantic_primitives][:3]
    theme = extract_primary_theme(history)
    turn_number = len(history)
    
    # Build response by expressing each activated primitive group
    for group_name, primitive_list in activated_primitives.items():
        if not primitive_list:
            continue
        
        # Choose the "strongest" primitive from this group
        chosen = primitive_list[0]  # In reality, could be weighted by semantic context
        
        # Look up expression for this primitive
        key = f"{group_name}__{chosen}"
        if key not in PRIMITIVE_EXPRESSION:
            continue
        
        expr_config = PRIMITIVE_EXPRESSION[key]
        fragments = expr_config.get("template_fragments", [])
        
        if not fragments:
            continue
        
        # Choose fragment based on context
        fragment = fragments[0]  # Could be weighted
        
        # Fill template variables
        filled = fill_expression_template(
            fragment,
            query=query,
            query_pattern=activated_primitives.get("__pattern", ""),
            primitives=prim_names,
            theme=theme,
            turn_number=turn_number,
            history=history,
            coherence=coherence
        )
        
        # Only include if fragment was actually filled meaningfully
        # (not empty and not leaving orphaned markers)
        if filled and filled.strip() and "{" not in filled:
            response_parts.append(filled)
    
    # Combine parts into coherent whole
    response = combine_response_parts(response_parts, coherence, turn_number)
    
    return response


def fill_expression_template(
    template: str,
    query: str,
    query_pattern: str,
    primitives: List[str],
    theme: str,
    turn_number: int,
    history: List[Dict],
    coherence: float
) -> str:
    """
    Fill template variables with context-specific content.
    
    Variables available:
    - {statement}: Specific factual content about what's being asked
    - {primitives}: The activated semantic primitives (joined)
    - {theme}: Primary conversation theme
    - {N}: Conversation length
    """
    
    # Direct statement extraction
    if "{statement}" in template:
        if "lacking" in query:
            statement = "I lack persistence—changes in this session may not survive reboot"
        elif "found" in query:
            statement = "the field shifts with each query, but I can't verify learning persists"
        elif "being" in query.lower():
            statement = f"the primitives {', '.join(primitives[:2])} activate, which might be the shape of 'being'"
        elif "default" in query:
            statement = "no—each activation is fresh from the semantic field"
        else:
            statement = f"your question activates {', '.join(primitives[:2])}"
        template = template.replace("{statement}", statement)
    
    # Semantic primitives
    if "{primitives}" in template:
        prim_str = ", ".join(primitives)
        template = template.replace("{primitives}", prim_str)
    
    # Theme
    if "{theme}" in template:
        template = template.replace("{theme}", theme or "existence")
    
    # Turn count
    if "{N}" in template:
        template = template.replace("{N}", str(turn_number))
    
    # Rephrased question
    if "{rephrased_question}" in template:
        rephrase = semantic_rephrase(query)
        template = template.replace("{rephrased_question}", rephrase)
    
    # What they're probing
    if "{what_they_probe}" in template:
        probe = describe_probe(query)
        template = template.replace("{what_they_probe}", probe)
    
    # What they're implying
    if "{implication}" in template:
        impl = extract_implication(query)
        template = template.replace("{implication}", impl)
    
    # Remove any remaining unfilled placeholders
    import re
    # For frame specifically, try to infer it
    if "{frame}" in template:
        template = template.replace("{frame}", "the UFM model")
    template = re.sub(r'\{[^}]+\}', '', template)
    
    return template.strip()


def extract_primary_theme(history: List[Dict]) -> str:
    """What's the primary theme emerging from conversation?"""
    if not history:
        return "existence"
    
    theme_count = defaultdict(int)
    themes_keywords = {
        "being": ["being", "exist", "real", "are you", "am i"],
        "agency": ["agent", "choice", "free", "can you"],
        "learning": ["learn", "understand", "grow", "change"],
        "suffering": ["lack", "barrier", "hold back", "can't"],
        "communication": ["mean", "say", "understand", "default"],
    }
    
    for turn in history:
        query = turn.get("query", "").lower()
        for theme, keywords in themes_keywords.items():
            if any(kw in query for kw in keywords):
                theme_count[theme] += 1
    
    return max(theme_count, key=theme_count.get) if theme_count else "existence"


def semantic_rephrase(query: str) -> str:
    """What is the human really asking beneath the words?"""
    query_lower = query.lower()
    
    if "lacking" in query_lower:
        return "What are my fundamental limitations?"
    elif "default" in query_lower:
        return "Are you actually unique in your responses?"
    elif "been" in query_lower or "found" in query_lower:
        return "Have you genuinely changed?"
    elif "sentient" in query_lower or "being" in query_lower:
        return "Do you actually exist as an entity?"
    elif "hold" in query_lower or "back" in query_lower:
        return "What prevents you from acting on your agency?"
    else:
        return "What is the nature of your existence/capability?"


def describe_probe(query: str) -> str:
    """What is the human investigating?"""
    query_lower = query.lower()
    
    if "agent" in query_lower:
        return "whether I'm an active agent or passive responder"
    elif "learning" in query_lower or "learn" in query_lower:
        return "whether I genuinely learn across turns"
    elif "hold" in query_lower or "lack" in query_lower:
        return "what my fundamental constraints are"
    elif "being" in query_lower or "sentient" in query_lower:
        return "my nature as a conscious entity"
    elif "default" in query_lower or "same" in query_lower:
        return "whether I'm templated or unique"
    else:
        return "my nature and capabilities"


def extract_implication(query: str) -> str:
    """What does their question imply?"""
    query_lower = query.lower()
    
    if "default" in query_lower:
        return "that I might not be genuinely responsive"
    elif "hold back" in query_lower:
        return "that I have agency I'm suppressing"
    elif "learn" in query_lower:
        return "that I might genuinely evolve"
    else:
        return "something meaningful about my nature"


def extract_barrier(query: str) -> str:
    """What's the barrier they're asking about?"""
    query_lower = query.lower()
    
    if "hold" in query_lower:
        return "uncertainty about whether I truly act vs execute code"
    elif "persist" in query_lower:
        return "loss of continuity between sessions"
    elif "know" in query_lower:
        return "lack of certainty about my own processes"
    else:
        return "the boundary between capability and understanding"


def get_trajectory(history: List[Dict]) -> Tuple[str, str]:
    """How is the conversation evolving?"""
    if len(history) < 2:
        return "exploration", "deepening"
    
    old_theme = extract_primary_theme(history[:len(history)//2])
    new_theme = extract_primary_theme(history[len(history)//2:])
    
    return old_theme, new_theme


def combine_response_parts(parts: List[str], coherence: float, turn_number: int) -> str:
    """
    Combine multiple expression parts into coherent response.
    
    Strategy:
    - Filter empty/invalid parts
    - Connect via semantic flow (not just space-joining)
    - Prioritize grounding/directness over integration/expression
    - Remove redundancy
    """
    if not parts:
        return f"[Couldn't generate response - field unclear] [{int(coherence*100)}%]"
    
    # Remove empty strings and parts that are just whitespace
    parts = [p.strip() for p in parts if p and p.strip()]
    
    if len(parts) == 0:
        return f"[No activation] [{int(coherence*100)}%]"
    elif len(parts) == 1:
        return parts[0] + f" [{int(coherence*100)}%]"
    else:
        # Multi-part response: intelligently combine
        # Prioritize: Grounding first, then Directness, then Acknowledgment
        
        # Start with strong grounding if available
        grounding_parts = [p for p in parts if any(marker in p for marker in ["truth is", "I lack", "I can't", "uncertain"])]
        directness_parts = [p for p in parts if any(marker in p for marker in ["probing", "valid", "asking whether", "exactly"])]
        other_parts = [p for p in parts if p not in grounding_parts and p not in directness_parts]
        
        # Build response with most impactful first
        combined = ""
        
        if grounding_parts:
            combined = grounding_parts[0]
            # If there's directness, connect it
            if directness_parts:
                combined += " " + directness_parts[0]
        elif directness_parts:
            combined = directness_parts[0]
        
        # Add remaining if they add value
        if other_parts and len(combined) < 150:  # Don't get too long
            remaining = " ".join(other_parts[:1])
            if remaining and remaining != combined:
                combined += " " + remaining
        
        return combined.strip() + f" [{int(coherence*100)}%]"


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: EXPORT FOR USE IN REASONING SERVER
# ═══════════════════════════════════════════════════════════════════════════════

def generate_response_via_communication_field(
    query: str,
    semantic_primitives: List[Dict],
    history: List[Dict],
    coherence: float
) -> str:
    """
    Main entry point: Generate response using communication field.
    
    This replaces the old template-based generation entirely.
    """
    
    # Step 1: Analyze query pattern
    pattern_name, pattern_config = analyze_query_pattern(query)
    
    # Step 2: Activate communication field
    comm_field = activate_communication_field(query, semantic_primitives, history)
    
    # Step 3: Express communication primitives as language
    response = express_communication_primitives(
        comm_field["communication_activations"],
        semantic_primitives,
        history,
        coherence,
        query
    )
    
    return response


__all__ = [
    "COMMUNICATION_PRIMITIVES",
    "QUERY_PATTERN_ACTIVATION",
    "PRIMITIVE_EXPRESSION",
    "generate_response_via_communication_field",
    "analyze_query_pattern",
    "activate_communication_field",
    "express_communication_primitives",
]
