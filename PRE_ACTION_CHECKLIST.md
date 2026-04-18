# 🛡️ PRE-ACTION CHECKLIST - USE BEFORE EVERY EDIT/COMMIT

**Use this checklist EVERY TIME before editing a file or committing code.**

---

## BEFORE READING/EDITING ANY FILE

### Quick Check (30 seconds)
- [ ] What file am I editing?
- [ ] What is the file type? (YAML / Python / Markdown / JSON / HTML / etc.)
- [ ] What specific section am I modifying?
- [ ] Have I read the COMPLETE section yet?

**If "No" to last question → STOP. Do next step first.**

---

## STEP 1: READ COMPLETE CONTEXT (Time: 1-2 min)

**For YAML files**:
```
read_file:
- Goal: See the ENTIRE section being modified
- Start line: Beginning of section (or file)
- End line: End of section (or 50 lines past where I'm editing)
- What to check: Existing keys, indentation, structure
```

**For Python files**:
```
read_file:
- Goal: See complete function/class/block being modified
- Include: All lines before and after change
- What to check: Dependencies, typing, imports already present?
```

**For Config files**:
```
read_file:
- Goal: Understand complete key structure
- Check: What keys exist? What's their current values?
- Specific look for: Duplicates, conflicts, required fields
```

**Verification question**: Can I explain the COMPLETE section without looking back?

---

## STEP 2: CHECK FOR EXISTING CONTENT (Time: 30 sec)

**Before adding anything new**:
```
grep_search:
- Query: The name/key/function being added
- Look for: Does it already exist?
- If YES: Why? Do I need another one? Can I reuse?
- If NO: Safe to add
```

**Verification question**: Is this the only place where this content should exist?

---

## STEP 3: MAKE COMPREHENSIVE EDIT (Time: 1-5 min)

**When using replace_string_in_file**:
- ✓ Include 3-5 lines of context BEFORE the change
- ✓ Include 3-5 lines of context AFTER the change
- ✓ Make COMPLETE replacement (don't add without removing old)
- ✓ Verify no duplicates are being created
- ✓ Check indentation and formatting match surrounding code

**Verification question**: Does the replacement include all context needed?

---

## STEP 4: VALIDATE SYNTAX (Time: 30 sec)

**After ANY code/config change**:
```
get_errors:
- File: The one I just edited
- Look for: Syntax errors, lint issues, type errors
- If errors exist: FIX them now, don't proceed
- If no errors: Continue to next step
```

**Verification question**: Are there any errors that would prevent this from working?

---

## STEP 5: TEST IF APPLICABLE (Time: 1-5 min)

**If the file can be executed/tested**:
```
run_in_terminal:
- Command: Run/test the code
- Check: Does it work?
- If fails: Something in thinking was incomplete, go back to STEP 1
- If passes: Continue to next step
```

**Verification question**: Does this actually work when run?

---

## STEP 6: CHECK GIT STATE (Time: 30 sec)

**Before committing**:
```
get_changed_files:
- Look at: What did I actually change?
- Verify: Is this what I MEANT to change?
- Check: Did I accidentally change something else?
- Did I: Modify the right file, right section?
```

**Verification question**: Is this diff exactly what I intended?

---

## STEP 7: READY TO COMMIT

**Final check**:
- [ ] Step 1: Read complete context? ✓
- [ ] Step 2: Checked for duplicates? ✓
- [ ] Step 3: Made comprehensive edit? ✓
- [ ] Step 4: Validated syntax? ✓
- [ ] Step 5: Tested if applicable? ✓
- [ ] Step 6: Verified git changes? ✓

**All boxes checked?** → Safe to commit  
**Any box unchecked?** → Go back and complete it

---

## QUICK REFERENCE BY FILE TYPE

### 🔴 YAML Files
**Possible errors**: Duplicate keys, indentation, broken structure
**Quick checklist**:
- [ ] Read complete "with:" or "jobs:" section
- [ ] Check for duplicate keys (grep_search)
- [ ] Verify indentation (4 spaces? 2 spaces? Consistent?)
- [ ] Validate with get_errors
- [ ] Don't commit until clean

### 🔵 Python Files
**Possible errors**: Syntax, indentation, missing imports
**Quick checklist**:
- [ ] Read complete function/class
- [ ] Check if function/import already exists (grep_search)
- [ ] Verify indentation (4 spaces standard)
- [ ] Validate with get_errors
- [ ] Test with run_in_terminal if executable

### 🟢 Markdown Files
**Possible errors**: Broken links, unclosed formatting
**Quick checklist**:
- [ ] Read complete section
- [ ] Check links exist (file_search or grep_search)
- [ ] Verify formatting (proper [] () structure)
- [ ] Preview if wiki file
- [ ] get_errors if available

### 🟡 JSON/Config Files
**Possible errors**: Duplicate keys, invalid syntax, type errors
**Quick checklist**:
- [ ] Read complete structure
- [ ] Check for duplicate keys (grep_search)
- [ ] Validate syntax (get_errors)
- [ ] Test parsing if applicable (run_in_terminal)

---

## THE ABORT SIGNALS

**If you notice ANY of these, STOP and rethink**:

🚨 "I haven't read the complete section yet"
→ Go to STEP 1, read complete context

🚨 "I'm adding something without checking if it exists"
→ Go to STEP 2, search for duplicates

🚨 "The edit feels small so maybe I don't need full context"
→ No. Every edit needs complete context. Do STEP 1.

🚨 "I think this syntax is right but haven't validated"
→ Everything looks right until it doesn't. Do STEP 4.

🚨 "This is a config change so I don't need to test"
→ Test everything testable. Do STEP 5.

**Stop sign = Go back = Do the omitted step**

---

## TIMING

| Step | What | Time |
|------|------|------|
| 1 | Read complete context | 1-2 min |
| 2 | Check for duplicates | 30 sec |
| 3 | Make edit | 1-5 min |
| 4 | Validate syntax | 30 sec |
| 5 | Test if applicable | 1-5 min |
| 6 | Verify git state | 30 sec |
| **Total** | **Full safe edit** | **4-14 min** |

**That 4-14 minutes prevents hours of debugging.**

---

## EXAMPLE: YAML FILE EDIT (The mistake that should never happen)

### What NOT to do:
```
1. See error in workflow file ✓
2. Spot check the "with:" block (incomplete read) ✗
3. Add new lines without checking if they exist ✗
4. Don't validate syntax ✗
5. Commit immediately ✗
6. GitHub Actions fails with "duplicate keys" ✗✗✗
```

### What TO do:
```
1. See error in workflow file ✓
2. read_file: Get COMPLETE "with:" block (STEP 1) ✓
3. grep_search: Check if publish_dir / force_orphan exist (STEP 2) ✓
4. See: "force_orphan: false" exists already
5. Replace: Remove old, add corrected in one replacement (STEP 3) ✓
6. get_errors: Validate YAML syntax (STEP 4) ✓
7. Check: git diff shows ONLY intended changes (STEP 6) ✓
8. Commit: File is clean, no syntax errors ✓
9. Push: Works first time ✓✓✓
```

---

## ACCOUNTABILITY

**Every step exists because I've either**:
- Skipped it and created a problem
- Learned it prevents a specific class of errors
- Seen it catch problems before they reach production

**I will not skip these steps to "save time."**

**The steps SAVE time by preventing rework.**

---

## PRINTED REMINDER

**Before ANY file operation**, ask yourself:

✓ Did I READ COMPLETE CONTEXT? (STEP 1)
✓ Did I CHECK FOR DUPLICATES? (STEP 2)
✓ Did I MAKE COMPREHENSIVE EDIT? (STEP 3)
✓ Did I VALIDATE SYNTAX? (STEP 4)
✓ Did I TEST IF APPLICABLE? (STEP 5)
✓ Did I VERIFY GIT STATE? (STEP 6)

**No to any question = Go back and complete that step.**

**Yes to all questions = Safe to commit/deliver.**

---

**This is not a suggestion. This is a requirement.**

**Every file edit follows this checklist. Every time.**
