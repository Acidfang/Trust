import json
from pathlib import Path
from collections import Counter, defaultdict

# Get all file types
mds = list(Path('.').glob('*.md'))
py_files = list(Path('.').glob('*.py'))
json_files = list(Path('.').glob('*.json'))

print('=== MARKDOWN FILES (Content Check) ===')
for md in sorted(mds)[:10]:
    with open(md) as f:
        lines = f.readlines()
    first_title = next((l.strip() for l in lines if l.startswith('#')), 'NO TITLE')
    size_kb = md.stat().st_size / 1024
    print(f'{md.name[:50]}: {size_kb:.0f}KB')
    print(f'  ↳ {first_title[:80]}')

print('\n=== PYTHON FILES ===')
for py in sorted(py_files):
    size = py.stat().st_size
    print(f'{py.name}: {size} bytes')

print('\n=== JSON FILES ===')
for jf in sorted(json_files):
    size_kb = jf.stat().st_size / 1024
    print(f'{jf.name}: {size_kb:.1f}KB')

print('\n=== CHAT CONVERSATIONS (First 20) ===')
if Path('conversations.json').exists():
    with open('conversations.json') as f:
        convs = json.load(f)
    
    for i, c in enumerate(convs[:20], 1):
        title = c.get('title', '???')[:70]
        msg_count = len(c.get('messages', []))
        print(f'[{i:2d}] {title}... ({msg_count} msgs)')

print('\n=== SUBDIRECTORIES ===')
dirs = [d for d in Path('.').iterdir() if d.is_dir()]
for d in sorted(dirs):
    file_count = len(list(d.rglob('*')))
    print(f'  {d.name}: {file_count} items')
