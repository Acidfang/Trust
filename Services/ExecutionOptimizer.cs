using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using Trust.Core;

namespace Trust.Services
{
    /// <summary>
    /// Advanced execution optimizer using structural identity analysis
    /// </summary>
    public class ExecutionOptimizer
    {
        private readonly InvariantLedger _ledger;
        private readonly StructuralIdentityEngine _identityEngine;
        private readonly Dictionary<string, ExecutionCache> _executionCache;

        public ExecutionOptimizer(InvariantLedger ledger)
        {
            _ledger = ledger;
            _identityEngine = new StructuralIdentityEngine();
            _executionCache = new Dictionary<string, ExecutionCache>();
        }

        /// <summary>
        /// Execute with structural deduplication - if identical structure seen before, return cached result
        /// </summary>
        public OptimizedExecutionResult ExecuteWithDeduplication<T>(
            byte[] inputData,
            Func<byte[], T> executionFunc,
            string context)
        {
            var sw = Stopwatch.StartNew();

            var identityResult = _identityEngine.ComputeStructuralId(inputData);
            string structuralId = identityResult.StructuralId;

            if (_executionCache.TryGetValue(structuralId, out var cached))
            {
                sw.Stop();
                return new OptimizedExecutionResult
                {
                    StructuralId = structuralId,
                    WasCached = true,
                    ExecutionTimeMs = sw.ElapsedMilliseconds,
                    CacheHitCount = cached.HitCount + 1,
                    IsBlackBrick = identityResult.IsBlackBrick,
                    Result = cached.Result
                };
            }

            var result = executionFunc(inputData);
            sw.Stop();

            _executionCache[structuralId] = new ExecutionCache
            {
                StructuralId = structuralId,
                Result = result,
                HitCount = 0,
                FirstExecutionTimeMs = sw.ElapsedMilliseconds,
                Context = context
            };

            _ledger.Ingest(inputData, context);

            return new OptimizedExecutionResult
            {
                StructuralId = structuralId,
                WasCached = false,
                ExecutionTimeMs = sw.ElapsedMilliseconds,
                CacheHitCount = 0,
                IsBlackBrick = identityResult.IsBlackBrick,
                Result = result
            };
        }

        /// <summary>
        /// Analyze execution patterns for stillness metrics
        /// </summary>
        public StillnessMetrics AnalyzeStillness()
        {
            var stats = _ledger.GetStatistics();
            
            return new StillnessMetrics
            {
                TotalBricks = stats.TotalBricks,
                TotalIngests = stats.TotalIngests,
                StillnessRatio = 1 - stats.CompressionRatio,
                CacheHitRate = CalculateCacheHitRate(),
                AverageEntropy = stats.AverageEntropy,
                BlackBrickPercentage = stats.BlackBrickCount / (double)Math.Max(1, stats.TotalBricks) * 100
            };
        }

        /// <summary>
        /// Predict if new data will create a new brick (useful for optimization decisions)
        /// </summary>
        public BrickPrediction PredictBrickCreation(byte[] data)
        {
            var identityResult = _identityEngine.ComputeStructuralId(data);
            var existingBrick = _ledger.RetrieveBrick(identityResult.StructuralId);

            return new BrickPrediction
            {
                StructuralId = identityResult.StructuralId,
                WillCreateNewBrick = existingBrick == null,
                Entropy = identityResult.Entropy,
                IsBlackBrick = identityResult.IsBlackBrick,
                TransformApplied = identityResult.TransformApplied,
                ExistingReferenceCount = existingBrick?.ReferenceCount ?? 0
            };
        }

        /// <summary>
        /// Find structurally similar bricks in the ledger
        /// </summary>
        public List<SimilarityMatch> FindSimilarBricks(byte[] data, int topN = 5)
        {
            var targetIdentity = _identityEngine.ComputeStructuralId(data);
            var allBricks = _ledger.GetAllBricks().ToList();

            var similarities = allBricks
                .Select(brick => new SimilarityMatch
                {
                    StructuralId = brick.StructuralId,
                    SimilarityScore = CalculateSimilarity(targetIdentity.CanonicalForm, brick.CanonicalForm),
                    Entropy = brick.Entropy,
                    TransformApplied = brick.TransformApplied,
                    ReferenceCount = brick.ReferenceCount
                })
                .OrderByDescending(s => s.SimilarityScore)
                .Take(topN)
                .ToList();

            return similarities;
        }

        private double CalculateCacheHitRate()
        {
            if (_executionCache.Count == 0)
                return 0;

            int totalHits = _executionCache.Values.Sum(c => c.HitCount);
            return totalHits / (double)(_executionCache.Count + totalHits);
        }

        private double CalculateSimilarity(byte[] a, byte[] b)
        {
            if (a.Length == 0 || b.Length == 0)
                return 0;

            int minLength = Math.Min(a.Length, b.Length);
            int matches = 0;

            for (int i = 0; i < minLength; i++)
            {
                if (a[i] == b[i])
                    matches++;
            }

            return matches / (double)Math.Max(a.Length, b.Length);
        }
    }

    public class ExecutionCache
    {
        public string StructuralId { get; set; } = string.Empty;
        public object? Result { get; set; }
        public int HitCount { get; set; }
        public long FirstExecutionTimeMs { get; set; }
        public string Context { get; set; } = string.Empty;
    }

    public class OptimizedExecutionResult
    {
        public string StructuralId { get; set; } = string.Empty;
        public bool WasCached { get; set; }
        public long ExecutionTimeMs { get; set; }
        public int CacheHitCount { get; set; }
        public bool IsBlackBrick { get; set; }
        public object? Result { get; set; }
    }

    public class StillnessMetrics
    {
        public long TotalBricks { get; set; }
        public long TotalIngests { get; set; }
        public double StillnessRatio { get; set; }
        public double CacheHitRate { get; set; }
        public double AverageEntropy { get; set; }
        public double BlackBrickPercentage { get; set; }
    }

    public class BrickPrediction
    {
        public string StructuralId { get; set; } = string.Empty;
        public bool WillCreateNewBrick { get; set; }
        public double Entropy { get; set; }
        public bool IsBlackBrick { get; set; }
        public string TransformApplied { get; set; } = string.Empty;
        public int ExistingReferenceCount { get; set; }
    }

    public class SimilarityMatch
    {
        public string StructuralId { get; set; } = string.Empty;
        public double SimilarityScore { get; set; }
        public double Entropy { get; set; }
        public string TransformApplied { get; set; } = string.Empty;
        public int ReferenceCount { get; set; }
    }
}
