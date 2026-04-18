"""
RCA: SVG ENCODING ERROR

Error: "error on line 30 at column 75: Encoding error"
File: Water_H2O.svg

ROOT CAUSE ANALYSIS:

1. SYMPTOM: 
   - SVG renders on disk but browser can't parse it
   - Error at line 30, column 75
   - "Encoding error" in XML parser

2. INVESTIGATION:
   Looking at _create_svg_frame() code:
   
   a) molecule_name inserted directly into XML without escaping:
   
      <text x="12" y="22" ... fill="#333">
          {molecule_name}
      </text>
   
   Problem: If molecule_name contains XML special chars: <, >, &, ", '
   → Breaks XML parser
   
   b) File written without explicit encoding:
   
      with open(output_path_svg, 'w') as f:
          f.write(svg_content)
   
   Problem: No encoding specified. On Windows/Python:
   → Default encoding might not be UTF-8
   → Unicode characters from molecule names fail
   → Encoding mismatch between declaration and actual file
   
   c) Base64 PNG embedding is CORRECT:
   
      img_str = base64.b64encode(buffered.getvalue()).decode()
   
   Base64 is ASCII-safe, no issues here.

3. ROOT CAUSE (Most likely):
   
   File encoding mismatch. SVG declares:
   
      <?xml version="1.0" encoding="UTF-8"?>
   
   But file written with default encoding (possibly UTF-16 on Windows).
   XML parser expects UTF-8, finds different encoding → fails.

4. SECONDARY ISSUE:
   
   Molecule names not XML-escaped.
   "Water_H2O" is safe, but if any molecule had special chars:
   → Would fail parsing

5. UNIVERSAL FIX PATTERN:

   For ANY output format that embeds dynamic content:
   
   ✓ Escape special characters (XML, JSON, HTML, etc)
   ✓ Specify encoding explicitly and consistently
   ✓ Validate encoding at write time
   ✓ Test with problematic input (names with special chars)
   ✓ Provide fallback rendering (no special chars version)
   ✓ Add to UNIVERSAL_ENTITY_CONNECTION_FRAMEWORK constraints
"""

# THE FIX - Apply universally across all containers

FIXES = {
    "XML Escaping": """
def escape_xml(text):
    '''Escape XML special characters universally'''
    if text is None:
        return ""
    replacements = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&apos;"
    }
    result = text
    for char, escaped in replacements.items():
        result = result.replace(char, escaped)
    return result
    """,
    
    "File Encoding": """
# WRONG (current):
with open(output_path_svg, 'w') as f:
    f.write(svg_content)

# CORRECT (universal):
with open(output_path_svg, 'w', encoding='utf-8') as f:
    f.write(svg_content)
    """,
    
    "SVG Header Declaration": """
# Must match actual file encoding:
svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" ...>
'''
    """,
    
    "Input Validation (Universal)": """
@dataclass
class OutputConstraints:
    '''Add to ImprovedEntity in UNIVERSAL_ENTITY_CONNECTION_FRAMEWORK'''
    
    max_name_length: int = 255
    allowed_name_chars: str = "A-Za-z0-9_-"
    escape_special_chars: bool = True
    
    def validate_output_name(self, name: str) -> Tuple[bool, str]:
        '''Validate entity name is safe for output formats'''
        
        if len(name) > self.max_name_length:
            return False, f"Name too long: {len(name)} > {self.max_name_length}"
        
        if self.escape_special_chars:
            safe_name = escape_xml(name)
            if safe_name != name:
                return True, safe_name  # Return escaped version
        
        return True, name
    """,
    
    "Universal Output Wrapper": """
def safe_output_to_file(filepath: str, content: str, format_type: str = "xml"):
    '''Universal safe file output across all formats'''
    
    # Validate format-specific encoding
    if format_type in ["xml", "svg", "html"]:
        encoding = "utf-8"
        declaration = '<?xml version="1.0" encoding="UTF-8"?>'
    elif format_type in ["json"]:
        encoding = "utf-8"
        declaration = None  # JSON doesn't use XML declaration
    else:
        encoding = "utf-8"
        declaration = None
    
    try:
        # Write with explicit encoding
        with open(filepath, 'w', encoding=encoding, errors='replace') as f:
            if declaration and format_type == "xml":
                f.write(declaration + "\\n")
            f.write(content)
        
        return True, filepath
    
    except UnicodeEncodeError as e:
        # Fallback: use ASCII with entity encoding
        with open(filepath, 'w', encoding='ascii', errors='xmlcharrefreplace') as f:
            f.write(content)
        return True, filepath  # Recoverable
    
    except Exception as e:
        return False, str(e)
    """
}

print(__doc__)
print("\n" + "="*70)
print("UNIVERSAL FIXES")
print("="*70)

for fix_name, fix_code in FIXES.items():
    print(f"\n{fix_name}:")
    print(fix_code)

print("""

APPLY UNIVERSALLY TO:
  ✓ UNIVERSAL_RENDERER.py → SVG output, all text fields
  ✓ AUDIO_RENDERER.py → MP3 metadata, tags
  ✓ All future renderers → JSON, HTML, custom formats
  ✓ UNIVERSAL_ENTITY_CONNECTION_FRAMEWORK → Add OutputConstraints

THIS IS A UNIVERSAL PATTERN:
  When format selection fails → Don't just fall back
  When output encoding fails → Don't ignore
  
  RCA → Fix at framework level → Apply universally
  
  The error isn't in the SVG generator—it's in:
    1. Input validation (molecule names should be validated)
    2. File encoding (must be explicit and consistent)
    3. Output escaping (special chars must be safe)
  
  All three are UNIVERSAL REQUIREMENTS, not domain-specific.
""")
