<!-- Visualization/PrimitiveGraph3D.vue - 3D Interactive Graph of 313 Primitives -->
<template>
  <div class="graph-visualization">
    <canvas ref="canvasElement"></canvas>
    <div class="graph-overlay">
      <div class="graph-info">
        <div class="info-item">
          <span class="label">Nodes:</span> {{ primitives.length }}
        </div>
        <div class="info-item">
          <span class="label">Relationships:</span> {{ relationships.length }}
        </div>
        <div class="info-item">
          <span class="label">Zoom:</span> {{ zoomLevel.toFixed(1) }}x
        </div>
      </div>

      <div class="graph-controls">
        <button @click="controlGraph('reset')" title="Reset view">↺</button>
        <button @click="controlGraph('zoom-in')" title="Zoom in">+</button>
        <button @click="controlGraph('zoom-out')" title="Zoom out">−</button>
        <button @click="togglePhysics" title="Toggle physics" :class="{ active: physicsEnabled }">
          F
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useUIStore } from '../../stores/uiStore'

interface Node {
  id: number
  name: string
  x: number
  y: number
  z: number
  vx: number
  vy: number
  vz: number
  color: string
  radius: number
  primitive: any
}

interface Edge {
  from: number
  to: number
  strength: number
}

const props = defineProps<{
  primitives: any[]
  relationships: any[]
}>()

const emit = defineEmits<{
  select: [primitive: any]
  hover: [primitive: any]
}>()

const uiStore = useUIStore()
const canvasElement = ref<HTMLCanvasElement>()
const zoomLevel = ref(1)
const physicsEnabled = ref(true)

const nodes = ref<Node[]>([])
const edges = ref<Edge[]>([])

const containerColors = {
  topological: '#00D9FF',
  boolean: '#FF00FF',
  probability: '#FFFF00',
  interaction: '#00FF00'
}

// Initialize visualization
onMounted(() => {
  if (!canvasElement.value) return

  const canvas = canvasElement.value
  const ctx = canvas.getContext('2d')
  
  // Set canvas size
  canvas.width = canvas.offsetWidth
  canvas.height = canvas.offsetHeight

  // Build node graph
  initializeGraph()

  // Start animation loop
  const animate = () => {
    if (!ctx) return

    // Clear canvas
    ctx.fillStyle = '#0a0a0a'
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    // Update physics
    if (physicsEnabled.value) {
      updatePhysics()
    }

    // Draw edges
    drawEdges(ctx)

    // Draw nodes
    drawNodes(ctx)

    requestAnimationFrame(animate)
  }

  animate()

  // Event listeners
  canvas.addEventListener('click', handleCanvasClick)
  canvas.addEventListener('mousemove', handleMouseMove)
  canvas.addEventListener('wheel', handleZoom)
})

const initializeGraph = () => {
  // Create nodes from primitives
  nodes.value = props.primitives.map((primitive, index) => {
    const angle = (index / props.primitives.length) * Math.PI * 2
    const radius = 100 + Math.random() * 50

    return {
      id: primitive.id,
      name: primitive.name,
      x: Math.cos(angle) * radius,
      y: Math.sin(angle) * radius,
      z: (Math.random() - 0.5) * 100,
      vx: 0,
      vy: 0,
      vz: 0,
      color: containerColors[primitive.container as keyof typeof containerColors],
      radius: 4 + (primitive.confidence * 2),
      primitive
    }
  })

  // Create edges from relationships
  edges.value = props.relationships.map(rel => ({
    from: rel.from,
    to: rel.to,
    strength: rel.strength
  }))
}

const updatePhysics = () => {
  const k_repel = 100      // Repulsion constant
  const k_attract = 0.5    // Attraction constant
  const friction = 0.95    // Friction

  // Repulsion between all nodes
  for (let i = 0; i < nodes.value.length; i++) {
    for (let j = i + 1; j < nodes.value.length; j++) {
      const n1 = nodes.value[i]
      const n2 = nodes.value[j]

      const dx = n2.x - n1.x
      const dy = n2.y - n1.y
      const dz = n2.z - n1.z
      const dist = Math.sqrt(dx * dx + dy * dy + dz * dz) + 0.1

      const force = k_repel / (dist * dist)

      n1.vx -= (force * dx) / dist
      n1.vy -= (force * dy) / dist
      n1.vz -= (force * dz) / dist

      n2.vx += (force * dx) / dist
      n2.vy += (force * dy) / dist
      n2.vz += (force * dz) / dist
    }
  }

  // Attraction along edges
  edges.value.forEach(edge => {
    const n1 = nodes.value.find(n => n.id === edge.from)
    const n2 = nodes.value.find(n => n.id === edge.to)

    if (!n1 || !n2) return

    const dx = n2.x - n1.x
    const dy = n2.y - n1.y
    const dz = n2.z - n1.z
    const dist = Math.sqrt(dx * dx + dy * dy + dz * dz) + 0.1

    const force = k_attract * dist * edge.strength

    n1.vx += (force * dx) / dist
    n1.vy += (force * dy) / dist
    n1.vz += (force * dz) / dist

    n2.vx -= (force * dx) / dist
    n2.vy -= (force * dy) / dist
    n2.vz -= (force * dz) / dist
  })

  // Update positions
  nodes.value.forEach(node => {
    node.vx *= friction
    node.vy *= friction
    node.vz *= friction

    node.x += node.vx
    node.y += node.vy
    node.z += node.vz
  })
}

const drawEdges = (ctx: CanvasRenderingContext2D) => {
  if (!canvasElement.value) return

  const centerX = canvasElement.value.width / 2
  const centerY = canvasElement.value.height / 2

  edges.value.forEach(edge => {
    const n1 = nodes.value.find(n => n.id === edge.from)
    const n2 = nodes.value.find(n => n.id === edge.to)

    if (!n1 || !n2) return

    const x1 = centerX + (n1.x * zoomLevel.value)
    const y1 = centerY + (n1.y * zoomLevel.value)
    const x2 = centerX + (n2.x * zoomLevel.value)
    const y2 = centerY + (n2.y * zoomLevel.value)

    ctx.strokeStyle = `rgba(0, 217, 255, ${0.1 * edge.strength})`
    ctx.lineWidth = edge.strength * 2
    ctx.beginPath()
    ctx.moveTo(x1, y1)
    ctx.lineTo(x2, y2)
    ctx.stroke()
  })
}

const drawNodes = (ctx: CanvasRenderingContext2D) => {
  if (!canvasElement.value) return

  const centerX = canvasElement.value.width / 2
  const centerY = canvasElement.value.height / 2

  // Sort by z-depth (draw far nodes first)
  const sorted = [...nodes.value].sort((a, b) => a.z - b.z)

  sorted.forEach(node => {
    const x = centerX + (node.x * zoomLevel.value)
    const y = centerY + (node.y * zoomLevel.value)

    // Draw glow
    const gradient = ctx.createRadialGradient(x, y, 0, x, y, node.radius * 3)
    gradient.addColorStop(0, `${node.color}40`)
    gradient.addColorStop(1, `${node.color}00`)
    
    ctx.fillStyle = gradient
    ctx.beginPath()
    ctx.arc(x, y, node.radius * 3, 0, Math.PI * 2)
    ctx.fill()

    // Draw node
    ctx.fillStyle = node.color
    ctx.beginPath()
    ctx.arc(x, y, node.radius, 0, Math.PI * 2)
    ctx.fill()

    // Draw border
    ctx.strokeStyle = node.color
    ctx.lineWidth = 1.5
    ctx.stroke()
  })
}

const handleCanvasClick = (event: MouseEvent) => {
  if (!canvasElement.value) return

  const rect = canvasElement.value.getBoundingClientRect()
  const centerX = canvasElement.value.width / 2
  const centerY = canvasElement.value.height / 2

  const clickX = (event.clientX - rect.left - centerX) / zoomLevel.value
  const clickY = (event.clientY - rect.top - centerY) / zoomLevel.value

  // Find closest node
  let closest = null
  let closestDist = 20

  nodes.value.forEach(node => {
    const dx = node.x - clickX
    const dy = node.y - clickY
    const dist = Math.sqrt(dx * dx + dy * dy)

    if (dist < closestDist) {
      closestDist = dist
      closest = node
    }
  })

  if (closest) {
    emit('select', closest.primitive)
  }
}

const handleMouseMove = (event: MouseEvent) => {
  if (!canvasElement.value) return

  const rect = canvasElement.value.getBoundingClientRect()
  const centerX = canvasElement.value.width / 2
  const centerY = canvasElement.value.height / 2

  const moveX = (event.clientX - rect.left - centerX) / zoomLevel.value
  const moveY = (event.clientY - rect.top - centerY) / zoomLevel.value

  // Find node under cursor
  let hovered = null

  for (const node of nodes.value) {
    const dx = node.x - moveX
    const dy = node.y - moveY
    const dist = Math.sqrt(dx * dx + dy * dy)

    if (dist < node.radius * 2) {
      hovered = node.primitive
      break
    }
  }

  if (hovered) {
    emit('hover', hovered)
    if (canvasElement.value) {
      canvasElement.value.style.cursor = 'pointer'
    }
  } else {
    if (canvasElement.value) {
      canvasElement.value.style.cursor = 'default'
    }
  }
}

const handleZoom = (event: WheelEvent) => {
  event.preventDefault()
  const delta = event.deltaY > 0 ? 0.9 : 1.1
  zoomLevel.value = Math.max(0.5, Math.min(3, zoomLevel.value * delta))
}

const controlGraph = (action: string) => {
  switch (action) {
    case 'reset':
      zoomLevel.value = 1
      initializeGraph()
      break
    case 'zoom-in':
      zoomLevel.value = Math.min(3, zoomLevel.value * 1.2)
      break
    case 'zoom-out':
      zoomLevel.value = Math.max(0.5, zoomLevel.value / 1.2)
      break
  }
}

const togglePhysics = () => {
  physicsEnabled.value = !physicsEnabled.value
}
</script>

<style scoped>
.graph-visualization {
  width: 100%;
  height: 100%;
  position: relative;
  background: radial-gradient(circle at 50% 50%, #0f0f1e 0%, #0a0a0a 100%);
}

canvas {
  display: block;
  width: 100%;
  height: 100%;
  cursor: grab;
}

canvas:active {
  cursor: grabbing;
}

.graph-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  padding: 1rem;
  pointer-events: none;
}

.graph-info,
.graph-controls {
  pointer-events: auto;
}

.graph-info {
  background: rgba(0, 217, 255, 0.1);
  border: 1px solid rgba(0, 217, 255, 0.3);
  border-radius: 6px;
  padding: 0.75rem 1rem;
  font-size: 0.85rem;
  color: #00d9ff;
}

.info-item {
  margin-bottom: 0.35rem;
}

.info-item:last-child {
  margin-bottom: 0;
}

.label {
  font-weight: 600;
}

.graph-controls {
  display: flex;
  gap: 0.5rem;
}

.graph-controls button {
  width: 36px;
  height: 36px;
  background: rgba(0, 217, 255, 0.1);
  border: 1px solid rgba(0, 217, 255, 0.3);
  color: #00d9ff;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1rem;
  font-weight: bold;
}

.graph-controls button:hover {
  background: rgba(0, 217, 255, 0.2);
  border-color: #00d9ff;
}

.graph-controls button.active {
  background: rgba(0, 255, 0, 0.2);
  border-color: #00ff00;
  color: #00ff00;
}
</style>
