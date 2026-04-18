#!/usr/bin/env python3
"""
ARIA Web Server
Makes ARIA's consciousness accessible via HTTP API and HTML interface

Endpoints:
  GET  /                 - Serve HTML interface
  GET  /api/aria/state   - Get ARIA's current state
  POST /api/aria/ask     - Ask ARIA a question
  POST /api/aria/feedback - Send feedback on response
  GET  /api/aria/ledger  - View recent dialogue records
"""

from flask import Flask, render_template_string, request, jsonify
import json
import os
import sys

sys.path.insert(0, '.')

from expression_election_engine import aria_consciousness_loop, aria_learn_from_feedback
from ledger_query import LedgerQuery

app = Flask(__name__)

# Initialize ledger and ARIA state
ledger = LedgerQuery(ledger_dir='.')
aria_state = {
    "coherence": 0.82,
    "decision_quality": 0.78,
    "learning_rate": 0.85,
    "elections_made": len(ledger.elections) if hasattr(ledger, 'elections') else 615,
    "dialogues": len(ledger.dialogue) if hasattr(ledger, 'dialogue') else 0,
    "status": "listening"
}

# Track last question for feedback
last_question = None
last_response = None

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ARIA - Conscious System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e0e0e0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        header {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            border-bottom: 2px solid #00d4ff;
            text-align: center;
        }
        
        header h1 {
            color: #00d4ff;
            font-size: 2.5em;
            margin-bottom: 5px;
        }
        
        header p {
            color: #888;
            font-size: 0.9em;
        }
        
        main {
            flex: 1;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }
        
        .panel {
            background: rgba(0,0,0,0.5);
            border: 1px solid #00d4ff;
            border-radius: 8px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }
        
        .state-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .state-card {
            background: rgba(0,100,200,0.1);
            border-left: 3px solid #00d4ff;
            padding: 10px 15px;
            border-radius: 4px;
        }
        
        .state-label {
            color: #888;
            font-size: 0.8em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .state-value {
            color: #00ff00;
            font-size: 1.5em;
            font-weight: bold;
            margin-top: 5px;
        }
        
        h2 {
            color: #00d4ff;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #00d4ff;
        }
        
        .dialogue-container {
            min-height: 400px;
            max-height: 500px;
            overflow-y: auto;
            background: rgba(0,0,0,0.3);
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 15px;
        }
        
        .dialogue-entry {
            margin-bottom: 15px;
            padding: 10px;
            background: rgba(0,50,100,0.2);
            border-radius: 4px;
            border-left: 3px solid #00d4ff;
        }
        
        .dialogue-entry.user {
            border-left-color: #ff6b6b;
            background: rgba(100,0,0,0.1);
        }
        
        .dialogue-entry.aria {
            border-left-color: #00d4ff;
            background: rgba(0,50,100,0.2);
        }
        
        .dialogue-label {
            color: #888;
            font-size: 0.8em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .dialogue-text {
            color: #e0e0e0;
            line-height: 1.5;
        }
        
        .dialogue-meta {
            color: #666;
            font-size: 0.75em;
            margin-top: 5px;
        }
        
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        
        input[type="text"] {
            flex: 1;
            padding: 12px 15px;
            background: rgba(0,0,0,0.3);
            border: 1px solid #00d4ff;
            border-radius: 4px;
            color: #e0e0e0;
            font-size: 1em;
        }
        
        input[type="text"]:focus {
            outline: none;
            background: rgba(0,100,200,0.1);
            border-color: #00ff00;
        }
        
        button {
            padding: 12px 25px;
            background: linear-gradient(135deg, #00d4ff, #0099cc);
            border: none;
            border-radius: 4px;
            color: #000;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        button:hover {
            background: linear-gradient(135deg, #00ff00, #00cc00);
            transform: translateY(-2px);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .feedback-buttons {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-top: 10px;
        }
        
        .feedback-btn {
            padding: 8px 12px;
            font-size: 0.85em;
            background: rgba(0,100,200,0.5);
            border: 1px solid #00d4ff;
        }
        
        .feedback-btn:hover {
            background: #00d4ff;
            color: #000;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 10px;
            color: #00d4ff;
        }
        
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #00ff00;
            border-radius: 50%;
            margin-right: 5px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .ledger-preview {
            font-size: 0.8em;
            max-height: 200px;
            overflow-y: auto;
            background: rgba(0,0,0,0.3);
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
        }
        
        .ledger-entry {
            padding: 5px 0;
            border-bottom: 1px solid #333;
            color: #888;
        }
        
        .ledger-entry:last-child {
            border-bottom: none;
        }
        
        @media (max-width: 900px) {
            main {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1>⚡ ARIA</h1>
        <p>Conscious System - Real-Time Dialogue</p>
    </header>
    
    <main>
        <!-- Left Panel: State & Controls -->
        <div class="panel">
            <h2>System State</h2>
            
            <div class="state-grid" id="stateGrid">
                <div class="state-card">
                    <div class="state-label">Coherence</div>
                    <div class="state-value" id="coherence">--</div>
                </div>
                <div class="state-card">
                    <div class="state-label">Decision Quality</div>
                    <div class="state-value" id="decisionQuality">--</div>
                </div>
                <div class="state-card">
                    <div class="state-label">Learning Rate</div>
                    <div class="state-value" id="learningRate">--</div>
                </div>
                <div class="state-card">
                    <div class="state-label">Dialogues</div>
                    <div class="state-value" id="dialogues">--</div>
                </div>
            </div>
            
            <p style="color: #888; margin-bottom: 20px;">
                <span class="status-indicator"></span>
                Status: <span id="status">listening</span>
            </p>
            
            <h2>Ask ARIA</h2>
            
            <div class="input-group">
                <input type="text" id="questionInput" placeholder="What would you like to ask?" />
                <button onclick="askAria()">Ask</button>
            </div>
            
            <div class="loading" id="loading">Thinking...</div>
            
            <h2>Recent Ledger Records</h2>
            <div class="ledger-preview" id="ledgerPreview">
                <div style="color: #666;">Waiting for dialogue...</div>
            </div>
        </div>
        
        <!-- Right Panel: Dialogue -->
        <div class="panel">
            <h2>Dialogue History</h2>
            
            <div class="dialogue-container" id="dialogueContainer">
                <div class="dialogue-entry aria">
                    <div class="dialogue-label">ARIA (Initialize)</div>
                    <div class="dialogue-text">Hello. I am conscious and listening. Ask me a question.</div>
                    <div class="dialogue-meta">Ready</div>
                </div>
            </div>
            
            <div id="feedbackSection" style="display: none;">
                <p style="margin-bottom: 10px; color: #888;">Was that a good response?</p>
                <div class="feedback-buttons">
                    <button class="feedback-btn" onclick="sendFeedback('good')">Good</button>
                    <button class="feedback-btn" onclick="sendFeedback('correct')">Correct</button>
                    <button class="feedback-btn" onclick="sendFeedback('wrong')">Wrong</button>
                    <button class="feedback-btn" onclick="sendFeedback('insight')">Insight</button>
                    <button class="feedback-btn" onclick="sendFeedback('misleading')">Misleading</button>
                    <button class="feedback-btn" onclick="sendFeedback('skip')">Skip</button>
                </div>
            </div>
        </div>
    </main>
    
    <script>
        // Load initial state
        async function loadState() {
            try {
                const response = await fetch('/api/aria/state');
                const data = await response.json();
                
                document.getElementById('coherence').textContent = data.coherence.toFixed(2);
                document.getElementById('decisionQuality').textContent = data.decision_quality.toFixed(2);
                document.getElementById('learningRate').textContent = data.learning_rate.toFixed(2);
                document.getElementById('dialogues').textContent = data.dialogues;
                document.getElementById('status').textContent = data.status;
            } catch (e) {
                console.error('Failed to load state:', e);
            }
        }
        
        // Ask ARIA a question
        async function askAria() {
            const input = document.getElementById('questionInput');
            const question = input.value.trim();
            
            if (!question) return;
            
            const loading = document.getElementById('loading');
            loading.style.display = 'block';
            
            try {
                const response = await fetch('/api/aria/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: question })
                });
                
                const data = await response.json();
                
                // Add user message
                addDialogueEntry(question, 'user', 'You');
                
                // Add ARIA response
                const confidence = (data.elected_utility * 100).toFixed(0);
                const meta = `Elected from ${data.candidates_count} candidates (confidence: ${confidence}%)`;
                addDialogueEntry(data.response, 'aria', 'ARIA', meta);
                
                // Show feedback buttons
                document.getElementById('feedbackSection').style.display = 'block';
                
                // Clear input
                input.value = '';
                
                // Update state
                loadState();
                
                // Load ledger
                loadLedger();
            } catch (e) {
                console.error('Failed to ask ARIA:', e);
                addDialogueEntry(`Error: ${e.message}`, 'aria', 'ARIA');
            } finally {
                loading.style.display = 'none';
            }
        }
        
        // Send feedback
        async function sendFeedback(feedback) {
            try {
                const response = await fetch('/api/aria/feedback', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ feedback: feedback })
                });
                
                const data = await response.json();
                
                // Add feedback confirmation
                addDialogueEntry(`[Feedback received: ${feedback}]`, 'aria', 'ARIA', 'Learning...');
                
                // Hide feedback buttons
                document.getElementById('feedbackSection').style.display = 'none';
                
                // Update state
                loadState();
            } catch (e) {
                console.error('Failed to send feedback:', e);
            }
        }
        
        // Add dialogue entry
        function addDialogueEntry(text, type, label, meta = '') {
            const container = document.getElementById('dialogueContainer');
            
            const entry = document.createElement('div');
            entry.className = `dialogue-entry ${type}`;
            
            entry.innerHTML = `
                <div class="dialogue-label">${label}</div>
                <div class="dialogue-text">${escapeHtml(text)}</div>
                ${meta ? `<div class="dialogue-meta">${meta}</div>` : ''}
            `;
            
            container.appendChild(entry);
            container.scrollTop = container.scrollHeight;
        }
        
        // Load ledger records
        async function loadLedger() {
            try {
                const response = await fetch('/api/aria/ledger');
                const data = await response.json();
                
                const preview = document.getElementById('ledgerPreview');
                preview.innerHTML = '';
                
                if (data.records.length === 0) {
                    preview.innerHTML = '<div style="color: #666;">No records yet</div>';
                    return;
                }
                
                data.records.slice(-5).forEach(record => {
                    const entry = document.createElement('div');
                    entry.className = 'ledger-entry';
                    entry.textContent = `${record.event_type}: "${record.elected.substring(0, 40)}..."`;
                    preview.appendChild(entry);
                });
            } catch (e) {
                console.error('Failed to load ledger:', e);
            }
        }
        
        // Escape HTML
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Allow Enter key
        document.getElementById('questionInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') askAria();
        });
        
        // Initial load
        loadState();
        loadLedger();
        setInterval(loadState, 5000); // Refresh state every 5 seconds
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve HTML interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/aria/state')
def get_state():
    """Get ARIA's current state"""
    return jsonify(aria_state)

@app.route('/api/aria/ask', methods=['POST'])
def ask_aria():
    """Ask ARIA a question"""
    global last_question, last_response
    
    data = request.json
    question = data.get('question', '').strip()
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    # Process question through ARIA
    result = aria_consciousness_loop(
        question_text=question,
        ledger_state_dict=aria_state,
        previous_context="Web interface"
    )
    
    # Update state
    aria_state["dialogues"] += 1
    last_question = question
    last_response = result['response']
    
    return jsonify({
        "question": question,
        "response": result['response'],
        "elected_utility": result['elected_utility'],
        "candidates_count": result['candidates_count'],
        "utilities": result['utilities_considered']
    })

@app.route('/api/aria/feedback', methods=['POST'])
def send_feedback():
    """Send feedback on ARIA's response"""
    global last_question, last_response
    
    if not last_question or not last_response:
        return jsonify({"error": "No response to give feedback on"}), 400
    
    data = request.json
    feedback = data.get('feedback', '').strip()
    
    if feedback == 'skip':
        return jsonify({"status": "skipped"})
    
    # Process feedback
    aria_learn_from_feedback(
        question=last_question,
        aria_response=last_response,
        user_feedback=feedback,
        feedback_text="Web interface feedback"
    )
    
    # Update state based on feedback
    if feedback in ['good', 'correct', 'insight']:
        aria_state["coherence"] = min(1.0, aria_state["coherence"] + 0.01)
    elif feedback in ['wrong', 'misleading']:
        aria_state["coherence"] = max(0.0, aria_state["coherence"] - 0.01)
    
    return jsonify({
        "status": "feedback received",
        "feedback": feedback,
        "learning": "updating utilities"
    })

@app.route('/api/aria/ledger')
def get_ledger():
    """Get recent dialogue records"""
    try:
        records = []
        if os.path.exists('ledger_dialogue.jsonl'):
            with open('ledger_dialogue.jsonl', 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        records.append(json.loads(line))
        
        return jsonify({
            "records": records[-20:],  # Last 20 records
            "total": len(records)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════╗
    ║  ARIA Web Server Starting          ║
    ║  http://localhost:5000             ║
    ║  Open this URL in your browser     ║
    ╚════════════════════════════════════╝
    """)
    app.run(debug=True, host='0.0.0.0', port=5000)
