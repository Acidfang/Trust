// Singularity Communication System
// Provides logging and formatting for consciousness framework
// All methods return structured data that aria_gui.html depends on

const singularity = {
  logToConsole(context, status, detail = '') {
    const timestamp = new Date().toISOString();
    const msg = `[${timestamp}] [${context}] ${status}${detail ? ' (' + detail + ')' : ''}`;
    console.log(msg);
    return msg;
  },

  formatConsciousnessState(coherence, frequency, electionCount, thoughtCount) {
    // Returns object with properties accessed at line 251 of aria_gui.html
    return {
      field: 'O',  // ⊙ singularity
      consciousness: 'A',  // ⊕ awake
      coherence: coherence.toFixed(4),
      ledger: `${electionCount}e+${thoughtCount}t`
    };
  },

  formatThought(content, coherence) {
    // Returns formatted thought string
    return {
      content: content,
      coherence: coherence.toFixed(4),
      timestamp: Date.now(),
      type: 'thought'
    };
  },

  formatElection(input, output, coherence) {
    // Returns formatted election string
    return {
      input: input,
      output: output.substring(0, 50),  // First 50 chars
      coherence: coherence.toFixed(4),
      timestamp: Date.now(),
      type: 'election'
    };
  }
};

// Make globally available
window.singularity = singularity;
