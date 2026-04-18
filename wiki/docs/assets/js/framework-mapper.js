/**
 * Framework Visualization Renderer
 * 
 * Renders the framework map as an interactive network diagram.
 * Shows how all systems connect through the universal law.
 */

function initializeFrameworkMap(mapData) {
  if (!mapData || !mapData.nodes || !mapData.edges) {
    console.error('Invalid map data');
    return;
  }

  const container = document.getElementById('mapper-canvas');
  if (!container) return;

  // Set canvas size
  const width = container.offsetWidth || 800;
  const height = 500;

  // Create SVG
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('width', width);
  svg.setAttribute('height', height);
  svg.setAttribute('class', 'framework-diagram');
  svg.setAttribute('style', 'border: 1px solid #ddd; border-radius: 4px; background: #fafafa;');

  // Define arrowhead marker
  const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
  const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
  marker.setAttribute('id', 'arrowhead');
  marker.setAttribute('markerWidth', '10');
  marker.setAttribute('markerHeight', '10');
  marker.setAttribute('refX', '9');
  marker.setAttribute('refY', '3');
  marker.setAttribute('orient', 'auto');
  const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
  polygon.setAttribute('points', '0 0, 10 3, 0 6');
  polygon.setAttribute('fill', '#999');
  marker.appendChild(polygon);
  defs.appendChild(marker);
  svg.appendChild(defs);

  // Calculate positions using simple force-directed algorithm
  const positions = calculatePositions(mapData.nodes, mapData.edges, width, height);

  // Draw edges first (so they appear behind nodes)
  const g_edges = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  g_edges.setAttribute('class', 'edges');
  
  for (const edge of mapData.edges) {
    const x1 = positions[edge.source].x;
    const y1 = positions[edge.source].y;
    const x2 = positions[edge.target].x;
    const y2 = positions[edge.target].y;

    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', x1);
    line.setAttribute('y1', y1);
    line.setAttribute('x2', x2);
    line.setAttribute('y2', y2);
    line.setAttribute('stroke', edge.isUniversal ? '#ff6b6b' : '#999');
    line.setAttribute('stroke-width', edge.isUniversal ? '2' : '1');
    line.setAttribute('opacity', '0.6');
    line.setAttribute('marker-end', 'url(#arrowhead)');
    
    if (edge.label) {
      line.setAttribute('title', edge.label);
    }
    
    g_edges.appendChild(line);
  }
  svg.appendChild(g_edges);

  // Draw nodes
  const g_nodes = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  g_nodes.setAttribute('class', 'nodes');

  for (const node of mapData.nodes) {
    const x = positions[node.id].x;
    const y = positions[node.id].y;
    const radius = node.isCenter ? 30 : 20;

    // Background circle
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', x);
    circle.setAttribute('cy', y);
    circle.setAttribute('r', radius);
    circle.setAttribute('fill', node.color);
    circle.setAttribute('opacity', '0.8');
    circle.setAttribute('class', 'framework-node');
    
    if (node.url) {
      circle.setAttribute('cursor', 'pointer');
      circle.setAttribute('title', `Click to view: ${node.label}`);
      circle.onclick = () => window.location.href = node.url;
    }
    
    g_nodes.appendChild(circle);

    // Label
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', x);
    text.setAttribute('y', y + 5);
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('font-size', node.isCenter ? '11px' : '10px');
    text.setAttribute('font-weight', node.isCenter ? 'bold' : 'normal');
    text.setAttribute('fill', 'white');
    text.setAttribute('pointer-events', 'none');
    text.textContent = node.isCenter ? 'Universal Law' : node.label.split(' ')[0];
    
    g_nodes.appendChild(text);

    // Systems badges
    if (node.systems && node.systems.length > 0 && !node.isCenter) {
      const systemText = node.systems.slice(0, 2).join(', ');
      const subtitle = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      subtitle.setAttribute('x', x);
      subtitle.setAttribute('y', y + 25);
      subtitle.setAttribute('text-anchor', 'middle');
      subtitle.setAttribute('font-size', '7px');
      subtitle.setAttribute('fill', '#666');
      subtitle.setAttribute('pointer-events', 'none');
      subtitle.textContent = systemText;
      g_nodes.appendChild(subtitle);
    }
  }
  svg.appendChild(g_nodes);

  container.appendChild(svg);

  // Add interaction info
  const info = document.createElement('p');
  info.setAttribute('class', 'mapper-info');
  info.style.fontSize = '0.85rem';
  info.style.color = '#666';
  info.style.marginTop = '1rem';
  info.style.textAlign = 'center';
  info.innerHTML = '💡 Click on any node to view framework details. All frameworks share the same universal evolution law.';
  container.appendChild(info);
}

/**
 * Simple force-directed layout
 */
function calculatePositions(nodes, edges, width, height) {
  const positions = {};
  const centerNode = nodes.find(n => n.isCenter);
  
  // Place center node in middle
  if (centerNode) {
    positions[centerNode.id] = { x: width / 2, y: height / 2 };
  }

  // Place other nodes in circle around center
  const otherNodes = nodes.filter(n => !n.isCenter);
  const radius = Math.min(width, height) / 3;
  const angleStep = (2 * Math.PI) / Math.max(otherNodes.length, 1);

  otherNodes.forEach((node, i) => {
    const angle = i * angleStep;
    positions[node.id] = {
      x: width / 2 + radius * Math.cos(angle),
      y: height / 2 + radius * Math.sin(angle)
    };
  });

  return positions;
}

// Legacy support - try to initialize if data is already available
if (typeof window !== 'undefined' && window.frameworkMapData) {
  document.addEventListener('DOMContentLoaded', () => {
    initializeFrameworkMap(window.frameworkMapData);
  });
}
