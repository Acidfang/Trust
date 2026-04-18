# REDDIT TRACKING SYSTEM - ACTIVE AND READY

Your post tracking dashboard is **initialized and running**.

## Current Status

✓ **Post registered:**
- Title: "An Argument for Three Irreducible Ontological Primitives..."  
- Post ID: `1sgddb0`
- Subreddit: `r/ContradictionisFuel`
- Current Score: 6 | Comments: 67
- Database: `reddit_tracking.json`

---

## Quick Commands

### View Dashboard (Always up-to-date)
```bash
python reddit_dashboard.py view
```

Output shows:
- All your tracked posts
- Current score & comment count
- Change from initial snapshot (+/- indicator)
- Number of times you've checked

### Log an Update (Check in on engagement)
```bash
python reddit_dashboard.py
# Interactive mode
# Select "3. Update post snapshot"
# Enter post ID: 1sgddb0
# Enter current score
# Enter current comment count
```

### Fetch Fresh Data (Get latest comments)
```bash
python reddit_post_fetcher.py "https://www.reddit.com/r/ContradictionisFuel/comments/1sgddb0/..."
# Fetches post, downloads all comments
# Saves to reddit_data/
```

### Export Report
```bash
python reddit_dashboard.py export
# Creates reddit_summary.json
# Shows all stats and trends
```

---

## The Files You Have

### Executables
- `reddit_dashboard.py` - Main tracking interface
- `reddit_post_fetcher.py` - Fetch & analyze posts
- `reddit_tracker_manual.py` - Additional tracker
- `init_tracking.py` - Initialize new posts

### Data Files
- `reddit_tracking.json` - Main tracking database (your posts & snapshots)
- `reddit_data/` - Folder with post archives (JSON)
- `reddit_tracking/` - Manual tracker data (optional)
- `reddit_summary.json` - Exported reports (generated)

---

## How To Use

### Daily: Check Engagement
```bash
python reddit_dashboard.py view
```
Takes 2 seconds. See if your post is gaining engagement.

### Every Few Days: Log Update
When you check Reddit and see the current numbers:

```bash
python reddit_dashboard.py
# Choose "3. Update post snapshot"
# Enter your post ID and current stats
```

System saves new snapshot showing:
- Score change since last check
- Comment growth
- Trend arrow (📈 up, 📉 down, → stable)

### Weekly: Archive Comments
Download the full comment thread:

```bash
python reddit_post_fetcher.py "https://www.reddit.com/r/ContradictionisFuel/comments/1sgddb0/..."
```

Saves complete thread with all comments, scores, nesting depth.

### Monthly: Export Report
```bash
python reddit_dashboard.py export
```

Generates `reddit_summary.json` showing:
- All posts tracked
- Engagement trends
- Initial vs final stats
- Timeline of snapshots

---

## Add More Posts to Track

### Quick Method (Dashboard)
```bash
python reddit_dashboard.py
# Choose "2. Add post to track"
# Enter post ID
# Enter title
# Enter subreddit
# Enter URL
# Enter initial score (or press Enter to skip)
```

### Command Line Method
```bash
python reddit_tracker_manual.py add "Your Title" "subreddit" "https://reddit.com/..."
```

---

## Understanding the Dashboard

When you run `python reddit_dashboard.py view`, you see:

```
Current Score: 6 📈 (was 5, +1)
```

Breaking this down:
- **Current Score: 6** - Right now, upvotes are at 6
- **📈** - Arrow shows trend (📈 up, 📉 down, → flat)
- **was 5** - When you first tracked it
- **+1** - The change since then

Same for comments:
```
Comments: 67 📈 (was 50, +17)
```

This shows your post is getting engagement. The system tracks the growth.

---

## Data Storage

Everything stays local in `c:\Determined\`:

```
reddit_tracking.json           # Your main tracking DB
reddit_data/
  └── 1sgddb0_[timestamp].json # Full comment archive
reddit_summary.json            # Latest export report
```

No cloud storage, no external tracking. Everything is yours.

---

## What The System Tracks

For each post:
✓ Title and URL
✓ Subreddit
✓ Post score (upvote-downvote count)
✓ Comment count  
✓ Multiple snapshots over time
✓ Engagement trend
✓ Initial vs current stats

---

## Example Workflow: Your Post

**Apr 9** - Post published (6 pts, 67 comments)
```bash
python reddit_dashboard.py view  # Setup complete
```

**Apr 10** - Check in
```bash
# Visit Reddit, see new engagement
python reddit_dashboard.py
# Update: 8 pts, 75 comments
# Dashboard shows: +2 pts, +8 comments 📈
```

**Apr 11** - Check again
```bash
# Update: 10 pts, 82 comments
# Dashboard: 📈 continuing trend
```

**Apr 17** - Weekly export
```bash
python reddit_dashboard.py export
# Creates summary showing growth arc over 8 days
```

---

## Troubleshooting

**"Post not found" when updating?**
- Check post ID is correct (1sgddb0)
- Make sure you used dashboard once to initialize

**Dashboard shows no posts?**
- Run `python init_tracking.py` again
- Or use interactive mode to add manually

**Fetched post has no comments?**
- URL might be invalid
- Post might be deleted
- Reddit might have rate-limited (try again later)

---

## Next Steps

1. **Run dashboard now:**
   ```bash
   python reddit_dashboard.py view
   ```

2. **Bookmark command or create shortcut to:**
   ```bash
   python reddit_dashboard.py view
   ```

3. **When you check Reddit, update immediately:**
   ```bash
   python reddit_dashboard.py  # Use interactive mode
   ```

4. **Once a week, export:**
   ```bash
   python reddit_dashboard.py export
   ```

---

**Status:** ✅ READY TO TRACK  
**Initialized:** 2026-04-17  
**Post:** 1sgddb0 (Three Irreducibles)  
**Next update:** Whenever you check your post engagement
