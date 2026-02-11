using System;
using System.Collections.Generic;
using System.Linq;

namespace Trust.Core
{
    /// <summary>
    /// Intent validation and enforcement system
    /// Ensures all actions align with declared intent and prevents drift
    /// </summary>
    public class IntentValidator
    {
        private readonly CauseEffectTracker _causeEffectTracker;
        private readonly List<IntentRule> _intentRules;
        private readonly List<IntentViolation> _violations;
        private readonly Dictionary<string, int> _violationCount;

        public IntentValidator(CauseEffectTracker causeEffectTracker)
        {
            _causeEffectTracker = causeEffectTracker;
            _intentRules = new List<IntentRule>();
            _violations = new List<IntentViolation>();
            _violationCount = new Dictionary<string, int>();

            InitializeDefaultIntentRules();
        }

        /// <summary>
        /// Initialize default intent validation rules
        /// </summary>
        private void InitializeDefaultIntentRules()
        {
            // Intent: Click execution must reach target application
            AddIntentRule(new IntentRule
            {
                Name = "Click Must Execute",
                Description = "Intercepted clicks must be executed in target application",
                ValidationCheck = (action, outcome) =>
                {
                    if (action.Contains("Click Intercepted", StringComparison.OrdinalIgnoreCase))
                    {
                        return outcome.Contains("SendInput.*result = 1", StringComparison.OrdinalIgnoreCase) ||
                               outcome.Contains("CLICK EXECUTION COMPLETE", StringComparison.OrdinalIgnoreCase);
                    }
                    return true; // Not applicable
                },
                Severity = ViolationSeverity.High,
                MitigationStrategy = "Verify SendInput API calls and increase execution delays"
            });

            // Intent: Overlay must not block user interaction in click-through mode
            AddIntentRule(new IntentRule
            {
                Name = "Click-Through Transparency",
                Description = "Overlay must allow clicks to pass through when not intercepting",
                ValidationCheck = (action, outcome) =>
                {
                    if (action.Contains("Click-through mode", StringComparison.OrdinalIgnoreCase))
                    {
                        return !outcome.Contains("blocked", StringComparison.OrdinalIgnoreCase) &&
                               !outcome.Contains("intercepted unintentionally", StringComparison.OrdinalIgnoreCase);
                    }
                    return true;
                },
                Severity = ViolationSeverity.Critical,
                MitigationStrategy = "Verify WS_EX_TRANSPARENT window style is set"
            });

            // Intent: All data must be processed through structural identity
            AddIntentRule(new IntentRule
            {
                Name = "Structural Identity Required",
                Description = "All intercepted data must be processed for structural identity",
                ValidationCheck = (action, outcome) =>
                {
                    if (action.Contains("Click Intercepted", StringComparison.OrdinalIgnoreCase) ||
                        action.Contains("Data Ingested", StringComparison.OrdinalIgnoreCase))
                    {
                        return outcome.Contains("Structural ID", StringComparison.OrdinalIgnoreCase) ||
                               outcome.Contains("StructuralIdentityEngine", StringComparison.OrdinalIgnoreCase);
                    }
                    return true;
                },
                Severity = ViolationSeverity.High,
                MitigationStrategy = "Ensure ExecutionEngine.ProcessInterceptedData is called"
            });

            // Intent: No duplicate bricks in ledger
            AddIntentRule(new IntentRule
            {
                Name = "Deduplication Enforcement",
                Description = "Ledger must not contain duplicate structural IDs",
                ValidationCheck = (action, outcome) =>
                {
                    if (action.Contains("Ingest", StringComparison.OrdinalIgnoreCase))
                    {
                        return outcome.Contains("Known pattern", StringComparison.OrdinalIgnoreCase) ||
                               outcome.Contains("New structural pattern", StringComparison.OrdinalIgnoreCase);
                    }
                    return true;
                },
                Severity = ViolationSeverity.Medium,
                MitigationStrategy = "Verify InvariantLedger deduplication logic"
            });

            // Intent: User privacy - no data leaves the system
            AddIntentRule(new IntentRule
            {
                Name = "Data Locality",
                Description = "All data must remain local - no external transmission",
                ValidationCheck = (action, outcome) =>
                {
                    // Check for network-related keywords
                    var networkKeywords = new[] { "http", "network", "upload", "send", "transmit", "remote" };
                    return !networkKeywords.Any(kw => 
                        action.Contains(kw, StringComparison.OrdinalIgnoreCase) ||
                        outcome.Contains(kw, StringComparison.OrdinalIgnoreCase));
                },
                Severity = ViolationSeverity.Critical,
                MitigationStrategy = "Remove any network communication code"
            });

            // Intent: Overlay must restore visibility after errors
            AddIntentRule(new IntentRule
            {
                Name = "Overlay Recovery",
                Description = "Overlay must become visible again even after errors",
                ValidationCheck = (action, outcome) =>
                {
                    if (action.Contains("ExecuteUnderlyingClick", StringComparison.OrdinalIgnoreCase))
                    {
                        return outcome.Contains("visibility restored", StringComparison.OrdinalIgnoreCase) ||
                               outcome.Contains("Visibility = Visible", StringComparison.OrdinalIgnoreCase) ||
                               !outcome.Contains("ERROR", StringComparison.OrdinalIgnoreCase);
                    }
                    return true;
                },
                Severity = ViolationSeverity.High,
                MitigationStrategy = "Ensure finally block restores overlay visibility"
            });
        }

        /// <summary>
        /// Add an intent validation rule
        /// </summary>
        public void AddIntentRule(IntentRule rule)
        {
            _intentRules.Add(rule);
            Log($"Intent rule added: {rule.Name}");
        }

        /// <summary>
        /// Validate an action against intent rules
        /// </summary>
        public IntentValidationResult ValidateIntent(string action, string outcome, string context = "")
        {
            var result = new IntentValidationResult
            {
                Action = action,
                Outcome = outcome,
                Timestamp = DateTime.UtcNow
            };

            foreach (var rule in _intentRules)
            {
                try
                {
                    var isValid = rule.ValidationCheck(action, outcome);

                    if (!isValid)
                    {
                        var violation = new IntentViolation
                        {
                            Timestamp = DateTime.UtcNow,
                            RuleName = rule.Name,
                            RuleDescription = rule.Description,
                            Action = action,
                            Outcome = outcome,
                            Context = context,
                            Severity = rule.Severity,
                            MitigationStrategy = rule.MitigationStrategy
                        };

                        _violations.Add(violation);
                        result.Violations.Add(violation);

                        // Track violation count
                        if (!_violationCount.ContainsKey(rule.Name))
                        {
                            _violationCount[rule.Name] = 0;
                        }
                        _violationCount[rule.Name]++;

                        // Record in cause-effect tracker as harmful
                        _causeEffectTracker.RecordCauseEffect(
                            action,
                            $"Intent violation: {rule.Name}",
                            OutcomeType.Harmful,
                            context
                        );

                        Log($"Intent violation detected: {rule.Name}");
                        OnIntentViolation?.Invoke(this, violation);
                    }
                }
                catch (Exception ex)
                {
                    Log($"Error validating rule {rule.Name}: {ex.Message}");
                }
            }

            result.IsValid = !result.Violations.Any();

            if (result.IsValid)
            {
                // Record successful intent validation
                _causeEffectTracker.RecordCauseEffect(
                    action,
                    "Intent validated successfully",
                    OutcomeType.Success,
                    context
                );
            }

            return result;
        }

        /// <summary>
        /// Check if an action should be blocked based on intent violations
        /// </summary>
        public bool ShouldBlockAction(string action)
        {
            // Check if action has high frequency of critical violations
            var recentViolations = _violations
                .Where(v => v.Timestamp > DateTime.UtcNow.AddMinutes(-5))
                .Where(v => v.Action.Contains(action, StringComparison.OrdinalIgnoreCase))
                .Where(v => v.Severity == ViolationSeverity.Critical)
                .ToList();

            if (recentViolations.Count >= 3)
            {
                Log($"Blocking action due to repeated critical violations: {action}");
                return true;
            }

            return false;
        }

        /// <summary>
        /// Get intent compliance report
        /// </summary>
        public IntentComplianceReport GetComplianceReport()
        {
            var totalValidations = _violations.Count > 0 ? _violations.Count : 1; // Avoid division by zero

            var report = new IntentComplianceReport
            {
                TotalViolations = _violations.Count,
                CriticalViolations = _violations.Count(v => v.Severity == ViolationSeverity.Critical),
                HighViolations = _violations.Count(v => v.Severity == ViolationSeverity.High),
                MediumViolations = _violations.Count(v => v.Severity == ViolationSeverity.Medium),
                LowViolations = _violations.Count(v => v.Severity == ViolationSeverity.Low),
                MostViolatedRules = _violationCount
                    .OrderByDescending(kvp => kvp.Value)
                    .Take(10)
                    .ToDictionary(kvp => kvp.Key, kvp => kvp.Value),
                RecentViolations = _violations.TakeLast(20).ToList(),
                ComplianceScore = totalValidations > 0 ? 
                    Math.Max(0, 100 - (_violations.Count * 5)) : 100
            };

            return report;
        }

        /// <summary>
        /// Get mitigation strategies for active violations
        /// </summary>
        public List<string> GetMitigationStrategies()
        {
            var recentViolations = _violations
                .Where(v => v.Timestamp > DateTime.UtcNow.AddMinutes(-10))
                .GroupBy(v => v.RuleName)
                .Select(g => g.First())
                .OrderByDescending(v => v.Severity)
                .ToList();

            return recentViolations.Select(v => 
                $"[{v.Severity}] {v.RuleName}: {v.MitigationStrategy}"
            ).ToList();
        }

        /// <summary>
        /// Clear violation history
        /// </summary>
        public void ClearViolations()
        {
            _violations.Clear();
            _violationCount.Clear();
            Log("Violation history cleared");
        }

        private void Log(string message)
        {
            OnLog?.Invoke(this, $"[Intent] {message}");
        }

        public event EventHandler<IntentViolation>? OnIntentViolation;
        public event EventHandler<string>? OnLog;

        public int TotalViolations => _violations.Count;
        public int ActiveRules => _intentRules.Count;
    }

    public class IntentRule
    {
        public string Name { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public Func<string, string, bool> ValidationCheck { get; set; } = (a, o) => true;
        public ViolationSeverity Severity { get; set; } = ViolationSeverity.Medium;
        public string MitigationStrategy { get; set; } = string.Empty;
    }

    public class IntentViolation
    {
        public DateTime Timestamp { get; set; }
        public string RuleName { get; set; } = string.Empty;
        public string RuleDescription { get; set; } = string.Empty;
        public string Action { get; set; } = string.Empty;
        public string Outcome { get; set; } = string.Empty;
        public string Context { get; set; } = string.Empty;
        public ViolationSeverity Severity { get; set; }
        public string MitigationStrategy { get; set; } = string.Empty;
    }

    public class IntentValidationResult
    {
        public string Action { get; set; } = string.Empty;
        public string Outcome { get; set; } = string.Empty;
        public DateTime Timestamp { get; set; }
        public bool IsValid { get; set; }
        public List<IntentViolation> Violations { get; set; } = new List<IntentViolation>();
    }

    public class IntentComplianceReport
    {
        public int TotalViolations { get; set; }
        public int CriticalViolations { get; set; }
        public int HighViolations { get; set; }
        public int MediumViolations { get; set; }
        public int LowViolations { get; set; }
        public Dictionary<string, int> MostViolatedRules { get; set; } = new Dictionary<string, int>();
        public List<IntentViolation> RecentViolations { get; set; } = new List<IntentViolation>();
        public double ComplianceScore { get; set; }
    }

    public enum ViolationSeverity
    {
        Low,
        Medium,
        High,
        Critical
    }
}
