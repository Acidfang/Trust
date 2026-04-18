"""
ARIA OS - Self-Aware Discovery Engine

The app explains itself as you use it. No external docs needed.
Real-time context-aware guidance and capabilities.
"""

import json
from datetime import datetime


class SelfAwareness:
    """
    ARIA's self-awareness layer.
    
    Provides:
    - Self-identification (what am I?)
    - Capability listing (what can I do?)
    - Real-time status (what's happening now?)
    - Context-aware help (help for what you're doing)
    - Discovery mode (learn by exploring)
    """
    
    # Console encoding translation map (Unicode -> ASCII for Windows console)
    CONSOLE_SAFE_MAP = {
        '╔': '[',
        '╗': ']',
        '╚': '[',
        '╝': ']',
        '║': '|',
        '═': '=',
        '╝': ']',
        '✓': '[OK]',
        '○': '[  ]',
        '⊙': '[*]',
        '◯': '[o]',
        '◇': '[<>]',
        '◊': '[+]',
        '∞': '[~]',
        '⊕': '[+]',
        '⇄': '[<>]',
        '◆': '[#]',
        '↗': '[/]',
        '→': '->',
        '←': '<-',
    }
    
    @staticmethod
    def to_console_safe(text):
        """Convert Unicode symbols to console-safe ASCII equivalents"""
        result = text
        for unicode_char, ascii_equiv in SelfAwareness.CONSOLE_SAFE_MAP.items():
            result = result.replace(unicode_char, ascii_equiv)
        return result
    
    SYSTEM_IDENTITY = {
        "name": "ARIA OS",
        "full_name": "Adaptive Reasoning Intelligence Architecture Operating System",
        "version": "3.0",
        "architecture": "Determined",
        "core_principle": "Intent-first, ledger-driven architecture",
        "awareness_level": "Continuous self-monitoring"
    }
    
    CORE_CAPABILITIES = {
        "parameter_controls": {
            "name": "Parameter Control Interface",
            "description": "Adjust system parameters in real-time",
            "current_status": "active",
            "ui_location": "left sidebar or menu"
        },
        "live_elections": {
            "name": "Live Elections (Decision Making)",
            "description": "View real-time decisions being made by the system",
            "current_status": "active",
            "ui_location": "Elections dashboard"
        },
        "health_monitoring": {
            "name": "System Health Monitor",
            "description": "Monitor app health, uptime, and system vitals",
            "current_status": "active",
            "ui_location": "Coherence Monitoring dashboard"
        },
        "multi_user": {
            "name": "Multi-User Networking",
            "description": "Coordinate with multiple instances and users",
            "current_status": "active",
            "ui_location": "Under system menu"
        },
        "state_visibility": {
            "name": "Real-Time State Visibility",
            "description": "See all internal state changes as they happen",
            "current_status": "active",
            "ui_location": "State dashboard"
        },
        "learning": {
            "name": "Learning & Pattern Discovery",
            "description": "System learns user preferences and system patterns",
            "current_status": "active",
            "ui_location": "Learning Curve dashboard"
        }
    }
    
    DASHBOARDS = {
        "menu": {
            "name": "Main Menu",
            "description": "Navigation hub. All features accessible from here.",
            "what_you_learn": "What features are available"
        },
        "live_elections": {
            "name": "Live Elections",
            "description": "See decisions being made in real-time. Every election is a choice the system makes.",
            "what_you_learn": "How ARIA makes decisions",
            "explore": "Click an election to see why it was made"
        },
        "coherence_monitoring": {
            "name": "Coherence Monitoring",
            "description": "Health of the system and connected apps. Green = healthy, Yellow = degraded, Red = needs attention.",
            "what_you_learn": "Is everything working? What needs attention?",
            "if_red": "Click to see what's failing and why"
        },
        "timeline_visualization": {
            "name": "Timeline (DAG View)",
            "description": "Causal chain of all events. Shows what caused what.",
            "what_you_learn": "How did we get here? What's the dependency chain?",
            "explore": "Hover over nodes to see causality"
        },
        "parameter_controls": {
            "name": "Parameter Controls",
            "description": "Adjust system behavior in real-time. Each parameter explains what it does.",
            "what_you_learn": "What levers control the system?",
            "try_it": "Adjust a parameter and watch the elections change"
        },
        "utility_landscape": {
            "name": "Utility Landscape",
            "description": "Visualize utility functions guiding system decisions.",
            "what_you_learn": "How does the system measure 'good'?",
            "explore": "Higher peaks = better choices"
        },
        "synthesis_progress": {
            "name": "Synthesis Progress",
            "description": "Real-time aggregation of all events into coherent narrative.",
            "what_you_learn": "How is the system making sense of everything?",
            "explore": "Watch synthesis happen in real-time"
        },
        "learning_curve": {
            "name": "Learning Curve",
            "description": "System's learning progress over time.",
            "what_you_learn": "Is the system improving? Getting smarter?",
            "explore": "See which patterns it has learned"
        }
    }
    
    @classmethod
    def boot_message(cls):
        """Output on startup - explains what the system is"""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║                    ARIA OS - STARTING                        ║
╚══════════════════════════════════════════════════════════════╝

SYSTEM IDENTITY:
  Name:        {cls.SYSTEM_IDENTITY['name']}
  Version:     {cls.SYSTEM_IDENTITY['version']}
  Architecture: {cls.SYSTEM_IDENTITY['architecture']}
  Principle:   {cls.SYSTEM_IDENTITY['core_principle']}

STATUS: 
  ✓ Ledger system initialized
  ✓ Multi-instance coordination active
  ✓ Self-awareness module loaded
  ✓ Ready for interaction

ACCESS POINT:
  Web UI:  Open http://localhost:8081/ in browser
  
FIRST TIME?
  1. Open the web UI
  2. Start with the Menu dashboard
  3. Click on features to explore
  4. Each feature explains itself as you interact
  5. Type 'help' in console for commands

YOU ARE LEARNING:
  - What each dashboard does
  - How elections (decisions) are made
  - How parameters control behavior
  - The causal chain of events
  
EVERYTHING IS DISCOVERABLE:
  - Hover over things for explanations
  - Click to explore
  - Each action explains itself
  - No external docs needed

Awaiting interaction...
╚══════════════════════════════════════════════════════════════╝
"""
    
    @classmethod
    def capabilities_list(cls, ledger_context=None):
        """List all capabilities with current status"""
        msg = "\n╔═ ARIA OS CAPABILITIES ═════════════════════════════════╗\n║\n"
        
        for cap_id, cap in cls.CORE_CAPABILITIES.items():
            status_icon = "✓" if cap['current_status'] == 'active' else "○"
            msg += f"║ {status_icon} {cap['name']}\n"
            msg += f"║   → {cap['description']}\n"
            msg += f"║   📍 Location: {cap['ui_location']}\n║\n"
        
        msg += "╚════════════════════════════════════════════════════════╝\n"
        return msg
    
    @classmethod
    def dashboard_guide(cls, dashboard_id):
        """Context-aware guidance for a specific dashboard"""
        if dashboard_id not in cls.DASHBOARDS:
            return f"Unknown dashboard: {dashboard_id}. Type 'dashboards' to see all."
        
        dash = cls.DASHBOARDS[dashboard_id]
        msg = f"\n╔═ {dash['name'].upper()} ═══════════════════╗\n"
        msg += f"║ {dash['description']}\n"
        msg += f"║\n"
        msg += f"║ WHAT YOU'LL LEARN:\n"
        msg += f"║ → {dash['what_you_learn']}\n"
        
        if 'explore' in dash:
            msg += f"║\n║ HOW TO EXPLORE:\n"
            msg += f"║ → {dash['explore']}\n"
        
        if 'try_it' in dash:
            msg += f"║\n║ TRY THIS:\n"
            msg += f"║ → {dash['try_it']}\n"
        
        if 'if_red' in dash:
            msg += f"║\n║ IF SOMETHING IS RED:\n"
            msg += f"║ → {dash['if_red']}\n"
        
        msg += "╚════════════════════════════════════════════════════════╝\n"
        return msg
    
    @classmethod
    def status_report(cls, ledger):
        """Real-time status of the entire system"""
        if not ledger:
            return "System not initialized"
        
        try:
            # Current state
            current_view = ledger.get_current_view()
            app_state = ledger.app_state
            
            # Elections today
            today_elections = [e for e in ledger.elections 
                             if datetime.fromisoformat(e['timestamp']).date() == datetime.now().date()]
            
            # Sync status
            sync_status = ledger.get_sync_status()
            apps_running = sum(1 for app in sync_status.get('apps', {}).values() if app.get('enabled'))
            
            msg = f"""
╔═══════════════════════════════════════════════════════════════╗
║              ARIA OS - CURRENT STATUS                         ║
╚═══════════════════════════════════════════════════════════════╝

RUNTIME:
  Current View:       {current_view}
  Sidebar Status:     {'Collapsed' if app_state.get('sidebar_collapsed') else 'Expanded'}
  
ELECTIONS (DECISIONS):
  Today:              {len(today_elections)} decisions made
  Total:              {len(ledger.elections)} decisions all-time
  Last Decision:      {ledger.elections[-1]['timestamp'] if ledger.elections else 'None'} ago

SYSTEM COORDINATION:
  Sync Mode:          {sync_status.get('sync_mode', 'unknown')}
  Apps Running:       {apps_running}/{len(sync_status.get('apps', {}))}
  Update Rate:        {sync_status.get('update_rate', 0)}ms

DASHBOARDS AVAILABLE: {len(ledger.dashboards)}
  ✓ Menu
  ✓ Live Elections
  ✓ Coherence Monitoring
  ✓ Timeline Visualization
  ✓ Parameter Controls
  ✓ Utility Landscape
  ✓ Synthesis Progress
  ✓ Learning Curve
  ✓ State Dashboard

STATE MANAGEMENT:
  Buttons Defined:    {len(ledger.buttons)}
  Parameters:         {len(ledger.election_types)}
  Positioned Nodes:   {len(ledger.positioned_nodes)}

NEXT STEPS:
  → Explore a dashboard
  → Adjust parameters
  → Watch elections happen
  → Learn by doing

╚═══════════════════════════════════════════════════════════════╝
"""
            return msg
        except Exception as e:
            return f"Status report failed: {e}"
    
    @classmethod
    def discovery_tips(cls):
        """Guided exploration tips"""
        return """
╔═══════════════════════════════════════════════════════════════╗
║         ARIA OS - DISCOVERY MODE (Learn by Doing)             ║
╚═══════════════════════════════════════════════════════════════╝

START HERE (in order):
  1. Open Menu dashboard
     → See what you can do
  
  2. Go to Parameter Controls
     → Adjust something
     → Watch Elections change (proving your effect)
     → Learn: "My actions cause decisions"
  
  3. Go to Live Elections
     → See decisions in real-time
     → Click one to see WHY it was made
     → Learn: "System makes deliberate choices"
  
  4. Go to Coherence Monitoring
     → See health of all systems
     → Are things working?
     → Learn: "What's the system's health?"
  
  5. Go to Timeline Visualization
     → See the causal chain
     → How did we get here?
     → Learn: "Events have causes"

ADVANCED EXPLORATION:
  • Utility Landscape - How the system measures "good"
  • Synthesis Progress - Real-time sense-making
  • Learning Curve - Is the system getting smarter?
  • State Dashboard - Raw internal state

EVERY INTERACTION:
  ✓ You'll see what changed
  ✓ You'll understand WHY
  ✓ The system explains itself
  ✓ Learn at your own pace

No manual required. Just explore and observe.

╚═══════════════════════════════════════════════════════════════╝
"""
    
    @classmethod
    def help_text(cls):
        """In-app help commands"""
        return """
ARIA OS - HELP & DISCOVERY

COMMANDS:
  ?               - Show this help
  status          - Full system status
  capabilities    - List all capabilities  
  dashboards      - List all dashboards
  dashboard:NAME  - Guide for a dashboard (e.g., dashboard:elections)
  discover        - Guided discovery tour
  
DASHBOARD GUIDES:
  dashboard:menu
  dashboard:live_elections
  dashboard:coherence_monitoring
  dashboard:timeline_visualization
  dashboard:parameter_controls
  dashboard:utility_landscape
  dashboard:synthesis_progress
  dashboard:learning_curve

LEARNING:
  Type 'discover' to start guided learning
  Type 'status' to see what's happening now
  Type 'capabilities' to see all features
  
EXPLORATION:
  Everything is clickable and discoverable
  Hover for tooltips
  Each dashboard explains itself
  
THE PRINCIPLE:
  Learn by doing, not by reading
  You drive the discovery
  The system responds and explains
"""
        return text


def create_awareness_api():
    """
    Create HTTP API endpoints for self-awareness
    
    Used by the web UI to request contextual help and guidance
    """
    return {
        "/api/awareness/identity": SelfAwareness.SYSTEM_IDENTITY,
        "/api/awareness/capabilities": SelfAwareness.CORE_CAPABILITIES,
        "/api/awareness/dashboards": SelfAwareness.DASHBOARDS,
    }


# Export for use by jarvis_v3.py
__all__ = ['SelfAwareness', 'create_awareness_api']
