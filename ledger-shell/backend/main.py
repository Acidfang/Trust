from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os

from ledger import Ledger
from executor import Executor

app = FastAPI(title="Ledger-Driven Shell")

ledger = Ledger("../ledger/ledger.json")
executor = Executor()

current_state = {
    "visual_state": {"objects": []},
    "system_state": {},
    "messages": []
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IntentRequest(BaseModel):
    action: str
    params: Optional[Dict[str, Any]] = None

@app.on_event("startup")
async def startup():
    global current_state
    print("[LEDGER-SHELL] Server started")
    print(f"[LEDGER-SHELL] Ledger entries: {len(ledger.get_all())}")
    current_state = ledger.replay()
    print(f"[LEDGER-SHELL] State replayed from ledger")

@app.post("/api/intent")
async def submit_intent(req: IntentRequest):
    """
    Submit intent to ledger.
    
    Flow:
    1. Accept intent
    2. Append to ledger
    3. Execute deterministically
    4. Append result to ledger
    5. Return result
    """
    global current_state
    
    # Create intent object
    intent = {
        "action": req.action,
        "params": req.params or {}
    }
    
    # Save state before execution
    state_before = dict(current_state)
    
    # Execute action
    output, is_valid = executor.execute(intent, current_state)
    
    # Save state after execution
    state_after = dict(current_state)
    
    # Append to ledger
    entry_id = ledger.append(
        intent=intent,
        action=req.action,
        input_data=req.params or {},
        output_data=output,
        state_before=state_before,
        state_after=state_after,
        valid=is_valid
    )
    
    return {
        "entry_id": entry_id,
        "action": req.action,
        "output": output,
        "valid": is_valid,
        "state": current_state
    }

@app.get("/api/state")
async def get_state():
    """Get current state (replayed from ledger)."""
    return {
        "state": current_state,
        "ledger_entries": len(ledger.get_all())
    }

@app.get("/api/ledger")
async def get_ledger():
    """Get entire ledger."""
    return {
        "entries": ledger.get_all(),
        "count": len(ledger.get_all())
    }

@app.get("/api/ledger/{entry_id}")
async def get_ledger_entry(entry_id: int):
    """Get specific ledger entry."""
    entry = ledger.get_entry(entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry

@app.post("/api/replay")
async def replay_ledger():
    """Replay entire ledger and return reconstructed state."""
    global current_state
    current_state = ledger.replay()
    return {
        "state": current_state,
        "entries_replayed": len(ledger.get_all())
    }

@app.get("/api/health")
async def health():
    """Health check."""
    return {
        "status": "ok",
        "ledger_entries": len(ledger.get_all()),
        "current_view": "main"
    }

@app.get("/")
async def root():
    """Serve frontend."""
    return {"message": "Ledger-Driven Shell - Access /api/health or open frontend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
