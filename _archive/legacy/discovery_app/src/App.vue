<!-- MAIN APP COMPONENT -->
<!-- Discovery Learning Platform - Interactive 3D Exploration of 313 Primitives -->

<template>
  <div id="app" :class="[`theme-${uiStore.theme}`, 'discovery-app']">
    <!-- HEADER -->
    <header class="app-header">
      <div class="header-content">
        <div class="logo-section">
          <h1>🔬 DETERMINED Discovery Platform</h1>
          <p class="subtitle">Explore {{ primitiveStore.allPrimitives.length }} Universal Primitives</p>
        </div>
        <div class="search-section">
          <SearchBar @search="handleSearch" />
        </div>
        <div class="controls-section">
          <button @click="toggleTheme" class="btn-icon" title="Toggle theme">
            {{ uiStore.theme === 'dark' ? '☀️' : '🌙' }}
          </button>
          <button @click="showHelp" class="btn-icon" title="Help">?</button>
        </div>
      </div>
    </header>

    <!-- MAIN LAYOUT -->
    <div class="app-main">
      <!-- NAVIGATION/SIDEBAR -->
      <aside class="app-sidebar" :class="{ collapsed: uiStore.sidebarCollapsed }">
        <div class="sidebar-header">
          <h3>Navigation</h3>
          <button @click="uiStore.toggleSidebar" class="btn-collapse">
            {{ uiStore.sidebarCollapsed ? '→' : '←' }}
          </button>
        </div>
        
        <div class="sidebar-content">
          <!-- Mega-Container Navigation -->
          <nav class="nav-containers">
            <h4>Mega-Containers</h4>
            <button
              v-for="container in CONTAINERS"
              :key="container.id"
              @click="selectContainer(container)"
              :class="['nav-item', { active: discoveryStore.activeContainer === container.id }]"
              :style="{ '--container-color': container.color }"
            >
              <span class="color-dot"></span>
              {{ container.name }}
              <span class="count">({{ container.count }})</span>
            </button>
          </nav>

          <!-- Structure Navigation -->
          <nav class="nav-structures" v-if="discoveryStore.activeContainer">
            <h4>Structures</h4>
            <button
              v-for="struct in currentStructures"
              :key="struct.id"
              @click="selectStructure(struct)"
              :class="['nav-item', { active: discoveryStore.activeStructure === struct.id }]"
            >
              {{ struct.name }}
              <span class="count">({{ struct.primitives }})</span>
            </button>
          </nav>

          <!-- Guided Paths -->
          <nav class="nav-paths">
            <h4>Learning Paths</h4>
            <button
              v-for="path in discoveryStore.guidedPaths"
              :key="path.id"
              @click="startPath(path)"
              class="nav-item path"
            >
              🎯 {{ path.name }}
            </button>
          </nav>
        </div>
      </aside>

      <!-- MAIN CONTENT AREA -->
      <main class="app-content">
        <!-- Breadcrumb -->
        <BreadcrumbTrail v-if="discoveryStore.breadcrumb.length" />

        <!-- 3D VISUALIZATION -->
        <div class="visualization-container">
          <PrimitiveGraph3D
            :primitives="currentDisplayPrimitives"
            :relationships="currentRelationships"
            @select="selectPrimitive"
            @hover="hoverPrimitive"
          />
        </div>

        <!-- DETAIL PANEL -->
        <aside class="detail-panel" v-if="discoveryStore.selectedPrimitive">
          <PrimitiveCard
            :primitive="discoveryStore.selectedPrimitive"
            @close="discoveryStore.clearSelection"
            @related="selectPrimitive"
          />
        </aside>
      </main>
    </div>

    <!-- BOTTOM BAR -->
    <footer class="app-footer">
      <div class="footer-left">
        <span v-if="discoveryStore.hoveredPrimitive" class="hover-info">
          Hovering: {{ discoveryStore.hoveredPrimitive.name }}
        </span>
      </div>
      <div class="footer-center">
        <span class="stats">
          Viewing: {{ currentDisplayPrimitives.length }} primitives | 
          Confidence: {{ currentConfidence }}
        </span>
      </div>
      <div class="footer-right">
        <button @click="exportDiscovery" class="btn-small">Export Path</button>
        <button @click="resetView" class="btn-small">Reset View</button>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { usePrimitiveStore } from './stores/primitiveStore'
import { useDiscoveryStore } from './stores/discoveryStore'
import { useUIStore } from './stores/uiStore'
import SearchBar from './components/Navigation/SearchBar.vue'
import BreadcrumbTrail from './components/Navigation/BreadcrumbTrail.vue'
import PrimitiveGraph3D from './components/Visualization/PrimitiveGraph3D.vue'
import PrimitiveCard from './components/Discovery/PrimitiveCard.vue'

const primitiveStore = usePrimitiveStore()
const discoveryStore = useDiscoveryStore()
const uiStore = useUIStore()

const CONTAINERS = [
  {
    id: 'topological',
    name: 'Topological Ordering',
    count: 142,
    color: '#00D9FF'
  },
  {
    id: 'boolean',
    name: 'Boolean Logic Family',
    count: 16,
    color: '#FF00FF'
  },
  {
    id: 'probability',
    name: 'Uncertainty/Probability',
    count: 68,
    color: '#FFFF00'
  },
  {
    id: 'interaction',
    name: 'Interaction/Mechanism',
    count: 87,
    color: '#00FF00'
  }
]

const currentStructures = computed(() => {
  if (!discoveryStore.activeContainer) return []
  return primitiveStore.structuresByContainer(discoveryStore.activeContainer)
})

const currentDisplayPrimitives = computed(() => {
  if (discoveryStore.activeStructure) {
    return primitiveStore.primitivesByStructure(discoveryStore.activeStructure)
  }
  if (discoveryStore.activeContainer) {
    return primitiveStore.primitivesByContainer(discoveryStore.activeContainer)
  }
  return primitiveStore.allPrimitives
})

const currentRelationships = computed(() => {
  const primitiveIds = new Set(currentDisplayPrimitives.value.map(p => p.id))
  return primitiveStore.allRelationships.filter(
    r => primitiveIds.has(r.from) && primitiveIds.has(r.to)
  )
})

const currentConfidence = computed(() => {
  if (currentDisplayPrimitives.value.length === 0) return '0.87'
  const avg = currentDisplayPrimitives.value.reduce((sum, p) => sum + p.confidence, 0) / currentDisplayPrimitives.value.length
  return avg.toFixed(2)
})

const selectContainer = (container: any) => {
  discoveryStore.setActiveContainer(container.id)
  discoveryStore.addBreadcrumb(container.name)
}

const selectStructure = (struct: any) => {
  discoveryStore.setActiveStructure(struct.id)
  discoveryStore.addBreadcrumb(struct.name)
}

const selectPrimitive = (primitive: any) => {
  discoveryStore.setSelectedPrimitive(primitive)
  discoveryStore.addBreadcrumb(`${primitive.name} (${primitive.id})`)
}

const hoverPrimitive = (primitive: any) => {
  discoveryStore.setHoveredPrimitive(primitive)
}

const startPath = (path: any) => {
  discoveryStore.startGuidedPath(path)
  discoveryStore.addBreadcrumb(`Path: ${path.name}`)
}

const toggleTheme = () => {
  uiStore.toggleTheme()
}

const showHelp = () => {
  alert('DETERMINED Discovery Learning Platform\n\nNavigate: Click containers/structures\nSearch: Use search bar\nExplore: Click nodes in 3D graph\nCompare: Select multiple primitives\nLearn: Follow guided paths')
}

const exportDiscovery = () => {
  const discovery = {
    path: discoveryStore.breadcrumb,
    selected: discoveryStore.selectedPrimitive?.id,
    container: discoveryStore.activeContainer,
    timestamp: new Date().toISOString()
  }
  console.log('Exported discovery:', discovery)
  // TODO: Implement export
}

const resetView = () => {
  discoveryStore.reset()
  uiStore.reset()
}

onMounted(async () => {
  await primitiveStore.loadPrimitives()
  console.log(`Loaded ${primitiveStore.allPrimitives.length} primitives`)
})
</script>

<style scoped>
:root {
  --color-topological: #00D9FF;
  --color-boolean: #FF00FF;
  --color-probability: #FFFF00;
  --color-interaction: #00FF00;
  --color-bg-dark: #0a0a0a;
  --color-bg-light: #f5f5f5;
  --color-text-dark: #ffffff;
  --color-text-light: #000000;
}

.discovery-app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg);
  color: var(--text);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.theme-dark {
  --bg: var(--color-bg-dark);
  --text: var(--color-text-dark);
  --border: #333;
  --panel-bg: #1a1a1a;
}

.theme-light {
  --bg: var(--color-bg-light);
  --text: var(--color-text-light);
  --border: #ddd;
  --panel-bg: #fff;
}

/* HEADER */
.app-header {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  color: #00d9ff;
  padding: 1.5rem;
  border-bottom: 2px solid #00d9ff;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
  max-width: 1600px;
  margin: 0 auto;
}

.logo-section h1 {
  font-size: 2rem;
  margin: 0;
  text-shadow: 0 0 20px rgba(0, 217, 255, 0.5);
}

.subtitle {
  font-size: 0.9rem;
  color: #00d9ff;
  margin: 0.25rem 0 0;
  opacity: 0.8;
}

/* MAIN LAYOUT */
.app-main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* SIDEBAR */
.app-sidebar {
  width: 280px;
  background: var(--panel-bg);
  border-right: 1px solid var(--border);
  overflow-y: auto;
  transition: width 0.3s ease;
  padding: 1rem;
}

.app-sidebar.collapsed {
  width: 60px;
}

.app-sidebar.collapsed .sidebar-content {
  display: none;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.sidebar-header h3 {
  margin: 0;
}

.btn-collapse {
  background: transparent;
  border: none;
  color: var(--text);
  cursor: pointer;
  font-size: 1.2rem;
}

.nav-containers, .nav-structures, .nav-paths {
  margin-bottom: 2rem;
}

.nav-containers h4, .nav-structures h4, .nav-paths h4 {
  font-size: 0.85rem;
  text-transform: uppercase;
  color: #00d9ff;
  margin: 0 0 0.75rem;
  opacity: 0.7;
}

.nav-item {
  width: 100%;
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text);
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.nav-item:hover {
  background: rgba(0, 217, 255, 0.1);
  border-color: #00d9ff;
}

.nav-item.active {
  background: rgba(0, 217, 255, 0.2);
  border-color: #00d9ff;
  color: #00d9ff;
  font-weight: bold;
}

.color-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--container-color);
}

.count {
  font-size: 0.75rem;
  opacity: 0.6;
  margin-left: auto;
}

/* MAIN CONTENT */
.app-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.visualization-container {
  flex: 1;
  background: radial-gradient(circle at 50% 50%, #0f0f1e 0%, #0a0a0a 100%);
  overflow: hidden;
}

/* DETAIL PANEL */
.detail-panel {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 400px;
  background: var(--panel-bg);
  border-left: 1px solid var(--border);
  overflow-y: auto;
  box-shadow: -4px 0 12px rgba(0, 0, 0, 0.3);
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* FOOTER */
.app-footer {
  background: var(--panel-bg);
  border-top: 1px solid var(--border);
  padding: 0.75rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
  font-size: 0.85rem;
}

.stats {
  color: #00d9ff;
  opacity: 0.8;
}

.btn-icon, .btn-small {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text);
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.btn-icon:hover, .btn-small:hover {
  background: rgba(0, 217, 255, 0.1);
  border-color: #00d9ff;
  color: #00d9ff;
}

/* RESPONSIVE */
@media (max-width: 1024px) {
  .app-sidebar {
    width: 200px;
  }
  .detail-panel {
    width: 300px;
  }
}

@media (max-width: 768px) {
  .app-main {
    flex-direction: column;
  }
  .app-sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid var(--border);
    max-height: 200px;
  }
  .detail-panel {
    width: 100%;
    height: auto;
    position: relative;
    border-left: none;
  }
}
</style>
