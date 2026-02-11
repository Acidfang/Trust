# Trust - Complete Project Operation Guide

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Event Flow](#event-flow)
3. [Component Interactions](#component-interactions)
4. [User Actions and Responses](#user-actions-and-responses)
5. [Logging and Diagnostics](#logging-and-diagnostics)
6. [Operational Modes](#operational-modes)

## System Architecture

### Core Components

```
???????????????????
?   MainWindow    ? ? Main UI, Control Center, Log Display
???????????????????
         ?
         ???????????????????
         ?                 ?
    ????????????     ?????????????????
    ?Execution ?     ? OverlayWindow ? ? Transparent overlay
    ?  Engine  ?     ?????????????????
    ????????????          ?
         ?                ????????????????
         ?                ?              ?
    ???????????????  ????????????? ??????????????
    ?  Invariant  ?  ? Timeline  ? ?   Click    ?
    ?   Ledger    ?  ?   Panel   ? ?  Executor  ?
    ???????????????  ????????????? ??????????????
         ?
    ?????????????????
    ?  Transform    ?
    ?   Pipeline    ?
    ?????????????????
```

### Component Responsibilities

| Component | Responsibility |
|-----------|---------------|
| **MainWindow** | User interface, button handling, log aggregation, statistics display |
| **OverlayWindow** | Screen overlay, click interception, transparency management, click execution |
| **ExecutionEngine** | Data processing orchestration, ledger interaction, result formatting |
| **StructuralIdentityEngine** | Transform application, entropy checking, structural ID computation |
| **InvariantLedger** | Brick storage, deduplication, reference counting |
| **TimelineInspectionPanel** | Event timeline visualization, frequency analysis, optimization detection |
| **Transform Pipeline** | Canonical form detection, transform sequencing |

## Event Flow

### 1. Application Startup

```
Application.Run()
    ?
MainWindow Constructor
    ?
new ExecutionEngine()
    ?
[READY STATE]
```

**Logs Generated:**
```
Application started
Status: Ready
```

### 2. Overlay Activation

```
User clicks "Show Overlay"
    ?
MainWindow.ShowOverlay()
    ?
new OverlayWindow()
    ?
OverlayWindow Constructor
    ?
[Overlay] OverlayWindow: Constructor started
    ?
InitializeOverlay()
    ?
[Overlay] InitializeOverlay: Screen size = 1920x1080
    ?
InitializeTimelinePanel()
    ?
[Overlay] OverlayWindow: Initialization complete
    ?
OverlayWindow.Show()
    ?
OverlayWindow_Loaded event
    ?
SetClickThrough(true)
    ?
[Overlay] SetClickThrough: Click-through enabled
    ?
[OVERLAY ACTIVE - CLICK-THROUGH MODE]
```

**User Sees:**
- Transparent blue overlay across entire screen
- Can interact with applications normally
- Status bar shows "Overlay Active"

### 3. Interception Mode Activation

```
User presses F9 (or clicks "Start Intercept")
    ?
MainWindow.ToggleInterception() OR OverlayWindow.KeyDown(F9)
    ?
OverlayWindow.StartInterception()
    ?
[Overlay] === StartInterception: Activating interception mode ===
    ?
SetClickThrough(false)
    ?
[Overlay] SetClickThrough: Click-through disabled
    ?
StatusText.Visibility = Visible
    ?
Background = Semi-transparent Red
    ?
[Overlay] StartInterception: Interception mode active
    ?
[INTERCEPTION MODE ACTIVE]
```

**User Sees:**
- Overlay turns semi-transparent red
- Status message at top: "INTERCEPTION MODE ACTIVE..."
- HUD appears at bottom left with shortcuts
- MainWindow log shows "=== INTERCEPTION MODE ACTIVE ==="

### 4. Click Interception and Execution

```
User clicks anywhere on screen
    ?
OverlayWindow.MouseDown event
    ?
[Overlay] MouseDown: Button=Left, ClickThrough=False, Intercepting=True
    ?
position = e.GetPosition(this)
    ?
[Overlay] MouseDown: Intercepted at (X, Y)
    ?
Create InterceptEventArgs
    ?
???????????????????????????????????????????????????
? PARALLEL PROCESSING                              ?
???????????????????????????????????????????????????
?                                                  ?
? Branch 1: Event Notification                    ?
? ???????????????????????                         ?
? OnInterceptClick?.Invoke()                      ?
?     ?                                            ?
? MainWindow.OverlayWindow_OnInterceptClick()     ?
?     ?                                            ?
? LogMessage("\n--- Click Intercepted ---")       ?
?     ?                                            ?
? ExecutionEngine.ProcessInterceptedData()        ?
?     ?                                            ?
? StructuralIdentityEngine.ComputeStructuralId()  ?
?     ?                                            ?
? Apply transforms, check entropy                  ?
?     ?                                            ?
? InvariantLedger.IngestBrick()                   ?
?     ?                                            ?
? Deduplication check                              ?
?     ?                                            ?
? Return result                                    ?
?     ?                                            ?
? Log result in MainWindow                         ?
?                                                  ?
???????????????????????????????????????????????????
?                                                  ?
? Branch 2: Timeline Processing                   ?
? ??????????????????????????                      ?
? ProcessInterceptForTimeline()                   ?
?     ?                                            ?
? StructuralIdentityEngine.ComputeStructuralId()  ?
?     ?                                            ?
? Create TimelineEvent                            ?
?     ?                                            ?
? TimelinePanel.AddEvent()                        ?
?     ?                                            ?
? Update frequency map                             ?
?     ?                                            ?
? Check if optimizable (frequency > 1)            ?
?     ?                                            ?
? Update statistics                                ?
?     ?                                            ?
? Refresh event list                               ?
?     ?                                            ?
? Redraw timeline graph                            ?
?                                                  ?
???????????????????????????????????????????????????
?                                                  ?
? Branch 3: Click Execution                       ?
? ?????????????????????                           ?
? ExecuteUnderlyingClick(position)                ?
?     ?                                            ?
? [Overlay] ExecuteUnderlyingClick: ========      ?
?           STARTING CLICK EXECUTION ==========    ?
?     ?                                            ?
? Save current cursor position                     ?
?     ?                                            ?
? Convert overlay position to screen coordinates   ?
?     ?                                            ?
? Get virtual screen dimensions (multi-monitor)    ?
?     ?                                            ?
? WindowFromPoint() - detect target window         ?
?     ?                                            ?
? this.Visibility = Collapsed                     ?
?     ?                                            ?
? [Overlay] ExecuteUnderlyingClick: Overlay hidden?
?     ?                                            ?
? Thread.Sleep(clickExecutionDelayMs)             ?
?     ?                                            ?
? WindowFromPoint() - verify window                ?
?     ?                                            ?
? SetCursorPos(targetX, targetY)                  ?
?     ?                                            ?
? [Overlay] ExecuteUnderlyingClick: Cursor moved  ?
?     ?                                            ?
? SendInput(MOUSEEVENTF_LEFTDOWN)                 ?
?     ?                                            ?
? [Overlay] ExecuteUnderlyingClick: DOWN sent     ?
?     ?                                            ?
? Thread.Sleep(50ms)                              ?
?     ?                                            ?
? SendInput(MOUSEEVENTF_LEFTUP)                   ?
?     ?                                            ?
? [Overlay] ExecuteUnderlyingClick: UP sent       ?
?     ?                                            ?
? Thread.Sleep(clickExecutionDelayMs)             ?
?     ?                                            ?
? this.Visibility = Visible                       ?
?     ?                                            ?
? [Overlay] ExecuteUnderlyingClick: ========      ?
?           CLICK EXECUTION COMPLETE ==========    ?
?                                                  ?
???????????????????????????????????????????????????
    ?
[CLICK PROCESSED AND EXECUTED]
    ?
Target application receives click and responds
```

**Logs Generated:**
```
[Overlay] MouseDown: Button=Left, ClickThrough=False, Intercepting=True
[Overlay] MouseDown: Intercepted at (350, 420)

--- Click Intercepted at (350, 420) ---
[Overlay] MouseDown: Click processed, now executing underlying action
[Overlay] ExecuteUnderlyingClick: ========== STARTING CLICK EXECUTION ==========
[Overlay] ExecuteUnderlyingClick: Overlay position = (350, 420)
[Overlay] ExecuteUnderlyingClick: Target screen coordinates = (350, 420)
[Overlay] ExecuteUnderlyingClick: Window at position before hide = 0x12345678
[Overlay] ExecuteUnderlyingClick: Hiding overlay...
[Overlay] ExecuteUnderlyingClick: Window at position after hide = 0x12345678
[Overlay] ExecuteUnderlyingClick: Moving cursor to (350, 420)
[Overlay] ExecuteUnderlyingClick: SendInput DOWN result = 1
[Overlay] ExecuteUnderlyingClick: SendInput UP result = 1
[Overlay] ExecuteUnderlyingClick: Restoring overlay visibility
[Overlay] ExecuteUnderlyingClick: ========== CLICK EXECUTION COMPLETE ==========

Structural ID: abc123def456...
Transform: IDENTITY
Entropy: 4.23
? Known pattern - ledger remains still
```

### 5. Timeline Inspection

```
User presses F10
    ?
OverlayWindow.KeyDown(F10)
    ?
[Overlay] KeyDown: F10 pressed - toggling timeline panel
    ?
ToggleTimelinePanel()
    ?
TimelinePanel.Visibility = Visible
    ?
[TIMELINE PANEL SHOWN]
```

**User Sees:**
- Timeline panel appears on right side
- Graph showing entropy over time
- Event list with structural IDs
- Statistics: Events, Unique IDs, Stillness
- Output function controls (entropy threshold)
- Transform filter dropdown

**Timeline Updates:**
- Every intercepted click adds a bar to the graph
- Height = entropy (0-8 bits/byte)
- Color = transform type
- Yellow border = optimizable pattern
- Red dashed line = entropy threshold

### 6. Optimization Detection

```
TimelinePanel.AddEvent()
    ?
_structuralIdFrequency[evt.StructuralId]++
    ?
if frequency > 1:
    ?
    evt.IsOptimizable = true
    ?
    OnOptimizableDetected?.Invoke()
    ?
    MainWindow.OverlayWindow_OnOptimizablePatternDetected()
    ?
    LogMessage("\n? OPTIMIZABLE PATTERN DETECTED")
    ?
    [OPTIMIZATION OPPORTUNITY LOGGED]
```

**Logs Generated:**
```
? OPTIMIZABLE PATTERN DETECTED
   Structural ID: abc123def456...
   Transform: IDENTITY
   This pattern has been seen before - execution can be optimized
   Reference count: 3
   First seen: 2024-01-15 14:30:22
```

### 7. Manual Optimization Trigger

```
User presses F11
    ?
OverlayWindow.KeyDown(F11)
    ?
[Overlay] KeyDown: F11 pressed - triggering optimization
    ?
TriggerOptimization()
    ?
OnOptimizationTriggered?.Invoke()
    ?
MainWindow.OverlayWindow_OnOptimizationTriggered()
    ?
LogMessage("?? OPTIMIZATION TRIGGERED (F11)")
    ?
Get ledger statistics
    ?
Display stillness and optimization potential
    ?
[OPTIMIZATION ANALYSIS LOGGED]
```

**Logs Generated:**
```
?? OPTIMIZATION TRIGGERED (F11)
   Threshold: 7.8
   Auto-optimize: True
   Analyzing structural patterns for execution enhancement...
   Current stillness: 67.3%
   Optimization potential: 156 redundant patterns
```

### 8. Timeline Export

```
User clicks "Export Analysis"
    ?
TimelinePanel.ExportAnalysis()
    ?
OnExportRequested?.Invoke()
    ?
MainWindow.OverlayWindow_OnTimelineExportRequested()
    ?
Calculate statistics
    ?
Find top 5 patterns
    ?
Count black bricks and optimizable events
    ?
Display comprehensive report
    ?
[ANALYSIS EXPORTED TO LOG]
```

**Logs Generated:**
```
?? TIMELINE ANALYSIS EXPORT
   Total events: 247
   Unique structural IDs: 81
   Entropy threshold: 7.8

   Top 5 most frequent patterns:
     abc123def456... : 23 occurrences
     def456abc123... : 18 occurrences
     789xyz012abc... : 15 occurrences
     012abc789xyz... : 12 occurrences
     xyz012abc789... : 10 occurrences

   Black Bricks: 8 (3.2%)
   Optimizable: 166 (67.2%)
```

### 9. Deactivation Flow

```
User presses F9 or ESC
    ?
OverlayWindow.KeyDown event
    ?
[Overlay] KeyDown: ESC pressed - stopping interception
    ?
StopInterception()
    ?
[Overlay] === StopInterception: Deactivating interception mode ===
    ?
SetClickThrough(true)
    ?
StatusText.Visibility = Collapsed
    ?
Background = Transparent
    ?
[Overlay] StopInterception: Click-through mode restored
    ?
[CLICK-THROUGH MODE RESTORED]
```

## Component Interactions

### MainWindow ? OverlayWindow

**Events from OverlayWindow to MainWindow:**
- `OnInterceptClick` ? Process click through engine
- `OnEntropyThresholdChanged` ? Log threshold adjustment
- `OnOptimizablePatternDetected` ? Log optimization opportunity
- `OnOptimizationTriggered` ? Show optimization analysis
- `OnTimelineExportRequested` ? Display export analysis
- `OnLog` ? Centralized logging

**Commands from MainWindow to OverlayWindow:**
- `Show()` ? Display overlay
- `ToggleInterception()` ? Start/stop intercept mode
- `SetClickExecutionDelay(ms)` ? Configure timing
- `Close()` ? Hide overlay

### ExecutionEngine ? StructuralIdentityEngine

**Request:**
```csharp
byte[] data = Encoding.UTF8.GetBytes(clickData);
var result = _identityEngine.ComputeStructuralId(data);
```

**Response:**
```csharp
{
    StructuralId: "abc123def456...",
    TransformApplied: "IDENTITY",
    Entropy: 4.23,
    IsBlackBrick: false
}
```

### StructuralIdentityEngine ? Transform Pipeline

**For each transform in sequence:**
1. BitRotationTransform
2. EndiannessSwapTransform  
3. Base64Transform
4. PaddingRemovalTransform

**Process:**
```csharp
foreach (var transform in _transforms)
{
    if (transform.CanApply(data))
    {
        transformedData = transform.Apply(data);
        if (IsMoreCanonical(transformedData, canonicalData))
        {
            canonicalData = transformedData;
            appliedTransform = transform.Name;
        }
    }
}
```

### ExecutionEngine ? InvariantLedger

**Ingestion:**
```csharp
var result = _ledger.IngestBrick(structuralId, metadata);
return new ExecutionResult
{
    IsNewBrick = result.IsNewBrick,
    StructuralId = result.StructuralId,
    Message = FormatMessage(result)
};
```

**Retrieval:**
```csharp
var brick = _ledger.RetrieveBrick(structuralId);
if (brick != null)
{
    LogMessage($"Reference count: {brick.ReferenceCount}");
}
```

## User Actions and Responses

### Complete Action Matrix

| User Action | System Response | Visual Feedback | Logs Generated |
|-------------|-----------------|-----------------|----------------|
| **Launch App** | Show MainWindow | Control panel visible | "Application started" |
| **Click "Show Overlay"** | Create and show overlay | Blue transparent overlay | "[Overlay] OverlayWindow: Constructor started" |
| **Press F9** | Toggle interception | Red overlay + status text | "=== INTERCEPTION MODE ACTIVE ===" |
| **Click while intercepting** | Process + execute click | Brief hide/show, target responds | Full click execution log |
| **Press F10** | Toggle timeline | Panel slides in/out | "[Overlay] KeyDown: F10 pressed" |
| **Press F11** | Trigger optimization | Log analysis appears | "?? OPTIMIZATION TRIGGERED" |
| **Press ESC** | Stop interception | Back to blue overlay | "=== StopInterception ===" |
| **Click "Run Test"** | Execute test suite | Tests in log window | Test results with comparisons |
| **Click "Validate Spec"** | Run validation | Compliance report | Pass/fail for each test |
| **Click "Clear Log"** | Clear output | Empty log window | "Log cleared." |
| **Adjust entropy slider** | Update threshold | Timeline red line moves | "? Entropy threshold adjusted" |
| **Filter transforms** | Update event list | Filtered events shown | None |
| **Click "Export Analysis"** | Generate report | Full analysis in log | "?? TIMELINE ANALYSIS EXPORT" |
| **Click "Clear Timeline"** | Reset timeline | Empty graph and list | None |
| **Close overlay** | Return to ready state | Overlay disappears | "Overlay deactivated" |

## Operational Modes

### Mode 1: Ready (Default)
**State:**
- MainWindow visible
- No overlay
- ExecutionEngine initialized
- Ledger empty or persisted

**Capabilities:**
- Run tests
- Validate specification
- View logs

### Mode 2: Overlay Active (Click-Through)
**State:**
- Transparent overlay covering screen
- `WS_EX_TRANSPARENT` enabled
- Can interact with apps normally
- Monitoring ready

**Capabilities:**
- All Mode 1 capabilities
- Press F9 to enter interception
- View overlay presence

### Mode 3: Interception Active
**State:**
- Red semi-transparent overlay
- `WS_EX_TRANSPARENT` disabled
- Captures all clicks
- Executes clicks after processing

**Capabilities:**
- Click interception and execution
- Structural ID computation
- Timeline recording
- Optimization detection
- Full logging

### Mode 4: Timeline Inspection
**State:**
- All Mode 3 capabilities
- Timeline panel visible
- Real-time graph updates
- Event list populated

**Capabilities:**
- Visual pattern analysis
- Frequency monitoring
- Entropy threshold adjustment
- Transform filtering
- Export analysis

## Summary

This guide covers the complete operational flow of the Trust application from startup through click interception, processing, and execution. Every user action triggers a well-defined sequence of events with comprehensive logging at each step.

**Key Takeaways:**
1. **Parallel Processing:** Click interception triggers three parallel branches (notification, timeline, execution)
2. **Comprehensive Logging:** Every operation is logged for diagnostics
3. **Multi-Layer Architecture:** Clear separation between UI, processing, and storage layers
4. **Event-Driven Design:** Components communicate via events for loose coupling
5. **Configurable Timing:** Click execution delay can be adjusted for different scenarios
6. **Multi-Monitor Support:** Works correctly across multiple displays
7. **Optimization Detection:** Automatic identification of redundant patterns

All events are covered, all flows are documented, and the system operates as a complete, integrated whole.
