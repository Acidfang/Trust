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
- **Purple connections**: Shared systems between frameworks

<div id="mapper-container" class="framework-mapper-container"></div>

## How to Read the Map

1. **Central Node (Red)**: Represents the universal law `dℹ/dt = -∇Φ` that all frameworks follow
2. **Framework Nodes**: Each colored circle represents a framework module
3. **Arrows**: Show relationships and connections between frameworks
4. **Click Nodes**: Click any framework node to view its detailed documentation

## Framework Connections

The frameworks connect through shared understanding of:

- **Quantum Systems**: Electrons, atoms, and their behavior
- **Classical Systems**: Molecules, cells, and biological structures  
- **Gravitational Systems**: Galaxies, binary systems, and cosmology
- **Temporal Dynamics**: How systems evolve forward and can be reversed in time

## Universal Systems Covered

{% assign all_systems = site.data.frameworks.frameworks | map: 'systems' | join: ', ' | split: ', ' | uniq %}

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

**Systems modeled**: Photons, electrons, atoms, molecules, cells, galaxies

**Key insight**: All these vastly different systems obey the same mathematical law.

### Cosmology Reversal Module

Applies time-reversal to the universal law by flipping the sign:

$$\frac{d\mathbf{i}}{dt} = +\nabla\Phi(\mathbf{x}, t) \text{ (reversed)}$$

This allows us to:

1. Start with observed galaxy positions
2. Reverse-integrate back in time
3. Find the initial diffusion point (origin)

**Verification**: Time-reversibility proven through ODE integration

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

<script>
  document.addEventListener('DOMContentLoaded', function() {
    // Load frameworks data and initialize mapper
    fetch('{{ "/assets/data/framework-map.json" | relative_url }}')
      .then(response => response.json())
      .then(data => {
        const container = document.getElementById('mapper-container');
        if (container && data.visualization) {
          initializeFrameworkMap(data.visualization);
        }
      })
      .catch(err => console.log('Framework map data not available (static version)', err));
  });
</script>

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
