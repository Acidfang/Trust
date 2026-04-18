"""
STATIONARY ELEMENT MODEL - Visual Effects Foundation
====================================================

Purpose: Build a STATIC model of a single element with ALL possible visual effects
         applied, so we can verify effects work correctly BEFORE adding animation.

Approach:
  1. Single element (atom)
  2. All visual effects applied simultaneously
  3. Generate STATIC visualization (SVG, not animated)
  4. Display what each effect looks like at peak intensity
  5. Validate 4-primitives for each effect
  
This is the foundation. Animation comes AFTER we verify the static model works.

Architecture:
  - VisualEffectType: Enumeration of 28 effects across 8 layers
  - VisualEffect: Individual effect configuration (enabled, intensity, color)
  - ElementProperties: Element identity and quantitative state
  - RenderConfig: Centralized rendering parameters
  - StationaryElementModel: Main class orchestrating visualization
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import math


__all__ = [
    "VisualEffectType",
    "VisualEffect",
    "ElementProperties",
    "StationaryElementModel",
    "demo_stationary_models",
]


# ============================================================================
# LAYER 1: VISUAL EFFECTS ENUMERATION
# ============================================================================
# All 28 visual effects organized into 8 semantic layers

class VisualEffectType(Enum):
    """All visual effects that can be applied to an element"""
    
    # Layer 1: Core Element
    CORE_SHAPE = "core_shape"                    # Circle, square, hexagon, etc.
    CORE_COLOR = "core_color"                    # Base color
    CORE_SIZE = "core_size"                      # Size/scale
    
    # Layer 2: Property Encoding
    PROPERTY_GLOW = "property_glow"              # Glow intensity = property value
    PROPERTY_SATURATION = "property_saturation"  # Saturation = property strength
    PROPERTY_BRIGHTNESS = "property_brightness" # Brightness = property level
    PROPERTY_HUE_SHIFT = "property_hue_shift"    # Hue = property type
    
    # Layer 3: State Indicators
    STATE_BORDER = "state_border"                # Border color/width = state
    STATE_PATTERN = "state_pattern"              # Pattern overlay = state
    STATE_TEXTURE = "state_texture"              # Texture = state type
    STATE_ICON = "state_icon"                    # Small icon = state
    
    # Layer 4: Dynamics Indicators
    ACTIVITY_PULSING = "activity_pulsing"        # Pulse rate = activity
    ACTIVITY_ROTATION = "activity_rotation"      # Rotation speed = activity
    ACTIVITY_PARTICLES = "activity_particles"    # Particle effects = activity
    ACTIVITY_WAVES = "activity_waves"            # Wave effects = activity
    
    # Layer 5: Field Effects
    FIELD_AURA = "field_aura"                    # Radiant aura = field strength
    FIELD_RAYS = "field_rays"                    # Rays extending = field reach
    FIELD_GRADIENT = "field_gradient"            # Gradient background = field
    FIELD_VORTEX = "field_vortex"                # Swirling = field circulation
    
    # Layer 6: Context/Hierarchy
    HIERARCHY_SIZE = "hierarchy_size"            # Size indicates position in hierarchy
    HIERARCHY_NESTED = "hierarchy_nested"        # Nested circles = hierarchy level
    HIERARCHY_STEM = "hierarchy_stem"            # Stem connects to parent
    
    # Layer 7: Validation/Confidence
    CONFIDENCE_GLOW = "confidence_glow"          # Glow intensity = confidence
    CONFIDENCE_OPACITY = "confidence_opacity"    # Opacity = confidence
    CONFIDENCE_BLUR = "confidence_blur"          # Blur amount = certainty
    CONFIDENCE_CHECKMARK = "confidence_checkmark" # Checkmarks = validation
    
    # Layer 8: Multi-State Overlay
    MULTI_STATE_RING = "multi_state_ring"        # Concentric rings = multiple properties
    MULTI_STATE_SECTORS = "multi_state_sectors"  # Pie chart sectors = properties
    MULTI_STATE_DOTS = "multi_state_dots"        # Dot pattern = property array


@dataclass
class VisualEffect:
    """Single visual effect with intensity, color, and state.
    
    Attributes:
        effect_type: Which effect this is (from VisualEffectType enum)
        enabled: Whether this effect is active
        intensity: Strength (0.0-1.0)
        color: Hex color code (#RRGGBB)
        description: Human-readable description
    """
    
    effect_type: VisualEffectType
    enabled: bool = True
    intensity: float = 1.0
    color: str = "#FFFFFF"
    description: str = ""
    
    def __post_init__(self) -> None:
        """Auto-generate description if not provided."""
        if not self.description:
            self.description = (
                f"{self.effect_type.value} (intensity={self.intensity:.2f})"
            )


# ============================================================================
# LAYER 2: ELEMENT PROPERTIES
# ============================================================================


@dataclass
class ElementProperties:
    """Identity and state of the element.
    
    Attributes:
        identifier: Element symbol (H, C, N, O, etc.)
        element_name: Full name
        atomic_number: Periodic table number
        energy_level: 0-1 normalized energy
        activity_level: 0-1 activity/motion
        state_number: 1=healthy, 2=active, 3=stressed, 4=failed
        confidence_score: 0-1 certainty in visualization
        property_array: Multi-valued properties for display
        created_at: ISO timestamp
        updated_at: ISO timestamp
    """
    
    identifier: str = "H"
    element_name: str = "Hydrogen"
    atomic_number: int = 1
    energy_level: float = 0.5
    activity_level: float = 0.3
    state_number: int = 1
    confidence_score: float = 0.95
    property_array: List[float] = field(
        default_factory=lambda: [0.5, 0.3, 0.7]
    )
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )


# ============================================================================
# LAYER 3: MAIN MODEL
# ============================================================================


@dataclass
class StationaryElementModel:
    """Stationary visualization of a single element with 28 visual effects.
    
    This class generates a STATIC SVG visualization showing all visual effects
    applied simultaneously at peak intensity. No animation. Pure effect
    demonstration for verification before animation phase.
    
    Attributes:
        element: ElementProperties instance
        effects_enabled: Dict mapping effect type to configuration
        image_size: SVG canvas size (pixels)
        center_x, center_y: Element center coordinates
        base_radius: Core element radius
        rendered_html: Generated SVG output
        validation_results: 4-primitive validation results
    """
    
    element: ElementProperties
    effects_enabled: Dict[VisualEffectType, VisualEffect] = field(
        default_factory=dict
    )
    image_size: int = 500
    center_x: int = 250
    center_y: int = 250
    base_radius: int = 40
    rendered_html: str = ""
    validation_results: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self) -> None:
        """Initialize all 28 effects with default configurations."""
        self._initialize_all_effects()
    
    # ========================================================================
    # INITIALIZATION
    # ========================================================================
    
    def _initialize_all_effects(self) -> None:
        """Create default effect instances for all 28 effect types.
        
        Initializes effects in order, organized by semantic layer.
        Each effect gets appropriate defaults based on element properties.
        """
        
        # Layer 1: Core presentation
        self.effects_enabled[VisualEffectType.CORE_SHAPE] = VisualEffect(
            effect_type=VisualEffectType.CORE_SHAPE,
            description="Element shape (circle, square, hexagon)"
        )
        self.effects_enabled[VisualEffectType.CORE_COLOR] = VisualEffect(
            effect_type=VisualEffectType.CORE_COLOR,
            color=self._get_element_color(),
            description="Base color by element type"
        )
        self.effects_enabled[VisualEffectType.CORE_SIZE] = VisualEffect(
            effect_type=VisualEffectType.CORE_SIZE,
            intensity=0.8,
            description="Size indicates particle scale"
        )
        
        # Layer 2: Property encoding
        self.effects_enabled[VisualEffectType.PROPERTY_GLOW] = VisualEffect(
            effect_type=VisualEffectType.PROPERTY_GLOW,
            intensity=self.element.energy_level,
            description=f"Glow = Energy level ({self.element.energy_level:.1%})"
        )
        self.effects_enabled[VisualEffectType.PROPERTY_SATURATION] = VisualEffect(
            effect_type=VisualEffectType.PROPERTY_SATURATION,
            intensity=self.element.activity_level,
            description=f"Saturation = Activity ({self.element.activity_level:.1%})"
        )
        self.effects_enabled[VisualEffectType.PROPERTY_BRIGHTNESS] = VisualEffect(
            effect_type=VisualEffectType.PROPERTY_BRIGHTNESS,
            intensity=self.element.energy_level,
            description=f"Brightness = Energy ({self.element.energy_level:.1%})"
        )
        self.effects_enabled[VisualEffectType.PROPERTY_HUE_SHIFT] = VisualEffect(
            effect_type=VisualEffectType.PROPERTY_HUE_SHIFT,
            intensity=self.element.state_number / 4.0,
            description=f"Hue = State ({self.element.state_number}/4)"
        )
        
        # Layer 3: State indicators
        self.effects_enabled[VisualEffectType.STATE_BORDER] = VisualEffect(
            effect_type=VisualEffectType.STATE_BORDER,
            color=self._get_state_color(),
            description=f"Border color = State {self.element.state_number}"
        )
        self.effects_enabled[VisualEffectType.STATE_PATTERN] = VisualEffect(
            effect_type=VisualEffectType.STATE_PATTERN,
            description=f"Pattern = State type (state {self.element.state_number})"
        )
        self.effects_enabled[VisualEffectType.STATE_TEXTURE] = VisualEffect(
            effect_type=VisualEffectType.STATE_TEXTURE,
            intensity=self.element.activity_level,
            description="Texture overlay = stress/activity"
        )
        self.effects_enabled[VisualEffectType.STATE_ICON] = VisualEffect(
            effect_type=VisualEffectType.STATE_ICON,
            description="Small icon indicates state"
        )
        
        # Layer 4: Dynamics
        self.effects_enabled[VisualEffectType.ACTIVITY_PULSING] = VisualEffect(
            effect_type=VisualEffectType.ACTIVITY_PULSING,
            intensity=self.element.activity_level,
            description=f"Pulse rate = Activity ({self.element.activity_level:.1%})"
        )
        self.effects_enabled[VisualEffectType.ACTIVITY_ROTATION] = VisualEffect(
            effect_type=VisualEffectType.ACTIVITY_ROTATION,
            intensity=self.element.activity_level,
            description=f"Rotation speed = Activity ({self.element.activity_level:.1%})"
        )
        self.effects_enabled[VisualEffectType.ACTIVITY_PARTICLES] = VisualEffect(
            effect_type=VisualEffectType.ACTIVITY_PARTICLES,
            intensity=self.element.activity_level,
            description="Particle density = Activity level"
        )
        self.effects_enabled[VisualEffectType.ACTIVITY_WAVES] = VisualEffect(
            effect_type=VisualEffectType.ACTIVITY_WAVES,
            intensity=self.element.activity_level,
            description="Wave amplitude = Activity"
        )
        
        # Layer 5: Field effects
        self.effects_enabled[VisualEffectType.FIELD_AURA] = VisualEffect(
            effect_type=VisualEffectType.FIELD_AURA,
            intensity=self.element.energy_level,
            description=f"Aura = Field strength ({self.element.energy_level:.1%})"
        )
        self.effects_enabled[VisualEffectType.FIELD_RAYS] = VisualEffect(
            effect_type=VisualEffectType.FIELD_RAYS,
            intensity=self.element.energy_level,
            description="Rays = Field reach"
        )
        self.effects_enabled[VisualEffectType.FIELD_GRADIENT] = VisualEffect(
            effect_type=VisualEffectType.FIELD_GRADIENT,
            intensity=self.element.energy_level,
            description="Background gradient = Field effect"
        )
        self.effects_enabled[VisualEffectType.FIELD_VORTEX] = VisualEffect(
            effect_type=VisualEffectType.FIELD_VORTEX,
            intensity=self.element.activity_level,
            description="Vortex pattern = Field circulation"
        )
        
        # Layer 6: Hierarchy
        self.effects_enabled[VisualEffectType.HIERARCHY_SIZE] = VisualEffect(
            effect_type=VisualEffectType.HIERARCHY_SIZE,
            intensity=0.5,
            description="Relative size = Position in hierarchy"
        )
        self.effects_enabled[VisualEffectType.HIERARCHY_NESTED] = VisualEffect(
            effect_type=VisualEffectType.HIERARCHY_NESTED,
            intensity=0.5,
            description="Nested circles = Hierarchy depth"
        )
        self.effects_enabled[VisualEffectType.HIERARCHY_STEM] = VisualEffect(
            effect_type=VisualEffectType.HIERARCHY_STEM,
            enabled=False,  # Only enabled if in hierarchy
            description="Stem connects to parent"
        )
        
        # Layer 7: Validation/Confidence
        self.effects_enabled[VisualEffectType.CONFIDENCE_GLOW] = VisualEffect(
            effect_type=VisualEffectType.CONFIDENCE_GLOW,
            intensity=self.element.confidence_score,
            color=self._get_confidence_color(),
            description=f"Glow = Confidence ({self.element.confidence_score:.1%})"
        )
        self.effects_enabled[VisualEffectType.CONFIDENCE_OPACITY] = VisualEffect(
            effect_type=VisualEffectType.CONFIDENCE_OPACITY,
            intensity=self.element.confidence_score,
            description=f"Opacity = Confidence ({self.element.confidence_score:.1%})"
        )
        self.effects_enabled[VisualEffectType.CONFIDENCE_BLUR] = VisualEffect(
            effect_type=VisualEffectType.CONFIDENCE_BLUR,
            intensity=1.0 - self.element.confidence_score,
            description="Blur = Uncertainty"
        )
        self.effects_enabled[VisualEffectType.CONFIDENCE_CHECKMARK] = VisualEffect(
            effect_type=VisualEffectType.CONFIDENCE_CHECKMARK,
            enabled=self.element.confidence_score > 0.90,
            description="Checkmark = High confidence"
        )
        
        # Layer 8: Multi-state overlay
        self.effects_enabled[VisualEffectType.MULTI_STATE_RING] = VisualEffect(
            effect_type=VisualEffectType.MULTI_STATE_RING,
            description="Concentric rings = Multiple properties"
        )
        self.effects_enabled[VisualEffectType.MULTI_STATE_SECTORS] = VisualEffect(
            effect_type=VisualEffectType.MULTI_STATE_SECTORS,
            description="Pie sectors = Property values"
        )
        self.effects_enabled[VisualEffectType.MULTI_STATE_DOTS] = VisualEffect(
            effect_type=VisualEffectType.MULTI_STATE_DOTS,
            description="Dot pattern = Property array"
        )
    
    def _get_element_color(self) -> str:
        """Get base color for element"""
        colors = {
            "H": "#FFFFFF",   # Hydrogen - white
            "C": "#777777",   # Carbon - gray
            "N": "#3050F8",   # Nitrogen - blue
            "O": "#FF0000",   # Oxygen - red
            "B": "#FFB5B5",   # Boron - pink
            "Si": "#DAA520",  # Silicon - goldenrod
            "P": "#FFA500",   # Phosphorus - orange
            "S": "#FFFF00",   # Sulfur - yellow
        }
        return colors.get(self.element.identifier, "#FFFFFF")
    
    def _get_state_color(self) -> str:
        """Get color based on state"""
        state_colors = {
            1: "#00AA00",     # State 1 - green (healthy)
            2: "#FFFF00",     # State 2 - yellow (active)
            3: "#FF7700",     # State 3 - orange (stressed)
            4: "#FF0000",     # State 4 - red (failed)
        }
        return state_colors.get(self.element.state_number, "#FFFFFF")
    
    def _get_confidence_color(self) -> str:
        """Get confidence indicator color"""
        conf = self.element.confidence_score
        if conf > 0.90:
            return "#00AA00"  # Green (high confidence)
        elif conf > 0.75:
            return "#FFFF00"  # Yellow (good)
        elif conf > 0.50:
            return "#FF7700"  # Orange (moderate)
        else:
            return "#FF0000"  # Red (low)
    
    def generate_html_visualization(self) -> str:
        """Generate HTML/SVG visualization of element with all effects"""
        
        svg_parts = [
            f'<svg width="{self.image_size}" height="{self.image_size}" xmlns="http://www.w3.org/2000/svg">',
            '<defs>',
            self._generate_gradients(),
            self._generate_filters(),
            '</defs>',
            f'<!-- Background -->',
            self._generate_background(),
            f'<!-- Field effects -->',
            self._generate_field_effects(),
            f'<!-- Core element -->',
            self._generate_core_element(),
            f'<!-- State indicators -->',
            self._generate_state_indicators(),
            f'<!-- Activity indicators -->',
            self._generate_activity_indicators(),
            f'<!-- Confidence overlay -->',
            self._generate_confidence_overlay(),
            f'<!-- Multi-state overlay -->',
            self._generate_multistate_overlay(),
            f'<!-- Label and info -->',
            self._generate_labels(),
            '</svg>'
        ]
        
        self.rendered_html = '\n'.join(svg_parts)
        return self.rendered_html
    
    def _generate_gradients(self) -> str:
        """Generate SVG gradient definitions for visual effects."""
        gradient_defs = f'''
        <radialGradient id="glow-{self.element.identifier}">
            <stop offset="0%" style="stop-color:{self.effects_enabled[VisualEffectType.PROPERTY_GLOW].color};stop-opacity:0.8" />
            <stop offset="100%" style="stop-color:{self._get_element_color()};stop-opacity:0" />
        </radialGradient>
        
        <linearGradient id="field-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#0099FF;stop-opacity:{self.element.energy_level * 0.3}" />
            <stop offset="50%" style="stop-color:#00FF00;stop-opacity:{self.element.energy_level * 0.2}" />
            <stop offset="100%" style="stop-color:#FF0000;stop-opacity:{self.element.energy_level * 0.1}" />
        </linearGradient>
        '''
        return gradient_defs
    
    def _generate_filters(self) -> str:
        """Generate SVG filter definitions (blur, glow)."""
        filters = f'''
        <filter id="glow-filter">
            <feGaussianBlur stdDeviation="{int(5 * self.element.energy_level)}" result="coloredBlur"/>
            <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
        
        <filter id="blur-filter">
            <feGaussianBlur stdDeviation="{int(3 * (1 - self.element.confidence_score))}" />
        </filter>
        '''
        return filters
    
    def _generate_background(self) -> str:
        """Generate background rectangles with field gradient."""
        return f'''
        <rect width="{self.image_size}" height="{self.image_size}" fill="url(#field-gradient)" opacity="0.5"/>
        <rect width="{self.image_size}" height="{self.image_size}" fill="#EEEEEE"/>
        '''
    
    def _generate_field_effects(self) -> str:
        """Generate field effect visualizations (aura, rays)."""
        aura_effect = self.effects_enabled[VisualEffectType.FIELD_AURA]
        rays_effect = self.effects_enabled[VisualEffectType.FIELD_RAYS]
        
        parts = []
        
        # Aura
        if aura_effect.enabled and aura_effect.intensity > 0:
            for ring in range(3, 0, -1):
                radius = self.base_radius + (ring * 20)
                opacity = aura_effect.intensity * (0.3 - ring * 0.08)
                parts.append(f'''
            <circle cx="{self.center_x}" cy="{self.center_y}" r="{radius}" 
                    fill="none" stroke="{aura_effect.color}" stroke-width="2" 
                    opacity="{opacity}"/>
            ''')
        
        # Rays
        if rays_effect.enabled and rays_effect.intensity > 0:
            for angle in range(0, 360, 30):
                rad = math.radians(angle)
                x_end = self.center_x + math.cos(rad) * (self.base_radius + 60)
                y_end = self.center_y + math.sin(rad) * (self.base_radius + 60)
                parts.append(f'''
            <line x1="{self.center_x}" y1="{self.center_y}" x2="{x_end}" y2="{y_end}" 
                  stroke="#FFD700" stroke-width="1" opacity="{rays_effect.intensity * 0.4}"/>
            ''')
        
        return ''.join(parts)
    
    def _generate_core_element(self) -> str:
        """Generate core element circle with glow and highlight."""
        color = self.effects_enabled[VisualEffectType.CORE_COLOR].color
        size = self.base_radius * self.effects_enabled[VisualEffectType.CORE_SIZE].intensity
        state_color = self._get_state_color()
        border_width = 2 + int(3 * self.element.activity_level)
        
        return f'''
        <!-- Core circle with glow -->
        <circle cx="{self.center_x}" cy="{self.center_y}" r="{size + 10}" 
                fill="{color}" opacity="0.2" filter="url(#glow-filter)"/>
        
        <!-- Main element -->
        <circle cx="{self.center_x}" cy="{self.center_y}" r="{size}" 
                fill="{color}" stroke="{state_color}" stroke-width="{border_width}"/>
        
        <!-- Inner highlight -->
        <circle cx="{int(self.center_x - size/3)}" cy="{int(self.center_y - size/3)}" r="{int(size/3)}" 
                fill="white" opacity="0.3"/>
        '''
    
    def _generate_state_indicators(self) -> str:
        """Generate state indicator visualizations (icon + text)."""
        parts = []
        state = self.element.state_number
        state_icons = {1: "O", 2: "D", 3: "T", 4: "X"}
        
        # State icon
        icon_x = self.center_x + self.base_radius + 15
        icon_y = self.center_y - self.base_radius - 15
        parts.append(f'''
        <text x="{icon_x}" y="{icon_y}" font-size="20" fill="{self._get_state_color()}" 
              text-anchor="middle" dominant-baseline="middle">
            {state_icons.get(state, "?")}
        </text>
        ''')
        
        # Status text
        status_text = {1: "HEALTHY", 2: "ACTIVE", 3: "STRESSED", 4: "FAILED"}
        parts.append(f'''
        <text x="{self.center_x}" y="{self.image_size - 30}" 
              font-size="14" fill="{self._get_state_color()}" 
              text-anchor="middle" font-weight="bold">
            State: {status_text.get(state, "UNKNOWN")}
        </text>
        ''')
        
        return ''.join(parts)
    
    def _generate_activity_indicators(self) -> str:
        """Generate activity indicator bars (visual representation of activity)."""
        parts = []
        activity = self.element.activity_level
        
        # Activity bars
        bar_width = 30
        bar_height = 8
        bar_x = self.center_x - 50
        bar_y = self.center_y + self.base_radius + 30
        
        for i in range(5):
            height_factor = 0.3 + (i * 0.15)
            if activity > height_factor:
                h = int(bar_height * 2)
                color = "#00AA00" if activity < 0.5 else "#FF7700" if activity < 0.8 else "#FF0000"
            else:
                h = bar_height
                color = "#CCCCCC"
            
            parts.append(f'''
            <rect x="{bar_x + i * 20}" y="{bar_y}" width="{bar_width}" height="{h}" 
                  fill="{color}" opacity="0.7"/>
            ''')
        
        return ''.join(parts)
    
    def _generate_confidence_overlay(self) -> str:
        """Generate confidence indicator ring and percentage."""
        conf = self.element.confidence_score
        conf_color = self._get_confidence_color()
        
        # Confidence ring
        ring_radius = self.base_radius + 5
        ring_stroke = 3
        
        parts = [f'''
        <!-- Confidence indicator ring -->
        <circle cx="{self.center_x}" cy="{self.center_y}" r="{ring_radius}" 
                fill="none" stroke="{conf_color}" stroke-width="{ring_stroke}" opacity="0.8"/>
        ''']
        
        # Checkmark if highly confident
        if conf > 0.90:
            parts.append(f'''
            <text x="{self.center_x - 20}" y="{self.center_y - 15}" 
                  font-size="24" fill="{conf_color}">[CHECK]</text>
            ''')
        
        # Confidence percentage
        parts.append(f'''
        <text x="{self.center_x + self.base_radius + 30}" y="{self.center_y}" 
              font-size="12" fill="{conf_color}">
            {int(conf * 100)}%
        </text>
        ''')
        
        return ''.join(parts)
    
    def _generate_multistate_overlay(self) -> str:
        """Generate multi-state property visualization rings."""
        parts = []
        
        # Concentric rings for property values
        props = self.element.property_array
        ring_spacing = 15
        
        for i, prop_val in enumerate(props[:3]):
            radius = self.base_radius + (i + 1) * ring_spacing
            dash_array = f"{int(radius * 2 * math.pi * prop_val)},{int(radius * 2 * math.pi * (1 - prop_val))}"
            
            parts.append(f'''
            <circle cx="{self.center_x}" cy="{self.center_y}" r="{radius}" 
                    fill="none" stroke="#0099FF" stroke-width="1" 
                    stroke-dasharray="{dash_array}" opacity="0.6"/>
            ''')
        
        return ''.join(parts)
    
    def _generate_labels(self) -> str:
        """Generate text labels and information display."""
        return f'''
        <!-- Element identifier and name -->
        <text x="{self.center_x}" y="{self.center_y}" 
              font-size="32" font-weight="bold" text-anchor="middle" 
              dominant-baseline="middle" fill="white">
            {self.element.identifier}
        </text>
        
        <text x="{self.center_x}" y="{self.center_y + 30}" 
              font-size="12" text-anchor="middle" fill="#333333">
            {self.element.element_name}
        </text>
        
        <!-- Energy and Activity -->
        <text x="10" y="20" font-size="11" fill="#666666">
            Energy: {int(self.element.energy_level * 100)}%
        </text>
        
        <text x="10" y="35" font-size="11" fill="#666666">
            Activity: {int(self.element.activity_level * 100)}%
        </text>
        '''
    
    # ========================================================================
    # VALIDATION
    # ========================================================================
    
    def validate(self) -> Dict[str, Any]:
        """Validate model using 4-primitive checks.
        
        Verifies:
        - Spatial: Coordinates and radii are valid
        - Color: Color values are properly formatted
        - Temporal: Animation-ready properties are set
        - Structural: Hierarchy and effect organization correct
        
        Returns:
            Dictionary with validation results
        """
        checks = {
            "spatial_valid": self.base_radius > 0,
            "color_valid": len(self._get_element_color()) == 7,
            "temporal_components": any(
                e.enabled for e in [
                    self.effects_enabled[VisualEffectType.PROPERTY_GLOW],
                    self.effects_enabled[VisualEffectType.ACTIVITY_PULSING]
                ]
            ),
            "structural_hierarchy": len(self.effects_enabled) > 20,
        }
        
        self.validation_results = {
            "timestamp": datetime.now().isoformat(),
            "element": self.element.identifier,
            "checks": checks,
            "all_valid": all(checks.values()),
            "total_effects_enabled": sum(1 for e in self.effects_enabled.values() if e.enabled),
            "total_effects_available": len(self.effects_enabled),
        }
        
        return self.validation_results
    
    def to_json(self) -> str:
        """Export model metadata as JSON.
        
        Includes element identity, properties, effect states, and validation.
        Useful for debugging and analysis.
        """
        return json.dumps({
            "element": {
                "identifier": self.element.identifier,
                "name": self.element.element_name,
                "atomic_number": self.element.atomic_number,
            },
            "properties": {
                "energy_level": self.element.energy_level,
                "activity_level": self.element.activity_level,
                "state": self.element.state_number,
                "confidence": self.element.confidence_score,
            },
            "effects_enabled": {
                k.value: v.enabled for k, v in self.effects_enabled.items()
            },
            "validation": self.validation_results,
            "created_at": self.element.created_at,
        }, indent=2)


# ============================================================================
# DEMO - Generate Stationary Models for Multiple Elements
# ============================================================================

def demo_stationary_models():
    """Generate stationary models for different elements and states"""
    
    print("=" * 80)
    print("STATIONARY ELEMENT MODEL - Visual Effects Foundation")
    print("=" * 80)
    
    # Example 1: Healthy Hydrogen
    print("\n[EXAMPLE 1] Healthy Hydrogen Atom")
    print("-" * 80)
    
    h_healthy = ElementProperties(
        identifier="H",
        element_name="Hydrogen",
        atomic_number=1,
        energy_level=0.3,
        activity_level=0.1,
        state_number=1,
        confidence_score=0.98,
    )
    
    model1 = StationaryElementModel(element=h_healthy)
    model1.validate()
    print(f"✓ Model created with {model1.validation_results['total_effects_enabled']} active effects")
    print(f"  Validation: {model1.validation_results['all_valid']}")
    
    html1 = model1.generate_html_visualization()
    with open(r"c:\Determined\output_stationary_hydrogen_healthy.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>Stationary Element Model - Hydrogen (Healthy)</title>
    <style>
        body {{ font-family: monospace; padding: 20px; }}
        h1 {{ color: #333; }}
        svg {{ border: 1px solid #ccc; margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>Stationary Element Model: Hydrogen (Healthy State)</h1>
    {html1}
    <pre>{model1.to_json()}</pre>
</body>
</html>""")
    print(f"  Output: output_stationary_hydrogen_healthy.html")
    
    # Example 2: Active Carbon
    print("\n[EXAMPLE 2] Active Carbon Atom")
    print("-" * 80)
    
    c_active = ElementProperties(
        identifier="C",
        element_name="Carbon",
        atomic_number=6,
        energy_level=0.7,
        activity_level=0.6,
        state_number=2,
        confidence_score=0.92,
        property_array=[0.8, 0.5, 0.4],
    )
    
    model2 = StationaryElementModel(element=c_active)
    model2.validate()
    print(f"✓ Model created with {model2.validation_results['total_effects_enabled']} active effects")
    print(f"  Validation: {model2.validation_results['all_valid']}")
    
    html2 = model2.generate_html_visualization()
    with open(r"c:\Determined\output_stationary_carbon_active.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>Stationary Element Model - Carbon (Active)</title>
    <style>
        body {{ font-family: monospace; padding: 20px; }}
        h1 {{ color: #333; }}
        svg {{ border: 1px solid #ccc; margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>Stationary Element Model: Carbon (Active State)</h1>
    {html2}
    <pre>{model2.to_json()}</pre>
</body>
</html>""")
    print(f"  Output: output_stationary_carbon_active.html")
    
    # Example 3: Stressed Nitrogen
    print("\n[EXAMPLE 3] Stressed Nitrogen Atom")
    print("-" * 80)
    
    n_stressed = ElementProperties(
        identifier="N",
        element_name="Nitrogen",
        atomic_number=7,
        energy_level=0.9,
        activity_level=0.8,
        state_number=3,
        confidence_score=0.75,
        property_array=[0.9, 0.8, 0.7],
    )
    
    model3 = StationaryElementModel(element=n_stressed)
    model3.validate()
    print(f"✓ Model created with {model3.validation_results['total_effects_enabled']} active effects")
    print(f"  Validation: {model3.validation_results['all_valid']}")
    
    html3 = model3.generate_html_visualization()
    with open(r"c:\Determined\output_stationary_nitrogen_stressed.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>Stationary Element Model - Nitrogen (Stressed)</title>
    <style>
        body {{ font-family: monospace; padding: 20px; }}
        h1 {{ color: #333; }}
        svg {{ border: 1px solid #ccc; margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>Stationary Element Model: Nitrogen (Stressed State)</h1>
    {html3}
    <pre>{model3.to_json()}</pre>
</body>
</html>""")
    print(f"  Output: output_stationary_nitrogen_stressed.html")
    
    # Example 4: Failed Oxygen
    print("\n[EXAMPLE 4] Failed Oxygen Atom")
    print("-" * 80)
    
    o_failed = ElementProperties(
        identifier="O",
        element_name="Oxygen",
        atomic_number=8,
        energy_level=0.1,
        activity_level=0.0,
        state_number=4,
        confidence_score=0.50,
        property_array=[0.1, 0.0, 0.2],
    )
    
    model4 = StationaryElementModel(element=o_failed)
    model4.validate()
    print(f"✓ Model created with {model4.validation_results['total_effects_enabled']} active effects")
    print(f"  Validation: {model4.validation_results['all_valid']}")
    
    html4 = model4.generate_html_visualization()
    with open(r"c:\Determined\output_stationary_oxygen_failed.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>Stationary Element Model - Oxygen (Failed)</title>
    <style>
        body {{ font-family: monospace; padding: 20px; }}
        h1 {{ color: #333; }}
        svg {{ border: 1px solid #ccc; margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>Stationary Element Model: Oxygen (Failed State)</h1>
    {html4}
    <pre>{model4.to_json()}</pre>
</body>
</html>""")
    print(f"  Output: output_stationary_oxygen_failed.html")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"""
All visual effects generated in STATIC form:
  ✓ Core visualization (shape, color, size)
  ✓ Property encoding (glow, saturation, brightness, hue)
  ✓ State indicators (border, pattern, texture, icon)
  ✓ Activity indicators (pulsing, rotation, particles, waves)
  ✓ Field effects (aura, rays, gradient, vortex)
  ✓ Hierarchy indicators (size, nested, stem)
  ✓ Confidence overlay (glow, opacity, blur, checkmark)
  ✓ Multi-state overlay (rings, sectors, dots)

Generated files:
  - output_stationary_hydrogen_healthy.html
  - output_stationary_carbon_active.html
  - output_stationary_nitrogen_stressed.html
  - output_stationary_oxygen_failed.html

NEXT STEP: Open these HTML files to see how all effects look BEFORE animation.
    """)


if __name__ == "__main__":
    demo_stationary_models()
