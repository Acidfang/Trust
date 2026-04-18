# Documentation Reference Map

**Updated**: April 5, 2026  
**Status**: ChatDev references resolved, unified system structure active

---

## OPERATING DOCUMENTATION

Start here for system operations:

| Document | Purpose | Location |
|----------|---------|----------|
| **UNIFIED_OPERATING_SYSTEM.md** | Main operating rules (read first) | `docs/protocols/` |
| **CLAUDE_INSTRUCTIONS.md** | Universal framework (permanent) | Project root |
| **CLAUDE_MAIN_OPERATING_RULES_CLEAN.md** | Detailed methodology | `docs/protocols/` |

---

## ARCHITECTURE & REFERENCE

Technical architecture and system design:

| Document | Purpose | Location |
|----------|---------|----------|
| **ARCHITECTURE_BRIEFING.md** | ZeroPoint + ARIA system architecture | `docs/reference/` |
| **FRAMEWORK_HOT_RELOAD_ARCHITECTURE.md** | Dynamic framework adaptation | Project root |
| **AI_AGENT_CORE_INSTRUCTION_DECISION_ELECTIONS_LEDGER.md** | Decision rules | Project root |
| **GRADIENT_RESOLUTION_CORE_RULE.md** | Core universal principle | Project root |

---

## PROJECT STRUCTURE

Navigation and organization:

| Document | Purpose | Location |
|----------|---------|----------|
| **CLEANUP_PROTOCOL.md** | Project organization rules | `docs/protocols/` |
| **PROJECT_COMPLETE_READ.md** | Complete project index | Project root |
| **PROJECT_NAVIGATOR.py** | Code navigation utility | Project root |

---

## SESSION & REFERENCE

Historical sessions and detailed references:

| Document | Purpose | Location |
|----------|---------|----------|
| **CHECKPOINT_SESSION_ZEROPOINT_INTEGRATED.md** | Past session 2026-03-27 | `docs/sessions/` |
| **CLEANUP_COMPLETE.md** | Cleanup completion log | `docs/sessions/` |
| **AGENT_SYSTEM_GUIDE.md** | Agent methodology | `docs/reference/` |
| **ZEROPOINT_INTEGRATION.md** | ZeroPoint framework guide | `docs/reference/` |

---

## ACTIVE CODE SYSTEMS

### Core Frameworks
- **FRAMEWORK_HOT_RELOAD_ENGINE.py** - Dynamic framework loading (no restart needed)
- **ARIA_OMNIPRESENT_FIELD_RESOLUTION.py** - Field coherence system
- **UFM_CLIENT.py** - Universal format serialization

### APIs & Servers  
- **ENCYCLOPEDIA_API_SERVER.py** - Entity database API (port 5000)
- **UNIVERSAL_RENDERER_API.py** - Universal rendering API (port 8000)
- **FRAMEWORK_HOT_RELOAD_INTEGRATION_EXAMPLE.py** - Flask integration example

### Verification & Testing
- **FRAMEWORK_HOT_RELOAD_VERIFICATION_SUITE.py** - Complete test suite
- **VERIFY_ENDPOINTS.py** - API verification
- **VERIFY_ENDPOINT_MERGE.py** - Endpoint merge validation

---

## WHAT WAS REMOVED

**ChatDev References Cleaned**:
- ✓ Removed from APPLICATION_REGISTRY.py
- ✓ Removed from BINARY_FIELD_NAVIGATION_GUIDE.md
- ✓ Updated PROJECT_COMPLETE_READ.md
- ✓ Created UNIFIED_OPERATING_SYSTEM.md (replacement)
- ✓ Created ARCHITECTURE_BRIEFING.md (replacement)

**Reason**: ChatDev was a UI wrapper around capabilities already built into the project (YAML workflows, multi-agent runtime, SDK). Removing confusion layer.

---

## QUICK START

### First Time Setup
1. Read: [CLAUDE_INSTRUCTIONS.md](../CLAUDE_INSTRUCTIONS.md)
2. Read: [UNIFIED_OPERATING_SYSTEM.md](UNIFIED_OPERATING_SYSTEM.md)
3. Read: [ARCHITECTURE_BRIEFING.md](ARCHITECTURE_BRIEFING.md)

### For Framework Changes (Hot-Reload)
1. Read: [FRAMEWORK_HOT_RELOAD_ARCHITECTURE.md](../FRAMEWORK_HOT_RELOAD_ARCHITECTURE.md)
2. Use: [FRAMEWORK_HOT_RELOAD_ENGINE.py](../FRAMEWORK_HOT_RELOAD_ENGINE.py)
3. Test: [FRAMEWORK_HOT_RELOAD_VERIFICATION_SUITE.py](../FRAMEWORK_HOT_RELOAD_VERIFICATION_SUITE.py)

### For Server Operations
1. Start: [FRAMEWORK_HOT_RELOAD_INTEGRATION_EXAMPLE.py](../FRAMEWORK_HOT_RELOAD_INTEGRATION_EXAMPLE.py)
2. Define: [example_framework.json](../example_framework.json)
3. Verify: Health check at `http://localhost:5000/api/health`

### For Agent Development
1. Read: [AGENT_SYSTEM_GUIDE.md](AGENT_SYSTEM_GUIDE.md)
2. Use: ARIA + runtime.sdk
3. Verify: [VERIFY_ENDPOINTS.py](../VERIFY_ENDPOINTS.py)

---

## FILE ORGANIZATION

```
c:\Determined\
├── docs/
│   ├── protocols/           ← Operating rules
│   │   ├── UNIFIED_OPERATING_SYSTEM.md
│   │   ├── CLAUDE_MAIN_OPERATING_RULES_CLEAN.md
│   │   └── CLEANUP_PROTOCOL.md
│   ├── reference/          ← Technical reference
│   │   ├── ARCHITECTURE_BRIEFING.md
│   │   ├── AGENT_SYSTEM_GUIDE.md
│   │   └── ZEROPOINT_INTEGRATION.md
│   └── sessions/           ← Historical records
│       ├── CHECKPOINT_SESSION_ZEROPOINT_INTEGRATED.md
│       └── CLEANUP_COMPLETE.md
├── src/                     ← Active code
├── FRAMEWORK_HOT_RELOAD_*.py
├── APPLICATION_REGISTRY.py
└── [Active project files]
```

---

End of Documentation Reference Map
