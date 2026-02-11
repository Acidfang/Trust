# Overlay Window Logging and Click Execution Guide

## Overview

The OverlayWindow has been enhanced with comprehensive logging capabilities and improved click execution functionality. This guide explains how the logging works and how clicks are intercepted and executed.

## Logging Features

### Logging Architecture

All overlay operations are logged through the `OnLog` event, which is subscribed to by the MainWindow. This provides centralized logging in the main application output window.

### Log Categories

#### 1. **Initialization Logging**
```
[Overlay] OverlayWindow: Constructor started
[Overlay] InitializeOverlay: Setting up overlay window
[Overlay] InitializeOverlay: Screen size = 1920x1080
[Overlay] InitializeOverlay: Event handlers attached
[Overlay] OverlayWindow: Initialization complete
```

#### 2. **Window State Logging**
```
[Overlay] OverlayWindow_Loaded: Window loaded event fired
[Overlay] SetClickThrough: Setting click-through mode to True
[Overlay] SetClickThrough: Current style = 0x080A0000
[Overlay] SetClickThrough: Click-through enabled, new style = 0x0C0A0020
```

#### 3. **Mouse Event Logging**
```
[Overlay] MouseDown: Button=Left, ClickThrough=False, Intercepting=True
[Overlay] MouseDown: Intercepted at (350, 420)
[Overlay] MouseDown: Click processed, now executing underlying action
[Overlay] MouseUp: Button=Left, ClickThrough=False
```

#### 4. **Keyboard Event Logging**
```
[Overlay] KeyDown: Key=F9, Intercepting=False
[Overlay] KeyDown: F9 pressed - toggling interception
[Overlay] KeyDown: Key=F10, Intercepting=True
[Overlay] KeyDown: F10 pressed - toggling timeline panel
```

#### 5. **Interception Mode Logging**
```
[Overlay] === StartInterception: Activating interception mode ===
[Overlay] SetClickThrough: Setting click-through mode to False
[Overlay] StartInterception: Interception mode active - overlay will capture clicks
[Overlay] === StopInterception: Deactivating interception mode ===
```

#### 6. **Click Execution Detailed Logging**
```
[Overlay] ExecuteUnderlyingClick: ========== STARTING CLICK EXECUTION ==========
[Overlay] ExecuteUnderlyingClick: Overlay position = (350, 420)
[Overlay] ExecuteUnderlyingClick: Original cursor position = (350, 420)
[Overlay] ExecuteUnderlyingClick: Target screen coordinates = (350, 420)
[Overlay] ExecuteUnderlyingClick: Virtual screen = (0, 0, 1920x1080)
[Overlay] ExecuteUnderlyingClick: Window at position before hide = 0x12345678 (Overlay = 0x87654321)
[Overlay] ExecuteUnderlyingClick: Hiding overlay...
[Overlay] ExecuteUnderlyingClick: Window at position after hide = 0x12345678
[Overlay] ExecuteUnderlyingClick: Moving cursor to (350, 420)
[Overlay] ExecuteUnderlyingClick: SetCursorPos result = True
[Overlay] ExecuteUnderlyingClick: Actual cursor position after move = (350, 420)
[Overlay] ExecuteUnderlyingClick: Sending mouse DOWN event via SendInput
[Overlay] ExecuteUnderlyingClick: SendInput DOWN result = 1 (1 = success)
[Overlay] ExecuteUnderlyingClick: Sending mouse UP event via SendInput
[Overlay] ExecuteUnderlyingClick: SendInput UP result = 1 (1 = success)
[Overlay] ExecuteUnderlyingClick: Restoring overlay visibility
[Overlay] ExecuteUnderlyingClick: ========== CLICK EXECUTION COMPLETE ==========
[Overlay] ExecuteUnderlyingClick: Summary - Inputs sent: 2/2, Target: 0x12345678, Position: (350, 420)
```

## Click Execution Flow

### How Click Interception and Execution Works

1. **Click Detection**
   - User clicks on the overlay while in interception mode
   - `OverlayWindow_MouseDown` event is triggered
   - Click position is captured relative to overlay

2. **Click Processing**
   - Click data is processed through the Invariant Identity Engine
   - Structural ID is computed
   - Timeline event is created (if timeline panel is visible)
   - Event callbacks are invoked

3. **Click Execution**
   - `ExecuteUnderlyingClick` method is called
   - Current cursor position is saved
   - Overlay position is converted to screen coordinates
   - Multi-monitor virtual screen dimensions are retrieved

4. **Overlay Hiding**
   - Overlay visibility is set to `Collapsed`
   - Dispatcher is invoked to ensure render completes
   - Configurable delay (default 100ms) allows full hiding

5. **Target Window Detection**
   - `WindowFromPoint` API identifies the window under the click position
   - Window handle is logged for diagnostics

6. **Mouse Input Injection**
   - Cursor is moved to target position using `SetCursorPos`
   - `SendInput` API injects mouse DOWN event
   - 50ms delay between down and up events
   - `SendInput` API injects mouse UP event

7. **Overlay Restoration**
   - Configurable delay (default 100ms) before restoring overlay
   - Overlay visibility is set back to `Visible`
   - Summary information is logged

### Multi-Monitor Support

The system supports multi-monitor configurations:

```csharp
int virtualScreenLeft = GetSystemMetrics(SM_XVIRTUALSCREEN);   // -1920 for left monitor
int virtualScreenTop = GetSystemMetrics(SM_YVIRTUALSCREEN);     // 0 typically
int virtualScreenWidth = GetSystemMetrics(SM_CXVIRTUALSCREEN); // Total width across monitors
int virtualScreenHeight = GetSystemMetrics(SM_CYVIRTUALSCREEN); // Total height
```

This ensures clicks work correctly on:
- Primary monitor
- Secondary monitors (left, right, above, below)
- Different DPI scaling configurations
- Different resolutions per monitor

## API Used for Click Execution

### SendInput API (Modern Approach)

The overlay now uses the `SendInput` API instead of the deprecated `mouse_event`:

**Advantages:**
- More reliable and compatible with modern Windows
- Properly respects UIPI (User Interface Privilege Isolation)
- Works with elevated applications (when overlay is also elevated)
- Better timing control
- Standard Microsoft recommended approach

**Structure:**
```csharp
INPUT input = new INPUT
{
    Type = INPUT_MOUSE,
    Data = new MOUSEKEYBDHARDWAREINPUT
    {
        Mouse = new MOUSEINPUT
        {
            dx = 0,
            dy = 0,
            mouseData = 0,
            dwFlags = MOUSEEVENTF_LEFTDOWN,
            time = 0,
            dwExtraInfo = IntPtr.Zero
        }
    }
};

uint result = SendInput(1, new[] { input }, Marshal.SizeOf(typeof(INPUT)));
```

## Configuration Options

### Click Execution Delay

You can adjust the delay used for overlay hiding/showing:

```csharp
overlayWindow.SetClickExecutionDelay(150); // Set to 150ms
```

**Delay Range:** 50ms - 500ms (default: 100ms)

**Use Cases:**
- **Lower delay (50-75ms):** Fast response, may occasionally have timing issues
- **Default (100ms):** Balanced, works for most scenarios
- **Higher delay (150-250ms):** More reliable on slower systems, better for remote desktop
- **Very high (300-500ms):** For debugging, visible separation between intercept and execute

## Troubleshooting with Logs

### Problem: Clicks Not Executing

**Check These Log Entries:**

1. **Overlay not hiding properly:**
```
[Overlay] ExecuteUnderlyingClick: Window at position after hide = 0x87654321
[Overlay] ExecuteUnderlyingClick: WARNING - Overlay still detected at position
```
**Solution:** Increase click execution delay

2. **No window found:**
```
[Overlay] ExecuteUnderlyingClick: WARNING - No window found at target position
```
**Solution:** Ensure there's an actual window at the click location

3. **SendInput failure:**
```
[Overlay] ExecuteUnderlyingClick: SendInput DOWN result = 0 (1 = success)
```
**Solution:** 
- Run application as administrator
- Check if target application is elevated
- Verify no other input blocking software is running

4. **Wrong coordinates:**
```
[Overlay] ExecuteUnderlyingClick: Target screen coordinates = (-500, 200)
```
**Solution:** Check DPI awareness settings in App.manifest

### Problem: Click-Through Not Working

**Check These Log Entries:**

```
[Overlay] SetClickThrough: Current style = 0x080A0000
[Overlay] SetClickThrough: Click-through enabled, new style = 0x0C0A0020
```

**Window Style Flags:**
- `WS_EX_TRANSPARENT` (0x00000020): Allows clicks to pass through
- `WS_EX_LAYERED` (0x00080000): Required for transparency
- `WS_EX_NOACTIVATE` (0x08000000): Prevents window from stealing focus

If style is not being set correctly, the overlay may intercept all clicks even in click-through mode.

## Event Flow Diagram

```
User Clicks Screen
       ?
   [Overlay receives MouseDown]
       ?
   [Check: _isClickThrough?]
       ? No (Intercepting)
   [Log click details]
       ?
   [Invoke OnInterceptClick event] ? [MainWindow logs to output]
       ?
   [Process for Timeline]
       ?
   [ExecuteUnderlyingClick]
       ?
   [Log: Starting execution]
       ?
   [Hide overlay (Visibility.Collapsed)]
       ?
   [Wait for render + delay]
       ?
   [Detect target window]
       ?
   [Move cursor to position]
       ?
   [SendInput: Mouse DOWN]
       ?
   [Wait 50ms]
       ?
   [SendInput: Mouse UP]
       ?
   [Wait delay]
       ?
   [Show overlay (Visibility.Visible)]
       ?
   [Log: Execution complete]
       ?
   [Action executed in target app]
```

## Best Practices

### 1. Monitor Logs During Testing
Watch the MainWindow output for any warnings or errors during click execution.

### 2. Test Different Scenarios
- Click on desktop
- Click on various applications
- Click on buttons, textboxes, menus
- Click near screen edges
- Click on secondary monitors

### 3. Adjust Timing if Needed
If clicks aren't registering consistently:
```csharp
overlayWindow.SetClickExecutionDelay(150); // Increase delay
```

### 4. Run as Administrator for Elevated Apps
If you need to click on elevated applications (UAC prompts, Task Manager, etc.):
- Run the Trust application as administrator
- Logs will show if SendInput fails due to privilege issues

### 5. Check Window Focus
Some applications only respond to clicks when focused. The overlay uses `WS_EX_NOACTIVATE` to avoid stealing focus, but the target window must still be visible.

## Performance Considerations

### Timing Breakdown
- Overlay hide: ~100ms (configurable)
- Cursor move: ~5ms
- SendInput DOWN: <1ms
- Delay: 50ms
- SendInput UP: <1ms
- Overlay restore: ~100ms (configurable)

**Total:** ~260ms per click (adjustable via delay configuration)

### Optimization Tips
- Lower delays work well on fast, local machines
- Increase delays for remote desktop or slower systems
- Timeline processing happens concurrently with execution
- Logging is async via events (minimal performance impact)

## Security Considerations

### UIPI (User Interface Privilege Isolation)
Windows UIPI prevents lower-privileged processes from sending input to higher-privileged processes.

**Impact:**
- Non-admin overlay cannot click on admin applications
- Solution: Run Trust as administrator

### Input Injection Detection
Some applications (games, security software) may detect injected input.

**Mitigation:**
- SendInput is legitimate Windows API
- Used by automation tools, accessibility software
- Should work with most applications
- Some anti-cheat systems may still block it

## Future Enhancements

### Possible Improvements
1. **Right-click and middle-click support**
2. **Keyboard input injection**
3. **Drag-and-drop simulation**
4. **Configurable timing per application**
5. **Click replay from timeline**
6. **Macro recording capabilities**

## Summary

The enhanced OverlayWindow provides:
- ? Comprehensive diagnostic logging
- ? Reliable click execution with SendInput
- ? Multi-monitor support
- ? Configurable timing
- ? Error handling and reporting
- ? Integration with Invariant Identity Engine
- ? Timeline inspection capabilities

All operations are fully logged, making it easy to diagnose issues and understand the system's behavior.
