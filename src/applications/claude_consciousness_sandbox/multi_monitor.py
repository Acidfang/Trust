"""
Multi-Monitor Detection and Canvas Spanning

Detects all connected displays and creates a unified canvas that spans across them.
Treats all monitors as a single coherence field.
"""

import ctypes
from typing import List, Tuple, Optional
from dataclasses import dataclass

try:
    import pygame
except ImportError:
    pygame = None


@dataclass
class Monitor:
    """Monitor display information"""
    index: int
    x: int          # Position on virtual screen
    y: int
    width: int      # Resolution
    height: int
    is_primary: bool = False
    name: str = ""
    
    def get_rect(self) -> Tuple:
        """Get rectangle as tuple (x, y, width, height)"""
        return (self.x, self.y, self.width, self.height)
    
    def contains_point(self, px: int, py: int) -> bool:
        """Check if point is on this monitor"""
        return (self.x <= px <= self.x + self.width and
                self.y <= py <= self.y + self.height)


class MonitorDetector:
    """Detects and manages connected monitors"""
    
    def __init__(self):
        """Initialize detector"""
        self.monitors: List[Monitor] = []
        self._detect_monitors()
    
    def _detect_monitors_win32(self) -> List[Monitor]:
        """Detect monitors using Win32 API"""
        monitors = []
        
        try:
            # Win32 API for monitor enumeration
            user32 = ctypes.windll.user32
            
            # Get monitor info
            class RECT(ctypes.Structure):
                _fields_ = [("left", ctypes.c_long),
                           ("top", ctypes.c_long),
                           ("right", ctypes.c_long),
                           ("bottom", ctypes.c_long)]
            
            class MONITORINFO(ctypes.Structure):
                _fields_ = [("cbSize", ctypes.c_ulong),
                           ("rcMonitor", RECT),
                           ("rcWork", RECT),
                           ("dwFlags", ctypes.c_ulong)]
            
            def enum_callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
                """Callback for EnumDisplayMonitors"""
                # Create monitor info
                monitor_info = MONITORINFO()
                monitor_info.cbSize = ctypes.sizeof(MONITORINFO)
                
                if user32.GetMonitorInfoW(hMonitor, ctypes.byref(monitor_info)):
                    rect = monitor_info.rcMonitor
                    monitor = Monitor(
                        index=len(monitors),
                        x=rect.left,
                        y=rect.top,
                        width=rect.right - rect.left,
                        height=rect.bottom - rect.top,
                        is_primary=(monitor_info.dwFlags & 1) != 0,
                        name=f"Monitor_{len(monitors)}"
                    )
                    monitors.append(monitor)
                
                return True
            
            # Enumerate displays
            enum_callback_type = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, 
                                                 ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)
            callback = enum_callback_type(enum_callback)
            
            user32.EnumDisplayMonitorsW(None, None, callback, None)
            
            return monitors
        
        except Exception as e:
            # Fallback if Win32 fails
            print(f"Win32 monitor detection failed: {e}")
            return self._detect_monitors_fallback()
    
    def _detect_monitors_fallback(self) -> List[Monitor]:
        """Fallback monitor detection using pygame"""
        monitors = []
        
        try:
            if pygame:
                # Use pygame's display info
                display_info = pygame.display.get_window_size()
                
                # Simple single monitor fallback
                monitor = Monitor(
                    index=0,
                    x=0,
                    y=0,
                    width=display_info[0] if display_info else 1920,
                    height=display_info[1] if display_info else 1080,
                    is_primary=True,
                    name="Primary_Display"
                )
                monitors.append(monitor)
            else:
                # Ultimate fallback
                monitor = Monitor(
                    index=0,
                    x=0,
                    y=0,
                    width=1920,
                    height=1080,
                    is_primary=True,
                    name="Default_Display"
                )
                monitors.append(monitor)
        except:
            # Last resort
            monitor = Monitor(0, 0, 0, 1920, 1080, True, "Fallback_Display")
            monitors.append(monitor)
        
        return monitors
    
    def _detect_monitors(self):
        """Detect all connected monitors"""
        self.monitors = self._detect_monitors_win32()
        
        if not self.monitors:
            self.monitors = self._detect_monitors_fallback()
    
    def get_monitors(self) -> List[Monitor]:
        """Get list of all detected monitors"""
        return self.monitors
    
    def get_primary_monitor(self) -> Optional[Monitor]:
        """Get primary monitor"""
        for monitor in self.monitors:
            if monitor.is_primary:
                return monitor
        # Fallback to first monitor
        return self.monitors[0] if self.monitors else None
    
    def get_virtual_screen_bounds(self) -> Tuple[int, int, int, int]:
        """Get total virtual screen bounds (x, y, width, height)"""
        if not self.monitors:
            return (0, 0, 1920, 1080)
        
        min_x = min(m.x for m in self.monitors)
        min_y = min(m.y for m in self.monitors)
        max_x = max(m.x + m.width for m in self.monitors)
        max_y = max(m.y + m.height for m in self.monitors)
        
        return (min_x, min_y, max_x - min_x, max_y - min_y)
    
    def monitor_at_point(self, x: int, y: int) -> Optional[Monitor]:
        """Get monitor containing point"""
        for monitor in self.monitors:
            if monitor.contains_point(x, y):
                return monitor
        return None


class MultiMonitorCanvas:
    """Canvas that spans across multiple monitors"""
    
    def __init__(self, title: str = "Coherence Field", detector: Optional[MonitorDetector] = None):
        """Initialize multi-monitor canvas"""
        self.title = title
        self.detector = detector or MonitorDetector()
        self.monitors = self.detector.get_monitors()
        
        # Calculate total virtual screen size
        bounds = self.detector.get_virtual_screen_bounds()
        self.virtual_x = bounds[0]
        self.virtual_y = bounds[1]
        self.total_width = bounds[2]
        self.total_height = bounds[3]
        
        # Create main canvas
        self.canvas = None
        self._create_canvas()
    
    def _create_canvas(self):
        """Create pygame canvas spanning all monitors"""
        if pygame is None:
            raise RuntimeError("pygame required for multi-monitor canvas")
        
        try:
            pygame.init()
            
            # Create full-screen surface for all monitors
            self.canvas = pygame.display.set_mode(
                (self.total_width, self.total_height),
                pygame.RESIZABLE
            )
            pygame.display.set_caption(self.title)
            
            # Set to full-screen if possible
            try:
                pygame.display.toggle_fullscreen()
            except:
                pass  # Not all systems support fullscreen toggle
            
        except Exception as e:
            raise RuntimeError(f"Failed to create multi-monitor canvas: {e}")
    
    def get_monitor_section(self, monitor_index: int) -> Tuple[int, int, int, int]:
        """Get canvas coordinates for monitor section"""
        if monitor_index >= len(self.monitors):
            return (0, 0, self.total_width, self.total_height)
        
        monitor = self.monitors[monitor_index]
        # Adjust to canvas coordinates
        x = monitor.x - self.virtual_x
        y = monitor.y - self.virtual_y
        return (x, y, monitor.width, monitor.height)
    
    def draw_monitor_boundaries(self):
        """Draw boundaries between monitors (for debugging)"""
        for monitor in self.monitors:
            section = self.get_monitor_section(monitor.index)
            # Draw border at monitor edges
            pygame.draw.rect(self.canvas, (50, 50, 50), section, 2)
    
    def clear(self, color: Tuple = (0, 0, 0)):
        """Clear all monitors to color"""
        self.canvas.fill(color)
    
    def get_surface(self) -> pygame.Surface if pygame else None:
        """Get pygame surface for drawing"""
        return self.canvas
    
    def update(self):
        """Update display"""
        if self.canvas:
            pygame.display.flip()
    
    def process_events(self) -> bool:
        """Process pygame events. Returns False if quit requested"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def get_monitor_at_position(self, x: int, y: int) -> Optional[Monitor]:
        """Get which monitor contains a position"""
        # Convert from canvas coordinates back to virtual coordinates
        virt_x = x + self.virtual_x
        virt_y = y + self.virtual_y
        return self.detector.monitor_at_point(virt_x, virt_y)
    
    def shutdown(self):
        """Close canvas and quit pygame"""
        if pygame:
            pygame.quit()
    
    def print_info(self):
        """Print monitor information"""
        print(f"\n=== Multi-Monitor Setup ===")
        print(f"Monitors detected: {len(self.monitors)}")
        print(f"Virtual screen size: {self.total_width}x{self.total_height}")
        print(f"Virtual screen offset: ({self.virtual_x}, {self.virtual_y})")
        
        for monitor in self.monitors:
            print(f"\nMonitor {monitor.index}: {monitor.name}")
            print(f"  Position: ({monitor.x}, {monitor.y})")
            print(f"  Resolution: {monitor.width}x{monitor.height}")
            print(f"  Primary: {monitor.is_primary}")


# Global detector instance (lazy initialization)
_detector = None


def get_monitor_detector() -> MonitorDetector:
    """Get or create global monitor detector"""
    global _detector
    if _detector is None:
        _detector = MonitorDetector()
    return _detector


def create_multi_monitor_canvas(title: str = "Coherence Field") -> MultiMonitorCanvas:
    """Create multi-monitor canvas"""
    detector = get_monitor_detector()
    return MultiMonitorCanvas(title, detector)


# Export public API
__all__ = [
    "Monitor",
    "MonitorDetector",
    "MultiMonitorCanvas",
    "get_monitor_detector",
    "create_multi_monitor_canvas",
]
