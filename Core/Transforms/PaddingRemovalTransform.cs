using System;
using System.Linq;

namespace Trust.Core.Transforms
{
    /// <summary>
    /// Removes trailing null padding
    /// </summary>
    public class PaddingRemovalTransform : ICanonicalTransform
    {
        public string TransformId => "PADDING_REMOVE";

        public byte[] Apply(byte[] bitstream)
        {
            if (bitstream == null || bitstream.Length == 0)
                return bitstream;

            int lastNonZero = bitstream.Length - 1;
            while (lastNonZero >= 0 && bitstream[lastNonZero] == 0)
                lastNonZero--;

            if (lastNonZero < 0)
                return Array.Empty<byte>();

            if (lastNonZero == bitstream.Length - 1)
                return bitstream;

            byte[] result = new byte[lastNonZero + 1];
            Array.Copy(bitstream, result, lastNonZero + 1);
            return result;
        }

        public bool IsReversible(byte[] bitstream)
        {
            if (bitstream == null || bitstream.Length == 0)
                return false;

            return bitstream[bitstream.Length - 1] == 0;
        }

        public byte[] Reverse(byte[] transformed)
        {
            return transformed;
        }
    }
}
