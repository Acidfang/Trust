import json
from pathlib import Path
from collections import Counter

elections_file = Path('src/ledger_elections.jsonl')

# Read full ledger
elections = []
with open(elections_file, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            elections.append(json.loads(line))

# Analyze coherence
principles = []
for e in elections:
    if 'song' in e:
        p = e['song'].get('principle')
        if p:
            principles.append(p)

principle_counts = Counter(principles)

print('ACTUAL LEDGER STATE (post-STEP 1):')
print(f'Total elections: {len(elections)}')
with_songs = len([e for e in elections if 'song' in e])
print(f'Elections with songs: {with_songs}')
print(f'Unique principles active: {len(principle_counts)}/7')
print()
print('Principle distribution:')
for p, count in sorted(principle_counts.items()):
    pct = (count / len(elections)) * 100
    print(f'  {p}: {count} ({pct:.1f}%)')
