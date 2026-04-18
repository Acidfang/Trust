// Civilization Visualization & Rendering Engine
// Handles rendering civilization models as interactive maps with metrics

class CivilizationRenderer {
  constructor() {
    this.container = document.getElementById('civilization-viewer') || document.body;
  }

  renderCivilization(civilizationData, comparisonData = null) {
    const html = `
      <div class="civilization-container">
        <div class="civilization-header">
          <h2>${civilizationData.title}</h2>
          <p>After ${civilizationData.timespan}</p>
        </div>
        
        <div class="civilization-map">
          ${this.renderCityMap(civilizationData)}
        </div>
        
        <div class="civilization-metrics">
          ${this.renderMetrics(civilizationData)}
        </div>
        
        <div class="civilization-features">
          <h3>What This Civilization Shows</h3>
          <ul>
            ${civilizationData.features.map(f => `<li>${f}</li>`).join('')}
          </ul>
        </div>
        
        ${comparisonData ? `
          <div class="civilization-comparison">
            <h3>Comparison: What Could Have Been</h3>
            <div class="comparison-side-by-side">
              <div class="comparison-left">
                <h4>Your Choice</h4>
                ${this.renderMetrics(civilizationData, 'compact')}
              </div>
              <div class="comparison-right">
                <h4>Alternate Choice</h4>
                ${this.renderMetrics(comparisonData, 'compact')}
              </div>
            </div>
          </div>
        ` : ''}
        
        <div class="civilization-reflection">
          <h3>What You've Learned</h3>
          <p>By choosing to ${civilizationData.choice_principle}, this is what emerges across a civilization of 1000 cities over 75 years.</p>
          <p>This is not theoretical. This is what your thinking produces at scale.</p>
        </div>
      </div>
    `;
    
    return html;
  }

  renderCityMap(civData) {
    const totalCities = civData.cities_healthy + civData.cities_struggling + (civData.cities_collapsed || 0);
    const healthyPercent = (civData.cities_healthy / totalCities * 100).toFixed(1);
    const strugglingPercent = (civData.cities_struggling / totalCities * 100).toFixed(1);
    const collapsedPercent = civData.cities_collapsed ? (civData.cities_collapsed / totalCities * 100).toFixed(1) : 0;
    
    // Create visual grid of cities
    let cityHtml = '';
    for (let i = 0; i < totalCities; i++) {
      let color = '';
      if (i < civData.cities_healthy) {
        color = 'city-healthy';
      } else if (i < civData.cities_healthy + civData.cities_struggling) {
        color = 'city-struggling';
      } else {
        color = 'city-collapsed';
      }
      cityHtml += `<div class="city ${color}" title="City ${i + 1}"></div>`;
    }
    
    return `
      <div class="city-map">
        <div class="city-grid">
          ${cityHtml}
        </div>
        <div class="city-legend">
          <div class="legend-item">
            <span class="legend-color city-healthy"></span>
            <span>${civData.cities_healthy} cities thriving (${healthyPercent}%)</span>
          </div>
          <div class="legend-item">
            <span class="legend-color city-struggling"></span>
            <span>${civData.cities_struggling} cities struggling (${strugglingPercent}%)</span>
          </div>
          ${civData.cities_collapsed ? `
            <div class="legend-item">
              <span class="legend-color city-collapsed"></span>
              <span>${civData.cities_collapsed} cities collapsed (${collapsedPercent}%)</span>
            </div>
          ` : ''}
        </div>
      </div>
    `;
  }

  renderMetrics(civData, mode = 'full') {
    const metrics = civData.metrics;
    
    if (mode === 'compact') {
      return `
        <div class="metrics-compact">
          ${Object.entries(metrics).map(([key, data]) => `
            <div class="metric-row">
              <span class="metric-label">${this.formatLabel(key)}:</span>
              <span class="metric-value">${data.value}</span>
            </div>
          `).join('')}
        </div>
      `;
    }
    
    // Full mode with detailed context
    return `
      <div class="metrics-full">
        <h3>Civilization Metrics (75-Year Outcome)</h3>
        <div class="metrics-grid">
          ${Object.entries(metrics).map(([key, data]) => `
            <div class="metric-card">
              <h4>${this.formatLabel(key)}</h4>
              <div class="metric-comparison">
                <div class="metric-current">
                  <span class="label">Outcome</span>
                  <span class="value">${data.value}</span>
                </div>
                <div class="metric-baseline">
                  <span class="label">Baseline</span>
                  <span class="value">${data.baseline}</span>
                </div>
              </div>
              <div class="metric-bar">
                ${this.renderComparisonBar(data.value, data.baseline, key)}
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  renderComparisonBar(current, baseline, metricKey) {
    // Parse values for comparison
    let currentNum = parseFloat(current);
    let baselineNum = parseFloat(baseline);
    
    // Handle percentage strings
    if (typeof current === 'string' && current.includes('%')) {
      currentNum = parseFloat(current);
    }
    if (typeof baseline === 'string' && baseline.includes('%')) {
      baselineNum = parseFloat(baseline);
    }
    
    // Determine direction (higher/lower is better depends on metric)
    const lowerIsBetter = ['infant_mortality', 'collapse_risk', 'cascade_failures', 'regime_changes'].includes(metricKey);
    
    let className = 'bar-neutral';
    if (lowerIsBetter) {
      if (currentNum < baselineNum) className = 'bar-improvement';
      else if (currentNum > baselineNum) className = 'bar-worse';
    } else {
      if (currentNum > baselineNum) className = 'bar-improvement';
      else if (currentNum < baselineNum) className = 'bar-worse';
    }
    
    return `<div class="comparison-bar ${className}"></div>`;
  }

  formatLabel(key) {
    return key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  }
}

// Initialize renderer on page load
document.addEventListener('DOMContentLoaded', function() {
  window.civRenderer = new CivilizationRenderer();
});
