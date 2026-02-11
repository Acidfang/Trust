using System;
using System.Text;
using System.Windows;
using Trust.Core;

namespace Trust.Services
{
    /// <summary>
    /// Execution engine that processes intercepted events through the ledger
    /// </summary>
    public class ExecutionEngine
    {
        private readonly InvariantLedger _ledger;
        private readonly StructuralIdentityEngine _identityEngine;

        public ExecutionEngine()
        {
            _ledger = new InvariantLedger();
            _identityEngine = new StructuralIdentityEngine();
        }

        public ExecutionResult ProcessInterceptedData(byte[] data, string context)
        {
            try
            {
                var identityResult = _identityEngine.ComputeStructuralId(data);
                var ingestResult = _ledger.Ingest(data, context);
                var statistics = _ledger.GetStatistics();

                return new ExecutionResult
                {
                    Success = true,
                    StructuralId = identityResult.StructuralId,
                    IsNewBrick = ingestResult.IsNewBrick,
                    IsBlackBrick = identityResult.IsBlackBrick,
                    TransformApplied = identityResult.TransformApplied,
                    Entropy = identityResult.Entropy,
                    TotalBricks = statistics.TotalBricks,
                    CompressionRatio = statistics.CompressionRatio,
                    Message = BuildResultMessage(identityResult, ingestResult, statistics)
                };
            }
            catch (Exception ex)
            {
                return new ExecutionResult
                {
                    Success = false,
                    Message = $"Execution failed: {ex.Message}"
                };
            }
        }

        public ExecutionResult ProcessTextInput(string text, string context)
        {
            byte[] data = Encoding.UTF8.GetBytes(text);
            return ProcessInterceptedData(data, context);
        }

        public ExecutionResult SimulateExecution(byte[] data, string simulationContext)
        {
            var identityResult = _identityEngine.ComputeStructuralId(data);
            
            return new ExecutionResult
            {
                Success = true,
                StructuralId = identityResult.StructuralId,
                IsBlackBrick = identityResult.IsBlackBrick,
                TransformApplied = identityResult.TransformApplied,
                Entropy = identityResult.Entropy,
                Message = $"[SIMULATION] {simulationContext}\nStructural ID: {identityResult.StructuralId}\nTransform: {identityResult.TransformApplied}\nEntropy: {identityResult.Entropy:F2} bits/byte"
            };
        }

        private string BuildResultMessage(StructuralIdentityResult identity, LedgerIngestResult ingest, LedgerStatistics stats)
        {
            var sb = new StringBuilder();
            sb.AppendLine($"Structural ID: {identity.StructuralId}");
            sb.AppendLine($"Status: {(ingest.IsNewBrick ? "NEW BRICK" : "EXISTING BRICK")}");
            
            if (identity.IsBlackBrick)
                sb.AppendLine($"Type: BLACK BRICK (High Entropy: {identity.Entropy:F2})");
            else
                sb.AppendLine($"Transform: {identity.TransformApplied}");
            
            sb.AppendLine($"Entropy: {identity.Entropy:F2} bits/byte");
            sb.AppendLine($"Total Bricks: {stats.TotalBricks}");
            sb.AppendLine($"Total Ingests: {stats.TotalIngests}");
            sb.AppendLine($"Compression Ratio: {(1 - stats.CompressionRatio) * 100:F2}%");
            
            return sb.ToString();
        }

        public LedgerStatistics GetLedgerStatistics()
        {
            return _ledger.GetStatistics();
        }

        public BrickEntry? RetrieveBrick(string structuralId)
        {
            return _ledger.RetrieveBrick(structuralId);
        }
    }

    public class ExecutionResult
    {
        public bool Success { get; set; }
        public string StructuralId { get; set; } = string.Empty;
        public bool IsNewBrick { get; set; }
        public bool IsBlackBrick { get; set; }
        public string TransformApplied { get; set; } = string.Empty;
        public double Entropy { get; set; }
        public long TotalBricks { get; set; }
        public double CompressionRatio { get; set; }
        public string Message { get; set; } = string.Empty;
    }
}
