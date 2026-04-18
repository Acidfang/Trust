#!/usr/bin/env python3
"""Analyze patterns across all Gemini conversations"""

import json
from collections import Counter, defaultdict
from datetime import datetime

# Load timeline
with open('timeline_all_messages.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

messages = data['messages']

# Analysis 1: Top topics (word frequency in user messages)
print("="*80)
print("ANALYZING YOUR CONVERSATIONS WITH GEMINI")
print("="*80)

user_messages = [m['content'] for m in messages if m['role'] == 'user']
gemini_messages = [m['content'] for m in messages if m['role'] == 'gemini']

print(f"\nTotal messages: {len(messages)}")
print(f"Your messages: {len(user_messages)}")
print(f"Gemini's messages: {len(gemini_messages)}")
print(f"Date range: {data['metadata']['date_range']['first'][:10]} to {data['metadata']['date_range']['last'][:10]}")

# Extract key words (words > 4 chars)
word_freq = Counter()
for msg in user_messages:
    words = msg.lower().split()
    for word in words:
        clean_word = ''.join(c for c in word if c.isalnum())
        if len(clean_word) > 4:
            word_freq[clean_word] += 1

print("\n" + "-"*80)
print("TOP 25 CONCEPTS IN YOUR QUESTIONING")
print("-"*80)
for word, count in word_freq.most_common(25):
    print(f"  {word:20} {count:4} times")

# Analysis 2: Message length patterns
user_avg_len = sum(len(m) for m in user_messages) / len(user_messages) if user_messages else 0
gemini_avg_len = sum(len(m) for m in gemini_messages) / len(gemini_messages) if gemini_messages else 0

print("\n" + "-"*80)
print("MESSAGE CHARACTERISTICS")
print("-"*80)
print(f"  Your avg message length: {user_avg_len:.0f} characters")
print(f"  Gemini avg response length: {gemini_avg_len:.0f} characters")

# Find longest messages
longest_user = max(user_messages, key=len)
longest_gemini = max(gemini_messages, key=len)
print(f"\n  Your longest message: {len(longest_user)} chars")
print(f"  Gemini's longest response: {len(longest_gemini)} chars")

# Analysis 3: Sample key messages - looking for questions
print("\n" + "-"*80)
print("SAMPLE OF YOUR QUESTIONS (first 30 messages)")
print("-"*80)
sample_count = 0
for msg in messages[:100]:
    if msg['role'] == 'user' and sample_count < 30:
        preview = msg['content'][:100].replace('\n', ' ')
        print(f"  • {preview}")
        sample_count += 1

# Analysis 4: Themes over time
print("\n" + "-"*80)
print("CONVERSATION DENSITY BY MONTH")
print("-"*80)
by_month = defaultdict(int)
for msg in messages:
    month = msg['timestamp'][:7]  # YYYY-MM
    by_month[month] += 1

for month in sorted(by_month.keys()):
    count = by_month[month]
    bar = "█" * (count // 200)  # Scale bars
    print(f"  {month}: {count:5} messages {bar}")

print("\n" + "="*80)
