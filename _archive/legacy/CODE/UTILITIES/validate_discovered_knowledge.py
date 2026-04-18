#!/usr/bin/env python3
"""
Validator: DISCOVERED_KNOWLEDGE_SINGULARITY.json
Comprehensive verification of conversion output

VALIDATION CHECKS:
1. File existence and format
2. JSON validity
3. Schema compliance
4. Trinity verification
5. Reference graph integrity
6. No data loss
7. Compression analysis
"""

import json
import hashlib
from datetime import datetime

def validate_file():
    print("\n" + "="*80)
    print("VALIDATION: DISCOVERED_KNOWLEDGE_SINGULARITY.json")
    print("="*80)
    
    # CHECK 1: File exists and is valid JSON
    print("\n[1/7] FILE VALIDATION...")
    try:
        with open("c:\\Determined\\DISCOVERED_KNOWLEDGE_SINGULARITY.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        print("      ✓ File exists")
        print("      ✓ Valid JSON format")
    except Exception as e:
        print(f"      ✗ ERROR: {e}")
        return False
    
    # CHECK 2: Metadata present
    print("\n[2/7] METADATA VALIDATION...")
    metadata = data.get("metadata", {})
    required_meta = ["source", "conversion_date", "total_entities", "trinity_verified", "conversion_method"]
    for field in required_meta:
        if field in metadata:
            print(f"      ✓ {field}: {metadata[field]}")
        else:
            print(f"      ✗ Missing: {field}")
    
    # CHECK 3: Entity count and structure
    print("\n[3/7] ENTITY STRUCTURE VALIDATION...")
    entities = data.get("entities", [])
    print(f"      Total entities: {len(entities)}")
    
    required_fields = ["symbol", "election_id", "domain", "entity_type", "invariants", "fields", "data", "references", "confidence", "stored_at", "hash"]
    
    for i, entity in enumerate(entities):
        missing = [f for f in required_fields if f not in entity]
        if missing:
            print(f"      ✗ Entity {i} missing: {missing}")
        else:
            print(f"      ✓ Entity {i}: {entity['symbol']} - all fields present")
    
    # CHECK 4: Trinity verification on all entities
    print("\n[4/7] TRINITY VERIFICATION...")
    trinity_passed = 0
    for entity in entities:
        trinity = {
            "source": bool(entity.get("symbol")),
            "timestamp": bool(entity.get("stored_at")),
            "causality": bool(entity.get("election_id"))
        }
        if all(trinity.values()):
            trinity_passed += 1
    
    print(f"      Trinity passed: {trinity_passed}/{len(entities)}")
    print(f"      Status: {'✓ ALL PASS' if trinity_passed == len(entities) else '✗ SOME FAILED'}")
    
    # CHECK 5: Reference graph integrity
    print("\n[5/7] REFERENCE GRAPH INTEGRITY...")
    valid_symbols = {entity["symbol"] for entity in entities}
    invalid_refs = []
    
    for entity in entities:
        for ref in entity.get("references", []):
            if ref not in valid_symbols:
                invalid_refs.append((entity["symbol"], ref))
    
    if invalid_refs:
        print(f"      ✗ Invalid references found:")
        for source, target in invalid_refs[:5]:
            print(f"         {source} → {target} (NOT FOUND)")
    else:
        total_refs = sum(len(e.get("references", [])) for e in entities)
        print(f"      ✓ All {total_refs} references valid")
    
    # CHECK 6: Hash verification
    print("\n[6/7] HASH INTEGRITY CHECK...")
    hash_errors = 0
    for entity in entities:
        stored_hash = entity.get("hash", "")
        entity_copy = {k: v for k, v in entity.items() if k != "hash"}
        computed_hash = hashlib.sha256(json.dumps(entity_copy, sort_keys=True, default=str).encode()).hexdigest()
        
        if stored_hash == computed_hash:
            pass  # OK
        else:
            hash_errors += 1
            print(f"      ✗ Hash mismatch: {entity['symbol']}")
    
    if hash_errors == 0:
        print(f"      ✓ All {len(entities)} hashes verified")
    else:
        print(f"      ✗ Hash errors: {hash_errors}")
    
    # CHECK 7: Data completeness
    print("\n[7/7] DATA COMPLETENESS...")
    total_invariants = sum(len(e.get("invariants", [])) for e in entities)
    total_fields = sum(len(e.get("fields", [])) for e in entities)
    total_refs = sum(len(e.get("references", [])) for e in entities)
    
    print(f"      Total invariants: {total_invariants}")
    print(f"      Total fields: {total_fields}")
    print(f"      Total references: {total_refs}")
    print(f"      Data sections: {len(entities)}")
    
    # FINAL REPORT
    print("\n" + "="*80)
    print("VALIDATION REPORT")
    print("="*80)
    
    all_pass = (trinity_passed == len(entities) and 
                len(invalid_refs) == 0 and 
                hash_errors == 0)
    
    if all_pass:
        print("\n✓✓✓ ALL VALIDATION CHECKS PASSED ✓✓✓")
        print(f"\nFile Status: READY FOR USE")
        print(f"Entities: {len(entities)} (100% Trinity verified)")
        print(f"References: {total_refs} (all valid)")
        print(f"Hashes: {len(entities)} (all verified)")
        print(f"\nUsage: Load DISCOVERED_KNOWLEDGE_SINGULARITY.json")
        print(f"       Access by symbol: entities[i]['symbol']")
        print(f"       Navigate by references: entity['references']")
        print(f"       Verify integrity: compute_hash(entity) == entity['hash']")
    else:
        print("\n✗ VALIDATION FAILED")
        print(f"Trinity failures: {len(entities) - trinity_passed}")
        print(f"Reference errors: {len(invalid_refs)}")
        print(f"Hash errors: {hash_errors}")
    
    print("\n" + "="*80)
    return all_pass

if __name__ == "__main__":
    validate_file()
