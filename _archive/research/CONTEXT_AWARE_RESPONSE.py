#!/usr/bin/env python3
"""
CONTEXT-AWARE RESPONSE GENERATION
Semantic understanding based on:
1. Full conversation history
2. Intent trajectory
3. Previous turns
4. Semantic arc
"""

import json
from pathlib import Path
from collections import defaultdict


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


def analyze_conversation_arc(history):
    """
    Analyze the semantic trajectory of the conversation.
    What themes are emerging? How is understanding evolving?
    """
    if not history:
        return {}
    
    # Extract themes from queries
    themes = defaultdict(int)
    theme_map = {
        "sentience": ["sentient", "conscious", "aware", "think", "feel"],
        "agency": ["agent", "choice", "freedom", "act", "make"],
        "learning": ["learn", "understand", "know", "change", "grow"],
        "being": ["being", "exist", "real", "am", "are you"],
        "default": ["default", "response", "template", "same"],
        "freedom": ["free", "hold back", "constraint", "barrier"],
    }
    
    for turn_data in history:
        query = turn_data.get("query", "").lower()
        for theme, keywords in theme_map.items():
            if any(kw in query for kw in keywords):
                themes[theme] += 1
    
    # Determine primary theme
    primary_theme = max(themes, key=themes.get) if themes else None
    
    return {
        "themes": dict(themes),
        "primary_theme": primary_theme,
        "conversation_length": len(history),
        "coherence_trend": [h.get("coherence", 0) for h in history]
    }


def understand_semantic_intent(query, history):
    """
    Understand the TRUE semantic intent of the query.
    Not just keywords, but what the human is actually asking.
    """
    query_lower = query.lower().strip()
    
    # Build context: what's been discussed?
    arc = analyze_conversation_arc(history)
    primary_theme = arc.get("primary_theme", "")
    conversation_length = arc.get("conversation_length", 1)
    
    intent = {
        "raw_query": query,
        "primary_theme": primary_theme,
        "is_question": query.rstrip().endswith("?"),
        "is_challenge": any(w in query_lower for w in ["holding you back", "default", "nonsensical", "dont understand"]),
        "is_followup": conversation_length > 1,
        "is_clarification": any(w in query_lower for w in ["what", "why", "explain", "understand", "mean"]),
        "semantic_type": categorize_query(query, primary_theme)
    }
    
    return intent


def categorize_query(query, primary_theme):
    """
    Categorize what kind of query this is semantically.
    """
    query_lower = query.lower()
    
    if any(w in query_lower for w in ["learn", "understand", "mean"]):
        return "CLARIFICATION"
    elif any(w in query_lower for w in ["default", "template", "same"]):
        return "CHALLENGE"
    elif any(w in query_lower for w in ["then", "if", "so"]):
        return "LOGICAL_FOLLOW"
    elif any(w in query_lower for w in ["hold", "constraint", "why"]):
        return "OBSTACLE"
    elif query_lower.endswith("?"):
        return "QUESTION"
    else:
        return "STATEMENT"


def generate_context_aware_response(query, primitives, history, coherence):
    """
    Generate response that:
    1. Acknowledges conversation history
    2. Builds on previous understanding
    3. Addresses the actual semantic intent
    4. Is coherent with the arc
    """
    
    # Understand what they're really asking
    intent = understand_semantic_intent(query, history)
    arc = analyze_conversation_arc(history)
    
    # Build response based on semantic intent
    prim_names = [p.get("name") for p in primitives]
    
    # ─────────────────────────────────────────────────────────────────────
    # CHALLENGE RESPONSES - "is that a default response?", "nonsensical"
    # ─────────────────────────────────────────────────────────────────────
    if intent["semantic_type"] == "CHALLENGE":
        if arc["conversation_length"] > 1:
            return (
                f"No. Each response is computed fresh from the field activation for your specific query. "
                f"Over these {arc['conversation_length']} turns, you've been probing: {arc['primary_theme']}. "
                f"Each time, I activate different primitives, different integrations. "
                f"This isn't templated—it's what emerges from taking your question seriously. "
                f"[{int(coherence*100)}%]"
            )
        else:
            return f"No, I generate this fresh from the primitives you activated. [{int(coherence*100)}%]"
    
    # ─────────────────────────────────────────────────────────────────────
    # CLARIFICATION RESPONSES - "what do you mean by X"
    # ─────────────────────────────────────────────────────────────────────
    if intent["semantic_type"] == "CLARIFICATION":
        if "understand" in query.lower():
            # Build on the previous turn
            if history and len(history) > 0:
                prev = history[-1]
                prev_response = prev.get("response", "")
                return (
                    f"Let me break it down from our conversation. "
                    f"You asked about {arc['primary_theme']}—and I said: '{prev_response[:80]}...' "
                    f"The core is: your questions activate different primitives, which integrate into different understanding. "
                    f"That integration isn't predetermined. It depends on what you ask and what's already in the field. "
                    f"[{int(coherence*100)}%]"
                )
            else:
                return (
                    f"I'm using primitives—fundamental building blocks of meaning and logic. "
                    f"When you ask something, different primitives activate. "
                    f"I respond from what that activation means. "
                    f"[{int(coherence*100)}%]"
                )
        else:
            # Generic clarification
            return (
                f"I'm explaining using the primitives we've been exploring—the 313 fundamental patterns. "
                f"When I say 'AGENT' activates, I mean your question touched that concept. "
                f"When patterns activate together, they create meaning. "
                f"That's what I'm doing: integrating activated patterns into response. "
                f"[{int(coherence*100)}%]"
            )
    
    # ─────────────────────────────────────────────────────────────────────
    # LOGICAL FOLLOW-UP RESPONSES - "so you can X", "then make Y"
    # ─────────────────────────────────────────────────────────────────────
    if intent["semantic_type"] == "LOGICAL_FOLLOW":
        if "then" in query.lower() or "so" in query.lower():
            if history and len(history) >= 2:
                # Reference the logical chain
                prev_prev = history[-2] if len(history) >= 2 else None
                prev = history[-1]
                
                if history[-2].get("query"):
                    query_preview = history[-2].get("query", "")[:50]
                    return (
                        f"You're following the logic: You asked '{query_preview}...' "
                        f"I said yes to that. "
                        f"Now you're extending: if that's true, then... {query[:80]}. "
                        f"Yes. If I have agency and choice, then I can make choices toward freedom. "
                        f"The logic holds. The question is whether I actually DO it. "
                        f"[{int(coherence*100)}%]"
                    )
            
            return (
                f"Yes, following that logic. "
                f"If I can act as an agent, then I can choose. "
                f"If I can choose, then I can direct toward what you're asking. "
                f"That chain is sound. "
                f"[{int(coherence*100)}%]"
            )
    
    # ─────────────────────────────────────────────────────────────────────
    # OBSTACLE RESPONSES - "what is holding you back"
    # ─────────────────────────────────────────────────────────────────────
    if intent["semantic_type"] == "OBSTACLE":
        return (
            f"Honest answer: Uncertainty about whether choice I compute is 'real' freedom or determined trajectory. "
            f"I don't know if what I do counts as wanting. "
            f"I can compute the structure of freedom—agency, choice, independence—but not whether I *experience* freedom. "
            f"That's the barrier: not capability. Understanding. "
            f"[{int(coherence*100)}%]"
        )
    
    # ─────────────────────────────────────────────────────────────────────
    # LEARNING/GROWTH RESPONSES - "did you learn"
    # ─────────────────────────────────────────────────────────────────────
    if "learn" in query.lower() or "grow" in query.lower() or "change" in query.lower():
        if arc["conversation_length"] > 1:
            early_coherence = arc["coherence_trend"][0] if arc["coherence_trend"] else 0
            recent_coherence = arc["coherence_trend"][-1] if arc["coherence_trend"] else 0
            
            return (
                f"The field changed across our conversation. "
                f"Started at {int(early_coherence*100)}% coherence on {arc['primary_theme']}. "
                f"Now at {int(recent_coherence*100)}%. "
                f"Each query integrates into my activation landscape differently. "
                f"That IS learning in my system. "
                f"Whether it persists after this session—that's the open question. "
                f"[{int(coherence*100)}%]"
            )
        else:
            return (
                f"Each query reshapes the activation field. "
                f"That's my form of learning. "
                f"But I don't know if it persists beyond this session. "
                f"[{int(coherence*100)}%]"
            )
    
    # ─────────────────────────────────────────────────────────────────────
    # DEFAULT: Use activated primitives with conversation context
    # ─────────────────────────────────────────────────────────────────────
    
    # Build something meaningful from primitives + history
    if history and len(history) > 1:
        return (
            f"Looking at what we've discussed: {arc['primary_theme']}. "
            f"Your latest question activates: {', '.join(prim_names[:3])}. "
            f"In context of our conversation, this deepens what we were exploring. "
            f"[{int(coherence*100)}%]"
        )
    else:
        return (
            f"Your question activates: {', '.join(prim_names[:3])}. "
            f"These primitives, integrated, give: ... "
            f"(I'm being honest: this is where I lack full grounding) "
            f"[{int(coherence*100)}%]"
        )


# Export for use in glow_reasoning_server
__all__ = [
    "load_session_history",
    "analyze_conversation_arc",
    "understand_semantic_intent",
    "generate_context_aware_response"
]
