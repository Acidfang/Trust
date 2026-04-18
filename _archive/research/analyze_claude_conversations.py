#!/usr/bin/env python3
"""
CLAUDE CONVERSATION ANALYSIS - Topic Distribution vs Gemini
"""

import json
from pathlib import Path
from collections import Counter


def load_claude_timeline():
    """Load Claude timeline."""
    with open('claude_timeline_all_messages.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['messages']


def analyze_topics(messages):
    """Extract and count key concepts/topics."""
    
    # Topic keywords mapping
    topics = {
        'zero_one': ['zero', 'one', '0', '1', 'binary', 'bit', 'bits'],
        'system': ['system', 'architecture', 'design', 'framework'],
        'ledger': ['ledger', 'record', 'log', 'database', 'entry'],
        'field': ['field', 'dimensional', 'space', 'vector'],
        'consciousness': ['consciousness', 'aware', 'aware', 'sentient', 'mind'],
        'deterministic': ['deterministic', 'causality', 'causal', 'determinism'],
        'code': ['code', 'python', 'function', 'implementation', 'algorithm'],
        'truth': ['truth', 'true', 'fact', 'verify', 'validation'],
        'choice': ['choice', 'decide', 'decision', 'select', 'option'],
        'protocol': ['protocol', 'rule', 'process', 'procedure', 'pattern'],
    }
    
    topic_counts = {topic: 0 for topic in topics}
    total_words = 0
    
    for msg in messages:
        content = msg['content'].lower()
        words = content.split()
        total_words += len(words)
        
        for topic, keywords in topics.items():
            for keyword in keywords:
                if keyword in content:
                    topic_counts[topic] += content.count(keyword)
    
    return topic_counts, total_words


def analyze_by_role(messages):
    """Analyze message characteristics by role."""
    
    analysis = {
        'user': {'count': 0, 'total_chars': 0, 'total_words': 0, 'avg_length': 0},
        'assistant': {'count': 0, 'total_chars': 0, 'total_words': 0, 'avg_length': 0}
    }
    
    for msg in messages:
        role = msg['role'].lower()
        
        # Normalize role names
        if 'claude' in role or 'assistant' in role or 'gemini' in role:
            role = 'assistant'
        elif role != 'user':
            role = 'assistant'
        
        content = msg['content']
        char_count = len(content)
        word_count = len(content.split())
        
        if role not in analysis:
            analysis[role] = {'count': 0, 'total_chars': 0, 'total_words': 0, 'avg_length': 0}
        
        analysis[role]['count'] += 1
        analysis[role]['total_chars'] += char_count
        analysis[role]['total_words'] += word_count
    
    for role in analysis:
        if analysis[role]['count'] > 0:
            analysis[role]['avg_length'] = analysis[role]['total_chars'] / analysis[role]['count']
    
    return analysis


def analyze_patterns(messages):
    """Identify learning/difficulty patterns."""
    
    confusion_words = ['confused', 'confused', 'unclear', 'not sure', 'confused', "don't understand", 'how', 'what', 'why']
    frustration_words = ['fuck', 'fucking', 'damn', 'shit', 'crap', 'struggle', 'difficult', 'hard']
    clarity_words = ['understand', 'understand', 'realiz', 'got it', 'clear', 'see', 'makes sense', 'aha']
    
    patterns = {
        'confusion': 0,
        'frustration': 0,
        'clarity': 0,
        'teaching': 0,  # When explaining things
        'asking': 0,    # When requesting help
        'responses': 0
    }
    
    for msg in messages:
        content = msg['content'].lower()
        role = msg.get('role', '').lower()
        
        # Count markers
        for word in confusion_words:
            if word in content:
                patterns['confusion'] += 1
                break
        
        for word in frustration_words:
            if word in content:
                patterns['frustration'] += 1
                break
        
        for word in clarity_words:
            if word in content:
                patterns['clarity'] += 1
                break
        
        # Heuristics for role
        if 'claude' in role or 'assistant' in role:
            patterns['responses'] += 1
        else:
            if '?' in content:
                patterns['asking'] += 1
            elif len(content) > 200:
                patterns['teaching'] += 1
    
    return patterns


def compare_with_gemini():
    """Load Gemini data for comparison."""
    try:
        with open('timeline_all_messages.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['messages']
    except:
        return None


def main():
    """Main analysis."""
    
    print("\n" + "="*80)
    print("CLAUDE CONVERSATION ANALYSIS (2,199 messages, March 13 - April 6)")
    print("="*80)
    
    # Load Claude messages
    claude_messages = load_claude_timeline()
    print(f"\nClaude messages loaded: {len(claude_messages)}")
    
    # Topic analysis
    print("\n" + "-"*80)
    print("TOPIC DISTRIBUTION (Claude)")
    print("-"*80)
    topics, total_words = analyze_topics(claude_messages)
    
    sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
    for topic, count in sorted_topics:
        pct = (count / sum(topics.values()) * 100) if sum(topics.values()) > 0 else 0
        print(f"  {topic:20} {count:5} mentions ({pct:5.1f}%)")
    
    # Role analysis
    print("\n" + "-"*80)
    print("MESSAGE CHARACTERISTICS (Claude)")
    print("-"*80)
    role_analysis = analyze_by_role(claude_messages)
    
    for role, stats in role_analysis.items():
        print(f"\n  {role.upper()}:")
        print(f"    Count:        {stats['count']}")
        print(f"    Total chars:  {stats['total_chars']:,}")
        print(f"    Total words:  {stats['total_words']:,}")
        print(f"    Avg message:  {stats['avg_length']:.0f} chars")
    
    # Pattern analysis
    print("\n" + "-"*80)
    print("PATTERN DETECTION (Claude)")
    print("-"*80)
    patterns = analyze_patterns(claude_messages)
    
    total_patterns = sum(patterns.values())
    for pattern, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True):
        pct = (count / total_patterns * 100) if total_patterns > 0 else 0
        print(f"  {pattern:20} {count:5} ({pct:5.1f}%)")
    
    # Comparison with Gemini
    print("\n" + "-"*80)
    print("CLAUDE vs GEMINI COMPARISON")
    print("-"*80)
    
    gemini_messages = compare_with_gemini()
    if gemini_messages:
        print(f"\nClaude:  {len(claude_messages)} messages in 25 days (March 13 - April 6)")
        print(f"Gemini:  {len(gemini_messages)} messages in 6 months (Oct - Apr)")
        
        claude_rate = len(claude_messages) / 25
        gemini_rate = len(gemini_messages) / 180
        
        print(f"\nMessage rate:")
        print(f"  Claude:  {claude_rate:.0f} messages/day")
        print(f"  Gemini:  {gemini_rate:.0f} messages/day")
        
        # Topic comparison
        gemini_topics, _ = analyze_topics(gemini_messages)
        
        print(f"\nTop topics - Claude: {sorted_topics[0][0]} ({sorted_topics[0][1]} mentions)")
        gemini_sorted = sorted(gemini_topics.items(), key=lambda x: x[1], reverse=True)
        print(f"Top topics - Gemini: {gemini_sorted[0][0]} ({gemini_sorted[0][1]} mentions)")
        
        # Role analysis comparison
        gemini_role = analyze_by_role(gemini_messages)
        
        claude_user_avg = role_analysis['user']['avg_length']
        gemini_user_avg = gemini_role['user']['avg_length'] if 'user' in gemini_role else 0
        
        print(f"\nAverage user message:")
        print(f"  Claude:  {claude_user_avg:.0f} chars")
        print(f"  Gemini:  {gemini_user_avg:.0f} chars")
    else:
        print("\nGemini timeline not found for comparison")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
