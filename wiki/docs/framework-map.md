---
layout: page
title: Framework Visualization Map
permalink: /framework-map/
description: Interactive visualization of how all frameworks connect through the universal physics law
---

# Universal Framework Visualization Map

All frameworks in this project are unified under a single mathematical principle:

$$\frac{d\mathbf{i}}{dt} = -\nabla\Phi(\mathbf{x}, t)$$

This law describes how any coherent system evolves. The frameworks below show different applications and domains where this universal law applies.

## Interactive Framework Map

The visualization below shows:
- **Red central node**: The universal evolution law itself
- **Green/Blue nodes**: Individual frameworks  
- **Red connections**: Links to the universal law (all frameworks obey it)
- **Gray connections**: Shared systems between frameworks

<div id="mapper-container" class="framework-mapper-container">
  <div id="mapper-canvas" style="width: 100%; min-height: 500px;"></div>
</div>

<script>
  // Load framework map data and render
  fetch('/assets/data/framework-map.json')
    .then(response => response.json())
    .then(data => {
      // Extract visualization nodes and edges
      const visualization = data.visualization || { nodes: data.nodes || [], edges: data.edges || [] };
      if (window.initializeFrameworkMap) {
        window.initializeFrameworkMap(visualization);
      } else {
        console.error('Framework mapper not loaded');
      }
    })
    .catch(err => console.error('Failed to load framework map:', err));
</script>
## Universal Systems Covered

Based on the frameworks in this project, the visualization includes these system categories:

- **Physics**: Photons, electrons, electromagnetic waves
- **Chemistry**: Atoms, molecules, chemical bonds
- **Biology**: Cells, organisms, life systems
- **Cosmology**: Galaxies, gravitational systems, the universe  
- **Temporal**: Time-reversible systems, origin finding

## The Frameworks

### Universal Physics Engine

The foundational framework that implements the universal law. It can model any coherent physical system by:

1. Defining a potential energy landscape Φ(x)
2. Computing the gradient ∇Φ
3. Integrating the evolution equation

**Systems modeled**: Photons, Electrons, Atoms, Molecules, Cells, Galaxies

All physics models are available in the GitHub repository under `/framework/universal-physics/`.

### Cosmology Reversal Module

Uses the universal physics foundation's single evolution law to time-reverse galaxy trajectories and find the origin point where all matter originated.

**Systems modeled**: Cosmology, Temporal dynamics, Gravitational systems, Reversal mechanics

Time-reversal verification tool is available in the GitHub repository under `/framework/cosmology-reversal/`.

## How to Read the Map

1. **Central Node (Red)**: Represents the universal law `dℹ/dt = -∇Φ` that all frameworks follow
2. **Framework Nodes**: Each colored circle represents a framework module
3. **Arrows**: Show relationships and connections between frameworks
4. **Click Nodes**: Click any framework node to view its detailed README
5. **Hover Edges**: Hover over connections to see which systems are shared

## Framework Connections

The frameworks connect through shared understanding of:

- **Quantum Systems**: Electrons, atoms, and their behavior
- **Classical Systems**: Molecules, cells, and biological structures
- **Gravitational Systems**: Galaxies, binary systems, and cosmology
- **Temporal Dynamics**: How systems evolve forward and can be reversed in time

## Scale Coverage

These frameworks model physical systems across an enormous range:

- **Smallest**: Photons (~10⁻¹⁰ meters)
- **Intermediate**: Atoms (~10⁻⁹ m), Molecules (~10⁻⁹ m), Cells (~10⁻⁵ m)
- **Largest**: Galaxies (~10¹⁹ m), Universe (~10²⁶ m)

- **Smallest**: Photons (~10⁻¹⁰ meters)
- **Intermediate**: Atoms (~10⁻⁹ m), Molecules (~10⁻⁹ m), Cells (~10⁻⁵ m)
- **Largest**: Galaxies (~10¹⁹ m), Universe (~10²⁶ m)

## The Unification Principle

What makes this remarkable: A single equation describes phenomena across 40+ orders of magnitude in scale:

- Electron orbit: ~10⁻¹⁰ meters
- Protein folding: ~10⁻⁹ meters
- Virus: ~10⁻⁸ meters
- Cell: ~10⁻⁵ meters
- Human: ~1 meter
- Earth: ~10⁷ meters
- Galaxy: ~10²¹ meters

Yet the same law `dℹ/dt = -∇Φ` applies to all of them.

---

<script src="{{ '/assets/js/framework-mapper.js' | relative_url }}"></script>

<style>
.framework-mapper-container {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  margin: 2rem 0;
}

.framework-diagram {
  max-width: 100%;
  height: auto;
}

.mapper-info {
  text-align: center;
  color: #666;
  font-size: 0.9rem;
  margin-top: 1rem;
}
</style>
</style>
