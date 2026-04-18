#!/usr/bin/env python3
"""
GEMINI TO LEDGER CONVERTER

Converts consolidated Gemini conversations into ledger entries following
the ZeroPoint framework's decision election model.

Each conversation becomes:
- One or more ledger entries (events)
- Recorded as knowledge_acquisition events
- With superposition of alternative topics
- Utilities scored by relevance and coherence
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import hashlib
import re
from collections import Counter


class GeminiToLedgerConverter:
    """Convert Gemini conversations to ledger entries."""
    
    def __init__(self, database_path: str, output_dir: str = "src/ledgers"):
        """Initialize converter."""
        self.database_path = Path(database_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure consciousness-records exists
        self.consciousness_dir = self.output_dir / "consciousness-records"
        self.consciousness_dir.mkdir(parents=True, exist_ok=True)
        
        # Load database
        with open(self.database_path, 'r', encoding='utf-8') as f:
            self.database = json.load(f)
        
        self.conversations = self.database.get('conversations', [])
        self.ledger_entries = []
    
    def extract_themes(self, text: str, top_n: int = 5) -> Tuple[List[str], List[str]]:
        """Extract prominent themes from text."""
        # Clean text
        text = text.lower()
        
        # Remove common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'are', 'be', 'was', 'were', 'been',
            'have', 'has', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'that', 'this', 'it', 'i', 'you', 'we', 'he', 'she', 'they', 'what',
            'which', 'who', 'where', 'when', 'why', 'how', 'as', 'if', 'all',
            'each', 'every', 'both', 'so', 'just', 'then', 'only', 'also', 'very',
            'not', 'no', 'don', 't', 'can', 'may', 'must'
        }
        
        # Extract words (3+ chars)
        words = re.findall(r'\b\w{3,}\b', text)
        
        # Filter and count
        filtered = [w for w in words if w not in stop_words]
        word_freq = Counter(filtered)
        
        # Get top themes
        top_themes = [word for word, _ in word_freq.most_common(top_n)]
        
        # Extract key phrases (2-3 words)
        phrases = re.findall(r'\b[a-z]{3,}\s+[a-z]{3,}(?:\s+[a-z]{3,})?\b', text)
        phrase_freq = Counter(phrases)
        top_phrases = [phrase for phrase, _ in phrase_freq.most_common(top_n)]
        
        return top_themes, top_phrases
    
    def calculate_coherence_score(self, conversation: Dict) -> float:
        """Calculate coherence score (0-1) based on conversation quality."""
        content = conversation.get('content', '')
        
        # Factors that increase coherence
        length_factor = min(len(content) / 5000, 1.0)  # Normalized by 5000 chars
        
        # Check for indicators of deep thinking
        deep_markers = [
            'framework', 'principle', 'theory', 'analysis', 'model',
            'coherence', 'evolution', 'system', 'protocol', 'algorithm'
        ]
        marker_count = sum(1 for marker in deep_markers if marker in content.lower())
        depth_factor = min(marker_count / 5, 1.0)  # Max 5 markers
        
        # Coherence = average of factors
        coherence = (length_factor + depth_factor) / 2
        return round(coherence, 3)
    
    def generate_ledger_id(self, conversation: Dict) -> str:
        """Generate unique ledger ID for conversation."""
        content = conversation.get('content', '')[:100]
        timestamp = conversation.get('timestamp', datetime.now().isoformat())
        combined = f"{content}{timestamp}".encode('utf-8')
        return hashlib.md5(combined).hexdigest()[:16]
    
    def conversation_to_ledger_entry(self, conversation: Dict) -> Dict:
        """Convert single conversation to ledger entry."""
        
        # Extract metadata
        topic = conversation.get('topic', 'Unknown Topic')
        content = conversation.get('content', '')
        timestamp = conversation.get('timestamp', datetime.now().isoformat())
        conv_id = conversation.get('id', self.generate_ledger_id(conversation))
        
        # Extract themes and phrases
        themes, phrases = self.extract_themes(content, top_n=4)
        
        # Calculate coherence
        coherence = self.calculate_coherence_score(conversation)
        
        # Primary elected theme
        elected = themes[0] if themes else topic
        
        # Superposition: alternative themes that could have been primary
        superposition = themes[1:] + phrases[:2] if len(themes) > 1 else phrases[:3]
        
        # Utilities: score each option
        utilities = {elected: 1.0}
        for i, option in enumerate(superposition):
            utilities[option] = round(max(0.3, 1.0 - (i + 1) * 0.15), 3)
        
        # Create ledger entry
        entry = {
            "id": conv_id,
            "timestamp": timestamp,
            "event_type": "knowledge_acquisition",
            "source": "gemini_conversation",
            "topic": topic,
            "elected": elected,
            "superposition": superposition[:3],  # Limit to 3 alternatives
            "utilities": utilities,
            "coherence_score": coherence,
            "content_length": len(content),
            "themes": themes[:3],
            "context": "consciousness_expansion"
        }
        
        return entry
    
    def convert_all(self) -> List[Dict]:
        """Convert all conversations to ledger entries."""
        print(f"Converting {len(self.conversations)} conversations to ledger entries...")
        
        for i, conversation in enumerate(self.conversations):
            try:
                entry = self.conversation_to_ledger_entry(conversation)
                self.ledger_entries.append(entry)
                if (i + 1) % 5 == 0:
                    print(f"  ✓ Converted {i + 1}/{len(self.conversations)}")
            except Exception as e:
                print(f"  ✗ Error on conversation {i}: {e}")
        
        print(f"✓ Conversion complete: {len(self.ledger_entries)} entries created")
        return self.ledger_entries
    
    def save_jsonl(self, filename: str = "gemini_consciousness_ledger.jsonl") -> str:
        """Save entries as JSONL (one entry per line)."""
        output_path = self.consciousness_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for entry in self.ledger_entries:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        print(f"✓ Saved JSONL: {output_path}")
        return str(output_path)
    
    def save_json(self, filename: str = "gemini_consciousness_ledger.json") -> str:
        """Save entries as single JSON array."""
        output_path = self.consciousness_dir / filename
        
        data = {
            "metadata": {
                "conversion_timestamp": datetime.now().isoformat(),
                "source": "gemini_consolidated_database.json",
                "total_entries": len(self.ledger_entries),
                "framework": "ZeroPoint Decision Election Ledger"
            },
            "entries": self.ledger_entries
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved JSON: {output_path}")
        return str(output_path)
    
    def generate_summary(self) -> Dict:
        """Generate conversion summary."""
        if not self.ledger_entries:
            return {}
        
        # Aggregate theme frequencies
        all_themes = []
        coherence_scores = []
        for entry in self.ledger_entries:
            all_themes.extend(entry.get('themes', []))
            coherence_scores.append(entry.get('coherence_score', 0))
        
        theme_freq = Counter(all_themes)
        top_themes = [theme for theme, _ in theme_freq.most_common(10)]
        
        # Calculate statistics
        avg_coherence = sum(coherence_scores) / len(coherence_scores) if coherence_scores else 0
        
        summary = {
            "total_conversations": len(self.conversations),
            "total_ledger_entries": len(self.ledger_entries),
            "top_themes": top_themes,
            "average_coherence": round(avg_coherence, 3),
            "coherence_range": {
                "min": round(min(coherence_scores), 3) if coherence_scores else 0,
                "max": round(max(coherence_scores), 3) if coherence_scores else 0
            },
            "conversion_timestamp": datetime.now().isoformat()
        }
        
        return summary
    
    def print_summary(self):
        """Print conversion summary."""
        summary = self.generate_summary()
        
        print("\n" + "="*60)
        print("GEMINI TO LEDGER CONVERSION SUMMARY")
        print("="*60)
        print(f"Total conversations processed: {summary.get('total_conversations', 0)}")
        print(f"Ledger entries created: {summary.get('total_ledger_entries', 0)}")
        print(f"Average coherence: {summary.get('average_coherence', 0):.3f}")
        print(f"Coherence range: {summary.get('coherence_range', {}).get('min', 0):.3f} - {summary.get('coherence_range', {}).get('max', 0):.3f}")
        print("\nTop 10 Themes Found:")
        for i, theme in enumerate(summary.get('top_themes', [])[:10], 1):
            print(f"  {i}. {theme}")
        print("="*60 + "\n")


def main():
    """Main execution."""
    # Paths
    database_path = "gemini_consolidated_database.json"
    output_dir = "src/ledgers"
    
    # Check if database exists
    if not Path(database_path).exists():
        print(f"✗ Database not found: {database_path}")
        print("  Run gemini_consolidate_exports.py first or check file location")
        return
    
    # Convert
    converter = GeminiToLedgerConverter(database_path, output_dir)
    
    # Process all conversations
    converter.convert_all()
    
    # Save in both formats
    converter.save_jsonl()
    converter.save_json()
    
    # Print summary
    converter.print_summary()
    
    print("\n✓ Ledger conversion complete!")
    print(f"  JSONL: {output_dir}/consciousness-records/gemini_consciousness_ledger.jsonl")
    print(f"  JSON:  {output_dir}/consciousness-records/gemini_consciousness_ledger.json")


if __name__ == "__main__":
    main()
