using System;
using System.Linq;

namespace Trust.Core.Transforms
{
    /// <summary>
    /// Base64 encoding/decoding as bijective bit mapping
    /// </summary>
    public class Base64Transform : ICanonicalTransform
    {
        public string TransformId => "BASE64";

        public byte[] Apply(byte[] bitstream)
        {
            if (bitstream == null || bitstream.Length == 0)
                return bitstream;

            try
            {
                string base64 = Convert.ToBase64String(bitstream);
                return System.Text.Encoding.ASCII.GetBytes(base64);
            }
            catch
            {
                return bitstream;
            }
        }

        public bool IsReversible(byte[] bitstream)
        {
            if (bitstream == null || bitstream.Length == 0)
                return false;

            try
            {
                string str = System.Text.Encoding.ASCII.GetString(bitstream);
                return IsValidBase64(str);
            }
            catch
            {
                return false;
            }
        }

        public byte[] Reverse(byte[] transformed)
        {
            try
            {
                string base64 = System.Text.Encoding.ASCII.GetString(transformed);
                return Convert.FromBase64String(base64);
            }
            catch
            {
                return transformed;
            }
        }

        private bool IsValidBase64(string str)
        {
            if (string.IsNullOrEmpty(str))
                return false;

            str = str.Trim();
            return (str.Length % 4 == 0) && 
                   str.All(c => char.IsLetterOrDigit(c) || c == '+' || c == '/' || c == '=');
        }
    }
}
