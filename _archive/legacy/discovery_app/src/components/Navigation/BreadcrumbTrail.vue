<!-- Navigation/BreadcrumbTrail.vue -->
<template>
  <div class="breadcrumb-trail">
    <nav class="breadcrumb-nav">
      <button @click="goHome" class="breadcrumb-home">🏠</button>
      <span v-for="(item, index) in breadcrumb" :key="index" class="breadcrumb-separator">/</span>
      <button
        v-for="(item, index) in breadcrumb"
        :key="index"
        @click="goTo(index)"
        :class="['breadcrumb-item', { active: index === breadcrumb.length - 1 }]"
      >
        {{ item }}
      </button>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useDiscoveryStore } from '../../stores/discoveryStore'

const discoveryStore = useDiscoveryStore()

const breadcrumb = computed(() => discoveryStore.breadcrumb)

const goHome = () => {
  discoveryStore.reset()
}

const goTo = (index: number) => {
  discoveryStore.breadcrumb = discoveryStore.breadcrumb.slice(0, index + 1)
}
</script>

<style scoped>
.breadcrumb-trail {
  padding: 0.75rem 1.5rem;
  background: rgba(0, 217, 255, 0.02);
  border-bottom: 1px solid rgba(0, 217, 255, 0.1);
  overflow-x: auto;
}

.breadcrumb-nav {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.9rem;
  min-width: min-content;
}

.breadcrumb-home,
.breadcrumb-item {
  background: transparent;
  border: none;
  color: #00d9ff;
  cursor: pointer;
  padding: 0.25rem 0.75rem;
  border-radius: 3px;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.breadcrumb-home:hover,
.breadcrumb-item:hover {
  background: rgba(0, 217, 255, 0.1);
  color: #00ff00;
}

.breadcrumb-item.active {
  background: rgba(0, 217, 255, 0.1);
  color: #00ff00;
  font-weight: bold;
}

.breadcrumb-separator {
  color: rgba(0, 217, 255, 0.3);
  user-select: none;
}

@media (max-width: 768px) {
  .breadcrumb-trail {
    padding: 0.5rem 1rem;
  }

  .breadcrumb-nav {
    font-size: 0.8rem;
  }

  .breadcrumb-item {
    padding: 0.2rem 0.5rem;
  }
}
</style>
