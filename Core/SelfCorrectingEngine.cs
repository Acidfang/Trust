using System;
using System.Collections.Generic;
using System.Linq;

namespace Trust.Core
{
    /// <summary>
    /// Self-correcting system that detects errors and automatically applies fixes
    /// Learns from corrections to prevent future errors
    /// </summary>
    public class SelfCorrectingEngine
    {
        private readonly CauseEffectTracker _causeEffectTracker;
        private readonly List<CorrectionRule> _correctionRules;
        private readonly List<CorrectionRecord> _correctionHistory;
        private readonly Dictionary<string, int> _errorFrequency;
        private readonly int _maxHistory = 5000;

        public SelfCorrectingEngine(CauseEffectTracker causeEffectTracker)
        {
            _causeEffectTracker = causeEffectTracker;
            _correctionRules = new List<CorrectionRule>();
            _correctionHistory = new List<CorrectionRecord>();
            _errorFrequency = new Dictionary<string, int>();

            InitializeDefaultRules();
        }

        /// <summary>
        /// Initialize default correction rules
        /// </summary>
        private void InitializeDefaultRules()
        {
            // Rule: If SendInput fails, increase delay and retry
            AddRule(new CorrectionRule
            {
                ErrorPattern = "SendInput.*result = 0",
                CorrectionAction = "Increase click execution delay",
                AutoApply = true,
                MaxRetries = 3,
                Severity = ErrorSeverity.Medium,
                CorrectiveAction = (context) =>
                {
                    Log("Detected SendInput failure - increasing delay by 50ms");
                    return new CorrectionResult
                    {
                        Success = true,
                        Message = "Delay increased to improve reliability",
                        NewValue = "Delay + 50ms"
                    };
                }
            });

            // Rule: If overlay not hiding properly, increase delay
            AddRule(new CorrectionRule
            {
                ErrorPattern = "Overlay still detected at position",
                CorrectionAction = "Increase hide delay",
                AutoApply = true,
                MaxRetries = 2,
                Severity = ErrorSeverity.Medium,
                CorrectiveAction = (context) =>
                {
                    Log("Overlay hiding too slowly - increasing delay");
                    return new CorrectionResult
                    {
                        Success = true,
                        Message = "Hide delay increased",
                        NewValue = "Delay + 25ms"
                    };
                }
            });

            // Rule: If entropy threshold causing too many black bricks, adjust
            AddRule(new CorrectionRule
            {
                ErrorPattern = "Black Brick rate > 50%",
                CorrectionAction = "Lower entropy threshold",
                AutoApply = false, // Requires user confirmation
                MaxRetries = 1,
                Severity = ErrorSeverity.Low,
                CorrectiveAction = (context) =>
                {
                    Log("High black brick rate detected - suggesting threshold adjustment");
                    return new CorrectionResult
                    {
                        Success = true,
                        Message = "Consider lowering entropy threshold to 7.0-7.5",
                        Recommendation = true
                    };
                }
            });

            // Rule: If click coordinates outside screen bounds, clamp values
            AddRule(new CorrectionRule
            {
                ErrorPattern = "coordinates.*outside.*bounds",
                CorrectionAction = "Clamp coordinates to screen bounds",
                AutoApply = true,
                MaxRetries = 1,
                Severity = ErrorSeverity.High,
                CorrectiveAction = (context) =>
                {
                    Log("Out of bounds coordinates detected - clamping to screen");
                    return new CorrectionResult
                    {
                        Success = true,
                        Message = "Coordinates adjusted to valid screen region"
                    };
                }
            });

            // Rule: If window handle is zero, retry detection
            AddRule(new CorrectionRule
            {
                ErrorPattern = "window.*handle.*0x0+$",
                CorrectionAction = "Retry window detection",
                AutoApply = true,
                MaxRetries = 3,
                Severity = ErrorSeverity.High,
                CorrectiveAction = (context) =>
                {
                    Log("No window found - retrying detection");
                    return new CorrectionResult
                    {
                        Success = true,
                        Message = "Retrying window detection with increased delay"
                    };
                }
            });
        }

        /// <summary>
        /// Add a correction rule
        /// </summary>
        public void AddRule(CorrectionRule rule)
        {
            _correctionRules.Add(rule);
            Log($"Correction rule added: {rule.CorrectionAction}");
        }

        /// <summary>
        /// Attempt to detect and correct an error
        /// </summary>
        public CorrectionAttempt AttemptCorrection(string errorMessage, string context = "")
        {
            Log($"Attempting correction for: {errorMessage}");

            // Record error frequency
            if (!_errorFrequency.ContainsKey(errorMessage))
            {
                _errorFrequency[errorMessage] = 0;
            }
            _errorFrequency[errorMessage]++;

            // Find matching rules
            var matchingRules = _correctionRules
                .Where(r => System.Text.RegularExpressions.Regex.IsMatch(errorMessage, r.ErrorPattern, 
                    System.Text.RegularExpressions.RegexOptions.IgnoreCase))
                .OrderByDescending(r => r.Severity)
                .ToList();

            if (!matchingRules.Any())
            {
                Log("No matching correction rules found");
                return new CorrectionAttempt
                {
                    Success = false,
                    Message = "No automatic correction available",
                    ErrorMessage = errorMessage
                };
            }

            // Try each matching rule
            foreach (var rule in matchingRules)
            {
                // Check retry limit
                var previousAttempts = _correctionHistory.Count(h => h.ErrorPattern == rule.ErrorPattern);
                if (previousAttempts >= rule.MaxRetries)
                {
                    Log($"Max retries ({rule.MaxRetries}) reached for rule: {rule.CorrectionAction}");
                    continue;
                }

                // Check if auto-apply
                if (!rule.AutoApply)
                {
                    Log($"Rule requires manual approval: {rule.CorrectionAction}");
                    return new CorrectionAttempt
                    {
                        Success = false,
                        Message = "Manual approval required",
                        Recommendation = rule.CorrectionAction,
                        RequiresApproval = true,
                        ErrorMessage = errorMessage
                    };
                }

                // Apply correction
                try
                {
                    var result = rule.CorrectiveAction?.Invoke(context);

                    if (result?.Success == true)
                    {
                        // Record successful correction
                        var record = new CorrectionRecord
                        {
                            Timestamp = DateTime.UtcNow,
                            ErrorMessage = errorMessage,
                            ErrorPattern = rule.ErrorPattern,
                            CorrectionAction = rule.CorrectionAction,
                            Result = result.Message,
                            Success = true
                        };

                        _correctionHistory.Add(record);

                        // Maintain max history
                        if (_correctionHistory.Count > _maxHistory)
                        {
                            _correctionHistory.RemoveAt(0);
                        }

                        // Record in cause-effect tracker
                        _causeEffectTracker.RecordCauseEffect(
                            errorMessage,
                            rule.CorrectionAction,
                            OutcomeType.Success,
                            context
                        );

                        OnCorrectionApplied?.Invoke(this, record);

                        Log($"Correction applied successfully: {rule.CorrectionAction}");

                        return new CorrectionAttempt
                        {
                            Success = true,
                            Message = result.Message,
                            CorrectionApplied = rule.CorrectionAction,
                            ErrorMessage = errorMessage
                        };
                    }
                }
                catch (Exception ex)
                {
                    Log($"Correction failed with exception: {ex.Message}");

                    // Record failed correction
                    var record = new CorrectionRecord
                    {
                        Timestamp = DateTime.UtcNow,
                        ErrorMessage = errorMessage,
                        ErrorPattern = rule.ErrorPattern,
                        CorrectionAction = rule.CorrectionAction,
                        Result = ex.Message,
                        Success = false
                    };

                    _correctionHistory.Add(record);

                    _causeEffectTracker.RecordCauseEffect(
                        errorMessage,
                        $"Correction attempt: {rule.CorrectionAction}",
                        OutcomeType.Failure,
                        ex.Message
                    );
                }
            }

            Log("All correction attempts exhausted");
            return new CorrectionAttempt
            {
                Success = false,
                Message = "All correction attempts failed",
                ErrorMessage = errorMessage
            };
        }

        /// <summary>
        /// Learn from manual corrections
        /// </summary>
        public void LearnFromManualCorrection(string errorMessage, string manualAction, bool successful)
        {
            Log($"Learning from manual correction: {manualAction} (success: {successful})");

            var record = new CorrectionRecord
            {
                Timestamp = DateTime.UtcNow,
                ErrorMessage = errorMessage,
                ErrorPattern = errorMessage,
                CorrectionAction = manualAction,
                Result = successful ? "Manual correction successful" : "Manual correction failed",
                Success = successful,
                ManualCorrection = true
            };

            _correctionHistory.Add(record);

            _causeEffectTracker.RecordCauseEffect(
                errorMessage,
                manualAction,
                successful ? OutcomeType.Success : OutcomeType.Failure,
                "Manual correction"
            );

            // If successful and frequent error, suggest creating automatic rule
            if (successful && _errorFrequency.GetValueOrDefault(errorMessage, 0) >= 3)
            {
                OnSuggestNewRule?.Invoke(this, new RuleSuggestion
                {
                    ErrorPattern = errorMessage,
                    SuggestedAction = manualAction,
                    Frequency = _errorFrequency[errorMessage]
                });
            }
        }

        /// <summary>
        /// Get correction effectiveness report
        /// </summary>
        public CorrectionReport GetCorrectionReport()
        {
            var totalAttempts = _correctionHistory.Count;
            var successfulCorrections = _correctionHistory.Count(r => r.Success);
            var failedCorrections = totalAttempts - successfulCorrections;

            var report = new CorrectionReport
            {
                TotalAttempts = totalAttempts,
                SuccessfulCorrections = successfulCorrections,
                FailedCorrections = failedCorrections,
                SuccessRate = totalAttempts > 0 ? (double)successfulCorrections / totalAttempts : 0,
                MostCommonErrors = _errorFrequency
                    .OrderByDescending(kvp => kvp.Value)
                    .Take(10)
                    .ToDictionary(kvp => kvp.Key, kvp => kvp.Value),
                RecentCorrections = _correctionHistory.TakeLast(20).ToList()
            };

            return report;
        }

        /// <summary>
        /// Get most effective corrections
        /// </summary>
        public List<CorrectionEffectiveness> GetMostEffectiveCorrections()
        {
            return _correctionHistory
                .GroupBy(r => r.CorrectionAction)
                .Select(g => new CorrectionEffectiveness
                {
                    CorrectionAction = g.Key,
                    TotalAttempts = g.Count(),
                    SuccessfulAttempts = g.Count(r => r.Success),
                    SuccessRate = g.Count() > 0 ? (double)g.Count(r => r.Success) / g.Count() : 0
                })
                .OrderByDescending(e => e.SuccessRate)
                .ThenByDescending(e => e.TotalAttempts)
                .Take(10)
                .ToList();
        }

        private void Log(string message)
        {
            OnLog?.Invoke(this, $"[SelfCorrect] {message}");
        }

        public event EventHandler<CorrectionRecord>? OnCorrectionApplied;
        public event EventHandler<RuleSuggestion>? OnSuggestNewRule;
        public event EventHandler<string>? OnLog;

        public int TotalCorrections => _correctionHistory.Count;
        public int ActiveRules => _correctionRules.Count;
    }

    public class CorrectionRule
    {
        public string ErrorPattern { get; set; } = string.Empty;
        public string CorrectionAction { get; set; } = string.Empty;
        public bool AutoApply { get; set; }
        public int MaxRetries { get; set; } = 3;
        public ErrorSeverity Severity { get; set; } = ErrorSeverity.Medium;
        public Func<string, CorrectionResult>? CorrectiveAction { get; set; }
    }

    public class CorrectionRecord
    {
        public DateTime Timestamp { get; set; }
        public string ErrorMessage { get; set; } = string.Empty;
        public string ErrorPattern { get; set; } = string.Empty;
        public string CorrectionAction { get; set; } = string.Empty;
        public string Result { get; set; } = string.Empty;
        public bool Success { get; set; }
        public bool ManualCorrection { get; set; }
    }

    public class CorrectionResult
    {
        public bool Success { get; set; }
        public string Message { get; set; } = string.Empty;
        public string NewValue { get; set; } = string.Empty;
        public bool Recommendation { get; set; }
    }

    public class CorrectionAttempt
    {
        public bool Success { get; set; }
        public string Message { get; set; } = string.Empty;
        public string CorrectionApplied { get; set; } = string.Empty;
        public string Recommendation { get; set; } = string.Empty;
        public bool RequiresApproval { get; set; }
        public string ErrorMessage { get; set; } = string.Empty;
    }

    public class CorrectionReport
    {
        public int TotalAttempts { get; set; }
        public int SuccessfulCorrections { get; set; }
        public int FailedCorrections { get; set; }
        public double SuccessRate { get; set; }
        public Dictionary<string, int> MostCommonErrors { get; set; } = new Dictionary<string, int>();
        public List<CorrectionRecord> RecentCorrections { get; set; } = new List<CorrectionRecord>();
    }

    public class CorrectionEffectiveness
    {
        public string CorrectionAction { get; set; } = string.Empty;
        public int TotalAttempts { get; set; }
        public int SuccessfulAttempts { get; set; }
        public double SuccessRate { get; set; }
    }

    public class RuleSuggestion
    {
        public string ErrorPattern { get; set; } = string.Empty;
        public string SuggestedAction { get; set; } = string.Empty;
        public int Frequency { get; set; }
    }

    public enum ErrorSeverity
    {
        Low,
        Medium,
        High,
        Critical
    }
}
