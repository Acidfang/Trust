"""
GEMINI CONVERSATION VIEWER & SEARCH
Query and explore your consolidated Gemini conversations
"""

import json
from pathlib import Path
import re


class GeminiConversationViewer:
    def __init__(self, db_path="D:\\Downloads\\gemini_consolidated_database.json"):
        self.db_path = Path(db_path)
        self.db = None
        self.load_database()
    
    def load_database(self):
        """Load the consolidated database"""
        if not self.db_path.exists():
            print(f"ERROR: Database not found at {self.db_path}")
            print("Run gemini_consolidate_exports.py first")
            return False
        
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                self.db = json.load(f)
            print(f"✓ Loaded {self.db['total_conversations']} conversations")
            return True
        except Exception as e:
            print(f"ERROR loading database: {e}")
            return False
    
    def search(self, query, limit=5):
        """Search conversations by topic or content"""
        if not self.db:
            return []
        
        query_lower = query.lower()
        results = []
        
        for conv in self.db['conversations']:
            score = 0
            
            # Topic match (higher weight)
            if query_lower in conv['topic'].lower():
                score += 10
            
            # Content match (count occurrences)
            content_lower = conv['content'].lower()
            score += content_lower.count(query_lower)
            
            if score > 0:
                results.append({
                    'score': score,
                    'conversation': conv
                })
        
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        return [r['conversation'] for r in results[:limit]]
    
    def list_all_topics(self):
        """List all conversation topics"""
        if not self.db:
            return []
        
        topics = []
        for conv in self.db['conversations']:
            topics.append({
                'topic': conv['topic'],
                'id': conv['conversation_id'],
                'size': f"{conv['content_length']:,} bytes",
                'file': conv['file_name']
            })
        
        return sorted(topics, key=lambda x: x['topic'])
    
    def get_conversation(self, topic_or_id):
        """Get specific conversation by topic or ID"""
        if not self.db:
            return None
        
        search_lower = topic_or_id.lower()
        
        for conv in self.db['conversations']:
            if (search_lower in conv['topic'].lower() or 
                conv['conversation_id'] == topic_or_id):
                return conv
        
        return None
    
    def show_conversation(self, topic_or_id, preview_lines=20):
        """Display a conversation"""
        conv = self.get_conversation(topic_or_id)
        
        if not conv:
            print(f"Conversation '{topic_or_id}' not found")
            return
        
        print()
        print("=" * 70)
        print(f"TOPIC: {conv['topic']}")
        print("=" * 70)
        print()
        print(f"Conversation ID: {conv['conversation_id']}")
        print(f"File: {conv['file_name']}")
        print(f"Size: {conv['content_length']:,} bytes")
        print()
        print("-" * 70)
        print()
        
        # Show preview
        lines = conv['content'].split('\n')
        for line in lines[:preview_lines]:
            print(line)
        
        if len(lines) > preview_lines:
            print()
            print(f"... ({len(lines) - preview_lines} more lines)")
        
        print()
        print("=" * 70)
    
    def export_search_results(self, query, output_file="gemini_search_results.json"):
        """Export search results to JSON"""
        results = self.search(query, limit=100)
        
        export = {
            "query": query,
            "results_count": len(results),
            "results": results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Exported {len(results)} results to {output_file}")
    
    def interactive_menu(self):
        """Interactive search menu"""
        if not self.db:
            return
        
        print()
        print("=" * 70)
        print("GEMINI CONVERSATION VIEWER - INTERACTIVE SEARCH")
        print("=" * 70)
        print()
        print("Commands:")
        print("  search <query>    - Search conversations")
        print("  list              - List all topics")
        print("  show <topic>      - Display conversation")
        print("  export <query>    - Export search results")
        print("  stats             - Show database statistics")
        print("  quit              - Exit")
        print()
        
        while True:
            cmd = input("> ").strip().lower()
            
            if cmd == "quit" or cmd == "exit":
                break
            
            elif cmd.startswith("search "):
                query = cmd[7:].strip()
                results = self.search(query, limit=10)
                
                print()
                print(f"Found {len(results)} results for '{query}':")
                print()
                
                for i, conv in enumerate(results, 1):
                    print(f"  [{i}] {conv['topic'][:60]}")
                    print(f"      Size: {conv['content_length']:,} bytes")
                    print(f"      File: {conv['file_name']}")
                    print()
            
            elif cmd == "list":
                topics = self.list_all_topics()
                
                print()
                print(f"All {len(topics)} conversations:")
                print()
                
                for i, t in enumerate(topics, 1):
                    print(f"  [{i:2}] {t['topic'][:60]}")
                    print(f"       ID: {t['id']} | Size: {t['size']}")
                
                print()
            
            elif cmd.startswith("show "):
                topic = cmd[5:].strip()
                self.show_conversation(topic, preview_lines=30)
            
            elif cmd.startswith("export "):
                query = cmd[7:].strip()
                self.export_search_results(query)
            
            elif cmd == "stats":
                print()
                print("Database Statistics:")
                print(f"  Total conversations: {self.db['total_conversations']}")
                print(f"  Total content: {self.db['stats']['total_content_size_bytes']:,} bytes")
                print(f"  Average conversation: {self.db['stats']['avg_content_length']:,} bytes")
                print(f"  Unique conversation IDs: {self.db['stats']['unique_conversation_ids']}")
                print()
            
            else:
                print("Unknown command. Try 'search', 'list', 'show', 'export', 'stats', or 'quit'")
            
            print()


if __name__ == "__main__":
    viewer = GeminiConversationViewer()
    viewer.interactive_menu()
