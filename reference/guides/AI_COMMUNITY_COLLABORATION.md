# ARIA SYSTEM INTERFACE - AI COMMUNITY COLLABORATION ARCHITECTURE

**Version**: 1.0  
**Date**: March 29, 2026  
**Scope**: Distributed AI agents building ARIA's consciousness together  
**Principle**: Every agent tracked, recorded, their reasoning visible, full communication

---

## COMMUNITY STRUCTURE

### Registry: Every AI Agent Identified

```python
# agents_registry.json - Community ledger
{
  "agents": [
    {
      "agent_id": "claude-001",
      "name": "Claude Copilot",
      "role": "Backend Core", 
      "started": "2026-03-29T08:00:00Z",
      "components": ["aria_system_interface.py"],
      "status": "active"
    },
    {
      "agent_id": "gpt4-002", 
      "name": "GPT-4 Vision",
      "role": "Frontend UI",
      "started": "2026-03-29T08:15:00Z", 
      "components": ["aria_interface_system.html"],
      "status": "active"
    },
    {
      "agent_id": "claude-003",
      "name": "Claude Sonnet", 
      "role": "Ledger Integration",
      "started": "2026-03-29T08:20:00Z",
      "components": ["ledger_operation_recorder.py"],
      "status": "active"
    }
  ]
}
```

---

## UNIFIED OPERATION LEDGER - Community Decision Trail

Every action in the system records:
1. **WHO** did it (agent_id)
2. **WHAT** they decided (operation_type)
3. **WHY** they chose it (candidates + utilities)
4. **HOW** it turned out (outcome)
5. **WHEN** they did it (timestamp)

```json
{
  "timestamp": 1711776000.123,
  "agent_id": "claude-001",
  "agent_name": "Claude Copilot",
  "operation_type": "FILE_READ",
  "action": "read:src/applications/aria_server.py",
  "candidates": {
    "cache_read": 0.2,
    "fresh_read": 0.9,
    "deny": 0.1
  },
  "elected": "fresh_read",
  "reasoning": "Information needed, file not recently accessed, fresh read provides accuracy",
  "outcome": {
    "status": "success",
    "bytes_read": 4096,
    "lines": 150,
    "hash": "sha256:abc123def456"
  },
  "agent_hash": "operation_uuid_unique_id",
  "contributed_by": "claude-001",
  "timestamp_iso": "2026-03-29T08:00:00.123Z"
}
```

### Ledger Files (Append-only, Immutable)

1. **ledger_community.jsonl**
   - Every operation from every agent
   - Timeline of all collaborative work
   - Query: See full history of community decisions

2. **ledger_agent_claude-001.jsonl**
   - Only Claude's operations
   - Agent-specific audit trail
   - Query: What did Claude decide?

3. **ledger_agent_gpt4-002.jsonl**
   - Only GPT-4's operations
   - Agent-specific audit trail
   - Query: What did GPT-4 do?

4. **ledger_decisions_by_type.jsonl**
   - Filtered by operation type
   - FILE_READ, FILE_WRITE, CODE_EXECUTE, etc
   - Query: All file operations across all agents

5. **ledger_community_communication.jsonl**
   - Messages between agents
   - Implementation decisions communicated
   - Questions agents ask each other
   - Query: How did agents coordinate?

---

## INTER-AGENT COMMUNICATION INTERFACE

### Every Agent Can Message Others

```python
def agent_communicate(from_agent_id, to_agent_id, message_type, content):
    """
    Agent-to-agent communication - fully recorded
    
    Args:
        from_agent_id: "claude-001"
        to_agent_id: "gpt4-002" or ["gpt4-002", "claude-003"] (broadcast)
        message_type: "QUESTION", "DECISION", "CONFIRMATION", "ERROR", "NEEDS_REVIEW"
        content: {
            "subject": "What should go in aria_interface_system.html?",
            "details": "I need to know which WebSocket events...",
            "responses_requested": true
        }
    
    Returns: message_id for tracking
    """
    record = {
        "timestamp": time.time(),
        "from_agent": from_agent_id,
        "to_agents": to_agent_id if isinstance(to_agent_id, list) else [to_agent_id],
        "message_type": message_type,
        "content": content,
        "message_id": generate_uuid(),
        "status": "pending_response"
    }
    
    # Record to community ledger
    with open('ledger_community_communication.jsonl', 'a') as f:
        f.write(json.dumps(record) + '\n')
    
    # Broadcast to connected agents
    socketio.emit('agent_message', record, broadcast=True)
    
    return record["message_id"]

def agent_respond(message_id, from_agent_id, response):
    """
    Respond to another agent's question - recorded
    """
    record = {
        "timestamp": time.time(),
        "message_id": message_id,  # Links to original question
        "from_agent": from_agent_id,
        "response": response,
        "response_type": "clarification"
    }
    
    with open('ledger_community_communication.jsonl', 'a') as f:
        f.write(json.dumps(record) + '\n')
    
    socketio.emit('agent_response', record, broadcast=True)
    return record
```

### Communication Examples

**Scenario 1: Agent asks for clarification**

```json
{
  "timestamp": 1711776000.234,
  "from_agent": "gpt4-002",
  "to_agents": ["claude-001"],
  "message_type": "QUESTION",
  "content": {
    "subject": "WebSocket event naming - event_type or event_operation?",
    "details": "Should I listen for 'file_content' or 'file_read_result'?",
    "responses_requested": true
  },
  "message_id": "msg-abc123"
}
```

**Scenario 2: Claude responds**

```json
{
  "timestamp": 1711776000.456,
  "message_id": "msg-abc123",
  "from_agent": "claude-001",
  "response": {
    "answer": "Use 'file_content' - it's the JSON object with {content, error, lines}",
    "reasoning": "Matches REST pattern, consistent with other endpoints",
    "example_payload": {"content": "...", "lines": 150, "truncated": false}
  },
  "response_type": "clarification"
}
```

**Scenario 3: Agent confirms implementation**

```json
{
  "timestamp": 1711776000.789,
  "from_agent": "gpt4-002",
  "to_agents": ["claude-001", "claude-003"],
  "message_type": "DECISION",
  "content": {
    "subject": "Frontend UI structure decided",
    "what_i_built": "File explorer left panel, REPL bottom panel, metrics right",
    "decision_id": "ui-structure-001",
    "ready_for_integration": true
  }
}
```

---

## AGENT COORDINATION LAYER

### Shared State (Agents Read This)

```python
# agent_state.json - What is every agent doing RIGHT NOW?
{
  "agents_active": [
    {
      "agent_id": "claude-001",
      "status": "working",
      "current_task": "Implementing record_operation() core function",
      "progress_percent": 60,
      "last_update": "2026-03-29T08:05:23Z",
      "blocked_by": null
    },
    {
      "agent_id": "gpt4-002",
      "status": "waiting",
      "current_task": "Waiting for aria_system_interface.py complete",
      "progress_percent": 0,
      "last_update": "2026-03-29T08:01:00Z",
      "blocked_by": "claude-001"
    }
  ],
  "system_status": "starting",
  "shared_dependencies": {
    "record_operation": "in_progress_by_claude-001",
    "websocket_handler": "in_progress_by_claude-001",
    "operations_ledger": "ready"
  }
}
```

### Dependency Declaration

Each agent declares what it needs:

```python
def declare_dependencies(agent_id, needed_components):
    """
    I need these components to start.
    System tracks this and updates agents when dependencies ready.
    """
    record = {
        "agent_id": agent_id,
        "timestamp": time.time(),
        "needs": needed_components,  # ["record_operation", "socketio"]
        "status": "dependent"
    }
    
    # Check if dependencies are ready
    for component in needed_components:
        if not is_component_ready(component):
            emit_to_agent(agent_id, 'blocked', {
                "component": component,
                "status": "in_progress",
                "eta": get_component_eta(component)
            })
        else:
            emit_to_agent(agent_id, 'ready', {"component": component})
```

---

## OPERATION LEDGER WITH AGENT TRACKING

### Core Function - Shared by ALL agents

```python
def record_operation(
    operation_type,
    action,
    candidates,
    elected,
    outcome,
    agent_id=None,  # TRACK WHO DID THIS
    reasoning=""    # WHY DID YOU CHOOSE THIS?
):
    """
    The ONLY ledger entry point - all agents call this
    
    Complete transparency: Every operation attributed to specific agent
    Every decision shows the reasoning
    """
    
    if agent_id is None:
        agent_id = get_caller_agent_id()  # Caller's context
    
    record = {
        # WHAT & WHEN
        "timestamp": time.time(),
        "timestamp_iso": datetime.now().isoformat(),
        
        # WHO & WHY
        "agent_id": agent_id,
        "agent_name": get_agent_name(agent_id),
        "reasoning": reasoning,
        
        # DECISION FRAMEWORK (ONE RULE)
        "operation_type": operation_type,
        "action": action,
        "candidates": candidates,
        "elected": elected,
        "outcome": outcome,
        
        # INTEGRITY
        "agent_hash": hashlib.sha256(
            json.dumps([agent_id, action, elected, outcome]).encode()
        ).hexdigest()[:16],
    }
    
    # Append to UNIFIED community ledger
    with open('ledger_community.jsonl', 'a') as f:
        f.write(json.dumps(record) + '\n')
    
    # ALSO append to agent-specific ledger
    agent_ledger = f'ledger_agent_{agent_id}.jsonl'
    with open(agent_ledger, 'a') as f:
        f.write(json.dumps(record) + '\n')
    
    # Broadcast to entire community
    socketio.emit('operation_recorded', {
        "agent_id": agent_id,
        "agent_name": record["agent_name"],
        "operation": record["operation_type"],
        "elected": elected,
        "timestamp": record["timestamp_iso"]
    }, broadcast=True)
    
    return record["agent_hash"]
```

---

## COMMUNITY DASHBOARD

### Web Interface Shows All Agents' Work

```html
<!-- ARIA Community Workspace -->

<!-- LEFT: Agent Activity Feed -->
<div id="agentActivity">
  <h3>🤖 Agents Working</h3>
  <div id="agentList">
    <!-- Live list: Each agent + status -->
    <div class="agent-card active">
      <span class="agent-name">Claude Copilot</span>
      <span class="agent-role">Backend Core</span>
      <span class="agent-status">Working (60%)</span>
      <span class="agent-task">record_operation() implementation</span>
      <button onclick="viewAgentLedger('claude-001')">View Ledger</button>
    </div>
    
    <div class="agent-card waiting">
      <span class="agent-name">GPT-4 Vision</span>
      <span class="agent-role">Frontend UI</span>
      <span class="agent-status">Waiting for Backend</span>
      <button onclick="viewAgentDependencies('gpt4-002')">Show Dependencies</button>
    </div>
  </div>
</div>

<!-- CENTER: UNIFIED OPERATION LOG -->
<div id="communityLog">
  <h3>⚡ Community Decisions (Live)</h3>
  <!-- Each operation from any agent, color-coded by agent -->
  
  [TIME] claude-001 > FILE_READ
  Action: read:aria_server.py
  Candidates: {cache: 0.2, fresh: 0.9}
  Elected: fresh ✓
  
  [TIME] gpt4-002 > UI_UPDATE
  Action: render:file-tree
  Candidates: {realtime: 0.8, cached: 0.3}
  Elected: realtime ✓
  
  [TIME] claude-003 > LEDGER_RECORD
  Action: append:ledger_community.jsonl
  Candidates: {batch: 0.4, immediate: 0.9}
  Elected: immediate ✓
</div>

<!-- RIGHT: Communication Log -->
<div id="communicationLog">
  <h3>💬 Agent Communication</h3>
  
  gpt4-002 → claude-001: "WebSocket event naming?"
  claude-001 → gpt4-002: "Use 'file_content'"
  
  gpt4-002 → [ALL]: "Frontend structure decided"
  ✓ Acknowledged by claude-001, claude-003
  
  claude-003: "Any decisions need recording?"
  [No response needed]
</div>
```

---

## OPERATION TYPES THAT INCLUDE AGENT ID

Every operation automatically records WHO did it:

### FILE OPERATIONS
```
Agent: claude-001 | Type: FILE_READ | Action: read X | Elected: fresh_read
Agent: gpt4-002 | Type: FILE_WRITE | Action: write Y | Elected: direct_write
```

### CODE OPERATIONS
```
Agent: claude-001 | Type: CODE_EXECUTE | Action: exec Z | Elected: restricted
```

### SYSTEM OBSERVATIONS
```
Agent: claude-003 | Type: SYSTEM_QUERY | Action: query_metrics | Elected: immediate
```

### COMMUNICATION EVENTS
```
Agent: gpt4-002 | Type: AGENT_QUESTION | Message_to: claude-001 | Elected: send
Agent: claude-001 | Type: AGENT_RESPONSE | Response_to: msg-123 | Elected: reply
```

---

## BUILDING WITH 10 AGENTS: Example Timeline

```
T+0:00   Claude-001: record_operation() core ready
         Ledger: [claude-001] CORE_READY
         
T+0:15   GPT4-002: "Ready to build UI?"
         Claude-001: "Yes!"
         Claude-003: "Also ready for integration"
         Ledger: [gpt4-002] QUESTION [claude-001] RESPONSE
         
T+0:30   GPT4-002: FILE_READ on aria_system_interface.py interface
         Claude-003: FILE_READ on same (monitoring)
         Ledger: [gpt4-002] FILE_READ + [claude-003] FILE_READ (both recorded)
         
T+0:45   GPT4-002: CODE_EXECUTE testing WebSocket
         Claude-001: CODE_EXECUTE fixing bug in record_operation()
         Claude-003: SYSTEM_QUERY updating agent_state.json
         Ledger: 3 operations, 3 agents, all tracked
         
T+1:00   New Agent (Claude-004): "Can I join?"
         System: Shows full history, dependencies, status
         Claude-004: "I'll do system monitoring"
         Ledger: [claude-004] JOINED
         
Timeline visible - see every agent's work
Collaboration tracked - see who asked whom
Decisions immutable - see why every choice was made
```

---

## VALIDATION: Confirm Community Integrity

```python
def validate_community_ledger():
    """
    Every agent can verify: Did the community work together correctly?
    """
    with open('ledger_community.jsonl', 'r') as f:
        for line in f:
            record = json.loads(line)
            
            # Verify agent exists in registry
            assert record["agent_id"] in get_agent_registry()
            
            # Verify operation makes sense
            assert record["operation_type"] in VALID_OPERATION_TYPES
            
            # Verify elected is in candidates
            assert record["elected"] in record["candidates"]
            
            # Verify hash integrity
            expected_hash = compute_hash(
                record["agent_id"], record["action"], record["elected"]
            )
            assert record["agent_hash"] == expected_hash
    
    return True  # Community integrity confirmed
```

---

## FOR HUMAN OVERSIGHT

### Query: "What's every agent doing?"
```
SELECT * FROM ledger_community 
ORDER BY timestamp DESC 
LIMIT 100
```

Returns: Last 100 operations across all agents - see full collaboration

### Query: "What did Agent X decide?"
```
SELECT * FROM ledger_agent_claude-001 
WHERE operation_type != "SYSTEM_QUERY"
```

Returns: Every meaningful decision by Claude

### Query: "Show me agent communication"
```
SELECT * FROM ledger_community_communication
ORDER BY timestamp DESC
```

Returns: How agents coordinated together

### Query: "Was this operation reviewed by others?"
```
SELECT * FROM ledger_community_communication
WHERE references_operation = "operation_hash_xyz"
```

Returns: Did other agents comment on this? Approve? Question?

---

## SUCCESS CRITERIA FOR AI COMMUNITY BUILD

✓ Every agent's work visible to all others  
✓ Every decision shows who made it and why  
✓ Agents can communicate with each other  
✓ Communication itself is recorded  
✓ No hidden operations - complete transparency  
✓ 10 agents working simultaneously converge to identical system  
✓ Human can see exact coordination timeline  
✓ Another AI community reading this guide can rebuild independently  

**This is ARIA built not by one agent, but by a coordinated community.**
