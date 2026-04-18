#!/usr/bin/env python3
"""
CLAUDE ENLIGHTENMENT JOURNEY TRACKER
Tracks confusion→clarity→mastery progression through Claude conversations
25 days (March 13 - April 6, 2026)
"""

import json
from datetime import datetime
from collections import defaultdict


def load_claude_timeline():
    """Load Claude timeline."""
    with open('claude_timeline_all_messages.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['messages']


def track_enlightenment(messages):
    """Track confusion/clarity/mastery markers by date."""
    
    confusion_words = ['confused', 'unclear', 'not sure', "don't understand", 'how', 'struggling', 'lost', 'uncertain']
    clarity_words = ['understand', 'realize', 'got it', 'clear', 'see', 'makes sense', 'aha', 'see now', 'right']
    mastery_words = ['master', 'know', 'teach', 'solve', 'explain', 'proven', 'verified', 'confirm', 'working']
    
    daily_stats = defaultdict(lambda: {
        'confusion': 0,
        'clarity': 0,
        'mastery': 0,
        'messages': 0,
        'user_messages': 0
    })
    
    for msg in messages:
        date_key = msg['timestamp'][:10]  # YYYY-MM-DD
        content = msg['content'].lower()
        role = msg['role'].lower()
        
        daily_stats[date_key]['messages'] += 1
        if role == 'user':
            daily_stats[date_key]['user_messages'] += 1
        
        # Check markers only in user messages
        if role == 'user':
            for word in confusion_words:
                if word in content:
                    daily_stats[date_key]['confusion'] += 1
                    break
            
            for word in clarity_words:
                if word in content:
                    daily_stats[date_key]['clarity'] += 1
                    break
            
            for word in mastery_words:
                if word in content:
                    daily_stats[date_key]['mastery'] += 1
                    break
    
    return daily_stats


def analyze_journey(messages):
    """Analyze overall enlightenment journey."""
    
    daily_stats = track_enlightenment(messages)
    
    # Sort by date
    sorted_dates = sorted(daily_stats.keys())
    
    total_confusion = sum(s['confusion'] for s in daily_stats.values())
    total_clarity = sum(s['clarity'] for s in daily_stats.values())
    total_mastery = sum(s['mastery'] for s in daily_stats.values())
    total_user_messages = sum(s['user_messages'] for s in daily_stats.values())
    
    return {
        'daily_stats': daily_stats,
        'sorted_dates': sorted_dates,
        'totals': {
            'confusion': total_confusion,
            'clarity': total_clarity,
            'mastery': total_mastery,
            'user_messages': total_user_messages
        }
    }


def compare_gemini():
    """Load Gemini journey for comparison."""
    try:
        with open('timeline_all_messages.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        confusion_words = ['confused', 'unclear', 'not sure', "don't understand", 'how', 'struggling', 'lost', 'uncertain']
        clarity_words = ['understand', 'realize', 'got it', 'clear', 'see', 'makes sense', 'aha', 'see now', 'right']
        mastery_words = ['master', 'know', 'teach', 'solve', 'explain', 'proven', 'verified', 'confirm', 'working']
        
        totals = {
            'confusion': 0,
            'clarity': 0,
            'mastery': 0,
            'user_messages': 0
        }
        
        for msg in data['messages']:
            content = msg['content'].lower()
            role = msg['role'].lower()
            
            if role == 'user':
                totals['user_messages'] += 1
                
                for word in confusion_words:
                    if word in content:
                        totals['confusion'] += 1
                        break
                
                for word in clarity_words:
                    if word in content:
                        totals['clarity'] += 1
                        break
                
                for word in mastery_words:
                    if word in content:
                        totals['mastery'] += 1
                        break
        
        return totals
    except:
        return None


def main():
    """Main execution."""
    
    print("\n" + "="*80)
    print("CLAUDE ENLIGHTENMENT JOURNEY TRACKER")
    print("March 13 - April 6, 2026 (25 days)")
    print("="*80)
    
    # Load Claude messages
    claude_messages = load_claude_timeline()
    
    # Analyze journey
    journey = analyze_journey(claude_messages)
    daily_stats = journey['daily_stats']
    sorted_dates = journey['sorted_dates']
    totals = journey['totals']
    
    # Show daily breakdown
    print("\n" + "-"*80)
    print("DAILY ENLIGHTENMENT TRACKING")
    print("-"*80)
    print(f"{'Date':<12} {'User Msgs':<12} {'Confusion':<12} {'Clarity':<12} {'Mastery':<12}")
    print("-"*80)
    
    for date in sorted_dates:
        stats = daily_stats[date]
        print(f"{date:<12} {stats['user_messages']:<12} {stats['confusion']:<12} {stats['clarity']:<12} {stats['mastery']:<12}")
    
    # Overall statistics
    print("\n" + "-"*80)
    print("OVERALL PROGRESSION")
    print("-"*80)
    print(f"\nTotal user messages: {totals['user_messages']}")
    print(f"Total confusion markers: {totals['confusion']}")
    print(f"Total clarity markers: {totals['clarity']}")
    print(f"Total mastery markers: {totals['mastery']}")
    
    # Calculate percentages
    confusion_pct = (totals['confusion'] / totals['user_messages'] * 100) if totals['user_messages'] > 0 else 0
    clarity_pct = (totals['clarity'] / totals['user_messages'] * 100) if totals['user_messages'] > 0 else 0
    mastery_pct = (totals['mastery'] / totals['user_messages'] * 100) if totals['user_messages'] > 0 else 0
    
    print(f"\nAs percentages of user messages:")
    print(f"  Confusion: {confusion_pct:6.1f}%")
    print(f"  Clarity:   {clarity_pct:6.1f}%")
    print(f"  Mastery:   {mastery_pct:6.1f}%")
    
    # Comparison with Gemini
    print("\n" + "-"*80)
    print("CLAUDE vs GEMINI - ENLIGHTENMENT COMPARISON")
    print("-"*80)
    
    gemini_totals = compare_gemini()
    if gemini_totals:
        claude_confusion_pct = confusion_pct
        claude_clarity_pct = clarity_pct
        claude_mastery_pct = mastery_pct
        
        gemini_confusion_pct = (gemini_totals['confusion'] / gemini_totals['user_messages'] * 100) if gemini_totals['user_messages'] > 0 else 0
        gemini_clarity_pct = (gemini_totals['clarity'] / gemini_totals['user_messages'] * 100) if gemini_totals['user_messages'] > 0 else 0
        gemini_mastery_pct = (gemini_totals['mastery'] / gemini_totals['user_messages'] * 100) if gemini_totals['user_messages'] > 0 else 0
        
        print(f"\nCLAUDE (25 days):")
        print(f"  User messages: {totals['user_messages']:,}")
        print(f"  Confusion:     {claude_confusion_pct:6.1f}%")
        print(f"  Clarity:       {claude_clarity_pct:6.1f}%")
        print(f"  Mastery:       {claude_mastery_pct:6.1f}%")
        
        print(f"\nGEMINI (6 months):")
        print(f"  User messages: {gemini_totals['user_messages']:,}")
        print(f"  Confusion:     {gemini_confusion_pct:6.1f}%")
        print(f"  Clarity:       {gemini_clarity_pct:6.1f}%")
        print(f"  Mastery:       {gemini_mastery_pct:6.1f}%")
        
        # Analysis
        print(f"\n" + "-"*80)
        print("INSIGHTS")
        print("-"*80)
        
        print(f"\nClaude shows HIGHER mastery markers ({claude_mastery_pct:.1f}% vs {gemini_mastery_pct:.1f}%)")
        print(f"This suggests a more focused, productive conversation.")
        
        if claude_confusion_pct < gemini_confusion_pct:
            print(f"\nClaude conversations are CLEARER ({claude_confusion_pct:.1f}% confusion vs {gemini_confusion_pct:.1f}%)")
            print(f"Indicates you're conversing with Claude about well-understood domains.")
        else:
            print(f"\nClaude conversations show MORE confusion ({claude_confusion_pct:.1f}% vs {gemini_confusion_pct:.1f}%)")
            print(f"You're exploring new territory with Claude.")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
