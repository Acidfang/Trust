// uiStore.ts - UI state management
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useLocalStorage } from '@vueuse/core'

export const useUIStore = defineStore('ui', () => {
  const theme = useLocalStorage('discovery-theme', 'dark')
  const sidebarCollapsed = ref(false)
  const detailPanelOpen = ref(false)
  const comparisonMode = ref(false)
  const selectedPrimitives = ref<number[]>([])
  const zoomLevel = ref(1)
  const visualizationType = ref<'3d' | '2d' | 'graph'>('3d')

  const toggleTheme = () => {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
    applyTheme()
  }

  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  const setDetailPanelOpen = (open: boolean) => {
    detailPanelOpen.value = open
  }

  const toggleComparisonMode = () => {
    comparisonMode.value = !comparisonMode.value
    if (!comparisonMode.value) {
      selectedPrimitives.value = []
    }
  }

  const togglePrimitiveSelection = (id: number) => {
    const index = selectedPrimitives.value.indexOf(id)
    if (index > -1) {
      selectedPrimitives.value.splice(index, 1)
    } else if (selectedPrimitives.value.length < 3) {
      selectedPrimitives.value.push(id)
    }
  }

  const setZoomLevel = (level: number) => {
    zoomLevel.value = Math.max(0.5, Math.min(3, level))
  }

  const setVisualizationType = (type: '3d' | '2d' | 'graph') => {
    visualizationType.value = type
  }

  const applyTheme = () => {
    if (theme.value === 'dark') {
      document.documentElement.style.colorScheme = 'dark'
    } else {
      document.documentElement.style.colorScheme = 'light'
    }
  }

  const reset = () => {
    sidebarCollapsed.value = false
    detailPanelOpen.value = false
    comparisonMode.value = false
    selectedPrimitives.value = []
    zoomLevel.value = 1
    visualizationType.value = '3d'
  }

  // Initialize theme on load
  applyTheme()

  return {
    theme,
    sidebarCollapsed,
    detailPanelOpen,
    comparisonMode,
    selectedPrimitives,
    zoomLevel,
    visualizationType,
    toggleTheme,
    toggleSidebar,
    setDetailPanelOpen,
    toggleComparisonMode,
    togglePrimitiveSelection,
    setZoomLevel,
    setVisualizationType,
    reset
  }
})
