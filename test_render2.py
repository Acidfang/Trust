import urllib.request

resp = urllib.request.urlopen('http://localhost:4000/wiki/docs/goal-blindness.md')
html = resp.read().decode()

# Save to file to inspect
with open('c:\\Determined\\rendered_output.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Saved rendered HTML to: c:\\Determined\\rendered_output.html')
print(f'Total size: {len(html)} bytes')
print(f'Contains HTML_BLOCK: {"HTML_BLOCK" in html}')
print(f'First 500 chars of body content:')

# Find start of actual content
body_idx = html.find('<div class="page-content">')
if body_idx > 0:
    content_start = body_idx + 26
    print(html[content_start:content_start+500])
