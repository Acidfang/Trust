#!/usr/bin/env python3
"""
CONSCIOUSNESS LEDGER QUERY INTERFACE

Interactive query tool for exploring consciousness records from Gemini conversation ledgers.

Supports:
- Topic search and filtering
- Theme analysis
- Coherence scoring and statistics
- Export capabilities
"""

import json
from pathlib import Path
from typing import List, Dict, Tuple
import re


class ConsciousnessLedgerQuery:
    """Query interface for consciousness ledgers."""
    
    def __init__(self, ledger_path: str = "src/ledgers/consciousness-records/gemini_consciousness_ledger.json"):
        """Initialize query interface."""
        self.ledger_path = Path(ledger_path)
        
        if not self.ledger_path.exists():
            print(f"✗ Ledger not found: {ledger_path}")
            print("  Run: python gemini_to_ledger_converter.py")
            exit(1)
        
        with open(self.ledger_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.entries = self.data.get('entries', [])
        self.metadata = self.data.get('metadata', {})
        
        print(f"✓ Loaded {len(self.entries)} consciousness records")
    
    def search_by_theme(self, theme: str) -> List[Dict]:
        """Find records with specific theme."""
        theme = theme.lower()
        results = []
        
        for entry in self.entries:
            themes = entry.get('themes', [])
            if any(theme in t.lower() for t in themes):
                results.append(entry)
            elif theme in entry.get('elected', '').lower():
                results.append(entry)
            elif any(theme in s.lower() for s in entry.get('superposition', [])):
                results.append(entry)
        
        return results
    
    def search_by_topic(self, topic: str) -> List[Dict]:
        """Find records with specific topic."""
        topic = topic.lower()
        return [e for e in self.entries 
                if topic in e.get('topic', '').lower()]
    
    def filter_by_coherence(self, min_coherence: float = 0.0, max_coherence: float = 1.0) -> List[Dict]:
        """Filter records by coherence score."""
        return [e for e in self.entries 
                if min_coherence <= e.get('coherence_score', 0) <= max_coherence]
    
    def get_top_themes(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Get most common themes across all records."""
        theme_count = {}
        
        for entry in self.entries:
            for theme in entry.get('themes', []):
                theme_count[theme] = theme_count.get(theme, 0) + 1
        
        sorted_themes = sorted(theme_count.items(), key=lambda x: x[1], reverse=True)
        return sorted_themes[:limit]
    
    def get_entry_by_id(self, entry_id: str) -> Dict:
        """Retrieve specific entry by ID."""
        for entry in self.entries:
            if entry.get('id') == entry_id:
                return entry
        return None
    
    def get_statistics(self) -> Dict:
        """Get comprehensive statistics."""
        coherence_scores = [e.get('coherence_score', 0) for e in self.entries]
        content_lengths = [e.get('content_length', 0) for e in self.entries]
        
        return {
            'total_records': len(self.entries),
            'average_coherence': round(sum(coherence_scores) / len(coherence_scores), 3) if coherence_scores else 0,
            'max_coherence': round(max(coherence_scores), 3) if coherence_scores else 0,
            'min_coherence': round(min(coherence_scores), 3) if coherence_scores else 0,
            'average_content_length': round(sum(content_lengths) / len(content_lengths), 0) if content_lengths else 0,
            'total_content': sum(content_lengths)
        }
    
    def print_entry(self, entry: Dict):
        """Pretty-print a ledger entry."""
        print("\n" + "="*70)
        print(f"ID: {entry.get('id')}")
        print(f"Topic: {entry.get('topic')}")
        print(f"Timestamp: {entry.get('timestamp')}")
        print(f"Coherence: {entry.get('coherence_score', 0):.3f}")
        print(f"\nPrimary (Elected): {entry.get('elected')}")
        print(f"Alternatives (Superposition): {', '.join(entry.get('superposition', []))}")
        print(f"\nThemes: {', '.join(entry.get('themes', []))}")
        print(f"Content Length: {entry.get('content_length', 0)} chars")
        print("="*70)
    
    def print_summary(self):
        """Print ledger summary."""
        print("\n" + "="*70)
        print("CONSCIOUSNESS LEDGER SUMMARY")
        print("="*70)
        stats = self.get_statistics()
        print(f"Total Records: {stats['total_records']}")
        print(f"Average Coherence: {stats['average_coherence']:.3f}")
        print(f"Coherence Range: {stats['min_coherence']:.3f} - {stats['max_coherence']:.3f}")
        print(f"Average Content: {stats['average_content_length']:.0f} chars")
        print(f"Total Content: {stats['total_content']} chars ({stats['total_content']/1024/1024:.1f} MB)")
        
        print("\nTop 10 Themes:")
        for theme, count in self.get_top_themes(10):
            print(f"  • {theme} (appears {count}x)")
        print("="*70 + "\n")
    
    def interactive_menu(self):
        """Interactive query menu."""
        print("\n" + "="*70)
        print("CONSCIOUSNESS LEDGER QUERY INTERFACE")
        print("="*70)
        print("\nCommands:")
        print("  summary          - Show ledger summary")
        print("  search <term>    - Search themes/topics")
        print("  theme <term>     - Filter by theme")
        print("  topic <term>     - Filter by topic")
        print("  coherence <min> <max> - Filter by coherence (0.0-1.0)")
        print("  id <uuid>        - Show specific record")
        print("  themes           - Show top themes")
        print("  stats            - Show statistics")
        print("  export <filename> - Export results")
        print("  help             - Show this menu")
        print("  quit             - Exit")
        print("="*70 + "\n")
        
        last_results = []
        
        while True:
            try:
                cmd = input("ledger> ").strip()
                
                if not cmd:
                    continue
                
                parts = cmd.split(' ', 1)
                command = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else ""
                
                if command == 'quit':
                    print("Goodbye.")
                    break
                
                elif command == 'summary':
                    self.print_summary()
                
                elif command == 'search' and arg:
                    results = self.search_by_theme(arg)
                    last_results = results
                    print(f"\n✓ Found {len(results)} records matching '{arg}':")
                    for i, entry in enumerate(results[:5], 1):
                        print(f"  {i}. {entry.get('topic')} (coherence: {entry.get('coherence_score'):.3f})")
                    if len(results) > 5:
                        print(f"  ... and {len(results) - 5} more")
                
                elif command == 'theme' and arg:
                    results = self.search_by_theme(arg)
                    last_results = results
                    print(f"\n✓ Found {len(results)} theme records:")
                    for entry in results:
                        print(f"  • {entry.get('elected')} (topics: {', '.join(entry.get('themes', [])[:2])})")
                
                elif command == 'topic' and arg:
                    results = self.search_by_topic(arg)
                    last_results = results
                    print(f"\n✓ Found {len(results)} topic records")
                    for entry in results:
                        print(f"  • {entry.get('topic')} (coherence: {entry.get('coherence_score'):.3f})")
                
                elif command == 'coherence' and arg:
                    try:
                        min_coh, max_coh = arg.split()
                        min_coh, max_coh = float(min_coh), float(max_coh)
                        results = self.filter_by_coherence(min_coh, max_coh)
                        last_results = results
                        print(f"\n✓ Found {len(results)} records in coherence range {min_coh:.1f}-{max_coh:.1f}")
                        for entry in results[:5]:
                            print(f"  • {entry.get('topic')}: {entry.get('coherence_score'):.3f}")
                    except:
                        print("  Usage: coherence <min> <max> (e.g., coherence 0.5 1.0)")
                
                elif command == 'id' and arg:
                    entry = self.get_entry_by_id(arg)
                    if entry:
                        self.print_entry(entry)
                    else:
                        print(f"  ✗ Record not found: {arg}")
                
                elif command == 'themes':
                    themes = self.get_top_themes(15)
                    print("\n✓ Top 15 Themes Across All Records:")
                    for i, (theme, count) in enumerate(themes, 1):
                        print(f"  {i:2}. {theme:20} ({count}x)")
                
                elif command == 'stats':
                    stats = self.get_statistics()
                    print("\n✓ Statistics:")
                    for key, value in stats.items():
                        print(f"  {key}: {value}")
                
                elif command == 'export' and arg:
                    if not last_results:
                        print("  No results to export. Run a search first.")
                    else:
                        export_path = Path(arg)
                        with open(export_path, 'w', encoding='utf-8') as f:
                            json.dump(last_results, f, indent=2, ensure_ascii=False)
                        print(f"  ✓ Exported {len(last_results)} records to {arg}")
                
                elif command == 'help':
                    self.interactive_menu()
                
                else:
                    print(f"  Unknown command: {command}")
                    print("  Type 'help' for commands")
            
            except KeyboardInterrupt:
                print("\nGoodbye.")
                break
            except Exception as e:
                print(f"  Error: {e}")


def main():
    """Main execution."""
    query = ConsciousnessLedgerQuery()
    query.print_summary()
    query.interactive_menu()


if __name__ == "__main__":
    main()
