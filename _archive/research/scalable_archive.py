#!/usr/bin/env python3
"""
SCALABLE CONVERSATION ARCHIVE

Optimized for 200+ conversations with efficient memory usage,
fast search, and batch processing.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Iterator
import hashlib
from collections import defaultdict
import pickle
import sqlite3


class ScalableConversationArchive:
    """Archive optimized for 200+ conversations."""
    
    def __init__(self, db_path: str = "conversation_archive.db"):
        """Initialize with SQLite backend for efficiency."""
        self.db_path = db_path
        self.init_database()
        self.index_cache = {}  # In-memory index for fast search
    
    def init_database(self):
        """Initialize SQLite database."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Create tables
        c.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                source TEXT,
                title TEXT,
                loaded_at TEXT,
                message_count INTEGER,
                qa_count INTEGER,
                content_length INTEGER,
                metadata TEXT
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS qa_pairs (
                id TEXT PRIMARY KEY,
                conversation_id TEXT,
                source TEXT,
                question TEXT,
                answer TEXT,
                q_length INTEGER,
                a_length INTEGER,
                FOREIGN KEY(conversation_id) REFERENCES conversations(id)
            )
        ''')
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS search_index (
                keyword TEXT,
                entry_type TEXT,
                entry_id TEXT,
                PRIMARY KEY(keyword, entry_type, entry_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_bulk_gemini(self, json_files: List[str], verbose: bool = True) -> Dict:
        """Load multiple Gemini JSON files efficiently."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        stats = {
            "total_loaded": 0,
            "total_conversations": 0,
            "total_qa_pairs": 0,
            "by_source": defaultdict(int),
            "errors": []
        }
        
        for i, filepath in enumerate(json_files, 1):
            if verbose:
                print(f"  [{i}/{len(json_files)}] {Path(filepath).name}...", end=" ", flush=True)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Handle different formats
                conversations = self._extract_conversations(data)
                
                for conv in conversations:
                    conv_id = hashlib.sha256(
                        (str(conv)[:100] + filepath).encode()
                    ).hexdigest()[:16]
                    
                    # Parse conversation
                    messages = self._extract_messages(conv)
                    title = self._extract_title(messages)
                    qa_pairs = self._extract_qa_pairs(messages, conv_id)
                    
                    # Store in DB
                    c.execute('''
                        INSERT OR REPLACE INTO conversations 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        conv_id, "gemini", title[:200], datetime.now().isoformat(),
                        len(messages), len(qa_pairs), 
                        sum(len(str(m)) for m in messages),
                        json.dumps({"source_file": filepath})
                    ))
                    
                    # Store Q&A pairs
                    for qa in qa_pairs:
                        c.execute('''
                            INSERT OR REPLACE INTO qa_pairs 
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            qa["id"], conv_id, "gemini",
                            qa["q"][:500], qa["a"][:1000],
                            len(qa["q"]), len(qa["a"])
                        ))
                    
                    # Index keywords
                    keywords = self._extract_keywords(title)
                    for keyword in keywords:
                        c.execute('''
                            INSERT OR IGNORE INTO search_index 
                            VALUES (?, ?, ?)
                        ''', (keyword, "conversation", conv_id))
                        
                        for qa in qa_pairs:
                            c.execute('''
                                INSERT OR IGNORE INTO search_index 
                                VALUES (?, ?, ?)
                            ''', (keyword, "qa", qa["id"]))
                    
                    stats["total_conversations"] += 1
                    stats["total_qa_pairs"] += len(qa_pairs)
                    stats["by_source"]["gemini"] += 1
                
                conn.commit()
                stats["total_loaded"] += 1
                if verbose:
                    print(f"✓ {len(conversations)} conversations")
            
            except Exception as e:
                stats["errors"].append({"file": filepath, "error": str(e)})
                if verbose:
                    print(f"✗ {str(e)}")
        
        conn.close()
        return stats
    
    def _extract_conversations(self, data):
        """Extract conversations from various formats."""
        if isinstance(data, dict):
            if "conversations" in data:
                return data["conversations"]
            elif "entries" in data:
                return data["entries"]
            else:
                return [data]
        elif isinstance(data, list):
            return data
        return [data]
    
    def _extract_messages(self, conv) -> List:
        """Extract messages from conversation."""
        if isinstance(conv, dict):
            for field in ["messages", "turns", "exchanges", "history"]:
                if field in conv and isinstance(conv[field], list):
                    return conv[field]
            if "conversation" in conv:
                return conv["conversation"]
        elif isinstance(conv, list):
            return conv
        return []
    
    def _extract_title(self, messages: List) -> str:
        """Extract title from first message."""
        if not messages:
            return "Untitled"
        first = messages[0]
        text = str(first.get("text") if isinstance(first, dict) else first)
        return text[:100].strip()
    
    def _extract_keywords(self, text: str, limit: int = 5) -> List[str]:
        """Extract keywords from text."""
        words = text.lower().split()
        stop_words = {"the", "a", "an", "and", "or", "is", "are"}
        keywords = [w for w in words if len(w) > 3 and w not in stop_words]
        return keywords[:limit]
    
    def _extract_qa_pairs(self, messages: List, conv_id: str) -> List[Dict]:
        """Extract Q&A pairs from messages."""
        qa_pairs = []
        i = 0
        while i + 1 < len(messages):
            q_msg = messages[i]
            a_msg = messages[i + 1]
            
            q_text = str(q_msg.get("text") if isinstance(q_msg, dict) else q_msg)
            a_text = str(a_msg.get("text") if isinstance(a_msg, dict) else a_msg)
            
            if q_text and a_text:
                qa_id = hashlib.sha256(f"{conv_id}{i}".encode()).hexdigest()[:16]
                qa_pairs.append({
                    "id": qa_id,
                    "q": q_text,
                    "a": a_text
                })
            
            i += 2
        
        return qa_pairs
    
    def search(self, query: str, limit: int = 50) -> List[Dict]:
        """Search archive - returns conversations and Q&A pairs."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        query_lower = query.lower()
        results = []
        
        # Search conversations by title
        c.execute('''
            SELECT DISTINCT id, title, message_count, qa_count 
            FROM conversations 
            WHERE title LIKE ?
            LIMIT ?
        ''', (f"%{query_lower}%", limit))
        
        for row in c.fetchall():
            results.append({
                "type": "conversation",
                "id": row[0],
                "title": row[1],
                "message_count": row[2],
                "qa_count": row[3]
            })
        
        # Search Q&A by question
        c.execute('''
            SELECT DISTINCT id, conversation_id, question, answer 
            FROM qa_pairs 
            WHERE question LIKE ? OR answer LIKE ?
            LIMIT ?
        ''', (f"%{query_lower}%", f"%{query_lower}%", limit))
        
        for row in c.fetchall():
            results.append({
                "type": "qa",
                "id": row[0],
                "conversation_id": row[1],
                "question": row[2][:100],
                "answer": row[3][:100]
            })
        
        conn.close()
        return results
    
    def get_statistics(self) -> Dict:
        """Get overall statistics."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM conversations")
        conv_count = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM qa_pairs")
        qa_count = c.fetchone()[0]
        
        c.execute('''
            SELECT source, COUNT(*) 
            FROM conversations 
            GROUP BY source
        ''')
        by_source = dict(c.fetchall())
        
        c.execute("SELECT SUM(content_length) FROM conversations")
        total_bytes = c.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "total_conversations": conv_count,
            "total_qa_pairs": qa_count,
            "total_bytes": total_bytes,
            "total_mb": round(total_bytes / (1024 * 1024), 1),
            "by_source": by_source
        }
    
    def export_json(self, output_path: str) -> Dict:
        """Export archive to JSON."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT * FROM conversations")
        conversations = [
            {
                "id": row[0], "source": row[1], "title": row[2],
                "messages": row[4], "qa_pairs": row[5]
            }
            for row in c.fetchall()
        ]
        
        c.execute("SELECT * FROM qa_pairs")
        qa_pairs = [
            {
                "id": row[0], "conversation_id": row[1], "source": row[2],
                "question": row[3], "answer": row[4]
            }
            for row in c.fetchall()
        ]
        
        export_data = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "total_conversations": len(conversations),
                "total_qa_pairs": len(qa_pairs)
            },
            "conversations": conversations,
            "qa_pairs": qa_pairs
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        conn.close()
        
        return {
            "status": "exported",
            "conversations": len(conversations),
            "qa_pairs": len(qa_pairs),
            "path": output_path
        }
    
    def print_statistics(self):
        """Print formatted statistics."""
        stats = self.get_statistics()
        print("\n" + "="*70)
        print("SCALABLE ARCHIVE STATISTICS")
        print("="*70)
        print(f"Total Conversations: {stats['total_conversations']}")
        print(f"Total Q&A Pairs: {stats['total_qa_pairs']}")
        print(f"Total Data: {stats['total_mb']} MB")
        print(f"\nBy Source:")
        for source, count in stats['by_source'].items():
            print(f"  • {source}: {count} conversations")
        print("="*70 + "\n")
    
    def interactive_interface(self):
        """Interactive search interface."""
        print("\n" + "="*70)
        print("SCALABLE CONVERSATION ARCHIVE (200+)")
        print("="*70)
        print("\nCommands:")
        print("  search <term>    - Search all conversations")
        print("  stats            - Show statistics")
        print("  export <file>    - Export to JSON")
        print("  quit             - Exit")
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
                    break
                
                elif command == "search" and arg:
                    results = self.search(arg)
                    print(f"\n✓ Found {len(results)} results for '{arg}':")
                    for i, r in enumerate(results[:10], 1):
                        if r["type"] == "conversation":
                            print(f"  {i}. [CONV] {r['title'][:60]}")
                        else:
                            print(f"  {i}. [QA] {r['question'][:60]}")
                    if len(results) > 10:
                        print(f"  ... and {len(results) - 10} more")
                
                elif command == "stats":
                    self.print_statistics()
                
                elif command == "export" and arg:
                    result = self.export_json(arg)
                    print(f"✓ Exported {result['conversations']} conversations")
                    print(f"  → {result['path']}")
                
                else:
                    print("Unknown command")
            
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Main execution."""
    import glob
    
    print("\n" + "="*70)
    print("SCALABLE ARCHIVE FOR 200+ CONVERSATIONS")
    print("="*70)
    
    # Find all JSON files
    json_files = glob.glob("*.json") + glob.glob("**/*.json", recursive=True)
    gemini_files = [f for f in json_files if "gemini" in f.lower()]
    
    if not gemini_files:
        print("\n✗ No Gemini JSON files found")
        print("Place your Gemini exports in this directory")
        return
    
    print(f"\n✓ Found {len(gemini_files)} Gemini export files")
    
    # Initialize archive
    archive = ScalableConversationArchive()
    
    # Load all files
    print("\nLoading all files...")
    stats = archive.load_bulk_gemini(gemini_files)
    
    # Summary
    print("\n" + "-"*70)
    print("LOADING SUMMARY")
    print("-"*70)
    print(f"Files Loaded: {stats['total_loaded']}")
    print(f"Total Conversations: {stats['total_conversations']}")
    print(f"Total Q&A Pairs: {stats['total_qa_pairs']}")
    
    if stats['errors']:
        print(f"\nErrors: {len(stats['errors'])}")
        for err in stats['errors'][:3]:
            print(f"  ✗ {err['file']}: {err['error']}")
    
    archive.print_statistics()
    archive.interactive_interface()


if __name__ == "__main__":
    main()
