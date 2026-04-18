#!/usr/bin/env python3
import urllib.request
import json

frame = json.loads(urllib.request.urlopen('http://127.0.0.1:8081/api/frame').read())

print("=" * 90)
print("MENU FRAME RENDERING CHECK")
print("=" * 90)

print(f"\n✓ Current View: {frame['view']}")
print(f"✓ Nodes in Frame: {len(frame.get('nodes', []))}")

print("\n" + "-" * 90)
print("MENU STRUCTURE (What kernel is sending):")
print("-" * 90)

for i, n in enumerate(frame.get('nodes', [])):
    print(f"\n[Node {i+1}]")
    print(f"  ID:    {n['id']}")
    print(f"  Area:  {n['area']}")
    print(f"  Type:  {n['type']}")
    if n['type'] == 'WIDGET':
        payload = n.get('payload', {})
        print(f"  Label: {payload.get('label', 'N/A')}")
        print(f"  Value: {payload.get('value', 'N/A')}")
    elif n['type'] == 'TEXT':
        payload = n.get('payload', {})
        content = payload.get('content', '')[:80]
        print(f"  Content: {content}")

print("\n" + "=" * 90)
print("ANALYSIS")
print("=" * 90)

buttons = [n for n in frame.get('nodes', []) if n.get('type') == 'WIDGET']
print(f"\n✓ Buttons in menu: {len(buttons)}")
for b in buttons:
    print(f"  - {b['payload']['label']}")

print("\n✓ Expected 7 buttons: ", "PASS" if len(buttons) >= 7 else "FAIL - Only " + str(len(buttons)))
