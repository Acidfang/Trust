#!/usr/bin/env python3
"""
BINARY COHERENCE LEDGER - PURE REPRESENTATION
No translation layers. Symbols are stored as-is in their binary form (UTF-8 bytes).
Whatever symbol is provided becomes the canonical binary record.
"""

import struct
import hashlib
from datetime import datetime
from pathlib import Path


class BinaryLedger:
    """
    Pure binary ledger. Zero translation.
    - Symbol: stored as UTF-8 bytes as-is
    - Timestamp: Unix epoch (8 bytes)
    - Vector: binary (1 byte: 0x01=verified, 0x00=unverified)  
    - Hash: SHA256 (32 bytes)
    
    Entry format (variable length):
    [symbol_length:2][symbol_bytes:N][timestamp:8][vector:1][hash:32]
    """
    
    VECTOR_VERIFIED = 0x01
    VECTOR_UNVERIFIED = 0x00
    
    def __init__(self, ledger_path: str = "coherence.ledger"):
        """Initialize binary ledger."""
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.ledger_path.exists():
            self.ledger_path.write_bytes(b"")
    
    def record(self, symbol: str, action_content: str, verified: bool = True) -> bool:
        """
        Record entry to binary ledger.
        
        Args:
            symbol: Any symbol/text (stored as UTF-8 bytes as-is)
            action_content: Content to hash
            verified: Boolean vector state
        
        Returns:
            True if recorded successfully
        """
        
        try:
            # Symbol as UTF-8 bytes (NO translation)
            symbol_bytes = symbol.encode('utf-8')
            symbol_length = len(symbol_bytes)
            
            # Timestamp
            timestamp_int = int(datetime.now().timestamp())
            timestamp_bytes = struct.pack("<Q", timestamp_int)
            
            # Vector
            vector_byte = bytes([self.VECTOR_VERIFIED if verified else self.VECTOR_UNVERIFIED])
            
            # Action hash
            action_hash = hashlib.sha256(action_content.encode()).digest()
            
            # Build entry: [length:2][symbol:N][timestamp:8][vector:1][hash:32]
            length_bytes = struct.pack("<H", symbol_length)
            entry = length_bytes + symbol_bytes + timestamp_bytes + vector_byte + action_hash
            
            # Write to ledger
            with open(self.ledger_path, "ab") as f:
                f.write(entry)
            
            return True
        
        except Exception as e:
            print(f"Ledger write failed: {e}")
            return False
    
    def read_entries(self) -> list:
        """
        Read all entries from binary ledger.
        
        Returns:
            List of dicts: {symbol, timestamp, verified, hash_hex}
        """
        data = self.ledger_path.read_bytes()
        entries = []
        offset = 0
        
        while offset < len(data):
            # Read symbol length
            if offset + 2 > len(data):
                break
            
            symbol_length = struct.unpack("<H", data[offset:offset+2])[0]
            offset += 2
            
            # Read symbol bytes
            if offset + symbol_length > len(data):
                break
            
            symbol_bytes = data[offset:offset+symbol_length]
            offset += symbol_length
            
            try:
                symbol = symbol_bytes.decode('utf-8')
            except:
                symbol = f"<invalid UTF-8: {symbol_bytes.hex()}>"
            
            # Read timestamp
            if offset + 8 > len(data):
                break
            
            timestamp_int = struct.unpack("<Q", data[offset:offset+8])[0]
            offset += 8
            timestamp = datetime.fromtimestamp(timestamp_int)
            
            # Read vector
            if offset + 1 > len(data):
                break
            
            vector_byte = data[offset]
            offset += 1
            verified = vector_byte == self.VECTOR_VERIFIED
            
            # Read hash
            if offset + 32 > len(data):
                break
            
            action_hash = data[offset:offset+32].hex()
            offset += 32
            
            entries.append({
                "symbol": symbol,
                "timestamp": timestamp,
                "verified": verified,
                "hash": action_hash
            })
        
        return entries
    
    def report(self) -> str:
        """Generate human-readable report of ledger."""
        entries = self.read_entries()
        
        report = []
        report.append("[BINARY COHERENCE LEDGER]")
        report.append(f"Ledger: {self.ledger_path.absolute()}")
        report.append(f"Size: {self.ledger_path.stat().st_size} bytes")
        report.append(f"Entries: {len(entries)}")
        report.append("")
        
        for i, entry in enumerate(entries, 1):
            verified_str = "✓" if entry["verified"] else "✗"
            report.append(f"[{i}] {entry['symbol']:20} | {verified_str} | {entry['timestamp'].isoformat()} | {entry['hash'][:12]}...")
        
        return "\n".join(report)


# Test with various symbols
if __name__ == "__main__":
    ledger = BinaryLedger("test_pure.ledger")
    
    # Clear
    ledger.ledger_path.write_bytes(b"")
    
    # Record with different symbols (as-is, no translation)
    ledger.record("◇", "coherence_verification.py created", True)
    ledger.record("[C]:", "COHERENCE_REDUCED.md created", True)
    ledger.record("claude", "generator modified", True)
    ledger.record("✓ VERIFIED", "all checks passed", True)
    ledger.record("×", "verification failed", False)
    
    print(ledger.report())
