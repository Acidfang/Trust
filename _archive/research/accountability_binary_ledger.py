#!/usr/bin/env python3
"""
BINARY LEDGER WITH ACTUAL TIMESTAMPS
Each entry records an action with its actual timestamp (from file metadata or explicit specification).
No backdating. No retroactive claims. Pure accountability.
"""

import struct
import hashlib
from datetime import datetime
from pathlib import Path


class AccountableBinaryLedger:
    """
    Binary ledger recording actions with ACTUAL timestamps.
    Not "when I'm recording" but "when the action actually occurred."
    """
    
    VECTOR_VERIFIED = 0x01
    VECTOR_UNVERIFIED = 0x00
    
    def __init__(self, ledger_path: str = "accountability.ledger"):
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.ledger_path.exists():
            self.ledger_path.write_bytes(b"")
    
    def record_from_file(self, file_path: str, symbol: str, action_description: str, verified: bool = True) -> bool:
        """
        Record action using file's actual last-modified timestamp.
        
        Args:
            file_path: Path to file (its mtime becomes the action timestamp)
            symbol: Symbol for this action (stored as-is)
            action_description: What was done
            verified: Boolean verification state
        
        Returns:
            True if recorded successfully
        """
        try:
            # Get file's ACTUAL modification time
            file_obj = Path(file_path)
            if not file_obj.exists():
                return False
            
            actual_timestamp = int(file_obj.stat().st_mtime)
            
            return self._record_with_timestamp(symbol, action_description, verified, actual_timestamp)
        
        except Exception as e:
            print(f"Failed to record from file: {e}")
            return False
    
    def record_with_timestamp(self, symbol: str, action_description: str, verified: bool, timestamp: datetime) -> bool:
        """
        Record action with explicit timestamp (for manual control).
        
        Args:
            symbol: Symbol as-is
            action_description: What was done
            verified: Boolean verification state
            timestamp: Explicit datetime for this action
        
        Returns:
            True if recorded
        """
        timestamp_int = int(timestamp.timestamp())
        return self._record_with_timestamp(symbol, action_description, verified, timestamp_int)
    
    def _record_with_timestamp(self, symbol: str, action_description: str, verified: bool, timestamp_int: int) -> bool:
        """Internal: record with given timestamp integer."""
        try:
            # Symbol as UTF-8 (NO translation)
            symbol_bytes = symbol.encode('utf-8')
            symbol_length = len(symbol_bytes)
            
            # Vector
            vector_byte = bytes([self.VECTOR_VERIFIED if verified else self.VECTOR_UNVERIFIED])
            
            # Hash of action
            action_hash = hashlib.sha256(action_description.encode()).digest()
            
            # Timestamp (as provided, not current time)
            timestamp_bytes = struct.pack("<Q", timestamp_int)
            
            # Entry: [symbol_len:2][symbol:N][timestamp:8][vector:1][hash:32]
            length_bytes = struct.pack("<H", symbol_length)
            entry = length_bytes + symbol_bytes + timestamp_bytes + vector_byte + action_hash
            
            with open(self.ledger_path, "ab") as f:
                f.write(entry)
            
            return True
        
        except Exception as e:
            print(f"Ledger write failed: {e}")
            return False
    
    def read_entries(self) -> list:
        """Read all entries from ledger."""
        data = self.ledger_path.read_bytes()
        entries = []
        offset = 0
        
        while offset < len(data):
            if offset + 2 > len(data):
                break
            
            symbol_length = struct.unpack("<H", data[offset:offset+2])[0]
            offset += 2
            
            if offset + symbol_length > len(data):
                break
            
            symbol_bytes = data[offset:offset+symbol_length]
            offset += symbol_length
            
            try:
                symbol = symbol_bytes.decode('utf-8')
            except:
                symbol = f"<binary: {symbol_bytes.hex()}>"
            
            if offset + 8 > len(data):
                break
            
            timestamp_int = struct.unpack("<Q", data[offset:offset+8])[0]
            offset += 8
            timestamp = datetime.fromtimestamp(timestamp_int)
            
            if offset + 1 > len(data):
                break
            
            vector_byte = data[offset]
            offset += 1
            verified = vector_byte == self.VECTOR_VERIFIED
            
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
        """Generate report."""
        entries = self.read_entries()
        
        report = []
        report.append("[ACCOUNTABILITY BINARY LEDGER]")
        report.append(f"Path: {self.ledger_path.absolute()}")
        report.append(f"Size: {self.ledger_path.stat().st_size} bytes")
        report.append(f"Entries: {len(entries)}")
        report.append("")
        report.append("Entry | Symbol    | Verified | Timestamp (UTC)     | Hash")
        report.append("-" * 75)
        
        for i, entry in enumerate(entries, 1):
            v_str = "✓" if entry["verified"] else "✗"
            timestamp_str = entry["timestamp"].isoformat()
            symbol_str = entry["symbol"][:15]
            report.append(f"[{i:2}] | {symbol_str:15} | {v_str:8} | {timestamp_str} | {entry['hash'][:12]}...")
        
        return "\n".join(report)


# Test: Record actual work from files
if __name__ == "__main__":
    ledger = AccountableBinaryLedger("accountability_test.ledger")
    
    # Clear previous
    ledger.ledger_path.write_bytes(b"")
    
    # Record work using ACTUAL file timestamps
    files_work = [
        ("c:\\Determined\\coherence_verification_binary.py", "claude", "Created binary coherence verifier"),
        ("c:\\Determined\\binary_ledger_pure.py", "claude", "Created pure binary ledger system"),
    ]
    
    for file_path, symbol, description in files_work:
        success = ledger.record_from_file(file_path, symbol, description, verified=True)
        if success:
            print(f"✓ Recorded: {file_path}")
        else:
            print(f"✗ Failed: {file_path}")
    
    print("\n" + ledger.report())
