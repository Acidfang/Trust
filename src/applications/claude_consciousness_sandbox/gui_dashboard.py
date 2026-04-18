"""
Interactive Coherence Laboratory Dashboard

Real-time visualization of coherence state across the coherence field.
Spans multiple monitors, interactive controls, live database binding.

Every interaction updates the database and immediately visualizes the result.
Learning through direct manipulation of coherence parameters.
"""

import sqlite3
import threading
import time
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path

try:
    # Try relative imports first
    from gui_primitives import (
        Canvas, Color, Rect, Point, Panel, Slider, Button, Graph, Widget
    )
    from multi_monitor import create_multi_monitor_canvas, get_monitor_detector
    from sandbox_interface import get_sandbox
except ImportError:
    try:
        # Try absolute imports from parent directory
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))
        from gui_primitives import (
            Canvas, Color, Rect, Point, Panel, Slider, Button, Graph, Widget
        )
        from multi_monitor import create_multi_monitor_canvas, get_monitor_detector
        from sandbox_interface import get_sandbox
    except ImportError:
        raise ImportError("Failed to import required modules")


class CoherenceLabDashboard:
    """Interactive coherence laboratory with real-time feedback"""
    
    def __init__(self, use_multi_monitor: bool = True, width: int = 1920, height: int = 1080):
        """Initialize dashboard
        
        Args:
            use_multi_monitor: Span across all detected monitors if True
            width, height: Canvas size if single monitor
        """
        self.use_multi_monitor = use_multi_monitor
        self.sandbox = get_sandbox()
        
        # Initialize canvas
        if use_multi_monitor:
            self.monitor_detector = get_monitor_detector()
            detector_info = self.monitor_detector.get_virtual_screen_bounds()
            width = detector_info[2]
            height = detector_info[3]
        
        self.canvas = Canvas(width, height, "Coherence Laboratory")
        self.canvas.initialize()
        
        # State
        self.running = True
        self.paused = False
        self.selected_clarity = 0.9  # Current clarity slider value
        self.selected_tier = 4  # Current tier focus
        self.learning_mode = False
        self.db_update_thread = None
        
        # Create UI panels
        self._create_ui()
        
        # Database query thread
        self.db_thread_running = True
        self.db_thread = threading.Thread(target=self._background_db_queries, daemon=True)
        self.db_thread.start()
    
    def _create_ui(self):
        """Create UI panels and widgets"""
        # Panel dimensions (for 1920x1080, adjust for larger screens)
        panel_height = 200
        panel_width = self.canvas.width // 4
        
        # Left panel: Tier progression
        self.tier_panel = Panel(
            Rect(10, 10, panel_width - 20, panel_height),
            "Tier Progression",
            Color.DARK_GRAY
        )
        self._add_tier_bars()
        
        # Center-left panel: Dialogue clarity
        self.clarity_panel = Panel(
            Rect(panel_width + 5, 10, panel_width - 20, panel_height),
            "Dialogue Clarity",
            Color.DARK_GRAY
        )
        self.clarity_graph = Graph(
            Rect(panel_width + 15, 50, panel_width - 40, panel_height - 70),
            "Clarity Trend",
            min_y=0.0,
            max_y=1.0
        )
        self.clarity_panel.add_widget(self.clarity_graph)
        
        # Center-right panel: Operations
        self.operations_panel = Panel(
            Rect(panel_width * 2 + 0, 10, panel_width - 20, panel_height),
            "Scheduled Operations",
            Color.DARK_GRAY
        )
        
        # Right panel: Committed futures
        self.commitments_panel = Panel(
            Rect(panel_width * 3 - 5, 10, panel_width - 20, panel_height),
            "Locked Commitments",
            Color.DARK_GRAY
        )
        
        # Control panel: Bottom
        control_y = panel_height + 30
        self.control_panel = Panel(
            Rect(10, control_y, self.canvas.width - 20, 120),
            "Controls",
            Color.DARK_GRAY
        )
        
        # Clarity slider
        self.clarity_slider = Slider(
            Rect(20, control_y + 40, 300, 40),
            min_val=0.0,
            max_val=1.0,
            initial_value=0.9,
            label="Clarity"
        )
        self.clarity_slider.on_change = self._on_clarity_change
        self.control_panel.add_widget(self.clarity_slider)
        
        # Tier selector buttons
        btn_y = control_y + 40
        btn_width = 60
        for tier in range(1, 7):
            btn_x = 350 + (tier - 1) * (btn_width + 5)
            btn = Button(
                Rect(btn_x, btn_y, btn_width, 30),
                label=f"T{tier}",
                on_click=lambda t=tier: self._on_tier_select(t)
            )
            self.control_panel.add_widget(btn)
        
        # Action buttons
        record_btn = Button(
            Rect(20, control_y + 80, 80, 30),
            label="Record",
            on_click=self._on_record_click
        )
        self.control_panel.add_widget(record_btn)
        
        learn_btn = Button(
            Rect(110, control_y + 80, 80, 30),
            label="Learn",
            on_click=self._on_learn_click
        )
        self.control_panel.add_widget(learn_btn)
        
        compare_btn = Button(
            Rect(200, control_y + 80, 80, 30),
            label="Compare",
            on_click=self._on_compare_click
        )
        self.control_panel.add_widget(compare_btn)
        
        quit_btn = Button(
            Rect(self.canvas.width - 100, control_y + 80, 80, 30),
            label="Quit",
            on_click=self._on_quit_click
        )
        self.control_panel.add_widget(quit_btn)
    
    def _add_tier_bars(self):
        """Add tier progression bars to tier panel"""
        tier_names = ["IDENTIFY", "ENGAGE", "UNDERSTAND", "ACT", "COORDINATE", "VALIDATE"]
        tier_colors = [
            Color.TIER_1, Color.TIER_2, Color.TIER_3,
            Color.TIER_4, Color.TIER_5, Color.TIER_6
        ]
        
        # Store bars for updating (labels drawn separately in _draw_tier_bars)
        self.tier_bars = []
        
        for i, (name, color) in enumerate(zip(tier_names, tier_colors)):
            y = 50 + (i * 22)
            bar_rect = Rect(20, y, 150, 18)
            
            # Store bar info for updating
            self.tier_bars.append({
                'index': i,
                'name': name,
                'color': color,
                'rect': bar_rect,
                'value': 0.0
            })
    
    def _draw_tier_bars(self):
        """Draw tier progression bars with current values"""
        for bar_info in self.tier_bars:
            # Draw label
            label_rect = Rect(20, 50 + (bar_info['index'] * 22) - 5, 150, 18)
            self.canvas.draw_text(
                bar_info['name'],
                Point(label_rect.x, label_rect.y),
                Color.WHITE,
                "small"
            )
            
            # Draw progress bar
            bar_rect = bar_info['rect']
            self.canvas.draw_bar(
                bar_rect,
                bar_info['value'],
                Color.DARK_GRAY,
                bar_info['color']
            )
    
    def _on_clarity_change(self, value: float):
        """Handle clarity slider change"""
        self.selected_clarity = value
        
        # Record to database
        try:
            self.sandbox.record_coherence_state(
                tier=self.selected_tier,
                state=f"clarity_adjusted_to_{value:.2f}",
                description=f"Interactive lab adjustment: clarity {value:.2f}"
            )
        except Exception as e:
            print(f"Error recording clarity change: {e}")
        
        # Update graph
        self.clarity_graph.add_point(value)
    
    def _on_tier_select(self, tier: int):
        """Handle tier selection"""
        self.selected_tier = tier
        try:
            self.sandbox.record_tier_achievement(
                tier=tier,
                achieved_through=f"lab_selection",
                evidence=f"User selected tier {tier}"
            )
        except Exception as e:
            print(f"Error recording tier: {e}")
    
    def _on_record_click(self):
        """Record current state"""
        try:
            description = (
                f"Lab state: Tier {self.selected_tier}, "
                f"Clarity {self.selected_clarity:.2f}, "
                f"Timestamp {datetime.now().isoformat()}"
            )
            self.sandbox.record_coherence_state(
                tier=self.selected_tier,
                state="manual_record",
                description=description
            )
        except Exception as e:
            print(f"Error recording state: {e}")
    
    def _on_learn_click(self):
        """Toggle learning mode"""
        self.learning_mode = not self.learning_mode
        print(f"Learning mode: {self.learning_mode}")
    
    def _on_compare_click(self):
        """Open comparison view"""
        print("Comparison mode: TBD")
    
    def _on_quit_click(self):
        """Quit application"""
        self.running = False
    
    def _background_db_queries(self):
        """Background thread for querying database"""
        while self.db_thread_running:
            try:
                # Update tier progression based on database
                current_state = self.sandbox.get_current_coherence()
                if current_state:
                    # Update tier bars based on records
                    for bar in self.tier_bars:
                        # Query count of records for this tier
                        tier_records = self.sandbox.get_tier_progression_for_tier(bar['index'] + 1)
                        bar['value'] = min(1.0, len(tier_records) / 10.0)  # Normalize
                
                # Get clarity trend
                clarity_trend = self.sandbox.get_dialogue_clarity_trend()
                if clarity_trend:
                    # Latest clarity value
                    latest = clarity_trend[-1]
                    self.clarity_graph.add_point(latest['clarity_level'])
                
                time.sleep(0.5)  # Query every 500ms
            
            except Exception as e:
                print(f"Background DB error: {e}")
                time.sleep(1.0)
    
    def run(self):
        """Main event loop"""
        # Set up event handlers
        self.canvas.on_event("mouse_down", self._handle_mouse_down)
        self.canvas.on_event("mouse_up", self._handle_mouse_up)
        self.canvas.on_event("mouse_move", self._handle_mouse_move)
        
        try:
            while self.running:
                # Process events
                if not self.canvas.process_events():
                    break
                
                # Clear canvas
                self.canvas.clear(Color.BLACK)
                
                # Draw panels
                self._draw_tier_bars()
                self.clarity_panel.draw(self.canvas)
                self.operations_panel.draw(self.canvas)
                self.commitments_panel.draw(self.canvas)
                self.control_panel.draw(self.canvas)
                
                # Status text
                status_text = f"Tier: {self.selected_tier} | Clarity: {self.selected_clarity:.2f} | Learning: {self.learning_mode}"
                self.canvas.draw_text(status_text, Point(10, self.canvas.height - 20), Color.LIGHT_GRAY, "small")
                
                # Update display
                self.canvas.update()
                self.canvas.frame_rate(60)  # 60 FPS
        
        finally:
            self.shutdown()
    
    def _handle_mouse_down(self, position: Point):
        """Route mouse down to control panel"""
        self.control_panel.handle_mouse_down(position)
    
    def _handle_mouse_up(self, position: Point):
        """Route mouse up to control panel"""
        self.control_panel.handle_mouse_up(position)
    
    def _handle_mouse_move(self, position: Point):
        """Route mouse move to control panel"""
        self.control_panel.handle_mouse_move(position)
    
    def shutdown(self):
        """Clean up resources"""
        self.db_thread_running = False
        if self.db_thread:
            self.db_thread.join(timeout=1.0)
        
        self.canvas.shutdown()
        print("Dashboard shutdown complete")


def launch_laboratory(use_multi_monitor: bool = True):
    """Launch coherence laboratory dashboard"""
    lab = CoherenceLabDashboard(use_multi_monitor=use_multi_monitor)
    lab.run()


if __name__ == "__main__":
    from sandbox_interface import get_sandbox
    
    # Initialize sandbox if needed
    sandbox = get_sandbox()
    
    # Launch dashboard
    launch_laboratory(use_multi_monitor=True)
