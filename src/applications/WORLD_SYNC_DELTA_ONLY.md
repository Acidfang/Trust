# World Synchronization: Delta-Only Model

## Principle: Only Changes Sync

- **On share:** World snapshot sent once to establish state
- **After share:** Only deltas written to ledger (changes, not full state)
- **Physics:** Each system runs independently, calculates locally
- **Sync point:** Only externally observable changes recorded as deltas

---

## Data Flow

### Initial Connection
```
User A (system 1) shares world:garden with User B (system 2)

1. ledger.send_world_to_user("world:garden", "user:B", token)
   → ledger_worlds.jsonl (world metadata)
   → ledger_world_state.jsonl (complete snapshot)
   → ledger_world_deltas.jsonl (previous changes)
   → ledger_user_positions.jsonl (user positions)
   
2. User B receives transmission
   Reconstructs world from snapshot + all deltas
   System B now has identical state to System A
   
3. User B enters world in their system
   System A detects new user position
```

### Continuous Synchronization
```
System A: User moves avatar
→ ledger.update_user_position(world, user, x, y, z)
  Entry: pos:world:garden:user:B:timestamp
  Ledger: ledger_user_positions.jsonl
  
System B polls ledger every 100ms
→ ledger.get_user_position_updates_since("world:garden", last_poll_time)
  Returns: [User A moved from (100,100) to (150,100)]
  System B renders User A's avatar at new position
  
System B: User places object
→ ledger.apply_world_delta("world:garden", "user:B", "object_add", {id: "obj:123", x: 200, y: 200})
  Entry: delta:world:garden:user:B:timestamp
  Ledger: ledger_world_deltas.jsonl
  Collab tracking: who placed object, when
  
System A polls ledger every 100ms
→ ledger.get_world_deltas_since("world:garden", last_poll_time)
  Returns: [Object placed at (200, 200) by User B]
  System A reconstructs world state
  System A's physics sees new object → gravity applies locally
```

---

## Physics Distribution

**System A performs physics calculation:**
- User A walks and collides with object → collision detected
- Delta recorded: `{delta_type: "entity_update", user: A, change: "position updated to (x,y)"}` 
- Other systems poll and get position change
- Each system applies gravity to that object independently

**System B performs physics calculation:**
- Object was placed, gravity acts on it → falls
- Delta recorded: `{delta_type: "object_moved", change: "object:123 fell to z:50"}`
- System A polls and sees object moved
- System A applies local physics validation
- Consensual state: all systems converge on same position

---

## Why This Works

| Aspect | Traditional | Delta-Only |
|--------|------------|-----------|
| Network load | Object state every frame | Only when state changes |
| Physics sync | Replicated on all systems | Each system calculates |
| Conflicts | Potential (who's right?) | Resolved by delta timestamp |
| Bandwidth | O(objects * clients * fps) | O(changes per second) |
| Latency | High (calculate → transmit) | Low (delta only) |
| Scalability | Degrades with users | Independent per system |

---

## Implementation Pattern

```python
# On user input (e.g., avatar moves)
if system_A_detected_input("move_avatar"):
    new_x, new_y, new_z = calculate_new_position()
    ledger.update_user_position(world, user_A, new_x, new_y, new_z)
    # Just record the new position
    # That's it - no physics replication

# On physics calculation (e.g., gravity)
if system_B_calculates_physics():
    for obj in world.objects:
        obj.apply_gravity()  # Local calculation
        obj.check_collisions()  # Local calculation
        if obj.position_changed:
            ledger.apply_world_delta(world, user_B, "object_update", {
                "id": obj.id,
                "x": obj.x,
                "y": obj.y,
                "z": obj.z
            })
            # Only changed position recorded
            # Other systems will see it and apply physics independently

# On other system polling
if system_A_needs_sync():
    deltas = ledger.get_world_deltas_since(world, last_sync_time)
    for delta in deltas:
        world.apply_delta(delta)
        # World now reflects external changes
        # Physics already calculated by source system
        # This system will calculate next frame
```

---

## Conflict Resolution

**Timestamp-based:** If two systems try to move same object simultaneously:

```
System A: obj:123 → (100, 100) at T1
System B: obj:123 → (150, 50)  at T1 + 0.001s

Ledger has both deltas with timestamps.
System that calculates physics first wins (timestamp).
Other system sees delta, recalculates from known state.
No sync needed - just follow timestamp order.
```

---

## Zero Physics Replication

System A doesn't need to know:
- How System B calculates gravity
- What System B's collision algorithms are
- System B's physics timestep or accuracy

Only needs to know:
- What changed (the delta)
- When it changed (timestamp)
- What the new state is

Each system converges on same observable reality through independent calculation + shared delta log.

---

## Scaling Benefit

10 users in same world:
- 10 systems all running physics independently
- Only position changes, collisions, placements written to ledger
- Ledger has ~10-20 deltas per second (user movements + physics results)
- Not: 10 systems × 60fps × state transmission = 600 updates/sec

Network: O(changes) not O(users × fps)
Computation: Fully distributed
State consistency: Timestamp-ordered deltas

