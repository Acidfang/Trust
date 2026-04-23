import urllib.request

resp = urllib.request.urlopen('http://localhost:4000/wiki/docs/goal-blindness.md')
html = resp.read().decode()

# Check if it's actually HTML or raw markdown
is_html = html.startswith('<!DOCTYPE')
has_frontmatter = html.startswith('---')

print(f'Response starts with <!DOCTYPE: {is_html}')
print(f'Response starts with ---: {has_frontmatter}')
print(f'Response length: {len(html)} bytes')
print(f'\nFirst 300 characters:')
print(html[:300])
