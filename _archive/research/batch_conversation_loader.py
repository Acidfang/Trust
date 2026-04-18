#!/usr/bin/env python3
"""
BATCH CONVERSATION LOADER

For efficiently loading 200+ conversations from multiple AIs into the archive.
"""

import json
from pathlib import Path
from datetime import datetime
import os
from typing import Dict, List


def find_all_exports(search_dir: str = ".") -> List[Dict]:
    """Find all AI export files in directory."""
    exports = []
    
    patterns = {
        "gemini": ["gemini*.json", "*gemini*"],
        "claude": ["claude*.json", "*claude*"],
        "chatgpt": ["chatgpt*.json", "*chatgpt*", "openai*.json"],
        "anthropic": ["anthropic*.json"],
        "gemini_consolidated": ["gemini_consolidated*.json"],
    }
    
    search_path = Path(search_dir)
    
    for filename in search_path.rglob("*.json"):
        name_lower = filename.name.lower()
        
        for source, patterns_list in patterns.items():
            for pattern in patterns_list:
                if pattern.replace("*", "") in name_lower:
                    exports.append({
                        "path": str(filename),
                        "name": filename.name,
                        "size": filename.stat().st_size / (1024 * 1024),  # MB
                        "source": source,
                        "detected": True
                    })
                    break
    
    return exports


def load_batch(archive_system, file_list: List[str], verbose: bool = True) -> Dict:
    """Load multiple files into archive."""
    results = {
        "total_files": len(file_list),
        "successful": 0,
        "failed": 0,
        "total_conversations": 0,
        "total_qa_pairs": 0,
        "by_source": {},
        "errors": []
    }
    
    for i, filepath in enumerate(file_list, 1):
        if verbose:
            print(f"  [{i}/{len(file_list)}] Loading {Path(filepath).name}...", end=" ", flush=True)
        
        try:
            result = archive_system.load_gemini_json(filepath)
            if result["status"] == "loaded":
                results["successful"] += 1
                results["total_conversations"] += result.get("conversations", 0)
                results["total_qa_pairs"] += result.get("qa_pairs", 0)
                
                source = result.get("source", "unknown")
                if source not in results["by_source"]:
                    results["by_source"][source] = {"count": 0, "conversations": 0}
                results["by_source"][source]["count"] += 1
                results["by_source"][source]["conversations"] += result.get("conversations", 0)
                
                if verbose:
                    print(f"✓ ({result.get('conversations', 0)} conversations)")
            else:
                results["failed"] += 1
                results["errors"].append({
                    "file": filepath,
                    "error": result.get("message", "Unknown error")
                })
                if verbose:
                    print(f"✗ {result.get('message')}")
        
        except Exception as e:
            results["failed"] += 1
            results["errors"].append({"file": filepath, "error": str(e)})
            if verbose:
                print(f"✗ {str(e)}")
    
    return results


def main():
    """Main batch loader."""
    from conversation_archive_ledger import ConversationArchiveLedger
    
    print("\n" + "="*70)
    print("BATCH CONVERSATION LOADER (200+ Format)")
    print("="*70)
    
    # Find all exports
    print("\nScanning for AI export files...")
    exports = find_all_exports(".")
    
    if exports:
        print(f"\n✓ Found {len(exports)} export files:")
        for exp in exports:
            print(f"  • {exp['name']} ({exp['size']:.1f}MB) - {exp['source']}")
    else:
        print("\n✗ No export files found")
        print("  Place your AI export JSONs in this directory:")
        print("    - gemini_consolidated_database.json")
        print("    - claude_export.json")
        print("    - chatgpt_export.json")
        print("    - etc.")
        return
    
    # Ask to load
    print("\n" + "-"*70)
    response = input("Load all found files? (y/n): ").strip().lower()
    
    if response != 'y':
        print("Cancelled.")
        return
    
    # Initialize archive
    archive = ConversationArchiveLedger()
    
    # Load all files
    print("\nLoading all files...")
    file_paths = [exp["path"] for exp in exports]
    results = load_batch(archive, file_paths, verbose=True)
    
    # Summary
    print("\n" + "="*70)
    print("BATCH LOADING SUMMARY")
    print("="*70)
    print(f"Files Processed: {results['successful']}/{results['total_files']}")
    print(f"Total Conversations: {results['total_conversations']}")
    print(f"Total Q&A Pairs: {results['total_qa_pairs']}")
    print(f"\nBy Source:")
    for source, data in results["by_source"].items():
        print(f"  • {source}: {data['conversations']} conversations ({data['count']} files)")
    
    if results["errors"]:
        print(f"\nErrors ({len(results['errors'])}):")
        for error in results["errors"][:5]:
            print(f"  ✗ {error['file']}: {error['error']}")
        if len(results["errors"]) > 5:
            print(f"  ... and {len(results['errors']) - 5} more")
    
    # Archive statistics
    print("\n" + "-"*70)
    archive.print_statistics()
    
    # Export option
    print("-"*70)
    export_response = input("Export unified archive? (y/n): ").strip().lower()
    if export_response == 'y':
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_path = f"archive_complete_{timestamp}.json"
        result = archive.export_archive(export_path)
        print(f"✓ Exported to {result['path']}")
    
    print("\n" + "="*70)
    print("Done! Your archive is ready to use.")
    print("\nNext: python conversation_archive_ledger.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
