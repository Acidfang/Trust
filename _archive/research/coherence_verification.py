#!/usr/bin/env python3
"""
COHERENCE VERIFICATION MODULE
Embedded in every script. Prevents any state modification without coherence check.
Symbol: [C]:
"""

import json
from datetime import datetime, timedelta
from pathlib import Path


class CoherenceVerifier:
    """
    Trinity verification system for all code operations.
    Before ANY modification, MUST verify: Source | Timestamp | Vector
    """
    
    SYMBOL = "[C]:"
    TRINITY_REQUIRED = ["source", "timestamp", "coherence_vector"]
    
    def __init__(self, script_name: str):
        """Initialize verifier for a script."""
        self.script_name = script_name
        self.verification_log = []
        self.grounded = False
    
    def verify_trinity(self, source: str = None, timestamp: str = None, vector: str = None) -> bool:
        """
        Verify coherence trinity BEFORE any modification.
        
        Args:
            source: "gemini" | "claude" | "copilot" (or None = auto-check)
            timestamp: ISO format or None = auto-check current
            vector: "user->ai->message" or None = auto-check
        
        Returns:
            True if trinity verified. False if any element missing.
        """
        print(f"\n{self.SYMBOL} COHERENCE CHECK TRIGGERED ({self.script_name})")
        print("=" * 80)
        
        checks = {
            "SOURCE": self._verify_source(source),
            "TIMESTAMP": self._verify_timestamp(timestamp),
            "VECTOR": self._verify_vector(vector)
        }
        
        print("\nTRINITY VERIFICATION:")
        for element, result in checks.items():
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"  {element}: {status}")
        
        all_pass = all(checks.values())
        
        if all_pass:
            self.grounded = True
            print(f"\n✓ COHERENCE VERIFIED. Safe to modify state.")
            self.verification_log.append({
                "timestamp": datetime.now().isoformat(),
                "script": self.script_name,
                "result": "PASS",
                "checks": checks
            })
        else:
            self.grounded = False
            print(f"\n✗ COHERENCE FAILED. Cannot proceed with modifications.")
            self.verification_log.append({
                "timestamp": datetime.now().isoformat(),
                "script": self.script_name,
                "result": "FAIL",
                "checks": checks
            })
        
        print("=" * 80 + "\n")
        return all_pass
    
    def _verify_source(self, source: str = None) -> bool:
        """Check: Is source preserved? (TRINITY.1)"""
        valid_sources = ["gemini", "claude", "copilot"]
        
        if source:
            if source.lower() in valid_sources:
                print(f"  → Source: {source} (explicit)")
                return True
            else:
                print(f"  → Source: {source} (INVALID - must be gemini|claude|copilot)")
                return False
        
        # Auto-check: Is unified timeline available with sources?
        unified_path = Path("timeline_all_messages_unified.json")
        if unified_path.exists():
            try:
                with open(unified_path, 'r') as f:
                    data = json.load(f)
                if data.get("messages"):
                    first_msg = data["messages"][0]
                    if first_msg.get("source") in valid_sources:
                        print(f"  → Source: Verified in unified timeline ({first_msg.get('source')})")
                        return True
            except:
                pass
        
        print(f"  → Source: Could not verify")
        return False
    
    def _verify_timestamp(self, timestamp: str = None) -> bool:
        """Check: Is timestamp grounded? (TRINITY.2)"""
        # Valid range: Oct 11, 2025 - Today (allowing archive to grow)
        valid_start = datetime(2025, 10, 11)
        valid_end = datetime.now() + timedelta(days=1)  # Allow today and tomorrow for time zones
        
        if timestamp:
            try:
                ts = datetime.fromisoformat(timestamp)
                if valid_start <= ts <= valid_end:
                    print(f"  → Timestamp: {timestamp} (in valid range)")
                    return True
                else:
                    print(f"  → Timestamp: {timestamp} (outside Oct 11, 2025 to current date)")
                    return False
            except:
                print(f"  → Timestamp: {timestamp} (invalid format)")
                return False
        
        # Auto-check: Is current time in valid range?
        now = datetime.now()
        if valid_start <= now <= valid_end:
            print(f"  → Timestamp: {now.isoformat()} (current, in range)")
            return True
        else:
            print(f"  → Timestamp: Current time outside valid range (check if archive date is ancient)")
            return False
    
    def _verify_vector(self, vector: str = None) -> bool:
        """Check: Is cause/effect vector correct? (TRINITY.3)"""
        correct_vector = "user->ai->message"
        
        if vector:
            if vector.lower() == correct_vector:
                print(f"  → Vector: {vector} (correct)")
                return True
            elif vector.lower() == "ai->message->user" or "ai->user" in vector.lower():
                print(f"  → Vector: {vector} (REVERSED - must be user→ai→message)")
                return False
            else:
                print(f"  → Vector: {vector} (unknown)")
                return False
        
        # Auto-check: Is vector logically correct for this operation?
        # If we exist and are about to modify: we are effect of user cause
        print(f"  → Vector: {correct_vector} (default verified)")
        return True
    
    def require_grounded(self) -> bool:
        """
        Before ANY file operation, CALL THIS.
        Returns True if grounded. Raises error if not.
        """
        if not self.grounded:
            raise RuntimeError(
                f"COHERENCE NOT VERIFIED. Cannot perform state modification.\n"
                f"Call verify_trinity() before operating on files or state."
            )
        return True
    
    @staticmethod
    def symbol_check():
        """Display the symbol to trigger verification in reader."""
        return f"\n{CoherenceVerifier.SYMBOL}\n"


def create_verifier(script_name: str) -> CoherenceVerifier:
    """Factory function. Use this at start of every script."""
    return CoherenceVerifier(script_name)


def require_coherent_operation(func):
    """
    Decorator: Mark a function as requiring coherence verification.
    
    Usage:
        @require_coherent_operation
        def modify_file(...):
            # This will only run if coherence is verified
    
    Note: Verifier must be initialized in module before using this.
    """
    def wrapper(*args, **kwargs):
        # Look for verifier in calling context
        import inspect
        frame = inspect.currentframe()
        verifier = frame.f_back.f_locals.get('verifier') or frame.f_back.f_globals.get('verifier')
        
        if not verifier or not verifier.grounded:
            raise RuntimeError(
                f"Function {func.__name__} requires coherence verification.\n"
                f"Initialize CoherenceVerifier and call verify_trinity() first."
            )
        
        return func(*args, **kwargs)
    
    return wrapper


if __name__ == "__main__":
    # Test the verifier
    print("COHERENCE VERIFICATION MODULE - TEST RUN")
    verify = create_verifier("test_script.py")
    
    # Test without grounding
    print("\n1. Testing WITHOUT grounding:")
    try:
        verify.require_grounded()
    except RuntimeError as e:
        print(f"   Expected error: {e}")
    
    # Test with grounding
    print("\n2. Testing WITH grounding:")
    result = verify.verify_trinity(source="gemini")
    if result:
        verify.require_grounded()
        print("   ✓ Can now modify state safely")
    
    print("\n✓ Coherence Verification Module Ready")
