// primitiveStore.ts - Global primitive data management
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface Primitive {
  id: number
  name: string
  container: 'topological' | 'boolean' | 'probability' | 'interaction'
  structure: string
  description: string
  definition: string
  axioms?: string[]
  applications: string[]
  relatedPrimitives: number[]
  confidence: number
  discovered: Date
  universality: string
  confidence_range?: string
}

interface Relationship {
  from: number
  to: number
  type: 'depends_on' | 'enables' | 'constrains' | 'meta'
  strength: number
  explanation: string
}

export const usePrimitiveStore = defineStore('primitives', () => {
  const allPrimitives = ref<Primitive[]>([])
  const allRelationships = ref<Relationship[]>([])
  const searchResults = ref<Primitive[]>([])

  // Load all primitives from singularity ledgers
  const loadPrimitives = async () => {
    try {
      // In production, fetch from UFM API or singularity ledgers
      const response = await fetch('/primitives-data.json')
      const data = await response.json()
      allPrimitives.value = data.primitives
      allRelationships.value = data.relationships
    } catch (error) {
      console.error('Failed to load primitives:', error)
      // Fallback to sample data
      loadSamplePrimitives()
    }
  }

  // Sample data generator (for development)
  const loadSamplePrimitives = () => {
    allPrimitives.value = [
      // Boolean Logic (16 primitives)
      {
        id: 1,
        name: 'NONE (F false)',
        container: 'boolean',
        structure: 'binary_functions',
        description: 'No operation - always false',
        definition: 'F(A,B) = 0',
        applications: ['Null operation', 'Logic gates'],
        relatedPrimitives: [16],
        confidence: 1.0,
        discovered: new Date('2024-01-01'),
        universality: 'Complete basis (2^4)'
      },
      {
        id: 2,
        name: 'AND',
        container: 'boolean',
        structure: 'binary_functions',
        description: 'Both inputs true',
        definition: 'F(A,B) = A ∧ B',
        applications: ['Logic gates', 'Circuits', 'Conditionals'],
        relatedPrimitives: [3, 8, 15],
        confidence: 1.0,
        discovered: new Date('2024-01-01'),
        universality: 'Digital computation'
      },
      {
        id: 8,
        name: 'OR',
        container: 'boolean',
        structure: 'binary_functions',
        description: 'At least one true',
        definition: 'F(A,B) = A ∨ B',
        applications: ['Logic gates', 'Circuits', 'Conditionals'],
        relatedPrimitives: [2, 9, 15],
        confidence: 1.0,
        discovered: new Date('2024-01-01'),
        universality: 'Digital computation'
      },
      {
        id: 15,
        name: 'NAND',
        container: 'boolean',
        structure: 'binary_functions',
        description: 'Not (AND) - universal gate',
        definition: 'F(A,B) = ¬(A ∧ B)',
        applications: ['Universal computation', 'CPU design'],
        relatedPrimitives: [2, 16],
        confidence: 1.0,
        discovered: new Date('2024-01-01'),
        universality: 'Turing complete alone'
      },
      // Temporal (sample)
      {
        id: 101,
        name: 'BEFORE',
        container: 'topological',
        structure: 'temporal_1d',
        description: 'Time ordering relationship',
        definition: 'A BEFORE B means time(A) < time(B)',
        applications: ['Temporal logic', 'Event ordering', 'Causation'],
        relatedPrimitives: [102, 103],
        confidence: 1.0,
        discovered: new Date('2024-02-01'),
        universality: 'Allen\'s interval algebra'
      },
      {
        id: 102,
        name: 'AFTER',
        container: 'topological',
        structure: 'temporal_1d',
        description: 'Time ordering relationship (inverse)',
        definition: 'A AFTER B ↔ B BEFORE A',
        applications: ['Temporal logic', 'Event ordering', 'Causation'],
        relatedPrimitives: [101, 103],
        confidence: 1.0,
        discovered: new Date('2024-02-01'),
        universality: 'Allen\'s interval algebra'
      },
      // Causal (sample)
      {
        id: 201,
        name: 'CAUSE',
        container: 'interaction',
        structure: 'causal_mechanics',
        description: 'Event that triggers another',
        definition: 'A CAUSES B when A temporally precedes B and produces B',
        applications: ['Physics', 'Philosophy', 'Systems thinking'],
        relatedPrimitives: [202, 203],
        confidence: 0.9,
        discovered: new Date('2024-03-01'),
        universality: 'Foundational to change'
      }
    ]

    allRelationships.value = [
      { from: 1, to: 16, type: 'depends_on', strength: 1.0, explanation: 'Complementary pair' },
      { from: 2, to: 8, type: 'constrains', strength: 0.8, explanation: 'Boolean duality' },
      { from: 2, to: 15, type: 'implies', strength: 0.9, explanation: 'NAND encodes AND' },
      { from: 101, to: 201, type: 'enables', strength: 0.95, explanation: 'Causation requires temporal order' }
    ]
  }

  // Filter by container
  const primitivesByContainer = (container: string) => {
    return allPrimitives.value.filter(p => p.container === container)
  }

  // Get structures in container
  const structuresByContainer = (container: string) => {
    const prims = primitivesByContainer(container)
    const structures = new Map<string, number>()
    prims.forEach(p => {
      structures.set(p.structure, (structures.get(p.structure) || 0) + 1)
    })
    return Array.from(structures, ([name, count]) => ({
      id: name,
      name: name.replace(/_/g, ' ').toUpperCase(),
      primitives: count
    }))
  }

  // Filter by structure
  const primitivesByStructure = (structure: string) => {
    return allPrimitives.value.filter(p => p.structure === structure)
  }

  // Search primitives
  const search = (query: string) => {
    const q = query.toLowerCase()
    searchResults.value = allPrimitives.value.filter(p =>
      p.name.toLowerCase().includes(q) ||
      p.description.toLowerCase().includes(q) ||
      p.definition.toLowerCase().includes(q)
    )
    return searchResults.value
  }

  // Get related primitives
  const getRelated = (primitiveId: number) => {
    const primitive = allPrimitives.value.find(p => p.id === primitiveId)
    if (!primitive) return []
    return primitive.relatedPrimitives
      .map(id => allPrimitives.value.find(p => p.id === id))
      .filter(p => p !== undefined) as Primitive[]
  }

  // Get relationships for primitive
  const getRelationships = (primitiveId: number) => {
    return allRelationships.value.filter(
      r => r.from === primitiveId || r.to === primitiveId
    )
  }

  const stats = computed(() => ({
    total: allPrimitives.value.length,
    byContainer: {
      topological: primitivesByContainer('topological').length,
      boolean: primitivesByContainer('boolean').length,
      probability: primitivesByContainer('probability').length,
      interaction: primitivesByContainer('interaction').length
    },
    avgConfidence: allPrimitives.value.length > 0
      ? allPrimitives.value.reduce((sum, p) => sum + p.confidence, 0) / allPrimitives.value.length
      : 0
  }))

  return {
    allPrimitives,
    allRelationships,
    searchResults,
    loadPrimitives,
    primitivesByContainer,
    structuresByContainer,
    primitivesByStructure,
    search,
    getRelated,
    getRelationships,
    stats
  }
})
