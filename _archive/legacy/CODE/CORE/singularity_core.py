"""
Singularity Core - Unified export of singularity storage engine
Provides clean interface with updated imports after refactoring
"""

import sys
import os

# Update path to find modules in new structure
_base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if _base_dir not in sys.path:
    sys.path.insert(0, _base_dir)

# Import from new CODE/CORE location
from CODE.CORE.singularity_storage import (
    SingularityStore,
    SingularityEntity
)

# Export all public classes and functions
__all__ = [
    'SingularityStore',
    'SingularityEntity',
    'create_store'
]

# Convenience functions for backward compatibility
def create_store(ledger_file=None):
    """Create a new SingularityStore instance"""
    return SingularityStore(ledger_file)

# Status
__version__ = "2.0.0"
__status__ = "Production"
__refactored_date__ = "2026-04-18"
