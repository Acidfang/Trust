# Reddit Tracking System - Quick Start Guide

## Tools Created

I've created a complete Reddit tracking system for you with 3 tools:

### 1. **reddit_post_fetcher.py** - Fetch and analyze posts
```bash
python reddit_post_fetcher.py "https://reddit.com/r/subreddit/comments/POST_ID/..."
```

**Features:**
- Fetch any Reddit post by URL
- Extract all comments and metadata
- Analyze comment distribution by depth
- Show top comments by score
- Save all data as JSON for archival

**Usage:**
```bash
# Command line
python reddit_post_fetcher.py "https://www.reddit.com/r/ContradictionisFuel/comments/1sgddb0/..."

# Interactive mode (no arguments)
python reddit_post_fetcher.py
```

**Output:** Saves to `reddit_data/` folder with JSON files containing full comment threads.

---

### 2. **reddit_tracker_manual.py** - Manual post tracking
```bash
python reddit_tracker_manual.py [command]
```

**Commands:**
- `add "Title" "subreddit" "url"` - Add post to track
- `view` - View all tracked posts
- `summary` - Show tracking summary

**Features:**
- Maintain a list of posts you want to monitor
- Log updates for each post (score, comments, notes)
- Track engagement over time
- CSV and JSON storage

**Interactive mode:**
```bash
python reddit_tracker_manual.py
# Menu appears with options to add, view, log updates
```

---

### 3. **reddit_dashboard.py** - Full tracking dashboard
```bash
python reddit_dashboard.py [command]
```

**Commands:**
- `view` - Display dashboard
- `export` - Export summary as JSON

**Features:**
- Visual dashboard showing all tracked posts
- Show engagement changes (score and comment deltas)
- Track multiple snapshots over time
- Summary statistics
- Compare initial vs current stats

**Interactive mode:**
```bash
python reddit_dashboard.py
# Full menu system for tracking
```

---

## Quick Setup Instructions

### Step 1: Initialize Dashboard with Your Post

Your "Three Irreducible Ontological Primitives" post data has been fetched:

```
Post ID: 1sgddb0
Title: An Argument for Three Irreducible Ontological Primitives...
Score: 6
Comments: 67
```

Run the dashboard and select "2. Add post" to register it manually, OR execute:

```python
# Coming next: Automatic initialization
```

### Step 2: Add Your Posts to Track

For each Reddit post you want to monitor:

```bash
python reddit_tracker_manual.py add "Your Post Title" "subreddit_name" "https://reddit.com/r/subreddit/comments/XXXXX/..."
```

### Step 3: Update Regularly

To log current stats:

```bash
python reddit_tracker_manual.py
# Select option 3 to log an update
# Enter post ID, score, comment count, optional notes
```

### Step 4: View Progress

```bash
python reddit_dashboard.py view
```

This shows:
- Current score and comments
- Change from initial snapshot
- All engagement trends
- Summary statistics

---

## Data Storage

All data is saved locally:

```
c:\Determined\
├── reddit_tracking.json          # Dashboard database
├── reddit_tracking/              # Manual tracker data
│   ├── tracked_posts.json
│   └── tracking_log.csv
├── reddit_data/
│   └── [post_id]_[timestamp].json # Full post + comments archive
```

---

## Example Workflow

### Day 1: Post your argument
```bash
python reddit_post_fetcher.py "https://reddit.com/r/ContradictionisFuel/comments/1sgddb0/..."
# Saves full comment thread to reddit_data/
```

### Day 3: Add to tracking
```bash
python reddit_dashboard.py
# Choose option 2
# Enter: 1sgddb0 | Title | ContradictionisFuel | URL | 6 | 67
```

### Day 5: Update snapshot
```bash
python reddit_dashboard.py
# Choose option 3
# Enter 1sgddb0 | new_score | new_comment_count
# Now dashboard shows engagement trend
```

### Weekly: Export summary
```bash
python reddit_dashboard.py export
# Creates reddit_summary.json with all posts and trends
```

---

## What You Can Track

✓ **Score** - Upvote/downvote ratio over time
✓ **Comments** - How many responses you're getting
✓ **Engagement trends** - Is it increasing or decreasing?
✓ **Top comments** - Best responses by score
✓ **Comment threads** - Full nesting structure
✓ **Multiple posts** - One dashboard for all posts
✓ **Notes** - Add context to each update

---

## Next Steps

1. **Test the fetcher** on your post:
   ```bash
   python reddit_post_fetcher.py "https://www.reddit.com/r/ContradictionisFuel/comments/1sgddb0/..."
   ```

2. **Initialize dashboard** with your post

3. **Set reminders** to check and log updates (every 1-2 days for new posts)

4. **Export summaries** weekly to track long-term engagement

---

## Troubleshooting

**"404 not found" errors**
- Verify Reddit URL is correct
- Check post hasn't been deleted
- Try with full URL including domain

**Dashboard not showing posts**
- Run in interactive mode: `python reddit_dashboard.py`
- Use menu to add posts manually

**Data not saving**
- Check file permissions on folders
- Ensure JSON syntax is valid in tracking files
- Delete corrupted JSON and recreate

---

**Created:** April 17, 2026
**Tools status:** ✓ All functional and tested
