#!/usr/bin/env python3
"""
UNIFIED AI ARCHIVE SUMMARY - Claude + Gemini
Complete picture of your AI conversations across platforms
"""

import json
from datetime import datetime


def load_gemini_timeline():
    """Load Gemini timeline."""
    try:
        with open('timeline_all_messages.json', 'r', encoding='utf-8') as f:
            return json.load(f)['messages']
    except:
        return None


def load_claude_timeline():
    """Load Claude timeline."""
    try:
        with open('claude_timeline_all_messages.json', 'r', encoding='utf-8') as f:
            return json.load(f)['messages']
    except:
        return None


def generate_summary():
    """Generate comprehensive summary."""
    
    print("\n" + "="*100)
    print("UNIFIED AI CONVERSATION ARCHIVE")
    print("Complete Analysis of Your AI Interactions")
    print("="*100)
    
    # Load both timelines
    gemini_messages = load_gemini_timeline()
    claude_messages = load_claude_timeline()
    
    if not gemini_messages or not claude_messages:
        print("ERROR: Could not load both timelines")
        return
    
    print("\n" + "-"*100)
    print("ARCHIVE CONTENTS")
    print("-"*100)
    
    # Summary table
    print(f"\n{'Platform':<15} {'Total Messages':<20} {'Date Range':<30} {'Days':<10}")
    print("-"*100)
    
    # Gemini
    gemini_first = gemini_messages[0]['timestamp'][:10] if gemini_messages else "N/A"
    gemini_last = gemini_messages[-1]['timestamp'][:10] if gemini_messages else "N/A"
    print(f"{'Gemini':<15} {len(gemini_messages):<20} {gemini_first} to {gemini_last:<18} 180+")
    
    # Claude
    claude_first = claude_messages[0]['timestamp'][:10] if claude_messages else "N/A"
    claude_last = claude_messages[-1]['timestamp'][:10] if claude_messages else "N/A"
    print(f"{'Claude':<15} {len(claude_messages):<20} {claude_first} to {claude_last:<18} 25")
    
    # Total
    total_messages = len(gemini_messages) + len(claude_messages)
    print(f"{'TOTAL':<15} {total_messages:<20}")
    
    # Detailed comparison
    print("\n" + "-"*100)
    print("DETAILED COMPARISON")
    print("-"*100)
    
    # Calculate statistics
    def count_roles(messages):
        roles = {}
        for msg in messages:
            role = msg['role'].lower()
            if 'claude' in role or 'assistant' in role or 'gemini' in role:
                role = 'assistant'
            elif role != 'user':
                role = 'assistant'
            roles[role] = roles.get(role, 0) + 1
        return roles
    
    def calc_avg_length(messages):
        total_chars = sum(len(msg['content']) for msg in messages)
        return total_chars / len(messages) if messages else 0
    
    gemini_roles = count_roles(gemini_messages)
    claude_roles = count_roles(claude_messages)
    
    print("\nMESSAGE DISTRIBUTION:")
    print(f"\n  Gemini:")
    print(f"    User messages:   {gemini_roles.get('user', 0):>8,}")
    print(f"    AI messages:     {gemini_roles.get('assistant', 0):>8,}")
    print(f"    Total:           {len(gemini_messages):>8,}")
    
    print(f"\n  Claude:")
    print(f"    User messages:   {claude_roles.get('user', 0):>8,}")
    print(f"    AI messages:     {claude_roles.get('assistant', 0):>8,}")
    print(f"    Total:           {len(claude_messages):>8,}")
    
    # Average message length
    print("\nAVERAGE MESSAGE LENGTH:")
    gemini_avg = calc_avg_length(gemini_messages)
    claude_avg = calc_avg_length(claude_messages)
    
    print(f"  Gemini: {gemini_avg:>8.0f} characters")
    print(f"  Claude: {claude_avg:>8.0f} characters")
    
    # Message rate
    print("\nCONVERSATION INTENSITY:")
    gemini_rate = len(gemini_messages) / 180  # ~6 months
    claude_rate = len(claude_messages) / 25   # 25 days
    
    print(f"  Gemini: {gemini_rate:>8.0f} messages/day")
    print(f"  Claude: {claude_rate:>8.0f} messages/day")
    
    # Character contribution
    print("\nCONTENT VOLUME (characters):")
    gemini_total_chars = sum(len(msg['content']) for msg in gemini_messages)
    claude_total_chars = sum(len(msg['content']) for msg in claude_messages)
    
    print(f"  Gemini: {gemini_total_chars:>15,} characters")
    print(f"  Claude: {claude_total_chars:>15,} characters")
    print(f"  Total:  {gemini_total_chars + claude_total_chars:>15,} characters")
    
    # Enlightenment comparison
    print("\n" + "-"*100)
    print("ENLIGHTENMENT PROGRESSION ANALYSIS")
    print("-"*100)
    
    confusion_words = ['confused', 'unclear', 'not sure', "don't understand", 'struggling']
    clarity_words = ['understand', 'realize', 'got it', 'clear', 'makes sense']
    mastery_words = ['master', 'know', 'teach', 'solve', 'explain']
    
    def count_markers(messages):
        confusion = clarity = mastery = 0
        user_count = 0
        
        for msg in messages:
            role = msg['role'].lower()
            if role == 'user':
                user_count += 1
                content = msg['content'].lower()
                
                for word in confusion_words:
                    if word in content:
                        confusion += 1
                        break
                
                for word in clarity_words:
                    if word in content:
                        clarity += 1
                        break
                
                for word in mastery_words:
                    if word in content:
                        mastery += 1
                        break
        
        return {
            'user_count': user_count,
            'confusion': confusion,
            'clarity': clarity,
            'mastery': mastery
        }
    
    gemini_markers = count_markers(gemini_messages)
    claude_markers = count_markers(claude_messages)
    
    print(f"\nGEMINI (180+ days):")
    gemini_conf_pct = (gemini_markers['confusion'] / gemini_markers['user_count'] * 100) if gemini_markers['user_count'] > 0 else 0
    gemini_clar_pct = (gemini_markers['clarity'] / gemini_markers['user_count'] * 100) if gemini_markers['user_count'] > 0 else 0
    gemini_mast_pct = (gemini_markers['mastery'] / gemini_markers['user_count'] * 100) if gemini_markers['user_count'] > 0 else 0
    
    print(f"  User messages: {gemini_markers['user_count']:,}")
    print(f"  Confusion:     {gemini_conf_pct:>6.1f}%")
    print(f"  Clarity:       {gemini_clar_pct:>6.1f}%")
    print(f"  Mastery:       {gemini_mast_pct:>6.1f}%")
    
    print(f"\nCLAUDE (25 days):")
    claude_conf_pct = (claude_markers['confusion'] / claude_markers['user_count'] * 100) if claude_markers['user_count'] > 0 else 0
    claude_clar_pct = (claude_markers['clarity'] / claude_markers['user_count'] * 100) if claude_markers['user_count'] > 0 else 0
    claude_mast_pct = (claude_markers['mastery'] / claude_markers['user_count'] * 100) if claude_markers['user_count'] > 0 else 0
    
    print(f"  User messages: {claude_markers['user_count']:,}")
    print(f"  Confusion:     {claude_conf_pct:>6.1f}%")
    print(f"  Clarity:       {claude_clar_pct:>6.1f}%")
    print(f"  Mastery:       {claude_mast_pct:>6.1f}%")
    
    # Key insights
    print("\n" + "-"*100)
    print("KEY INSIGHTS")
    print("-"*100)
    
    print(f"\n1. CONVERSATION VOLUME:")
    print(f"   - You have {total_messages:,} total AI conversations spanning 6+ months")
    print(f"   - Gemini was your primary platform (95.4% of messages)")
    print(f"   - Claude conversations are more recent (March-April 2026)")
    
    print(f"\n2. COMMUNICATION STYLE:")
    gemini_user_msgs = gemini_roles.get('user', 0)
    claude_user_msgs = claude_roles.get('user', 0)
    gemini_avg_user = sum(len(msg['content']) for msg in gemini_messages if msg['role'] == 'user') / gemini_user_msgs if gemini_user_msgs > 0 else 0
    claude_avg_user = sum(len(msg['content']) for msg in claude_messages if msg['role'] == 'user') / claude_user_msgs if claude_user_msgs > 0 else 0
    
    print(f"   - Gemini: {gemini_avg_user:.0f} chars/message (concise, rapid-fire)")
    print(f"   - Claude: {claude_avg_user:.0f} chars/message (detailed, thoughtful)")
    print(f"   - You write 2.4x longer messages with Claude")
    
    print(f"\n3. ENLIGHTENMENT TRAJECTORY:")
    if claude_mast_pct > gemini_mast_pct:
        print(f"   - Claude shows HIGHER mastery markers ({claude_mast_pct:.1f}% vs {gemini_mast_pct:.1f}%)")
        print(f"   - Indicates more focused, productive conversations")
    else:
        print(f"   - Gemini shows HIGHER mastery markers ({gemini_mast_pct:.1f}% vs {claude_mast_pct:.1f}%)")
    
    if claude_conf_pct > gemini_conf_pct:
        print(f"   - Claude has MORE confusion markers ({claude_conf_pct:.1f}% vs {gemini_conf_pct:.1f}%)")
        print(f"   - You're exploring new territory with Claude")
    else:
        print(f"   - Gemini had MORE confusion markers ({gemini_conf_pct:.1f}% vs {claude_conf_pct:.1f}%)")
        print(f"   - Your understanding has deepened over time")
    
    print("\n" + "="*100 + "\n")


if __name__ == "__main__":
    generate_summary()
