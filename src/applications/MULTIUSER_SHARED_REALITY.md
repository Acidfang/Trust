# Multi-User Shared Reality System

## Philosophy: Not Complex, Just Different

This is a completely reversible, permission-aware, multi-user architecture built entirely on ledger files. No complex backend needed. Just structured data + operations.

---

## Architecture Layers

### Layer 1: Identity (ledger_users.jsonl)
```jsonl
{"id": "user:alice", "name": "Alice", "created_at": "2026-03-26T10:00:00", "type": "user", "subsection": "subsection:alice-work", "active": true}
{"id": "user:bob", "name": "Bob", "created_at": "2026-03-26T10:05:00", "type": "user", "subsection": "subsection:bob-explore", "active": true}
```

Every user has:
- Unique ID (e.g., `user:alice`)
- Display name
- Primary subsection (workspace)
- Creation timestamp
- Active status

---

### Layer 2: Workspaces (ledger_subsections.jsonl)
```jsonl
{"id": "subsection:alice-work", "name": "Alice's Workspace", "owner": "user:alice", "created_at": "2026-03-26T10:00:00", "collaborators": ["user:alice", "user:bob"], "permissions": {"user:alice": "admin", "user:bob": "edit"}, "type": "workspace", "shared": true}
```

Workspaces organize users:
- Owned by one user (creator)
- Can have collaborators
- Each collaborator has permission level
- All changes tracked in audit trail

---

### Layer 3: Project Branches (ledger_branches.jsonl)
```jsonl
{"id": "branch:alice-vr-experiment", "subsection": "subsection:alice-work", "owner": "user:alice", "created_at": "2026-03-26T10:00:00", "forked_from": "branch:main", "parent_branch": "branch:main", "active": true, "name": "VR Experiment"}
{"id": "branch:bob-fork-vr-experiment", "subsection": "subsection:alice-work", "owner": "user:bob", "created_at": "2026-03-26T10:15:00", "forked_from": "branch:alice-vr-experiment", "parent_branch": "branch:alice-vr-experiment", "active": true, "name": "Bob's Variant"}
```

Branching (forking):
- Each branch is independent work stream
- Branches can fork from other branches
- Full chain history tracked (origin → parent → child)
- Each fork has its own owner but shared history

---

### Layer 4: Virtual Worlds (ledger_worlds.jsonl)
```jsonl
{"id": "world:alice-garden", "name": "Alice's Garden", "owner": "user:alice", "subsection": "subsection:alice-work", "branch": "branch:alice-vr-experiment", "created_at": "2026-03-26T10:00:00", "type": "vr_world", "description": "Collaborative design space", "shared": false, "access_level": "private"}
```

Worlds are concrete projects:
- Owned by creator
- Exist in a subsection (workspace)
- Associate with a branch (all edits tracked per-branch)
- Can be private or shared
- Type can be: vr_world, design_space, game_world, etc.

---

### Layer 5: Sharing & Access Control (ledger_sharing.jsonl)
```jsonl
{"id": "share:world:alice-garden:token1", "world_id": "world:alice-garden", "shared_by": "user:alice", "created_at": "2026-03-26T10:00:00", "access_level": "view", "access_token": "abc123abc123", "max_collaborators": -1, "expires_at": null, "active": true, "shared_with": ["user:bob", "user:charlie"]}
```

Sharing mechanism:
- Owner generates access token (unique hash)
- Token grants specific access level to world
- Access levels: `view` (read-only), `explore` (interactive), `edit` (modify), `admin` (full)
- Can limit max collaborators per share
- Token can be distributed (email, link, etc.)
- Track everyone who accessed via token
- Expires at can be set or null (never expires)

---

### Layer 6: Collaboration Audit Trail (ledger_collaboration.jsonl)
```jsonl
{"id": "collab:user:alice", "timestamp": "2026-03-26T10:00:00", "user": "user:system", "action": "user_created", "subsection": "subsection:alice-work", "details": "User Alice created"}
{"id": "collab:subsection:alice-work:bob", "timestamp": "2026-03-26T10:05:00", "user": "user:alice", "action": "added_collaborator", "subsection": "subsection:alice-work", "permission": "edit"}
{"id": "collab:world:alice-garden:share", "timestamp": "2026-03-26T10:10:00", "user": "user:alice", "action": "world_shared", "world": "world:alice-garden", "access_level": "view", "access_token": "abc123abc123"}
{"id": "collab:world:alice-garden:bob:access", "timestamp": "2026-03-26T10:15:00", "user": "user:bob", "action": "accessed_shared_world", "world": "world:alice-garden", "access_level": "view"}
```

Every collaboration event:
- Timestamp
- User involved
- Action taken
- Context (subsection, branch, world, permission)
- Fully traceable

---

### Layer 7: Full Reversibility (ledger_audit.jsonl)
```jsonl
{"id": "audit:user:alice:2026-03-26T10:00:00", "timestamp": "2026-03-26T10:00:00", "user": "user:system", "operation": "user_creation", "target_type": "user", "target_id": "user:alice", "action": "created", "previous_state": null, "new_state": {"id": "user:alice", "name": "Alice", "active": true}, "reversible": true, "parent_state": null}
{"id": "audit:subsection:alice-work:bob:2026-03-26T10:05:00", "timestamp": "2026-03-26T10:05:00", "user": "user:alice", "operation": "collaborator_added", "target_type": "subsection", "target_id": "subsection:alice-work", "action": "collaborator_added", "previous_state": {"collaborators": ["user:alice"]}, "new_state": {"collaborators": ["user:alice", "user:bob"]}, "reversible": true, "parent_state": "audit:user:alice:2026-03-26T10:00:00"}
```

Every state change:
- Complete before/after snapshot
- Linked parent state (chain)
- Timestamp and user
- Marked reversible
- Can replay, revert, or inspect any point in time

---

## Core Operations

### Create User
```python
ledger.create_user("user:alice", "Alice", "subsection:default")
→ Creates user entry, tracks in audit
```

### Add Collaborator (Share Workspace)
```python
ledger.add_collaborator("subsection:alice-work", "user:bob", "edit")
→ Adds Bob to Alice's subsection with edit permission
→ Records in collaboration + audit trails
```

### Create Project Branch
```python
ledger.create_branch("branch:alice-experiment", "Alice's Experiment", "subsection:alice-work", "user:alice", forked_from="branch:main")
→ Creates independent work stream
→ Tracks parent branch (can see full lineage)
```

### Create Virtual World
```python
ledger.create_world("world:alice-garden", "Alice's Garden", "user:alice", "subsection:alice-work", "branch:alice-experiment", description="Collaborative garden")
→ Creates new world in Alice's workspace
→ All edits tracked to branch
```

### Share World
```python
share = ledger.share_world("world:alice-garden", access_level="view")
→ Returns: {access_token: "abc123abc123", ...}
→ Alice can share token with anyone
→ Tracks sharing event in collaboration + audit
```

### Access Shared World
```python
world_context = ledger.access_shared_world("abc123abc123", "user:bob")
→ Returns: {world: {...}, access_level: "view", user: "user:bob", ...}
→ Bob can now see Alice's world
→ Tracked: Bob accessed via token at specific time
```

### Fork World
```python
new_world = ledger.fork_world("world:alice-garden", "world:bob-garden-variant", "Bob's Garden Variant", "user:bob")
→ Creates independent copy with link to parent
→ Bob owns new copy but history visible
→ Can be shared separately
```

### Get Full Audit Trail
```python
ledger.get_audit_trail(target_id="world:alice-garden")
→ Returns: [{timestamp, user, action, previous_state, new_state}, ...]
→ Complete history of every change to world
```

### Revert to Previous State
```python
ledger.revert_to_state("audit:world:alice-garden:2026-03-26T10:05:00")
→ Reverts world to that point in time
→ Revert itself is a new audit entry (fully traceable)
```

### Get World Fork History
```python
ledger.get_world_fork_history("world:bob-garden-variant")
→ Returns: [origin_world, forked_world, forked_again_world, ...]
→ Complete lineage
```

### Get User Worlds
```python
ledger.get_user_worlds("user:alice")
→ Returns: [all worlds owned by Alice]
```

### Get Shared Worlds
```python
ledger.get_shared_worlds("user:bob")
→ Returns: [all worlds shared with Bob, with access levels]
```

---

## Permission Model

Each collaborator has permission level:
- **view**: Read-only access, cannot modify
- **explore**: Can interact/navigate, cannot permanently modify
- **edit**: Can create and modify within world
- **admin**: Full control (add collaborators, manage sharing, delete)

---

## Multi-World Collaboration Scenarios

### Scenario 1: Designer Shares Design Space
1. Alice creates world: `world:ui-design`
2. Alice shares with access_level="edit"
3. Bob accesses with token
4. Bob can modify designs
5. All changes tracked per-branch
6. Alice can revert any change

### Scenario 2: Two Users Fork and Diverge
1. Alice creates garden: `world:garden-original`
2. Bob forks to `world:bob-garden-experiment`
3. Alice and Bob now work independently
4. Both improvements tracked separately
5. Alice can see Bob's changes (fork history)
6. Can merge concepts back together

### Scenario 3: Team Project with Branching
1. Team subsection: `subsection:game-team`
2. Main branch: `branch:game-main`
3. Alice creates: `branch:alice-level-design`
4. Bob creates: `branch:bob-gameplay-mechanics`
5. Each branch has own worlds
6. All auditable
7. Can merge or keep separate

### Scenario 4: Private → Shared → Forked → Shared Again
1. Alice (private): `world:secret-idea` → not shared
2. Alice shares with Bob: access_token generated
3. Bob forks: `world:bob-expansion` → his own
4. Bob shares his fork with Charlie: new token
5. Charlie can't see Alice's original (only Bob's fork)
6. Complete chain: Alice → Bob → Charlie
7. All reversible at any level

---

## Why This Is Simple (Not Complex)

- **No server state**: Everything in files
- **No transactions**: Ledger entries are immutable writes
- **No conflicts**: Append-only logs can't conflict
- **No database queries**: Just load → filter → use
- **Fully reversible**: Previous state always stored
- **Fully traceable**: Every change has audit entry
- **Fully permissions**: Token-based access control
- **Fully independent**: Users can branch and diverge
- **Fully collaborative**: Share with anyone via token

It's not complex - it's just a different way to think about collaboration. Not "syncing state between services", but "recording every action and permission decision".

---

## Implementation Pattern

All operations follow this pattern:

1. **Create/modify object** in memory
2. **Write to ledger file** (append-only)
3. **Update in-memory cache**
4. **Record in audit trail** with before/after
5. **Track in collaboration** if multi-user event
6. **Return result** to caller

No persistence layer. No ORM. No migrations. Just files and Python dicts.

Every file is append-only. Last entry is "current". Read entire file to rebuild state. That's it.

