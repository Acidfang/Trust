from pathlib import Path

dirs = [
    'src',
    'src/ledgers',
    'src/applications',
    'src/applications/ledgers'
]

for d in dirs:
    path = Path(d) / 'ledger_elections.jsonl'
    if path.exists():
        count = sum(1 for line in open(path) if line.strip())
        print(f'{d}: {count} elections')
    else:
        print(f'{d}: NOT FOUND')
