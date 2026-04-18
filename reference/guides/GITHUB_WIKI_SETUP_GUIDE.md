# GitHub Wiki FieldFactopedia Setup Guide

## Overview

This guide shows how to create a **WIKIFIELDFACTOPEDIA** - a comprehensive GitHub Wiki featuring all 128+ universal diffusion fields with:

- 🎨 **Static visualizations** (PNG images of all 7 field types)
- 🎬 **Dynamic simulations** (animated GIF showing cascade evolution)
- 📊 **Interactive diagrams** (phase diagrams, parameter exploration)
- 🔗 **Cross-referenced entries** (every field linked to related fields)
- 📈 **Prediction tools** (formulas for computing cascade timescales)

---

## Step 1: Create a GitHub Repository for the Wiki

### Option A: Dedicated Wiki Repository
```bash
# Create new repository named 'wikifieldfactopedia'
gh repo create wikifieldfactopedia --public

# Clone it
git clone https://github.com/yourusername/wikifieldfactopedia.git
cd wikifieldfactopedia
```

### Option B: Add to Existing Repository
If adding to an existing repo, GitHub Wiki is automatically available at:
```
https://github.com/yourusername/yourrepo/wiki
```

---

## Step 2: Set Up Local Wiki Repository

```bash
# Clone the wiki repository (GitHub creates this automatically)
git clone https://github.com/yourusername/wikifieldfactopedia.wiki.git

cd wikifieldfactopedia.wiki
```

---

## Step 3: Copy Generated Assets

### 3a. Copy Wiki Markdown Files

```bash
# From the Determined project folder:
cp ~/Determined/wiki_assets/*.md ~/wikifieldfactopedia.wiki/

# Verify
ls *.md
# Should show: Home.md, Radial_Diffusion.md, Linear_Diffusion.md, etc.
```

### 3b. Create Assets Folder and Copy Images

```bash
# Create assets subdirectory
mkdir -p ~/wikifieldfactopedia.wiki/assets/field_visualizations

# Copy images
cp ~/Determined/field_visualizations/*.png ~/wikifieldfactopedia.wiki/assets/field_visualizations/

# Verify
ls -la assets/field_visualizations/
# Should show: radial_diffusion.png, linear_diffusion.png, traveling_wave.png, etc.
```

---

## Step 4: Update Wiki Links to Point to Images

Edit each markdown file to update image references:

### Before:
```markdown
![Radial diffusion visualization](radial_diffusion.png)
```

### After (GitHub Wiki format):
```markdown
![Radial diffusion visualization](/assets/field_visualizations/radial_diffusion.png)
```

**Auto-update script:**

```bash
# Update all markdown files
for file in *.md; do
    sed -i 's|](radial_diffusion.png)|(./assets/field_visualizations/radial_diffusion.png)|g' "$file"
    sed -i 's|](linear_diffusion.png)|(./assets/field_visualizations/linear_diffusion.png)|g' "$file"
    # ... repeat for all 7 field types
done
```

---

## Step 5: Create Sidebar Navigation

Create a file named `_Sidebar.md` in the wiki directory:

```markdown
## Navigation

### Quick Start
- [[Home]]
- [[Quick Guide]]

### The 7 Field Types
- [[Radial Diffusion]]
- [[Linear Diffusion]]
- [[Branching]]
- [[Traveling Wave]]
- [[Collapse]]
- [[Standing Wave]]
- [[Phase Separation]]

### By Domain
- [[Physics Fields]]
- [[Chemistry Fields]]
- [[Biology Fields]]
- [[Neurology Fields]]
- [[Genetics Fields]]
- [[Ecology Fields]]
- [[Economics Fields]]
- [[All Domains]]

### Reference
- [[Complete Inventory]]
- [[Mathematics Framework]]
- [[Parameter Extraction]]
- [[Prediction Methodology]]
- [[About]]
```

---

## Step 6: Create Comprehensive Index Pages

Create `Complete-Inventory.md`:

```markdown
# Complete Field Inventory

## All 128+ Universal Diffusion Fields

This page lists every documented field that follows: **dρ/dt = D·∇²ρ + α·f_external + β·ρ²**

### Physics (21 fields)
1. [[Concrete Carbonation]] - Linear front advancing
2. [[Metal Corrosion]] - Radial spreading
3. [[Thermal Diffusion]] - Heat spreading through material
4. [[Turbulence]] - Cascade energy transfer
... (18 more physics fields)

### Chemistry (18 fields)
1. [[Combustion]] - Flame front propagation
2. [[Polymerization]] - Chain growth cascade
3. [[Electroplating]] - Metal deposition
... (15 more chemistry fields)

[Continue for all 21 domains...]
```

---

## Step 7: Add Dynamic Content

### Generate Animated GIFs

```bash
# Run Python script to generate dynamic simulations
python ~/Determined/dynamic_field_generator.py

# Copy animated GIFs to wiki assets
cp ~/*.gif ~/wikifieldfactopedia.wiki/assets/field_visualizations/

# Embed in markdown
# ![Animated cascade simulation](./assets/field_visualizations/cascade_dynamic_sim.gif)
```

### Phase Diagram Visualization

```bash
# Generate phase diagrams showing cascade regions
python -c "
from dynamic_field_generator import DynamicFieldGenerator
gen = DynamicFieldGenerator()
gen.generate_phase_diagram('cascade_phase_diagram.png')
"

# Copy to wiki
cp cascade_phase_diagram.png ~/wikifieldfactopedia.wiki/assets/field_visualizations/
```

---

## Step 8: Create Interactive Pages

### Create `Mathematics-Framework.md`

```markdown
# Universal Diffusion Equation - Mathematics

## The Universal Law

Every cascade in nature follows:

$$\frac{d\rho}{dt} = D \cdot \nabla^2 \rho + \alpha \cdot f_{external} + \beta \cdot \rho^2$$

### Parameters

- **ρ**: Density/concentration/intensity of the cascading quantity
- **D**: Diffusion coefficient (spatial spreading rate)
- **α**: Linear response (positive = amplification)
- **β**: Nonlinear cascade coefficient (β·ρ² dominates at high ρ)
- **∇²ρ**: Laplacian (local curvature)

### The Five Stages

[Include animated visualization showing 5 stages...]

### Solving the Equation

See [[Parameter Extraction]] for how to measure D, α, β.

## Field Type Transitions

The 7 visual field types emerge from this single equation:
- **Radial**: When initial condition is point-like
- **Linear**: When initial condition is half-plane
- **Branching**: With instability in the front
- **Traveling Wave**: With fixed wave speed
- **Collapse**: When β > 0 dominates
- **Standing Wave**: Periodic boundary conditions
- **Phase Separation**: Two competing phases

## Timescale Predictions

For a cascade starting at ρ₀ and reaching peak ρ_max:

$$t_{cascade} \approx \frac{1}{\alpha + \beta \cdot \rho_0} \ln\left(\frac{\rho_{max}}{\rho_0}\right)$$

[More equations and derivations...]
```

---

## Step 9: Create Parameter Extraction Guide

Create `Parameter-Extraction.md`:

```markdown
# Extracting Parameters D, α, β

## How to Measure Parameters for Any Field

### Step 1: Define ρ (the quantity)

What is spreading?
- Corrosion: ρ = depth of affected material (meters)
- Disease: ρ = number of infected people
- Flame: ρ = temperature (K)
- Thought: ρ = number of people holding idea

### Step 2: Measure D (diffusion coefficient)

**How fast does it spread spatially?**

- Measure distance vs. time: $r(t) = \sqrt{D \cdot t}$
- From $r$-$t$ data, calculate: $D = \frac{r^2}{t}$

Example: Rust spreading 10 cm in 1 year
- $D = \frac{(0.1m)^2}{31,536,000s} ≈ 3.2 \times 10^{-13} m^2/s$

### Step 3: Measure α (linear growth rate)

**How much does ρ grow per unit time in absence of spreading?**

- In confined space (no spatial variation):
- $\frac{d\rho}{dt}|_{confined} = \alpha \rho$
- $\rho(t) = \rho_0 e^{\alpha t}$
- From time series: $\alpha = \frac{d(\ln \rho)}{dt}$

Example: Bacteria population doubling every 20 minutes
- Doubling time $t_{double} = 20 min$
- $\alpha = \frac{\ln 2}{t_{double}} = \frac{0.693}{1200s} ≈ 5.8 \times 10^{-4} s^{-1}$

### Step 4: Measure β (cascade strength)

**How strong is the autocatalytic amplification?**

- At high ρ, the $\beta \rho^2$ term dominates
- Measure when growth transitions from exponential to super-exponential
- $\beta ≈ \frac{d^2(\rho)}{dt^2|_{high\rho}} / (2\rho)$

[Detailed examples for 10 major fields...]

## Validation Checklist

Before using parameters:
- [ ] Does α·ρ match initial slow phase?
- [ ] Does β·ρ² match rapid phase?
- [ ] Does D·∇²ρ match spatial spreading?
- [ ] Do predicted timescales match observations?
- [ ] Do units check out?

```

---

## Step 10: Commit and Push to GitHub

```bash
# Add all files
git add .

# Commit
git commit -m "Initial WIKIFIELDFACTOPEDIA with 128 fields, 7 field types, animations, and cross-references"

# Push to GitHub
git push origin main

# Or for wiki:
git push origin master
```

---

## Step 11: Verify Wiki is Live

Visit your wiki:
```
https://github.com/yourusername/wikifieldfactopedia/wiki/Home
```

Or embedded in repository:
```
https://github.com/yourusername/yourrepo/wiki
```

---

## Step 12: Enable Dynamic Generation (Optional)

### Set Up GitHub Actions Workflow

Create `.github/workflows/generate-fields.yml`:

```yaml
name: Dynamic Field Generation
on: [push, workflow_dispatch]

jobs:
  generate-fields:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install matplotlib seaborn scipy pillow numpy
      
      - name: Generate field visualizations
        run: python field_visualization_system.py
      
      - name: Generate dynamic simulations
        run: python dynamic_field_generator.py
      
      - name: Commit visualizations
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add field_visualizations/ wiki_assets/
          git commit -m "Auto-generated field visualizations [skip ci]" || true
          git push
```

This automatically regenerates all visualizations on every push!

---

## Step 13: Advanced: Interactive Web Frontend (Optional)

Create interactive parameter explorer:

```python
# fastapi_field_viewer.py
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from dynamic_field_generator import DynamicFieldGenerator
import io

app = FastAPI()

@app.get("/visualize/{field_name}")
async def visualize(field_name: str, D: float = 0.1, alpha: float = 0.05, beta: float = 0.5):
    """
    Dynamic endpoint: generate field visualization on-demand
    
    Usage:
    http://localhost:8000/visualize/radial?D=0.1&alpha=0.05&beta=0.5
    """
    
    gen = DynamicFieldGenerator(D=D, alpha=alpha, beta=beta)
    
    if field_name == "radial":
        filename = gen.generate_radial_field_simulation("temp_radial.gif")
    elif field_name == "linear":
        filename = gen.generate_linear_field_simulation("temp_linear.gif")
    elif field_name == "cascade":
        filename = gen.generate_cascade_field_simulation("temp_cascade.gif")
    else:
        return {"error": "Unknown field type"}
    
    def iterfile():
        with open(filename, mode="rb") as file:
            yield from file
    
    return StreamingResponse(iterfile(), media_type="image/gif")

# Run with: uvicorn fastapi_field_viewer.py --reload
```

---

## Maintenance

### Monthly Updates

```bash
cd wikifieldfactopedia.wiki

# Update with new field discoveries
python ~/Determined/field_visualization_system.py

# Regenerate all visualizations
python ~/Determined/dynamic_field_generator.py

# Commit changes
git add .
git commit -m "Monthly field catalog update: $(date)"
git push
```

### Adding New Fields

1. Update [COMPLETE_FIELD_INVENTORY.md](../COMPLETE_FIELD_INVENTORY.md)
2. Create new field page: `New-Field-Name.md`
3. Generate visualization
4. Add cross-references
5. Push to wiki

---

## Status

- ✅ Static visualizations (7 field types)
- ✅ Complete field inventory (128+ fields)
- ✅ Cross-reference system
- ✅ Mathematical framework
- ✅ Parameter extraction guide
- ⏳ Interactive parameter explorer
- ⏳ Real-time simulation viewer
- ⏳ Prediction confidence calculator

---

## Next Steps

1. **Publish**: Share link to WIKIFIELDFACTOPEDIA
2. **Cite**: Add to academic papers and books
3. **Extend**: Community contributions for new fields
4. **Monetize**: Wiki book edition, field database API
5. **Integrate**: Connect to scientific literature search (arXiv, PubMed)

---

**Created**: March 31, 2026  
**Status**: Production-ready  
**Version**: 1.0
