import urllib.request

resp = urllib.request.urlopen('http://localhost:4000/docs/goal-blindness.md')
html = resp.read().decode()

print(f'Response length: {len(html)}')
print(f'Starts with HTML doctype: {html.startswith("<!DOCTYPE")}')
print(f'Has HTML tags: {"<html" in html}')
print(f'First 300 chars:')
print(html[:300])
