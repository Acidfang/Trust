import json

# Load the unified master timeline
try:
    with open('c:\\Determined\\UNIFIED_MASTER_TIMELINE.json', 'r') as f:
        data = json.load(f)
    
    # Search for Θ or CORP or oxygen-rich references
    results = []
    for msg in data.get('messages', []):
        content = (msg.get('content', '') or '').lower()
        if any(term in content for term in ['theta', 'corp', 'oxygen', 'hydrogen-limited', 'peroxide', 'h2o2', 'dioxid']):
            results.append({
                'timestamp': msg.get('timestamp'),
                'role': msg.get('role'),
                'platform': msg.get('platform'),
                'content_preview': (msg.get('content', '') or '')[:300]
            })
    
    print(f"Found {len(results)} messages mentioning similar concepts")
    
    if results:
        print("\n=== FIRST 5 MATCHES ===")
        for r in results[:5]:
            print(f"\n{r['timestamp']} ({r['platform']}) - {r['role']}")
            print(f"  {r['content_preview'][:200]}")
    else:
        print("No direct matches found")
        
        # Try exact Θ symbol
        theta_count = 0
        for msg in data.get('messages', []):
            if 'Θ' in (msg.get('content', '') or ''):
                theta_count += 1
                print(f"\nFound Θ symbol in {msg['role']} message ({msg['platform']})")
                print((msg.get('content', '') or '')[:200])
        
        if theta_count == 0:
            print("\nNo Θ symbol found in unified timeline")
            print("The share link document might be NEW or from a separate source")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
