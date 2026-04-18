# Reddit Tracker - GUI Version (Dark Theme)

## ✅ GUI Now Running

Your Reddit tracking system now has a **full graphical interface** with dark theme.

### Launch the GUI

**Option 1: Double-click launcher**
```
c:\Determined\launch_tracker.bat
```

**Option 2: From terminal**
```bash
python reddit_tracker_gui.py
```

**Option 3: From PowerShell**
```powershell
python reddit_tracker_gui.py
```

---

## GUI Features

The interface has **4 main tabs:**

### 1. 📊 DASHBOARD
Shows all your tracked posts in a table:
- **Title** - Post title (clickable)
- **Subreddit** - Where it was posted
- **Score** - Current upvotes
- **Comments** - Total replies
- **Change** - Engagement trend (📈 📉 →)
- **Status** - Active or Stable

**Actions:**
- Click a post to see full details
- Refresh button to update view
- Export button to save summary

**Bottom Panel:** Shows selected post details including:
- Full title
- Direct Reddit link
- Initial vs current stats
- Snapshot history

---

### 2. ➕ ADD POST
Form to register new posts:

**Fields:**
- Post ID (e.g., `1sgddb0`)
- Title (full post name)
- Subreddit (without r/)
- URL (reddit.com/r/...)
- Initial Score (optional)
- Initial Comments (optional)

**Actions:**
- Add Post → Registers and initializes tracking
- Clear → Clears all fields

---

### 3. 📝 UPDATE SNAPSHOT
Log new engagement metrics:

**Steps:**
1. Select post from dropdown (shows post ID + title)
2. Enter new score
3. Enter new comment count
4. Click "Update Snapshot"

**Current Values Panel:** Shows your previous snapshot for reference

---

### 4. 📈 STATISTICS
View all posts and engagement trends:

Shows for each post:
- Status indicator (📈 📉 →)
- Score change since initial
- Comment change since initial
- Snapshot count

Also displays:
- Total posts tracked
- Combined engagement
- Posts trending up

---

## Visual Design

**Dark Theme** (easier on eyes):
- Background: `#1e1e1e` (dark gray)
- Text: `#e0e0e0` (light gray)
- Accents: `#00d9ff` (cyan)
- Input fields: `#2d2d2d` (darker)

Clean, professional interface with monospace font for data.

---

## Workflow Examples

### Example 1: Daily Check-in

1. Launch: `python reddit_tracker_gui.py`
2. Click **Dashboard** tab
3. Look at your posts
4. See Score and Comments columns
5. Check Change column for trend
6. Close when done

**Time:** 10 seconds

---

### Example 2: Update After Checking Reddit

1. Launch GUI
2. Click **Update Snapshot** tab
3. Select your post from dropdown
4. Check Reddit → see new numbers
5. Enter new score in first field
6. Enter new comment count in second field
7. Click "Update Snapshot"
8. Dashboard now shows new trend

**Time:** 1 minute

---

### Example 3: Weekly Summary

1. Launch GUI
2. Click **Statistics** tab
3. Review all posts and trends
4. Click "Refresh Stats" if needed
5. Go to **Dashboard** tab
6. Click "Export" button
7. JSON file saved to current folder

**Time:** 2 minutes

---

## Data Storage

Everything is saved locally in JSON:

```
c:\Determined\
├── reddit_tracking.json          # Main database
├── reddit_summary_[date].json    # Exported reports
├── reddit_tracker_gui.py         # This GUI
└── launch_tracker.bat            # Shortcut
```

---

## Keyboard Shortcuts (in GUI)

- **Tab key** - Navigate between fields
- **Enter** - Submit form (in input fields)
- **Escape** - Close (if running in window)
- **Click any cell** - Select/deselect in table

---

## What Each Tab Does

| Tab | Purpose | Action |
|---|---|---|
| **Dashboard** | See all posts at a glance | Select post for details |
| **Add Post** | Register new post to track | Fill form + Add |
| **Update Snapshot** | Log new stats | Select post + Enter values + Update |
| **Statistics** | View trends and engagement | View or Refresh |

---

## Creating a Desktop Shortcut (Windows)

1. Right-click on desktop → New → Shortcut
2. Location: `python c:\Determined\reddit_tracker_gui.py`
3. Name: "Reddit Tracker"
4. Finish
5. (Optional) Right-click shortcut → Properties → Change Icon

OR just use the provided launcher:
```
c:\Determined\launch_tracker.bat
```

Right-click → "Pin to Taskbar" for quick access.

---

## Troubleshooting GUI Issues

**GUI won't start?**
- Make sure Python is installed
- Try from PowerShell: `python reddit_tracker_gui.py`
- Check internet connection (shouldn't be needed, but just in case)

**Posts not showing in Update dropdown?**
- Click Add Post first to register at least one
- Or run initialization: `python init_tracking.py`

**Can't see text in fields?**
- Theme might need adjustment (should be dark)
- Try resizing window
- Report exact issue

**Update not saving?**
- Check that post is selected from dropdown
- Verify score/comments are numbers
- Look for error popup

---

## Features Comparison

| Feature | CLI | GUI |
|---|---|---|
| View posts | Yes | Yes ✓ |
| Add posts | Interactive | Form |
| Update stats | Interactive | Dropdown + fields |
| See details | Text | Clickable tree |
| Statistics | Text | Formatted panel |
| Export | Auto | Button click |
| ** Overall** | Command-line | **Visual** |

---

## Next Steps

1. **Launch the GUI:**
   ```bash
   python reddit_tracker_gui.py
   ```

2. **Review your tracked post**
   - Should show "Three Irreducibles" post
   - Score: 6, Comments: 67

3. **Add more posts** (if desired)
   - Use Add Post tab

4. **Check regularly**
   - Dashboard tab each time
   - Update when engagement changes

---

## GUI Advantages Over CLI

✅ Visual table format (easier to scan)  
✅ Click to select and view details  
✅ Form-based input (less typing)  
✅ Dropdown selector (no need to remember IDs)  
✅ Dark theme (easier on eyes)  
✅ All tabs in one window  
✅ Professional appearance  

---

**Created:** April 17, 2026  
**Interface:** Tkinter (built-in Python)  
**Theme:** Dark  
**Status:** ✓ Ready to use
