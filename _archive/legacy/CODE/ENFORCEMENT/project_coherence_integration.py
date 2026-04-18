"""
Project Coherence Integration - Bridges enforcement system to core engine
Provides unified interface for Trinity verification and auto-rollback
"""

import sys
import os

# Update path to find modules in new structure
_base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if _base_dir not in sys.path:
    sys.path.insert(0, _base_dir)

# Import from new CODE/ENFORCEMENT location
from CODE.ENFORCEMENT.PROJECT_COHERENCE_CHECKPOINT_SYSTEM import (
    CoherenceCheckpoint,
    CoherenceCheckpointSystem,
    ViolationDetector,
    AutoRollbackMechanism
)

# Import core engine
from CODE.CORE.singularity_core import SingularityStore

# Unified enforcement bridge
class ProjectCoherenceIntegration:
    """
    Unified interface providing:
    - Trinity verification gates
    - Checkpoint system integration
    - Auto-rollback on violations
    - Immutable operation ledger
    """
    
    def __init__(self, checkpoint_file=None):
        self.checkpoint_system = CoherenceCheckpointSystem(checkpoint_file or "COHERENCE_CHECKPOINTS.json")
        self.violation_detector = ViolationDetector()
        self.rollback_mechanism = AutoRollbackMechanism()
        self.singularity_store = SingularityStore()
    
    def verify_trinity_and_execute(self, operation_name, operation_func, *args, **kwargs):
        """
        Verify Trinity protocol, then execute operation with checkpoint
        
        Args:
            operation_name: Name of the operation
            operation_func: Callable to execute
            *args: Arguments to pass to operation_func
            **kwargs: Keyword arguments to pass to operation_func
            
        Returns:
            Result if Trinity passes, raises exception if fails
        """
        # Verify Trinity before execution
        source = kwargs.pop('source', None)
        timestamp = kwargs.pop('timestamp', None)
        causality = kwargs.pop('causality', None)
        
        if not all([source, timestamp, causality]):
            raise ValueError("Trinity verification requires source, timestamp, and causality")
        
        # Execute operation with checkpoint
        try:
            result = operation_func(*args, **kwargs)
            
            # Create checkpoint
            checkpoint = CoherenceCheckpoint(
                source=source,
                timestamp=timestamp,
                operation=operation_name,
                files_modified=[],  # Caller can specify
                status="SUCCESS"
            )
            self.checkpoint_system.record_checkpoint(checkpoint)
            
            return result
        except Exception as e:
            # Violation detected - trigger auto-rollback
            self.rollback_mechanism.rollback_operation(operation_name)
            raise

# Singleton instance
_integration = None

def get_integration(checkpoint_file=None):
    """Get or create singleton integration instance"""
    global _integration
    if _integration is None:
        _integration = ProjectCoherenceIntegration(checkpoint_file)
    return _integration

# Status
__version__ = "2.0.0"
__status__ = "Production"
__refactored_date__ = "2026-04-18"
