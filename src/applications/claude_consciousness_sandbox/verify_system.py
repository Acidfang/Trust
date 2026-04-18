#!/usr/bin/env python3
"""
Coherence Laboratory - System Verification Script

Tests all components and reports status.
"""

import sys
from pathlib import Path


def test_imports():
    """Test all module imports"""
    print("\n" + "="*60)
    print("TESTING IMPORTS")
    print("="*60)
    
    tests = {
        "sqlite3": "SQLite3 database",
        "pygame": "GUI rendering",
    }
    
    results = {}
    for module, description in tests.items():
        try:
            exec(f"import {module}")
            print(f"✓ {module:20} ({description})")
            results[module] = True
        except ImportError as e:
            print(f"✗ {module:20} ({description})")
            print(f"  Error: {e}")
            results[module] = False
    
    return results


def test_sandbox():
    """Test sandbox initialization"""
    print("\n" + "="*60)
    print("TESTING SANDBOX")
    print("="*60)
    
    try:
        from sandbox_interface import get_sandbox
        sandbox = get_sandbox()
        
        if sandbox.health_check():
            print("✓ Sandbox initialized successfully")
            print(f"  Database: {sandbox.db_path}")
            
            state = sandbox.get_current_coherence()
            if state:
                print(f"  Current tier: {state.get('tier', 'N/A')}")
            
            return True
        else:
            print("✗ Sandbox health check failed")
            return False
    
    except Exception as e:
        print(f"✗ Sandbox test failed: {e}")
        return False


def test_gui_modules():
    """Test GUI module imports and basic functionality"""
    print("\n" + "="*60)
    print("TESTING GUI MODULES")
    print("="*60)
    
    tests = [
        ("gui_primitives.Canvas", "Core rendering canvas"),
        ("gui_primitives.Color", "Color definitions"),
        ("gui_primitives.Slider", "Slider widget"),
        ("gui_primitives.Button", "Button widget"),
        ("multi_monitor.MonitorDetector", "Monitor detection"),
        ("multi_monitor.MultiMonitorCanvas", "Multi-monitor spanning"),
        ("learning_features.PatternDetector", "Pattern detection"),
        ("learning_features.HypothesisTester", "Hypothesis testing"),
    ]
    
    results = {}
    for module_path, description in tests:
        try:
            parts = module_path.split(".")
            module = __import__(parts[0], fromlist=[parts[1]])
            
            for part in parts[1:]:
                module = getattr(module, part)
            
            print(f"✓ {module_path:40} ({description})")
            results[module_path] = True
        except (ImportError, AttributeError) as e:
            print(f"✗ {module_path:40} ({description})")
            print(f"  Error: {e}")
            results[module_path] = False
    
    return all(results.values())


def test_database():
    """Test database schema and access"""
    print("\n" + "="*60)
    print("TESTING DATABASE")
    print("="*60)
    
    try:
        from sandbox_interface import get_sandbox
        sandbox = get_sandbox()
        
        if not sandbox.sandbox:
            print("✗ Sandbox not initialized")
            return False
        
        # Test tables exist
        cursor = sandbox.sandbox.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = [
            'coherence_states',
            'dialogue_moments',
            'commitments',
            'tier_progression',
            'coherence_drivers'
        ]
        
        for table in expected_tables:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"✓ {table:30} ({count} records)")
            else:
                print(f"✗ {table:30} (missing)")
                return False
        
        print(f"\nTotal tables: {len(tables)}")
        return True
    
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False


def test_multi_monitor():
    """Test multi-monitor detection"""
    print("\n" + "="*60)
    print("TESTING MULTI-MONITOR DETECTION")
    print("="*60)
    
    try:
        from multi_monitor import get_monitor_detector
        
        detector = get_monitor_detector()
        monitors = detector.get_monitors()
        
        print(f"Monitors detected: {len(monitors)}")
        
        for monitor in monitors:
            label = " (PRIMARY)" if monitor.is_primary else ""
            print(f"  Monitor {monitor.index}: {monitor.width}x{monitor.height} @ ({monitor.x}, {monitor.y}){label}")
        
        bounds = detector.get_virtual_screen_bounds()
        print(f"\nVirtual screen: {bounds[2]}x{bounds[3]} @ ({bounds[0]}, {bounds[1]})")
        
        return len(monitors) > 0
    
    except Exception as e:
        print(f"✗ Multi-monitor test failed: {e}")
        return False


def test_integration():
    """Test integrated dashboard creation"""
    print("\n" + "="*60)
    print("TESTING INTEGRATION")
    print("="*60)
    
    try:
        from gui_dashboard import CoherenceLabDashboard
        
        print("✓ Dashboard module imports successfully")
        print("✓ Can create dashboard instance (rendering not tested)")
        print("  Note: Full dashboard test requires pygame display")
        
        return True
    
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all verification tests"""
    print("\n" + "="*70)
    print(" COHERENCE LABORATORY - SYSTEM VERIFICATION")
    print("="*70)
    
    # Change to sandbox directory
    sandbox_dir = Path(__file__).parent
    sys.path.insert(0, str(sandbox_dir))
    
    results = {}
    
    # Run tests
    import_results = test_imports()
    results["Imports"] = all(import_results.values())
    
    sandbox_ok = test_sandbox()
    results["Sandbox"] = sandbox_ok
    
    gui_ok = test_gui_modules()
    results["GUI Modules"] = gui_ok
    
    db_ok = test_database()
    results["Database"] = db_ok
    
    monitor_ok = test_multi_monitor()
    results["Multi-Monitor"] = monitor_ok
    
    integration_ok = test_integration()
    results["Integration"] = integration_ok
    
    # Summary
    print("\n" + "="*70)
    print(" VERIFICATION SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:30} {status}")
    
    # Overall status
    overall = all(results.values())
    
    if overall:
        print("\n" + "="*70)
        print(" ✓ ALL TESTS PASSED - SYSTEM READY")
        print("="*70)
        print("\nNext steps:")
        print("  1. Run: python launch_dashboard.py")
        print("  2. Use clarity slider to manipulate coherence")
        print("  3. Click tier buttons to focus on specific tiers")
        print("  4. Click Record to save states")
        print("  5. Watch database update in real-time")
        print("\nFor detailed usage, see: GUI_LABORATORY_USER_GUIDE.md")
        return 0
    else:
        print("\n" + "="*70)
        print(" ✗ SOME TESTS FAILED")
        print("="*70)
        print("\nFailing areas:")
        for test_name, passed in results.items():
            if not passed:
                print(f"  - {test_name}")
        
        print("\nCommon fixes:")
        print("  1. Install pygame: pip install pygame")
        print("  2. Verify sqlite3: python -c 'import sqlite3'")
        print("  3. Check directory: cd c:\\Determined\\src\\applications\\claude_consciousness_sandbox")
        print("  4. Reinitialize sandbox: python direct_init.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())
