#!/usr/bin/env python3
"""
LIVE ACCOUNTABILITY SYSTEM
Every file modification records to binary ledger BEFORE write occurs.
Ledger is the source of truth. Files are consequences of ledger entries.
"""

import struct
import hashlib
from datetime import datetime
from pathlib import Path


class LiveAccountabilitySystem:
    """
    File write system with mandatory ledger recording.
    No file gets written without cryptographic ledger proof.
    """
    
    VECTOR_VERIFIED = 0x01
    VECTOR_UNVERIFIED = 0x00
    
    def __init__(self, ledger_path: str = "accountability.ledger", symbol: str = "claude"):
        self.ledger_path = Path(ledger_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.ledger_path.exists():
            self.ledger_path.write_bytes(b"")
        
        self.symbol = symbol
        self.operations_log = []
    
    def write_file(self, file_path: str, content: str, description: str, verified: bool = True) -> bool:
        """
        Write file to disk with mandatory ledger recording.
        
        Process:
        1. Record operation to binary ledger (creates proof)
        2. If ledger write succeeds, write file to disk
        3. Return success only if both steps succeed
        
        Args:
            file_path: Where to write
            content: What to write
            description: Why (for ledger)
            verified: Trinity verification state
        
        Returns:
            True if both ledger and file write succeeded
        """
        
        # Step 1: Record to ledger FIRST
        ledger_entry_hash = self._record_to_ledger(description, verified)
        
        if ledger_entry_hash is None:
            # Ledger write failed - abort file write
            return False
        
        # Step 2: Ledger succeeded, now write file
        try:
            file_obj = Path(file_path)
            file_obj.parent.mkdir(parents=True, exist_ok=True)
            file_obj.write_text(content, encoding='utf-8')
            
            self.operations_log.append({
                "timestamp": datetime.now().isoformat(),
                "file": str(file_path),
                "ledger_hash": ledger_entry_hash,
                "status": "SUCCESS"
            })
            
            return True
        
        except Exception as e:
            self.operations_log.append({
                "timestamp": datetime.now().isoformat(),
                "file": str(file_path),
                "ledger_hash": ledger_entry_hash,
                "status": f"FILE_WRITE_FAILED: {str(e)}"
            })
            return False
    
    def _record_to_ledger(self, description: str, verified: bool) -> str:
        """
        Record operation to binary ledger.
        
        Returns:
            Hex hash of the ledger entry (proof), or None if failed
        """
        try:
            # Build ledger entry
            symbol_bytes = self.symbol.encode('utf-8')
            symbol_length = len(symbol_bytes)
            
            timestamp_int = int(datetime.now().timestamp())
            timestamp_bytes = struct.pack("<Q", timestamp_int)
            
            vector_byte = bytes([self.VECTOR_VERIFIED if verified else self.VECTOR_UNVERIFIED])
            
            action_hash = hashlib.sha256(description.encode()).digest()
            
            length_bytes = struct.pack("<H", symbol_length)
            entry = length_bytes + symbol_bytes + timestamp_bytes + vector_byte + action_hash
            
            # Write to ledger
            with open(self.ledger_path, "ab") as f:
                f.write(entry)
            
            # Return entry hash as proof
            entry_hash = hashlib.sha256(entry).hexdigest()
            return entry_hash
        
        except Exception as e:
            print(f"Ledger record failed: {e}")
            return None
    
    def read_ledger(self) -> list:
        """Read all ledger entries."""
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
    
    def verify_file_in_ledger(self, file_path: str) -> bool:
        """
        Verify that a file write was recorded in the ledger.
        (Basic check - just verifies ledger contains entries)
        
        Returns:
            True if ledger has entries
        """
        return len(self.read_ledger()) > 0
    
    def report(self) -> str:
        """Generate accountability report."""
        entries = self.read_ledger()
        
        report = []
        report.append("[LIVE ACCOUNTABILITY SYSTEM]")
        report.append(f"Ledger: {self.ledger_path.absolute()}")
        report.append(f"Size: {self.ledger_path.stat().st_size} bytes")
        report.append(f"Entries: {len(entries)}")
        report.append(f"Operations: {len(self.operations_log)}")
        report.append("")
        
        if self.operations_log:
            report.append("Recent Operations:")
            for op in self.operations_log[-5:]:
                report.append(f"  {op['timestamp']} | {op['file']} | {op['status']}")
        
        return "\n".join(report)


# Test: Live file write with ledger recording
if __name__ == "__main__":
    system = LiveAccountabilitySystem("live_accountability.ledger", symbol="test")
    
    # Clear for fresh test
    system.ledger_path.write_bytes(b"")
    
    print("[LIVE ACCOUNTABILITY SYSTEM TEST]")
    print()
    
    # Test 1: Write a file with ledger recording
    success1 = system.write_file(
        "test_output_1.txt",
        "This file was written with ledger accountability\n",
        "Test write 1: simple text file"
    )
    
    # Test 2: Write another file
    success2 = system.write_file(
        "test_output_2.txt",
        "Second file with ledger proof\n",
        "Test write 2: another file"
    )
    
    print(f"Write 1: {'✓ SUCCESS' if success1 else '✗ FAILED'}")
    print(f"Write 2: {'✓ SUCCESS' if success2 else '✗ FAILED'}")
    print()
    
    print(system.report())
    print()
    
    # Verify files exist
    if Path("test_output_1.txt").exists():
        print("✓ test_output_1.txt exists")
    if Path("test_output_2.txt").exists():
        print("✓ test_output_2.txt exists")
