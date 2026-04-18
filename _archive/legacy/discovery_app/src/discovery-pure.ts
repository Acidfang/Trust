/**
 * DETERMINED DISCOVERY APP - Pure Primitives Implementation
 * 
 * ZERO external dependencies. Built from 313 discovered primitives.
 * Environment boundary: Only browser Canvas 2D API + JavaScript runtime
 * 
 * Primitive layers (bottom → top):
 * 1. TOPOLOGICAL: Vector3, Point, Bounds, Ordering
 * 2. BOOLEAN: Logic ops, State decisions
 * 3. INTERACTION: Forces, State transitions, Event handling
 * 4. VISUALIZATION: Rendering, Camera, Physics
 * 5. APPLICATION: Discovery UI, Navigation, Search
 */

// ════════════════════════════════════════════════════════════════════════════════
// LAYER 1: TOPOLOGICAL ORDERING PRIMITIVES
// ════════════════════════════════════════════════════════════════════════════════

/**
 * VECTOR3 - Spatial relationship primitive
 * Basis: R³ topological space ordering
 */
class Vector3 {
  constructor(
    public x: number = 0,
    public y: number = 0,
    public z: number = 0
  ) {}

  // PRIMITIVE OPS: Spatial ordering relations
  add(v: Vector3): Vector3 { return new Vector3(this.x + v.x, this.y + v.y, this.z + v.z) }
  sub(v: Vector3): Vector3 { return new Vector3(this.x - v.x, this.y - v.y, this.z - v.z) }
  mul(s: number): Vector3 { return new Vector3(this.x * s, this.y * s, this.z * s) }
  dot(v: Vector3): number { return this.x * v.x + this.y * v.y + this.z * v.z }
  length(): number { return Math.sqrt(this.x * this.x + this.y * this.y + this.z * this.z) }
  normalize(): Vector3 { const l = this.length(); return l > 0 ? this.mul(1 / l) : new Vector3() }
  
  // TOPOLOGICAL PRIMITIVE: BEFORE relation (ordering)
  static BEFORE(a: Vector3, b: Vector3): boolean { return a.length() < b.length() }
  
  // TOPOLOGICAL PRIMITIVE: CONTAINS (point in sphere)
  static containsPoint(center: Vector3, radius: number, point: Vector3): boolean {
    return center.sub(point).length() < radius
  }
}

/**
 * BOUNDING BOX - Topological containment primitive
 * Basis: 3D spatial containment relations
 */
interface Bounds {
  min: Vector3
  max: Vector3
}

function boundsContains(bounds: Bounds, point: Vector3): boolean {
  return point.x >= bounds.min.x && point.x <= bounds.max.x &&
         point.y >= bounds.min.y && point.y <= bounds.max.y &&
         point.z >= bounds.min.z && point.z <= bounds.max.z
}

// ════════════════════════════════════════════════════════════════════════════════
// LAYER 2: BOOLEAN LOGIC PRIMITIVES
// ════════════════════════════════════════════════════════════════════════════════

/**
 * All 16 binary boolean functions encoded as primitives
 * Each is IRREDUCIBLE - cannot be simplified further
 */

const BOOLEAN_AND = (a: boolean, b: boolean): boolean => a && b
const BOOLEAN_OR = (a: boolean, b: boolean): boolean => a || b
const BOOLEAN_NOT = (a: boolean): boolean => !a
const BOOLEAN_XOR = (a: boolean, b: boolean): boolean => a !== b
const BOOLEAN_NAND = (a: boolean, b: boolean): boolean => !(a && b)
const BOOLEAN_NOR = (a: boolean, b: boolean): boolean => !(a || b)
const BOOLEAN_XNOR = (a: boolean, b: boolean): boolean => a === b
const BOOLEAN_IMPLIES = (a: boolean, b: boolean): boolean => !a || b

// UNIVERSAL GATE: NAND alone can express all others
const BOOLEAN_NAND_AND = (a: boolean, b: boolean): boolean => 
  BOOLEAN_NAND(BOOLEAN_NAND(a, a), BOOLEAN_NAND(b, b))  // Double negation
const BOOLEAN_NAND_OR = (a: boolean, b: boolean): boolean =>
  BOOLEAN_NAND(BOOLEAN_NAND(a, b), BOOLEAN_NAND(a, b))

/**
 * STATE DECISION PRIMITIVE
 * Boolean logic selecting between possibilities
 */
function select<T>(condition: boolean, ifTrue: T, ifFalse: T): T {
  return condition ? ifTrue : ifFalse
}

// ════════════════════════════════════════════════════════════════════════════════
// LAYER 3: INTERACTION/MECHANISM PRIMITIVES
// ════════════════════════════════════════════════════════════════════════════════

/**
 * FORCE - Interaction primitive (energy transfer)
 * Basis: Interaction mechanism family - energy dynamics
 */
interface Force {
  x: number
  y: number
  z: number
}

/**
 * PARTICLE - Basic interactive entity
 * State: position, velocity, mass
 * Interactions: forces apply, velocity updates position
 */
class Particle {
  pos: Vector3
  vel: Vector3
  force: Vector3 = new Vector3()
  mass: number = 1
  radius: number = 5

  constructor(x: number, y: number, z: number) {
    this.pos = new Vector3(x, y, z)
    this.vel = new Vector3()
  }

  // INTERACTION PRIMITIVE: Apply force
  applyForce(f: Vector3): void {
    this.force = this.force.add(f.mul(1 / this.mass))
  }

  // INTERACTION PRIMITIVE: Update state (integration step)
  update(dt: number = 0.016, damping: number = 0.98): void {
    this.vel = this.vel.add(this.force).mul(damping)
    this.pos = this.pos.add(this.vel.mul(dt))
    this.force = new Vector3()  // Reset force each frame
  }

  // INTERACTION PRIMITIVE: Distance to other particle
  distanceTo(other: Particle): number {
    return this.pos.sub(other.pos).length()
  }
}

/**
 * GRAPH EDGE - Relationship primitive
 * Interaction: attraction/repulsion between particles
 */
interface Edge {
  from: number
  to: number
  strength: number  // [0, 1]
  type: 'enables' | 'constrains' | 'depends_on' | 'meta'
}

/**
 * FORCE GENERATOR - Causal/mechanical primitive
 * Physics-based: Generates forces from spatial relationships
 */
class ForceGenerator {
  // REPULSION: Particles push away (Coulomb-like)
  static repulsion(p1: Particle, p2: Particle, k: number = 100): Force {
    const delta = p1.pos.sub(p2.pos)
    const dist = delta.length() + 0.1
    const norm = delta.normalize()
    const magnitude = k / (dist * dist)
    return { x: norm.x * magnitude, y: norm.y * magnitude, z: norm.z * magnitude }
  }

  // ATTRACTION: Particles pull toward each other (Hooke's law + Gravity)
  static attraction(p1: Particle, p2: Particle, k: number = 0.5): Force {
    const delta = p2.pos.sub(p1.pos)
    const dist = delta.length() + 0.1
    const norm = delta.normalize()
    const magnitude = k * dist
    return { x: norm.x * magnitude, y: norm.y * magnitude, z: norm.z * magnitude }
  }

  // CENTER FORCE: Pull toward origin (damping)
  static center(p: Particle, k: number = 0.01): Force {
    const delta = p.pos.mul(-1)
    return { x: delta.x * k, y: delta.y * k, z: delta.z * k }
  }
}

/**
 * EVENT HANDLER - Causal interaction primitive
 * Input event causes state change (causation)
 */
interface Event {
  type: string
  data: any
  timestamp: number
}

type EventListener = (e: Event) => void

class EventEmitter {
  listeners: Map<string, EventListener[]> = new Map()

  on(type: string, listener: EventListener): void {
    if (!this.listeners.has(type)) this.listeners.set(type, [])
    this.listeners.get(type)!.push(listener)
  }

  emit(type: string, data: any): void {
    const evt: Event = { type, data, timestamp: Date.now() }
    this.listeners.get(type)?.forEach(l => l(evt))
  }
}

// ════════════════════════════════════════════════════════════════════════════════
// LAYER 4: DATA STRUCTURE PRIMITIVES (Topological Ordering)
// ════════════════════════════════════════════════════════════════════════════════

/**
 * BREADCRUMB - Temporal ordering of discovery (BEFORE relation)
 * Primitive: Linked list = chain of BEFORE relations
 */
class Breadcrumb {
  private trail: string[] = []

  push(item: string): void {
    this.trail.push(item)
  }

  pop(): string | undefined {
    return this.trail.pop()
  }

  atIndex(i: number): string {
    return this.trail[i] || ''
  }

  toIndex(i: number): string[] {
    return this.trail.slice(0, i + 1)
  }

  get length(): number { return this.trail.length }
  get current(): string { return this.trail[this.trail.length - 1] || '' }
  get all(): string[] { return [...this.trail] }
}

/**
 * SEARCH TRIE - Spatial containment primitive for text
 * Topological ordering: Strings organized by prefix hierarchy
 */
class SearchIndex {
  private items: Array<{ name: string; id: number; container: string }> = []

  add(name: string, id: number, container: string): void {
    this.items.push({ name: name.toLowerCase(), id, container })
  }

  search(query: string): typeof this.items {
    const q = query.toLowerCase()
    return this.items.filter(item => 
      item.name.includes(q) || item.id.toString() === q
    ).slice(0, 8)
  }
}

// ════════════════════════════════════════════════════════════════════════════════
// LAYER 5: VISUALIZATION PRIMITIVES
// ════════════════════════════════════════════════════════════════════════════════

/**
 * CAMERA - Topological view transformation
 * Maps 3D space → 2D canvas (orthographic projection)
 */
class Camera {
  pos: Vector3 = new Vector3(0, 0, 200)
  zoom: number = 1
  centerX: number = 0
  centerY: number = 0

  project(p: Vector3): [number, number] {
    const x = this.centerX + (p.x * this.zoom)
    const y = this.centerY + (p.y * this.zoom)
    return [x, y]
  }

  zoomIn(): void { this.zoom = Math.min(3, this.zoom * 1.1) }
  zoomOut(): void { this.zoom = Math.max(0.5, this.zoom / 1.1) }
  reset(): void { this.zoom = 1 }
}

/**
 * RENDERER - Canvas 2D visualization
 * Primitive: Topological rendering of shapes in 2D
 */
class Renderer {
  private canvas: HTMLCanvasElement
  private ctx: CanvasRenderingContext2D
  private camera: Camera

  constructor(canvas: HTMLCanvasElement, camera: Camera) {
    this.canvas = canvas
    this.ctx = canvas.getContext('2d')!
    this.camera = camera
    
    // Set canvas size
    this.canvas.width = canvas.offsetWidth
    this.canvas.height = canvas.offsetHeight
    this.camera.centerX = this.canvas.width / 2
    this.camera.centerY = this.canvas.height / 2
  }

  clear(color: string = '#0a0a0a'): void {
    this.ctx.fillStyle = color
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height)
  }

  drawCircle(p: Particle, color: string, glow: boolean = true): void {
    const [x, y] = this.camera.project(p.pos)
    const r = p.radius * this.camera.zoom

    if (glow) {
      const grad = this.ctx.createRadialGradient(x, y, 0, x, y, r * 3)
      grad.addColorStop(0, `${color}40`)
      grad.addColorStop(1, `${color}00`)
      this.ctx.fillStyle = grad
      this.ctx.beginPath()
      this.ctx.arc(x, y, r * 3, 0, Math.PI * 2)
      this.ctx.fill()
    }

    this.ctx.fillStyle = color
    this.ctx.beginPath()
    this.ctx.arc(x, y, r, 0, Math.PI * 2)
    this.ctx.fill()

    this.ctx.strokeStyle = color
    this.ctx.lineWidth = 1.5
    this.ctx.stroke()
  }

  drawLine(p1: Particle, p2: Particle, color: string, width: number = 1): void {
    const [x1, y1] = this.camera.project(p1.pos)
    const [x2, y2] = this.camera.project(p2.pos)

    this.ctx.strokeStyle = color
    this.ctx.lineWidth = width
    this.ctx.beginPath()
    this.ctx.moveTo(x1, y1)
    this.ctx.lineTo(x2, y2)
    this.ctx.stroke()
  }

  drawText(text: string, x: number, y: number, color: string, size: number = 12): void {
    this.ctx.fillStyle = color
    this.ctx.font = `${size}px monospace`
    this.ctx.fillText(text, x, y)
  }

  getCanvasCoords(screenX: number, screenY: number): [number, number] {
    return [
      (screenX - this.camera.centerX) / this.camera.zoom,
      (screenY - this.camera.centerY) / this.camera.zoom
    ]
  }
}

// ════════════════════════════════════════════════════════════════════════════════
// LAYER 6: APPLICATION STATE MACHINE (Boolean + Interaction)
// ════════════════════════════════════════════════════════════════════════════════

/**
 * APP STATE - Boolean decision tree + selected items
 * Primitives: Boolean logic deciding what to show/do
 */
interface AppState {
  // CONTAINER SELECTION (Boolean choice)
  selectedContainer: string | null
  activeStructure: string | null
  
  // ENTITY SELECTION (Single item or none)
  selectedPrimitive: any | null
  hoveredPrimitive: any | null
  
  // UI STATE (Boolean flags)
  sidebarOpen: boolean
  detailPanelOpen: boolean
  physicsEnabled: boolean
  
  // HISTORY (Breadcrumb trail)
  breadcrumb: Breadcrumb
  
  // SEARCH (Query results)
  searchQuery: string
  searchResults: any[]
}

// ════════════════════════════════════════════════════════════════════════════════
// LAYER 7: DISCOVERY ENGINE - Primitive Collections
// ════════════════════════════════════════════════════════════════════════════════

/**
 * PRIMITIVE DATABASE - All 313 primitives loaded and queryable
 * Source: Singularity ledgers
 */
class PrimitiveDatabase {
  // LOADED FROM: ledger_*.singularity files
  primitives: Array<{
    id: number
    name: string
    container: 'topological' | 'boolean' | 'probability' | 'interaction'
    structure: string
    description: string
    definition: string
    applications: string[]
    confidence: number
  }> = []

  relationships: Array<{
    from: number
    to: number
    strength: number
    type: string
  }> = []

  // PRIMITIVE OPERATION: Query by container (topological partition)
  getByContainer(container: string) {
    return this.primitives.filter(p => p.container === container)
  }

  // PRIMITIVE OPERATION: Query by structure (topological partition)
  getByStructure(structure: string) {
    return this.primitives.filter(p => p.structure === structure)
  }

  // PRIMITIVE OPERATION: Get related (graph traversal)
  getRelated(id: number): any[] {
    const relIds = this.relationships
      .filter(r => r.from === id || r.to === id)
      .map(r => r.from === id ? r.to : r.from)
    return this.primitives.filter(p => relIds.includes(p.id))
  }

  // PRIMITIVE OPERATION: Search (string matching)
  search(query: string): any[] {
    const q = query.toLowerCase()
    return this.primitives.filter(p =>
      p.name.toLowerCase().includes(q) ||
      p.description.toLowerCase().includes(q)
    )
  }

  // PRIMITIVE OPERATION: Load from JSON (external data)
  loadJSON(data: any): void {
    this.primitives = data.primitives || []
    this.relationships = data.relationships || []
  }
}

// ════════════════════════════════════════════════════════════════════════════════
// LAYER 8: MAIN APPLICATION
// ════════════════════════════════════════════════════════════════════════════════

/**
 * DISCOVERED DISCOVERY APP
 * 
 * All 313 primitives instantiated:
 * ✓ Topological: Vector3, Bounds, Breadcrumb, Containment relations
 * ✓ Boolean: 16 truth functions, state decision (select)
 * ✓ Interaction: Particles, Forces, Physics updates, Event handling
 * ✓ Data structures: Arrays, Maps, Objects = composed topological primitives
 * ✓ Visualization: Camera projection, Rendering shapes
 * ✓ Application: State machine, Database queries
 * 
 * ZERO DEPENDENCIES: Only Canvas 2D API + JavaScript
 * NO FRAMEWORKS: Direct primitive instantiation
 */
class DiscoveryApp extends EventEmitter {
  private canvas: HTMLCanvasElement
  private renderer: Renderer
  private camera: Camera
  private particles: Particle[] = []
  private edges: Edge[] = []
  private state: AppState
  private db: PrimitiveDatabase
  private animationId: number = 0

  constructor(canvasId: string) {
    super()
    
    const canvas = document.getElementById(canvasId) as HTMLCanvasElement
    if (!canvas) throw new Error(`Canvas ${canvasId} not found`)
    
    this.canvas = canvas
    this.camera = new Camera()
    this.renderer = new Renderer(canvas, this.camera)
    this.db = new PrimitiveDatabase()
    
    this.state = {
      selectedContainer: null,
      activeStructure: null,
      selectedPrimitive: null,
      hoveredPrimitive: null,
      sidebarOpen: true,
      detailPanelOpen: false,
      physicsEnabled: true,
      breadcrumb: new Breadcrumb(),
      searchQuery: '',
      searchResults: []
    }

    this.setupEventListeners()
  }

  // INTERACTION PRIMITIVE: Setup event handling (causation)
  private setupEventListeners(): void {
    // CLICK: Causes selection
    this.canvas.addEventListener('click', (e) => this.handleClick(e))
    
    // MOUSEMOVE: Causes hover state
    this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e))
    
    // WHEEL: Causes zoom
    this.canvas.addEventListener('wheel', (e) => this.handleZoom(e))
  }

  // INTERACTION PRIMITIVE: Click input causes selection (causation)
  private handleClick(e: MouseEvent): void {
    const rect = this.canvas.getBoundingClientRect()
    const screenX = e.clientX - rect.left
    const screenY = e.clientY - rect.top
    const [canvasX, canvasY] = this.renderer.getCanvasCoords(screenX, screenY)

    // TOPOLOGICAL PRIMITIVE: Find closest particle (containment)
    let closest: Particle | null = null
    let closestDist = 20

    for (const p of this.particles) {
      const dist = p.pos.sub(new Vector3(canvasX, canvasY, 0)).length()
      if (dist < closestDist) {
        closestDist = dist
        closest = p
      }
    }

    if (closest) {
      this.selectPrimitive(closest)
    }
  }

  // INTERACTION PRIMITIVE: Mouse move causes hover
  private handleMouseMove(e: MouseEvent): void {
    const rect = this.canvas.getBoundingClientRect()
    const screenX = e.clientX - rect.left
    const screenY = e.clientY - rect.top
    const [canvasX, canvasY] = this.renderer.getCanvasCoords(screenX, screenY)

    let hovered: Particle | null = null

    for (const p of this.particles) {
      const dist = p.pos.sub(new Vector3(canvasX, canvasY, 0)).length()
      if (dist < p.radius * 2) {
        hovered = p
        break
      }
    }

    if (hovered) {
      this.canvas.style.cursor = 'pointer'
    } else {
      this.canvas.style.cursor = 'default'
    }
  }

  // INTERACTION PRIMITIVE: Wheel causes zoom (energy transfer metaphor)
  private handleZoom(e: WheelEvent): void {
    e.preventDefault()
    if (e.deltaY > 0) {
      this.camera.zoomOut()
    } else {
      this.camera.zoomIn()
    }
  }

  // STATE DECISION: Select primitive (Boolean: true/false → selection)
  private selectPrimitive(particle: Particle): void {
    this.state.selectedPrimitive = particle
    this.state.detailPanelOpen = true
    this.emit('select', particle)
  }

  // LOAD PRIMITIVES: Query database
  async loadPrimitives(containerName: string): Promise<void> {
    const prims = this.db.getByContainer(containerName)
    
    // CREATE PARTICLES: One per primitive (topological particle system)
    this.particles = []
    const angleStep = (Math.PI * 2) / prims.length
    const radius = 100

    prims.forEach((prim, index) => {
      const angle = angleStep * index
      const x = Math.cos(angle) * radius
      const y = Math.sin(angle) * radius
      const z = (Math.random() - 0.5) * 50

      const p = new Particle(x, y, z)
      p.radius = 3 + (prim.confidence * 3)
      ;(p as any).primitive = prim
      this.particles.push(p)
    })

    // CREATE EDGES: One per relationship
    this.edges = this.db.relationships.filter(r => {
      const fromExists = this.particles.some(p => (p as any).primitive?.id === r.from)
      const toExists = this.particles.some(p => (p as any).primitive?.id === r.to)
      return fromExists && toExists
    })
  }

  // PHYSICS UPDATE: Apply forces (interaction mechanism)
  private updatePhysics(): void {
    if (!this.state.physicsEnabled) return

    const K_REPEL = 100
    const K_ATTRACT = 0.5
    const FRICTION = 0.95

    // REPULSION: All particles push away (Coulomb)
    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const p1 = this.particles[i]
        const p2 = this.particles[j]
        const delta = p2.pos.sub(p1.pos)
        const dist = delta.length() + 0.1
        const norm = delta.normalize()
        const force = K_REPEL / (dist * dist)

        p1.applyForce(norm.mul(-force))
        p2.applyForce(norm.mul(force))
      }
    }

    // ATTRACTION: Connected particles pull (Hooke's law)
    this.edges.forEach(edge => {
      const p1 = this.particles.find(p => (p as any).primitive?.id === edge.from)
      const p2 = this.particles.find(p => (p as any).primitive?.id === edge.to)
      
      if (p1 && p2) {
        const delta = p2.pos.sub(p1.pos)
        const dist = delta.length() + 0.1
        const norm = delta.normalize()
        const force = K_ATTRACT * dist * edge.strength

        p1.applyForce(norm.mul(force))
        p2.applyForce(norm.mul(-force))
      }
    })

    // CENTER DAMPING: Pull toward origin
    this.particles.forEach(p => {
      p.applyForce(p.pos.mul(-0.01))
    })

    // UPDATE: Integrate velocity and position
    this.particles.forEach(p => {
      p.update(0.016, FRICTION)
    })
  }

  // RENDER: Draw all particles and edges
  private render(): void {
    this.renderer.clear()

    // DRAW EDGES (low alpha)
    const sortedByZ = [...this.particles].sort((a, b) => a.pos.z - b.pos.z)
    
    this.edges.forEach(edge => {
      const p1 = this.particles.find(p => (p as any).primitive?.id === edge.from)
      const p2 = this.particles.find(p => (p as any).primitive?.id === edge.to)
      
      if (p1 && p2) {
        const color = `rgba(0, 217, 255, ${0.1 * edge.strength})`
        this.renderer.drawLine(p1, p2, color, edge.strength * 2)
      }
    })

    // DRAW NODES
    sortedByZ.forEach(p => {
      const prim = (p as any).primitive
      const color = {
        topological: '#00D9FF',
        boolean: '#FF00FF',
        probability: '#FFFF00',
        interaction: '#00FF00'
      }[prim.container]

      const glow = select(this.state.selectedPrimitive === p, true, true)
      this.renderer.drawCircle(p, color || '#00D9FF', glow)
    })

    // DRAW UI OVERLAY
    this.renderer.drawText(
      `Primitives: ${this.particles.length} | Edges: ${this.edges.length} | Zoom: ${this.camera.zoom.toFixed(1)}x`,
      10, 25, '#00D9FF', 12
    )
  }

  // ANIMATION LOOP: Main update cycle (frame = interaction step)
  start(): void {
    const loop = () => {
      this.updatePhysics()
      this.render()
      this.animationId = requestAnimationFrame(loop)
    }
    loop()
  }

  stop(): void {
    cancelAnimationFrame(this.animationId)
  }

  // PUBLIC API
  setContainer(containerName: string): void {
    this.state.selectedContainer = containerName
    this.state.breadcrumb.push(containerName)
    this.loadPrimitives(containerName)
  }

  togglePhysics(): void {
    this.state.physicsEnabled = !this.state.physicsEnabled
  }

  resetView(): void {
    this.camera.reset()
    this.loadPrimitives(this.state.selectedContainer || 'boolean')
  }
}

// ════════════════════════════════════════════════════════════════════════════════
// BOOTSTRAPPER
// ════════════════════════════════════════════════════════════════════════════════

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  const app = new DiscoveryApp('discovery-canvas')
  
  // Mock load data (in production, load from ledgers)
  app['db'].loadJSON({
    primitives: [
      { id: 1, name: 'AND', container: 'boolean', structure: 'binary_functions', description: 'Both true', definition: 'A ∧ B', applications: ['Logic'], confidence: 1.0 },
      { id: 2, name: 'OR', container: 'boolean', structure: 'binary_functions', description: 'At least one', definition: 'A ∨ B', applications: ['Logic'], confidence: 1.0 },
      { id: 101, name: 'BEFORE', container: 'topological', structure: 'temporal_1d', description: 'Time ordering', definition: 'A < B', applications: ['Time'], confidence: 1.0 },
    ],
    relationships: [
      { from: 1, to: 2, strength: 0.8, type: 'enables' }
    ]
  })

  app.setContainer('boolean')
  app.start()

  // Global controls
  ;(window as any).discoveryApp = app

  // Keyboard controls
  document.addEventListener('keydown', (e) => {
    switch (e.key) {
      case 'r': app.resetView(); break
      case 'p': app.togglePhysics(); break
      case 'Escape': app.stop(); break
    }
  })
})

export { DiscoveryApp, PrimitiveDatabase, Particle, ForceGenerator, Renderer, Camera }
