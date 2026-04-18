"""
GEMINI LOCAL DATABASE EXTRACTOR
Directly access Chrome's local databases where Gemini stores conversations
"""

import json
import sqlite3
import os
import shutil
from pathlib import Path
from datetime import datetime
import sys

def find_chrome_profile():
    """Find the active Chrome profile directory"""
    username = os.getenv('USERNAME')
    chrome_path = Path(f"C:/Users/{username}/AppData/Local/Google/Chrome/User Data/Default")
    
    if chrome_path.exists():
        return chrome_path
    
    # Try alternate location
    chrome_path = Path(f"C:/Users/{username}/AppData/Local/Google/Chrome/User Data/Profile 1")
    if chrome_path.exists():
        return chrome_path
    
    return None

def extract_from_indexeddb():
    """Extract data from IndexedDB databases"""
    chrome_path = find_chrome_profile()
    if not chrome_path:
        print("ERROR: Could not find Chrome profile")
        return {}
    
    idb_path = chrome_path / "IndexedDB"
    data = {}
    
    if not idb_path.exists():
        print("[*] IndexedDB path doesn't exist yet")
        return data
    
    print(f"[+] Found IndexedDB at: {idb_path}")
    
    # List all .leveldb directories (IDB stores)
    for leveldb_dir in idb_path.glob("*/*.leveldb"):
        db_name = leveldb_dir.parent.name
        print(f"    - Database: {db_name}")
        data[db_name] = {
            "path": str(leveldb_dir),
            "location": leveldb_dir.parent.name
        }
    
    return data

def extract_from_local_storage():
    """Extract Local Storage data (stored in SQLite)"""
    chrome_path = find_chrome_profile()
    if not chrome_path:
        return {}
    
    data = {}
    
    # Check for leveldb format local storage
    local_storage_path = chrome_path / "Local Storage"
    
    if local_storage_path.exists():
        print(f"[+] Found Local Storage at: {local_storage_path}")
        
        # List leveldb directories
        for leveldb_dir in local_storage_path.glob("*.leveldb"):
            domain = leveldb_dir.name.replace(".leveldb", "")
            print(f"    - Storage: {domain}")
            data[domain] = {
                "path": str(leveldb_dir),
                "type": "leveldb"
            }
    
    return data

def search_for_gemini_data():
    """Search for any Gemini-related data in the profile"""
    chrome_path = find_chrome_profile()
    if not chrome_path:
        return {}
    
    print(f"[+] Searching in Chrome profile: {chrome_path}")
    
    results = {
        "indexeddb": extract_from_indexeddb(),
        "local_storage": extract_from_local_storage(),
        "chrome_path": str(chrome_path),
        "profile_exists": chrome_path.exists(),
        "databases": {}
    }
    
    # Look for any SQLite databases
    print("\n[+] Scanning for databases...")
    database_dirs = [
        chrome_path / "Databases",
        chrome_path / "Session Storage",
        chrome_path,
    ]
    
    for db_dir in database_dirs:
        if db_dir.exists():
            for db_file in db_dir.glob("*.db"):
                print(f"    - Found DB: {db_file.name}")
                try:
                    # Try to read it
                    conn = sqlite3.connect(str(db_file))
                    cursor = conn.cursor()
                    
                    # Get table names
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    
                    table_names = [t[0] for t in tables]
                    results["databases"][db_file.name] = {
                        "tables": table_names,
                        "path": str(db_file)
                    }
                    
                    print(f"      Tables: {', '.join(table_names[:5])}")
                    
                    conn.close()
                except Exception as e:
                    print(f"      (Could not read: {e})")
    
    return results

def main():
    print("=" * 70)
    print("GEMINI LOCAL DATABASE EXTRACTOR")
    print("=" * 70)
    print()
    
    results = {
        "extracted_at": datetime.now().isoformat(),
        "data": None,
        "status": "searching",
        "error": None
    }
    
    try:
        print("[1] Locating Chrome profile...")
        chrome_path = find_chrome_profile()
        
        if not chrome_path:
            results["error"] = "Chrome profile not found"
            results["status"] = "error"
            print("[!] ERROR: Could not find Chrome profile")
            print("    Checked locations:")
            print(f"    - C:/Users/{os.getenv('USERNAME')}/AppData/Local/Google/Chrome/User Data/Default")
            print(f"    - C:/Users/{os.getenv('USERNAME')}/AppData/Local/Google/Chrome/User Data/Profile 1")
        else:
            print(f"    ✓ Found: {chrome_path}")
            print()
            
            print("[2] Searching for Gemini data...")
            data = search_for_gemini_data()
            
            results["data"] = data
            results["status"] = "success"
            
            print()
            print(f"[+] IndexedDB databases: {len(data['indexeddb'])}")
            print(f"[+] Local Storage entries: {len(data['local_storage'])}")
            print(f"[+] Database files found: {len(data['databases'])}")
            
            # Show what we found
            if data['indexeddb']:
                print("\n[+] IndexedDB Databases:")
                for name, info in list(data['indexeddb'].items())[:10]:
                    print(f"    - {name}")
            
            if data['databases']:
                print("\n[+] Database Files:")
                for name, info in data['databases'].items():
                    print(f"    - {name}")
                    if info['tables']:
                        print(f"      Tables: {', '.join(info['tables'][:3])}")
    
    except Exception as e:
        results["error"] = str(e)
        results["status"] = "error"
        print(f"[!] ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    # Save results
    output_file = Path("gemini_local_database_scan.json")
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print()
    print(f"[3] Saved to: {output_file}")
    print()
    print("=" * 70)
    print("DONE")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Check gemini_local_database_scan.json to see what databases exist")
    print("2. If you see IndexedDB or Local Storage entries, we can parse them")
    print("3. Look for anything with 'gemini', 'bard', 'chat', or 'conversation'")

if __name__ == "__main__":
    main()
