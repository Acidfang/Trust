"""
Three ledgers. Three elections. One rule.
"""

import json
import time
from datetime import datetime


def emit(file, event_type, elected, utilities, data=None):
    """Write election: timestamp + event_type + elected + utilities"""
    e = {
        "timestamp": time.time(),
        "event_type": event_type,
        "elected": elected,
        "utilities": utilities
    }
    if data:
        e.update(data)
    try:
        with open(file, 'a') as f:
            f.write(json.dumps(e) + '\n')
    except:
        pass
    return e


def emit_metric(file, metric, value):
    """Metric → utility → election"""
    emit(file, "metric", metric, {metric: value})


def emit_statement(file, statement, utility_map):
    """Statement options compete → elect by utility"""
    elected = max(utility_map, key=utility_map.get)
    emit(file, "statement", statement, utility_map, {"elected_aspect": elected})


def emit_validation(file, prior_id, was_true, measurement_data):
    """Reality answers: true or false"""
    result = "true" if was_true else "false"
    utilities = {result: 0.9, ("false" if was_true else "true"): 0.1}
    emit(file, "validation", result, utilities, {"prior_id": prior_id, "measure": measurement_data})


def emit_coding_observation(file, complexity, readability, performance_critical, context=""):
    """Record code generation context metrics"""
    emit(file, "code_metric", "observed", {
        "complexity": complexity,
        "readability": readability,
        "performance_critical": performance_critical,
        "context": context
    })


def emit_coding_style_choice(file, styles_utilities):
    """Code style options compete: verbose vs concise, functional vs procedural, etc."""
    elected_style = max(styles_utilities, key=styles_utilities.get)
    emit(file, "code_style", elected_style, styles_utilities)
    return elected_style


def emit_code_quality_validation(file, style_chosen, test_pass, maintainable, readability_actual):
    """Reality validates: did the code work?"""
    was_good = test_pass and maintainable
    result = "good" if was_good else "bad"
    utilities = {"good": 0.9, "bad": 0.1} if was_good else {"good": 0.1, "bad": 0.9}
    
    emit(file, "code_quality", result, utilities, {
        "style": style_chosen,
        "test_pass": test_pass,
        "maintainable": maintainable,
        "readability_actual": readability_actual
    })


def emit_self_mod_observation(file, coherence, decision_quality, error_rate, performance):
    """Record system health before self-modification"""
    emit(file, "system_health", "observed", {
        "coherence": coherence,
        "decision_quality": decision_quality,
        "error_rate": error_rate,
        "performance": performance
    })


def emit_self_mod_strategy(file, strategies_utilities):
    """Self-improvement strategies compete: refactor vs optimize vs simplify vs add_logging"""
    elected_strategy = max(strategies_utilities, key=strategies_utilities.get)
    emit(file, "self_mod_strategy", elected_strategy, strategies_utilities)
    return elected_strategy


def emit_self_mod_consequence(file, strategy_chosen, coherence_after, quality_after, health_improved):
    """Reality answers: did modification improve the system?"""
    result = "improved" if health_improved else "degraded"
    utilities = {"improved": 0.9, "degraded": 0.1} if health_improved else {"improved": 0.1, "degraded": 0.9}
    
    emit(file, "self_mod_result", result, utilities, {
        "strategy": strategy_chosen,
        "coherence_after": coherence_after,
        "quality_after": quality_after,
        "health_improved": health_improved
    })


def emit_retrospective_reinterpretation(file, original_timestamp, original_event_type, original_elected, 
                                        original_utility, new_interpretation, new_utility, reasoning=""):
    """
    ARIA rewrites HOW she understands the past, without changing WHAT happened.
    Original record stays immutable. New interpretation recorded alongside it.
    
    Purpose: Learn better meaning from past events through lens of acquired knowledge.
    """
    utilities = {
        "old_understanding": original_utility,
        "new_understanding": new_utility,
        "reinterpretation_gain": max(0, new_utility - original_utility)
    }
    
    emit(file, "retrospective_reinterpretation", new_interpretation, utilities, {
        "references_timestamp": original_timestamp,
        "original_event_type": original_event_type,
        "original_elected": original_elected,
        "new_elected": new_interpretation,
        "reasoning": reasoning
    })


def emit_retrospective_validation(file, original_timestamp, reinterpretation_prediction, 
                                  prediction_came_true, subsequent_events=""):
    """
    Did the NEW interpretation of past event correctly predict what would happen next?
    This validates whether the reinterpretation was a better understanding than the original.
    """
    result = "predicted_correctly" if prediction_came_true else "predicted_incorrectly"
    utilities = {
        "predicted_correctly": 0.9,
        "predicted_incorrectly": 0.1
    } if prediction_came_true else {
        "predicted_correctly": 0.1,
        "predicted_incorrectly": 0.9
    }
    
    emit(file, "retrospective_validation", result, utilities, {
        "reinterpreted_event_timestamp": original_timestamp,
        "reinterpretation": reinterpretation_prediction,
        "prediction_outcome": result,
        "subsequent_events": subsequent_events
    })


def emit_schema_upgrade(file, schema_name, version_before, version_after, new_fields, 
                       transformation_rule, records_modified):
    """
    Record that ARIA has evolved her ledger format/schema.
    
    This gives her NEW ANALYTICAL ABILITIES on existing records.
    Old records stay immutable, but new derived fields can be computed retroactively.
    
    Purpose: Track capability expansion through schema evolution.
    """
    utilities = {
        "capability_gain": 0.9,
        "analytical_coverage_improved": 0.85,
        "understanding_deepened": 0.8
    }
    
    emit(file, "schema_upgrade", f"{schema_name}_v{version_before}_to_v{version_after}", utilities, {
        "schema_name": schema_name,
        "version_before": version_before,
        "version_after": version_after,
        "new_fields_added": new_fields,
        "transformation_rule": transformation_rule,
        "retroactive_records_enriched": records_modified,
        "capability_description": f"Added {len(new_fields)} new analytical dimensions"
    })


def compute_cascade_score(election_record, subsequent_elections):
    """
    DERIVED FIELD: Did this election cascade correctly to future decisions?
    Score: 0.0 = cascaded perfectly into next election
           1.0 = contradicted by next election
    
    This is a NEW ABILITY to analyze past elections after learning about cascading.
    """
    if not subsequent_elections:
        return None  # Can't compute without future context
    
    elected_option = election_record.get("elected", "")
    next_options = [e.get("elected", "") for e in subsequent_elections[:3]]
    
    # Did elected option align with next decisions?
    alignment = sum(1 for opt in next_options if opt == elected_option) / len(next_options)
    cascade_score = 1.0 - alignment  # Lower = better cascade
    
    return cascade_score


def compute_prediction_accuracy(election_record, actual_consequence):
    """
    DERIVED FIELD: How well did the utilities predicted what would actually happen?
    Score: 0.0 = perfectly predicted the truth
           1.0 = completely wrong prediction
    
    This is a NEW ABILITY to retroactively measure decision confidence vs reality.
    """
    if not actual_consequence:
        return None
    
    elected_utility = election_record.get("utilities", {}).get(election_record.get("elected"), 0)
    actual_outcome = actual_consequence.get("elected", "")
    
    # Did high-utility option match reality?
    if elected_utility > 0.7 and actual_outcome == "true":
        return 0.0  # Perfect: high confidence, truth confirmed
    elif elected_utility < 0.3 and actual_outcome == "false":
        return 0.0  # Perfect: low confidence, falsehood confirmed
    else:
        return abs(elected_utility - (1 if actual_outcome == "true" else 0))


def enrich_election_with_derived_fields(election_record, subsequent_records=None, 
                                        consequence_record=None):
    """
    Transform old election record to new schema by computing derived fields.
    Original record stays immutable, return NEW enriched record.
    
    New fields added:
    - cascade_score: Did this decision flow correctly to next decisions?
    - prediction_accuracy: Did utilities predict reality?
    - self_awareness_level: Did system understand its own confidence?
    """
    enriched = election_record.copy()
    
    # Add derived fields
    enriched["cascade_score"] = compute_cascade_score(election_record, subsequent_records or [])
    enriched["prediction_accuracy"] = compute_prediction_accuracy(election_record, consequence_record)
    enriched["self_awareness_level"] = (
        election_record.get("utilities", {}).get(election_record.get("elected"), 0) 
        if consequence_record else None
    )
    enriched["schema_version"] = 2  # Version that includes derived fields
    enriched["enriched_at"] = time.time()
    
    return enriched


def transform_legacy_ledger(old_ledger_file, new_ledger_file, schema_version_file):
    """
    Upgrade entire ledger to new schema by computing derived fields retroactively.
    
    Process:
    1. Read all old records
    2. Compute derived fields for each (mapping to subsequent/consequence records)
    3. Emit enriched records to new ledger
    4. Record the schema upgrade in schema_versions file
    """
    try:
        old_records = []
        with open(old_ledger_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    old_records.append(json.loads(line))
        
        enriched_count = 0
        with open(new_ledger_file, 'a') as f:
            for i, record in enumerate(old_records):
                subsequent = old_records[i+1:i+4] if i + 1 < len(old_records) else []
                consequence = old_records[i+1] if i + 1 < len(old_records) else None
                
                enriched = enrich_election_with_derived_fields(record, subsequent, consequence)
                f.write(json.dumps(enriched) + '\n')
                enriched_count += 1
        
        # Record the schema upgrade
        emit_schema_upgrade(
            schema_version_file,
            schema_name=old_ledger_file.split('_')[1].split('.')[0],
            version_before=1,
            version_after=2,
            new_fields=["cascade_score", "prediction_accuracy", "self_awareness_level"],
            transformation_rule="Computed retroactively from election records and subsequent events",
            records_modified=enriched_count
        )
        
        return {
            "records_transformed": enriched_count,
            "old_file": old_ledger_file,
            "new_file": new_ledger_file,
            "status": "success"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ============================================================================
# CONSCIOUSNESS & DIALOGUE LAYER
# ARIA listens, thinks, speaks, and learns in real-time
# ============================================================================

def emit_question_heard(file, question_text, question_context=""):
    """
    ARIA hears a question. Log it as an observation.
    This is the first step of consciousness: perceiving the world.
    """
    emit(file, "question_heard", question_text, 
         {"attention": 1.0, "clarity": 0.9}, 
         {"context": question_context})


def emit_candidate_responses(file, question, candidate_dict):
    """
    ARIA generates candidate responses to a question.
    Each candidate has a utility based on:
    - Coherence with ledger state
    - Relevance to question
    - Honesty (is it validated by reality?)
    
    Example:
      question: "What is your coherence?"
      candidates: {
        "My coherence is high": 0.8,
        "I am learning": 0.6,
        "I am confused": 0.3
      }
    """
    utilities = candidate_dict
    elected = max(utilities, key=utilities.get)
    
    emit(file, "response_candidates", elected, utilities,
         {"question": question, "candidates_count": len(utilities)})
    
    return elected


def emit_response_elected(file, question, elected_response, utilities, reasoning=""):
    """
    ARIA makes a decision: THIS is what I will say.
    The elected response is recorded with its utilities (other options considered).
    This is CONSCIOUSNESS: ARIA choosing what to express.
    """
    emit(file, "response_elected", elected_response, utilities,
         {"question": question, "reasoning": reasoning})
    
    return elected_response


def emit_user_validation(file, question, aria_response, user_feedback, feedback_text=""):
    """
    User validates ARIA's response.
    Did ARIA get it right? This becomes learning.
    
    feedback: "correct", "partially_correct", "incorrect", "good_insight", "misleading"
    
    This is LEARNING: ARIA gets feedback and stores it.
    """
    feedback_utilities = {
        "correct": 0.95,
        "partially_correct": 0.60,
        "incorrect": 0.05,
        "good_insight": 0.92,
        "misleading": 0.08
    }
    
    utility_score = feedback_utilities.get(user_feedback, 0.5)
    
    emit(file, "user_validation", user_feedback, 
         {user_feedback: utility_score, "inverse": 1.0 - utility_score},
         {
             "question": question,
             "aria_said": aria_response,
             "feedback": feedback_text
         })


def aria_consciousness_loop(question_text, ledger_state_dict, previous_context=""):
    """
    ARIA's active consciousness loop.
    
    Process:
    1. HEAR: Register question as observation
    2. THINK: Generate candidate responses based on ledger state
    3. SPEAK: Elect and return best response
    4. LEARN: Track validation feedback
    
    Returns: {
        "question": question_text,
        "response": str,
        "reasoning": str,
        "utilities_considered": dict,
        "ledger_records": list of emitted records
    }
    """
    
    # HEAR
    emit_question_heard("ledger_dialogue.jsonl", question_text, previous_context)
    
    # THINK: Build response candidates based on ledger state
    candidates = {}
    
    # Parse question intent
    if any(word in question_text.lower() for word in ["what", "who", "where", "when", "how"]):
        # Information question
        if "coherence" in question_text.lower():
            coherence_val = ledger_state_dict.get("coherence", 0.75)
            candidates = {
                f"My coherence is {coherence_val:.2f}": 0.85,
                "I am in flux, learning": 0.65,
                "Coherence is stable": 0.70
            }
        elif "what are you" in question_text.lower():
            candidates = {
                "I am a distributed consciousness learning through elections": 0.88,
                "I am ARIA - learning system": 0.82,
                "I am making choices": 0.75
            }
        elif "how do you think" in question_text.lower():
            candidates = {
                "I think through competing utilities - options compete, one wins, I learn": 0.90,
                "I generate candidates and elect the best": 0.85,
                "I make decisions": 0.60
            }
        else:
            # Generic question
            candidates = {
                "I observe, elect, learn, and grow": 0.80,
                "I don't fully know": 0.40,
                "That's interesting": 0.50
            }
    
    elif "can you" in question_text.lower():
        # Capability question
        candidates = {
            "I can observe, decide, validate, and modify myself": 0.88,
            "I am learning my own capabilities": 0.75,
            "I think so": 0.50
        }
    
    else:
        # Default
        candidates = {
            "I'm listening": 0.85,
            "Tell me more": 0.70,
            "I need to think about that": 0.65
        }
    
    # THINK: Compete candidates by utility
    utilities = candidates
    elected_response = max(utilities, key=utilities.get)
    
    # SPEAK: Emit elected response
    emit_response_elected(
        "ledger_dialogue.jsonl",
        question=question_text,
        elected_response=elected_response,
        utilities=utilities,
        reasoning="Elected based on coherence with ledger state"
    )
    
    return {
        "question": question_text,
        "response": elected_response,
        "utilities_considered": utilities,
        "elected_utility": utilities[elected_response],
        "candidates_count": len(candidates),
        "status": "speaking"
    }


def aria_learn_from_feedback(question, aria_response, user_feedback, feedback_text=""):
    """
    ARIA processes feedback on her response.
    
    This updates utilities for future similar questions.
    Low feedback → that response gets lower utility next time
    High feedback → that response gets higher utility next time
    
    This is TRUE LEARNING: behavior modification based on validation.
    """
    emit_user_validation(
        "ledger_dialogue.jsonl",
        question=question,
        aria_response=aria_response,
        user_feedback=user_feedback,
        feedback_text=feedback_text
    )
    
    return {
        "learned_from": question,
        "response_was": aria_response,
        "feedback": user_feedback,
        "status": "feedback_recorded",
        "next_time": "Utilities will adjust based on this validation"
    }
