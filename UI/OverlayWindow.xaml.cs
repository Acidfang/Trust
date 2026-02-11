using System;
using System.Runtime.InteropServices;
using System.Windows;
using System.Windows.Input;
using System.Windows.Interop;
using System.Windows.Media;
using Trust.Core;

namespace Trust.UI
{
    /// <summary>
    /// Click-through overlay window with interception capabilities
    /// </summary>
    public partial class OverlayWindow : Window
    {
        private const int WS_EX_TRANSPARENT = 0x00000020;
        private const int WS_EX_LAYERED = 0x00080000;
        private const int WS_EX_NOACTIVATE = 0x08000000;
        private const int GWL_EXSTYLE = -20;
        
        private const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
        private const uint MOUSEEVENTF_LEFTUP = 0x0004;

        private bool _isClickThrough = true;
        private bool _isIntercepting = false;
        private TimelineInspectionPanel? _timelinePanel;
        private StructuralIdentityEngine _identityEngine;
        private int _clickExecutionDelayMs = 100;

        [DllImport("user32.dll")]
        private static extern int GetWindowLong(IntPtr hwnd, int index);

        [DllImport("user32.dll")]
        private static extern int SetWindowLong(IntPtr hwnd, int index, int newStyle);
        
        [DllImport("user32.dll")]
        private static extern uint SendInput(uint nInputs, INPUT[] pInputs, int cbSize);
        
        [DllImport("user32.dll")]
        private static extern bool SetCursorPos(int X, int Y);
        
        [DllImport("user32.dll")]
        private static extern IntPtr WindowFromPoint(POINT Point);
        
        [DllImport("user32.dll")]
        private static extern bool GetCursorPos(out POINT lpPoint);
        
        [DllImport("user32.dll")]
        private static extern bool ScreenToClient(IntPtr hWnd, ref POINT lpPoint);
        
        [DllImport("user32.dll")]
        private static extern int GetSystemMetrics(int nIndex);
        
        private const int SM_XVIRTUALSCREEN = 76;
        private const int SM_YVIRTUALSCREEN = 77;
        private const int SM_CXVIRTUALSCREEN = 78;
        private const int SM_CYVIRTUALSCREEN = 79;
        
        [StructLayout(LayoutKind.Sequential)]
        public struct POINT
        {
            public int X;
            public int Y;
        }
        
        [StructLayout(LayoutKind.Sequential)]
        public struct INPUT
        {
            public uint Type;
            public MOUSEKEYBDHARDWAREINPUT Data;
        }
        
        [StructLayout(LayoutKind.Explicit)]
        public struct MOUSEKEYBDHARDWAREINPUT
        {
            [FieldOffset(0)] public MOUSEINPUT Mouse;
        }
        
        [StructLayout(LayoutKind.Sequential)]
        public struct MOUSEINPUT
        {
            public int dx;
            public int dy;
            public uint mouseData;
            public uint dwFlags;
            public uint time;
            public IntPtr dwExtraInfo;
        }
        
        private const uint INPUT_MOUSE = 0;
        private const uint MOUSEEVENTF_MOVE = 0x0001;
        private const uint MOUSEEVENTF_ABSOLUTE = 0x8000;
        private const uint MOUSEEVENTF_VIRTUALDESK = 0x4000;

        public OverlayWindow()
        {
            InitializeComponent();
            _identityEngine = new StructuralIdentityEngine();
            Log("OverlayWindow: Constructor started");
            InitializeOverlay();
            InitializeTimelinePanel();
            Log("OverlayWindow: Initialization complete");
        }

        private void InitializeOverlay()
        {
            Log($"InitializeOverlay: Setting up overlay window");
            WindowStyle = WindowStyle.None;
            ResizeMode = ResizeMode.NoResize;
            AllowsTransparency = true;
            Background = new SolidColorBrush(Color.FromArgb(30, 0, 150, 255));
            Topmost = true;
            ShowInTaskbar = false;

            Left = 0;
            Top = 0;
            Width = SystemParameters.PrimaryScreenWidth;
            Height = SystemParameters.PrimaryScreenHeight;
            
            Log($"InitializeOverlay: Screen size = {Width}x{Height}");

            Loaded += OverlayWindow_Loaded;
            MouseDown += OverlayWindow_MouseDown;
            MouseUp += OverlayWindow_MouseUp;
            KeyDown += OverlayWindow_KeyDown;
            Log("InitializeOverlay: Event handlers attached");
        }

        private void InitializeTimelinePanel()
        {
            _timelinePanel = new TimelineInspectionPanel
            {
                Visibility = Visibility.Collapsed
            };

            _timelinePanel.OnThresholdChanged += TimelinePanel_OnThresholdChanged;
            _timelinePanel.OnOptimizableDetected += TimelinePanel_OnOptimizableDetected;
            _timelinePanel.OnExportRequested += TimelinePanel_OnExportRequested;

            TimelinePanelContainer.Child = _timelinePanel;
        }

        private void OverlayWindow_Loaded(object sender, RoutedEventArgs e)
        {
            Log("OverlayWindow_Loaded: Window loaded event fired");
            SetClickThrough(true);
            Log("OverlayWindow_Loaded: Click-through mode activated");
        }

        private void OverlayWindow_MouseDown(object sender, MouseButtonEventArgs e)
        {
            Log($"MouseDown: Button={e.ChangedButton}, ClickThrough={_isClickThrough}, Intercepting={_isIntercepting}");
            
            if (!_isClickThrough && e.ChangedButton == MouseButton.Left)
            {
                var position = e.GetPosition(this);
                Log($"MouseDown: Intercepted at ({position.X:F0}, {position.Y:F0})");
                
                var interceptEventArgs = new InterceptEventArgs
                {
                    Position = position,
                    Timestamp = DateTime.UtcNow,
                    InterceptType = InterceptType.MouseClick
                };

                OnInterceptClick?.Invoke(this, interceptEventArgs);
                ProcessInterceptForTimeline(interceptEventArgs);
                
                Log("MouseDown: Click processed, now executing underlying action");
                ExecuteUnderlyingClick(position);
            }
            else
            {
                Log("MouseDown: Click passed through (click-through mode active)");
            }
        }
        
        private void OverlayWindow_MouseUp(object sender, MouseButtonEventArgs e)
        {
            Log($"MouseUp: Button={e.ChangedButton}, ClickThrough={_isClickThrough}");
        }

        private void OverlayWindow_KeyDown(object sender, KeyEventArgs e)
        {
            Log($"KeyDown: Key={e.Key}, Intercepting={_isIntercepting}");
            
            if (e.Key == Key.F9)
            {
                Log("KeyDown: F9 pressed - toggling interception");
                ToggleInterception();
                e.Handled = true;
            }
            else if (e.Key == Key.Escape && _isIntercepting)
            {
                Log("KeyDown: ESC pressed - stopping interception");
                StopInterception();
                e.Handled = true;
            }
            else if (e.Key == Key.F10)
            {
                Log("KeyDown: F10 pressed - toggling timeline panel");
                ToggleTimelinePanel();
                e.Handled = true;
            }
            else if (e.Key == Key.F11 && _isIntercepting)
            {
                Log("KeyDown: F11 pressed - triggering optimization");
                TriggerOptimization();
                e.Handled = true;
            }
        }

        private void ProcessInterceptForTimeline(InterceptEventArgs args)
        {
            if (_timelinePanel == null || _timelinePanel.Visibility != Visibility.Visible)
                return;

            try
            {
                string clickData = $"CLICK:{args.Position.X:F0},{args.Position.Y:F0}:{args.Timestamp:O}";
                byte[] data = System.Text.Encoding.UTF8.GetBytes(clickData);

                var identityResult = _identityEngine.ComputeStructuralId(data);

                var timelineEvent = new TimelineEvent
                {
                    Timestamp = args.Timestamp,
                    StructuralId = identityResult.StructuralId,
                    TransformApplied = identityResult.TransformApplied,
                    Entropy = identityResult.Entropy,
                    IsBlackBrick = identityResult.IsBlackBrick,
                    ClickPosition = args.Position,
                    OriginalData = data
                };

                _timelinePanel.AddEvent(timelineEvent);
            }
            catch
            {
                // Silently handle errors to avoid disrupting overlay
            }
        }

        public void SetClickThrough(bool clickThrough)
        {
            _isClickThrough = clickThrough;
            Log($"SetClickThrough: Setting click-through mode to {clickThrough}");

            var hwnd = new WindowInteropHelper(this).Handle;
            var extendedStyle = GetWindowLong(hwnd, GWL_EXSTYLE);
            Log($"SetClickThrough: Current style = 0x{extendedStyle:X8}");

            if (clickThrough)
            {
                int newStyle = extendedStyle | WS_EX_TRANSPARENT | WS_EX_LAYERED | WS_EX_NOACTIVATE;
                SetWindowLong(hwnd, GWL_EXSTYLE, newStyle);
                Background = new SolidColorBrush(Color.FromArgb(10, 0, 150, 255));
                Log($"SetClickThrough: Click-through enabled, new style = 0x{newStyle:X8}");
            }
            else
            {
                int newStyle = (extendedStyle & ~WS_EX_TRANSPARENT) | WS_EX_LAYERED;
                SetWindowLong(hwnd, GWL_EXSTYLE, newStyle);
                Background = new SolidColorBrush(Color.FromArgb(30, 0, 150, 255));
                Log($"SetClickThrough: Click-through disabled, new style = 0x{newStyle:X8}");
            }
        }

        public void ToggleInterception()
        {
            if (_isIntercepting)
                StopInterception();
            else
                StartInterception();
        }

        public void StartInterception()
        {
            Log("=== StartInterception: Activating interception mode ===");
            _isIntercepting = true;
            SetClickThrough(false);
            StatusText.Text = "INTERCEPTION MODE ACTIVE (F9:Toggle | F10:Timeline | F11:Optimize | ESC:Stop)";
            StatusText.Visibility = Visibility.Visible;
            Background = new SolidColorBrush(Color.FromArgb(50, 255, 0, 0));
            QuickControlsHUD.Visibility = Visibility.Visible;
            Log("StartInterception: Interception mode active - overlay will capture clicks");
        }

        public void StopInterception()
        {
            Log("=== StopInterception: Deactivating interception mode ===");
            _isIntercepting = false;
            SetClickThrough(true);
            StatusText.Text = "Click-through mode (F9 to intercept)";
            StatusText.Visibility = Visibility.Collapsed;
            Background = new SolidColorBrush(Color.FromArgb(10, 0, 150, 255));
            QuickControlsHUD.Visibility = Visibility.Collapsed;
            Log("StopInterception: Click-through mode restored");
        }

        public void ToggleTimelinePanel()
        {
            if (_timelinePanel == null) return;

            if (_timelinePanel.Visibility == Visibility.Visible)
            {
                _timelinePanel.Visibility = Visibility.Collapsed;
                TimelinePanelContainer.Visibility = Visibility.Collapsed;
            }
            else
            {
                _timelinePanel.Visibility = Visibility.Visible;
                TimelinePanelContainer.Visibility = Visibility.Visible;
            }
        }

        private void TriggerOptimization()
        {
            OnOptimizationTriggered?.Invoke(this, new OptimizationEventArgs
            {
                Timestamp = DateTime.UtcNow,
                EntropyThreshold = _timelinePanel?.EntropyThreshold ?? 7.8,
                AutoOptimize = _timelinePanel?.AutoOptimize ?? true
            });
        }

        private void TimelinePanel_OnThresholdChanged(object? sender, double newThreshold)
        {
            OnEntropyThresholdChanged?.Invoke(this, newThreshold);
        }

        private void TimelinePanel_OnOptimizableDetected(object? sender, TimelineEvent evt)
        {
            OnOptimizablePatternDetected?.Invoke(this, evt);
        }

        private void TimelinePanel_OnExportRequested(object? sender, ExportAnalysisEventArgs e)
        {
            OnTimelineExportRequested?.Invoke(this, e);
        }

        public void AddTimelineEvent(string structuralId, string transform, double entropy, bool isBlackBrick, byte[] data)
        {
            if (_timelinePanel == null || _timelinePanel.Visibility != Visibility.Visible)
                return;

            var evt = new TimelineEvent
            {
                Timestamp = DateTime.UtcNow,
                StructuralId = structuralId,
                TransformApplied = transform,
                Entropy = entropy,
                IsBlackBrick = isBlackBrick,
                OriginalData = data
            };

            _timelinePanel.AddEvent(evt);
        }

        private void ExecuteUnderlyingClick(Point overlayPosition)
        {
            try
            {
                Log($"ExecuteUnderlyingClick: ========== STARTING CLICK EXECUTION ==========");
                Log($"ExecuteUnderlyingClick: Overlay position = ({overlayPosition.X:F0}, {overlayPosition.Y:F0})");
                
                // Get current cursor position for restoration
                POINT originalCursor;
                GetCursorPos(out originalCursor);
                Log($"ExecuteUnderlyingClick: Original cursor position = ({originalCursor.X}, {originalCursor.Y})");
                
                // Convert overlay position to screen coordinates
                var screenPoint = this.PointToScreen(overlayPosition);
                int targetX = (int)screenPoint.X;
                int targetY = (int)screenPoint.Y;
                Log($"ExecuteUnderlyingClick: Target screen coordinates = ({targetX}, {targetY})");
                
                // Get virtual screen dimensions for multi-monitor support
                int virtualScreenLeft = GetSystemMetrics(SM_XVIRTUALSCREEN);
                int virtualScreenTop = GetSystemMetrics(SM_YVIRTUALSCREEN);
                int virtualScreenWidth = GetSystemMetrics(SM_CXVIRTUALSCREEN);
                int virtualScreenHeight = GetSystemMetrics(SM_CYVIRTUALSCREEN);
                Log($"ExecuteUnderlyingClick: Virtual screen = ({virtualScreenLeft}, {virtualScreenTop}, {virtualScreenWidth}x{virtualScreenHeight})");
                
                // Check which window is at this position before hiding overlay
                POINT checkPoint = new POINT { X = targetX, Y = targetY };
                IntPtr targetWindowBefore = WindowFromPoint(checkPoint);
                var overlayHandle = new WindowInteropHelper(this).Handle;
                Log($"ExecuteUnderlyingClick: Window at position before hide = 0x{targetWindowBefore:X} (Overlay = 0x{overlayHandle:X})");
                
                // Temporarily hide overlay to allow click to reach underlying window
                Log("ExecuteUnderlyingClick: Hiding overlay...");
                this.Visibility = Visibility.Collapsed;
                
                // Wait for visibility change to take effect
                Application.Current.Dispatcher.Invoke(() => { }, System.Windows.Threading.DispatcherPriority.Render);
                System.Threading.Thread.Sleep(_clickExecutionDelayMs);
                
                // Check window at position after hiding overlay
                IntPtr targetWindowAfter = WindowFromPoint(checkPoint);
                Log($"ExecuteUnderlyingClick: Window at position after hide = 0x{targetWindowAfter:X}");
                
                if (targetWindowAfter == IntPtr.Zero)
                {
                    Log("ExecuteUnderlyingClick: WARNING - No window found at target position");
                }
                else if (targetWindowAfter == overlayHandle)
                {
                    Log("ExecuteUnderlyingClick: WARNING - Overlay still detected at position (may not be fully hidden)");
                }
                
                // Move cursor to target position
                Log($"ExecuteUnderlyingClick: Moving cursor to ({targetX}, {targetY})");
                bool cursorMoved = SetCursorPos(targetX, targetY);
                Log($"ExecuteUnderlyingClick: SetCursorPos result = {cursorMoved}");
                
                // Verify cursor position
                POINT actualCursor;
                GetCursorPos(out actualCursor);
                Log($"ExecuteUnderlyingClick: Actual cursor position after move = ({actualCursor.X}, {actualCursor.Y})");
                
                // Small delay to allow cursor position to stabilize
                System.Threading.Thread.Sleep(50);
                
                // Create mouse down input
                INPUT[] inputs = new INPUT[2];
                
                // Mouse down
                inputs[0] = new INPUT
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
                
                // Mouse up
                inputs[1] = new INPUT
                {
                    Type = INPUT_MOUSE,
                    Data = new MOUSEKEYBDHARDWAREINPUT
                    {
                        Mouse = new MOUSEINPUT
                        {
                            dx = 0,
                            dy = 0,
                            mouseData = 0,
                            dwFlags = MOUSEEVENTF_LEFTUP,
                            time = 0,
                            dwExtraInfo = IntPtr.Zero
                        }
                    }
                };
                
                Log("ExecuteUnderlyingClick: Sending mouse DOWN event via SendInput");
                uint downResult = SendInput(1, new[] { inputs[0] }, Marshal.SizeOf(typeof(INPUT)));
                Log($"ExecuteUnderlyingClick: SendInput DOWN result = {downResult} (1 = success)");
                
                System.Threading.Thread.Sleep(50);
                
                Log("ExecuteUnderlyingClick: Sending mouse UP event via SendInput");
                uint upResult = SendInput(1, new[] { inputs[1] }, Marshal.SizeOf(typeof(INPUT)));
                Log($"ExecuteUnderlyingClick: SendInput UP result = {upResult} (1 = success)");
                
                // Wait before restoring
                System.Threading.Thread.Sleep(_clickExecutionDelayMs);
                
                // Restore cursor to original position (optional)
                // Uncomment if you want cursor to return to original position
                // SetCursorPos(originalCursor.X, originalCursor.Y);
                // Log($"ExecuteUnderlyingClick: Cursor restored to original position ({originalCursor.X}, {originalCursor.Y})");
                
                // Show overlay again
                Log("ExecuteUnderlyingClick: Restoring overlay visibility");
                this.Visibility = Visibility.Visible;
                
                Log($"ExecuteUnderlyingClick: ========== CLICK EXECUTION COMPLETE ==========");
                Log($"ExecuteUnderlyingClick: Summary - Inputs sent: {downResult + upResult}/2, Target: 0x{targetWindowAfter:X}, Position: ({targetX}, {targetY})");
            }
            catch (Exception ex)
            {
                Log($"ExecuteUnderlyingClick: ========== ERROR OCCURRED ==========");
                Log($"ExecuteUnderlyingClick: Exception type: {ex.GetType().Name}");
                Log($"ExecuteUnderlyingClick: Error message: {ex.Message}");
                Log($"ExecuteUnderlyingClick: Stack trace:");
                foreach (var line in ex.StackTrace?.Split('\n') ?? Array.Empty<string>())
                {
                    Log($"  {line.Trim()}");
                }
                
                // Ensure overlay is visible even if error occurs
                this.Visibility = Visibility.Visible;
                Log("ExecuteUnderlyingClick: Overlay visibility restored after error");
            }
        }
        
        private void Log(string message)
        {
            OnLog?.Invoke(this, $"[Overlay] {message}");
        }
        
        public void SetClickExecutionDelay(int delayMs)
        {
            _clickExecutionDelayMs = Math.Max(50, Math.Min(delayMs, 500));
            Log($"SetClickExecutionDelay: Delay set to {_clickExecutionDelayMs}ms");
        }

        public event EventHandler<InterceptEventArgs>? OnInterceptClick;
        public event EventHandler<double>? OnEntropyThresholdChanged;
        public event EventHandler<TimelineEvent>? OnOptimizablePatternDetected;
        public event EventHandler<OptimizationEventArgs>? OnOptimizationTriggered;
        public event EventHandler<ExportAnalysisEventArgs>? OnTimelineExportRequested;
        public event EventHandler<string>? OnLog;
    }

    public class InterceptEventArgs : EventArgs
    {
        public Point Position { get; set; }
        public DateTime Timestamp { get; set; }
        public InterceptType InterceptType { get; set; }
    }

    public enum InterceptType
    {
        MouseClick,
        KeyPress,
        SystemEvent
    }

    public class OptimizationEventArgs : EventArgs
    {
        public DateTime Timestamp { get; set; }
        public double EntropyThreshold { get; set; }
        public bool AutoOptimize { get; set; }
    }
}
