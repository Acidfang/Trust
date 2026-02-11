using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Shapes;
using Trust.Core;

namespace Trust.UI
{
    /// <summary>
    /// Interactive timeline panel for structural identity inspection and optimization
    /// </summary>
    public class TimelineInspectionPanel : Border
    {
        private readonly Canvas _timelineCanvas;
        private readonly StackPanel _controlPanel;
        private readonly TextBlock _statsText;
        private readonly Slider _entropyThresholdSlider;
        private readonly CheckBox _autoOptimizeCheckbox;
        private readonly ComboBox _transformFilterCombo;
        private readonly ListBox _eventListBox;
        
        private readonly List<TimelineEvent> _events;
        private readonly Dictionary<string, int> _structuralIdFrequency;
        private double _currentEntropyThreshold = 7.8;
        private bool _autoOptimize = true;

        public TimelineInspectionPanel()
        {
            _events = new List<TimelineEvent>();
            _structuralIdFrequency = new Dictionary<string, int>();

            Width = 400;
            MinHeight = 200;
            Background = new SolidColorBrush(Color.FromArgb(230, 30, 30, 30));
            BorderBrush = new SolidColorBrush(Color.FromArgb(255, 0, 150, 255));
            BorderThickness = new Thickness(2);
            CornerRadius = new CornerRadius(8);
            Padding = new Thickness(10);
            Margin = new Thickness(20);

            var mainPanel = new StackPanel();

            var headerPanel = new DockPanel { Margin = new Thickness(0, 0, 0, 10) };
            var titleText = new TextBlock
            {
                Text = "? Timeline Inspector",
                FontSize = 18,
                FontWeight = FontWeights.Bold,
                Foreground = Brushes.Cyan
            };
            DockPanel.SetDock(titleText, Dock.Left);

            var closeButton = new Button
            {
                Content = "?",
                Width = 25,
                Height = 25,
                Background = new SolidColorBrush(Color.FromArgb(100, 255, 0, 0)),
                Foreground = Brushes.White,
                BorderThickness = new Thickness(0),
                FontWeight = FontWeights.Bold,
                Cursor = System.Windows.Input.Cursors.Hand
            };
            closeButton.Click += (s, e) => Visibility = Visibility.Collapsed;
            DockPanel.SetDock(closeButton, Dock.Right);

            headerPanel.Children.Add(titleText);
            headerPanel.Children.Add(closeButton);
            mainPanel.Children.Add(headerPanel);

            _statsText = new TextBlock
            {
                Text = "Events: 0 | Unique IDs: 0 | Stillness: 0%",
                Foreground = Brushes.LightGreen,
                FontFamily = new FontFamily("Consolas"),
                FontSize = 11,
                Margin = new Thickness(0, 0, 0, 10)
            };
            mainPanel.Children.Add(_statsText);

            var controlsExpander = new Expander
            {
                Header = "? Output Function Controls",
                IsExpanded = true,
                Foreground = Brushes.White,
                Margin = new Thickness(0, 0, 0, 10)
            };

            _controlPanel = new StackPanel { Margin = new Thickness(10, 5, 0, 5) };

            var entropyPanel = new StackPanel { Margin = new Thickness(0, 5, 0, 5) };
            entropyPanel.Children.Add(new TextBlock
            {
                Text = $"Entropy Threshold: {_currentEntropyThreshold:F1}",
                Foreground = Brushes.Orange,
                FontSize = 11,
                Name = "EntropyLabel"
            });

            _entropyThresholdSlider = new Slider
            {
                Minimum = 5.0,
                Maximum = 8.0,
                Value = _currentEntropyThreshold,
                TickFrequency = 0.1,
                IsSnapToTickEnabled = true,
                Margin = new Thickness(0, 2, 0, 0)
            };
            _entropyThresholdSlider.ValueChanged += EntropyThresholdSlider_ValueChanged;
            entropyPanel.Children.Add(_entropyThresholdSlider);
            _controlPanel.Children.Add(entropyPanel);

            _autoOptimizeCheckbox = new CheckBox
            {
                Content = "Auto-Optimize Redundant Patterns",
                IsChecked = _autoOptimize,
                Foreground = Brushes.LightBlue,
                Margin = new Thickness(0, 5, 0, 5)
            };
            _autoOptimizeCheckbox.Checked += (s, e) => _autoOptimize = true;
            _autoOptimizeCheckbox.Unchecked += (s, e) => _autoOptimize = false;
            _controlPanel.Children.Add(_autoOptimizeCheckbox);

            var filterPanel = new StackPanel { Margin = new Thickness(0, 5, 0, 5) };
            filterPanel.Children.Add(new TextBlock
            {
                Text = "Transform Filter:",
                Foreground = Brushes.White,
                FontSize = 11
            });

            _transformFilterCombo = new ComboBox
            {
                Margin = new Thickness(0, 2, 0, 0),
                Background = new SolidColorBrush(Color.FromArgb(255, 50, 50, 50)),
                Foreground = Brushes.White
            };
            _transformFilterCombo.Items.Add("All Transforms");
            _transformFilterCombo.Items.Add("IDENTITY");
            _transformFilterCombo.Items.Add("BITROT");
            _transformFilterCombo.Items.Add("ENDIAN");
            _transformFilterCombo.Items.Add("BASE64");
            _transformFilterCombo.Items.Add("PADDING_REMOVE");
            _transformFilterCombo.Items.Add("BLACK_BRICK");
            _transformFilterCombo.SelectedIndex = 0;
            _transformFilterCombo.SelectionChanged += (s, e) => RefreshEventList();
            filterPanel.Children.Add(_transformFilterCombo);
            _controlPanel.Children.Add(filterPanel);

            controlsExpander.Content = _controlPanel;
            mainPanel.Children.Add(controlsExpander);

            var eventsExpander = new Expander
            {
                Header = "?? Event Timeline",
                IsExpanded = true,
                Foreground = Brushes.White,
                Margin = new Thickness(0, 0, 0, 10)
            };

            _eventListBox = new ListBox
            {
                MaxHeight = 200,
                Background = new SolidColorBrush(Color.FromArgb(255, 20, 20, 20)),
                Foreground = Brushes.White,
                BorderThickness = new Thickness(1),
                BorderBrush = Brushes.Gray,
                FontFamily = new FontFamily("Consolas"),
                FontSize = 10,
                Margin = new Thickness(10, 5, 0, 5)
            };
            eventsExpander.Content = _eventListBox;
            mainPanel.Children.Add(eventsExpander);

            _timelineCanvas = new Canvas
            {
                Height = 60,
                Background = new SolidColorBrush(Color.FromArgb(255, 40, 40, 40)),
                Margin = new Thickness(0, 5, 0, 0)
            };
            mainPanel.Children.Add(_timelineCanvas);

            var buttonPanel = new StackPanel
            {
                Orientation = Orientation.Horizontal,
                HorizontalAlignment = HorizontalAlignment.Center,
                Margin = new Thickness(0, 10, 0, 0)
            };

            var clearButton = new Button
            {
                Content = "Clear Timeline",
                Padding = new Thickness(10, 3, 10, 3),
                Background = new SolidColorBrush(Color.FromArgb(255, 100, 50, 50)),
                Foreground = Brushes.White,
                BorderThickness = new Thickness(0),
                Margin = new Thickness(5, 0, 5, 0),
                Cursor = System.Windows.Input.Cursors.Hand
            };
            clearButton.Click += (s, e) => ClearTimeline();

            var exportButton = new Button
            {
                Content = "Export Analysis",
                Padding = new Thickness(10, 3, 10, 3),
                Background = new SolidColorBrush(Color.FromArgb(255, 50, 100, 50)),
                Foreground = Brushes.White,
                BorderThickness = new Thickness(0),
                Margin = new Thickness(5, 0, 5, 0),
                Cursor = System.Windows.Input.Cursors.Hand
            };
            exportButton.Click += (s, e) => ExportAnalysis();

            buttonPanel.Children.Add(clearButton);
            buttonPanel.Children.Add(exportButton);
            mainPanel.Children.Add(buttonPanel);

            Child = mainPanel;
        }

        private void EntropyThresholdSlider_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            _currentEntropyThreshold = e.NewValue;
            
            foreach (var child in _controlPanel.Children)
            {
                if (child is StackPanel panel)
                {
                    foreach (var panelChild in panel.Children)
                    {
                        if (panelChild is TextBlock tb && tb.Name == "EntropyLabel")
                        {
                            tb.Text = $"Entropy Threshold: {_currentEntropyThreshold:F1}";
                        }
                    }
                }
            }

            OnThresholdChanged?.Invoke(this, _currentEntropyThreshold);
        }

        public void AddEvent(TimelineEvent evt)
        {
            _events.Add(evt);

            if (!_structuralIdFrequency.ContainsKey(evt.StructuralId))
                _structuralIdFrequency[evt.StructuralId] = 0;
            
            _structuralIdFrequency[evt.StructuralId]++;

            if (_autoOptimize && _structuralIdFrequency[evt.StructuralId] > 1)
            {
                evt.IsOptimizable = true;
                OnOptimizableDetected?.Invoke(this, evt);
            }

            UpdateStats();
            RefreshEventList();
            DrawTimeline();
        }

        private void UpdateStats()
        {
            int totalEvents = _events.Count;
            int uniqueIds = _structuralIdFrequency.Count;
            double stillness = totalEvents > 0 ? (1 - (uniqueIds / (double)totalEvents)) * 100 : 0;

            _statsText.Text = $"Events: {totalEvents} | Unique IDs: {uniqueIds} | Stillness: {stillness:F1}%";
        }

        private void RefreshEventList()
        {
            _eventListBox.Items.Clear();

            var filter = _transformFilterCombo.SelectedItem?.ToString() ?? "All Transforms";
            var filteredEvents = _events.AsEnumerable();

            if (filter != "All Transforms")
            {
                filteredEvents = _events.Where(e =>
                {
                    if (filter == "BLACK_BRICK") return e.IsBlackBrick;
                    if (filter == "BITROT") return e.TransformApplied.StartsWith("BITROT");
                    if (filter == "ENDIAN") return e.TransformApplied.StartsWith("ENDIAN");
                    return e.TransformApplied == filter;
                });
            }

            foreach (var evt in filteredEvents.TakeLast(50).Reverse())
            {
                var color = GetEventColor(evt);
                var optimizeMarker = evt.IsOptimizable ? "?" : " ";
                var blackBrickMarker = evt.IsBlackBrick ? "??" : " ";
                
                var item = new ListBoxItem
                {
                    Content = $"{optimizeMarker}{blackBrickMarker} [{evt.Timestamp:HH:mm:ss}] {evt.TransformApplied,-12} E:{evt.Entropy:F2} ID:{evt.StructuralId.Substring(0, 8)}...",
                    Foreground = new SolidColorBrush(color),
                    FontFamily = new FontFamily("Consolas"),
                    FontSize = 10
                };

                _eventListBox.Items.Add(item);
            }
        }

        private void DrawTimeline()
        {
            _timelineCanvas.Children.Clear();

            if (_events.Count == 0) return;

            double canvasWidth = _timelineCanvas.ActualWidth > 0 ? _timelineCanvas.ActualWidth : 380;
            double canvasHeight = 60;

            int visibleEvents = Math.Min(_events.Count, 100);
            var recentEvents = _events.TakeLast(visibleEvents).ToList();

            double barWidth = canvasWidth / visibleEvents;

            for (int i = 0; i < recentEvents.Count; i++)
            {
                var evt = recentEvents[i];
                double x = i * barWidth;
                
                double normalizedEntropy = Math.Min(evt.Entropy / 8.0, 1.0);
                double height = canvasHeight * normalizedEntropy;

                var rect = new Rectangle
                {
                    Width = Math.Max(barWidth - 1, 1),
                    Height = height,
                    Fill = new SolidColorBrush(GetEventColor(evt)),
                    Stroke = evt.IsOptimizable ? Brushes.Yellow : Brushes.Transparent,
                    StrokeThickness = evt.IsOptimizable ? 1 : 0
                };

                Canvas.SetLeft(rect, x);
                Canvas.SetBottom(rect, 0);

                rect.ToolTip = $"Time: {evt.Timestamp:HH:mm:ss}\n" +
                              $"Transform: {evt.TransformApplied}\n" +
                              $"Entropy: {evt.Entropy:F2}\n" +
                              $"ID: {evt.StructuralId.Substring(0, 16)}...\n" +
                              $"Optimizable: {evt.IsOptimizable}";

                _timelineCanvas.Children.Add(rect);
            }

            var thresholdLine = new Line
            {
                X1 = 0,
                X2 = canvasWidth,
                Y1 = canvasHeight * (1 - _currentEntropyThreshold / 8.0),
                Y2 = canvasHeight * (1 - _currentEntropyThreshold / 8.0),
                Stroke = Brushes.Red,
                StrokeThickness = 1,
                StrokeDashArray = new DoubleCollection { 4, 2 }
            };

            _timelineCanvas.Children.Add(thresholdLine);
        }

        private Color GetEventColor(TimelineEvent evt)
        {
            if (evt.IsBlackBrick)
                return Color.FromRgb(255, 50, 50);
            
            if (evt.IsOptimizable)
                return Color.FromRgb(255, 255, 0);

            return evt.TransformApplied switch
            {
                "IDENTITY" => Color.FromRgb(100, 200, 100),
                var t when t.StartsWith("BITROT") => Color.FromRgb(100, 150, 255),
                var t when t.StartsWith("ENDIAN") => Color.FromRgb(255, 150, 100),
                "BASE64" => Color.FromRgb(150, 100, 255),
                "PADDING_REMOVE" => Color.FromRgb(100, 255, 200),
                _ => Color.FromRgb(200, 200, 200)
            };
        }

        private void ClearTimeline()
        {
            _events.Clear();
            _structuralIdFrequency.Clear();
            UpdateStats();
            RefreshEventList();
            DrawTimeline();
        }

        private void ExportAnalysis()
        {
            OnExportRequested?.Invoke(this, new ExportAnalysisEventArgs
            {
                Events = _events.ToList(),
                Frequency = new Dictionary<string, int>(_structuralIdFrequency),
                EntropyThreshold = _currentEntropyThreshold,
                AutoOptimize = _autoOptimize
            });
        }

        protected override void OnRenderSizeChanged(SizeChangedInfo sizeInfo)
        {
            base.OnRenderSizeChanged(sizeInfo);
            if (sizeInfo.WidthChanged)
                DrawTimeline();
        }

        public event EventHandler<double>? OnThresholdChanged;
        public event EventHandler<TimelineEvent>? OnOptimizableDetected;
        public event EventHandler<ExportAnalysisEventArgs>? OnExportRequested;

        public double EntropyThreshold => _currentEntropyThreshold;
        public bool AutoOptimize => _autoOptimize;
    }

    public class TimelineEvent
    {
        public DateTime Timestamp { get; set; }
        public string StructuralId { get; set; } = string.Empty;
        public string TransformApplied { get; set; } = string.Empty;
        public double Entropy { get; set; }
        public bool IsBlackBrick { get; set; }
        public bool IsOptimizable { get; set; }
        public Point? ClickPosition { get; set; }
        public byte[] OriginalData { get; set; } = Array.Empty<byte>();
    }

    public class ExportAnalysisEventArgs : EventArgs
    {
        public List<TimelineEvent> Events { get; set; } = new List<TimelineEvent>();
        public Dictionary<string, int> Frequency { get; set; } = new Dictionary<string, int>();
        public double EntropyThreshold { get; set; }
        public bool AutoOptimize { get; set; }
    }
}
