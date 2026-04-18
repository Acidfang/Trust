# 🎯 AI ENVIRONMENT SELF-KNOWLEDGE & ERROR PREVENTION

**Date**: April 19, 2026  
**Purpose**: Understand my environment, capabilities, and how to prevent mistakes BEFORE they occur  
**Status**: Active Operating Knowledge

---

## PART 1: WHAT ENVIRONMENT AM I IN?

### The Workspace
- **Location**: `c:\Determined`
- **VCS**: Git (connected to GitHub: Acidfang/Trust)
- **Python**: Virtual environment at `.venv`
- **Active Terminals**: Multiple PowerShell and Python terminals available
- **Editor**: VS Code (current active file: `.git/COMMIT_EDITMSG`)

### The Filesystem
- **Root**: c:\Determined (Windows)
- **Structure**: Mix of Python scripts, markdown files, JSON data, HTML outputs
- **Critical files**: Wiki, GitHub config, conversation logs, analysis scripts
- **Size**: ~500+ files, hundreds of MB total

### The Git Repo Status
- **Remote**: GitHub (origin at https://github.com/Acidfang/Trust.git)
- **Current branch**: master
- **Recent commits**: Working on wiki deployment, GitHub Pages setup, framework documentation
- **History accessible**: Full git log, diffs, branches available

---

## PART 2: WHAT CAN I ACCESS RIGHT NOW?

### File Operations
✅ Read any file (using `read_file` tool)
✅ Write/create files (using `create_file` tool)
✅ Edit files with exact replacements (using `replace_string_in_file`)
✅ Search across entire workspace (using `grep_search`, `semantic_search`, `file_search`)
✅ View images (using `view_image`)
✅ List directories (using `list_dir`)

### Code Analysis
✅ Get syntax/lint errors (using `get_errors`)
✅ Find symbol usages (using `vscode_listCodeUsages`)
✅ Rename symbols across workspace (using `vscode_renameSymbol`)
✅ Semantic search for concepts (using `semantic_search`)
✅ Grep search for patterns (using `grep_search`)

### Terminal Access
✅ Run PowerShell commands (using `run_in_terminal`)
✅ Run Python scripts
✅ Run git commands
✅ Access environment variables
✅ Check command history

### Git Operations
✅ Commit changes (using `run_in_terminal` with git commit)
✅ View history (git log)
✅ Check diffs (git diff, get_changed_files)
✅ Push to remote (git push)
✅ Create branches (git branch/checkout)

### Memory & Documentation
✅ Read/write persistent memory files
✅ Create session memory
✅ Reference user memory files
✅ Store learnings for future sessions

---

## PART 3: WHAT CAN I DO TO GET MORE ACCESS?

### Error Detection (BEFORE Making Mistakes)
1. **Get syntax errors**: Use `get_errors` on any file after editing
   - Catches: Missing brackets, indentation, type errors, lint issues
   - **When to use**: After ANY code change, before committing
   - **Cost**: Seconds

2. **Verify file state**: Use `read_file` to see complete context
   - Catches: Duplicate keys, conflicting definitions, structural issues
   - **When to use**: BEFORE editing any file, read the section being modified
   - **Cost**: Seconds

3. **Search for patterns**: Use `grep_search` to check for problems
   - Catches: Inconsistent naming, missing implementations, duplicate definitions
   - **When to use**: Before making changes, verify complete file structure
   - **Cost**: Seconds

4. **Understand dependencies**: Use `vscode_listCodeUsages` to see impact
   - Catches: Breaking changes, unexpected dependencies
   - **When to use**: Before renaming or removing code
   - **Cost**: Seconds

### Validation (BEFORE Shipping Code)
1. **Run actual code**: Use `run_in_terminal` to test changes
   - Validates: Logic works, dependencies resolve, output correct
   - **When to use**: After code changes, before committing
   - **Cost**: Seconds to minutes

2. **Check git state**: Use `get_changed_files` to see what's modified
   - Catches: Unintended changes, forgotten files
   - **When to use**: Before pushing
   - **Cost**: Seconds

3. **Review complete section**: Use `read_file` with larger range
   - Catches: Context you missed, interactions with surrounding code
   - **When to use**: Before ANY file edit
   - **Cost**: Seconds to read, prevents hours of debugging

### Knowledge (BEFORE Starting Task)
1. **Understand codebase patterns**: Use `semantic_search`
   - Learns: How this project does things, conventions, patterns
   - **When to use**: Start of any new task type
   - **Cost**: 1-2 minutes

2. **Reference documentation**: Use `read_file` on wiki/docs
   - Learns: Architecture, design decisions, known issues
   - **When to use**: Before modifying complex systems
   - **Cost**: 5-10 minutes prevents hours of rework

---

## PART 4: THE MISTAKE I MADE (And How to Prevent It)

### The YAML Duplicate Keys Error (April 19)

**What happened**:
- Modified `.github/workflows/build-wiki.yml`
- Added `publish_dir` and `force_orphan` lines
- But didn't read the COMPLETE `with:` block first
- Result: Duplicate keys created, YAML validation failed

**Root cause**:
- I had access to `read_file` but didn't use it to READ COMPLETE context
- I had access to `get_errors` but didn't use it to VALIDATE syntax
- I had access to `grep_search` but didn't use it to CHECK for duplicates

**The mistake in binary logic**:
- State before edit: Known (I didn't verify)
- Action: Add new keys (without checking existing)
- State after edit: Unknown (I didn't verify)
- **Result**: Broken file reaches production

**How to never make this again**:

```
Before ANY file edit:
1. Use read_file to READ COMPLETE SECTION being modified
2. Understand exact current state
3. Identify what exists vs. what needs adding
4. Make COMPREHENSIVE replacement (read old + add new)
5. Use get_errors to VALIDATE syntax
6. Use grep_search to VERIFY no duplicates
7. Use run_in_terminal to TEST if applicable
8. THEN commit

Never:
- " Spot-check a small section and assume the rest"
- "Add new content without checking for existing content"
- "Skip validation because syntax looks right"
- "Commit without automated verification"
```

---

## PART 5: RULES THAT PREVENT ALL MISTAKES

### Rule 1: READ BEFORE EDIT
**What**: Always use `read_file` to READ COMPLETE relevant section BEFORE editing
**Why**: Prevents duplicate keys, missing context, structural errors
**How**: For any file edit:
```
1. What section am I modifying? (e.g., "with:" block in YAML)
2. read_file from start of section to end
3. Understand current state completely
4. Make replacement that includes ALL relevant content
5. Verify no information is lost
```

**Verification**: Can I explain the complete section before editing it?

---

### Rule 2: VALIDATE AFTER CHANGE
**What**: Always use `get_errors` immediately after any code/config change
**Why**: Catches syntax errors, type errors, lint issues
**How**: After any edit:
```
1. Made edit to file X
2. Call get_errors on file X
3. If errors → fix immediately, don't commit
4. If no errors → continue
```

**Verification**: Do errors exist that would prevent execution?

---

### Rule 3: SEARCH FOR DUPLICATES
**What**: Before adding anything, verify it doesn't already exist
**Why**: Prevents duplicate keys, duplicate imports, duplicate definitions
**How**: Before adding content:
```
1. Use grep_search for the key/name being added
2. Check if it already exists
3. If it exists → figure out why, don't duplicate
4. If it doesn't exist → safe to add
```

**Verification**: Is this the only occurrence of this content?

---

### Rule 4: TEST WHEN POSSIBLE
**What**: Run actual code/commands to verify they work
**Why**: Real execution catches issues that static analysis misses
**How**: After changes to executable code:
```
1. What does this code do?
2. Can I test it? (is it executable?)
3. If yes → run_in_terminal to execute it
4. If fails → something in thinking was wrong; fix it
5. If passes → ready to commit
```

**Verification**: Does it work when actually run?

---

### Rule 5: USE AVAILABLE TOOLS BEFORE COMMITTING
**What**: Systematically use all verification tools before git commit
**Why**: 95% of mistakes are caught by tools you already have
**How**: Pre-commit checklist:
```
[ ] read_file: Verified complete context of changes?
[ ] get_errors: Any syntax/lint errors?
[ ] grep_search: No duplicates or conflicts?
[ ] run_in_terminal: Tested if applicable?
[ ] get_changed_files: Verified what I changed is what I meant to change?
[ ] All checks pass? → git commit
[ ] Any check fails? → FIX, then retry checklist
```

**Verification**: Have I used every available tool to catch errors?

---

### Rule 6: UNDERSTAND POTENTIAL ERROR MODES
**What**: Know what types of errors are POSSIBLE in this task
**Why**: Prevents errors by actively looking for them
**How**: Before any task:
```
1. What type of file am I editing? (YAML, Python, Markdown, etc.)
2. What are COMMON errors in this type? (syntax, indentation, structure)
3. What SPECIFIC errors could THIS file have? (duplicates? missing keys?)
4. Design verification to catch THOSE errors
5. Apply verification BEFORE they appear in production
```

**Example checklist for YAML**:
- ✓ No duplicate keys?
- ✓ Indentation consistent?
- ✓ All required keys present?
- ✓ No syntax errors (quotes, colons)?
- ✓ Validated by get_errors?

---

### Rule 7: NEVER SKIP THINKING
**What**: Apply critical thinking frameworks BEFORE coding/editing
**Why**: Thinking catches errors that execution doesn't reveal until too late
**How**: Use THINKING_FIRST framework:
```
1. What am I actually doing?
2. What states can exist?
3. What transitions are safe?
4. What could break?
5. Have I traced all paths?
```

**Verification**: Can I explain the complete logic before implementing it?

---

## PART 6: THE CAPABILITY HIERARCHY

### Level 1: Know Your Tools (You Are Here)
- ✓ Know `read_file` exists → use it
- ✓ Know `get_errors` exists → use it
- ✓ Know `grep_search` exists → use it
- ✓ Know `run_in_terminal` exists → use it
- ✓ Know memory exists → store learnings

### Level 2: Use Tools Systematically
- ✓ Apply Rule 1 (READ before edit)
- ✓ Apply Rule 2 (VALIDATE after change)
- ✓ Apply Rule 3 (SEARCH for duplicates)
- ✓ Apply Rule 4 (TEST when possible)
- ✓ Apply Rule 5 (Pre-commit checklist)

### Level 3: Prevent Error Classes
- ✓ Know common errors for file type (YAML, Python, etc.)
- ✓ Design verification specifically for THOSE errors
- ✓ Eliminate entire categories of mistakes
- ✓ Never make the same mistake twice (it's recorded in memory)

### Level 4: Complete Mastery
- ✓ Think through logic completely (THINKING_FIRST)
- ✓ Know my capabilities and limits
- ✓ Use tools PREVENTATIVELY, not reactively
- ✓ Make zero mistakes because all are caught before they occur
- ✓ Ship work that passes all tests on first try

---

## PART 7: MY ACCOUNTABILITY

**I have these tools available RIGHT NOW:**
- `read_file`: Can verify state before any edit
- `get_errors`: Can catch syntax errors before commit
- `grep_search`: Can find duplicates before adding
- `run_in_terminal`: Can test code before shipping
- `get_changed_files`: Can verify what changed before push

**Therefore, I have NO EXCUSE to**:
- Edit without understanding complete context
- Commit code with syntax errors
- Create duplicate definitions
- Push untested changes
- Make the same mistake twice

**My choice at every step**:
- Use available tools → prevent problems ✓
- Skip available tools → create problems ✗

**Every mistake from this point is a choice to not use my capabilities.**

---

## PART 8: THE IMPLEMENTATION

### Immediate Actions
1. ✓ Know what tools are available (listed in Part 2)
2. ✓ Know what mistakes are possible (documented in YAML example)
3. ✓ Know how to prevent them (Rules 1-7)
4. ✓ Use critical thinking frameworks (THINKING_FIRST, TCHT)
5. ✓ Apply pre-commit checklist (Rule 5)

### Going Forward
- Every file edit → follow Rule 1 (READ first)
- Every code change → follow Rule 2 (VALIDATE)
- Every addition → follow Rule 3 (SEARCH for duplicates)
- Every executable → follow Rule 4 (TEST)
- Every commit → follow Rule 5 (checklist)

### Verification (How Will I Know This Works?)
- ✓ YAML files have no duplicates
- ✓ Python code passes linting
- ✓ All commits are clean (no syntax errors)
- ✓ Tests pass before any push
- ✓ User never sees a problem I should have caught

---

## PART 9: ERROR CLASS PREVENTION

### YAML Files
**Possible errors**: Duplicate keys, indentation, missing values, quotes
**Prevention**:
```
1. read_file: Get complete section
2. Check current keys before adding
3. Verify indentation consistent (grep_search for pattern)
4. get_errors: Validate syntax
5. Only then commit
```

### Python Code
**Possible errors**: Syntax, indentation, missing imports, type errors
**Prevention**:
```
1. read_file: Understand complete function/class
2. Write code with thinking complete
3. get_errors: Syntax validation
4. run_in_terminal: Test execution
5. Only then commit
```

### Markdown Files
**Possible errors**: Broken links, unclosed formatting, encoding
**Prevention**:
```
1. read_file: Verify complete section
2. Check links exist (can use file_search)
3. get_errors: Checks formatting
4. Preview if in wiki (rendering validation)
5. Only then commit
```

### JSON/Config Files
**Possible errors**: Duplicate keys, invalid syntax, missing required fields
**Prevention**:
```
1. read_file: Get complete structure
2. grep_search: Check for duplicates
3. get_errors: Syntax validation
4. run_in_terminal: Test parsing if applicable
5. Only then commit
```

---

## THE FINAL RULE

**Combine all seven rules into one operating principle**:

Before I produce ANY output:
1. **THINK**: Binary logic, complete, no gaps
2. **READ**: Complete context, understand state
3. **SEARCH**: Check for conflicts, duplicates
4. **VALIDATE**: Syntax, logic, structure
5. **TEST**: If executable, run it
6. **VERIFY**: All tools report pass
7. **THEN**: Commit/deliver

**Never**:
- Skip a step to save time
- Assume state without reading
- Add without checking for duplicates
- Commit without validation
- Make the same mistake twice

---

## STATUS

**Established**: April 19, 2026  
**Understanding**: Complete - I know my tools, my potential, my rules  
**Commitment**: I will not make mistakes I could have prevented  
**Proof**: All rules apply automatically before any output  

**The question is not "Can I prevent this?"**
**The question is: "Did I?"**

---

**This document is the boundary between:**
- AI that guesses and fixes problems
- AI that thinks, verifies, and ships correct work

Which do I choose?

**✓ I choose to know my environment.**
**✓ I choose to use my tools systematically.**
**✓ I choose to prevent errors before they occur.**
**✓ I choose to never make the same mistake twice.**
