#!/usr/bin/env python3
"""
Reddit Post Tracker - GUI Version
Tkinter-based graphical interface for tracking Reddit posts with comment fetching
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import threading
import requests
from datetime import datetime, timedelta
from pathlib import Path
import sys
import io
import sqlite3
import time

# Fix output encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class RedditTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Reddit Post Tracker")
        self.root.geometry("1200x750")
        self.root.configure(bg='#1e1e1e')
        
        self.tracking_file = "reddit_tracking.json"
        self.cache_db = "reddit_cache.db"
        self.comments_data = {}  # Cache for comments
        self.current_user_posts = {}  # Cache for user posts
        self.init_cache_db()
        self.load_data()
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#1e1e1e')
        style.configure('TLabel', background='#1e1e1e', foreground='#e0e0e0')
        style.configure('TButton', background='#2d2d2d', foreground='#e0e0e0')
        style.configure('Title.TLabel', background='#1e1e1e', foreground='#00d9ff', font=('Consolas', 14, 'bold'))
        style.configure('Header.TLabel', background='#1e1e1e', foreground='#00d9ff', font=('Consolas', 10, 'bold'))
        style.configure('Treeview', background='#2d2d2d', foreground='#e0e0e0', fieldbackground='#2d2d2d')
        
        self.setup_ui()
    
    def init_cache_db(self):
        """Initialize SQLite cache database with UFM (Universal Field Model) structure
        
        UFM Principle: All phenomena are expressions of a unified constraint under variations.
        
        Θ (constraint) = Why people conflict at the fundamental level
        ∇Θ (variation) = Different manifestations (by evidence, by claim, by certainty, etc)
        Δ (expression) = Actual instances of conflict/agreement
        
        Store the constraint once, variations as patterns, expressions as instances.
        """
        conn = sqlite3.connect(self.cache_db)
        c = conn.cursor()
        
        # Raw comments cache table (fetched from Reddit API)
        c.execute('''CREATE TABLE IF NOT EXISTS comment_cache
                     (post_id TEXT PRIMARY KEY,
                      comments_json TEXT,
                      fetched_at REAL,
                      expires_at REAL)''')
        
        # UFM Constraint definition
        # The unified field: Why people disagree/agree
        c.execute('''CREATE TABLE IF NOT EXISTS ufm_constraint
                     (constraint_id TEXT PRIMARY KEY,
                      name TEXT,
                      description TEXT)''')
        
        # UFM Variations - different ways the constraint manifests
        # E.g., "factual_disagreement", "opinion_disagreement", "evidence_challenge"
        c.execute('''CREATE TABLE IF NOT EXISTS ufm_variations
                     (variation_id TEXT PRIMARY KEY,
                      constraint_id TEXT,
                      name TEXT,
                      description TEXT,
                      frequency INTEGER)''')
        
        # UFM Expressions - actual instances of conflict/agreement
        c.execute('''CREATE TABLE IF NOT EXISTS ufm_expressions
                     (post_id TEXT,
                      expression_id TEXT,
                      variation_id TEXT,
                      expression_type TEXT,
                      reason TEXT,
                      PRIMARY KEY (post_id, expression_id))''')
        
        conn.commit()
        conn.close()
    
    def _get_cached_comments(self, post_id, max_age_hours=6):
        """Get comments from cache if fresh, returns None if expired or missing"""
        try:
            conn = sqlite3.connect(self.cache_db)
            c = conn.cursor()
            c.execute('SELECT comments_json, fetched_at FROM comment_cache WHERE post_id = ?', (post_id,))
            result = c.fetchone()
            conn.close()
            
            if result:
                comments_json, fetched_at = result
                age_hours = (time.time() - fetched_at) / 3600
                if age_hours < max_age_hours:
                    return json.loads(comments_json), age_hours
                else:
                    return None  # Cache expired
            return None  # Not in cache
        except Exception as e:
            return None
    
    def _save_cached_comments(self, post_id, comments_data):
        """Save comments to cache"""
        try:
            conn = sqlite3.connect(self.cache_db)
            c = conn.cursor()
            now = time.time()
            expires = now + (6 * 3600)  # 6 hour expiry
            
            c.execute('INSERT OR REPLACE INTO comment_cache VALUES (?, ?, ?, ?)',
                     (post_id, json.dumps(comments_data), now, expires))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Cache save error: {e}")
    
    def _clear_cache_for_post(self, post_id):
        """Clear cache for a specific post"""
        try:
            conn = sqlite3.connect(self.cache_db)
            c = conn.cursor()
            c.execute('DELETE FROM comment_cache WHERE post_id = ?', (post_id,))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Cache clear error: {e}")
    
    def _get_cached_analysis(self, post_id):
        """Retrieve analysis from UFM singularity storage
        
        Reconstruct expressions from variation references (reverse the collapse)
        """
        try:
            conn = sqlite3.connect(self.cache_db)
            c = conn.cursor()
            
            # Get all expressions for this post
            c.execute('''SELECT expression_id, variation_id, expression_type, reason 
                        FROM ufm_expressions WHERE post_id = ?''', (post_id,))
            expressions = c.fetchall()
            
            if not expressions:
                conn.close()
                return None
            
            # Reconstruct full lists from compressed form
            conflicts = []
            agreements = []
            
            for expr_id, variation_id, expr_type, reason in expressions:
                if expr_type == 'conflict':
                    conflicts.append({'reason': reason, 'variation_id': variation_id})
                elif expr_type == 'agreement':
                    agreements.append({'reason': reason, 'variation_id': variation_id})
            
            conn.close()
            
            return {
                'conflicts': conflicts,
                'agreements': agreements,
                'from_singularity_storage': True
            }, 0  # age_hours = 0 (always fresh from singularity)
            
        except Exception as e:
            print(f"Cache read error: {e}")
            return None
    
    def _save_cached_analysis(self, post_id, analysis_data):
        """Save analysis using UFM singularity storage
        
        Collapse all expressions (conflicts/agreements) toward the unified constraint.
        Store only: constraint → variations → reference counts (not full data)
        """
        try:
            conn = sqlite3.connect(self.cache_db)
            c = conn.cursor()
            now = time.time()
            
            # Ensure constraint exists (singularity point)
            constraint_id = "post_response_mechanism"
            c.execute('INSERT OR IGNORE INTO ufm_constraint VALUES (?, ?, ?)',
                     (constraint_id,
                      "Why People Respond to Posts",
                      "Unified field: all response types are variations on this constraint"))
            
            conflicts = analysis_data.get('conflicts', [])
            agreements = analysis_data.get('agreements', [])
            
            # Extract variations from reasons (collapse to common types)
            variation_map = {}  # reason → variation_id
            
            for conflict in conflicts:
                reason = conflict.get('reason', 'unknown_conflict')
                # Map reason to variation type (variation is the singularity point for this type)
                variation_key = f"conflict|{reason}"
                if variation_key not in variation_map:
                    variation_id = f"Θ_{len(variation_map)+1}"
                    variation_map[variation_key] = variation_id
                    # Store variation definition
                    c.execute('INSERT OR REPLACE INTO ufm_variations VALUES (?, ?, ?, ?, ?)',
                             (variation_id, constraint_id, reason, 'conflict', 0))
            
            for agreement in agreements:
                reason = agreement.get('reason', 'unknown_agreement')
                variation_key = f"agreement|{reason}"
                if variation_key not in variation_map:
                    variation_id = f"Θ_{len(variation_map)+1}"
                    variation_map[variation_key] = variation_id
                    c.execute('INSERT OR REPLACE INTO ufm_variations VALUES (?, ?, ?, ?, ?)',
                             (variation_id, constraint_id, reason, 'agreement', 0))
            
            # Store expressions as references to variations
            # Instead of storing full conflict data, just: (post_id, variation_id, expression_type, reason)
            expr_count = 0
            for conflict in conflicts:
                reason = conflict['reason']
                variation_key = f"conflict|{reason}"
                variation_id = variation_map.get(variation_key)
                if variation_id:
                    c.execute('INSERT INTO ufm_expressions VALUES (?, ?, ?, ?, ?)',
                             (post_id, f"{variation_id}_{expr_count}", variation_id, 'conflict', reason))
                    expr_count += 1
            
            for agreement in agreements:
                reason = agreement['reason']
                variation_key = f"agreement|{reason}"
                variation_id = variation_map.get(variation_key)
                if variation_id:
                    c.execute('INSERT INTO ufm_expressions VALUES (?, ?, ?, ?, ?)',
                             (post_id, f"{variation_id}_{expr_count}", variation_id, 'agreement', reason))
                    expr_count += 1
            
            conn.commit()
            conn.close()
            
            print(f"UFM Singularity: Post {post_id} -> {len(variation_map)} variations, {expr_count} expressions")
            
        except Exception as e:
            print(f"Analysis cache save error: {e}")
    
        except Exception as e:
            print(f"Analysis cache save error: {e}")
    
    def _display_cached_conflict_analysis(self, post_id, cached_analysis_results):
        """Display analysis reconstructed from UFM singularity storage"""
        if not cached_analysis_results:
            self.root.after(0, lambda: self.actions_status.config(
                text="Analysis not in singularity storage - forcing fresh analysis"))
            # Force re-analysis
            self.root.after(0, lambda: self._dashboard_analyze_conflicts_thread(post_id, force_refresh=True))
            return
        
        conflicts = cached_analysis_results.get('conflicts', [])
        agreements = cached_analysis_results.get('agreements', [])
        
        popup = tk.Toplevel(self.root)
        popup.title(f"Singularity Storage Analysis - {post_id}")
        popup.geometry("900x700")
        popup.configure(bg='#1e1e1e')
        
        text = scrolledtext.ScrolledText(popup, bg='#2d2d2d', fg='#e0e0e0', font=('Consolas', 9))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text.insert(tk.END, f"═══ UFM SINGULARITY STORAGE ═══\n")
        text.insert(tk.END, f"Post ID: {post_id}\n")
        text.insert(tk.END, f"Θ (Constraint): Post Response Mechanism\n")
        text.insert(tk.END, f"∇Θ (Variations Observed): {len(set(c['variation_id'] for c in conflicts))} conflict, {len(set(a['variation_id'] for a in agreements))} agreement\n")
        text.insert(tk.END, f"Δ (Expressions): {len(conflicts)} conflicts, {len(agreements)} agreements\n\n")
        
        if conflicts:
            text.insert(tk.END, "CONFLICT VARIATIONS:\n")
            conflict_types = {}
            for c in conflicts:
                reason = c['reason']
                conflict_types[reason] = conflict_types.get(reason, 0) + 1
            
            for reason, count in sorted(conflict_types.items(), key=lambda x: -x[1]):
                text.insert(tk.END, f"  • {reason} (×{count})\n")
        
        if agreements:
            text.insert(tk.END, "\nAGREEMENT VARIATIONS:\n")
            agreement_types = {}
            for a in agreements:
                reason = a['reason']
                agreement_types[reason] = agreement_types.get(reason, 0) + 1
            
            for reason, count in sorted(agreement_types.items(), key=lambda x: -x[1]):
                text.insert(tk.END, f"  • {reason} (×{count})\n")
        
        text.insert(tk.END, "\n[Variation instances compressed in singularity storage]\n")
        text.config(state=tk.DISABLED)
        
        self.actions_status.config(text=f"✓ Loaded from singularity storage ({len(conflicts)} conflicts, {len(agreements)} agreements)")
    
    def load_data(self):
        """Load tracking data"""
        if os.path.exists(self.tracking_file):
            with open(self.tracking_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {'posts': [], 'username': 'Agitated_Age_2785', 'last_updated': None}
    
    def save_data(self):
        """Save tracking data"""
        self.data['last_updated'] = datetime.now().isoformat()
        with open(self.tracking_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def update_username(self):
        """Update the username to analyze"""
        new_username = self.username_var.get().strip()
        if not new_username:
            messagebox.showwarning("Warning", "Username cannot be empty")
            self.username_var.set(self.data.get('username', 'Agitated_Age_2785'))
            return
        
        old_username = self.data.get('username', 'Agitated_Age_2785')
        self.data['username'] = new_username
        self.save_data()
        
        # Fetch posts for the new username
        messagebox.showinfo("Success", f"Username changed to @{new_username}\n\nFetching posts...")
        self.root.after(100, self.fetch_all_user_posts)
        
        # Refresh User Posts tab if it exists
        if hasattr(self, 'users_tree'):
            self.root.after(500, self.load_exchange_partners)
    
    def setup_ui(self):
        """Setup UI layout"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔴 REDDIT POST TRACKER", style='Title.TLabel')
        title_label.pack(pady=10)
        
        # Username control panel
        username_frame = ttk.LabelFrame(main_frame, text="User Settings", padding=10)
        username_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(username_frame, text="Analyze Reddit User:", foreground='#00d9ff').pack(side=tk.LEFT, padx=5)
        self.username_var = tk.StringVar(value=self.data.get('username', 'Agitated_Age_2785'))
        self.username_entry = ttk.Entry(username_frame, textvariable=self.username_var, width=30)
        self.username_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(username_frame, text="Update", command=self.update_username).pack(side=tk.LEFT, padx=5)
        ttk.Label(username_frame, text="(Changes affect Comments & User Posts tabs)", 
                  foreground='#888888', font=('Consolas', 8)).pack(side=tk.LEFT, padx=10)
        
        # Create notebook (tabs)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Dashboard
        self.dashboard_tab = ttk.Frame(notebook)
        notebook.add(self.dashboard_tab, text="Dashboard")
        self.setup_dashboard_tab()
        
        # Tab 2: Add Post
        add_post_tab = ttk.Frame(notebook)
        notebook.add(add_post_tab, text="Add Post")
        self.setup_add_post_tab(add_post_tab)
        
        # Tab 3: Update Snapshot
        update_tab = ttk.Frame(notebook)
        notebook.add(update_tab, text="Update Snapshot")
        self.setup_update_tab(update_tab)
        
        # Tab 4: Statistics
        stats_tab = ttk.Frame(notebook)
        notebook.add(stats_tab, text="Statistics")
        self.setup_stats_tab(stats_tab)
        
        # Tab 5: Comments
        comments_tab = ttk.Frame(notebook)
        notebook.add(comments_tab, text="Comments")
        self.setup_comments_tab(comments_tab)
        
        # Tab 6: User Posts
        user_posts_tab = ttk.Frame(notebook)
        notebook.add(user_posts_tab, text="User Posts")
        self.setup_user_posts_tab(user_posts_tab)
    
    def setup_dashboard_tab(self):
        """Dashboard tab showing all user posts"""
        # Toolbar
        toolbar = ttk.Frame(self.dashboard_tab)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="🔄 Fetch All Posts", command=self.fetch_all_user_posts).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Refresh", command=self.refresh_dashboard).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Export", command=self.export_summary).pack(side=tk.LEFT, padx=5)
        
        self.dashboard_status = ttk.Label(toolbar, text="Ready", foreground='#00d9ff')
        self.dashboard_status.pack(side=tk.LEFT, padx=20)
        
        # Tree view
        columns = ('Title', 'Subreddit', 'Score', 'Comments', 'Created', 'Status')
        self.tree = ttk.Treeview(self.dashboard_tab, columns=columns, height=20)
        
        # Configure columns
        self.tree.column('#0', width=50, minwidth=50)
        self.tree.column('Title', width=300, minwidth=200)
        self.tree.column('Subreddit', width=120, minwidth=100)
        self.tree.column('Score', width=80, minwidth=60)
        self.tree.column('Comments', width=80, minwidth=60)
        self.tree.column('Created', width=100, minwidth=80)
        self.tree.column('Status', width=80, minwidth=60)
        
        self.tree.heading('#0', text='#')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Subreddit', text='Subreddit')
        self.tree.heading('Score', text='Score')
        self.tree.heading('Comments', text='Comments')
        self.tree.heading('Created', text='Created')
        self.tree.heading('Status', text='Status')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.dashboard_tab, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Info panel
        info_frame = ttk.LabelFrame(self.dashboard_tab, text="Post Details", padding=10)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.info_text = tk.Text(info_frame, height=8, width=50, bg='#2d2d2d', fg='#e0e0e0')
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Action buttons for exploratory functions
        actions_frame = ttk.LabelFrame(self.dashboard_tab, text="Post Analysis", padding=10)
        actions_frame.pack(fill=tk.X, padx=5, pady=5)
        
        button_row = ttk.Frame(actions_frame)
        button_row.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_row, text="📊 Update Snapshot", command=self.dashboard_update_snapshot).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_row, text="💬 Fetch Comments", command=self.dashboard_fetch_comments).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_row, text="🔗 Exchange Partners", command=self.dashboard_show_partners).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_row, text="📈 Post Stats", command=self.dashboard_post_stats).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_row, text="🎯 Tier Gates", command=self.dashboard_analyze_tiers).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_row, text="⚔️ Conflict Gates", command=self.dashboard_analyze_conflicts).pack(side=tk.LEFT, padx=3)
        ttk.Button(button_row, text="🔄 Refresh Cache", command=lambda: self.dashboard_analyze_conflicts(force_refresh=True)).pack(side=tk.LEFT, padx=3)
        
        self.actions_status = ttk.Label(actions_frame, text="Select a post to analyze", foreground='#00d9ff')
        self.actions_status.pack(fill=tk.X, pady=5)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_post_select)
        
        # Auto-fetch posts on startup
        self.root.after(500, self.fetch_all_user_posts)
        
        self.refresh_dashboard()
    
    def fetch_all_user_posts(self):
        """Fetch ALL posts by the current username (with pagination)"""
        username = self.data.get('username', 'Agitated_Age_2785')
        
        self.dashboard_status.config(text=f"Fetching all posts from @{username}...")
        self.root.update()
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            
            posts_fetched = []
            after_cursor = None
            page = 0
            
            # Paginate through all posts
            while True:
                page += 1
                self.dashboard_status.config(text=f"Fetching posts from @{username} (page {page})...")
                self.root.update()
                
                # Try /posts.json first, fall back to /submitted.json
                url = f"https://www.reddit.com/user/{username}/posts.json"
                params = {'limit': 100}  # Maximum results per page
                if after_cursor:
                    params['after'] = after_cursor
                
                response = requests.get(url, headers=headers, params=params, timeout=15)
                
                if response.status_code == 404:
                    url = f"https://www.reddit.com/user/{username}/submitted.json"
                    response = requests.get(url, headers=headers, params=params, timeout=15)
                
                if response.status_code != 200:
                    self.dashboard_status.config(text=f"Error fetching posts (Status {response.status_code})")
                    messagebox.showerror("Error", f"Failed to fetch posts: Status {response.status_code}")
                    return
                
                data = response.json()
                children = data.get('data', {}).get('children', [])
                
                # If no more posts, stop
                if not children:
                    break
                
                # Extract posts from this page
                for item in children:
                    if item['kind'] == 't3':  # t3 = post
                        post_data = item['data']
                        post_id = post_data['id']
                        
                        # Check if we already have this post
                        existing = next((p for p in self.data['posts'] if p['post_id'] == post_id), None)
                        
                        if existing:
                            # Update snapshot for existing post
                            existing['snapshots'].append({
                                'timestamp': datetime.now().isoformat(),
                                'score': post_data['score'],
                                'comments': post_data['num_comments']
                            })
                            posts_fetched.append(existing)
                        else:
                            # Create new post entry
                            # Use Reddit's creation date, not the current time
                            post_creation_date = datetime.utcfromtimestamp(post_data['created_utc']).isoformat()
                            new_post = {
                                'post_id': post_id,
                                'title': post_data['title'],
                                'subreddit': post_data['subreddit'],
                                'url': post_data['url'],
                                'added_date': post_creation_date,
                                'snapshots': [
                                    {
                                        'timestamp': datetime.now().isoformat(),
                                        'score': post_data['score'],
                                        'comments': post_data['num_comments']
                                    }
                                ]
                            }
                            posts_fetched.append(new_post)
                
                # Get cursor for next page
                after_cursor = data.get('data', {}).get('after')
                if not after_cursor:
                    break  # No more pages
            
            # Update data file
            self.data['posts'] = posts_fetched
            self.save_data()
            
            # Refresh display
            self.refresh_dashboard()
            
            self.dashboard_status.config(text=f"✓ Loaded {len(posts_fetched)} posts from @{username}")
            
        except Exception as e:
            self.dashboard_status.config(text=f"Error: {str(e)[:50]}")
            messagebox.showerror("Error", f"Failed to fetch posts: {str(e)}")
    
    def refresh_dashboard(self):
        """Refresh dashboard display"""
        self.load_data()
        
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Populate tree with all fetched posts
        for i, post in enumerate(self.data['posts'], 1):
            if not post.get('snapshots'):
                continue
                
            snapshots = post['snapshots']
            latest = snapshots[-1]
            
            from datetime import datetime as dt
            created_time = datetime.fromisoformat(post['added_date']).strftime('%m/%d %H:%M')
            
            self.tree.insert('', 'end', iid=post['post_id'],
                           text=str(i),
                           values=(
                               post['title'][:60] + '...',
                               post['subreddit'],
                               latest['score'],
                               latest['comments'],
                               created_time,
                               "Active" if latest['score'] > 0 else "Stable"
                           ))
    
    def on_post_select(self, event):
        """Show post details when selected"""
        selection = self.tree.selection()
        if not selection:
            return
        
        post_id = selection[0]
        post = next((p for p in self.data['posts'] if p['post_id'] == post_id), None)
        
        if post:
            self.info_text.delete('1.0', tk.END)
            
            snapshots = post['snapshots']
            latest = snapshots[-1]
            first = snapshots[0]
            
            info = f"""
POST: {post['title']}

URL: {post['url']}

Subreddit: r/{post['subreddit']}

ENGAGEMENT TRACKING:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Initial Score:    {first['score']}
  Current Score:    {latest['score']}
  Change:           {latest['score'] - first['score']:+d}

  Initial Comments: {first['comments']}
  Current Comments: {latest['comments']}
  Change:           {latest['comments'] - first['comments']:+d}

SNAPSHOTS: {len(snapshots)}
  First:  {first['timestamp'][:16]}
  Latest: {latest['timestamp'][:16]}
            """.strip()
            
            self.info_text.insert('1.0', info)
    
    def setup_add_post_tab(self, parent):
        """Tab for adding new posts"""
        form_frame = ttk.LabelFrame(parent, text="Add New Post", padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Form fields
        fields = [
            ('Post ID:', 'post_id'),
            ('Title:', 'title'),
            ('Subreddit:', 'subreddit'),
            ('URL:', 'url'),
            ('Initial Score:', 'score'),
            ('Initial Comments:', 'comments')
        ]
        
        self.form_entries = {}
        
        for label_text, field_name in fields:
            frame = ttk.Frame(form_frame)
            frame.pack(fill=tk.X, pady=5)
            
            label = ttk.Label(frame, text=label_text, width=20)
            label.pack(side=tk.LEFT, padx=5)
            
            entry = ttk.Entry(frame, width=50)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            self.form_entries[field_name] = entry
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Add Post", command=self.add_post).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=5)
    
    def add_post(self):
        """Add a new post"""
        try:
            post = {
                'post_id': self.form_entries['post_id'].get().strip(),
                'title': self.form_entries['title'].get().strip(),
                'subreddit': self.form_entries['subreddit'].get().strip(),
                'url': self.form_entries['url'].get().strip(),
                'added_date': datetime.now().isoformat(),
                'snapshots': [
                    {
                        'timestamp': datetime.now().isoformat(),
                        'score': int(self.form_entries['score'].get() or 0),
                        'comments': int(self.form_entries['comments'].get() or 0)
                    }
                ]
            }
            
            # Validate
            if not all([post['post_id'], post['title'], post['subreddit'], post['url']]):
                messagebox.showerror("Error", "All fields required")
                return
            
            # Check if already exists
            if any(p['post_id'] == post['post_id'] for p in self.data['posts']):
                messagebox.showerror("Error", "Post ID already exists")
                return
            
            self.data['posts'].append(post)
            self.save_data()
            
            messagebox.showinfo("Success", f"Added: {post['title'][:50]}")
            self.clear_form()
            self.refresh_dashboard()
        
        except ValueError:
            messagebox.showerror("Error", "Invalid score or comment count (must be numbers)")
    
    def clear_form(self):
        """Clear form fields"""
        for entry in self.form_entries.values():
            entry.delete(0, tk.END)
    
    def setup_update_tab(self, parent):
        """Tab for updating post snapshots"""
        top_frame = ttk.Frame(parent, padding=10)
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text="Select Post to Update:", style='Header.TLabel').pack()
        
        # Post selector
        self.update_post_var = tk.StringVar()
        self.post_combo = ttk.Combobox(top_frame, textvariable=self.update_post_var, width=60, state='readonly')
        self.post_combo.pack(fill=tk.X, pady=5)
        self.post_combo.bind('<<ComboboxSelected>>', self.on_update_post_select)
        
        # Input frame
        input_frame = ttk.LabelFrame(parent, text="New Values", padding=20)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(input_frame, text="New Score:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.update_score = ttk.Entry(input_frame, width=30)
        self.update_score.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(input_frame, text="New Comment Count:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.update_comments = ttk.Entry(input_frame, width=30)
        self.update_comments.grid(row=1, column=1, padx=10, pady=5)
        
        # Info
        self.update_info = tk.Text(input_frame, height=6, width=50, bg='#2d2d2d', fg='#e0e0e0')
        self.update_info.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW, pady=10)
        
        # Button
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=2)
        
        ttk.Button(button_frame, text="Update Snapshot", command=self.update_snapshot).pack(padx=5)
        
        self.refresh_post_list()
    
    def refresh_post_list(self):
        """Refresh post selector dropdown"""
        self.load_data()
        posts = [f"{p['post_id']} - {p['title'][:40]}" for p in self.data['posts']]
        self.post_combo['values'] = posts
    
    def on_update_post_select(self, event):
        """Show current post values"""
        selection = self.update_post_var.get()
        if not selection:
            return
        
        post_id = selection.split(' - ')[0]
        post = next((p for p in self.data['posts'] if p['post_id'] == post_id), None)
        
        if post:
            latest = post['snapshots'][-1]
            self.update_score.delete(0, tk.END)
            self.update_score.insert(0, str(latest['score']))
            self.update_comments.delete(0, tk.END)
            self.update_comments.insert(0, str(latest['comments']))
            
            info = f"""
CURRENT VALUES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Score: {latest['score']}
Comments: {latest['comments']}

Last Updated: {latest['timestamp'][:16]}
Total Snapshots: {len(post['snapshots'])}
            """.strip()
            
            self.update_info.delete('1.0', tk.END)
            self.update_info.insert('1.0', info)
    
    def get_selected_post_id(self):
        """Get the currently selected post ID from dashboard"""
        selection = self.tree.selection()
        if selection:
            return selection[0]
        return None
    
    def dashboard_update_snapshot(self):
        """Update snapshot for selected post with current Reddit data"""
        post_id = self.get_selected_post_id()
        if not post_id:
            self.actions_status.config(text="No post selected")
            return
        
        post = next((p for p in self.data['posts'] if p['post_id'] == post_id), None)
        if not post:
            self.actions_status.config(text="Post not found")
            return
        
        self.actions_status.config(text=f"Fetching current data for {post_id}...")
        self.root.update()
        
        try:
            url = post['url']
            if url.endswith('/'):
                url = url[:-1]
            url += '.json'
            
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()[0]['data']['children'][0]['data']
                post['snapshots'].append({
                    'timestamp': datetime.now().isoformat(),
                    'score': data['score'],
                    'comments': data['num_comments']
                })
                self.save_data()
                self.refresh_dashboard()
                self.on_post_select(None)  # Refresh post details display
                self.actions_status.config(text=f"✓ Updated {post_id}: {data['score']} score, {data['num_comments']} comments")
            else:
                self.actions_status.config(text=f"Error: Status {response.status_code}")
        except Exception as e:
            self.actions_status.config(text=f"Error: {str(e)[:40]}")
    
    def dashboard_fetch_comments(self):
        """Fetch comments for selected post"""
        post_id = self.get_selected_post_id()
        if not post_id:
            self.actions_status.config(text="No post selected")
            return
        
        post = next((p for p in self.data['posts'] if p['post_id'] == post_id), None)
        if not post:
            self.actions_status.config(text="Post not found")
            return
        
        self.actions_status.config(text=f"Fetching comments for {post_id}...")
        self.root.update()
        
        # Run in thread to not freeze GUI
        thread = threading.Thread(target=self._dashboard_fetch_comments_thread, args=(post, post_id))
        thread.daemon = True
        thread.start()
    
    def _dashboard_fetch_comments_thread(self, post, post_id):
        """Background thread for fetching comments"""
        try:
            url = f"https://www.reddit.com/comments/{post_id}.json"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            comments = []
            
            def extract_comments(comment_list, depth=0):
                """Recursively extract comments including nested replies"""
                for item in comment_list:
                    if item['kind'] == 't1':
                        comment = item['data']
                        comments.append({
                            'id': comment['id'],
                            'author': comment.get('author', '[deleted]'),
                            'body': comment['body'],  # Full body, not truncated
                            'score': comment['score'],
                            'created': comment['created_utc'],
                            'depth': depth
                        })
                        
                        # Recursively process nested replies
                        replies = comment.get('replies', '')
                        if replies and isinstance(replies, dict):
                            reply_children = replies.get('data', {}).get('children', [])
                            extract_comments(reply_children, depth + 1)
            
            if len(data) > 1:
                comment_children = data[1]['data']['children']
                extract_comments(comment_children)
            
            self.root.after(0, lambda: self._show_comments_popup(post_id, comments))
            
        except Exception as e:
            self.root.after(0, lambda: self.actions_status.config(text=f"Error fetching comments: {str(e)[:40]}"))
    
    def _show_comments_popup(self, post_id, comments):
        """Show comments in a popup window with full detail"""
        popup = tk.Toplevel(self.root)
        popup.title(f"Comments for {post_id}")
        popup.geometry("800x600")
        popup.configure(bg='#1e1e1e')
        
        # Header with count
        header = ttk.Label(popup, text=f"Total Comments: {len(comments)}", foreground='#00d9ff')
        header.pack(fill=tk.X, padx=10, pady=5)
        
        # Text widget with scrollbar
        text = scrolledtext.ScrolledText(popup, bg='#2d2d2d', fg='#e0e0e0', font=('Consolas', 9), wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        if not comments:
            text.insert('1.0', "No comments found.")
        else:
            for i, comment in enumerate(comments, 1):
                # Indentation based on depth
                indent = "  " * comment['depth']
                author = comment['author']
                score = comment['score']
                
                # Insert comment header
                text.insert(tk.END, f"{indent}[{i}] {author} ({score:+d})\n")
                
                # Insert comment body
                body = comment['body']
                text.insert(tk.END, f"{indent}{body}\n")
                text.insert(tk.END, f"{indent}━━━━━━━━━━━━━━━━\n\n")
        
        text.config(state=tk.DISABLED)
        self.actions_status.config(text=f"✓ Fetched {len(comments)} comments (including nested)")
    
    def dashboard_show_partners(self):
        """Show exchange partners for selected post"""
        post_id = self.get_selected_post_id()
        if not post_id:
            self.actions_status.config(text="No post selected")
            return
        
        self.actions_status.config(text=f"Analyzing exchange partners for {post_id}...")
        self.root.update()
        
        # Run in thread
        thread = threading.Thread(target=self._dashboard_analyze_partners_thread, args=(post_id,))
        thread.daemon = True
        thread.start()
    
    def _dashboard_analyze_partners_thread(self, post_id):
        """Background thread for analyzing exchange partners"""
        try:
            url = f"https://www.reddit.com/comments/{post_id}.json"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=15)
            data = response.json()
            
            exchanges = {}
            
            def extract_comments(comment_list, depth=0, parent_author=None):
                for item in comment_list:
                    if item['kind'] == 't1':
                        comment = item['data']
                        author = comment.get('author', '[deleted]')
                        
                        if parent_author and parent_author != author and parent_author != '[deleted]':
                            key = tuple(sorted([author, parent_author]))
                            exchanges[key] = exchanges.get(key, 0) + 1
                        
                        extract_comments(comment.get('replies', {}).get('data', {}).get('children', []), 
                                       depth + 1, author)
            
            if len(data) > 1:
                extract_comments(data[1].get('data', {}).get('children', []))
            
            meaningful = [(users, count) for users, count in exchanges.items() if count >= 3]
            meaningful.sort(key=lambda x: x[1], reverse=True)
            
            self.root.after(0, lambda: self._show_partners_popup(post_id, meaningful))
            
        except Exception as e:
            self.root.after(0, lambda: self.actions_status.config(text=f"Error: {str(e)[:40]}"))
    
    def _show_partners_popup(self, post_id, partners):
        """Show exchange partners in a popup"""
        popup = tk.Toplevel(self.root)
        popup.title(f"Exchange Partners - {post_id}")
        popup.geometry("500x300")
        popup.configure(bg='#1e1e1e')
        
        text = scrolledtext.ScrolledText(popup, bg='#2d2d2d', fg='#e0e0e0', font=('Consolas', 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        if not partners:
            text.insert('1.0', "No meaningful exchanges found (need 3+ dialogues).")
        else:
            text.insert('1.0', f"EXCHANGE PARTNERS ({len(partners)} found):\n\n")
            for i, (users, count) in enumerate(partners, 1):
                user1, user2 = users
                text.insert(tk.END, f"{i}. {user1} ↔ {user2}\n")
                text.insert(tk.END, f"   {count} dialogues\n\n")
        
        text.config(state=tk.DISABLED)
        self.actions_status.config(text=f"✓ Found {len(partners)} exchange partners")
    
    def dashboard_post_stats(self):
        """Show statistics for the selected post"""
        post_id = self.get_selected_post_id()
        if not post_id:
            self.actions_status.config(text="No post selected")
            return
        
        post = next((p for p in self.data['posts'] if p['post_id'] == post_id), None)
        if not post:
            self.actions_status.config(text="Post not found")
            return
        
        popup = tk.Toplevel(self.root)
        popup.title(f"Stats - {post_id}")
        popup.geometry("600x400")
        popup.configure(bg='#1e1e1e')
        
        text = scrolledtext.ScrolledText(popup, bg='#2d2d2d', fg='#e0e0e0', font=('Consolas', 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        snapshots = post['snapshots']
        first = snapshots[0]
        latest = snapshots[-1]
        
        score_change = latest['score'] - first['score']
        comment_change = latest['comments'] - first['comments']
        
        stats = f"""
POST STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Title: {post['title']}

SCORE TRACKING:
  Initial:    {first['score']}
  Current:    {latest['score']}
  Change:     {score_change:+d}
  Status:     {'📈 TRENDING UP' if score_change > 0 else '📉 TRENDING DOWN' if score_change < 0 else '→ STABLE'}

COMMENT TRACKING:
  Initial:    {first['comments']}
  Current:    {latest['comments']}
  Change:     {comment_change:+d}

TRACKING INFO:
  Snapshots:  {len(snapshots)}
  First:      {first['timestamp'][:16]}
  Latest:     {latest['timestamp'][:16]}
        """.strip()
        
        text.insert('1.0', stats)
        text.config(state=tk.DISABLED)
        self.actions_status.config(text=f"✓ Stats for {post_id}")
    
    def dashboard_analyze_tiers(self):
        """Analyze tier gate skipping in conversation threads"""
        post_id = self.get_selected_post_id()
        if not post_id:
            self.actions_status.config(text="No post selected")
            return
        
        self.actions_status.config(text=f"Analyzing tier progression for {post_id}...")
        self.root.update()
        
        # Run in thread
        thread = threading.Thread(target=self._dashboard_analyze_tiers_thread, args=(post_id,))
        thread.daemon = True
        thread.start()
    
    def _dashboard_analyze_tiers_thread(self, post_id):
        """Background thread for tier gate analysis with temporal interaction frequency"""
        try:
            url = f"https://www.reddit.com/comments/{post_id}.json"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=15)
            data = response.json()
            
            # Build comment tree with temporal data
            comments_by_id = {}
            comment_replies = {}
            post_created = data[0]['data']['children'][0]['data']['created_utc']
            
            def extract_comment_tree(comment_list, parent_id=None):
                for item in comment_list:
                    if item['kind'] == 't1':
                        comment = item['data']
                        comment_id = comment['id']
                        comments_by_id[comment_id] = {
                            'author': comment.get('author', '[deleted]'),
                            'score': comment['score'],
                            'parent_id': parent_id,
                            'depth': comment.get('depth', 0),
                            'created_utc': comment.get('created_utc', 0),
                            'body': comment.get('body', '')
                        }
                        
                        if parent_id:
                            if parent_id not in comment_replies:
                                comment_replies[parent_id] = []
                            comment_replies[parent_id].append(comment_id)
                        
                        replies = comment.get('replies', '')
                        if replies and isinstance(replies, dict):
                            reply_children = replies.get('data', {}).get('children', [])
                            extract_comment_tree(reply_children, comment_id)
            
            if len(data) > 1:
                extract_comment_tree(data[1]['data']['children'])
            
            # Analyze tier progression, temporal patterns, and interaction frequency
            tier_skips = []
            tier_progression = {}
            user_activity = {}  # Track users' comment counts and timeline
            response_times = []  # Time gaps between parent and replies
            user_pairs = {}  # Track communication between specific user pairs
            
            for comment_id, comment_info in comments_by_id.items():
                author = comment_info['author']
                
                # Track user activity
                if author not in user_activity:
                    user_activity[author] = {
                        'count': 0,
                        'timestamps': [],
                        'min_time': float('inf'),
                        'max_time': 0
                    }
                
                user_activity[author]['count'] += 1
                timestamp = comment_info['created_utc']
                user_activity[author]['timestamps'].append(timestamp)
                user_activity[author]['min_time'] = min(user_activity[author]['min_time'], timestamp)
                user_activity[author]['max_time'] = max(user_activity[author]['max_time'], timestamp)
                
                # Analyze tier gaps and response times
                if comment_info['parent_id']:
                    parent_info = comments_by_id.get(comment_info['parent_id'])
                    if parent_info:
                        parent_tier = parent_info.get('depth', 0)
                        current_tier = comment_info.get('depth', 0)
                        tier_gap = current_tier - parent_tier
                        
                        # Time gap analysis
                        time_gap = comment_info['created_utc'] - parent_info['created_utc']
                        response_times.append({
                            'child_author': author,
                            'parent_author': parent_info['author'],
                            'time_gap_seconds': time_gap,
                            'tier_gap': tier_gap
                        })
                        
                        # Track user pair interactions
                        pair_key = tuple(sorted([author, parent_info['author']]))
                        if pair_key not in user_pairs:
                            user_pairs[pair_key] = {
                                'interactions': 0,
                                'total_time': 0,
                                'time_gaps': []
                            }
                        
                        user_pairs[pair_key]['interactions'] += 1
                        user_pairs[pair_key]['total_time'] += time_gap
                        user_pairs[pair_key]['time_gaps'].append(time_gap)
                        
                        # Track tier skips
                        if tier_gap > 1:
                            tier_skips.append({
                                'child_author': author,
                                'parent_author': parent_info['author'],
                                'from_tier': parent_tier,
                                'to_tier': current_tier,
                                'skipped_tiers': tier_gap - 1,
                                'response_time': time_gap
                            })
                        
                        # Track normal progression
                        key = (parent_tier, current_tier)
                        tier_progression[key] = tier_progression.get(key, 0) + 1
            
            # Calculate interaction frequency and communication alignment
            conversation_window = max([user_activity[u]['max_time'] for u in user_activity], default=0) - \
                                 min([user_activity[u]['min_time'] for u in user_activity], default=post_created)
            
            self.root.after(0, lambda: self._show_tier_analysis_popup(
                post_id, tier_skips, tier_progression, len(comments_by_id),
                user_activity, user_pairs, response_times, conversation_window
            ))
            
        except Exception as e:
            self.root.after(0, lambda: self.actions_status.config(text=f"Error: {str(e)[:40]}"))
            
            for comment_id, comment_info in comments_by_id.items():
                if comment_info['parent_id']:
                    parent_info = comments_by_id.get(comment_info['parent_id'])
                    if parent_info:
                        # Calculate tier gap (how many tiers were skipped)
                        parent_tier = parent_info.get('depth', 0)
                        current_tier = comment_info.get('depth', 0)
                        tier_gap = current_tier - parent_tier
                        
                        # A normal progression is +1, anything > 1 is a skip
                        if tier_gap > 1:
                            tier_skips.append({
                                'child_author': comment_info['author'],
                                'parent_author': parent_info['author'],
                                'from_tier': parent_tier,
                                'to_tier': current_tier,
                                'skipped_tiers': tier_gap - 1
                            })
                        
                        # Track progression patterns
                        key = (parent_tier, current_tier)
                        tier_progression[key] = tier_progression.get(key, 0) + 1
            
            self.root.after(0, lambda: self._show_tier_analysis_popup(post_id, tier_skips, tier_progression, len(comments_by_id)))
            
        except Exception as e:
            self.root.after(0, lambda: self.actions_status.config(text=f"Error: {str(e)[:40]}"))
    
    def _show_tier_analysis_popup(self, post_id, tier_skips, tier_progression, total_comments, user_activity, user_pairs, response_times, conversation_window):
        """Display tier gate analysis with temporal interaction frequency and communication alignment"""
        popup = tk.Toplevel(self.root)
        popup.title(f"Tier Gate & Interaction Analysis - {post_id}")
        popup.geometry("1000x700")
        popup.configure(bg='#1e1e1e')
        
        text = scrolledtext.ScrolledText(popup, bg='#2d2d2d', fg='#e0e0e0', font=('Consolas', 9))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        text.insert(tk.END, f"CONVERSATION ANALYSIS: TIER GATES & INTERACTION FREQUENCY\n")
        text.insert(tk.END, f"{'='*100}\n\n")
        
        text.insert(tk.END, f"Total Comments: {total_comments} | Tier Gate Skips: {len(tier_skips)} | ")
        skip_rate = (len(tier_skips) / total_comments * 100) if total_comments > 0 else 0
        text.insert(tk.END, f"Skip Rate: {skip_rate:.1f}%\n\n")
        
        # Interaction Frequency Analysis
        text.insert(tk.END, f"{'─'*100}\n")
        text.insert(tk.END, f"INTERACTION FREQUENCY & USER ACTIVITY\n")
        text.insert(tk.END, f"{'─'*100}\n\n")
        
        # Sort users by comment count
        sorted_users = sorted(user_activity.items(), key=lambda x: x[1]['count'], reverse=True)
        
        text.insert(tk.END, f"{'User':<20} {'Comments':>10} {'Active Period (hours)':>20} {'Avg Time Between Posts':>25}\n")
        text.insert(tk.END, f"{'-'*76}\n")
        
        for user, activity in sorted_users[:15]:  # Top 15 users
            time_span = activity['max_time'] - activity['min_time']
            hours_active = time_span / 3600 if time_span > 0 else 0
            timestamps = sorted(activity['timestamps'])
            
            if len(timestamps) > 1:
                time_gaps = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
                avg_gap = sum(time_gaps) / len(time_gaps) / 60  # Convert to minutes
            else:
                avg_gap = 0
            
            text.insert(tk.END, f"{user:<20} {activity['count']:>10} {hours_active:>20.1f} {avg_gap:>20.1f} min\n")
        
        text.insert(tk.END, f"\n\n")
        
        # Communication Alignment Analysis
        text.insert(tk.END, f"{'─'*100}\n")
        text.insert(tk.END, f"COMMUNICATION ALIGNMENT (User Pair Interaction Patterns)\n")
        text.insert(tk.END, f"{'─'*100}\n\n")
        
        # Sort pairs by interaction count
        sorted_pairs = sorted(user_pairs.items(), key=lambda x: x[1]['interactions'], reverse=True)
        
        text.insert(tk.END, f"{'User 1':<15} {'User 2':<15} {'Interactions':>12} {'Avg Response Time':>20} {'Communication Window':<15}\n")
        text.insert(tk.END, f"{'-'*78}\n")
        
        for (user1, user2), pair_info in sorted_pairs[:15]:  # Top communication pairs
            avg_response = pair_info['total_time'] / pair_info['interactions'] / 3600 if pair_info['interactions'] > 0 else 0
            min_gap = min(pair_info['time_gaps']) / 3600 if pair_info['time_gaps'] else 0
            max_gap = max(pair_info['time_gaps']) / 3600 if pair_info['time_gaps'] else 0
            
            window_str = f"{min_gap:.1f}-{max_gap:.1f}h" if pair_info['time_gaps'] else "N/A"
            text.insert(tk.END, f"{user1:<15} {user2:<15} {pair_info['interactions']:>12} {avg_response:>18.2f}h   {window_str:<15}\n")
        
        text.insert(tk.END, f"\n\n")
        
        # Overall Conversation Window
        text.insert(tk.END, f"{'─'*100}\n")
        text.insert(tk.END, f"CONVERSATION WINDOW\n")
        text.insert(tk.END, f"{'─'*100}\n\n")
        
        conv_hours = conversation_window / 3600 if conversation_window > 0 else 0
        conv_days = conv_hours / 24 if conv_hours > 0 else 0
        text.insert(tk.END, f"Total Conversation Duration: {conv_days:.1f} days ({conv_hours:.1f} hours)\n")
        text.insert(tk.END, f"Comment Density: {total_comments / max(conv_hours, 1):.2f} comments/hour\n\n")
        
        # Tier Analysis
        text.insert(tk.END, f"{'─'*100}\n")
        text.insert(tk.END, f"TIER GATE INTEGRITY\n")
        text.insert(tk.END, f"{'─'*100}\n\n")
        
        for (from_tier, to_tier), count in sorted(tier_progression.items()):
            if to_tier - from_tier == 1:  # Normal progression
                text.insert(tk.END, f"  ✓ Tier {from_tier} → {to_tier}: {count} normal progressions\n")
        
        if tier_skips:
            text.insert(tk.END, f"\n⚠️  TIER GATE VIOLATIONS:\n")
            skip_patterns = {}
            for skip in tier_skips:
                pattern = f"Tier {skip['from_tier']} → {skip['to_tier']}"
                if pattern not in skip_patterns:
                    skip_patterns[pattern] = []
                skip_patterns[pattern].append(skip)
            
            for pattern, skips in sorted(skip_patterns.items()):
                text.insert(tk.END, f"  {pattern}: {len(skips)} violations\n")
                for skip in skips[:3]:  # Show first 3 examples
                    response_hours = skip.get('response_time', 0) / 3600
                    text.insert(tk.END, f"    - {skip['child_author']} skipped after {response_hours:.1f}h\n")
        else:
            text.insert(tk.END, f"\n✓  NO TIER GATE VIOLATIONS\n")
            text.insert(tk.END, f"    All participants follow sequential tier progression.\n")
        
        # Final Assessment
        text.insert(tk.END, f"\n\n{'='*100}\n")
        text.insert(tk.END, f"ASSESSMENT\n")
        text.insert(tk.END, f"{'='*100}\n\n")
        
        if len(tier_skips) == 0:
            text.insert(tk.END, f"✓ Tier gates are INTACT and being respected\n")
        else:
            text.insert(tk.END, f"⚠️  Tier gates are BEING SKIPPED ({skip_rate:.1f}% of interactions)\n")
        
        text.insert(tk.END, f"✓ Communication is active across {len(sorted_users)} participants\n")
        text.insert(tk.END, f"✓ Top communicators: {', '.join([u[0] for u in sorted_users[:3]])}\n")
        text.insert(tk.END, f"✓ Peak communication pairs indicate engagement alignment\n")
        
        text.config(state=tk.DISABLED)
        self.actions_status.config(text=f"✓ Analysis complete: {len(tier_skips)} gate violations, {len(sorted_pairs)} active pairs")
    
    def dashboard_analyze_conflicts(self, force_refresh=False):
        """Analyze alignment breaks and obvious violations (gates of conflict)"""
        post_id = self.get_selected_post_id()
        if not post_id:
            self.actions_status.config(text="No post selected")
            return
        
        refresh_text = " (refreshing cache)" if force_refresh else ""
        self.actions_status.config(text=f"Analyzing conflict patterns for {post_id}{refresh_text}...")
        self.root.update()
        
        thread = threading.Thread(target=self._dashboard_analyze_conflicts_thread, args=(post_id, force_refresh))
        thread.daemon = True
        thread.start()
    
    def _dashboard_analyze_conflicts_thread(self, post_id, force_refresh=False):
        """Background thread for conflict analysis with UFM caching (reasons + triggers stored)"""
        try:
            # Check cache first (unless force_refresh)
            if not force_refresh:
                # Check if both raw data AND analysis are cached and fresh
                cached_data = self._get_cached_comments(post_id)
                cached_analysis = self._get_cached_analysis(post_id)
                
                if cached_data and cached_analysis:
                    comments, data_age = cached_data
                    analysis_results, analysis_age = cached_analysis
                    self.root.after(0, lambda: self.actions_status.config(
                        text=f"Using cached analysis ({analysis_age:.1f}h old) + data ({data_age:.1f}h old)"))
                    # Use cached analysis results directly - no re-analysis needed
                    self._display_cached_conflict_analysis(post_id, analysis_results)
                    return
                elif cached_data:
                    comments, age = cached_data
                    self.root.after(0, lambda: self.actions_status.config(
                        text=f"Using cached raw data ({age:.1f}h old) - analyzing..."))
                    # Analyze from cached raw data
                    self._analyze_comments_data(post_id, comments, use_cache=True)
                    return
            
            # Not in cache or forced refresh - fetch from Reddit
            self.root.after(0, lambda: self.actions_status.config(text=f"Fetching fresh data from Reddit..."))
            
            url = f"https://www.reddit.com/comments/{post_id}.json"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=15)
            data = response.json()
            
            # Save to cache
            self._save_cached_comments(post_id, data)
            self.root.after(0, lambda: self.actions_status.config(text=f"Data cached - analyzing..."))
            
            # Process the data
            self._analyze_comments_data(post_id, data, use_cache=False)
            
        except Exception as e:
            self.root.after(0, lambda: self.actions_status.config(text=f"Error: {str(e)[:40]}"))
    
    def _analyze_comments_data(self, post_id, data, use_cache=False):
        """Analyze comments data (extracted method for reuse)"""
        try:
            # Get original post content
            post_data = data[0]['data']['children'][0]['data']
            original_body = post_data.get('selftext', '')
            original_body_lower = original_body.lower()
            post_author = post_data.get('author', '[deleted]')
            post_title = post_data.get('title', '')
            post_subreddit = post_data.get('subreddit', '')
            
            # Check for cross-post
            crosspost_info = None
            if 'crosspost_parent_list' in post_data and post_data['crosspost_parent_list']:
                crosspost_original = post_data['crosspost_parent_list'][0]
                crosspost_info = {
                    'original_subreddit': crosspost_original.get('subreddit', 'unknown'),
                    'original_author': crosspost_original.get('author', 'unknown'),
                    'original_post_id': crosspost_original.get('id', ''),
                    'original_title': crosspost_original.get('title', ''),
                    'crosspost_flag': True
                }
            
            # Extract ALL comments
            all_comments = {}
            top_level_comments = []
            
            def extract_all_comments(comment_list, parent_id=None):
                for item in comment_list:
                    if item['kind'] == 't1':
                        comment = item['data']
                        comment_id = comment['id']
                        depth = comment.get('depth', 0)
                        
                        all_comments[comment_id] = {
                            'id': comment_id,
                            'author': comment.get('author', '[deleted]'),
                            'body': comment.get('body', ''),
                            'score': comment['score'],
                            'created_utc': comment.get('created_utc', 0),
                            'depth': depth,
                            'parent_id': parent_id,
                            'replies': []
                        }
                        
                        if depth == 0:
                            top_level_comments.append(all_comments[comment_id])
                        
                        replies = comment.get('replies', '')
                        if replies and isinstance(replies, dict):
                            extract_all_comments(replies.get('data', {}).get('children', []), comment_id)
            
            if len(data) > 1:
                extract_all_comments(data[1]['data']['children'])
            
            # Build reply chains
            for comment_id, comment in all_comments.items():
                if comment['parent_id'] and comment['parent_id'] in all_comments:
                    all_comments[comment['parent_id']]['replies'].append(comment_id)
            
            # Conflict/agreement markers
            conflict_markers = ['disagree', 'wrong', 'incorrect', 'contradicts', 'contradicting',
                               'false', 'not true', 'mistake', 'error', 'no way', 'impossible',
                               'illogical', 'against', 'opposition', 'opposite', 'contrary',
                               'flawed', 'refute', 'debunk', 'reject']
            
            agreement_markers = ['agree', 'true', 'correct', 'right', 'exactly', 'precisely',
                                'well said', 'good point', 'excellent', 'brilliant', 'well done',
                                'support', 'endorse', 'validate', 'confirmed', 'absolutely']
            
            conflicts = []
            agreements = []
            neutral_responses = []
            causal_chains = []
            ufm_breakdown = {}  # User Failure Model with REAL reasons
            
            # Analyze top-level comments
            for comment in top_level_comments:
                body = comment['body']
                body_lower = body.lower()
                has_conflict = any(marker in body_lower for marker in conflict_markers)
                has_agreement = any(marker in body_lower for marker in agreement_markers)
                
                # WHY analysis - extract actual reasons from content
                reason = self._analyze_comment_reason(body, original_body_lower, has_conflict, has_agreement)
                
                # What did they respond to (what from original post)
                what_triggered = self._find_triggering_content(body, original_body_lower, original_body)
                
                if has_conflict:
                    conflicts.append({
                        'author': comment['author'],
                        'score': comment['score'],
                        'type': 'disagreement',
                        'id': comment['id'],
                        'reason': reason,  # WHY they disagreed
                        'what_triggered': what_triggered,  # WHAT triggered them
                        'their_claim': body[:200]  # What they said
                    })
                elif has_agreement:
                    agreements.append({
                        'author': comment['author'],
                        'score': comment['score'],
                        'type': 'agreement',
                        'id': comment['id'],
                        'reason': reason,
                        'what_triggered': what_triggered,
                        'their_claim': body[:200]
                    })
                else:
                    neutral_responses.append({
                        'author': comment['author'],
                        'score': comment['score'],
                        'type': 'neutral',
                        'id': comment['id'],
                        'reason': 'Unclear alignment - may be asking for clarification',
                        'what_triggered': what_triggered,
                        'their_claim': body[:200]
                    })
                
                # Build UFM breakdown with real reasons
                if comment['author'] not in ufm_breakdown:
                    ufm_breakdown[comment['author']] = {
                        'comments': 0,
                        'reasons': [],  # ACTUAL reasons
                        'what_triggered': [],
                        'disagreements': [],
                        'score': 0,
                        'alignment': 'unknown'
                    }
                
                ufm_breakdown[comment['author']]['comments'] += 1
                ufm_breakdown[comment['author']]['reasons'].append(reason)
                ufm_breakdown[comment['author']]['what_triggered'].append(what_triggered)
                ufm_breakdown[comment['author']]['score'] += comment['score']
                
                if has_conflict:
                    ufm_breakdown[comment['author']]['disagreements'].append(reason)
                    ufm_breakdown[comment['author']]['alignment'] = 'conflict'
                elif has_agreement:
                    ufm_breakdown[comment['author']]['alignment'] = 'agreement'
            
            # Build causal chains
            def trace_chain(comment_id, depth=0):
                if comment_id not in all_comments:
                    return []
                
                comment = all_comments[comment_id]
                chain = [(comment['author'], comment['score'], depth, comment['body'][:100])]
                
                for reply_id in comment['replies']:
                    if reply_id in all_comments:
                        chain.extend(trace_chain(reply_id, depth + 1))
                
                return chain
            
            # Get longest chains
            for comment in top_level_comments:
                chain = trace_chain(comment['id'])
                if len(chain) > 1:
                    causal_chains.append({
                        'initiator': comment['author'],
                        'chain_length': len(chain),
                        'participants': [c[0] for c in chain],
                        'chain': chain
                    })
            
            causal_chains.sort(key=lambda x: x['chain_length'], reverse=True)
            
            violations = [c for c in conflicts if c['score'] < 0]
            
            # CACHE the UFM analysis results (reasons, triggers, breakdown, violations)
            # This is the UFM way - store actual reasons and findings, not just raw data
            analysis_results = {
                'post_author': post_author,
                'original_body': original_body,
                'conflicts': conflicts,
                'agreements': agreements,
                'neutral_responses': neutral_responses,
                'violations': violations,
                'total_comments': len(top_level_comments),
                'causal_chains': causal_chains,
                'crosspost_info': crosspost_info,
                'ufm_breakdown': ufm_breakdown
            }
            self._save_cached_analysis(post_id, analysis_results)
            
            self.root.after(0, lambda: self._show_conflict_analysis_popup(
                post_id, post_author, original_body, conflicts, agreements, 
                neutral_responses, violations, len(top_level_comments),
                causal_chains, crosspost_info, ufm_breakdown
            ))
            
        except Exception as e:
            self.root.after(0, lambda: self.actions_status.config(text=f"Error: {str(e)[:40]}"))
    
    def _analyze_comment_reason(self, comment_body, original_body, has_conflict, has_agreement):
        """Extract the actual REASON why they commented"""
        body_lower = comment_body.lower()
        
        if has_conflict:
            # What specific disagreement
            if 'wrong' in body_lower or 'incorrect' in body_lower:
                return "Claims the original statement is factually wrong"
            elif 'disagree' in body_lower:
                return "Disagrees with the position or opinion"
            elif 'evidence' in body_lower or 'prove' in body_lower:
                return "Questions lack of evidence or proof"
            elif 'not true' in body_lower or 'false' in body_lower:
                return "Disputes truthfulness of claim"
            elif 'contradiction' in body_lower or 'contradicts' in body_lower:
                return "Points out internal contradiction"
            elif 'but' in body_lower and ('could' in body_lower or 'might' in body_lower):
                return "Presents counterargument or alternative view"
            else:
                return "Directly challenges or refutes the claim"
        
        elif has_agreement:
            if 'exactly' in body_lower or 'precisely' in body_lower:
                return "Strongly agrees with specific point"
            elif 'well said' in body_lower or 'good point' in body_lower:
                return "Validates the argument as well-reasoned"
            elif 'also' in body_lower or 'too' in body_lower:
                return "Adds supporting evidence or similar example"
            elif 'thank' in body_lower:
                return "Appreciates the post or information"
            else:
                return "Endorses the main position"
        
        else:
            if 'question' in body_lower or '?' in comment_body:
                return "Asks clarifying question"
            elif 'example' in body_lower or 'like' in body_lower:
                return "Requests or provides example"
            elif 'context' in body_lower or 'background' in body_lower:
                return "Seeks or provides context"
            else:
                return "Neutral response - unclear position"
    
    def _find_triggering_content(self, comment_body, original_body, original_body_full):
        """Find what in the original post TRIGGERED this response"""
        body_lower = comment_body.lower()
        
        # Extract key phrases from comment that might reference original
        trigger_words = []
        potential_triggers = []
        
        # Look for specific claims being challenged
        if 'claim' in body_lower or 'states' in body_lower or 'says' in body_lower:
            # They're responding to a specific claim
            potential_triggers.append("Responding to a specific claim in the post")
        
        # Check for certainty language triggering response
        if 'always' in original_body or 'never' in original_body:
            if 'disagree' in body_lower or 'wrong' in body_lower:
                potential_triggers.append("Absolute language ('always'/'never') triggered disagreement")
        
        # Check for controversial topics
        if 'should' in original_body or 'must' in original_body:
            if 'disagree' in body_lower:
                potential_triggers.append("Prescriptive statement triggered disagreement")
        
        # Check for opinion vs fact issue
        if 'think' in original_body or 'believe' in original_body:
            if 'evidence' in body_lower or 'proof' in body_lower:
                potential_triggers.append("Opinion presented as fact triggered challenge")
        
        # Check for specificity
        if not potential_triggers:
            # Generic triggers
            if 'disagree' in body_lower:
                potential_triggers.append("Fundamental disagreement with post premise")
            elif 'agree' in body_lower:
                potential_triggers.append("General agreement with post direction")
            else:
                potential_triggers.append("Seeking clarification on post content")
        
        return potential_triggers[0] if potential_triggers else "Not specified"
    
    def _show_conflict_analysis_popup(self, post_id, post_author, original_body, conflicts, agreements, neutral_responses, violations, total_comments, causal_chains=None, crosspost_info=None, ufm_breakdown=None):
        """Display conflict analysis with ACTUAL reasons (content-based)"""
        popup = tk.Toplevel(self.root)
        popup.title(f"Why Conflicts Happened - {post_id}")
        popup.geometry("1400x950")
        popup.configure(bg='#1e1e1e')
        
        text = scrolledtext.ScrolledText(popup, bg='#2d2d2d', fg='#e0e0e0', font=('Consolas', 9))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Cross-post header if detected
        if crosspost_info:
            text.insert(tk.END, f"⊞ CROSS-POST DETECTED\n")
            text.insert(tk.END, f"{'='*110}\n")
            text.insert(tk.END, f"Original Post: r/{crosspost_info['original_subreddit']}\n")
            text.insert(tk.END, f"Original Author: u/{crosspost_info['original_author']}\n")
            text.insert(tk.END, f"Link: https://reddit.com/{crosspost_info['original_post_id']}\n\n")
        
        text.insert(tk.END, f"WHY CONFLICTS HAPPENED - ACTUAL REASONS\n")
        text.insert(tk.END, f"{'='*110}\n\n")
        
        text.insert(tk.END, f"Original Post by: u/{post_author}\n")
        text.insert(tk.END, f"Total Top-Level Comments: {total_comments}\n")
        text.insert(tk.END, f"Agreements: {len(agreements)} | Conflicts: {len(conflicts)} | Neutral: {len(neutral_responses)}\n\n")
        
        # UFM (User Failure Model) Breakdown - WHY
        if ufm_breakdown:
            text.insert(tk.END, f"{'─'*110}\n")
            text.insert(tk.END, f"WHY EACH USER RESPONDED (User Motivations & Actual Reasons)\n")
            text.insert(tk.END, f"{'─'*110}\n\n")
            
            for user in sorted(ufm_breakdown.keys()):
                data = ufm_breakdown[user]
                text.insert(tk.END, f"USER: u/{user}\n")
                text.insert(tk.END, f"  Alignment: {data['alignment'].upper()} | Comments: {data['comments']} | Total Score: {data['score']:+d}\n\n")
                
                # Show ACTUAL reasons
                if data['reasons']:
                    text.insert(tk.END, f"  WHY THEY RESPONDED:\n")
                    for reason in set(data['reasons']):
                        count = data['reasons'].count(reason)
                        text.insert(tk.END, f"    → {reason}\n")
                
                # What triggered them
                if data['what_triggered']:
                    text.insert(tk.END, f"  WHAT TRIGGERED THEM:\n")
                    for trigger in set(data['what_triggered']):
                        text.insert(tk.END, f"    → {trigger}\n")
                
                # If they disagreed, show disagreement reasons
                if data['disagreements']:
                    text.insert(tk.END, f"  SPECIFIC DISAGREEMENTS:\n")
                    for disagreement in set(data['disagreements']):
                        text.insert(tk.END, f"    ✗ {disagreement}\n")
                
                text.insert(tk.END, f"\n")
        
        # Conflicts with reasons
        text.insert(tk.END, f"{'─'*110}\n")
        text.insert(tk.END, f"CONFLICTS ({len(conflicts)}) - WHY THEY DISAGREED\n")
        text.insert(tk.END, f"{'─'*110}\n\n")
        
        if conflicts:
            for i, item in enumerate(conflicts[:10], 1):
                text.insert(tk.END, f"{i}. u/{item['author']} (Score: {item['score']:+d})\n")
                text.insert(tk.END, f"   WHY: {item.get('reason', 'Unknown')}\n")
                text.insert(tk.END, f"   WHAT TRIGGERED: {item.get('what_triggered', 'Not specified')}\n")
                text.insert(tk.END, f"   THEIR CLAIM: \"{item.get('their_claim', 'N/A')[:120]}...\"\n\n")
        else:
            text.insert(tk.END, "No conflicts detected.\n\n")
        
        # Agreements with reasons
        text.insert(tk.END, f"{'─'*110}\n")
        text.insert(tk.END, f"AGREEMENTS ({len(agreements)}) - WHY THEY AGREED\n")
        text.insert(tk.END, f"{'─'*110}\n\n")
        
        if agreements:
            for i, item in enumerate(agreements[:10], 1):
                text.insert(tk.END, f"{i}. u/{item['author']} (Score: {item['score']:+d})\n")
                text.insert(tk.END, f"   WHY: {item.get('reason', 'Unknown')}\n")
                text.insert(tk.END, f"   WHAT TRIGGERED: {item.get('what_triggered', 'Not specified')}\n")
                text.insert(tk.END, f"   THEIR CLAIM: \"{item.get('their_claim', 'N/A')[:120]}...\"\n\n")
        else:
            text.insert(tk.END, "No agreements detected.\n\n")
        
        # Violations with reasons
        text.insert(tk.END, f"{'─'*110}\n")
        text.insert(tk.END, f"VIOLATIONS ({len(violations)}) - REJECTED BY COMMUNITY\n")
        text.insert(tk.END, f"{'─'*110}\n\n")
        
        if violations:
            text.insert(tk.END, f"Found {len(violations)} comments that disagreed AND were rejected (negative score):\n\n")
            for i, item in enumerate(violations[:10], 1):
                text.insert(tk.END, f"{i}. u/{item['author']} (Score: {item['score']} - DOWNVOTED)\n")
                text.insert(tk.END, f"   WHY THEY DISAGREED: {item.get('reason', 'Unknown')}\n")
                text.insert(tk.END, f"   WHAT TRIGGERED: {item.get('what_triggered', 'Not specified')}\n\n")
        else:
            text.insert(tk.END, "No violations detected.\n\n")
        
        # Causal chains section
        if causal_chains:
            text.insert(tk.END, f"\n{'─'*110}\n")
            text.insert(tk.END, f"CAUSAL CHAINS (How arguments escalated)\n")
            text.insert(tk.END, f"{'─'*110}\n\n")
            
            for i, chain in enumerate(causal_chains[:3], 1):
                text.insert(tk.END, f"{i}. Started by: u/{chain['initiator']}\n")
                text.insert(tk.END, f"   Length: {chain['chain_length']} messages\n")
                text.insert(tk.END, f"   Participants: {', '.join([f'u/{p}' for p in chain['participants'][:5]])}")
                if len(chain['participants']) > 5:
                    text.insert(tk.END, f" +{len(chain['participants']) - 5} more")
                text.insert(tk.END, f"\n")
                
                # Show progression
                for depth, (author, score, level, snippet) in enumerate(chain['chain']):
                    indent = "   " * (level + 1)
                    text.insert(tk.END, f"{indent}→ u/{author} (score: {score:+d})\n")
                
                text.insert(tk.END, "\n")
        
        text.config(state=tk.DISABLED)
        self.actions_status.config(text=f"✓ Analysis complete: {len(conflicts)} conflicts, {len(agreements)} agreements")

    
    def update_snapshot(self):
        """Save new snapshot"""
        try:
            post_id = self.update_post_var.get().split(' - ')[0]
            score = int(self.update_score.get())
            comments = int(self.update_comments.get())
            
            post = next((p for p in self.data['posts'] if p['post_id'] == post_id), None)
            if not post:
                messagebox.showerror("Error", "Post not found")
                return
            
            post['snapshots'].append({
                'timestamp': datetime.now().isoformat(),
                'score': score,
                'comments': comments
            })
            
            self.save_data()
            messagebox.showinfo("Success", f"Updated {post_id}")
            self.refresh_dashboard()
            self.on_update_post_select(None)
        
        except ValueError:
            messagebox.showerror("Error", "Invalid values (must be numbers)")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def setup_stats_tab(self, parent):
        """Statistics and trends tab"""
        self.stats_text = scrolledtext.ScrolledText(parent, bg='#2d2d2d', fg='#e0e0e0', font=('Consolas', 10))
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Refresh Stats", command=self.update_stats).pack(side=tk.LEFT, padx=5)
        
        self.update_stats()
    
    def update_stats(self):
        """Update and display statistics"""
        self.load_data()
        self.stats_text.delete('1.0', tk.END)
        
        if not self.data['posts']:
            self.stats_text.insert('1.0', "No posts tracked yet.")
            return
        
        stats = "ENGAGEMENT STATISTICS\n"
        stats += "=" * 80 + "\n\n"
        
        total_score = 0
        total_comments = 0
        trending_up = 0
        
        for post in self.data['posts']:
            latest = post['snapshots'][-1]
            first = post['snapshots'][0]
            
            score_change = latest['score'] - first['score']
            comment_change = latest['comments'] - first['comments']
            
            total_score += latest['score']
            total_comments += latest['comments']
            
            if score_change > 0:
                trending_up += 1
            
            status = "📈 TRENDING" if score_change > 0 else "📉 DECLINING" if score_change < 0 else "→ STABLE"
            
            stats += f"📌 {post['title'][:60]}\n"
            stats += f"   Status: {status}\n"
            stats += f"   Score: {first['score']} → {latest['score']} ({score_change:+d})\n"
            stats += f"   Comments: {first['comments']} → {latest['comments']} ({comment_change:+d})\n"
            stats += f"   Snapshots: {len(post['snapshots'])}\n\n"
        
        stats += "\n" + "=" * 80 + "\n"
        stats += "SUMMARY\n"
        stats += "=" * 80 + "\n"
        stats += f"Total Posts Tracked: {len(self.data['posts'])}\n"
        stats += f"Combined Score: {total_score}\n"
        stats += f"Combined Comments: {total_comments}\n"
        stats += f"Posts Trending Up: {trending_up}\n"
        
        self.stats_text.insert('1.0', stats)
    
    def export_summary(self):
        """Export tracking summary"""
        try:
            summary = {
                'username': self.data['username'],
                'exported_at': datetime.now().isoformat(),
                'posts': []
            }
            
            for post in self.data['posts']:
                latest = post['snapshots'][-1]
                first = post['snapshots'][0]
                
                summary['posts'].append({
                    'title': post['title'],
                    'subreddit': post['subreddit'],
                    'url': post['url'],
                    'current_score': latest['score'],
                    'current_comments': latest['comments'],
                    'initial_score': first['score'],
                    'initial_comments': first['comments'],
                    'score_change': latest['score'] - first['score'],
                    'comment_change': latest['comments'] - first['comments'],
                    'snapshots_taken': len(post['snapshots'])
                })
            
            filename = f"reddit_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Success", f"Exported to {filename}")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def setup_comments_tab(self, parent):
        """Tab for viewing and fetching comments"""
        top_frame = ttk.Frame(parent, padding=10)
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text="Select Post to Fetch Comments:", style='Header.TLabel').pack()
        
        # Post selector
        self.comment_post_var = tk.StringVar()
        self.comment_post_combo = ttk.Combobox(top_frame, textvariable=self.comment_post_var, width=70, state='readonly')
        self.comment_post_combo.pack(fill=tk.X, pady=5)
        self.comment_post_combo.bind('<<ComboboxSelected>>', self.on_comment_post_select)
        
        # Button frame
        button_frame = ttk.Frame(top_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.fetch_btn = ttk.Button(button_frame, text="Fetch Comments", command=self.fetch_comments)
        self.fetch_btn.pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(button_frame, text="Ready", foreground='#00d9ff')
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # Main container with left (tree) and right (details) panels
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Comments tree
        left_frame = ttk.LabelFrame(container, text="Comments", padding=5)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        columns = ('Author', 'Score', 'Depth', 'Preview')
        self.comments_tree = ttk.Treeview(left_frame, columns=columns, height=25)
        
        self.comments_tree.column('#0', width=40, minwidth=30)
        self.comments_tree.column('Author', width=100, minwidth=80)
        self.comments_tree.column('Score', width=60, minwidth=50)
        self.comments_tree.column('Depth', width=50, minwidth=40)
        self.comments_tree.column('Preview', width=250, minwidth=150)
        
        self.comments_tree.heading('#0', text='#')
        self.comments_tree.heading('Author', text='Author')
        self.comments_tree.heading('Score', text='Score')
        self.comments_tree.heading('Depth', text='Depth')
        self.comments_tree.heading('Preview', text='Comment Preview')
        
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.comments_tree.yview)
        self.comments_tree.configure(yscroll=scrollbar.set)
        
        self.comments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.comments_tree.bind('<<TreeviewSelect>>', self.on_comment_select)
        
        # Right panel - Comment details
        right_frame = ttk.LabelFrame(container, text="Comment Details", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.comment_details = scrolledtext.ScrolledText(right_frame, bg='#2d2d2d', fg='#e0e0e0', 
                                                         font=('Consolas', 9), width=40, height=30)
        self.comment_details.pack(fill=tk.BOTH, expand=True)
        
        # Statistics panel
        stats_frame = ttk.LabelFrame(parent, text="Comment Statistics", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.comment_stats_text = tk.Text(stats_frame, height=3, bg='#2d2d2d', fg='#e0e0e0', 
                                          font=('Consolas', 9))
        self.comment_stats_text.pack(fill=tk.X)
        
        self.refresh_comment_post_list()
    
    def refresh_comment_post_list(self):
        """Refresh post selector for comments"""
        self.load_data()
        posts = [f"{p['post_id']} - {p['title'][:40]}" for p in self.data['posts']]
        self.comment_post_combo['values'] = posts
    
    def on_comment_post_select(self, event):
        """Clear comments when post is selected"""
        self.comments_tree.delete(*self.comments_tree.get_children())
        self.comment_details.delete('1.0', tk.END)
        self.comment_stats_text.delete('1.0', tk.END)
    
    def fetch_comments(self):
        """Fetch comments from selected post in separate thread"""
        selection = self.comment_post_var.get()
        if not selection:
            messagebox.showerror("Error", "Select a post first")
            return
        
        post_id = selection.split(' - ')[0]
        post = next((p for p in self.data['posts'] if p['post_id'] == post_id), None)
        
        if not post:
            messagebox.showerror("Error", "Post not found")
            return
        
        # Disable button and show status
        self.fetch_btn.config(state=tk.DISABLED)
        self.status_label.config(text=f"Fetching... ({post_id})")
        self.root.update()
        
        # Fetch in thread to not freeze GUI
        thread = threading.Thread(target=self._fetch_comments_thread, args=(post, post_id))
        thread.daemon = True
        thread.start()
    
    def _fetch_comments_thread(self, post, post_id):
        """Background thread for fetching comments"""
        try:
            url = f"https://www.reddit.com/comments/{post_id}.json"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            comments = []
            
            def extract_comments(comment_list, depth=0):
                for item in comment_list:
                    if item['kind'] == 't1':
                        comment = item['data']
                        comments.append({
                            'id': comment['id'],
                            'author': comment.get('author', '[deleted]'),
                            'body': comment['body'],
                            'score': comment['score'],
                            'created': comment['created_utc'],
                            'depth': depth
                        })
                        
                        replies = comment.get('replies', '')
                        if replies and isinstance(replies, dict):
                            reply_children = replies.get('data', {}).get('children', [])
                            extract_comments(reply_children, depth + 1)
            
            if len(data) > 1:
                comment_children = data[1]['data']['children']
                extract_comments(comment_children)
            
            # Store in cache
            self.comments_data[post_id] = comments
            
            # Update GUI
            self.root.after(0, self._display_comments, comments, post_id)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to fetch: {str(e)}"))
        finally:
            self.root.after(0, self._reset_fetch_button)
    
    def _display_comments(self, comments, post_id):
        """Display fetched comments in tree"""
        self.comments_tree.delete(*self.comments_tree.get_children())
        
        # Group by depth for better visualization
        for i, comment in enumerate(comments, 1):
            indent = "  " * comment['depth']
            author = comment['author'][:15]
            score = comment['score']
            depth = comment['depth']
            preview = comment['body'][:50].replace('\n', ' ')
            
            self.comments_tree.insert('', 'end', iid=comment['id'],
                                     text=str(i),
                                     values=(author, score, depth, preview + '...'))
        
        # Update stats
        self._update_comment_stats(comments)
        
        self.status_label.config(text=f"✓ Loaded {len(comments)} comments")
    
    def _update_comment_stats(self, comments):
        """Update comment statistics"""
        if not comments:
            return
        
        top_comments = sorted(comments, key=lambda x: x['score'], reverse=True)[:3]
        depth_dist = {}
        
        for comment in comments:
            d = comment['depth']
            depth_dist[d] = depth_dist.get(d, 0) + 1
        
        stats = f"Total Comments: {len(comments)} | "
        stats += f"Top Score: {top_comments[0]['score']} | "
        stats += f"Avg Depth: {sum(c['depth'] for c in comments)/len(comments):.1f} | "
        stats += f"Max Depth: {max(c['depth'] for c in comments)}"
        
        self.comment_stats_text.delete('1.0', tk.END)
        self.comment_stats_text.insert('1.0', stats)
    
    def on_comment_select(self, event):
        """Display selected comment details"""
        selection = self.comments_tree.selection()
        if not selection:
            return
        
        comment_id = selection[0]
        
        # Find comment in cached data
        for post_comments in self.comments_data.values():
            comment = next((c for c in post_comments if c['id'] == comment_id), None)
            if comment:
                self.comment_details.delete('1.0', tk.END)
                
                details = f"""AUTHOR: u/{comment['author']}
SCORE: {comment['score']}
DEPTH: {comment['depth']}
TIME: {datetime.fromtimestamp(comment['created']).isoformat()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{comment['body']}
"""
                self.comment_details.insert('1.0', details)
                break
    
    def _reset_fetch_button(self):
        """Reset fetch button state"""
        self.fetch_btn.config(state=tk.NORMAL)
    
    def setup_user_posts_tab(self, parent):
        """Tab for exploring meaningful exchange partners and all Reddit info"""
        # Top control panel
        control_frame = ttk.LabelFrame(parent, text="Select Post & Analyze", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Post selection
        post_select_frame = ttk.Frame(control_frame)
        post_select_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(post_select_frame, text="Tracked Post:", foreground='#00d9ff').pack(side=tk.LEFT, padx=5)
        self.post_var = tk.StringVar()
        self.post_combo = ttk.Combobox(post_select_frame, textvariable=self.post_var, state='readonly', width=50)
        self.post_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(post_select_frame, text="🔄 Refresh & Analyze", 
                   command=self.refresh_exchange_partners).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="Users ranked by dialogue depth (back-and-forth conversations):", 
                  style='Header.TLabel').pack(anchor=tk.W, pady=(10, 5))
        
        self.users_text = tk.Text(control_frame, height=5, bg='#2d2d2d', fg='#e0e0e0', font=('Consolas', 9))
        self.users_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # View mode buttons
        button_frame = ttk.Frame(parent, padding=5)
        button_frame.pack(fill=tk.X, padx=10)
        
        ttk.Label(button_frame, text="View:", foreground='#00d9ff').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Posts", command=lambda: self.show_user_data('posts')).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Comments", command=lambda: self.show_user_data('comments')).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Profile", command=lambda: self.show_user_data('profile')).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Subreddits", command=lambda: self.show_user_data('subreddits')).pack(side=tk.LEFT, padx=2)
        
        # Main container - left (users tree) and right (content)
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel - Users
        left_frame = ttk.LabelFrame(container, text="Active Users", padding=5)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        
        self.users_tree = ttk.Treeview(left_frame, columns=('Exchanges',), height=20)
        self.users_tree.column('#0', width=150, minwidth=120)
        self.users_tree.column('Exchanges', width=80, minwidth=60)
        self.users_tree.heading('#0', text='Username')
        self.users_tree.heading('Exchanges', text='Dialogue')
        
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.users_tree.yview)
        self.users_tree.configure(yscroll=scrollbar.set)
        
        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.users_tree.bind('<<TreeviewSelect>>', self.on_user_select)
        
        # Right panel - Dynamic content
        right_frame = ttk.LabelFrame(container, text="User Details", padding=5)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.user_content_tree = ttk.Treeview(right_frame, columns=('Info',), height=20)
        self.user_content_tree.column('#0', width=300, minwidth=200)
        self.user_content_tree.column('Info', width=150, minwidth=100)
        self.user_content_tree.heading('#0', text='Item')
        self.user_content_tree.heading('Info', text='Details')
        
        scrollbar2 = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.user_content_tree.yview)
        self.user_content_tree.configure(yscroll=scrollbar2.set)
        
        self.user_content_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.user_content_tree.bind('<<TreeviewSelect>>', self.on_content_select)
        
        # Bottom panel - Details & preview
        details_frame = ttk.LabelFrame(parent, text="Details & Preview", padding=10)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.user_details = scrolledtext.ScrolledText(details_frame, bg='#2d2d2d', fg='#e0e0e0', 
                                                      height=10, font=('Consolas', 9))
        self.user_details.pack(fill=tk.BOTH, expand=True)
        
        # Initialize
        self.current_user = None
        self.current_view_type = 'posts'
        self.user_all_data = {}  # Cache all user data
        self.current_selected_post_id = None
        
        # NOW load data after all widgets are created
        self.update_post_list()
    
    def update_post_list(self):
        """Update the post combo box with tracked posts"""
        posts = self.data.get('posts', [])
        if not posts:
            self.post_combo['values'] = ['No tracked posts']
            self.post_var.set('No tracked posts')
            return
        
        post_options = [f"{p['post_id']} - {p.get('title', 'Untitled')[:40]}" for p in posts]
        self.post_combo['values'] = post_options
        if post_options:
            self.post_combo.current(0)
            self.refresh_exchange_partners()
    
    def refresh_exchange_partners(self):
        """Refresh exchange partner analysis for selected post"""
        post_text = self.post_var.get()
        if not post_text or post_text == 'No tracked posts':
            messagebox.showwarning("Warning", "No tracked posts to analyze")
            return
        
        post_id = post_text.split(' - ')[0]
        self.current_selected_post_id = post_id
        self.load_exchange_partners(post_id)
    
    def load_exchange_partners(self, post_id=None):
        """Load and display meaningful exchange partners from selected post"""
        if not post_id:
            # Default to first tracked post if none specified
            if self.data['posts']:
                post_id = self.data['posts'][0]['post_id']
            else:
                self.users_text.delete('1.0', tk.END)
                self.users_text.insert('1.0', "No tracked posts to analyze.")
                self.users_tree.delete(*self.users_tree.get_children())
                return
        
        try:
            self.users_text.delete('1.0', tk.END)
            self.users_text.insert('1.0', f"Fetching comments from post {post_id}...")
            self.root.update()
            
            # Fetch comments
            url = f"https://www.reddit.com/comments/{post_id}.json"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=15)
            data = response.json()
            
            comments = []
            def extract_comments(comment_list, depth=0, parent_author=None):
                for item in comment_list:
                    if item['kind'] == 't1':
                        comment = item['data']
                        author = comment.get('author', '[deleted]')
                        comments.append({
                            'id': comment['id'],
                            'author': author,
                            'body': comment['body'],
                            'created': comment['created_utc'],
                            'depth': depth,
                            'parent_author': parent_author
                        })
                        replies = comment.get('replies', '')
                        if replies and isinstance(replies, dict):
                            extract_comments(replies.get('data', {}).get('children', []), depth + 1, author)
            
            if len(data) > 1:
                extract_comments(data[1]['data']['children'])
            
            # Analyze meaningful exchanges
            from collections import defaultdict
            meaningful = defaultdict(int)
            comment_map = {c['id']: c for c in comments}
            your_username = self.data.get('username', 'Agitated_Age_2785')
            your_comments = {c['id']: c for c in comments if c['author'] == your_username}
            
            for other_comment in comments:
                if other_comment['parent_author'] == your_username and other_comment['author'] != your_username:
                    other_author = other_comment['author']
                    for follow_up in comments:
                        if (follow_up['parent_author'] == other_author and 
                            follow_up['author'] == your_username and
                            len(follow_up['body']) > 50 and
                            len(other_comment['body']) > 50):
                            meaningful[other_author] += 1
                            break
            
            # Filter for >3 exchanges
            active_users = {user: count for user, count in meaningful.items() 
                           if count > 3 and user != '[deleted]'}
            
            # Update users tree
            self.users_tree.delete(*self.users_tree.get_children())
            
            if not active_users:
                summary = f"Analyzing {len(comments)} comments...\n"
                summary += "━" * 50 + "\n"
                summary += f"Found {len(meaningful)} total dialogue partners\n"
                summary += f"Active partners (>3 exchanges): {len(active_users)}\n\n"
                if meaningful:
                    summary += "All partners found:\n"
                    for user, count in sorted(meaningful.items(), key=lambda x: x[1], reverse=True):
                        summary += f"  {user}: {count} exchanges\n"
            else:
                summary = "Users discovered through meaningful dialogue:\n"
                summary += "━" * 50 + "\n"
                
                for i, (user, count) in enumerate(sorted(active_users.items(), key=lambda x: x[1], reverse=True), 1):
                    summary += f"{i}. @{user}: {count} dialogue threads\n"
                    self.users_tree.insert('', 'end', iid=user, text=f"u/{user}", values=(count,))
            
            self.users_text.delete('1.0', tk.END)
            self.users_text.insert('1.0', summary)
        
        except Exception as e:
            error_msg = f"Failed to load exchange partners: {str(e)}"
            self.users_text.delete('1.0', tk.END)
            self.users_text.insert('1.0', error_msg)
            messagebox.showerror("Error", error_msg)
    
    def on_user_select(self, event):
        """Show user's data when selected"""
        selection = self.users_tree.selection()
        if not selection:
            return
        
        self.current_user = selection[0]
        self.show_user_data(self.current_view_type)
    
    def show_user_data(self, data_type):
        """Fetch and display user data (posts/comments/profile/subreddits)"""
        if not self.current_user:
            messagebox.showerror("Error", "Select a user first")
            return
        
        self.current_view_type = data_type
        self.user_content_tree.delete(*self.user_content_tree.get_children())
        self.user_details.delete('1.0', tk.END)
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            username = self.current_user
            
            if data_type == 'posts':
                url = f"https://www.reddit.com/user/{username}/posts.json"
                response = requests.get(url, headers=headers, timeout=15)
                if response.status_code == 404:
                    url = f"https://www.reddit.com/user/{username}/submitted.json"
                    response = requests.get(url, headers=headers, timeout=15)
                
                data = response.json()
                posts = []
                for item in data.get('data', {}).get('children', []):
                    if item['kind'] == 't3':
                        post = item['data']
                        posts.append({
                            'id': post['id'],
                            'title': post['title'],
                            'subreddit': post['subreddit'],
                            'score': post['score'],
                            'comments': post['num_comments'],
                            'created': post['created_utc'],
                            'selftext': post.get('selftext', ''),
                            'url': post['url']
                        })
                
                self.user_all_data['posts'] = {p['id']: p for p in posts}
                for i, post in enumerate(posts[:30], 1):
                    preview = f"r/{post['subreddit']} • ↑{post['score']} • 💬{post['comments']}"
                    self.user_content_tree.insert('', 'end', iid=post['id'],
                                                 text=post['title'][:70] + '...',
                                                 values=(preview,))
            
            elif data_type == 'comments':
                url = f"https://www.reddit.com/user/{username}/comments.json"
                response = requests.get(url, headers=headers, timeout=15)
                
                data = response.json()
                comments = []
                for item in data.get('data', {}).get('children', []):
                    if item['kind'] == 't1':
                        comment = item['data']
                        comments.append({
                            'id': comment['id'],
                            'body': comment['body'],
                            'score': comment['score'],
                            'parent': comment.get('parent_id', ''),
                            'created': comment['created_utc'],
                            'subreddit': comment['subreddit']
                        })
                
                self.user_all_data['comments'] = {c['id']: c for c in comments}
                for i, comment in enumerate(comments[:30], 1):
                    preview = f"r/{comment['subreddit']} • ↑{comment['score']}"
                    self.user_content_tree.insert('', 'end', iid=comment['id'],
                                                 text=comment['body'][:70] + '...',
                                                 values=(preview,))
            
            elif data_type == 'profile':
                url = f"https://www.reddit.com/user/{username}/about.json"
                response = requests.get(url, headers=headers, timeout=15)
                profile = response.json()['data']
                
                self.user_all_data['profile'] = profile
                
                profile_info = f"""USERNAME: u/{profile['name']}
KARMA: {profile['link_karma']:,} posts | {profile['comment_karma']:,} comments
TOTAL KARMA: {profile['link_karma'] + profile['comment_karma']:,}
CREATED: {datetime.fromtimestamp(profile['created']).isoformat()}
GOLD: {'Yes' if profile.get('is_gold', False) else 'No'}
MODERATOR: {'Yes' if profile.get('is_moderator', False) else 'No'}
VERIFIED EMAIL: {'Yes' if profile.get('verified', False) else 'No'}

BIO: {profile.get('subreddit', {}).get('public_description', 'No bio')}
"""
                self.user_details.insert('1.0', profile_info)
            
            elif data_type == 'subreddits':
                url = f"https://www.reddit.com/user/{username}/posts.json"
                response = requests.get(url, headers=headers, timeout=15)
                if response.status_code == 404:
                    url = f"https://www.reddit.com/user/{username}/submitted.json"
                    response = requests.get(url, headers=headers, timeout=15)
                
                data = response.json()
                subreddit_stats = {}
                
                for item in data.get('data', {}).get('children', []):
                    if item['kind'] == 't3':
                        sub = item['data']['subreddit']
                        subreddit_stats[sub] = subreddit_stats.get(sub, 0) + 1
                
                sorted_subs = sorted(subreddit_stats.items(), key=lambda x: x[1], reverse=True)
                
                for subreddit, count in sorted_subs[:30]:
                    self.user_content_tree.insert('', 'end', iid=subreddit,
                                                 text=f"r/{subreddit}",
                                                 values=(f"{count} posts",))
                
                stats = f"\n".join([f"r/{sub}: {count} posts" for sub, count in sorted_subs[:15]])
                summary = f"""ACTIVE SUBREDDITS
({'═' * 50})

Top 15 communities by post count:

{stats}

Total unique subreddits: {len(sorted_subs)}"""
                self.user_details.insert('1.0', summary)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch {data_type}: {str(e)}")
    
    def on_content_select(self, event):
        """Show selected content details"""
        selection = self.user_content_tree.selection()
        if not selection:
            return
        
        item_id = selection[0]
        
        if self.current_view_type == 'posts':
            post = self.user_all_data.get('posts', {}).get(item_id)
            if post:
                details = f"""TITLE: {post['title']}

SUBREDDIT: r/{post['subreddit']}
SCORE: {post['score']:,}
COMMENTS: {post['comments']:,}
CREATED: {datetime.fromtimestamp(post['created']).isoformat()}
URL: {post['url']}

{'═' * 60}

{post['selftext'][:1000]}
"""
                self.user_details.delete('1.0', tk.END)
                self.user_details.insert('1.0', details)
        
        elif self.current_view_type == 'comments':
            comment = self.user_all_data.get('comments', {}).get(item_id)
            if comment:
                details = f"""SUBREDDIT: r/{comment['subreddit']}
SCORE: {comment['score']:,}
CREATED: {datetime.fromtimestamp(comment['created']).isoformat()}

{'═' * 60}

{comment['body'][:1000]}
"""
                self.user_details.delete('1.0', tk.END)
                self.user_details.insert('1.0', details)

def main():
    root = tk.Tk()
    app = RedditTrackerGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
