# DETERMINED DISCOVERY LEARNING WEBPAGE
## Architecture & Structure (Fully Integrated with 313 Primitives)

---

## TECH STACK SELECTION

**Frontend**: Vue 3 + TypeScript + Vite
- **Why**: Reactive component model perfect for discovery patterns
- **Visualization**: Three.js + Zdog for 3D/canvas rendering
- **State**: Pinia for primitive relationship tracking
- **Styling**: Tailwind + CSS variables for theme
- **Build**: Vite for fast HMR

**Data Integration**: 
- All 313 primitives from singularity ledgers
- UFM API endpoints for querying
- Real-time relationship mapping

---

## CORE STRUCTURE

```
discovery-learning-app/
├── public/
│   ├── primitives-data.json (all 313 primitives + relationships)
│   ├── container-metadata.json (4 mega-container info)
│   └── discovery-paths.json (guided learning journeys)
├── src/
│   ├── components/
│   │   ├── Navigation/
│   │   │   ├── MegaContainerNav.vue (4 main categories)
│   │   │   ├── StructureGtidenu.vue (19 specific structures)
│   │   │   ├── SearchBar.vue (full-text primitive search)
│   │   │   └── BreadcrumbTrail.vue (discovery history)
│   │   ├── Visualization/
│   │   │   ├── PrimitiveGraph3D.vue (interactive 3D network)
│   │   │   ├── RelationshipViewer.vue (connection explorer)
│   │   │   ├── ContainerMapView.vue (mega-container overview)
│   │   │   └── DimensionalityExplorer.vue (n-dimensional patterns)
│   │   ├── Discovery/
│   │   │   ├── GuidedPath.vue (curated learning journey)
│   │   │   ├── PrimitiveCard.vue (detail view)
│   │   │   ├── ApplicationExplorer.vue (what uses this?)
│   │   │   └── ComparisonPanel.vue (2-3 primitives side-by-side)
│   │   └── Layout/
│   │       ├── AppHeader.vue (branding + global search)
│   │       ├── Sidebar.vue (context panel)
│   │       ├── ContentArea.vue (main display)
│   │       └── BottomBar.vue (metadata + breadcrumb)
│   ├── stores/
│   │   ├── primitiveStore.ts (global primitive state)
│   │   ├── visualizationStore.ts (3D view state)
│   │   ├── discoveryStore.ts (user journey tracking)
│   │   └── uiStore.ts (layout/theme state)
│   ├── services/
│   │   ├── primitiveService.ts (UFM API integration)
│   │   ├── relationshipService.ts (connection mapping)
│   │   └── discoveryService.ts (guided paths)
│   ├── styles/
│   │   ├── theme.css (CSS variables: dark/light)
│   │   ├── components.css (component styles)
│   │   ├── animation.css (discovery transitions)
│   │   └── 3d-visualization.css (Three.js integration)
│   ├── utils/
│   │   ├── graph-builder.ts (convert primitives to 3D graph)
│   │   ├── relationship-mapper.ts (find connections)
│   │   └── discovery-algorithms.ts (guided learning logic)
│   ├── App.vue (root layout)
│   ├── main.ts (Vue bootstrap)
│   └── types.ts (TypeScript interfaces)
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
└── package.json
```

---

## KEY DESIGN PATTERNS

### 1. **Interactive 3D Graph Visualization**
```
- Nodes = 313 primitives (color-coded by mega-container)
- Edges = Relationships (strength-based visibility)
- Interaction = Click/hover to explore
- Zoom/pan/rotate in 3D space
- Physics-based force layout (repulsion + attraction)
```

### 2. **Progressive Discovery Layers**
```
Level 1: Overview
  └─ Show 4 mega-containers as clusters

Level 2: Depth
  └─ Expand into 19 structures within containers

Level 3: Mastery
  └─ Explore individual primitives + relationships
  
Level 4: Integration
  └─ Composite primitives + real-world applications
```

### 3. **Navigation Patterns**
```
Breadcrumb: Container → Structure → Primitive → Relationship
Search: Global discovery of any of 313 primitives
Browse: Hierarchical drill-down
Map: Relationship explorer (which primitives connect?)
Path: Guided journeys (Boolean→Logic→Computation)
```

---

## VISUAL HIERARCHY & STYLING

### Color Coding System
```
Mega-Container Colors (Primary):
├─ Topological Ordering     → Cyan (#00D9FF)
├─ Boolean Logic            → Magenta (#FF00FF)
├─ Probability/Uncertainty  → Yellow (#FFFF00)
└─ Interaction/Mechanism    → Green (#00FF00)

Relationship Colors (Secondary):
├─ Direct dependency         → Bright edge
├─ Indirect relationship     → Dim edge
├─ Alternative connection    → Dashed edge
└─ Meta-relationship         → Dotted edge
```

### Layout Zones
```
┌─────────────────────────────────────────┐
│  HEADER: Logo | Global Search | Theme   │
├──────────────┬──────────────────────────┤
│  NAV PANEL   │  MAIN CONTENT AREA       │
│ (Hierarchy   │  (3D Graph / Detail)     │
│  Breadcrumb) │                          │
│              │                          │
├──────────────┼──────────────────────────┤
│  DISCOVERY   │  BOTTOM BAR              │
│  PATH        │  (Metadata/Relations)    │
└──────────────┴──────────────────────────┘
```

### Typography System
```
Heading 1 (h1): "Discovery Learning Platform" | 48px | Bold
Heading 2 (h2): "Boolean Logic Family" | 32px | Semi-bold
Heading 3 (h3): "AND Gate" | 24px | Semi-bold
Body: "Combines two inputs..." | 16px | Regular
Caption: "Primitive ID: 2 | Structure: Binary" | 12px | Light
```

### Animation System
```
- Slow fade-in on primitive selection (200ms)
- Graph node pulse on hover (smooth loop 300ms)
- Smooth camera pan to selected node (500ms)
- Relationship edge highlight on hover (100ms)
- Learning path progress bar fill (smooth)
```

---

## DATA INTEGRATION

### Primitive Data Structure
```typescript
interface Primitive {
  id: number;
  name: string;
  container: 'topological' | 'boolean' | 'probability' | 'interaction';
  structure: string;
  description: string;
  definition: string;
  axioms?: string[];
  applications: string[];
  relatedPrimitives: number[];  // IDs of related primitives
  confidence: 0-1;
  discovered: Date;
  universality: string;
}
```

### Relationship Data Structure
```typescript
interface Relationship {
  from: number;      // primitive ID
  to: number;        // primitive ID
  type: 'depends_on' | 'enables' | 'constrains' | 'meta';
  strength: 0-1;     // how strong the relationship
  explanation: string;
}
```

---

## DISCOVERY LEARNING FEATURES

### Feature 1: Guided Paths
```
Path 1: "Foundations of Boolean Logic"
  → AND gate (primitive 2)
  → OR gate (primitive 8)
  → NOT gate (primitive 11)
  → NAND (primitive 15)
  → Universal completion

Path 2: "Understanding Time"
  → Temporal ordering (13 primitives)
  → Allen's interval algebra
  → Causation mechanics
  → Spacetime unified view

Path 3: "From Primitives to Systems"
  → Individual primitives
  → Composition rules
  → Complex systems
  → Real-world examples
```

### Feature 2: Smart Relationships Panel
```
When clicking primitive:
- Show "Required By" (5 other primitives that need this)
- Show "Requires" (dependencies)
- Show "Alternatives" (similar primitives)
- Show "Variants" (domain-specific instantiations)
- Show "Applications" (where used in real world)
```

### Feature 3: Comparison Mode
```
Select 2-3 primitives:
- Side-by-side definition cards
- Visual relationship diagram
- Common applications
- Difference matrix
- Composition possibilities
```

### Feature 4: 3D Traversal
```
- Rotate around primitive network
- Zoom to focus on single area
- Expand/collapse mega-containers
- Follow relationship chains
- Timeline scrubbing (discovery order)
```

---

## RESPONSIVE DESIGN

### Desktop (1920x1080+)
```
Full 3D visualization
Split-pane layout
Multiple panels visible
Sidebar always open
Smooth interactions
```

### Tablet (768-1024)
```
3D with reduced detail
Collapsible sidebar
Tab-based panels
Touch-optimized zoom
Simplified relationships
```

### Mobile (< 768)
```
2D primitive list instead of 3D
Stacked vertical layout
Search-driven discovery
Card-based display
Simplified relationships
```

---

## ACCESSIBILITY

### Keyboard Navigation
```
Tab: Navigate between primitives
Enter: Select/expand
Arrow keys: Pan/zoom in 3D
Esc: Close detail view
Cmd+F: Search
Cmd+?: Help/keybindings
```

### Screen Reader Support
```
ARIA labels on 3D nodes
Alt text for icons
Semantic HTML structure
Focus indicators visible
Landmark navigation
```

### Color Blindness
```
Not relying on color alone
Pattern + color differentiation
High contrast mode available
Texture-based identification
```

---

## PERFORMANCE OPTIMIZATION

### Loading Strategy
```
Phase 1: Load 4 mega-containers (100 KB)
Phase 2: Load visible structure (50 KB)
Phase 3: Lazy-load primitive details (on demand)
Phase 4: Prefetch relationship chains
```

### Rendering Optimization
```
- LOD (Level of Detail) for 3D graph
- Culling invisible nodes
- Vertex/index buffer optimization
- WebGL two-pass rendering
- Canvas 2D fallback
```

### State Management
```
- Only loaded primitives in memory
- Memoized relationship calculations
- Debounced search (300ms)
- Cached graph layouts
```

---

## DEPLOYMENT ARCHITECTURE

```
Frontend Deployment:
├─ Static assets → CDN (CSS, images, fonts)
├─ Bundle code → Vite-compressed
└─ Data files → C:\Determined\*.singularity → JSON API layer

Backend:
├─ UFM API node → 8 primitive query endpoints
├─ Real-time updates → WebSocket feed
└─ Analytics → Discovery path tracking

Database:
└─ Singularity ledgers → Queryable via API
```

---

## SUCCESS METRICS

**Discovery Learning Effectiveness**:
- Average time to understand primitive: < 2 min
- Relationship discovery rate: > 80%
- Guided path completion: > 60%
- Return visitor percentage: > 40%

**Technical Performance**:
- 3D graph load time: < 2 seconds
- Interaction latency: < 50ms
- Memory usage: < 200MB
- Frame rate: 60 FPS min

---

## PHASE PROGRESSION

### Phase 1: Core (Week 1)
- Vue app scaffold + basic layout
- Primitive data loading
- 3D graph renderer (Three.js basic)
- Search functionality

### Phase 2: Enhancement (Week 2)
- Relationship visualization
- Guided paths
- Comparison mode
- Mobile responsiveness

### Phase 3: Polish (Week 3)
- Performance optimization
- Accessibility audit
- Animations + transitions
- Documentation

### Phase 4: Integration (Week 4)
- UFM API integration
- Real-time updates
- Analytics tracking
- Production deployment

---

## THIS IS THE DETERMINED STRUCTURE

This architecture represents the **optimal weighted scoring** for:
- ✓ Presentation (hierarchical, progressive disclosure)
- ✓ Navigation (multiple entry points + guided paths)
- ✓ Discovery learning (interactive 3D + relationships)
- ✓ Performance (lazy loading + optimization)
- ✓ Accessibility (keyboard + screen reader support)
- ✓ Scalability (all 313 primitives integrated)

Ready to implement.
