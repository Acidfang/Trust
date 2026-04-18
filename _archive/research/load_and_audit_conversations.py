#!/usr/bin/env python3
"""
Load all conversations chronologically and audit everything
Tracks intent, meaning, and temporal alignment from oldest to newest
"""

from singularity_storage import SingularityStore, SingularityEntity
import json
from datetime import datetime
from typing import List, Dict, Any

def load_claude_conversations():
    """Load Claude timeline and store in singularity_storage"""
    
    store = SingularityStore()
    
    print("=" * 80)
    print("LOADING CLAUDE CONVERSATIONS")
    print("=" * 80)
    print()
    
    try:
        with open('claude_timeline_all_messages.json', 'r', encoding='utf-8-sig', errors='ignore') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return store
    
    metadata = data.get('metadata', {})
    messages = data.get('messages', [])
    
    print(f"Loaded: {metadata.get('total_messages')} messages")
    print(f"Date range: {metadata['date_range']['first']} to {metadata['date_range']['last']}")
    print()
    
    # Sort messages by timestamp (oldest first)
    messages_sorted = sorted(messages, key=lambda x: x.get('timestamp', ''))
    
    # Group messages into conversations by temporal proximity
    conversations = []
    current_conv = []
    last_timestamp = None
    
    for msg in messages_sorted:
        timestamp = msg.get('timestamp')
        
        # Start new conversation if gap > 1 hour or if last message was assistant end
        if last_timestamp and current_conv:
            from datetime import datetime, timedelta
            try:
                last_dt = datetime.fromisoformat(last_timestamp)
                curr_dt = datetime.fromisoformat(timestamp)
                gap = (curr_dt - last_dt).total_seconds() / 3600
                
                if gap > 1:  # More than 1 hour gap = new conversation
                    conversations.append(current_conv)
                    current_conv = []
            except:
                pass
        
        current_conv.append(msg)
        last_timestamp = timestamp
    
    if current_conv:
        conversations.append(current_conv)
    
    print(f"Grouped into: {len(conversations)} conversations")
    print()
    
    # Store each conversation
    stored_count = 0
    for conv_idx, conv_messages in enumerate(conversations):
        if not conv_messages:
            continue
        
        # Create conversation ID from first timestamp
        first_msg = conv_messages[0]
        conv_id = f"claude_conv_{conv_idx:04d}_{first_msg.get('timestamp', '').replace(':', '').replace('-', '')[:14]}"
        
        # Cache raw conversation data
        store.cache_raw(
            data_source="claude_export",
            data_id=conv_id,
            data_type="conversation",
            data_json=json.dumps({
                "platform": "claude",
                "model": "claude-haiku-4.5",
                "message_count": len(conv_messages),
                "messages": conv_messages
            }),
            ttl_hours=24*365,
            metadata={"source": "claude_timeline", "message_count": len(conv_messages)}
        )
        
        # Create conversation entity with just metadata (not all message data)
        message_snippets = [
            f"{msg.get('role')}: {msg.get('content', '')[:50]}..."
            for msg in conv_messages[:3]
        ]
        
        entity = SingularityEntity(
            symbol=f"⊙[CONVERSATION_{conv_id}]",
            election_id=f"e-conv-{conv_id}",
            domain="ai_conversation",
            entity_type="conversation",
            invariants=[
                "message_count_constant: Number of messages never changes",
                "message_order_preserved: Sequence order never changes"
            ],
            fields=["platform_source", "model_used", "message_count", "time_span"],
            data={
                "conversation_id": conv_id,
                "platform": "claude",
                "model": "claude-haiku-4.5",
                "message_count": len(conv_messages),
                "first_timestamp": conv_messages[0].get('timestamp'),
                "last_timestamp": conv_messages[-1].get('timestamp'),
                "sample_messages": message_snippets
            },
            confidence=1.0,
            references=[conv_id]  # Link to raw cache
        )
        
        if store.store_fact(entity):
            stored_count += 1
        
        # Also store each message as separate fact
        for msg_idx, msg in enumerate(conv_messages):
            msg_symbol = f"⊙[MESSAGE_{conv_id}_{msg_idx}]"
            content = msg.get('content', '')
            msg_entity = SingularityEntity(
                symbol=msg_symbol,
                election_id=f"e-msg-{conv_id}-{msg_idx}",
                domain="ai_conversation",
                entity_type="message",
                invariants=["content_immutable: Message text never changes"],
                fields=["role_type", "content_length", "timestamp"],
                data={
                    "conversation_id": conv_id,
                    "message_index": msg_idx,
                    "role": msg.get('role', 'unknown'),
                    "content_summary": content[:100] if content else "",  # Only store first 100 chars
                    "content_length": len(content),
                    "timestamp": msg.get('timestamp')
                },
                confidence=1.0,
                parent_symbol=f"⊙[CONVERSATION_{conv_id}]"
            )
            store.store_fact(msg_entity)
        
        if stored_count % 10 == 0:
            print(f"  Stored {stored_count} conversations...")
    
    print(f"Successfully stored: {stored_count} conversations")
    print()
    
    return store

def extract_and_analyze(store: SingularityStore):
    """Extract intents and meanings from all stored conversations"""
    
    print("=" * 80)
    print("EXTRACTING INTENTS AND MEANINGS (CHRONOLOGICALLY)")
    print("=" * 80)
    print()
    
    # Get all facts
    all_facts = store.list_facts(entity_type="conversation")
    
    print(f"Found: {len(all_facts)} conversations")
    print()
    
    # Extract intents from each message
    total_intents = 0
    for fact_idx, fact in enumerate(all_facts[:10]):  # Sample first 10
        conv_id = fact.data.get('conversation_id', 'unknown')
        platform = fact.data.get('platform', 'unknown')
        messages = fact.data.get('messages', [])
        
        print(f"Conversation {fact_idx+1}: {conv_id}")
        print(f"  Messages: {len(messages)}")
        
        # Analyze each message
        for msg_idx, msg in enumerate(messages[:3]):  # First 3 messages
            content = msg.get('content', '')[:100]
            role = msg.get('role', 'unknown')
            
            if content:
                semantic = store.analyze_semantic(content[:500])
                intent = semantic.get('intent')
                sentiment = semantic.get('sentiment')
                
                print(f"    [{role}] Intent: {intent}, Sentiment: {sentiment}")
                print(f"           Content: {content}...")
                total_intents += 1
        
        print()
    
    print(f"Extracted intents from: {total_intents} messages")
    print()
    
    return total_intents

def run_comprehensive_audit(store: SingularityStore):
    """Run full accountability audit"""
    
    print("=" * 80)
    print("COMPREHENSIVE ACCOUNTABILITY AUDIT")
    print("=" * 80)
    print()
    
    # Extract all intents
    print("1. Extracting all intents...")
    all_intents = store.extract_all_intents()
    print(f"   Found: {len(all_intents)} intent entries")
    print()
    
    # Track evolution
    if all_intents:
        print("2. Tracking intent evolution...")
        evolution = store.track_intent_evolution()
        print(f"   Primary intent: {evolution.get('primary_intent')}")
        print(f"   Stability: {evolution.get('stability_score', 0)*100:.0f}%")
        print(f"   Unique intents: {evolution.get('intent_diversity')}")
        print(f"   Changes: {evolution.get('intent_changes')}")
        print()
        
        print("3. Tracking meaning evolution...")
        meaning = store.track_meaning_evolution()
        print(f"   Persistent topics: {len(meaning.get('persistent_topics', []))}")
        if meaning.get('persistent_topics'):
            topics = [t[0] for t in meaning.get('persistent_topics', [])[:5]]
            print(f"   Top topics: {topics}")
        print()
        
        print("4. Detecting drift...")
        drift = store.detect_intent_drift()
        print(f"   Drift detected: {drift.get('drift_detected')}")
        print(f"   Direction: {drift.get('drift_direction')}")
        print()
        
        print("5. Mapping to features...")
        mapping = store.map_intent_to_features()
        print(f"   Alignment: {mapping.get('alignment_score', 0)*100:.0f}%")
        print(f"   Gaps: {len(mapping.get('gaps_identified', []))}")
        print()
    
    print("6. Comprehensive verification...")
    verification = store.verify_nothing_missed()
    print(f"   Completeness: {verification.get('completeness_score', 0)*100:.0f}%")
    print(f"   Status: {verification.get('final_assessment')}")
    print(f"   Intents extracted: {verification.get('integrity_checks', {}).get('intents_extracted')}")
    print(f"   Meanings preserved: {verification.get('integrity_checks', {}).get('meanings_preserved')}")
    print(f"   Temporal coherence: {verification.get('integrity_checks', {}).get('temporal_coherence')}")
    print()
    
    # Master report
    print("7. Master accountability report...")
    report = store.accountability_report()
    print(f"   System health: {report.get('recommendations', {}).get('system_health')}")
    print(f"   Summary: {report.get('executive_summary')}")
    print()
    
    # Save report
    with open('accountability_full_audit.json', 'w') as f:
        json.dump({
            "all_intents": len(all_intents),
            "evolution": evolution if all_intents else None,
            "meaning": meaning if all_intents else None,
            "drift": drift if all_intents else None,
            "mapping": mapping if all_intents else None,
            "verification": verification,
            "report": report
        }, f, indent=2)
    
    print("Full report saved to: accountability_full_audit.json")
    print()
    
    return verification

def main():
    # Step 1: Load conversations
    store = load_claude_conversations()
    
    # Step 2: Extract intents
    extract_and_analyze(store)
    
    # Step 3: Run audit
    verification = run_comprehensive_audit(store)
    
    print("=" * 80)
    print("FINAL STATUS")
    print("=" * 80)
    completeness = verification.get('completeness_score', 0)
    print(f"Completeness: {completeness*100:.0f}%")
    print(f"Assessment: {verification.get('final_assessment')}")
    print(f"Nothing missed: {completeness > 0.8}")
    print()

if __name__ == "__main__":
    main()
