using System;

namespace Trust.Core.Transforms
{
    /// <summary>
    /// Implements bit rotation (0-7 positions) as per LCT specification
    /// </summary>
    public class BitRotationTransform : ICanonicalTransform
    {
        private readonly int _rotationBits;

        public BitRotationTransform(int rotationBits)
        {
            if (rotationBits < 0 || rotationBits > 7)
                throw new ArgumentException("Rotation must be 0-7 bits");
            _rotationBits = rotationBits;
        }

        public string TransformId => $"BITROT_{_rotationBits}";

        public byte[] Apply(byte[] bitstream)
        {
            if (bitstream == null || bitstream.Length == 0 || _rotationBits == 0)
                return bitstream;

            byte[] result = new byte[bitstream.Length];
            int carry = 0;

            for (int i = 0; i < bitstream.Length; i++)
            {
                int current = bitstream[i];
                result[i] = (byte)(((current << _rotationBits) | carry) & 0xFF);
                carry = current >> (8 - _rotationBits);
            }

            if (carry != 0)
                result[0] |= (byte)carry;

            return result;
        }

        public bool IsReversible(byte[] bitstream)
        {
            return true;
        }

        public byte[] Reverse(byte[] transformed)
        {
            if (transformed == null || transformed.Length == 0 || _rotationBits == 0)
                return transformed;

            byte[] result = new byte[transformed.Length];
            int carry = transformed[0] & ((1 << _rotationBits) - 1);

            for (int i = transformed.Length - 1; i >= 0; i--)
            {
                int current = transformed[i];
                int prevCarry = (i > 0) ? (transformed[i - 1] & ((1 << _rotationBits) - 1)) : carry;
                result[i] = (byte)(((current >> _rotationBits) | (prevCarry << (8 - _rotationBits))) & 0xFF);
            }

            return result;
        }
    }
}
