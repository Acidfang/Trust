import requests
import json

url = 'https://share.google/aimode/l4zX8GJdxDmfKTmn8'

headers_list = [
    {
        'User-Agent': 'curl/7.89.1',
        'Accept': 'application/json'
    },
    {
        'User-Agent': 'curl/7.89.1',
        'Accept': '*/*'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    },
]

for i, headers in enumerate(headers_list):
    try:
        print(f"\nRequest {i+1} with headers: {headers}")
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'unknown')}")
        print(f"Size: {len(response.text)} bytes")
        print(f"Final URL: {response.url[:100]}")
        
        # Check if it's JSON
        if response.text.strip().startswith('{'):
            try:
                data = json.loads(response.text)
                print(f"JSON keys: {list(data.keys())[:5]}")
                with open(f'c:\\Determined\\raw_response_{i}.json', 'w') as f:
                    json.dump(data, f, indent=2)
            except:
                print(f"Content preview: {response.text[:200]}")
        elif 'conversation' in response.text.lower():
            print("Contains 'conversation'")
            with open(f'c:\\Determined\\raw_response_{i}.txt', 'w') as f:
                f.write(response.text)
        elif len(response.text) < 5000:
            print(f"Content: {response.text[:300]}")
            
    except Exception as e:
        print(f"Error: {e}")
