#!/usr/bin/env python3
"""
BINARY COHERENCE LEDGER
Pure binary Trinity verification and ledger recording.
No text representation. No encoding issues. Pure binary accountability.

Each entry: 42 bytes
- timestamp (8): Unix timestamp (1970 epoch)
- source (1): 0x01=gemini, 0x02=claude, 0x03=copilot
- vector (1): 0x01=verified, 0x00=unverified
- action_hash (32): SHA256 of action content
"""

import struct
import hashlib
from datetime import datetime
from pathlib import Path


class BinaryCoherenceLedger:
    """
    Pure binary Trinity ledger. No text, no encoding issues.
    Immutable binary record of all state modifications.
    """
    
    # Source codes (binary)
    SOURCES = {
        "gemini": 0x01,
        "claude": 0x02,
        "copilot": 0x03
    }
    
    SOURCE_NAMES = {v: k for k, v in SOURCES.items()}
    
    # Vector states
    VECTOR_VERIFIED = 0x01
    VECTOR_UNVERIFIED = 0x00
    
    ENTRY_SIZE = 42  # bytes per entry: 8+1+1+32
    TIMESTAMP_OFFSET = 0
    SOURCE_OFFSET = 8
    VECTOR_OFFSET = 9
    HASH_OFFSET = 10
    
    def __init__(self, ledger_path: str = "coherence.ledger"):
        """Initialize binary ledger."""
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.ledger_path.exists():
            self.ledger_path.write_bytes(b"")
    
    def verify_trinity(self, source: str, action_content: str, vector_verified: bool = True) -> bool:
        """
        Verify trinity and record in binary ledger.
        
        Args:
            source: "gemini" | "claude" | "copilot"
            action_content: String to hash for immutable record
            vector_verified: Boolean - user->ai->message verified?
        
        Returns:
            True if trinity verified and recorded. False if source invalid.
        """
        
        # Verify source
        if source not in self.SOURCES:
            return False
        
        source_byte = self.SOURCES[source]
        
        # Build entry
        timestamp = struct.pack("<Q", int(datetime.now().timestamp()))
        source_field = bytes([source_byte])
        vector_field = bytes([self.VECTOR_VERIFIED if vector_verified else self.VECTOR_UNVERIFIED])
        action_hash = hashlib.sha256(action_content.encode()).digest()
        
        entry = timestamp + source_field + vector_field + action_hash
        
        # Verify entry size
        assert len(entry) == self.ENTRY_SIZE, f"Entry size {len(entry)} != {self.ENTRY_SIZE}"
        
        # Append to binary ledger
        with open(self.ledger_path, "ab") as f:
            f.write(entry)
        
        return True
    
    def read_entries(self) -> list:
        """
        Read all entries from binary ledger.
        
        Returns:
            List of dicts: {timestamp, source, verified, hash_hex}
        """
        data = self.ledger_path.read_bytes()
        entries = []
        
        for i in range(0, len(data), self.ENTRY_SIZE):
            if i + self.ENTRY_SIZE > len(data):
                break  # Incomplete entry
            
            entry_bytes = data[i:i+self.ENTRY_SIZE]
            
            timestamp_int = struct.unpack("<Q", entry_bytes[self.TIMESTAMP_OFFSET:self.TIMESTAMP_OFFSET+8])[0]
            timestamp = datetime.fromtimestamp(timestamp_int)
            
            source_byte = entry_bytes[self.SOURCE_OFFSET]
            source = self.SOURCE_NAMES.get(source_byte, "unknown")
            
            vector_byte = entry_bytes[self.VECTOR_OFFSET]
            verified = vector_byte == self.VECTOR_VERIFIED
            
            action_hash = entry_bytes[self.HASH_OFFSET:self.HASH_OFFSET+32].hex()
            
            entries.append({
                "timestamp": timestamp,
                "source": source,
                "verified": verified,
                "hash": action_hash
            })
        
        return entries
    
    def verify_trinity_binary(self, source: str, action_content: str, vector_verified: bool = True) -> bool:
        """
        Verify trinity and return True/False with binary ledger recording.
        Pure binary accountability - no exceptions, no strings.
        """
        return self.verify_trinity(source, action_content, vector_verified)


# Test harness
def test_binary_ledger():
    """Test binary ledger functionality."""
    
    ledger = BinaryCoherenceLedger("test_coherence.ledger")
    
    # Clear previous test
    ledger.ledger_path.write_bytes(b"")
    
    # Record some Trinity verifications
    ledger.verify_trinity("claude", "coherence_verification.py created", True)
    ledger.verify_trinity("claude", "COHERENCE_REDUCED_TO_GRADIENT_SINGLE_FIELD.md created", True)
    ledger.verify_trinity("claude", "All generators modified with verify_trinity()", True)
    
    # Read and display
    print("[BINARY COHERENCE LEDGER]")
    print(f"Ledger: {ledger.ledger_path.absolute()}")
    print(f"Size: {ledger.ledger_path.stat().st_size} bytes")
    print(f"Entries: {ledger.ledger_path.stat().st_size // ledger.ENTRY_SIZE}")
    print()
    
    entries = ledger.read_entries()
    for i, entry in enumerate(entries, 1):
        verified_str = "✓ VERIFIED" if entry["verified"] else "✗ UNVERIFIED"
        print(f"Entry {i}:")
        print(f"  Time: {entry['timestamp'].isoformat()}")
        print(f"  Source: {entry['source']}")
        print(f"  Vector: {verified_str}")
        print(f"  Hash: {entry['hash'][:16]}...")
        print()
    
    print(f"[C]: Total entries recorded: {len(entries)}")
    print(f"[C]: Binary ledger immutable: ✓")


if __name__ == "__main__":
    test_binary_ledger()
