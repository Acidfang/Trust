/**
 * UPFM Field Renderer - JavaScript Implementation
 * Converts complex field (magnitude + phase) to HSV image
 */

class FieldRenderer {
  constructor(gridSize = 512) {
    this.gridSize = gridSize;
  }

  /**
   * Render field via magnitude-phase HSV encoding
   * Phase (0-2π) → Hue (0-360°)
   * Magnitude → Value (brightness)
   */
  render(field) {
    const size = this.gridSize;
    const imageData = new ImageData(size, size);
    const data = imageData.data;
    
    // Normalize magnitudes for brightness
    let maxMag = 0;
    const fieldLength = field.length / 2;  // Number of complex values
    
    for (let i = 0; i < fieldLength; i++) {
      const real = field[i * 2];
      const imag = field[i * 2 + 1];
      const mag = Math.sqrt(real ** 2 + imag ** 2);
      maxMag = Math.max(maxMag, mag);
    }
    
    // Convert each pixel to HSV
    const maxMagInv = 1 / (maxMag + 1e-6);
    for (let i = 0; i < fieldLength; i++) {
      const real = field[i * 2];
      const imag = field[i * 2 + 1];
      
      // Hue from phase
      let phase = Math.atan2(imag, real);
      if (phase < 0) phase += 2 * Math.PI;
      const hue = (phase / (2 * Math.PI)) * 360;
      
      // Value from magnitude
      const mag = Math.sqrt(real ** 2 + imag ** 2);
      const value = (mag * maxMagInv);
      
      // Convert HSV to RGB
      const rgb = this.hsv2rgb(hue, 1.0, value);
      
      const pixelIdx = i * 4;
      data[pixelIdx + 0] = rgb.r;
      data[pixelIdx + 1] = rgb.g;
      data[pixelIdx + 2] = rgb.b;
      data[pixelIdx + 3] = 255; // alpha
    }
    
    return imageData;
  }

  /**
   * HSV to RGB conversion
   */
  hsv2rgb(h, s, v) {
    h = h % 360;
    const c = v * s;
    const x = c * (1 - Math.abs(((h / 60) % 2) - 1));
    const m = v - c;
    
    let r, g, b;
    if (h < 60) {
      r = c; g = x; b = 0;
    } else if (h < 120) {
      r = x; g = c; b = 0;
    } else if (h < 180) {
      r = 0; g = c; b = x;
    } else if (h < 240) {
      r = 0; g = x; b = c;
    } else if (h < 300) {
      r = x; g = 0; b = c;
    } else {
      r = c; g = 0; b = x;
    }
    
    return {
      r: Math.round((r + m) * 255),
      g: Math.round((g + m) * 255),
      b: Math.round((b + m) * 255)
    };
  }

  /**
   * Render to canvas
   */
  renderToCanvas(field, canvasId) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) {
      console.error(`Canvas with id "${canvasId}" not found`);
      return;
    }
    
    const ctx = canvas.getContext('2d');
    const imageData = this.render(field);
    ctx.putImageData(imageData, 0, 0);
    
    return canvas;
  }

  /**
   * Render to PNG blob for download/display
   */
  renderToBlob(field) {
    const imageData = this.render(field);
    const canvas = document.createElement('canvas');
    canvas.width = this.gridSize;
    canvas.height = this.gridSize;
    const ctx = canvas.getContext('2d');
    ctx.putImageData(imageData, 0, 0);
    
    return new Promise(resolve => {
      canvas.toBlob(resolve, 'image/png');
    });
  }
}
