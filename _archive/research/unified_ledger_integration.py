#!/usr/bin/env python3
"""
UNIFIED LEDGER INTEGRATION SYSTEM

Merges multiple ledger sources (Gemini JSON, Election Ledgers, Consciousness Records)
into a single queryable, cross-referenced system.

Ledger Types Supported:
1. Gemini JSON chats (from Google Takeout or manual export)
2. Election Ledgers (ZeroPoint decision records)
3. Consciousness Records (AI interaction history)
4. Session Ledgers (temporal records)
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
import hashlib
from collections import defaultdict


class UnifiedLedgerSystem:
    """Unified interface for multiple ledger types."""
    
    def __init__(self):
        """Initialize unified ledger system."""
        self.ledgers = {}  # ledger_name -> ledger_data
        self.index = defaultdict(list)  # keyword -> [(ledger, entry_id)]
        self.entries_by_id = {}  # entry_id -> entry
        self.cross_references = defaultdict(list)  # entry_id -> [related_entry_ids]
        
    def load_gemini_json(self, json_path: str, ledger_name: str = "gemini") -> Dict:
        """Load Gemini JSON export."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different Gemini JSON formats
            if isinstance(data, dict):
                conversations = data.get('conversations', [data]) if 'conversations' in data else [data]
            else:
                conversations = data if isinstance(data, list) else [data]
            
            ledger_data = {
                "type": "gemini_json",
                "source": json_path,
                "loaded_at": datetime.now().isoformat(),
                "entries": []
            }
            
            for i, conv in enumerate(conversations):
                entry = self._normalize_gemini_entry(conv, i, ledger_name)
                if entry:
                    ledger_data["entries"].append(entry)
                    entry_id = entry["id"]
                    self.entries_by_id[entry_id] = entry
                    # Index key terms
                    self._index_entry(entry, ledger_name)
            
            self.ledgers[ledger_name] = ledger_data
            return {
                "status": "loaded",
                "ledger": ledger_name,
                "entries": len(ledger_data["entries"])
            }
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _normalize_gemini_entry(self, conv: Any, index: int, ledger_name: str) -> Optional[Dict]:
        """Convert Gemini format to unified entry."""
        try:
            # Extract content
            content = ""
            if isinstance(conv, dict):
                # Check common Gemini fields
                content = conv.get('content', conv.get('text', conv.get('message', str(conv))))
            else:
                content = str(conv)
            
            if not content:
                return None
            
            # Generate ID
            entry_id = hashlib.sha256(
                f"{content[:100]}{index}".encode()
            ).hexdigest()[:16]
            
            # Extract topic/title
            lines = content.split('\n')
            title = next((l.strip() for l in lines if l.strip() and len(l.strip()) > 10), "Untitled")
            
            return {
                "id": entry_id,
                "timestamp": datetime.now().isoformat(),
                "type": "gemini_conversation",
                "ledger": ledger_name,
                "title": title[:100],
                "content_preview": content[:500],
                "content_length": len(content),
                "content_hash": hashlib.sha256(content.encode()).hexdigest(),
                "metadata": {
                    "source": "gemini_json",
                    "index": index,
                    "original_format": type(conv).__name__
                }
            }
        
        except Exception as e:
            print(f"    Error normalizing entry {index}: {e}")
            return None
    
    def load_election_ledger(self, jsonl_path: str, ledger_name: str = "elections") -> Dict:
        """Load ZeroPoint election ledger (JSONL format)."""
        try:
            ledger_data = {
                "type": "election_ledger",
                "source": jsonl_path,
                "loaded_at": datetime.now().isoformat(),
                "entries": []
            }
            
            with open(jsonl_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if line.strip():
                        entry = json.loads(line)
                        entry["ledger"] = ledger_name
                        ledger_data["entries"].append(entry)
                        entry_id = entry.get("id")
                        if entry_id:
                            self.entries_by_id[entry_id] = entry
                            self._index_entry(entry, ledger_name)
            
            self.ledgers[ledger_name] = ledger_data
            return {
                "status": "loaded",
                "ledger": ledger_name,
                "entries": len(ledger_data["entries"])
            }
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _index_entry(self, entry: Dict, ledger_name: str):
        """Index entry for fast keyword search."""
        entry_id = entry.get("id")
        
        # Index standard fields
        for field in ["title", "topic", "elected", "context"]:
            if field in entry and entry[field]:
                key = str(entry[field]).lower()
                self.index[key].append((ledger_name, entry_id))
        
        # Index themes if present
        for theme in entry.get("themes", []):
            self.index[theme.lower()].append((ledger_name, entry_id))
        
        # Index superposition options
        for option in entry.get("superposition", []):
            self.index[option.lower()].append((ledger_name, entry_id))
    
    def cross_reference(self, threshold: float = 0.7) -> Dict:
        """Find related entries across ledgers based on content similarity."""
        results = {
            "total_cross_references": 0,
            "reference_pairs": []
        }
        
        entry_ids = list(self.entries_by_id.keys())
        
        for i, id1 in enumerate(entry_ids):
            for id2 in entry_ids[i+1:]:
                similarity = self._calculate_similarity(
                    self.entries_by_id[id1],
                    self.entries_by_id[id2]
                )
                
                if similarity >= threshold:
                    results["reference_pairs"].append({
                        "entry1": id1,
                        "entry2": id2,
                        "similarity": round(similarity, 3),
                        "ledger1": self.entries_by_id[id1].get("ledger"),
                        "ledger2": self.entries_by_id[id2].get("ledger")
                    })
                    self.cross_references[id1].append(id2)
                    self.cross_references[id2].append(id1)
                    results["total_cross_references"] += 1
        
        return results
    
    def _calculate_similarity(self, entry1: Dict, entry2: Dict) -> float:
        """Calculate similarity score between two entries (0.0-1.0)."""
        # Extract comparable fields
        def get_keywords(entry):
            words = set()
            for field in ["title", "topic", "elected", "content_preview"]:
                if field in entry:
                    val = str(entry[field]).lower()
                    words.update(w for w in val.split() if len(w) > 3)
            for theme in entry.get("themes", []):
                words.add(theme.lower())
            return words
        
        words1 = get_keywords(entry1)
        words2 = get_keywords(entry2)
        
        if not words1 or not words2:
            return 0.0
        
        # Jaccard similarity
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def search_unified(self, query: str, ledger_filter: Optional[str] = None) -> List[Dict]:
        """Search across all ledgers."""
        query_lower = query.lower()
        results = []
        seen_ids = set()
        
        # Keyword index lookup
        for keyword, entries in self.index.items():
            if query_lower in keyword or keyword in query_lower:
                for ledger_name, entry_id in entries:
                    if entry_id not in seen_ids:
                        if ledger_filter is None or ledger_filter == ledger_name:
                            entry = self.entries_by_id[entry_id]
                            results.append(entry)
                            seen_ids.add(entry_id)
        
        # Content preview search
        for entry in self.entries_by_id.values():
            if entry["id"] not in seen_ids:
                preview = entry.get("content_preview", "").lower()
                if query_lower in preview:
                    if ledger_filter is None or ledger_filter == entry.get("ledger"):
                        results.append(entry)
                        seen_ids.add(entry["id"])
        
        return results[:20]  # Return top 20
    
    def get_statistics(self) -> Dict:
        """Get unified statistics across all ledgers."""
        stats = {
            "total_entries": len(self.entries_by_id),
            "total_ledgers": len(self.ledgers),
            "total_cross_references": sum(len(refs) for refs in self.cross_references.values()),
            "by_ledger": {}
        }
        
        for ledger_name, ledger_data in self.ledgers.items():
            ledger_type = ledger_data.get("type", "unknown")
            count = len(ledger_data.get("entries", []))
            stats["by_ledger"][ledger_name] = {
                "type": ledger_type,
                "entries": count
            }
        
        return stats
    
    def export_merged(self, output_path: str) -> Dict:
        """Export all ledgers as single merged ledger."""
        merged = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "system": "unified_ledger_integration",
                "total_entries": len(self.entries_by_id),
                "total_ledgers": len(self.ledgers),
                "ledger_sources": list(self.ledgers.keys())
            },
            "entries": list(self.entries_by_id.values()),
            "cross_references": dict(self.cross_references)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)
        
        return {
            "status": "exported",
            "path": output_path,
            "entries": len(self.entries_by_id)
        }
    
    def interactive_merge_interface(self):
        """Interactive interface for ledger integration."""
        print("\n" + "="*70)
        print("UNIFIED LEDGER INTEGRATION SYSTEM")
        print("="*70)
        print("\nCommands:")
        print("  load gemini <path>          - Load Gemini JSON chats")
        print("  load elections <path>       - Load election ledger (JSONL)")
        print("  search <term>               - Search across all ledgers")
        print("  stats                       - Show integration statistics")
        print("  cross-reference             - Find related entries")
        print("  list-ledgers                - Show loaded ledgers")
        print("  merge <output.json>         - Export merged ledger")
        print("  quit                        - Exit")
        print("="*70 + "\n")
        
        while True:
            try:
                cmd = input("ledger> ").strip()
                
                if not cmd:
                    continue
                
                parts = cmd.split(' ', 2)
                command = parts[0].lower()
                
                if command == "quit":
                    print("Goodbye.")
                    break
                
                elif command == "load" and len(parts) >= 3:
                    source_type = parts[1].lower()
                    source_path = parts[2]
                    
                    if source_type == "gemini":
                        result = self.load_gemini_json(source_path, "gemini")
                    elif source_type == "elections":
                        result = self.load_election_ledger(source_path, "elections")
                    else:
                        result = {"status": "error", "message": f"Unknown type: {source_type}"}
                    
                    if result.get("status") == "loaded":
                        print(f"  ✓ Loaded: {result['entries']} entries")
                    else:
                        print(f"  ✗ Error: {result.get('message', 'Unknown error')}")
                
                elif command == "search" and len(parts) > 1:
                    query = ' '.join(parts[1:])
                    results = self.search_unified(query)
                    print(f"\n✓ Found {len(results)} results for '{query}':")
                    for i, entry in enumerate(results[:5], 1):
                        title = entry.get("title", entry.get("topic", "Unknown"))
                        ledger = entry.get("ledger", "?")
                        print(f"  {i}. [{ledger}] {title[:60]}")
                    if len(results) > 5:
                        print(f"  ... and {len(results) - 5} more")
                
                elif command == "stats":
                    stats = self.get_statistics()
                    print("\n✓ Unified Statistics:")
                    print(f"  Total Entries: {stats['total_entries']}")
                    print(f"  Total Ledgers: {stats['total_ledgers']}")
                    print(f"  Cross-References: {stats['total_cross_references']}")
                    print("\n  By Ledger:")
                    for ledger_name, info in stats["by_ledger"].items():
                        print(f"    • {ledger_name} ({info['type']}): {info['entries']} entries")
                
                elif command == "cross-reference":
                    print("  Analyzing cross-references...")
                    results = self.cross_reference()
                    print(f"  ✓ Found {results['total_cross_references']} cross-references")
                    if results['reference_pairs']:
                        print("\n  Top 5 Connections:")
                        for pair in results['reference_pairs'][:5]:
                            print(f"    • {pair['ledger1']} ↔ {pair['ledger2']} (similarity: {pair['similarity']})")
                
                elif command == "list-ledgers":
                    print("\n✓ Loaded Ledgers:")
                    for name, data in self.ledgers.items():
                        ledger_type = data.get("type")
                        count = len(data.get("entries", []))
                        print(f"  • {name} ({ledger_type}): {count} entries")
                
                elif command == "merge" and len(parts) > 1:
                    output_path = parts[1]
                    result = self.export_merged(output_path)
                    print(f"  ✓ Merged {result['entries']} entries → {output_path}")
                
                elif command == "help":
                    print("  [see commands above]")
                
                else:
                    print(f"  Unknown command: {command}")
            
            except KeyboardInterrupt:
                print("\nGoodbye.")
                break
            except Exception as e:
                print(f"  Error: {e}")


def main():
    """Main execution."""
    system = UnifiedLedgerSystem()
    
    # Load example ledgers if they exist
    print("UNIFIED LEDGER INTEGRATION SYSTEM")
    print("="*70)
    
    # Try to load election ledger
    election_path = "src/ledgers/ledger_elections.jsonl"
    if Path(election_path).exists():
        print(f"\nLoading election ledger from {election_path}...")
        result = system.load_election_ledger(election_path, "elections")
        print(f"  ✓ {result.get('entries', 0)} election entries loaded")
    
    # Try to load gemini consciousness ledger
    gemini_ledger_path = "src/ledgers/consciousness-records/gemini_consciousness_ledger.json"
    if Path(gemini_ledger_path).exists():
        print(f"Loading Gemini consciousness ledger from {gemini_ledger_path}...")
        result = system.load_gemini_json(gemini_ledger_path, "gemini_consciousness")
        print(f"  ✓ {result.get('entries', 0)} Gemini consciousness entries loaded")
    
    # Start interactive interface
    system.interactive_merge_interface()


if __name__ == "__main__":
    main()
