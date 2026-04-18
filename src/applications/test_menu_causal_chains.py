"""
Test Suite: Menu Causal Chains Fixed

Verifies that all menu navigation and sidebar toggle operations
are now spec-driven (reverse causality complete).
"""

from ledger_query import LedgerQuery
import json

def test_toggle_operator():
    """Test __toggle__ operator works in update_app_state."""
    lq = LedgerQuery(".")

    # Start with sidebar expanded
    lq.update_app_state({'sidebar_collapsed': False})
    assert lq.app_state['sidebar_collapsed'] == False, "Start expanded"

    # Apply __toggle__ operator
    lq.update_app_state({'sidebar_collapsed': '__toggle__'})
    assert lq.app_state['sidebar_collapsed'] == True, "After toggle: collapsed"

    # Toggle again
    lq.update_app_state({'sidebar_collapsed': '__toggle__'})
    assert lq.app_state['sidebar_collapsed'] == False, "After second toggle: expanded"

    print("[PASS] Toggle operator works")


def test_toggle_button_spec():
    """Test toggle button spec is correct."""
    lq = LedgerQuery(".")
    btn = lq.get_button('btn:toggle-sidebar')

    assert btn is not None, "Toggle button exists"
    assert 'on_click' in btn, "Button has on_click"

    on_click = btn['on_click']
    assert 'elections' in on_click, "Button spec has elections"
    assert 'state_updates' in on_click, "Button spec has state_updates"

    state_updates = on_click['state_updates']
    assert state_updates.get('sidebar_collapsed') == '__toggle__', "Spec has __toggle__ operator"
    assert state_updates.get('last_action') == 'toggle_sidebar', "Spec has last_action"

    print("[PASS] Toggle button spec is correct")


def test_settings_button_spec():
    """Test settings button spec is corrected format."""
    lq = LedgerQuery(".")
    btn = lq.get_button('btn:settings')

    assert btn is not None, "Settings button exists"
    assert 'on_click' in btn, "Button has on_click"

    on_click = btn['on_click']
    assert 'elections' in on_click, "Button spec uses elections (not old target/action format)"
    assert 'state_updates' in on_click, "Button spec has state_updates"

    state_updates = on_click['state_updates']
    assert state_updates.get('current_view') == 'settings_sync', "Spec navigates to settings_sync"
    assert 'navigate:settings_sync' in state_updates.get('last_action', ''), "Spec has last_action"

    print("[PASS] Settings button spec is correct")


def test_toggle_position_removed():
    """Test toggle button position removed from ledger."""
    lq = LedgerQuery(".")

    # Toggle button should NOT be in positioned_nodes ledger
    toggle_node = lq.positioned_nodes.get('node:btn:toggle-sidebar')
    assert toggle_node is None, "Toggle button position removed from ledger"

    print("[PASS] Toggle button position correctly removed from ledger")


def test_button_click_flow():
    """Test button click executes spec correctly."""
    lq = LedgerQuery(".")

    # Initial state
    initial_collapsed = lq.app_state.get('sidebar_collapsed', False)
    initial_view = lq.app_state.get('current_view')

    # Click toggle button (without printing the Unicode label)
    # This internally reads the spec and applies __toggle__
    button_spec = lq.get_button('btn:toggle-sidebar')
    on_click = button_spec['on_click']
    state_updates = on_click['state_updates']

    lq.update_app_state(state_updates)

    # Verify toggle happened
    new_collapsed = lq.app_state['sidebar_collapsed']
    assert new_collapsed == (not initial_collapsed), "Toggle inverted sidebar_collapsed"
    assert lq.app_state.get('last_action') == 'toggle_sidebar', "last_action recorded"

    print("[PASS] Button click executes spec correctly")


def run_all_tests():
    """Run all tests."""
    tests = [
        ("Toggle operator in update_app_state", test_toggle_operator),
        ("Toggle button spec correct", test_toggle_button_spec),
        ("Settings button spec correct", test_settings_button_spec),
        ("Toggle position removed from ledger", test_toggle_position_removed),
        ("Button click executes spec", test_button_click_flow),
    ]

    passed = 0
    failed = 0

    print("=" * 70)
    print("Menu Causal Chains Fix - Test Suite")
    print("=" * 70)

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {name}: {e}")
            failed += 1

    print("=" * 70)
    print(f"RESULTS: {passed} PASSED, {failed} FAILED")
    print("=" * 70)

    if failed == 0:
        print("Causal chains FIXED - all tests pass!")
    else:
        print("Causal chains INCOMPLETE - some tests failed")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
