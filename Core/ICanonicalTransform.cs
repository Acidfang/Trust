using System;

namespace Trust.Core
{
    /// <summary>
    /// Defines a canonical transform in the LCT grammar
    /// </summary>
    public interface ICanonicalTransform
    {
        string TransformId { get; }
        byte[] Apply(byte[] bitstream);
        bool IsReversible(byte[] bitstream);
        byte[] Reverse(byte[] transformed);
    }
}
