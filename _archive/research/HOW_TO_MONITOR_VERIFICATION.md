# How to Monitor Agent Verification

This document explains how to track and verify what I'm doing in real-time.

## Quick Check - What Changed

After I report an action, you can verify by:

**1. Check the Verification Ledger**
```
cat c:\Determined\AGENT_VERIFICATION_LEDGER.md
```
Shows EVERY action I took, success criteria, and verification status.

**2. Check Modified Files**
Using Git (if available):
```powershell
cd c:\Determined
git diff  # See ALL file changes since last commit
git status  # See which files were modified
```

Without Git:
```powershell
# Modified files (recent)
Get-ChildItem -Recurse | Where-Object {$_.LastWriteTime -gt (Get-Date).AddMinutes(-10)}
```

**3. Check Running Processes**
```powershell
# See what Python servers are running
Get-Process | Where-Object {$_.Name -match "python|node|flask"}

# Check if API server is up
curl http://localhost:5000/health
```

**4. Browser Console**
When I make 3D rendering changes:
- Press F12 in browser at http://localhost:5000
- Look for my debug output that shows initialization state
- Example: "Scene initialized: 3 chains, 11 total bytes"

## Verification Symbols

When I report an action, I'll use these symbols:
- ✅ **DONE** - Action complete and verified to work
- ✗ **FAILED** - Attempted but didn't work
- 🔄 **IN PROGRESS** - Currently executing
- ⏳ **WAITING** - Needs user action (like browser refresh)
- ❌ **ABANDONED** - Dead-end, trying different approach

## Action Report Template (What you'll see)

Example of what I'll provide after each action:

```
### ACTION: [Title]
✅ VERIFIED

What I did:
- Modified file X
- Changed Y from A to B  
- Added Z feature

Why I did it:
- User requested X
- Previous approach failed

How I verified:
- Ran test Y, result Z
- Called API endpoint, got response 200
- Checked file content matches expectation

User can verify:
□ Check file at path X (should show Y changed to B)
□ Refresh browser, look for Z feature
□ Run command: `curl http://localhost:5000`
□ Press F12 and check console for "message X"

If something's wrong:
- Undo with: `git revert [commit]` or `delete file X`
- Or contact me and I'll reverse it
```

## What NOT to Trust (Without Verification)

⚠️ I can **claim** something works, but you should **verify** it actually does:
- ❌ Don't trust me saying "3D scene renders" until you refresh browser and see it
- ❌ Don't trust "file modified correctly" until you check the file content  
- ❌ Don't trust "API working" until you test the endpoint yourself
- ✅ **DO** trust the verification ledger - it has proof

## Real-Time Monitoring

**For multi-step work**, you can watch progress live:

```powershell
# Watch the verification ledger update in real-time
Get-Content c:\Determined\AGENT_VERIFICATION_LEDGER.md -Wait

# Watch file changes as I make them
[System.IO.FileSystemWatcher]::new('c:\Determined') | ForEach-Object {
    $_.EnableRaisingEvents = $true
    $_.IncludeSubdirectories = $true
    $_.Changed += {
        Write-Host "Modified: $($_.FullPath)"
    }
}
```

## Questions to Ask Me

When reviewing my work:

1. **"Show me the success criteria"** - I should clearly state what success looks like
2. **"Where's the verification?"** - I should show proof it worked  
3. **"How do I undo this?"** - I should have documented the reverse operation
4. **"What was learned?"** - I should explain what worked and what didn't

## Accountability Chain

1. **I do action A** → Add to ledger with criteria  
2. **I verify A succeeded** → Record proof in ledger
3. **You spot-check the ledger** → Confirm changes or run user verification steps
4. **If failed** → Activate undo, document failure, try different approach
5. **Repeat until success** → Action marked complete only when verified

---

## Current Status

☑️ **Verification ledger system active**  
☑️ **All future actions will be logged**  
⏳ **First action pending browser verification** (3D scene visibility improvement)

Check the ledger file for what I've done and what you need to verify.

