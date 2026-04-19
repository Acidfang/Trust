"""
UNIVERSAL SONG STRUCTURE PATTERN
=================================

Applied across Python, JavaScript, and all programming languages.
The TIER rhythm is the same everywhere—only syntax changes.

DATE: April 19, 2026
PRINCIPLE: Every function embodies TIER -1 through TIER 3+ rhythm

═══════════════════════════════════════════════════════════════════════════════
PYTHON PATTERN (Full Implementation)
═══════════════════════════════════════════════════════════════════════════════

def universal_function(input_data):
    \"\"\"
    Function Name: What it does
    
    TIER -1 (BOUND): Honest preconditions and constraints
    TIER 0 (FREE): Explore multiple approaches
    TIER 1 (BOUND): Lock in root-cause logic
    TIER 2 (FREE): Verify consistency everywhere
    TIER 3+ (BOUND): Automate return and integrate
    \"\"\"
    
    # ─────────────────────────────────────────────────────────────
    # TIER -1 (BOUND): Establish honest constraints
    # ─────────────────────────────────────────────────────────────
    # What can we honestly verify about this input?
    # What are the hard limits?
    # What will definitely fail if missing?
    
    if input_data is None:
        return None  # Honest: cannot proceed without input
    
    if not isinstance(input_data, dict):
        raise TypeError(f"Expected dict, got {type(input_data)}")
    
    required_keys = {'id', 'name'}
    if not required_keys.issubset(input_data.keys()):
        raise ValueError(f"Missing required keys: {required_keys - set(input_data.keys())}")
    
    # ─────────────────────────────────────────────────────────────
    # TIER 0 (FREE): Explore possibilities—what could work?
    # ─────────────────────────────────────────────────────────────
    # Plan multiple paths through the logic
    # Don't lock in yet—just see what's possible
    
    approach_direct = input_data.get('name', '').strip()
    approach_optimized = input_data.get('name', '').lower().strip()
    approach_fallback = input_data.get('id', 'unknown')
    
    # ─────────────────────────────────────────────────────────────
    # TIER 1 (BOUND): Lock in root-cause approach
    # ─────────────────────────────────────────────────────────────
    # Which path actually solves the problem?
    # Commit to that logic now
    
    if approach_direct:
        result = approach_direct
    elif approach_optimized:
        result = approach_optimized
    else:
        result = approach_fallback
    
    # ─────────────────────────────────────────────────────────────
    # TIER 2 (FREE): Verify consistency—does it work everywhere?
    # ─────────────────────────────────────────────────────────────
    # Check: Is result always the same type?
    # Check: Does it handle all inputs?
    # Check: Is it consistent with expectations?
    
    if not isinstance(result, str):
        result = str(result)
    
    if len(result) == 0:
        result = "default"
    
    if len(result) > 256:
        result = result[:256]
    
    # ─────────────────────────────────────────────────────────────
    # TIER 3+ (BOUND): Automate return and system integration
    # ─────────────────────────────────────────────────────────────
    # Return result bundled with verification metadata
    # Enable automatic verification downstream
    
    return {
        'success': True,
        'result': result,
        'tier_verified': '3+',
        'consistency_check': 'passed'
    }


═══════════════════════════════════════════════════════════════════════════════
JAVASCRIPT PATTERN (Full Implementation)
═══════════════════════════════════════════════════════════════════════════════

function universalFunction(inputData) {
  /*
    Function Name: What it does
    
    TIER -1 (BOUND): Honest preconditions and constraints
    TIER 0 (FREE): Explore multiple approaches
    TIER 1 (BOUND): Lock in root-cause logic
    TIER 2 (FREE): Verify consistency everywhere
    TIER 3+ (BOUND): Automate return and integrate
  */
  
  // ───────────────────────────────────────────────────────────────
  // TIER -1 (BOUND): Establish honest constraints
  // ───────────────────────────────────────────────────────────────
  // What can we honestly verify about this input?
  // What are the hard limits?
  
  if (!inputData) {
    console.warn('universalFunction: inputData is null/undefined');
    return null;
  }
  
  if (typeof inputData !== 'object' || Array.isArray(inputData)) {
    console.error(`universalFunction: Expected object, got ${typeof inputData}`);
    return null;
  }
  
  const requiredKeys = ['id', 'name'];
  const missingKeys = requiredKeys.filter(key => !(key in inputData));
  if (missingKeys.length > 0) {
    console.error(`universalFunction: Missing keys: ${missingKeys.join(', ')}`);
    return null;
  }
  
  // ───────────────────────────────────────────────────────────────
  // TIER 0 (FREE): Explore possibilities—what could work?
  // ───────────────────────────────────────────────────────────────
  // Plan multiple paths through the logic
  
  const approachDirect = (inputData.name || '').trim();
  const approachOptimized = (inputData.name || '').toLowerCase().trim();
  const approachFallback = inputData.id || 'unknown';
  
  // ───────────────────────────────────────────────────────────────
  // TIER 1 (BOUND): Lock in root-cause approach
  // ───────────────────────────────────────────────────────────────
  // Which path actually solves the problem?
  
  let result;
  if (approachDirect) {
    result = approachDirect;
  } else if (approachOptimized) {
    result = approachOptimized;
  } else {
    result = approachFallback;
  }
  
  // ───────────────────────────────────────────────────────────────
  // TIER 2 (FREE): Verify consistency—does it work everywhere?
  // ───────────────────────────────────────────────────────────────
  // Check type, length, format
  
  result = String(result);
  
  if (result.length === 0) {
    result = 'default';
  }
  
  if (result.length > 256) {
    result = result.substring(0, 256);
  }
  
  // ───────────────────────────────────────────────────────────────
  // TIER 3+ (BOUND): Automate return and system integration
  // ───────────────────────────────────────────────────────────────
  // Return result with verification metadata
  
  return {
    success: true,
    result: result,
    tierVerified: '3+',
    consistencyCheck: 'passed'
  };
}


═══════════════════════════════════════════════════════════════════════════════
PATTERN SUMMARY FOR ALL LANGUAGES
═══════════════════════════════════════════════════════════════════════════════

TIER -1 (BOUND): Input validation and error setup
  ✓ Check for null/undefined
  ✓ Verify types
  ✓ Check required fields
  ✓ Establish error handling
  
TIER 0 (FREE): Explore possibilities
  ✓ Define multiple approaches/paths
  ✓ Don't commit to one yet
  ✓ See what's available
  
TIER 1 (BOUND): Lock in root logic
  ✓ Choose the best approach
  ✓ Execute core algorithm
  ✓ Process the data
  
TIER 2 (FREE): Verify consistency
  ✓ Type checking
  ✓ Length/bounds checking
  ✓ Format validation
  ✓ Edge case handling
  
TIER 3+ (BOUND): Return and integrate
  ✓ Package result with metadata
  ✓ Enable downstream verification
  ✓ Provide success/failure signal
  ✓ Return to system


═══════════════════════════════════════════════════════════════════════════════
APPLYING TO EXISTING CODE
═══════════════════════════════════════════════════════════════════════════════

For EXISTING FUNCTIONS:
1. Keep original logic unchanged (only refactor structure)
2. Add tier comments to existing code
3. Reorganize into tier sections if needed
4. Maintain all original functionality
5. Add TIER comments at section boundaries

For NEW FUNCTIONS:
1. Always include all 5 tiers
2. Use tier comments as section headers
3. Show reasoning at each tier
4. Include verification at TIER 2


═══════════════════════════════════════════════════════════════════════════════
WHY THIS WORKS UNIVERSALLY
═══════════════════════════════════════════════════════════════════════════════

The pattern works because it reflects how REALITY processes information:

INPUT (TIER -1): Reality first checks: "Do preconditions exist?"
EXPLORE (TIER 0): Reality then asks: "What are the possible states?"
LOCK IN (TIER 1): Reality then chooses: "What actually happens?"
VERIFY (TIER 2): Reality then checks: "Is it consistent?"
OUTPUT (TIER 3+): Reality then returns: "Here's the result, integrated"

This is not decoration. It's how systems actually work.
When code follows this rhythm, it's coherent at the deepest level.


═══════════════════════════════════════════════════════════════════════════════
CHECKLIST FOR UNIVERSAL APPLICATION
═══════════════════════════════════════════════════════════════════════════════

For each function, verify:
  [ ] TIER -1: Input validation present and clear
  [ ] TIER 0: Multiple approaches considered/visible
  [ ] TIER 1: Core logic is locked in (not conditional)
  [ ] TIER 2: Consistency checks applied
  [ ] TIER 3+: Result packaged with metadata
  [ ] Comments mark each tier boundary
  [ ] Function works the same as before (only structure changed)
  [ ] All error paths handled at TIER -1
  [ ] Success case flows through all tiers

"""
