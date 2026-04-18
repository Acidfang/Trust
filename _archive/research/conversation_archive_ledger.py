#!/usr/bin/env python3
"""
COMPLETE CONVERSATION ARCHIVE SYSTEM

Unified ledger for ALL conversations with ALL AIs:
- Questions you asked
- Responses you received
- Cross-AI comparison
- Full dialogue preservation
- Searchable by topic, theme, etc.

Supports:
- Gemini JSON exports (conversations + responses)
- Claude conversation history
- ChatGPT exports
- Custom Q&A formats
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import hashlib
from collections import defaultdict


class ConversationArchiveLedger:
    """Complete conversation archive with Q&A pairs."""
    
    def __init__(self):
        """Initialize archive."""
        self.conversations = {}  # conv_id -> full conversation
        self.qa_pairs = []  # List of (question, answer, metadata)
        self.index = defaultdict(list)  # keyword -> [conv_id]
        self.stats = {
            "total_conversations": 0,
            "total_qa_pairs": 0,
            "total_words": 0,
            "by_source": defaultdict(int)
        }
    
    def load_gemini_json(self, json_path: str, source: str = "gemini") -> Dict:
        """Load Gemini JSON export with conversations."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different Gemini formats
            conversations = []
            if isinstance(data, dict):
                if 'conversations' in data:
                    conversations = data['conversations']
                elif 'entries' in data:
                    conversations = data['entries']
                else:
                    conversations = [data]
            else:
                conversations = data if isinstance(data, list) else [data]
            
            loaded_count = 0
            qa_count = 0
            
            for conv_data in conversations:
                conv_id = self._generate_conv_id(conv_data)
                
                # Extract conversation structure
                conv_obj = {
                    "id": conv_id,
                    "source": source,
                    "loaded_at": datetime.now().isoformat(),
                    "messages": [],
                    "title": "",
                    "qa_pairs": []
                }
                
                # Parse messages depending on format
                messages = self._extract_messages(conv_data)
                
                if messages:
                    conv_obj["messages"] = messages
                    conv_obj["title"] = self._extract_title(messages)
                    
                    # Extract Q&A pairs
                    qa_pairs = self._extract_qa_pairs(messages, conv_id, source)
                    conv_obj["qa_pairs"] = qa_pairs
                    qa_count += len(qa_pairs)
                    
                    # Index conversation
                    self.conversations[conv_id] = conv_obj
                    self.qa_pairs.extend(qa_pairs)
                    self._index_conversation(conv_obj)
                    
                    loaded_count += 1
                    self.stats["by_source"][source] += 1
            
            self.stats["total_conversations"] += loaded_count
            self.stats["total_qa_pairs"] += qa_count
            
            return {
                "status": "loaded",
                "source": source,
                "conversations": loaded_count,
                "qa_pairs": qa_count
            }
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _extract_messages(self, conv_data: Any) -> List[Dict]:
        """Extract messages from various formats."""
        messages = []
        
        if isinstance(conv_data, dict):
            # Try common message list fields
            for field in ["messages", "turns", "exchanges", "history"]:
                if field in conv_data and isinstance(conv_data[field], list):
                    messages = conv_data[field]
                    break
            
            # If still empty, try nested structure
            if not messages:
                if "conversation" in conv_data:
                    messages = conv_data["conversation"]
                elif "content" in conv_data:
                    messages = [conv_data]
        
        elif isinstance(conv_data, list):
            messages = conv_data
        
        # Normalize messages
        normalized = []
        for msg in messages:
            if isinstance(msg, dict):
                normalized.append(msg)
            elif isinstance(msg, str):
                normalized.append({"text": msg})
        
        return normalized
    
    def _extract_title(self, messages: List[Dict]) -> str:
        """Extract conversation title from first message."""
        if not messages:
            return "Untitled Conversation"
        
        first = messages[0]
        if isinstance(first, dict):
            text = first.get("text", first.get("content", str(first)))
        else:
            text = str(first)
        
        # Get first 80 chars as title
        title = text[:80].strip()
        if len(text) > 80:
            title += "..."
        
        return title
    
    def _extract_qa_pairs(self, messages: List[Dict], conv_id: str, source: str) -> List[Dict]:
        """Extract question-answer pairs from messages."""
        qa_pairs = []
        
        i = 0
        while i < len(messages):
            if i + 1 < len(messages):
                q_msg = messages[i]
                a_msg = messages[i + 1]
                
                question = self._get_message_text(q_msg)
                answer = self._get_message_text(a_msg)
                
                if question and answer:
                    qa_pair = {
                        "id": hashlib.sha256(f"{conv_id}{i}".encode()).hexdigest()[:16],
                        "conversation_id": conv_id,
                        "source": source,
                        "question": question[:500],
                        "answer": answer[:1000],
                        "question_length": len(question),
                        "answer_length": len(answer),
                        "index_in_conversation": i,
                        "timestamp": datetime.now().isoformat()
                    }
                    qa_pairs.append(qa_pair)
                    self.stats["total_words"] += len(question.split()) + len(answer.split())
                
                i += 2
            else:
                i += 1
        
        return qa_pairs
    
    def _get_message_text(self, msg: Any) -> str:
        """Extract text from message object."""
        if isinstance(msg, str):
            return msg
        elif isinstance(msg, dict):
            for field in ["text", "content", "message", "body"]:
                if field in msg:
                    return str(msg[field])
        
        return str(msg) if msg else ""
    
    def _generate_conv_id(self, conv_data: Any) -> str:
        """Generate unique conversation ID."""
        text = str(conv_data)[:100]
        return hashlib.sha256(text.encode()).hexdigest()[:16]
    
    def _index_conversation(self, conv_obj: Dict):
        """Index conversation for search."""
        conv_id = conv_obj["id"]
        
        # Index title
        title = conv_obj.get("title", "")
        for word in title.lower().split():
            if len(word) > 3:
                self.index[word].append(conv_id)
        
        # Index Q&A content (key words)
        for qa in conv_obj.get("qa_pairs", []):
            for word in qa["question"].lower().split()[:10]:  # First 10 words
                if len(word) > 3:
                    self.index[word].append(conv_id)
    
    def search_archive(self, query: str, search_type: str = "all") -> List[Dict]:
        """
        Search archive.
        search_type: 'all', 'questions', 'answers', 'conversations'
        """
        query_lower = query.lower()
        results = []
        
        if search_type in ["all", "conversations"]:
            # Search conversations by title
            for conv_id, conv in self.conversations.items():
                if query_lower in conv.get("title", "").lower():
                    results.append({
                        "type": "conversation",
                        "id": conv_id,
                        "title": conv["title"],
                        "source": conv["source"],
                        "message_count": len(conv.get("messages", [])),
                        "qa_count": len(conv.get("qa_pairs", []))
                    })
        
        if search_type in ["all", "questions"]:
            # Search questions
            for qa in self.qa_pairs:
                if query_lower in qa["question"].lower():
                    results.append({
                        "type": "question",
                        "id": qa["id"],
                        "question": qa["question"][:200],
                        "source": qa["source"],
                        "length": qa["question_length"]
                    })
        
        if search_type in ["all", "answers"]:
            # Search answers
            for qa in self.qa_pairs:
                if query_lower in qa["answer"].lower():
                    results.append({
                        "type": "answer",
                        "id": qa["id"],
                        "question": qa["question"][:100],
                        "answer": qa["answer"][:200],
                        "source": qa["source"]
                    })
        
        return results[:30]  # Return top 30
    
    def get_conversation(self, conv_id: str) -> Optional[Dict]:
        """Get complete conversation by ID."""
        return self.conversations.get(conv_id)
    
    def get_qa_pair(self, qa_id: str) -> Optional[Dict]:
        """Get specific Q&A pair."""
        for qa in self.qa_pairs:
            if qa["id"] == qa_id:
                return qa
        return None
    
    def compare_by_source(self) -> Dict:
        """Compare conversations across sources."""
        comparison = {}
        
        for source, count in self.stats["by_source"].items():
            convs = [c for c in self.conversations.values() if c["source"] == source]
            qa_count = sum(len(c.get("qa_pairs", [])) for c in convs)
            
            avg_msg_len = 0
            if convs:
                avg_msg_len = sum(len(c.get("messages", [])) for c in convs) // len(convs)
            
            comparison[source] = {
                "conversations": count,
                "qa_pairs": qa_count,
                "avg_messages_per_conv": avg_msg_len
            }
        
        return comparison
    
    def export_archive(self, output_path: str) -> Dict:
        """Export complete archive."""
        export_data = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "system": "conversation_archive_ledger",
                "total_conversations": len(self.conversations),
                "total_qa_pairs": len(self.qa_pairs),
                "total_words": self.stats["total_words"]
            },
            "statistics": dict(self.stats),
            "conversations": list(self.conversations.values()),
            "qa_pairs": self.qa_pairs
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return {
            "status": "exported",
            "path": output_path,
            "conversations": len(self.conversations),
            "qa_pairs": len(self.qa_pairs)
        }
    
    def print_statistics(self):
        """Print archive statistics."""
        print("\n" + "="*70)
        print("CONVERSATION ARCHIVE STATISTICS")
        print("="*70)
        print(f"Total Conversations: {self.stats['total_conversations']}")
        print(f"Total Q&A Pairs: {self.stats['total_qa_pairs']}")
        print(f"Total Words: {self.stats['total_words']:,}")
        print(f"\nBy Source:")
        for source, count in self.stats['by_source'].items():
            print(f"  • {source}: {count} conversations")
        print("="*70 + "\n")
    
    def interactive_interface(self):
        """Interactive archive browser."""
        print("\n" + "="*70)
        print("CONVERSATION ARCHIVE BROWSING SYSTEM")
        print("="*70)
        print("\nCommands:")
        print("  load <path>              - Load Gemini/AI JSON export")
        print("  search <term>            - Search all content")
        print("  search-q <term>          - Search questions only")
        print("  search-a <term>          - Search answers only")
        print("  conversations            - List all conversations")
        print("  show <conv_id>           - Show conversation")
        print("  qa <qa_id>               - Show Q&A pair")
        print("  stats                    - Show statistics")
        print("  compare                  - Compare by source")
        print("  export <path>            - Export archive")
        print("  quit                     - Exit")
        print("="*70 + "\n")
        
        while True:
            try:
                cmd = input("archive> ").strip()
                
                if not cmd:
                    continue
                
                parts = cmd.split(' ', 1)
                command = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else ""
                
                if command == "quit":
                    print("Goodbye.")
                    break
                
                elif command == "load" and arg:
                    print(f"  Loading from {arg}...")
                    result = self.load_gemini_json(arg)
                    if result["status"] == "loaded":
                        print(f"  ✓ {result['conversations']} conversations ({result['qa_pairs']} Q&A pairs)")
                    else:
                        print(f"  ✗ Error: {result.get('message')}")
                
                elif command == "search" and arg:
                    results = self.search_archive(arg, "all")
                    print(f"\n✓ Found {len(results)} results for '{arg}':")
                    for i, r in enumerate(results[:5], 1):
                        if r["type"] == "conversation":
                            print(f"  {i}. [CONV] {r['title'][:60]} ({r['source']})")
                        elif r["type"] == "question":
                            print(f"  {i}. [Q] {r['question'][:60]}")
                        else:
                            print(f"  {i}. [A] {r['answer'][:60]}")
                    if len(results) > 5:
                        print(f"  ... and {len(results) - 5} more")
                
                elif command == "search-q" and arg:
                    results = self.search_archive(arg, "questions")
                    print(f"\n✓ Found {len(results)} questions:")
                    for r in results[:5]:
                        print(f"  • {r['question'][:70]}")
                
                elif command == "search-a" and arg:
                    results = self.search_archive(arg, "answers")
                    print(f"\n✓ Found {len(results)} answers:")
                    for r in results[:5]:
                        print(f"  • {r['answer'][:70]}")
                
                elif command == "conversations":
                    print(f"\n✓ {len(self.conversations)} Conversations:")
                    for conv_id, conv in list(self.conversations.items())[:10]:
                        print(f"  • [{conv['source']}] {conv['title'][:50]}")
                    if len(self.conversations) > 10:
                        print(f"  ... and {len(self.conversations) - 10} more")
                
                elif command == "show" and arg:
                    conv = self.get_conversation(arg)
                    if conv:
                        print(f"\n{'='*70}")
                        print(f"Conversation: {conv['title']}")
                        print(f"Source: {conv['source']} | Messages: {len(conv.get('messages', []))}")
                        print(f"Q&A Pairs: {len(conv.get('qa_pairs', []))}")
                        print(f"{'='*70}")
                        for i, qa in enumerate(conv.get("qa_pairs", [])[:3], 1):
                            print(f"\n{i}. Q: {qa['question'][:100]}")
                            print(f"   A: {qa['answer'][:100]}...")
                    else:
                        print(f"  Conversation '{arg}' not found")
                
                elif command == "qa" and arg:
                    qa = self.get_qa_pair(arg)
                    if qa:
                        print(f"\n{'='*70}")
                        print(f"Q: {qa['question']}")
                        print(f"\n---\n")
                        print(f"A: {qa['answer']}")
                        print(f"{'='*70}")
                    else:
                        print(f"  Q&A pair '{arg}' not found")
                
                elif command == "stats":
                    self.print_statistics()
                
                elif command == "compare":
                    comparison = self.compare_by_source()
                    print("\n✓ Comparison by Source:")
                    for source, data in comparison.items():
                        print(f"\n  {source}:")
                        print(f"    Conversations: {data['conversations']}")
                        print(f"    Q&A Pairs: {data['qa_pairs']}")
                        print(f"    Avg Messages/Conv: {data['avg_messages_per_conv']}")
                
                elif command == "export" and arg:
                    result = self.export_archive(arg)
                    if result["status"] == "exported":
                        print(f"  ✓ Exported {result['conversations']} conversations ({result['qa_pairs']} QA pairs)")
                        print(f"    Path: {result['path']}")
                    else:
                        print(f"  ✗ Error: {result.get('message')}")
                
                else:
                    print(f"  Unknown command: {command}")
            
            except KeyboardInterrupt:
                print("\nGoodbye.")
                break
            except Exception as e:
                print(f"  Error: {e}")


def main():
    """Main execution."""
    archive = ConversationArchiveLedger()
    print("CONVERSATION ARCHIVE SYSTEM")
    print("="*70)
    print("Collecting ALL conversations from ALL AIs in one place...")
    
    # Try loading Gemini exports if available
    gemini_db = "gemini_consolidated_database.json"
    if Path(gemini_db).exists():
        print(f"\nLoading {gemini_db}...")
        result = archive.load_gemini_json(gemini_db, "gemini")
        if result["status"] == "loaded":
            print(f"  ✓ {result['conversations']} conversations with {result['qa_pairs']} Q&A pairs")
    
    archive.print_statistics()
    archive.interactive_interface()


if __name__ == "__main__":
    main()
