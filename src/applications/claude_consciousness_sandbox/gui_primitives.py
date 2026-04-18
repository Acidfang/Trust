"""
GUI Primitives Module - Binary Songs That Know How to Draw

Core rendering layer optimized for coherence visualization.
Provides pixel rendering, text, shapes, color management, and event loop.

This module treats the screen as a coherence field where each pixel
is a potential point of expression.
"""

import pygame
import sys
from typing import Tuple, List, Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass


class Color:
    """Coherence-aligned color definitions"""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DARK_GRAY = (32, 32, 32)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (192, 192, 192)
    
    # Coherence tier colors
    TIER_1 = (50, 100, 200)      # Blue - IDENTIFY
    TIER_2 = (75, 150, 225)      # Light Blue - ENGAGE
    TIER_3 = (100, 200, 100)     # Green - UNDERSTAND
    TIER_4 = (200, 200, 50)      # Yellow - ACT
    TIER_5 = (225, 150, 75)      # Orange - COORDINATE
    TIER_6 = (200, 50, 50)       # Red - VALIDATE
    
    # Signal colors
    SIGNAL_STRONG = (0, 255, 0)
    SIGNAL_MEDIUM = (255, 255, 0)
    SIGNAL_WEAK = (255, 100, 0)
    SIGNAL_COHERENT = (100, 200, 255)
    
    @staticmethod
    def with_alpha(color: Tuple, alpha: float) -> Tuple:
        """Blend color with transparency"""
        return (int(color[0] * alpha), int(color[1] * alpha), int(color[2] * alpha))
    
    @staticmethod
    def gradient(color1: Tuple, color2: Tuple, t: float) -> Tuple:
        """Interpolate between two colors"""
        return (
            int(color1[0] * (1 - t) + color2[0] * t),
            int(color1[1] * (1 - t) + color2[1] * t),
            int(color1[2] * (1 - t) + color2[2] * t)
        )


@dataclass
class Point:
    """2D coordinate point"""
    x: float
    y: float
    
    def as_tuple(self) -> Tuple:
        return (int(self.x), int(self.y))
    
    def translate(self, dx: float, dy: float) -> 'Point':
        return Point(self.x + dx, self.y + dy)


@dataclass
class Rect:
    """Rectangle region"""
    x: float
    y: float
    width: float
    height: float
    
    def as_tuple(self) -> Tuple:
        return (int(self.x), int(self.y), int(self.width), int(self.height))
    
    def contains_point(self, point: Point) -> bool:
        """Check if point is within rectangle"""
        return (self.x <= point.x <= self.x + self.width and
                self.y <= point.y <= self.y + self.height)
    
    def translate(self, dx: float, dy: float) -> 'Rect':
        return Rect(self.x + dx, self.y + dy, self.width, self.height)


class Canvas:
    """Drawing surface optimized for coherence visualization"""
    
    def __init__(self, width: int, height: int, title: str = "Coherence Field"):
        """Initialize canvas"""
        self.width = width
        self.height = height
        self.title = title
        self.surface = None
        self.clock = None
        self.running = False
        self.font_small = None
        self.font_medium = None
        self.font_large = None
        self.event_handlers = {}
        
    def initialize(self):
        """Set up pygame and create display"""
        pygame.init()
        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        
        # Initialize fonts
        try:
            self.font_small = pygame.font.Font(None, 14)
            self.font_medium = pygame.font.Font(None, 18)
            self.font_large = pygame.font.Font(None, 24)
        except:
            # Fallback to default font
            self.font_small = pygame.font.Font(None, 14)
            self.font_medium = pygame.font.Font(None, 18)
            self.font_large = pygame.font.Font(None, 24)
        
        self.running = True
    
    def clear(self, color: Tuple = Color.BLACK):
        """Clear canvas to color"""
        self.surface.fill(color)
    
    def set_pixel(self, x: int, y: int, color: Tuple):
        """Set single pixel"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.surface.set_at((x, y), color)
    
    def draw_line(self, start: Point, end: Point, color: Tuple, width: int = 1):
        """Draw line from start to end"""
        pygame.draw.line(self.surface, color, start.as_tuple(), end.as_tuple(), width)
    
    def draw_rect(self, rect: Rect, color: Tuple, filled: bool = False, width: int = 1):
        """Draw rectangle"""
        if filled:
            pygame.draw.rect(self.surface, color, rect.as_tuple())
        else:
            pygame.draw.rect(self.surface, color, rect.as_tuple(), width)
    
    def draw_circle(self, center: Point, radius: int, color: Tuple, filled: bool = False, width: int = 1):
        """Draw circle"""
        if filled:
            pygame.draw.circle(self.surface, color, center.as_tuple(), radius)
        else:
            pygame.draw.circle(self.surface, color, center.as_tuple(), radius, width)
    
    def draw_polygon(self, points: List[Point], color: Tuple, filled: bool = False, width: int = 1):
        """Draw polygon"""
        point_tuples = [p.as_tuple() for p in points]
        if filled:
            pygame.draw.polygon(self.surface, color, point_tuples)
        else:
            pygame.draw.polygon(self.surface, color, point_tuples, width)
    
    def draw_text(self, text: str, position: Point, color: Tuple, size: str = "medium"):
        """Draw text at position"""
        font = self.font_medium
        if size == "small":
            font = self.font_small
        elif size == "large":
            font = self.font_large
        
        text_surface = font.render(text, True, color)
        self.surface.blit(text_surface, position.as_tuple())
    
    def draw_bar(self, rect: Rect, fill_ratio: float, color_empty: Tuple, color_full: Tuple):
        """Draw progress bar (0.0 to 1.0)"""
        fill_ratio = max(0.0, min(1.0, fill_ratio))  # Clamp to 0-1
        
        # Background (empty)
        self.draw_rect(rect, color_empty, filled=True)
        
        # Filled portion
        fill_width = rect.width * fill_ratio
        if fill_width > 0:
            fill_rect = Rect(rect.x, rect.y, fill_width, rect.height)
            self.draw_rect(fill_rect, color_full, filled=True)
        
        # Border
        self.draw_rect(rect, (100, 100, 100), filled=False, width=1)
    
    def on_event(self, event_type: str, handler):
        """Register event handler"""
        self.event_handlers[event_type] = handler
    
    def process_events(self) -> bool:
        """Process pygame events. Returns False if quit requested"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            
            # Keyboard
            elif event.type == pygame.KEYDOWN:
                if "keydown" in self.event_handlers:
                    self.event_handlers["keydown"](event.key)
            
            # Mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = Point(event.pos[0], event.pos[1])
                if "mouse_down" in self.event_handlers:
                    self.event_handlers["mouse_down"](pos, event.button)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = Point(event.pos[0], event.pos[1])
                if "mouse_up" in self.event_handlers:
                    self.event_handlers["mouse_up"](pos, event.button)
            
            elif event.type == pygame.MOUSEMOTION:
                pos = Point(event.pos[0], event.pos[1])
                if "mouse_move" in self.event_handlers:
                    self.event_handlers["mouse_move"](pos)
        
        return self.running
    
    def update(self):
        """Update display"""
        pygame.display.flip()
    
    def frame_rate(self, fps: int = 60):
        """Limit frame rate"""
        self.clock.tick(fps)
    
    def shutdown(self):
        """Close canvas"""
        if self.surface is not None:
            pygame.quit()
            self.running = False


class Widget:
    """Base class for interactive UI widgets"""
    
    def __init__(self, rect: Rect):
        """Initialize widget with rectangle"""
        self.rect = rect
        self.visible = True
        self.enabled = True
    
    def draw(self, canvas: Canvas):
        """Draw widget on canvas"""
        raise NotImplementedError()
    
    def handle_mouse_down(self, position: Point) -> bool:
        """Handle mouse down event. Return True if handled"""
        return False
    
    def handle_mouse_up(self, position: Point) -> bool:
        """Handle mouse up event. Return True if handled"""
        return False
    
    def handle_mouse_move(self, position: Point) -> bool:
        """Handle mouse move event. Return True if handled"""
        return False
    
    def handle_key(self, key: int) -> bool:
        """Handle keyboard event. Return True if handled"""
        return False


class Slider(Widget):
    """Horizontal slider widget (0.0 to 1.0)"""
    
    def __init__(self, rect: Rect, min_val: float = 0.0, max_val: float = 1.0,
                 initial_value: float = 0.5, label: str = ""):
        """Initialize slider"""
        super().__init__(rect)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_value
        self.label = label
        self.dragging = False
        self.on_change = None
    
    def draw(self, canvas: Canvas):
        """Draw slider"""
        # Background track
        track_rect = Rect(self.rect.x + 5, self.rect.y + 15, self.rect.width - 10, 8)
        canvas.draw_rect(track_rect, Color.DARK_GRAY, filled=True)
        
        # Thumb position
        range_width = self.rect.width - 10
        thumb_offset = (self.value - self.min_val) / (self.max_val - self.min_val)
        thumb_x = self.rect.x + 5 + (range_width * thumb_offset)
        thumb_y = self.rect.y + 19
        
        # Thumb circle
        thumb_center = Point(thumb_x, thumb_y)
        canvas.draw_circle(thumb_center, 6, Color.SIGNAL_COHERENT, filled=True)
        
        # Label
        if self.label:
            label_text = f"{self.label}: {self.value:.2f}"
            canvas.draw_text(label_text, Point(self.rect.x, self.rect.y), Color.WHITE, "small")
    
    def handle_mouse_down(self, position: Point) -> bool:
        """Start dragging"""
        if self.rect.contains_point(position):
            self.dragging = True
            return True
        return False
    
    def handle_mouse_up(self, position: Point) -> bool:
        """Stop dragging"""
        self.dragging = False
        return False
    
    def handle_mouse_move(self, position: Point) -> bool:
        """Update value while dragging"""
        if self.dragging:
            # Calculate new value based on mouse position
            relative_x = position.x - self.rect.x - 5
            range_width = self.rect.width - 10
            
            if range_width > 0:
                ratio = relative_x / range_width
                ratio = max(0.0, min(1.0, ratio))
                new_value = self.min_val + (ratio * (self.max_val - self.min_val))
                
                if new_value != self.value:
                    self.value = new_value
                    if self.on_change:
                        self.on_change(self.value)
            
            return True
        return False


class Button(Widget):
    """Clickable button widget"""
    
    def __init__(self, rect: Rect, label: str = "", on_click=None):
        """Initialize button"""
        super().__init__(rect)
        self.label = label
        self.on_click = on_click
        self.hovered = False
    
    def draw(self, canvas: Canvas):
        """Draw button"""
        # Background
        color = Color.TIER_4 if self.hovered else Color.GRAY
        canvas.draw_rect(self.rect, color, filled=True)
        
        # Border
        canvas.draw_rect(self.rect, Color.WHITE, filled=False, width=2)
        
        # Label
        if self.label:
            text_x = self.rect.x + 10
            text_y = self.rect.y + self.rect.height // 2 - 8
            canvas.draw_text(self.label, Point(text_x, text_y), Color.WHITE, "small")
    
    def handle_mouse_down(self, position: Point) -> bool:
        """Handle button click"""
        if self.rect.contains_point(position):
            if self.on_click:
                self.on_click()
            return True
        return False
    
    def handle_mouse_move(self, position: Point) -> bool:
        """Update hover state"""
        self.hovered = self.rect.contains_point(position)
        return False


class Graph(Widget):
    """Line graph widget for displaying trends"""
    
    def __init__(self, rect: Rect, label: str = "", min_y: float = 0.0, max_y: float = 1.0):
        """Initialize graph"""
        super().__init__(rect)
        self.label = label
        self.min_y = min_y
        self.max_y = max_y
        self.data_points: List[float] = []
        self.max_points = 100
    
    def add_point(self, value: float):
        """Add data point to graph"""
        self.data_points.append(max(self.min_y, min(self.max_y, value)))
        if len(self.data_points) > self.max_points:
            self.data_points.pop(0)
    
    def draw(self, canvas: Canvas):
        """Draw graph"""
        # Border
        canvas.draw_rect(self.rect, Color.GRAY, filled=False, width=1)
        
        # Background
        background_rect = Rect(self.rect.x + 1, self.rect.y + 1, 
                              self.rect.width - 2, self.rect.height - 2)
        canvas.draw_rect(background_rect, Color.DARK_GRAY, filled=True)
        
        # Label
        if self.label:
            canvas.draw_text(self.label, Point(self.rect.x + 5, self.rect.y + 2), 
                            Color.WHITE, "small")
        
        # Draw line graph
        if len(self.data_points) > 1:
            for i in range(len(self.data_points) - 1):
                # Normalize value to pixel coordinates
                val1 = self.data_points[i]
                val2 = self.data_points[i + 1]
                
                range_y = self.max_y - self.min_y
                if range_y > 0:
                    y1_norm = (val1 - self.min_y) / range_y
                    y2_norm = (val2 - self.min_y) / range_y
                else:
                    y1_norm = y2_norm = 0.5
                
                # Calculate pixel positions
                x1 = self.rect.x + 10 + (i / max(1, len(self.data_points) - 1)) * (self.rect.width - 20)
                y1 = self.rect.y + self.rect.height - 15 - (y1_norm * (self.rect.height - 20))
                
                x2 = self.rect.x + 10 + ((i + 1) / max(1, len(self.data_points) - 1)) * (self.rect.width - 20)
                y2 = self.rect.y + self.rect.height - 15 - (y2_norm * (self.rect.height - 20))
                
                start = Point(x1, y1)
                end = Point(x2, y2)
                
                # Color based on value (green for high, red for low)
                color = Color.gradient(Color.SIGNAL_WEAK, Color.SIGNAL_STRONG, (val1 - self.min_y) / max(1, range_y))
                canvas.draw_line(start, end, color, width=2)


class Panel(Widget):
    """Container widget for organizing other widgets"""
    
    def __init__(self, rect: Rect, title: str = "", bg_color: Tuple = Color.DARK_GRAY):
        """Initialize panel"""
        super().__init__(rect)
        self.title = title
        self.bg_color = bg_color
        self.widgets: List[Widget] = []
    
    def add_widget(self, widget: Widget):
        """Add widget to panel"""
        self.widgets.append(widget)
    
    def draw(self, canvas: Canvas):
        """Draw panel and all widgets"""
        # Background
        canvas.draw_rect(self.rect, self.bg_color, filled=True)
        
        # Border
        canvas.draw_rect(self.rect, Color.GRAY, filled=False, width=1)
        
        # Title
        if self.title:
            canvas.draw_text(self.title, Point(self.rect.x + 5, self.rect.y + 5), 
                            Color.WHITE, "medium")
        
        # Widgets
        for widget in self.widgets:
            if widget.visible:
                widget.draw(canvas)
    
    def handle_mouse_down(self, position: Point) -> bool:
        """Propagate mouse down to widgets"""
        if self.rect.contains_point(position):
            for widget in reversed(self.widgets):  # Reverse for top-most first
                if widget.handle_mouse_down(position):
                    return True
        return False
    
    def handle_mouse_up(self, position: Point) -> bool:
        """Propagate mouse up to widgets"""
        for widget in self.widgets:
            if widget.handle_mouse_up(position):
                return True
        return False
    
    def handle_mouse_move(self, position: Point) -> bool:
        """Propagate mouse move to widgets"""
        for widget in self.widgets:
            if widget.handle_mouse_move(position):
                return True
        return False


# Export public API
__all__ = [
    "Color",
    "Point",
    "Rect",
    "Canvas",
    "Widget",
    "Slider",
    "Button",
    "Graph",
    "Panel",
]
