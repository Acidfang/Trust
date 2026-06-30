/**
 * Framework Visualization Renderer
 * 
 * Renders the framework map as an interactive network diagram.
 * Shows how all systems connect through the universal law.
 * 
 * TIER 1 (Input): Validates mapData structure
 * TIER 2 (Compute): Calculates node positions
 * TIER 3 (Output): Renders SVG visualization
 * TIER 4 (Verify): Validates rendered output and interactions
 */

function initializeFrameworkMap(mapData) {
  // TIER 1: Validate input data structure
  if (!mapData || !mapData.nodes || !mapData.edges) {
    console.error('[TIER 1 FAIL] Invalid map data structure');
    return;
  }
  
  if (!Array.isArray(mapData.nodes) || !Array.isArray(mapData.edges)) {
    console.error('[TIER 1 FAIL] Nodes and edges must be arrays');
    return;
  }
  
  for (const node of mapData.nodes) {
    if (!node.id || !node.label) {
      console.error('[TIER 1 FAIL] Node missing id or label:', node);
      return;
    }
  }
  
  for (const edge of mapData.edges) {
    if (!edge.source || !edge.target) {
      console.error('[TIER 1 FAIL] Edge missing source or target:', edge);
      return;
    }
  }
  
  console.log('[TIER 1 OK] Input data structure validated');

  // TIER 2: Calculate positions
  const container = document.getElementById('mapper-canvas');
  if (!container) {
    console.error('[TIER 2 FAIL] mapper-canvas container not found');
    return;
  }

  const width = container.offsetWidth || 800;
  const height = 500;
  
  const positions = calculatePositions(mapData.nodes, mapData.edges, width, height);
  console.log('[TIER 2 OK] Positions calculated for ' + mapData.nodes.length + ' nodes');

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

  console.log('[TIER 3] Starting SVG rendering...');

  // Draw edges first (so they appear behind nodes)
  const g_edges = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  g_edges.setAttribute('class', 'edges');
  g_edges.setAttribute('id', 'edges-group');
  
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
    line.setAttribute('class', 'edge-line');
    
    // Add hover effect data
    if (edge.label) {
      line.setAttribute('data-systems', edge.label);
      line.setAttribute('title', 'Shared: ' + edge.label);
    }
    
    // Add hover interactivity
    line.addEventListener('mouseenter', function() {
      this.setAttribute('opacity', '1');
      this.setAttribute('stroke-width', edge.isUniversal ? '3' : '2');
      if (edge.label) {
        showEdgeLabel(x1, y1, x2, y2, edge.label);
      }
    });
    
    line.addEventListener('mouseleave', function() {
      this.setAttribute('opacity', '0.6');
      this.setAttribute('stroke-width', edge.isUniversal ? '2' : '1');
      hideEdgeLabel();
    });
    
    g_edges.appendChild(line);
  }
  svg.appendChild(g_edges);
  
  console.log('[TIER 3] Rendered ' + mapData.edges.length + ' edges');

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
    text.textContent = node.isCenter ? 'Universal Law' : truncateLabel(node.label, 12);
    
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

/**
 * TIER 4: Verify rendered SVG visualization
 */
function verifyRenderedVisualization(svg, mapData) {
  console.log('[TIER 4] Verifying rendered visualization...');
  let verified = true;
  
  // Check SVG exists and has content
  if (!svg || !mapData) {
    console.error('[TIER 4 FAIL] SVG or mapData missing');
    return false;
  }
  
  // Check all nodes are rendered
  const renderedNodes = svg.querySelectorAll('circle.framework-node');
  if (renderedNodes.length !== mapData.nodes.length) {
    console.warn('[TIER 4 WARN] Expected ' + mapData.nodes.length + ' nodes, found ' + renderedNodes.length);
  }
  
  // Check all edges are rendered
  const renderedEdges = svg.querySelectorAll('line.edge-line');
  if (renderedEdges.length !== mapData.edges.length) {
    console.warn('[TIER 4 WARN] Expected ' + mapData.edges.length + ' edges, found ' + renderedEdges.length);
  }
  
  // Check nodes have labels
  const labels = svg.querySelectorAll('text');
  if (labels.length < mapData.nodes.length) {
    console.error('[TIER 4 FAIL] Not all nodes have labels');
    verified = false;
  }
  
  // Check SVG has reasonable dimensions
  const width = svg.getAttribute('width');
  const height = svg.getAttribute('height');
  if (!width || !height || parseInt(width) < 100 || parseInt(height) < 100) {
    console.error('[TIER 4 FAIL] SVG has invalid dimensions');
    verified = false;
  }
  
  if (verified) {
    console.log('[TIER 4 OK] All rendered elements verified');
  } else {
    console.error('[TIER 4 FAIL] Verification found issues');
  }
  
  return verified;
}

/**
 * Helper: Show edge label on hover
 */
function showEdgeLabel(x1, y1, x2, y2, label) {
  if (document.getElementById('edge-label-tooltip')) {
    hideEdgeLabel();
  }
  
  const tooltip = document.createElement('div');
  tooltip.id = 'edge-label-tooltip';
  tooltip.style.position = 'fixed';
  tooltip.style.background = '#333';
  tooltip.style.color = '#fff';
  tooltip.style.padding = '4px 8px';
  tooltip.style.borderRadius = '3px';
  tooltip.style.fontSize = '0.75rem';
  tooltip.style.pointerEvents = 'none';
  tooltip.style.zIndex = '1000';
  tooltip.style.whiteSpace = 'nowrap';
  tooltip.textContent = 'Shared systems: ' + label;
  
  const midX = (x1 + x2) / 2;
  const midY = (y1 + y2) / 2;
  tooltip.style.left = (midX + 10) + 'px';
  tooltip.style.top = (midY - 20) + 'px';
  
  document.body.appendChild(tooltip);
}

/**
 * Helper: Hide edge label tooltip
 */
function hideEdgeLabel() {
  const tooltip = document.getElementById('edge-label-tooltip');
  if (tooltip) {
    tooltip.remove();
  }
}

/**
 * Helper: Truncate long labels for space
 */
function truncateLabel(label, maxLen) {
  if (!label) return '';
  if (label.length <= maxLen) return label;
  return label.substring(0, maxLen - 3) + '...';
}
