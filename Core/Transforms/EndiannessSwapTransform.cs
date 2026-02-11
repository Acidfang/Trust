using System;

namespace Trust.Core.Transforms
{
    /// <summary>
    /// Endianness swap transform (16-bit, 32-bit, 64-bit)
    /// </summary>
    public class EndiannessSwapTransform : ICanonicalTransform
    {
        private readonly int _wordSize;

        public EndiannessSwapTransform(int wordSize)
        {
            if (wordSize != 2 && wordSize != 4 && wordSize != 8)
                throw new ArgumentException("Word size must be 2, 4, or 8 bytes");
            _wordSize = wordSize;
        }

        public string TransformId => $"ENDIAN_{_wordSize * 8}";

        public byte[] Apply(byte[] bitstream)
        {
            if (bitstream == null || bitstream.Length < _wordSize)
                return bitstream;

            byte[] result = new byte[bitstream.Length];
            int fullWords = bitstream.Length / _wordSize;

            for (int i = 0; i < fullWords; i++)
            {
                int offset = i * _wordSize;
                for (int j = 0; j < _wordSize; j++)
                {
                    result[offset + j] = bitstream[offset + (_wordSize - 1 - j)];
                }
            }

            int remainder = bitstream.Length % _wordSize;
            if (remainder > 0)
            {
                Array.Copy(bitstream, fullWords * _wordSize, result, fullWords * _wordSize, remainder);
            }

            return result;
        }

        public bool IsReversible(byte[] bitstream)
        {
            return bitstream != null && bitstream.Length >= _wordSize;
        }

        public byte[] Reverse(byte[] transformed)
        {
            return Apply(transformed);
        }
    }
}
