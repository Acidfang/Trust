# Troubleshooting Quick Reference

## Common Issues and Solutions

### Issue 1: Clicks Not Executing in Target Application

**Symptoms:**
- Click is intercepted (shows in log)
- Overlay hides/shows briefly
- Target application doesn't respond

**Check Logs For:**
```
[Overlay] ExecuteUnderlyingClick: SendInput DOWN result = 0
```

**Solutions:**

| Problem | Solution |
|---------|----------|
| SendInput returns 0 | Run as Administrator |
| Target is elevated app | Run Trust as Administrator |
| Overlay not hiding | Increase delay: `overlayWindow.SetClickExecutionDelay(200)` |
| Wrong coordinates | Check DPI awareness in App.manifest |
| Target not focused | Ensure target window is visible, not minimized |

**Quick Fix:**
1. Run Trust.exe as Administrator
2. In MainWindow.ShowOverlay(), add:
   ```csharp
   _overlayWindow.SetClickExecutionDelay(150);
   ```

---

### Issue 2: Overlay Not Showing

**Symptoms:**
- "Show Overlay" button clicked
- No visible overlay
- No error in logs

**Check Logs For:**
```
[Overlay] OverlayWindow: Constructor started
[Overlay] OverlayWindow: Initialization complete
[Overlay] OverlayWindow_Loaded: Window loaded event fired
```

**Solutions:**

| Problem | Solution |
|---------|----------|
| No logs at all | Check event subscription: `_overlayWindow.OnLog += ...` |
| Logs show initialization | Overlay may be too transparent, press F9 to make it visible |
| Screen size = 0x0 | Check `SystemParameters.PrimaryScreenWidth/Height` |
| Multi-monitor issue | Check which monitor overlay appears on |

**Quick Fix:**
1. Press F9 to enter interception mode (turns red)
2. Check Windows display settings for primary monitor

---

### Issue 3: Click-Through Not Working

**Symptoms:**
- Overlay blocks all clicks
- Can't interact with applications below
- Even when not in interception mode

**Check Logs For:**
```
[Overlay] SetClickThrough: Click-through enabled, new style = 0x...
```

**Solutions:**

| Problem | Solution |
|---------|----------|
| Style not changing | Check `GetWindowLong`/`SetWindowLong` return values |
| Style correct but still blocking | Restart application |
| WS_EX_TRANSPARENT not set | Style should include 0x00000020 flag |

**Quick Fix:**
1. Press F9 twice (toggle interception on/off)
2. Check log for style values
3. Style should be `0x0C0A0020` for click-through

---

### Issue 4: Timeline Not Showing Events

**Symptoms:**
- Press F10, timeline panel appears
- No events in list or graph
- Clicks are being intercepted

**Check Logs For:**
```
[Overlay] MouseDown: Click processed, now executing underlying action
```

**Solutions:**

| Problem | Solution |
|---------|----------|
| Timeline panel null | Check `InitializeTimelinePanel()` was called |
| Clicks not intercepted | Ensure in interception mode (F9) |
| ProcessInterceptForTimeline exception | Check `StructuralIdentityEngine` initialization |
| Events added but not visible | Check panel Visibility property |

**Quick Fix:**
1. Ensure in interception mode (overlay should be red)
2. Timeline panel must be visible (press F10)
3. Click somewhere on screen
4. Check timeline panel for new event

---

### Issue 5: High Latency Between Click and Execution

**Symptoms:**
- Clicks work but delayed
- 500ms+ between click and action
- Logs show long execution times

**Check Logs For:**
```
[Overlay] ExecuteUnderlyingClick: ========== STARTING CLICK EXECUTION ==========
...
[Overlay] ExecuteUnderlyingClick: ========== CLICK EXECUTION COMPLETE ==========
```

**Solutions:**

| Problem | Solution |
|---------|----------|
| Default delay too high | Reduce delay: `SetClickExecutionDelay(75)` |
| Thread.Sleep too long | Check code for excessive delays |
| Processing bottleneck | Optimize `ProcessInterceptedData` |
| Remote desktop | Increase delay, latency expected |

**Quick Fix:**
```csharp
// In MainWindow.ShowOverlay():
_overlayWindow.SetClickExecutionDelay(75); // Faster response
```

---

### Issue 6: Overlay Crashes or Freezes

**Symptoms:**
- Application stops responding
- Overlay window frozen
- No new logs appearing

**Check Logs For:**
```
[Overlay] ExecuteUnderlyingClick: ========== ERROR OCCURRED ==========
[Overlay] ExecuteUnderlyingClick: Exception type: ...
```

**Solutions:**

| Problem | Solution |
|---------|----------|
| Exception in click execution | Check exception details in log |
| Deadlock in event handler | Ensure no blocking operations on UI thread |
| Memory leak | Check event handler subscriptions |
| Infinite loop | Check transform pipeline logic |

**Quick Fix:**
1. Press ESC to stop interception
2. Close overlay
3. Check MainWindow log for errors
4. Restart application

---

### Issue 7: Multi-Monitor Issues

**Symptoms:**
- Overlay only on one monitor
- Clicks work on primary but not secondary
- Wrong coordinates on secondary monitor

**Check Logs For:**
```
[Overlay] InitializeOverlay: Screen size = ...
[Overlay] ExecuteUnderlyingClick: Virtual screen = (X, Y, WxH)
```

**Solutions:**

| Problem | Solution |
|---------|----------|
| Overlay only on primary | Use `SystemParameters.VirtualScreenWidth/Height` |
| Coordinates offset | Check virtual screen origin (may be negative) |
| Different DPI per monitor | Enable DPI awareness in App.manifest |
| Secondary monitor not detected | Check Windows display settings |

**Quick Fix:**
```csharp
// In InitializeOverlay():
Left = SystemParameters.VirtualScreenLeft;
Top = SystemParameters.VirtualScreenTop;
Width = SystemParameters.VirtualScreenWidth;
Height = SystemParameters.VirtualScreenHeight;
```

---

### Issue 8: Timeline Shows All Black Bricks

**Symptoms:**
- Every event is red (BLACK_BRICK)
- Entropy values all > 7.8
- No canonical patterns detected

**Check Logs For:**
```
Transform: BLACK_BRICK
Entropy: 7.95
```

**Solutions:**

| Problem | Solution |
|---------|----------|
| Entropy threshold too high | Lower threshold: Slide to 6.5-7.0 |
| Data truly random | Expected for certain types of data |
| Transforms not applying | Check transform pipeline |
| Wrong data encoding | Verify UTF8 encoding of click data |

**Quick Fix:**
1. Open Timeline Inspector (F10)
2. Adjust "Entropy Threshold" slider to 7.0
3. Should see more GREEN (IDENTITY) events

---

### Issue 9: No Logs Appearing in MainWindow

**Symptoms:**
- Actions happening but no logs
- Output window empty
- Events firing but not logged

**Check Logs For:**
(Nothing - that's the problem!)

**Solutions:**

| Problem | Solution |
|---------|----------|
| OnLog not subscribed | Check: `_overlayWindow.OnLog += OverlayWindow_OnLog;` |
| LogMessage method broken | Verify Dispatcher.Invoke |
| OutputTextBox null | Check XAML bindings |
| Exception in log handler | Wrap in try-catch |

**Quick Fix:**
```csharp
// In MainWindow.ShowOverlay():
_overlayWindow.OnLog += OverlayWindow_OnLog;

// Verify handler exists:
private void OverlayWindow_OnLog(object? sender, string message)
{
    LogMessage(message);
}
```

---

### Issue 10: Optimization Not Triggering

**Symptoms:**
- Same pattern clicked multiple times
- No "OPTIMIZABLE" events
- Timeline shows frequency > 1

**Check Logs For:**
```
? OPTIMIZABLE PATTERN DETECTED
```

**Solutions:**

| Problem | Solution |
|---------|----------|
| Auto-optimize disabled | Check Timeline Inspector checkbox |
| Event handler not subscribed | Verify `OnOptimizableDetected` subscription |
| Frequency tracking broken | Check `_structuralIdFrequency` dictionary |
| Structural IDs not matching | Check transform consistency |

**Quick Fix:**
1. Open Timeline Inspector (F10)
2. Ensure "Auto-Optimize Redundant Patterns" is checked
3. Click same location twice
4. Should see yellow border on events + log message

---

## Diagnostic Commands

### Enable Maximum Logging
```csharp
// Add to MainWindow constructor:
_executionEngine.EnableVerboseLogging(true);
```

### Check Window Styles
```csharp
// Log current window style:
var hwnd = new WindowInteropHelper(_overlayWindow).Handle;
var style = GetWindowLong(hwnd, GWL_EXSTYLE);
LogMessage($"Current style: 0x{style:X8}");
```

### Verify Screen Dimensions
```csharp
LogMessage($"Primary: {SystemParameters.PrimaryScreenWidth}x{SystemParameters.PrimaryScreenHeight}");
LogMessage($"Virtual: {SystemParameters.VirtualScreenWidth}x{SystemParameters.VirtualScreenHeight}");
LogMessage($"Origin: ({SystemParameters.VirtualScreenLeft}, {SystemParameters.VirtualScreenTop})");
```

### Test Click Execution Manually
```csharp
// In MainWindow, add button:
private void TestClickButton_Click(object sender, RoutedEventArgs e)
{
    _overlayWindow?.ExecuteUnderlyingClick(new Point(500, 500));
}
```

---

## Log Patterns to Know

### Successful Click Execution
```
[Overlay] ExecuteUnderlyingClick: ========== STARTING CLICK EXECUTION ==========
[Overlay] ExecuteUnderlyingClick: Overlay position = (350, 420)
[Overlay] ExecuteUnderlyingClick: SendInput DOWN result = 1
[Overlay] ExecuteUnderlyingClick: SendInput UP result = 1
[Overlay] ExecuteUnderlyingClick: ========== CLICK EXECUTION COMPLETE ==========
```

### Click-Through Mode Active
```
[Overlay] SetClickThrough: Click-through enabled, new style = 0x0C0A0020
[Overlay] MouseDown: Click passed through (click-through mode active)
```

### Interception Mode Active
```
[Overlay] === StartInterception: Activating interception mode ===
[Overlay] StartInterception: Interception mode active - overlay will capture clicks
[Overlay] MouseDown: Button=Left, ClickThrough=False, Intercepting=True
```

### Error Pattern
```
[Overlay] ExecuteUnderlyingClick: ========== ERROR OCCURRED ==========
[Overlay] ExecuteUnderlyingClick: Exception type: ...
[Overlay] ExecuteUnderlyingClick: Error message: ...
```

---

## Quick Fixes by Symptom

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| Nothing happens when clicking overlay | Not in interception mode | Press F9 |
| Clicks intercepted but not executed | SendInput failing | Run as Admin |
| Overlay invisible | Too transparent | Press F9 to make red |
| Timeline empty | Timeline not visible or no clicks | Press F10, then click |
| All events are black bricks | Entropy threshold too high | Lower to 7.0 |
| Slow click response | Delay too high | `SetClickExecutionDelay(75)` |
| No logs | Event not subscribed | Check `OnLog` subscription |
| Optimization not working | Auto-optimize off | Check Timeline checkbox |
| Multi-monitor issues | Using primary screen only | Use virtual screen dimensions |
| App crashes | Exception in handler | Check log for stack trace |

---

## Emergency Recovery

### Application Frozen
1. Press `Ctrl+Alt+Del`
2. Task Manager ? End Task "Trust.exe"
3. Restart application

### Overlay Won't Close
1. Press ESC
2. Alt+F4
3. Task Manager ? End Task

### Logs Not Visible
1. Click "Clear Log"
2. Click "Run Test" to generate logs
3. If still empty, restart application

---

## Getting Help

### Information to Provide
1. **Full log output** from MainWindow
2. **Windows version** and DPI scaling settings
3. **Administrator status** (elevated or not)
4. **Multi-monitor setup** (if applicable)
5. **Target application** you're trying to click
6. **Specific error messages** or exception types

### Reproduce the Issue
1. Start with fresh application
2. Document each step taken
3. Note when issue occurs
4. Capture full log from start to error

This quick reference covers the most common issues and their solutions. For detailed architecture and event flow, see `PROJECT_OPERATION_GUIDE.md`. For detailed logging information, see `OVERLAY_LOGGING_GUIDE.md`.
