using System.Text;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Trust.UI;
using Trust.Services;
using Trust.Core;
using Trust.Tests;

namespace Trust
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private OverlayWindow? _overlayWindow;
        private ExecutionEngine _executionEngine;
        private bool _isOverlayVisible = false;

        public MainWindow()
        {
            InitializeComponent();
            _executionEngine = new ExecutionEngine();
            
            KeyDown += MainWindow_KeyDown;
        }

        private void MainWindow_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.F9)
            {
                ToggleInterception();
                e.Handled = true;
            }
        }

        private void ToggleOverlayButton_Click(object sender, RoutedEventArgs e)
        {
            if (_isOverlayVisible)
            {
                HideOverlay();
            }
            else
            {
                ShowOverlay();
            }
        }

        private void ShowOverlay()
        {
            if (_overlayWindow == null)
            {
                _overlayWindow = new OverlayWindow();
                _overlayWindow.OnInterceptClick += OverlayWindow_OnInterceptClick;
                _overlayWindow.OnEntropyThresholdChanged += OverlayWindow_OnEntropyThresholdChanged;
                _overlayWindow.OnOptimizablePatternDetected += OverlayWindow_OnOptimizablePatternDetected;
                _overlayWindow.OnOptimizationTriggered += OverlayWindow_OnOptimizationTriggered;
                _overlayWindow.OnTimelineExportRequested += OverlayWindow_OnTimelineExportRequested;
                _overlayWindow.OnLog += OverlayWindow_OnLog;
                _overlayWindow.Closed += (s, e) =>
                {
                    _overlayWindow = null;
                    _isOverlayVisible = false;
                    ToggleOverlayButton.Content = "Show Overlay";
                };
            }

            _overlayWindow.Show();
            _isOverlayVisible = true;
            ToggleOverlayButton.Content = "Hide Overlay";
            LogMessage("Overlay activated - Click-through mode enabled");
            LogMessage("Press F10 to show Timeline Inspector");
            LogMessage("Press F9 to activate interception mode");
            UpdateStatus("Overlay Active");
        }

        private void HideOverlay()
        {
            _overlayWindow?.Close();
            _overlayWindow = null;
            _isOverlayVisible = false;
            ToggleOverlayButton.Content = "Show Overlay";
            LogMessage("Overlay deactivated");
            UpdateStatus("Ready");
        }

        private void ToggleInterceptButton_Click(object sender, RoutedEventArgs e)
        {
            ToggleInterception();
        }

        private void ToggleInterception()
        {
            if (_overlayWindow == null)
            {
                ShowOverlay();
            }

            _overlayWindow?.ToggleInterception();
            
            bool isIntercepting = _overlayWindow?.StatusText.Visibility == Visibility.Visible;
            ToggleInterceptButton.Content = isIntercepting ? "Stop Intercept (F9)" : "Start Intercept (F9)";
            
            if (isIntercepting)
            {
                LogMessage("=== INTERCEPTION MODE ACTIVE ===");
                LogMessage("All clicks will be captured and processed through the Invariant Identity Engine");
                UpdateStatus("INTERCEPTING");
            }
            else
            {
                LogMessage("Interception mode stopped");
                UpdateStatus("Overlay Active");
            }
        }

        private void OverlayWindow_OnInterceptClick(object? sender, InterceptEventArgs e)
        {
            LogMessage($"\n--- Click Intercepted at ({e.Position.X:F0}, {e.Position.Y:F0}) ---");
            
            string clickData = $"CLICK:{e.Position.X},{e.Position.Y}:{e.Timestamp:O}";
            byte[] data = Encoding.UTF8.GetBytes(clickData);
            
            var result = _executionEngine.ProcessInterceptedData(data, $"InterceptClick_{e.Timestamp:yyyyMMddHHmmss}");
            
            LogMessage(result.Message);
            UpdateStatistics();
            
            if (result.IsNewBrick)
            {
                LogMessage("✓ New structural pattern identified and stored");
            }
            else
            {
                LogMessage("✓ Known pattern - ledger remains still");
            }
        }

        private void OverlayWindow_OnEntropyThresholdChanged(object? sender, double newThreshold)
        {
            LogMessage($"\n⚙ Entropy threshold adjusted: {newThreshold:F2} bits/byte");
            LogMessage("Output functions will be recalibrated with new threshold");
        }

        private void OverlayWindow_OnOptimizablePatternDetected(object? sender, TimelineEvent evt)
        {
            LogMessage($"\n⚡ OPTIMIZABLE PATTERN DETECTED");
            LogMessage($"   Structural ID: {evt.StructuralId.Substring(0, 16)}...");
            LogMessage($"   Transform: {evt.TransformApplied}");
            LogMessage($"   This pattern has been seen before - execution can be optimized");
            
            if (_executionEngine != null)
            {
                var brick = _executionEngine.RetrieveBrick(evt.StructuralId);
                if (brick != null)
                {
                    LogMessage($"   Reference count: {brick.ReferenceCount}");
                    LogMessage($"   First seen: {brick.FirstSeenUtc:yyyy-MM-dd HH:mm:ss}");
                }
            }
        }

        private void OverlayWindow_OnOptimizationTriggered(object? sender, OptimizationEventArgs e)
        {
            LogMessage($"\n🚀 OPTIMIZATION TRIGGERED (F11)");
            LogMessage($"   Threshold: {e.EntropyThreshold:F2}");
            LogMessage($"   Auto-optimize: {e.AutoOptimize}");
            LogMessage("   Analyzing structural patterns for execution enhancement...");
            
            var stats = _executionEngine.GetLedgerStatistics();
            LogMessage($"   Current stillness: {(1 - stats.CompressionRatio) * 100:F2}%");
            LogMessage($"   Optimization potential: {stats.TotalIngests - stats.TotalBricks} redundant patterns");
        }

        private void OverlayWindow_OnTimelineExportRequested(object? sender, ExportAnalysisEventArgs e)
        {
            LogMessage($"\n📊 TIMELINE ANALYSIS EXPORT");
            LogMessage($"   Total events: {e.Events.Count}");
            LogMessage($"   Unique structural IDs: {e.Frequency.Count}");
            LogMessage($"   Entropy threshold: {e.EntropyThreshold:F2}");
            
            var topPatterns = e.Frequency.OrderByDescending(kv => kv.Value).Take(5);
            LogMessage("\n   Top 5 most frequent patterns:");
            foreach (var pattern in topPatterns)
            {
                LogMessage($"     {pattern.Key.Substring(0, 16)}... : {pattern.Value} occurrences");
            }
            
            int blackBricks = e.Events.Count(ev => ev.IsBlackBrick);
            int optimizable = e.Events.Count(ev => ev.IsOptimizable);
            
            LogMessage($"\n   Black Bricks: {blackBricks} ({(blackBricks / (double)e.Events.Count * 100):F1}%)");
            LogMessage($"   Optimizable: {optimizable} ({(optimizable / (double)e.Events.Count * 100):F1}%)");
        }
        
        private void OverlayWindow_OnLog(object? sender, string message)
        {
            LogMessage(message);
        }

        private void TestButton_Click(object sender, RoutedEventArgs e)
        {
            LogMessage("\n=== Running Adversarial Test Suite ===\n");

            string testData = "The quick brown fox jumps over the lazy dog";
            
            LogMessage("Test 1: Original data");
            var result1 = _executionEngine.ProcessTextInput(testData, "Test_Original");
            LogMessage(result1.Message);

            LogMessage("\nTest 2: Base64 encoded (should produce same ID)");
            byte[] base64Data = Encoding.ASCII.GetBytes(Convert.ToBase64String(Encoding.UTF8.GetBytes(testData)));
            var result2 = _executionEngine.ProcessInterceptedData(base64Data, "Test_Base64");
            LogMessage(result2.Message);

            LogMessage("\nTest 3: Padded version");
            byte[] paddedData = new byte[testData.Length + 10];
            Encoding.UTF8.GetBytes(testData).CopyTo(paddedData, 0);
            var result3 = _executionEngine.ProcessInterceptedData(paddedData, "Test_Padded");
            LogMessage(result3.Message);

            LogMessage("\nTest 4: High entropy (Black Brick test)");
            byte[] randomData = new byte[64];
            new Random().NextBytes(randomData);
            var result4 = _executionEngine.ProcessInterceptedData(randomData, "Test_HighEntropy");
            LogMessage(result4.Message);

            LogMessage("\n=== Test Suite Complete ===");
            UpdateStatistics();
        }

        private void ClearButton_Click(object sender, RoutedEventArgs e)
        {
            OutputTextBox.Text = "Log cleared.\n\n";
        }

        private void ValidateButton_Click(object sender, RoutedEventArgs e)
        {
            LogMessage("\n=== RUNNING SPECIFICATION VALIDATION ===\n");
            LogMessage("Validating against formal specification in brief.md...\n");

            var validator = new SpecificationValidator();
            var report = validator.RunFullValidation();

            LogMessage(report.ToString());

            if (report.IsCompliant)
            {
                LogMessage("✓✓✓ SYSTEM IS SPECIFICATION COMPLIANT ✓✓✓");
                UpdateStatus("Spec Compliant");
            }
            else
            {
                LogMessage("✗✗✗ SPECIFICATION COMPLIANCE FAILED ✗✗✗");
                UpdateStatus("Non-Compliant");
            }
        }

        private void LogMessage(string message)
        {
            Dispatcher.Invoke(() =>
            {
                OutputTextBox.AppendText(message + "\n");
                OutputTextBox.ScrollToEnd();
            });
        }

        private void UpdateStatus(string status)
        {
            Dispatcher.Invoke(() =>
            {
                StatusLabel.Text = $"Status: {status}";
            });
        }

        private void UpdateStatistics()
        {
            var stats = _executionEngine.GetLedgerStatistics();
            Dispatcher.Invoke(() =>
            {
                BrickCountLabel.Text = $"Bricks: {stats.TotalBricks}";
                CompressionLabel.Text = $"Compression: {(1 - stats.CompressionRatio) * 100:F2}%";
            });
        }

        protected override void OnClosed(EventArgs e)
        {
            _overlayWindow?.Close();
            base.OnClosed(e);
        }
    }
}