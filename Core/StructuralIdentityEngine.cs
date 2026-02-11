using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using Trust.Core.Transforms;

namespace Trust.Core
{
    /// <summary>
    /// History-independent canonical identity engine implementing LCT specification
    /// </summary>
    public class StructuralIdentityEngine
    {
        private const double EntropyThreshold = 7.8;
        private readonly List<ICanonicalTransform> _lctSet;

        public StructuralIdentityEngine()
        {
            _lctSet = InitializeLctSet();
        }

        /// <summary>
        /// Initialize bounded LCT grammar set
        /// </summary>
        private List<ICanonicalTransform> InitializeLctSet()
        {
            var transforms = new List<ICanonicalTransform>();

            for (int i = 0; i <= 7; i++)
            {
                transforms.Add(new BitRotationTransform(i));
            }

            transforms.Add(new EndiannessSwapTransform(2));
            transforms.Add(new EndiannessSwapTransform(4));
            transforms.Add(new EndiannessSwapTransform(8));
            transforms.Add(new Base64Transform());
            transforms.Add(new PaddingRemovalTransform());

            return transforms;
        }

        /// <summary>
        /// Compute Structural ID: ID(B) = HASH(C(B))
        /// </summary>
        public StructuralIdentityResult ComputeStructuralId(byte[] bitstream)
        {
            if (bitstream == null || bitstream.Length == 0)
                throw new ArgumentException("Bitstream cannot be null or empty");

            var result = new StructuralIdentityResult
            {
                OriginalLength = bitstream.Length,
                Entropy = CalculateShannonEntropy(bitstream)
            };

            if (result.Entropy > EntropyThreshold)
            {
                result.IsBlackBrick = true;
                result.StructuralId = $"BLACK_BRICK:{BitConverter.ToString(SHA256.HashData(bitstream)).Replace("-", "")}";
                result.CanonicalForm = bitstream;
                result.TransformApplied = "NONE";
                return result;
            }

            var (canonical, transformId) = Canonicalize(bitstream);
            result.CanonicalForm = canonical;
            result.TransformApplied = transformId;
            result.StructuralId = BitConverter.ToString(SHA256.HashData(canonical)).Replace("-", "");

            return result;
        }

        /// <summary>
        /// Deterministic canonicalization: C(B) = MIN_? { T_i(B) | T_i ? T and reversible }
        /// </summary>
        private (byte[] canonical, string transformId) Canonicalize(byte[] bitstream)
        {
            var candidates = new List<(byte[] data, string transformId)>
            {
                (bitstream, "IDENTITY")
            };

            foreach (var transform in _lctSet)
            {
                if (transform.IsReversible(bitstream))
                {
                    try
                    {
                        byte[] candidate = transform.Apply(bitstream);
                        if (candidate != null && candidate.Length > 0)
                        {
                            candidates.Add((candidate, transform.TransformId));
                        }
                    }
                    catch
                    {
                        // Transform failed, skip
                    }
                }
            }

            var minimal = candidates.OrderBy(c => c.data, new LexicographicByteArrayComparer()).First();
            return minimal;
        }

        /// <summary>
        /// Calculate Shannon entropy in bits per byte
        /// </summary>
        private double CalculateShannonEntropy(byte[] data)
        {
            if (data == null || data.Length == 0)
                return 0;

            var frequency = new int[256];
            foreach (byte b in data)
                frequency[b]++;

            double entropy = 0;
            foreach (int count in frequency)
            {
                if (count == 0) continue;
                double probability = (double)count / data.Length;
                entropy -= probability * Math.Log2(probability);
            }

            return entropy;
        }
    }

    /// <summary>
    /// Lexicographic comparator for deterministic ordering
    /// </summary>
    public class LexicographicByteArrayComparer : IComparer<byte[]>
    {
        public int Compare(byte[]? x, byte[]? y)
        {
            if (x == null && y == null) return 0;
            if (x == null) return -1;
            if (y == null) return 1;

            int minLength = Math.Min(x.Length, y.Length);
            for (int i = 0; i < minLength; i++)
            {
                int comparison = x[i].CompareTo(y[i]);
                if (comparison != 0)
                    return comparison;
            }

            return x.Length.CompareTo(y.Length);
        }
    }

    /// <summary>
    /// Result of structural identity computation
    /// </summary>
    public class StructuralIdentityResult
    {
        public string StructuralId { get; set; } = string.Empty;
        public byte[] CanonicalForm { get; set; } = Array.Empty<byte>();
        public string TransformApplied { get; set; } = string.Empty;
        public bool IsBlackBrick { get; set; }
        public double Entropy { get; set; }
        public int OriginalLength { get; set; }
    }
}
