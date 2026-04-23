import urllib.request

resp = urllib.request.urlopen('http://localhost:4000/wiki/docs/spiral-field-renderer.md')
html = resp.read().decode()

has_block = 'HTML_BLOCK' in html
has_script = '<script' in html

print(f'HTML_BLOCK placeholders found: {has_block}')
print(f'Actual <script> tags found: {has_script}')

if has_block:
    idx = html.find('HTML_BLOCK')
    print(f'\nPlaceholder at position {idx}')
    print('Context:')
    print(html[max(0, idx-200):idx+300])

if has_script:
    idx = html.find('<script')
    print(f'\nScript tag at position {idx}')
    count = html.count('<script')
    print(f'Total <script> tags: {count}')
