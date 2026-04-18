"""
SHELL ENGINE
FastAPI server. Pure execution shell driven by ledger.

Flow:
INPUT → ledger append → execute → ledger append → return
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import json

from ledger_manager import LedgerManager
from executor import Executor
from state_reconstructor import StateReconstructor


# ============================================================================
# MODELS
# ============================================================================

class IntentRequest(BaseModel):
    type: str
    object_id: str | None = None
    data: Dict[str, Any] | None = None
    message: str | None = None
    x: float | None = None
    y: float | None = None
    z: float | None = None
    key: str | None = None
    value: Any = None


class ShellResponse(BaseModel):
    success: bool
    entry_id: int | None = None
    action: str
    output: Dict[str, Any]
    state: Dict[str, Any]
    error: str | None = None


# ============================================================================
# APP
# ============================================================================

app = FastAPI(title="Ledger Shell", description="Deterministic execution shell")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
ledger = LedgerManager(ledger_path="../../ledger/ledger.json")


# ============================================================================
# ROUTES
# ============================================================================

@app.get("/health")
def health_check():
    """Health check"""
    return {"status": "ok", "ledger_entries": ledger.count()}


@app.post("/api/intent")
def process_intent(request: IntentRequest) -> ShellResponse:
    """
    Process intent:
    1. Get current state from ledger
    2. Execute intent
    3. Append result to ledger
    4. Return result
    """
    
    try:
        # 1. Get current state from ledger
        entries = ledger.read_all()
        current_state = StateReconstructor.reconstruct_from_ledger(entries)
        
        # 2. Execute intent
        result = Executor.execute(request.model_dump(), current_state)
        
        # 3. Append to ledger
        entry = ledger.append(
            intent=request.model_dump(),
            action=result["action"],
            input_data=request.model_dump(),
            output_data=result["output"],
            state_before=current_state,
            state_after=result["state_after"],
            valid=result["valid"]
        )
        
        # 4. Return response
        return ShellResponse(
            success=result["valid"],
            entry_id=entry["id"],
            action=result["action"],
            output=result["output"],
            state=result["state_after"],
            error=result.get("error")
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/state")
def get_state():
    """Get current state"""
    try:
        entries = ledger.read_all()
        state = StateReconstructor.reconstruct_from_ledger(entries)
        return {
            "success": True,
            "entries": len(entries),
            "state": state
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ledger")
def get_ledger():
    """Get entire ledger"""
    try:
        entries = ledger.read_all()
        return {
            "success": True,
            "entries": entries
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ledger/{entry_id}")
def get_entry(entry_id: int):
    """Get specific ledger entry"""
    try:
        entry = ledger.get_by_id(entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        return {
            "success": True,
            "entry": entry
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/state-at/{entry_id}")
def get_state_at(entry_id: int):
    """Get state at specific entry"""
    try:
        entries = ledger.read_all()
        state = StateReconstructor.reconstruct_at_entry(entries, entry_id)
        return {
            "success": True,
            "entry_id": entry_id,
            "state": state
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# STARTUP
# ============================================================================

@app.on_event("startup")
def startup_event():
    print("[SHELL] Ledger-Driven Execution Shell")
    print(f"[SHELL] Ledger path: {ledger.ledger_path}")
    print(f"[SHELL] Initial entries: {ledger.count()}")
    print(f"[SHELL] Server starting on http://127.0.0.1:8000")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
