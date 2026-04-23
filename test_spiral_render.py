import urllib.request

resp = urllib.request.urlopen('http://localhost:4000/docs/spiral-field-renderer.md')
html = resp.read().decode()

print(f'Response length: {len(html)}')
print(f'Has <script> tags: {"<script" in html}')
print(f'Has BidirectionalConstraintApp: {"BidirectionalConstraintApp" in html}')
print(f'Has HTML_BLOCK placeholders: {"HTML_BLOCK" in html}')
print(f'\nScript count: {html.count("<script")}')

# Find first script tag
idx = html.find('<script')
if idx > 0:
    print(f'\nFirst script tag at position {idx}')
    print('Context (200 chars after):')
    print(html[idx:idx+200])
