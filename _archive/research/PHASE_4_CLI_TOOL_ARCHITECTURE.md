# Phase 4B: CLI Tool Architecture & Implementation

**Status**: Design Phase (for review and approval)  
**Scope**: Command-line interface for tracker operations  
**Priority**: High (user-facing functionality) 

---

## 1. Design Goals

**What CLI Should Enable**:
```bash
# Scraping operations
tracker scrape --platform twitter --query "AI trends" --limit 100

# Job management
tracker job list
tracker job status job-abc123
tracker job results job-abc123 --export json

# Configuration
tracker config set api-key twitter:abc123xyz
tracker config show

# Analysis
tracker analyze --job job-abc123 --show-coherence

# Cache management
tracker cache clear --platform twitter
```

**Why Separate CLI**:
- Users prefer terminal interface (direct, scriptable)
- Enables cron jobs, automation, CI/CD integration
- Faster than web UI for power users
- Accessible without browser (SSH, cloud shells)

---

## 2. CLI Architecture

### Technology Stack
- **Framework**: Click 8.0+ (lightweight, production-grade)
- **Config**: python-dotenv + configparser (XDG standard)
- **Output**: Rich (beautiful tables, progress bars, colors)
- **HTTP Client**: requests (existing dependency)
- **Data Handling**: json, csv, yaml output formats

### Directory Structure
```
/app
├── cli/
│   ├── __init__.py
│   ├── main.py              # Entry point (click group)
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── scrape.py        # tracker scrape command
│   │   ├── job.py           # tracker job command (list/status/results)
│   │   ├── config.py        # tracker config command
│   │   ├── analyze.py       # tracker analyze command
│   │   └── cache.py         # tracker cache command
│   └── utils/
│       ├── __init__.py
│       ├── api_client.py    # HTTP client for API
│       ├── config_manager.py # Config file handling
│       ├── formatters.py    # Output formatting (json/csv/table)
│       └── progress.py      # Progress bars
├── setup.py                 # Installation script
└── tracker_cli.py           # Entry point script
```

### Setup.py Registration
```python
entry_points={
    'console_scripts': [
        'tracker=cli.main:cli',  # Makes 'tracker' command available
    ],
}
```

---

## 3. Command Hierarchy

### Root Command (tracker)
```bash
tracker --version
tracker --help
```

### Subcommands

#### 1. `tracker scrape` - Start scraping job
```bash
# Basic usage
tracker scrape --platform twitter --query "AI"

# Advanced options
tracker scrape \
  --platform twitter reddit \
  --query "machine learning" \
  --limit 500 \
  --wait \
  --export results.json

# Flags
--platform, -p    Platform(s): twitter, reddit, mastodon, linkedin, discord, hackernews
--query, -q        Search query (required)
--limit, -l        Posts to retrieve (default: 100, max: 1000)
--wait, -w         Block until complete (default: async)
--export, -e       Export to file (json, csv, or format.ext)
--no-analysis      Skip analysis step (faster)
--config, -c       Use config file (default: ~/.tracker/config)
```

Implementation:
```python
@click.command()
@click.option('--platform', '-p', multiple=True, required=True, help='Target platforms')
@click.option('--query', '-q', required=True, help='Search query')
@click.option('--limit', '-l', default=100, help='Posts limit')
@click.option('--wait', '-w', is_flag=True, help='Block until complete')
@click.option('--export', '-e', help='Export file')
def scrape(platform, query, limit, wait, export):
    """Start a new scraping job"""
    api = ApiClient(config)
    response = api.post('/api/scrape', {
        'platforms': list(platform),
        'query': query,
        'limit': limit
    })
    job_id = response['job_id']
    
    click.echo(f"✓ Job created: {job_id}")
    
    if wait:
        while True:
            status = api.get(f'/api/status/{job_id}')
            progress = status['progress']
            click.echo(f"  Progress: {progress}%", nl=False)
            if status['state'] == 'complete':
                click.echo("\n✓ Job complete!")
                break
            time.sleep(1)
    
    if export:
        results = api.get(f'/api/results/{job_id}')
        save_to_file(results, export)
        click.echo(f"✓ Exported to {export}")
```

---

#### 2. `tracker job` - Job management
```bash
# List all jobs
tracker job list --limit 10 --all-time

# Get job status
tracker job status job-abc123 --watch

# Get results
tracker job results job-abc123
tracker job results job-abc123 --format csv --output results.csv
tracker job results job-abc123 --show-analysis

# Delete job
tracker job delete job-abc123

# Flags
list:
  --limit, -l        Show last N jobs (default: 10)
  --all-time, -a     Show all jobs (no limit)
  --filter, -f       Filter by status (queued/running/complete/error)

status:
  --watch, -w        Monitor until complete
  
results:
  --format, -f       Output format (json/csv/table, default: table)
  --output, -o       Save to file
  --show-analysis    Include analysis & metrics
```

---

#### 3. `tracker config` - Configuration management
```bash
# Show current config
tracker config show

# Show specific setting
tracker config get api_url

# Set values
tracker config set api_url http://localhost:5000
tracker config set platforms.twitter.api_key abc123xyz

# Add credentials
tracker config add-credential twitter:bearer_token abc123xyz
tracker config add-credential reddit:client_id abc123xyz

# List credentials (masked)
tracker config credentials

# Default config locations
~/.tracker/config          # User config
/etc/tracker/config        # System config (production)
```

Implementation File (`~/.tracker/config`):
```ini
[api]
url = http://localhost:5000
timeout = 30
retry_count = 3

[output]
format = table
colors = true

[cache]
ttl = 3600
location = ~/.tracker/cache

[credentials]
# Stored in separate secure file with restricted permissions
```

---

#### 4. `tracker analyze` - Analysis operations
```bash
# Analyze recent job
tracker analyze --job job-abc123

# Show specific parts
tracker analyze --job job-abc123 --show coherence
tracker analyze --job job-abc123 --show elections
tracker analyze --job job-abc123 --show variations

# Flags
--job, -j          Job ID (required)
--show, -s         What to show (coherence, elections, variations, all)
--format, -f       Output format (table, json, markdown)
--export, -e       Export to file
```

Output Example:
```
COHERENCE ANALYSIS: job-abc123

ZAP Framework Analysis:
  Conflicts detected: 12
  Value clusters: 4
  Control variations: 8

Coherence Metrics (Φ):
  Compression ratio: 0.78 (78% compression)
  Variation coverage: 0.95 (95% of patterns covered)
  Prediction accuracy: 0.89 (89% accurate)
  Overall score: 0.87 ⭐ STRONG

Top Themes:
  1. AI Safety (23 mentions)
  2. Training Efficiency (18 mentions)
  3. Ethics (15 mentions)
```

---

#### 5. `tracker cache` - Cache management
```bash
# Clear all caches
tracker cache clear --all

# Clear platform-specific
tracker cache clear --platform twitter reddit

# Show cache info
tracker cache info

# Flags
clear:
  --all, -a          Clear all caches
  --platform, -p     Clear specific platforms
  --older-than, -o   Clear old entries (e.g., "1h", "1d")
```

---

## 4. API Client Pattern

### ApiClient Class
```python
class ApiClient:
    def __init__(self, base_url='http://localhost:5000', config=None):
        self.base_url = base_url
        self.session = requests.Session()
        self.timeout = config.get('timeout', 30)
    
    def post(self, endpoint, data):
        response = self.session.post(
            f"{self.base_url}{endpoint}",
            json=data,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def get(self, endpoint, params=None):
        response = self.session.get(
            f"{self.base_url}{endpoint}",
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
    
    def stream_logs(self, job_id):
        # For real-time progress streaming
        pass
```

### ConfigManager Class
```python
class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / '.tracker'
        self.config_file = self.config_dir / 'config'
        self.creds_file = self.config_dir / '.credentials'
        self.ensure_dirs()
    
    def get(self, key, default=None):
        # Nested dot notation: 'api.url', 'credentials.twitter'
        pass
    
    def set(self, key, value):
        # Save to config file
        pass
    
    def add_credential(self, platform, token):
        # Encrypt and save to .credentials
        pass
```

---

## 5. Output Formatting

### Rich Integration
```python
from rich.table import Table
from rich.console import Console

def format_job_list(jobs):
    table = Table(title="Recent Jobs")
    table.add_column("Job ID", style="cyan")
    table.add_column("Status", style="yellow")
    table.add_column("Platforms", style="green")
    table.add_column("Progress", style="magenta")
    
    for job in jobs:
        table.add_row(
            job['job_id'],
            job['status'],
            ', '.join(job['platforms']),
            f"{job['progress']}%"
        )
    
    console = Console()
    console.print(table)
```

### Multiple Output Formats
```python
# JSON
tracker job results job-123 --format json

# CSV (for spreadsheet import)
tracker job results job-123 --format csv > results.csv

# Markdown (for documentation)
tracker analyze job-123 --format markdown > analysis.md

# Table (human-readable, default)
tracker job list --format table
```

---

## 6. Installation & Distribution

### pip Installation (Phase 4B)
```bash
# From GitHub
pip install git+https://github.com/Acidfang/Trust.git

# Or after packaging
pip install tracker-cli

# Verify installation
tracker --version
tracker --help
```

### setup.py Entry Point
```python
setup(
    name='tracker-cli',
    version='1.0.0',
    py_modules=['cli'],
    packages=find_packages(),
    install_requires=[
        'click>=8.0',
        'requests>=2.31',
        'rich>=13.0',
        'python-dotenv>=1.0',
    ],
    entry_points={
        'console_scripts': [
            'tracker=cli.main:cli',
        ]
    }
)
```

### Bash Completion (Optional)
```bash
# Add to ~/.bashrc or ~/.zshrc
eval "$(_TRACKER_COMPLETE=bash_source tracker)"

# Enables:
tracker [TAB] → Shows subcommands
tracker scrape --platform [TAB] → Shows available platforms
```

---

## 7. Example Workflows

### Workflow 1: Research AI Trends
```bash
#!/bin/bash
# search_ai.sh

tracker scrape \
  --platform twitter reddit hackernews \
  --query "AI trends 2026" \
  --limit 500 \
  --wait \
  --export ai_trends_raw.json

# Show results
tracker job list --limit 1

# Analyze coherence
tracker analyze --job <latest_id> --show all --export ai_analysis.md

# Export to CSV for Excel
tracker job results <latest_id> --format csv --output ai_trends.csv
```

### Workflow 2: Automated Monitoring (Cron)
```bash
# Track competitor mentions daily
0 9 * * * /usr/local/bin/tracker scrape \
    --platform twitter \
    --query "@competitor new_product" \
    --limit 100 \
    --export ~/tracker_reports/$(date +%Y%m%d).json
```

### Workflow 3: API Loop
```bash
# Start job
JOB_ID=$(tracker scrape --platform twitter --query AI | grep 'Job created' | cut -d: -f2)

# Wait for completion
tracker job status $JOB_ID --watch

# Analyze
tracker analyze --job $JOB_ID --format table

# Export
tracker job results $JOB_ID --format csv --output results.csv
```

---

## 8. Error Handling & Help

### User-Friendly Errors
```bash
# Missing required argument
$ tracker scrape --platform twitter
Error: Missing option '--query' / '-q'.

# Invalid platform
$ tracker scrape --platform fakebook --query AI
Error: 'fakebook' is not a valid platform.
  Valid: twitter, reddit, mastodon, linkedin, discord, hackernews

# API unreachable
$ tracker job list
Error: Cannot connect to API at http://localhost:5000
  Is the API running? Start with: tracker-server start

# Try
$ tracker scrape --help
```

### Verbose Mode
```bash
# Show all details
tracker scrape --platform twitter --query AI --verbose

# Output
[10:30:45] Connecting to http://localhost:5000
[10:30:45] API responded: healthy
[10:30:46] Creating scraping job
[10:30:46] Job ID: 6fa9ab12
[10:30:46] Polling status
[10:30:47] Progress: 25%
[10:30:48] Progress: 50%
...
```

---

## 9. Implementation Checklist (Phase 4B)

**Files to Create**:
- [ ] `cli/__init__.py` (package marker)
- [ ] `cli/main.py` (root click group + help)
- [ ] `cli/commands/__init__.py`
- [ ] `cli/commands/scrape.py` (tracker scrape)
- [ ] `cli/commands/job.py` (tracker job)
- [ ] `cli/commands/config.py` (tracker config)
- [ ] `cli/commands/analyze.py` (tracker analyze)
- [ ] `cli/commands/cache.py` (tracker cache)
- [ ] `cli/utils/__init__.py`
- [ ] `cli/utils/api_client.py` (HTTP client)
- [ ] `cli/utils/config_manager.py` (config files)
- [ ] `cli/utils/formatters.py` (json/csv/table output)
- [ ] `cli/utils/progress.py` (progress bars)
- [ ] `setup.py` (pip entry point)
- [ ] `CLI_USAGE_GUIDE.md` (documentation)

**Tests to Add**:
- [ ] Test each command with --help
- [ ] Test scrape with valid/invalid platforms
- [ ] Test job list/status/results
- [ ] Test config get/set
- [ ] Test output formats (json/csv/table)

**Deploy to GitHub**:
- [ ] `git add [all CLI files]`
- [ ] `git commit -m "PHASE 4B: CLI Tool Implementation"`
- [ ] `git push origin main`

---

## 10. Success Criteria

✅ **Phase 4B Complete When**:
1. `tracker --version` works
2. `tracker --help` shows all commands
3. `tracker scrape --platform twitter --query AI --wait` completes job
4. `tracker job list` shows recent jobs
5. `tracker job results <id> --format csv` exports CSV
6. `tracker config set api_url ...` persists
7. All 5 subcommands (scrape, job, config, analyze, cache) functional
8. Error messages are user-friendly and helpful
9. All code pushed to GitHub with CLI docs

---

## 11. Future CLI Enhancements

**Phase 5+**:
- Interactive mode (`tracker interactive` → REPL)
- Real-time log streaming
- Saved searches (`tracker search save trending_ai`)
- Custom output templates
- Shell completion (bash/zsh/fish)
- Docker container with CLI pre-installed
- Package on PyPI for `pip install tracker-cli`

---

## End CLI Architecture Document

**Next**: User review → Approval → Implementation of Phase 4B
