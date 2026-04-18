# REDDIT TRACKER - GUI COMPLETE SETUP

## 🎯 Status
✅ **GUI is now running** in your terminal (TID: 06bce5bc-9889-4fc5-8a22-8ff70103d329)  
✅ **Dark theme interface** with 4 main tabs  
✅ **Your post already registered** (Three Irreducibles, 1sgddb0)  
✅ **Ready to use immediately**

---

## 🚀 Quick Start

### Launch GUI (Anytime)

**Method 1 - Double-click launcher:**
```
c:\Determined\launch_tracker.bat
```

**Method 2 - From command line:**
```bash
cd c:\Determined
python reddit_tracker_gui.py
```

**Method 3 - Create desktop shortcut (one-time):**
```bash
python create_desktop_shortcut.py
```
Then click "Reddit Tracker" on desktop.

---

## 📋 What You Have

### Files
```
c:\Determined\
├── reddit_tracker_gui.py           ← THE GUI (run this)
├── launch_tracker.bat              ← Windows launcher
├── create_desktop_shortcut.py      ← Make desktop shortcut
├── reddit_tracking.json            ← Your data
├── GUI_GUIDE.md                    ← Full documentation
├── TRACKING_ACTIVE.md              ← Command-line guide
└── reddit_tracking_data/           ← Post archives
```

### Database
```
reddit_tracking.json:
{
  "posts": [
    {
      "post_id": "1sgddb0",
      "title": "An Argument for Three Irreducible Ontological Primitives...",
      "snapshots": [
        {"timestamp": "2026-04-09...", "score": 6, "comments": 67},
        ...
      ]
    }
  ]
}
```

---

## 🎨 GUI Interface Overview

### Tab 1: Dashboard 
**Main view of all your posts**

```
┌─────────────────────────────────────────────────────────────┐
│ # │ Title                │ Sub  │ Score │ Cmts │ Change │ St│
├─────────────────────────────────────────────────────────────┤
│ 1 │ Three Irreducibles.. │ Con  │   6   │  67  │  →  0  │ St│
└─────────────────────────────────────────────────────────────┘
  [Refresh] [Export]

┌─ POST DETAILS ────────────────────────────────────┐
│ Three Irreducibles...                             │
│ r/ContradictionisFuel                             │
│ URL: https://reddit.com/r/ContradictionisFuel... │
│ Initial Score: 6  → Current Score: 6 (Change: 0) │
│ Initial Cmts: 67  → Current Cmts: 67 (Change: 0) │
│ Snapshots: 2                                      │
└───────────────────────────────────────────────────┘
```

**Actions:**
- Click any post to see details below
- Refresh button updates display
- Export button saves JSON summary

---

### Tab 2: Add Post
**Register new posts to track**

```
┌─ ADD NEW POST ─────────────────────────────────────┐
│ Post ID:          [________________]               │
│ Title:            [________________]               │
│ Subreddit:        [________________]               │
│ URL:              [________________]               │
│ Initial Score:    [________________]               │
│ Initial Comments: [________________]               │
│                                                    │
│            [Add Post]  [Clear]                     │
└────────────────────────────────────────────────────┘
```

**Usage:**
1. Enter post details
2. Click "Add Post"
3. Returns to Dashboard showing new post

---

### Tab 3: Update Snapshot
**Log new engagement metrics**

```
┌─ SELECT POST ──────────────────────────────────────┐
│ Post: [Three Irreducibles... ▼]                   │
└────────────────────────────────────────────────────┘

┌─ NEW VALUES ─────────────────────────────────────┐
│ New Score:         [6     ]                      │
│ New Comment Count: [67    ]                      │
│                                                  │
│ CURRENT VALUES:                                 │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━       │
│ Score: 6                                        │
│ Comments: 67                                    │
│ Last Updated: 2026-04-17T13:35:47              │
│ Total Snapshots: 2                              │
│                                                  │
│            [Update Snapshot]                     │
└──────────────────────────────────────────────────┘
```

**Steps:**
1. Select post from dropdown
2. Sees previous snapshot values
3. Enter new numbers
4. Click "Update Snapshot"
5. New snapshot saved automatically

---

### Tab 4: Statistics
**View engagement trends and summaries**

```
┌─ ENGAGEMENT STATISTICS ────────────────────────────┐
│                                                    │
│ 📌 Three Irreducibles...                           │
│    Status: → STABLE                               │
│    Score: 6 → 6 (+0)                              │
│    Comments: 67 → 67 (+0)                         │
│    Snapshots: 2                                   │
│                                                    │
│ ════════════════════════════════════════════════   │
│ SUMMARY                                           │
│ ════════════════════════════════════════════════   │
│ Total Posts Tracked: 1                            │
│ Combined Score: 6                                 │
│ Combined Comments: 67                             │
│ Posts Trending Up: 0                              │
│                                                    │
│            [Refresh Stats]                        │
└────────────────────────────────────────────────────┘
```

---

## 🎯 Daily Workflow

### Morning: Quick Status Check
```bash
python reddit_tracker_gui.py
# → Click Dashboard
# → Glance at Change column
# → Close
# Time: 10 seconds
```

### Afternoon: Log New Engagement
```bash
python reddit_tracker_gui.py
# → Click Update Snapshot
# → Select post
# → Check Reddit for current numbers
# → Enter score and comments
# → Click Update Snapshot
# → Close
# Time: 1-2 minutes
```

### Weekly: Review Trends
```bash
python reddit_tracker_gui.py
# → Click Statistics
# → Review all posts
# → Click Export
# → Save JSON report
# Time: 5 minutes
```

---

## 📊 How to Track Engagement

### Initial Setup (Already Done)
✓ Post registered with post ID, title, subreddit, URL
✓ First snapshot recorded (when post published)

### Track Updates
1. **Visit your Reddit post**
2. **Note the current:**
   - Upvote/downvote score
   - Total comments
3. **Open GUI → Update Snapshot tab**
4. **Select your post**
5. **Enter new numbers**
6. **Click Update**

### Monitor Trends
- Dashboard shows: Current vs Initial (with change indicator)
- 📈 = Gaining engagement
- 📉 = Losing engagement  
- → = Stable

---

## 🔄 Data Flow

```
┌──────────────┐
│ Your Reddit  │
│    Post      │ ← Check manually
└──────────────┘
        ↓
┌──────────────────────────┐
│  You enter current stats  │ ← GUI: Update Snapshot tab
│   (score, comments)      │
└──────────────────────────┘
        ↓
┌──────────────────────────┐
│  GUI saves to            │
│  reddit_tracking.json    │
└──────────────────────────┘
        ↓
┌──────────────────────────┐
│  Dashboard shows trend   │ ← GUI: Dashboard tab
│  (📈 📉 → with delta)    │
└──────────────────────────┘
```

---

## 💾 Saving & Exporting

### Automatic Saves
- Every update is saved to `reddit_tracking.json`
- Happens immediately when you click buttons
- No manual save required

### Manual Export
1. Dashboard tab
2. Click "Export" button
3. Creates `reddit_summary_[date].json`
4. Contains all posts and stats

### Export File Format
```json
{
  "username": "Agitated_Age_2785",
  "exported_at": "2026-04-17T14:00:00",
  "posts": [
    {
      "title": "Three Irreducibles...",
      "subreddit": "ContradictionisFuel",
      "url": "https://reddit.com/...",
      "current_score": 6,
      "current_comments": 67,
      "initial_score": 6,
      "initial_comments": 67,
      "score_change": 0,
      "comment_change": 0,
      "snapshots_taken": 2
    }
  ]
}
```

---

## 🎨 Customization (Advanced)

### Change Theme Colors
Edit these lines in `reddit_tracker_gui.py`:

```python
# Dark theme colors (currently):
background='#1e1e1e'    # Dark gray
foreground='#e0e0e0'    # Light gray
accent='#00d9ff'        # Cyan

# Change to your preference and restart
```

### Resize Window
On startup, adjust window size:
```python
self.root.geometry("1000x700")  # Width x Height
# Change to fit your screen
```

---

## ⚠️ Troubleshooting

### GUI Won't Open
```bash
# Check Python installation
python --version

# Try explicit path
"C:\Users\[username]\AppData\Local\Python\pythoncore-3.14-64\python.exe" reddit_tracker_gui.py
```

### Posts Disappeared
```bash
# Check if reddit_tracking.json exists
# If corrupted, restore from backup or:
python init_tracking.py
```

### Update Not Saving
- Verify post is selected from dropdown
- Check that score/comments are numbers (not text)
- Look for error popup message
- Check file permissions on folder

### GUI Appears Blank
- Resize window (drag corner)
- Restart GUI
- Check screen resolution

---

## 📝 Tips & Tricks

### Efficient Tracking
- Update immediately after checking Reddit (while you remember numbers)
- Use Dashboard view most often (fastest)
- Export weekly for historical record

### Better Organization
- Use short, descriptive post IDs
- Include subreddit in title for clarity
- Add notes in post title (e.g., "Feature Request - UI Design")

### Batch Updates
- If several posts to update, do all at once
- Select each post → update → next
- Takes few minutes per batch

---

## 🔗 Quick Links to All Tools

### GUI System (What You're Using Now)
- **Launch:** `python reddit_tracker_gui.py`
- **Launcher:** `launch_tracker.bat`
- **Guide:** `GUI_GUIDE.md`

### Command-Line System (Alternative)
- **Dashboard:** `python reddit_dashboard.py view`
- **Interactive:** `python reddit_dashboard.py`
- **Guide:** `TRACKING_ACTIVE.md`

### Web Scraper (Get Comments)
- **Fetch post:** `python reddit_post_fetcher.py "URL"`
- **Guide:** `REDDIT_TRACKING_GUIDE.md`

---

## 📞 Support

For issues or questions:

1. **Check the relevant guide** first
2. **Read error messages** carefully
3. **Try restarting GUI**
4. **Check data file** (reddit_tracking.json)

---

## ✅ Next Steps

1. **Close this terminal** (GUI is minimized, running in background)
2. **Open GUI anytime with:**
   ```bash
   python reddit_tracker_gui.py
   ```
3. **Let it run in background** while you work
4. **Use Dashboard tab** to monitor engagement

---

**Created:** April 17, 2026  
**Status:** ✅ Ready to use  
**Interface:** Tkinter (Python GUI)  
**Theme:** Dark  
**Posts Tracked:** 1 (Three Irreducibles)  
**Your Data:** Safe, local, always accessible
