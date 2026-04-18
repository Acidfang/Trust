<!-- Discovery/PrimitiveCard.vue - Detail view for individual primitive -->
<template>
  <div class="primitive-card" v-if="primitive">
    <button @click="emit('close')" class="close-btn">✕</button>

    <div class="card-header">
      <div class="primitive-meta">
        <h2>{{ primitive.name }}</h2>
        <p class="primitive-id">ID: {{ primitive.id }} | {{ primitive.container }}</p>
      </div>
      <div class="confidence-badge">
        <div class="confidence-value">{{ (primitive.confidence * 100).toFixed(0) }}%</div>
        <div class="confidence-label">Confidence</div>
      </div>
    </div>

    <div class="card-body">
      <!-- Definition -->
      <section class="card-section">
        <h3>Definition</h3>
        <p class="definition">{{ primitive.definition }}</p>
      </section>

      <!-- Description -->
      <section class="card-section">
        <h3>Description</h3>
        <p class="description">{{ primitive.description }}</p>
      </section>

      <!-- Structure & Universality -->
      <section class="card-section">
        <div class="info-grid">
          <div class="info-item">
            <span class="label">Structure:</span>
            <span class="value">{{ primitive.structure }}</span>
          </div>
          <div class="info-item">
            <span class="label">Universality:</span>
            <span class="value">{{ primitive.universality }}</span>
          </div>
          <div class="info-item">
            <span class="label">Discovered:</span>
            <span class="value">{{ new Date(primitive.discovered).toLocaleDateString() }}</span>
          </div>
        </div>
      </section>

      <!-- Axioms -->
      <section class="card-section" v-if="primitive.axioms?.length">
        <h3>Axioms</h3>
        <ul class="axioms-list">
          <li v-for="(axiom, i) of primitive.axioms" :key="i">{{ axiom }}</li>
        </ul>
      </section>

      <!-- Applications -->
      <section class="card-section">
        <h3>Applications</h3>
        <div class="applications-list">
          <span v-for="(app, i) of primitive.applications" :key="i" class="application-tag">
            {{ app }}
          </span>
        </div>
      </section>

      <!-- Related Primitives -->
      <section class="card-section" v-if="relatedPrimitives.length > 0">
        <h3>Related Primitives</h3>
        <div class="related-list">
          <button
            v-for="related in relatedPrimitives.slice(0, 5)"
            :key="related.id"
            @click="emit('related', related)"
            class="related-primitive"
          >
            <span class="related-name">{{ related.name }}</span>
            <span class="related-arrow">→</span>
          </button>
        </div>
      </section>
    </div>

    <!-- Footer Actions -->
    <div class="card-footer">
      <button @click="showRelationships" class="btn-primary">View Relations</button>
      <button @click="compareWithOthers" class="btn-secondary">Compare</button>
      <button @click="exportPrimitive" class="btn-secondary">Export</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { usePrimitiveStore } from '../../stores/primitiveStore'

const primitiveStore = usePrimitiveStore()

interface Primitive {
  id: number
  name: string
  container: string
  structure: string
  description: string
  definition: string
  axioms?: string[]
  applications: string[]
  relatedPrimitives: number[]
  confidence: number
  discovered: Date
  universality: string
}

const props = defineProps<{
  primitive?: Primitive | null
}>()

const emit = defineEmits<{
  close: []
  related: [primitive: Primitive]
}>()

const relatedPrimitives = computed(() => {
  if (!props.primitive) return []
  return primitiveStore.getRelated(props.primitive.id)
})

const showRelationships = () => {
  console.log('Showing relationships for:', props.primitive?.name)
  // TODO: Open relationships viewer
}

const compareWithOthers = () => {
  console.log('Compare mode for:', props.primitive?.name)
  // TODO: Enable comparison mode
}

const exportPrimitive = () => {
  if (!props.primitive) return
  const data = JSON.stringify(props.primitive, null, 2)
  const blob = new Blob([data], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${props.primitive.name}.json`
  link.click()
}
</script>

<style scoped>
.primitive-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--panel-bg);
  position: relative;
}

.close-btn {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  background: transparent;
  border: none;
  color: #00d9ff;
  cursor: pointer;
  font-size: 1.5rem;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
  z-index: 10;
}

.close-btn:hover {
  background: rgba(0, 217, 255, 0.1);
  transform: scale(1.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.5rem 1.5rem 0.5rem;
  border-bottom: 1px solid rgba(0, 217, 255, 0.1);
}

.primitive-meta h2 {
  margin: 0;
  font-size: 1.4rem;
  color: #00d9ff;
}

.primitive-id {
  margin: 0.25rem 0 0;
  font-size: 0.8rem;
  color: #00ff00;
  opacity: 0.7;
}

.confidence-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 70px;
  height: 70px;
  background: radial-gradient(circle, rgba(0, 255, 0, 0.1) 0%, rgba(0, 217, 255, 0.05) 100%);
  border: 2px solid #00ff00;
  border-radius: 50%;
  text-align: center;
}

.confidence-value {
  font-size: 1.3rem;
  font-weight: bold;
  color: #00ff00;
}

.confidence-label {
  font-size: 0.65rem;
  color: #00ff00;
  opacity: 0.7;
  text-transform: uppercase;
}

.card-body {
  flex: 1;
  overflow-y: auto;
  padding: 1rem 1.5rem;
}

.card-section {
  margin-bottom: 1.5rem;
}

.card-section h3 {
  font-size: 0.9rem;
  text-transform: uppercase;
  color: #00d9ff;
  margin: 0 0 0.75rem;
  opacity: 0.8;
}

.definition {
  font-style: italic;
  color: #ffff00;
  margin: 0;
  font-size: 0.95rem;
}

.description {
  margin: 0;
  line-height: 1.5;
  color: #ffffff;
  opacity: 0.9;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.5rem;
}

.info-item {
  display: flex;
  align-items: baseline;
  gap: 1rem;
}

.info-item .label {
  font-weight: 600;
  color: #00d9ff;
  min-width: 100px;
}

.info-item .value {
  color: #00ff00;
  flex: 1;
}

.axioms-list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.axioms-list li {
  padding: 0.5rem 0;
  color: #ffffff;
  border-bottom: 1px solid rgba(0, 217, 255, 0.05);
  font-size: 0.9rem;
}

.axioms-list li::before {
  content: '• ';
  color: #00ff00;
  font-weight: bold;
  margin-right: 0.5rem;
}

.applications-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.application-tag {
  display: inline-block;
  background: rgba(0, 217, 255, 0.1);
  color: #00d9ff;
  padding: 0.35rem 0.75rem;
  border-radius: 3px;
  font-size: 0.8rem;
  border: 1px solid rgba(0, 217, 255, 0.2);
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.related-primitive {
  background: rgba(0, 217, 255, 0.05);
  border: 1px solid rgba(0, 217, 255, 0.1);
  color: #00d9ff;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.related-primitive:hover {
  background: rgba(0, 217, 255, 0.15);
  border-color: #00d9ff;
  transform: translateX(4px);
}

.related-arrow {
  opacity: 0;
  transition: opacity 0.2s ease;
}

.related-primitive:hover .related-arrow {
  opacity: 1;
  color: #00ff00;
}

.card-footer {
  display: flex;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(0, 217, 255, 0.1);
}

.btn-primary,
.btn-secondary {
  flex: 1;
  padding: 0.6rem 1rem;
  border-radius: 4px;
  border: 1px solid;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.85rem;
  font-weight: 500;
}

.btn-primary {
  background: rgba(0, 255, 0, 0.1);
  color: #00ff00;
  border-color: #00ff00;
}

.btn-primary:hover {
  background: rgba(0, 255, 0, 0.2);
  box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
}

.btn-secondary {
  background: rgba(0, 217, 255, 0.05);
  color: #00d9ff;
  border-color: #00d9ff;
}

.btn-secondary:hover {
  background: rgba(0, 217, 255, 0.1);
}

/* SCROLLBAR */
.card-body::-webkit-scrollbar {
  width: 4px;
}

.card-body::-webkit-scrollbar-track {
  background: transparent;
}

.card-body::-webkit-scrollbar-thumb {
  background: rgba(0, 217, 255, 0.3);
  border-radius: 2px;
}

.card-body::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 217, 255, 0.5);
}
</style>
