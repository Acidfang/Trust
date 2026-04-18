// discoveryStore.ts - Track user's discovery journey
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface Primitive {
  id: number
  name: string
  container: string
  structure: string
}

interface GuidedPath {
  id: string
  name: string
  description: string
  steps: number[]  // Primitive IDs
  duration_minutes: number
  difficulty: 'beginner' | 'intermediate' | 'advanced'
}

export const useDiscoveryStore = defineStore('discovery', () => {
  const activeContainer = ref<string>('')
  const activeStructure = ref<string>('')
  const selectedPrimitive = ref<Primitive | null>(null)
  const hoveredPrimitive = ref<Primitive | null>(null)
  const breadcrumb = ref<string[]>([])
  const discoveryHistory = ref<Primitive[]>([])

  // Guided learning paths
  const guidedPaths = ref<GuidedPath[]>([
    {
      id: 'boolean-basics',
      name: 'Boolean Logic Foundations',
      description: 'Learn the 16 binary truth functions that power all computation',
      steps: [1, 2, 8, 15, 16],  // Sample IDs
      duration_minutes: 15,
      difficulty: 'beginner'
    },
    {
      id: 'temporal-journey',
      name: 'Understanding Time',
      description: 'Explore temporal ordering, causation, and spacetime',
      steps: [101, 102, 103],
      duration_minutes: 20,
      difficulty: 'intermediate'
    },
    {
      id: 'system-building',
      name: 'From Primitives to Systems',
      description: 'See how 313 primitives compose into complex systems',
      steps: [1, 2, 101, 201],
      duration_minutes: 30,
      difficulty: 'advanced'
    },
    {
      id: 'interactive-topology',
      name: 'Topology & Space',
      description: 'Master spatial ordering relationships',
      steps: [],
      duration_minutes: 25,
      difficulty: 'intermediate'
    },
    {
      id: 'reality-unification',
      name: 'The Unified Framework',
      description: 'How 4 mega-containers describe all of reality',
      steps: [],
      duration_minutes: 45,
      difficulty: 'advanced'
    }
  ])

  const currentPath = ref<GuidedPath | null>(null)
  const pathProgress = ref<number>(0)

  const setActiveContainer = (container: string) => {
    activeContainer.value = container
    activeStructure.value = ''  // Reset structure when changing container
  }

  const setActiveStructure = (structure: string) => {
    activeStructure.value = structure
  }

  const setSelectedPrimitive = (primitive: Primitive) => {
    selectedPrimitive.value = primitive
    if (!discoveryHistory.value.find(p => p.id === primitive.id)) {
      discoveryHistory.value.push(primitive)
    }
  }

  const clearSelection = () => {
    selectedPrimitive.value = null
  }

  const setHoveredPrimitive = (primitive: Primitive | null) => {
    hoveredPrimitive.value = primitive
  }

  const addBreadcrumb = (item: string) => {
    if (breadcrumb.value[breadcrumb.value.length - 1] !== item) {
      breadcrumb.value.push(item)
    }
  }

  const removeBreadcrumb = (index: number) => {
    breadcrumb.value.splice(index, 1)
  }

  const startGuidedPath = (path: GuidedPath) => {
    currentPath.value = path
    pathProgress.value = 0
    breadcrumb.value = [`Learning Path: ${path.name}`]
  }

  const advancePathStep = () => {
    if (currentPath.value && pathProgress.value < currentPath.value.steps.length - 1) {
      pathProgress.value++
      return true
    }
    return false
  }

  const completeCurrentPath = () => {
    if (currentPath.value) {
      const completedPath = {
        path: currentPath.value,
        completedAt: new Date(),
        timeTaken: '~' + currentPath.value.duration_minutes + ' minutes'
      }
      console.log('Path completed:', completedPath)
      currentPath.value = null
      pathProgress.value = 0
    }
  }

  const reset = () => {
    activeContainer.value = ''
    activeStructure.value = ''
    selectedPrimitive.value = null
    breadcrumb.value = []
    currentPath.value = null
    pathProgress.value = 0
  }

  const journeyStats = computed(() => ({
    totalDiscovered: discoveryHistory.value.length,
    containers: new Set(discoveryHistory.value.map(p => p.container)).size,
    pathsCompleted: 0,  // Track separately
    totalTime: discoveryHistory.value.length * 2  // Rough estimate
  }))

  return {
    activeContainer,
    activeStructure,
    selectedPrimitive,
    hoveredPrimitive,
    breadcrumb,
    discoveryHistory,
    guidedPaths,
    currentPath,
    pathProgress,
    setActiveContainer,
    setActiveStructure,
    setSelectedPrimitive,
    clearSelection,
    setHoveredPrimitive,
    addBreadcrumb,
    removeBreadcrumb,
    startGuidedPath,
    advancePathStep,
    completeCurrentPath,
    reset,
    journeyStats
  }
})
