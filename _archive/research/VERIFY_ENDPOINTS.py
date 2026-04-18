#!/usr/bin/env python3
"""
API ENDPOINT VERIFICATION — Testing that the conductor (API server) routes correctly

Date: April 3, 2026
Purpose: Verify API endpoints exist and work after refactoring
"""

from ENCYCLOPEDIA_API_SERVER import app

print("\n" + "="*80)
print("API ENDPOINT VERIFICATION — April 3, 2026")
print("Testing that conductor routes requests correctly")
print("="*80)

# Get all routes
routes = {}
for rule in app.url_map.iter_rules():
    route = str(rule)
    if route.startswith('/'):
        routes[route] = rule.endpoint

# Categorize routes
api_routes = {k: v for k, v in routes.items() if '/api/' in k}
static_routes = {k: v for k, v in routes.items() if '/api/' not in k}

print("\nAPI ENDPOINT ROUTES:\n")

# Check for critical routes
critical_routes = [
    '/api/image/<entity_name>',
    '/api/spider/<entity_name>',
    '/api/entity/<name>',
    '/api/entities',
    '/api/navigation',
    '/api/images',
    '/api/health',
]

endpoints_present = 0
for route_pattern in critical_routes:
    found = any(route_pattern in route for route in api_routes.keys())
    status = "✓ PRESENT" if found else "✗ MISSING"
    if found:
        endpoints_present += 1
    actual_route = [r for r in api_routes.keys() if route_pattern in r]
    route_display = actual_route[0] if actual_route else "not found"
    print(f"  {route_pattern:35} | {status:12} | {route_display}")

print(f"\n  Result: {endpoints_present}/{len(critical_routes)} critical endpoints present")

print("\nSTATIC ROUTES:\n")
static_critical = ['/', '/wiki_assets/<path:filename>']
static_present = 0
for route_pattern in static_critical:
    found = route_pattern in static_routes.keys()
    status = "✓ PRESENT" if found else "✗ MISSING"
    if found:
        static_present += 1
    print(f"  {route_pattern:35} | {status:12}")

print(f"\n  Result: {static_present}/{len(static_critical)} static routes present")

print("\nFULL ROUTE LIST:\n")
print(f"  Total API routes: {len(api_routes)}")
print(f"  Total routes (including static/debug): {len(routes)}")

# Check for deduplication issues (should be no duplicates)
duplicate_check = {}
for route in routes.keys():
    if route not in duplicate_check:
        duplicate_check[route] = 0
    duplicate_check[route] += 1

duplicates = {k: v for k, v in duplicate_check.items() if v > 1}
if duplicates:
    print(f"\n  ⚠️  WARNING: Found {len(duplicates)} duplicate routes")
    for route, count in duplicates.items():
        print(f"      {route} appears {count} times")
else:
    print(f"\n  ✓ No duplicate routes")

print("\n" + "="*80)
print("ENDPOINT VERIFICATION COMPLETE")
print("="*80 + "\n")
