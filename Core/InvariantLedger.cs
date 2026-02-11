using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;

namespace Trust.Core
{
    /// <summary>
    /// History-independent ledger implementing deterministic trie structure
    /// </summary>
    public class InvariantLedger
    {
        private readonly ConcurrentDictionary<string, BrickEntry> _ledger;
        private readonly StructuralIdentityEngine _identityEngine;
        private long _totalIngestCount;
        private long _uniqueBrickCount;

        public InvariantLedger()
        {
            _ledger = new ConcurrentDictionary<string, BrickEntry>();
            _identityEngine = new StructuralIdentityEngine();
        }

        public LedgerIngestResult Ingest(byte[] bitstream, string? metadata = null)
        {
            _totalIngestCount++;

            var identityResult = _identityEngine.ComputeStructuralId(bitstream);
            var result = new LedgerIngestResult
            {
                StructuralId = identityResult.StructuralId,
                IsBlackBrick = identityResult.IsBlackBrick,
                Entropy = identityResult.Entropy,
                TransformApplied = identityResult.TransformApplied,
                OriginalLength = identityResult.OriginalLength,
                IngestTimestamp = DateTime.UtcNow
            };

            bool isNew = _ledger.TryAdd(identityResult.StructuralId, new BrickEntry
            {
                StructuralId = identityResult.StructuralId,
                CanonicalForm = identityResult.CanonicalForm,
                TransformApplied = identityResult.TransformApplied,
                IsBlackBrick = identityResult.IsBlackBrick,
                Entropy = identityResult.Entropy,
                FirstSeenUtc = DateTime.UtcNow,
                ReferenceCount = 1,
                Metadata = metadata
            });

            if (isNew)
            {
                _uniqueBrickCount++;
                result.IsNewBrick = true;
            }
            else
            {
                _ledger[identityResult.StructuralId].ReferenceCount++;
                result.IsNewBrick = false;
            }

            result.TotalBrickCount = _uniqueBrickCount;
            result.TotalIngestCount = _totalIngestCount;

            return result;
        }

        public BrickEntry? RetrieveBrick(string structuralId)
        {
            return _ledger.TryGetValue(structuralId, out var entry) ? entry : null;
        }

        public LedgerStatistics GetStatistics()
        {
            return new LedgerStatistics
            {
                TotalBricks = _uniqueBrickCount,
                TotalIngests = _totalIngestCount,
                BlackBrickCount = _ledger.Values.Count(b => b.IsBlackBrick),
                AverageEntropy = _ledger.Values.Any() ? _ledger.Values.Average(b => b.Entropy) : 0,
                CompressionRatio = _totalIngestCount > 0 ? (double)_uniqueBrickCount / _totalIngestCount : 0
            };
        }

        public IEnumerable<BrickEntry> GetAllBricks()
        {
            return _ledger.Values.OrderBy(b => b.StructuralId);
        }
    }

    public class BrickEntry
    {
        public string StructuralId { get; set; } = string.Empty;
        public byte[] CanonicalForm { get; set; } = Array.Empty<byte>();
        public string TransformApplied { get; set; } = string.Empty;
        public bool IsBlackBrick { get; set; }
        public double Entropy { get; set; }
        public DateTime FirstSeenUtc { get; set; }
        public int ReferenceCount { get; set; }
        public string? Metadata { get; set; }
    }

    public class LedgerIngestResult
    {
        public string StructuralId { get; set; } = string.Empty;
        public bool IsNewBrick { get; set; }
        public bool IsBlackBrick { get; set; }
        public double Entropy { get; set; }
        public string TransformApplied { get; set; } = string.Empty;
        public int OriginalLength { get; set; }
        public long TotalBrickCount { get; set; }
        public long TotalIngestCount { get; set; }
        public DateTime IngestTimestamp { get; set; }
    }

    public class LedgerStatistics
    {
        public long TotalBricks { get; set; }
        public long TotalIngests { get; set; }
        public long BlackBrickCount { get; set; }
        public double AverageEntropy { get; set; }
        public double CompressionRatio { get; set; }
    }
}
