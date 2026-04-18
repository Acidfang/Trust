"""
SHELL ENGINE - FastAPI backend

Single responsibility: HTTP → ledger → execute → ledger → HTTP

Flow:
1. Accept POST /intent
2. Read current state from ledger
3. Validate intent
4. Execute action deterministically
5. Record result to ledger
6. Return response

No state exists outside ledger.
All responses derived from ledger.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
from typing import Dict, Any

from ledger_core import LedgerCore
from executor import Executor
from state_model import StateModel


# Initialize components
app = FastAPI()
ledger = LedgerCore("../ledger/ledger.json")
executor = Executor()
state_model = StateModel(ledger)


@app.on_event("startup")
async def startup_event():
    """Initialize system on startup."""
    print("[⊙] ZEROPOINT SHELL ENGINE")
    print(f"[⊙] Ledger entries: {len(ledger.all_entries())}")
    print(f"[⊙] Current state: {state_model.get_state()['metadata']}")


@app.post("/intent")
async def handle_intent(intent_data: Dict[str, Any]):
    """
    Main entry point: Accept intent, execute, record.
    
    Intent format:
    {
        "action": "render_object" | "log_message" | "move_object" | "update_state" | "noop",
        "object_id": (optional) string,
        "message": (optional) string,
        "position": (optional) [x, y, z],
        "color": (optional) [r, g, b],
        ...
    }
    
    Response:
    {
        "entry_id": int,
        "valid": bool,
        "action": string,
        "output": object,
        "state_after": object
    }
    """
    
    # Step 1: Get current state (from ledger)
    state_before = state_model.get_state()
    
    # Step 2: Validate intent
    if "action" not in intent_data:
        raise HTTPException(status_code=400, detail="Intent must have 'action'")
    
    # Step 3: Execute deterministically
    valid, output, action_taken = executor.execute(intent_data, state_before)
    
    # Step 4: Update state model
    state_model.refresh()
    state_after = state_model.get_state()
    
    # Step 5: Record to ledger
    entry_id = ledger.append({
        "action": action_taken,
        "input": intent_data,
        "output": output,
        "intent": intent_data,
        "state_before": state_before,
        "state_after": state_after,
        "valid": valid
    })
    
    return JSONResponse({
        "entry_id": entry_id,
        "valid": valid,
        "action": action_taken,
        "output": output,
        "state_after": state_after
    })


@app.get("/state")
async def get_state():
    """Get current state derived from ledger."""
    return JSONResponse(state_model.get_state())


@app.get("/ledger")
async def get_ledger():
    """Return complete ledger."""
    return JSONResponse({
        "entries": ledger.all_entries(),
        "total": len(ledger.all_entries())
    })


@app.get("/ledger/{entry_id}")
async def get_entry(entry_id: int):
    """Get specific ledger entry."""
    entry = ledger.get_entry(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return JSONResponse(entry)


@app.post("/replay")
async def replay_ledger(until_id: int = None):
    """
    Replay ledger from start, reconstructing exact state at that point.
    Used for verification and debugging.
    """
    entries = ledger.replay(until_id)
    
    # Reconstruct state by replaying
    state = {
        "objects": {},
        "messages": [],
        "metadata": {"total_intents": len(entries), "total_valid": 0}
    }
    
    for entry in entries:
        if entry.get("valid"):
            state["metadata"]["total_valid"] += 1
            output = entry.get("output", {})
            if "object_id" in output:
                state["objects"][output["object_id"]] = output
    
    return JSONResponse({
        "replayed_entries": len(entries),
        "reconstructed_state": state
    })


@app.get("/health")
async def health():
    """Health check."""
    return JSONResponse({
        "status": "operational",
        "ledger_entries": len(ledger.all_entries()),
        "state": state_model.get_state()
    })


# Serve frontend
frontend_path = Path("../frontend/dist")
if frontend_path.exists():
    app.mount("/app", StaticFiles(directory=str(frontend_path), html=True), name="frontend")


@app.get("/")
async def root():
    """Redirect to frontend."""
    frontend_file = Path("../frontend/dist/index.html")
    if frontend_file.exists():
        return FileResponse(str(frontend_file))
    return JSONResponse({"message": "ZEROPOINT Shell Engine running. POST /intent to execute."})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)
