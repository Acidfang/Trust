<!-- Navigation/SearchBar.vue - Global search for all 313 primitives -->
<template>
  <div class="search-bar">
    <input
      v-model="searchQuery"
      @input="handleSearch"
      @keyup.enter="performSearch"
      type="text"
      placeholder="Search 313 primitives... (AND, TEMPORAL, CAUSAL, etc.)"
      class="search-input"
    />
    
    <div v-if="searchResults.length > 0" class="search-results">
      <div
        v-for="result in searchResults.slice(0, 8)"
        :key="result.id"
        @click="selectResult(result)"
        class="search-result-item"
        :style="{ '--container-color': containerColors[result.container] }"
      >
        <span class="result-name">{{ result.name }}</span>
        <span class="result-structure">{{ result.structure }}</span>
        <span class="result-id">#{{ result.id }}</span>
      </div>
      <div v-if="searchResults.length > 8" class="search-more">
        +{{ searchResults.length - 8 }} more results
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { usePrimitiveStore } from '../../stores/primitiveStore'
import { useDiscoveryStore } from '../../stores/discoveryStore'

const primitiveStore = usePrimitiveStore()
const discoveryStore = useDiscoveryStore()

const searchQuery = ref('')
const searchResults = ref([])
const debouncedSearchTimeout = ref<NodeJS.Timeout>()

const containerColors = {
  topological: '#00D9FF',
  boolean: '#FF00FF',
  probability: '#FFFF00',
  interaction: '#00FF00'
}

const handleSearch = (event: Event) => {
  // Debounce search
  if (debouncedSearchTimeout.value) {
    clearTimeout(debouncedSearchTimeout.value)
  }

  debouncedSearchTimeout.value = setTimeout(() => {
    const query = (event.target as HTMLInputElement).value
    if (query.length > 1) {
      searchResults.value = primitiveStore.search(query)
      console.log(`Found ${searchResults.value.length} results for "${query}"`)
    } else {
      searchResults.value = []
    }
  }, 300)
}

const performSearch = () => {
  // Perform full search
  const results = primitiveStore.search(searchQuery.value)
  searchResults.value = results
  console.log(`Search complete: ${results.length} results`)
}

const selectResult = (primitive: any) => {
  discoveryStore.setSelectedPrimitive(primitive)
  discoveryStore.addBreadcrumb(`Search: ${primitive.name}`)
  searchResults.value = []
  searchQuery.value = ''
}

const emit = defineEmits<{
  search: [query: string]
}>()
</script>

<style scoped>
.search-bar {
  position: relative;
  flex: 1;
  max-width: 500px;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1.5rem;
  background: rgba(0, 217, 255, 0.05);
  border: 2px solid #00d9ff;
  border-radius: 6px;
  color: #00d9ff;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

.search-input::placeholder {
  color: rgba(0, 217, 255, 0.4);
}

.search-input:focus {
  outline: none;
  background: rgba(0, 217, 255, 0.1);
  border-color: #00ff00;
  box-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #1a1a2e;
  border: 1px solid #00d9ff;
  border-top: none;
  border-radius: 0 0 6px 6px;
  margin-top: -2px;
  max-height: 400px;
  overflow-y: auto;
  z-index: 1000;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
}

.search-result-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  background: rgba(0, 217, 255, 0.02);
  border-bottom: 1px solid rgba(0, 217, 255, 0.1);
  cursor: pointer;
  transition: all 0.15s ease;
}

.search-result-item:hover {
  background: rgba(0, 217, 255, 0.1);
  padding-left: 1.5rem;
}

.search-result-item::before {
  content: '';
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--container-color);
  opacity: 0;
  transition: opacity 0.15s ease;
}

.search-result-item:hover::before {
  opacity: 1;
}

.result-name {
  font-weight: 500;
  color: #00d9ff;
  flex: 1;
}

.result-structure {
  font-size: 0.75rem;
  color: #00ff00;
  text-transform: uppercase;
  opacity: 0.7;
}

.result-id {
  font-size: 0.75rem;
  color: #ffff00;
  opacity: 0.5;
}

.search-more {
  padding: 0.5rem 1rem;
  text-align: center;
  font-size: 0.8rem;
  color: #00d9ff;
  opacity: 0.5;
  background: rgba(0, 217, 255, 0.02);
}

/* Scrollbar styling */
.search-results::-webkit-scrollbar {
  width: 6px;
}

.search-results::-webkit-scrollbar-track {
  background: rgba(0, 217, 255, 0.05);
}

.search-results::-webkit-scrollbar-thumb {
  background: #00d9ff;
  border-radius: 3px;
}

.search-results::-webkit-scrollbar-thumb:hover {
  background: #00ff00;
}
</style>
