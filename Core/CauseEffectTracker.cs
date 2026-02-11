using System;
using System.Collections.Generic;
using System.Linq;

namespace Trust.Core
{
    /// <summary>
    /// Tracks cause-and-effect relationships between actions and outcomes
    /// Enables the system to learn from its behavior and predict consequences
    /// </summary>
    public class CauseEffectTracker
    {
        private readonly List<CauseEffectRecord> _records;
        private readonly Dictionary<string, List<string>> _causeToEffects;
        private readonly Dictionary<string, OutcomeStatistics> _outcomeStats;
        private readonly int _maxRecords = 10000;

        public CauseEffectTracker()
        {
            _records = new List<CauseEffectRecord>();
            _causeToEffects = new Dictionary<string, List<string>>();
            _outcomeStats = new Dictionary<string, OutcomeStatistics>();
        }

        /// <summary>
        /// Record a cause-and-effect relationship
        /// </summary>
        public void RecordCauseEffect(string cause, string effect, OutcomeType outcomeType, string context = "")
        {
            var record = new CauseEffectRecord
            {
                Timestamp = DateTime.UtcNow,
                Cause = cause,
                Effect = effect,
                OutcomeType = outcomeType,
                Context = context
            };

            _records.Add(record);

            // Maintain max records
            if (_records.Count > _maxRecords)
            {
                _records.RemoveAt(0);
            }

            // Update cause-to-effects mapping
            if (!_causeToEffects.ContainsKey(cause))
            {
                _causeToEffects[cause] = new List<string>();
            }
            _causeToEffects[cause].Add(effect);

            // Update outcome statistics
            var key = $"{cause}:{effect}";
            if (!_outcomeStats.ContainsKey(key))
            {
                _outcomeStats[key] = new OutcomeStatistics();
            }

            var stats = _outcomeStats[key];
            stats.TotalOccurrences++;

            switch (outcomeType)
            {
                case OutcomeType.Success:
                    stats.SuccessCount++;
                    break;
                case OutcomeType.Failure:
                    stats.FailureCount++;
                    break;
                case OutcomeType.Warning:
                    stats.WarningCount++;
                    break;
                case OutcomeType.Harmful:
                    stats.HarmfulCount++;
                    break;
            }

            OnCauseEffectRecorded?.Invoke(this, record);
        }

        /// <summary>
        /// Predict likely effects of a given cause based on historical data
        /// </summary>
        public List<EffectPrediction> PredictEffects(string cause)
        {
            var predictions = new List<EffectPrediction>();

            if (!_causeToEffects.ContainsKey(cause))
            {
                return predictions;
            }

            var effects = _causeToEffects[cause];
            var effectGroups = effects.GroupBy(e => e);

            foreach (var group in effectGroups.OrderByDescending(g => g.Count()))
            {
                var effect = group.Key;
                var key = $"{cause}:{effect}";

                if (_outcomeStats.ContainsKey(key))
                {
                    var stats = _outcomeStats[key];
                    var probability = (double)group.Count() / effects.Count;

                    predictions.Add(new EffectPrediction
                    {
                        Effect = effect,
                        Probability = probability,
                        SuccessRate = stats.SuccessRate,
                        HarmfulRate = stats.HarmfulRate,
                        Statistics = stats
                    });
                }
            }

            return predictions;
        }

        /// <summary>
        /// Determine if a cause is likely to be harmful
        /// </summary>
        public bool IsLikelyHarmful(string cause, double threshold = 0.1)
        {
            var predictions = PredictEffects(cause);

            if (!predictions.Any())
            {
                // Unknown action - conservative approach
                return false;
            }

            // Check if any predicted effect has high harmful rate
            return predictions.Any(p => p.HarmfulRate > threshold);
        }

        /// <summary>
        /// Get recommendations for avoiding harmful outcomes
        /// </summary>
        public List<string> GetSafetyRecommendations(string cause)
        {
            var recommendations = new List<string>();
            var predictions = PredictEffects(cause);

            foreach (var prediction in predictions.Where(p => p.HarmfulRate > 0))
            {
                recommendations.Add(
                    $"Warning: {prediction.Effect} has occurred {prediction.Statistics.HarmfulCount} times " +
                    $"({prediction.HarmfulRate:P1} harmful rate) when performing '{cause}'"
                );
            }

            // Find alternative causes that achieve similar effects with lower harm rates
            var desiredEffects = predictions.Where(p => p.SuccessRate > 0.5).Select(p => p.Effect).ToList();
            var alternatives = FindSaferAlternatives(cause, desiredEffects);

            if (alternatives.Any())
            {
                recommendations.Add("Safer alternatives detected:");
                recommendations.AddRange(alternatives.Select(alt => $"  - {alt.Cause} (harm rate: {alt.HarmRate:P1})"));
            }

            return recommendations;
        }

        /// <summary>
        /// Find alternative causes that produce similar effects with lower harm rates
        /// </summary>
        private List<AlternativeCause> FindSaferAlternatives(string originalCause, List<string> desiredEffects)
        {
            var alternatives = new List<AlternativeCause>();

            foreach (var kvp in _causeToEffects)
            {
                if (kvp.Key == originalCause)
                    continue;

                var causeEffects = kvp.Value.Distinct().ToList();
                var matchCount = desiredEffects.Count(e => causeEffects.Contains(e));

                if (matchCount > 0)
                {
                    var predictions = PredictEffects(kvp.Key);
                    var harmRate = predictions.Any() ? predictions.Average(p => p.HarmfulRate) : 0;

                    var originalHarmRate = PredictEffects(originalCause).Any()
                        ? PredictEffects(originalCause).Average(p => p.HarmfulRate)
                        : 0;

                    if (harmRate < originalHarmRate)
                    {
                        alternatives.Add(new AlternativeCause
                        {
                            Cause = kvp.Key,
                            MatchingEffects = matchCount,
                            HarmRate = harmRate
                        });
                    }
                }
            }

            return alternatives.OrderBy(a => a.HarmRate).ThenByDescending(a => a.MatchingEffects).Take(3).ToList();
        }

        /// <summary>
        /// Get recent records for analysis
        /// </summary>
        public List<CauseEffectRecord> GetRecentRecords(int count = 100)
        {
            return _records.TakeLast(count).ToList();
        }

        /// <summary>
        /// Get records matching a pattern
        /// </summary>
        public List<CauseEffectRecord> GetRecordsByPattern(string causePattern = null, string effectPattern = null, OutcomeType? outcomeType = null)
        {
            return _records.Where(r =>
                (causePattern == null || r.Cause.Contains(causePattern, StringComparison.OrdinalIgnoreCase)) &&
                (effectPattern == null || r.Effect.Contains(effectPattern, StringComparison.OrdinalIgnoreCase)) &&
                (outcomeType == null || r.OutcomeType == outcomeType.Value)
            ).ToList();
        }

        /// <summary>
        /// Clear all tracking data
        /// </summary>
        public void Clear()
        {
            _records.Clear();
            _causeToEffects.Clear();
            _outcomeStats.Clear();
        }

        public event EventHandler<CauseEffectRecord>? OnCauseEffectRecorded;

        public int RecordCount => _records.Count;
        public int UniqueCauses => _causeToEffects.Count;
    }

    public class CauseEffectRecord
    {
        public DateTime Timestamp { get; set; }
        public string Cause { get; set; } = string.Empty;
        public string Effect { get; set; } = string.Empty;
        public OutcomeType OutcomeType { get; set; }
        public string Context { get; set; } = string.Empty;
    }

    public class OutcomeStatistics
    {
        public int TotalOccurrences { get; set; }
        public int SuccessCount { get; set; }
        public int FailureCount { get; set; }
        public int WarningCount { get; set; }
        public int HarmfulCount { get; set; }

        public double SuccessRate => TotalOccurrences > 0 ? (double)SuccessCount / TotalOccurrences : 0;
        public double FailureRate => TotalOccurrences > 0 ? (double)FailureCount / TotalOccurrences : 0;
        public double WarningRate => TotalOccurrences > 0 ? (double)WarningCount / TotalOccurrences : 0;
        public double HarmfulRate => TotalOccurrences > 0 ? (double)HarmfulCount / TotalOccurrences : 0;
    }

    public class EffectPrediction
    {
        public string Effect { get; set; } = string.Empty;
        public double Probability { get; set; }
        public double SuccessRate { get; set; }
        public double HarmfulRate { get; set; }
        public OutcomeStatistics Statistics { get; set; } = new OutcomeStatistics();
    }

    public class AlternativeCause
    {
        public string Cause { get; set; } = string.Empty;
        public int MatchingEffects { get; set; }
        public double HarmRate { get; set; }
    }

    public enum OutcomeType
    {
        Success,
        Failure,
        Warning,
        Harmful
    }
}
