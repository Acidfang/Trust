#!/usr/bin/env python3
"""
Load ALL AI conversations (Gemini, Claude, ChatGPT/Copilot) and run unified accountability audit
"""

from singularity_storage import SingularityStore, SingularityEntity
import json
from datetime import datetime
from typing import List, Dict, Any

def load_all_conversations():
    """Load all AI conversations from unified timeline"""
    
    store = SingularityStore()
    
    print("=" * 80)
    print("LOADING ALL AI CONVERSATIONS (UNIFIED TIMELINE)")
    print("=" * 80)
    print()
    
    # Try loading unified master timeline first
    timeline_files = [
        ('UNIFIED_MASTER_TIMELINE.json', 'unified_master'),
        ('timeline_all_messages_unified.json', 'unified'),
        ('UNIFIED_CONVERSATION_TIMELINE_COMPLETE.json', 'unified_complete'),
        ('gemini_consolidated_database.json', 'gemini'),
        ('claude_timeline_all_messages.json', 'claude'),
        ('copilot_timeline_all_messages.json', 'copilot')
    ]
    
    total_messages = 0
    platforms_loaded = {}
    all_conversations = []
    
    for filename, source_type in timeline_files:
        try:
            print(f"Loading {filename}...")
            with open(filename, 'r', encoding='utf-8-sig', errors='ignore') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            messages = []
            metadata = {}
            
            if isinstance(data, dict):
                if 'messages' in data:
                    messages = data.get('messages', [])
                    metadata = data.get('metadata', {})
                elif 'conversations' in data:
                    # Array of conversations
                    for conv in data.get('conversations', []):
                        if isinstance(conv, dict) and 'messages' in conv:
                            messages.extend(conv['messages'])
                elif 'data' in data:
                    messages = data.get('data', [])
                else:
                    # Try to get values
                    for key in data:
                        if isinstance(data[key], list) and len(data[key]) > 0:
                            if isinstance(data[key][0], dict) and any(k in data[key][0] for k in ['content', 'text', 'message']):
                                messages = data[key]
                                break
            elif isinstance(data, list):
                messages = data
            
            if messages:
                print(f"  Found: {len(messages)} messages")
                
                # Detect platform from filename or content
                if 'gemini' in filename.lower():
                    platform = 'gemini'
                elif 'claude' in filename.lower():
                    platform = 'claude'
                elif 'copilot' in filename.lower():
                    platform = 'copilot'
                elif 'unified' in filename.lower():
                    platform = 'unified'
                else:
                    platform = 'unknown'
                
                # Store all messages from this file
                all_conversations.append({
                    'platform': platform,
                    'source': filename,
                    'messages': messages,
                    'count': len(messages)
                })
                
                total_messages += len(messages)
                platforms_loaded[platform] = platforms_loaded.get(platform, 0) + len(messages)
                print(f"  Platform: {platform}")
                print()
        
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"  Error: {e}")
            print()
    
    print(f"Total messages loaded: {total_messages}")
    print(f"Platforms: {platforms_loaded}")
    print()
    
    # Now store in singularity format
    print("=" * 80)
    print("STORING IN SINGULARITY FORMAT")
    print("=" * 80)
    print()
    
    stored_count = 0
    for conv_source in all_conversations:
        platform = conv_source['platform']
        filename = conv_source['source']
        messages = conv_source['messages']
        
        # Sort by timestamp
        def get_timestamp(msg):
            if isinstance(msg, dict):
                for ts_key in ['timestamp', 'created_at', 'date', 'time']:
                    if ts_key in msg:
                        return msg[ts_key]
            return ''
        
        try:
            messages_sorted = sorted(messages, key=lambda x: get_timestamp(x))
        except:
            messages_sorted = messages
        
        # Group into conversations by temporal proximity (1 hour gap)
        conversations = []
        current_conv = []
        last_timestamp = None
        
        for msg in messages_sorted:
            timestamp = get_timestamp(msg)
            
            # Start new conversation if gap > 1 hour
            if last_timestamp and current_conv and timestamp:
                try:
                    from datetime import datetime, timedelta
                    # Try various timestamp formats
                    for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y%m%dT%H%M%S']:
                        try:
                            last_dt = datetime.strptime(str(last_timestamp)[:19], fmt)
                            curr_dt = datetime.strptime(str(timestamp)[:19], fmt)
                            gap = (curr_dt - last_dt).total_seconds() / 3600
                            
                            if gap > 1:  # More than 1 hour gap
                                conversations.append(current_conv)
                                current_conv = []
                            break
                        except:
                            pass
                except:
                    pass
            
            current_conv.append(msg)
            last_timestamp = timestamp
        
        if current_conv:
            conversations.append(current_conv)
        
        print(f"{platform} from {filename}:")
        print(f"  Messages: {len(messages)}")
        print(f"  Conversations: {len(conversations)}")
        
        # Store each conversation group
        for conv_idx, conv_messages in enumerate(conversations):
            if not conv_messages:
                continue
            
            first_msg = conv_messages[0]
            conv_id = f"{platform}_conv_{conv_idx:04d}_{get_timestamp(first_msg)[:10].replace('-', '')}"
            
            # Create conversation entity
            entity = SingularityEntity(
                symbol=f"⊙[CONVERSATION_{conv_id}]",
                election_id=f"e-conv-{conv_id}",
                domain="ai_conversation",
                entity_type="conversation",
                invariants=[
                    "message_count_constant",
                    "order_preserved"
                ],
                fields=["platform", "message_count", "time_span"],
                data={
                    "conversation_id": conv_id,
                    "platform": platform,
                    "message_count": len(conv_messages),
                    "first_timestamp": get_timestamp(conv_messages[0]),
                    "last_timestamp": get_timestamp(conv_messages[-1])
                },
                confidence=1.0,
                references=[conv_id]
            )
            
            if store.store_fact(entity):
                stored_count += 1
                
                # Store individual messages
                for msg_idx, msg in enumerate(conv_messages):
                    msg_symbol = f"⊙[MESSAGE_{conv_id}_{msg_idx}]"
                    
                    # Extract content
                    content = ""
                    role = "unknown"
                    
                    if isinstance(msg, dict):
                        content = msg.get('content', '') or msg.get('text', '') or msg.get('message', '')
                        role = msg.get('role', '') or msg.get('author', '') or msg.get('sender', '')
                    
                    msg_entity = SingularityEntity(
                        symbol=msg_symbol,
                        election_id=f"e-msg-{conv_id}-{msg_idx}",
                        domain="ai_conversation",
                        entity_type="message",
                        invariants=["content_immutable"],
                        fields=["role", "content_length", "timestamp"],
                        data={
                            "conversation_id": conv_id,
                            "message_index": msg_idx,
                            "platform": platform,
                            "role": role,
                            "content_summary": content[:100] if content else "",
                            "content_length": len(content),
                            "timestamp": get_timestamp(msg)
                        },
                        confidence=1.0,
                        parent_symbol=f"⊙[CONVERSATION_{conv_id}]"
                    )
                    store.store_fact(msg_entity)
        
        print()
    
    print(f"Successfully stored: {stored_count} conversations")
    print()
    
    return store

def run_unified_audit(store: SingularityStore):
    """Run comprehensive accountability audit across all platforms"""
    
    print("=" * 80)
    print("UNIFIED ACCOUNTABILITY AUDIT (ALL PLATFORMS)")
    print("=" * 80)
    print()
    
    # Extract all intents
    print("1. Extracting all intents...")
    all_intents = store.extract_all_intents()
    print(f"   Found: {len(all_intents)} intent entries")
    print()
    
    # Analyze by platform
    print("2. Platform breakdown...")
    platform_data = {}
    for intent in all_intents:
        platform = intent.get('full_entry', {}).get('platform', 'unknown')
        if platform not in platform_data:
            platform_data[platform] = []
        platform_data[platform].append(intent)
    
    for platform, intents in sorted(platform_data.items()):
        print(f"   {platform}: {len(intents)} messages")
    print()
    
    # Track evolution
    print("3. Intent evolution...")
    evolution = store.track_intent_evolution()
    print(f"   Primary intent: {evolution.get('primary_intent')}")
    print(f"   Stability: {evolution.get('stability_score', 0)*100:.1f}%")
    print(f"   Unique intents: {evolution.get('intent_diversity', 0)}")
    print()
    
    # Verify completeness
    print("4. Comprehensive verification...")
    verification = store.verify_nothing_missed()
    print(f"   Completeness: {verification.get('completeness_score', 0)*100:.1f}%")
    print(f"   Status: {verification.get('final_assessment')}")
    print(f"   Intents extracted: {verification.get('integrity_checks', {}).get('intents_extracted')}")
    print(f"   Temporal coherence: {verification.get('integrity_checks', {}).get('temporal_coherence')}")
    print()
    
    # Master report
    print("5. Master accountability report...")
    report = store.accountability_report()
    print(f"   System health: {report.get('recommendations', {}).get('system_health')}")
    print(f"   Summary: {report.get('executive_summary')}")
    print()
    
    # Save unified report
    unified_report = {
        "audit_type": "UNIFIED_ALL_PLATFORMS",
        "timestamp": datetime.now().isoformat(),
        "total_messages": len(all_intents),
        "platform_breakdown": {p: len(d) for p, d in platform_data.items()},
        "primary_intent": evolution.get('primary_intent'),
        "stability": evolution.get('stability_score', 0),
        "completeness": verification.get('completeness_score', 0),
        "verification_status": verification.get('final_assessment'),
        "all_platforms_captured": list(platform_data.keys()),
        "intents_detected": evolution.get('intent_diversity', 0),
        "report_summary": report.get('executive_summary')
    }
    
    with open('accountability_unified_all_platforms.json', 'w') as f:
        json.dump(unified_report, f, indent=2)
    
    print(f"Full report saved to: accountability_unified_all_platforms.json")
    print()
    
    return unified_report

def main():
    store = load_all_conversations()
    report = run_unified_audit(store)
    
    print("=" * 80)
    print("FINAL STATUS")
    print("=" * 80)
    print(f"Completeness: {report.get('completeness', 0)*100:.1f}%")
    print(f"Platforms covered: {', '.join(report.get('all_platforms_captured', []))}")
    print(f"Status: {report.get('verification_status')}")

if __name__ == '__main__':
    main()
