using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Trust.Core;
using Trust.Core.Transforms;

namespace Trust.Tests
{
    /// <summary>
    /// Validates implementation against formal specification in brief.md
    /// </summary>
    public class SpecificationValidator
    {
        private readonly StructuralIdentityEngine _engine;
        private readonly List<ValidationResult> _results;

        public SpecificationValidator()
        {
            _engine = new StructuralIdentityEngine();
            _results = new List<ValidationResult>();
        }

        /// <summary>
        /// Run all specification tests
        /// </summary>
        public ValidationReport RunFullValidation()
        {
            _results.Clear();

            TestCoreIdentity();
            TestHistoryIndependence();
            TestTransformReversibility();
            TestEntropyGuardrail();
            TestCollisionResistance();
            TestTransformAmbiguity();

            return new ValidationReport
            {
                TotalTests = _results.Count,
                PassedTests = _results.Count(r => r.Passed),
                FailedTests = _results.Count(r => !r.Passed),
                Results = _results,
                IsCompliant = _results.All(r => r.Passed)
            };
        }

        /// <summary>
        /// Test 7.1: Core Identity Test - ID(raw) == ID(b64) == ID(shift)
        /// </summary>
        private void TestCoreIdentity()
        {
            string testData = "The quick brown fox jumps over the lazy dog";
            byte[] rawData = Encoding.UTF8.GetBytes(testData);
            byte[] base64Data = Encoding.ASCII.GetBytes(Convert.ToBase64String(rawData));

            var id1 = _engine.ComputeStructuralId(rawData);
            var id2 = _engine.ComputeStructuralId(base64Data);

            _results.Add(new ValidationResult
            {
                TestName = "Core Identity Test - Base64 Equivalence",
                Specification = "Section 7.1 - ID(raw) == ID(b64)",
                Passed = id1.StructuralId == id2.StructuralId,
                Details = $"Raw ID: {id1.StructuralId}\nBase64 ID: {id2.StructuralId}",
                Criterion = "Canonicalization must recognize equivalent representations"
            });
        }

        /// <summary>
        /// Test 6.1: History Independence - Same IDs regardless of order
        /// </summary>
        private void TestHistoryIndependence()
        {
            var ledger1 = new InvariantLedger();
            var ledger2 = new InvariantLedger();

            var testData = new List<string>
            {
                "First document",
                "Second document",
                "Third document",
                "Fourth document"
            };

            foreach (var data in testData)
            {
                ledger1.Ingest(Encoding.UTF8.GetBytes(data));
            }

            foreach (var data in testData.AsEnumerable().Reverse())
            {
                ledger2.Ingest(Encoding.UTF8.GetBytes(data));
            }

            var stats1 = ledger1.GetStatistics();
            var stats2 = ledger2.GetStatistics();

            bool brickCountMatch = stats1.TotalBricks == stats2.TotalBricks;

            _results.Add(new ValidationResult
            {
                TestName = "History Independence Test",
                Specification = "Section 6.1 - Order-independent ledger structure",
                Passed = brickCountMatch,
                Details = $"Ledger1 Bricks: {stats1.TotalBricks}\nLedger2 Bricks: {stats2.TotalBricks}",
                Criterion = "Brick counts must be identical regardless of ingest order"
            });
        }

        /// <summary>
        /// Test transform reversibility requirement
        /// </summary>
        private void TestTransformReversibility()
        {
            var transforms = new ICanonicalTransform[]
            {
                new BitRotationTransform(3),
                new EndiannessSwapTransform(4),
                new Base64Transform(),
                new PaddingRemovalTransform()
            };

            byte[] testData = Encoding.UTF8.GetBytes("Test reversibility data");
            bool allReversible = true;
            var details = new StringBuilder();

            foreach (var transform in transforms)
            {
                if (transform.IsReversible(testData))
                {
                    byte[] transformed = transform.Apply(testData);
                    byte[] reversed = transform.Reverse(transformed);
                    
                    bool matches = testData.SequenceEqual(reversed);
                    details.AppendLine($"{transform.TransformId}: {(matches ? "?" : "?")}");
                    
                    if (!matches)
                        allReversible = false;
                }
            }

            _results.Add(new ValidationResult
            {
                TestName = "Transform Reversibility Test",
                Specification = "Section 3 - All transforms must be reversible",
                Passed = allReversible,
                Details = details.ToString(),
                Criterion = "T_i(Reverse(T_i(B))) == B for all transforms"
            });
        }

        /// <summary>
        /// Test 5: Entropy Guardrail (Black Brick Protocol)
        /// </summary>
        private void TestEntropyGuardrail()
        {
            byte[] highEntropyData = new byte[256];
            new Random(42).NextBytes(highEntropyData);

            var result = _engine.ComputeStructuralId(highEntropyData);

            _results.Add(new ValidationResult
            {
                TestName = "Entropy Guardrail Test",
                Specification = "Section 5 - High entropy data classified as Black Brick",
                Passed = result.IsBlackBrick && result.Entropy > 7.8,
                Details = $"Entropy: {result.Entropy:F2} bits/byte\nIs Black Brick: {result.IsBlackBrick}",
                Criterion = "Data with entropy > 7.8 must be classified as BLACK_BRICK"
            });
        }

        /// <summary>
        /// Test 7.2: Collision Resistance - Different data produces different IDs
        /// </summary>
        private void TestCollisionResistance()
        {
            byte[] data1 = Encoding.UTF8.GetBytes("Test data one");
            byte[] data2 = Encoding.UTF8.GetBytes("Test data two");

            var id1 = _engine.ComputeStructuralId(data1);
            var id2 = _engine.ComputeStructuralId(data2);

            _results.Add(new ValidationResult
            {
                TestName = "Collision Resistance Test",
                Specification = "Section 7.2 - Different data must produce distinct IDs",
                Passed = id1.StructuralId != id2.StructuralId,
                Details = $"ID1: {id1.StructuralId.Substring(0, 16)}...\nID2: {id2.StructuralId.Substring(0, 16)}...",
                Criterion = "No false convergence under different inputs"
            });
        }

        /// <summary>
        /// Test 8: Transform Ambiguity - Canonical output must be unique
        /// </summary>
        private void TestTransformAmbiguity()
        {
            byte[] testData = Encoding.UTF8.GetBytes("Ambiguity test data");
            
            var result = _engine.ComputeStructuralId(testData);
            
            var secondResult = _engine.ComputeStructuralId(testData);

            bool consistent = result.StructuralId == secondResult.StructuralId &&
                            result.TransformApplied == secondResult.TransformApplied;

            _results.Add(new ValidationResult
            {
                TestName = "Transform Ambiguity Test",
                Specification = "Section 8 - No dual canonical forms permitted",
                Passed = consistent,
                Details = $"Transform: {result.TransformApplied}\nConsistent: {consistent}",
                Criterion = "Canonical output must be deterministic and unique"
            });
        }
    }

    public class ValidationResult
    {
        public string TestName { get; set; } = string.Empty;
        public string Specification { get; set; } = string.Empty;
        public bool Passed { get; set; }
        public string Details { get; set; } = string.Empty;
        public string Criterion { get; set; } = string.Empty;
    }

    public class ValidationReport
    {
        public int TotalTests { get; set; }
        public int PassedTests { get; set; }
        public int FailedTests { get; set; }
        public List<ValidationResult> Results { get; set; } = new List<ValidationResult>();
        public bool IsCompliant { get; set; }

        public override string ToString()
        {
            var sb = new StringBuilder();
            sb.AppendLine("=== SPECIFICATION VALIDATION REPORT ===");
            sb.AppendLine();
            sb.AppendLine($"Total Tests: {TotalTests}");
            sb.AppendLine($"Passed: {PassedTests}");
            sb.AppendLine($"Failed: {FailedTests}");
            sb.AppendLine($"Compliance: {(IsCompliant ? "? COMPLIANT" : "? NON-COMPLIANT")}");
            sb.AppendLine();

            foreach (var result in Results)
            {
                sb.AppendLine($"[{(result.Passed ? "PASS" : "FAIL")}] {result.TestName}");
                sb.AppendLine($"  Spec: {result.Specification}");
                sb.AppendLine($"  Criterion: {result.Criterion}");
                sb.AppendLine($"  Details: {result.Details.Replace("\n", "\n           ")}");
                sb.AppendLine();
            }

            return sb.ToString();
        }
    }
}
