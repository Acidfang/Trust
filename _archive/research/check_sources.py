import json

with open('gemini_consolidated_database.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('Source file references in consolidated database:')
if data.get('conversations'):
    for i, conv in enumerate(data['conversations'][:5]):
        fname = conv.get('file_name', 'N/A')
        fpath = conv.get('file_path', 'N/A')
        parsed = conv.get('parsed_at', 'N/A')
        print(f'{i+1}. File: {fname}')
        print(f'   Path: {fpath}')
        print(f'   Parsed: {parsed}')
        print()
