# WikiFieldFactopedia - GitHub Setup Guide

**Your GitHub Account:** Acidfang  
**Repository Name:** WikiFieldFactopedia  
**Visibility:** Public  
**Date:** March 31, 2026

---

## 🚀 QUICK START: Create the Repository on GitHub.com

### Step 1: Go to GitHub and Create a New Repository

1. Visit: **https://github.com/new**
2. Fill in the form:
   - **Repository name:** `WikiFieldFactopedia`
   - **Description:** "Universal Field Genealogy: Electrons → Atoms → Molecules → Life"
   - **Public:** ✓ Select this
   - **Initialize with:** Check "Add a README file"
   - Click **Create repository**

3. After creation, you'll see:
   - Repository URL: `https://github.com/Acidfang/WikiFieldFactopedia`
   - Clone URL: `git@github.com:Acidfang/WikiFieldFactopedia.git`

---

## 📁 Step 2: Clone the Repository Locally

In PowerShell, run:

```powershell
cd C:\
git clone https://github.com/Acidfang/WikiFieldFactopedia.git
cd WikiFieldFactopedia
```

---

## 📊 Step 3: Add Visualization Files

Copy all generated visualization files to your local repo:

```powershell
# Copy PNG and GIF visualizations
Copy-Item "C:\Determined\electron_tree_static.png" ".\electron_tree_static.png"
Copy-Item "C:\Determined\electron_element_tree.png" ".\electron_element_tree.png"
Copy-Item "C:\Determined\orbital_filling_order.png" ".\orbital_filling_order.png"
Copy-Item "C:\Determined\electron_growth_animation.gif" ".\electron_growth_animation.gif"
Copy-Item "C:\Determined\composition_hierarchy_tree.png" ".\composition_hierarchy_tree.png"
Copy-Item "C:\Determined\branching_genealogy.png" ".\branching_genealogy.png"
Copy-Item "C:\Determined\binary_genealogy_tree.png" ".\binary_genealogy_tree.png"
```

---

## 📝 Step 4: Create Wiki Structure

Create wiki markdown files in root directory:

### File 1: `README.md` (Main landing page)

```markdown
# WikiFieldFactopedia

Universal Field Genealogy: How electrons evolve into complexity.

## Quick Navigation

- 📚 [Full Wiki](./wiki/)
- 🧬 [Electron Genealogy](./wiki/01-Electron-Genealogy.md)
- ⚛️ [Periodic Table Evolution](./wiki/02-Element-Evolution.md)
- 🌍 [Composition Hierarchy](./wiki/03-Composition-Hierarchy.md)
- 🔢 [Binary Genealogy](./wiki/04-Binary-Genealogy.md)
- 🎬 [Animations](./wiki/05-Animations.md)

## Key Visualizations

### Electron Orbital Genealogy
![Electron Tree](./electron_tree_static.png)

### Compositional Hierarchy
![Composition Tree](./composition_hierarchy_tree.png)

### Binary Genealogy
![Binary Tree](./binary_genealogy_tree.png)

## The Universal Law

```
dρ/dt = D·∇²ρ + α·f_external + β·ρ²
```

Every field evolves according to this diffusion equation. From electrons to atoms to molecules to life—one law governs all composition.

---

## Learn More

- Full documentation in the [Wiki section](#wiki-structure)
- Source code: [`electron_tree_generator.py`](./electron_tree_generator.py)
- All visualizations are generated dynamically
```

---

## 🌳 Step 5: Enable GitHub Wiki

1. Go to your repository on GitHub
2. Click **Settings** (top menu)
3. Under "Features," check **☑️ Wikis**
4. Click **Save**

---

## 📖 Step 6: Create Wiki Pages (On GitHub)

Once wiki is enabled:

1. Click **Wiki** tab (next to Code)
2. Click **Create the first page**

Create these 5 pages:

### Page 1: `Home`
```markdown
# WikiFieldFactopedia

**Universal taxonomy of fields and their genealogy**

## Five Levels of Understanding

1. **Electron Genealogy** - How electrons fill orbitals
2. **Element Evolution** - Periodic table emergence
3. **Composition Hierarchy** - Containers all the way down
4. **Binary Genealogy** - How composition creates binary signatures
5. **Animations** - Watch it happen in real-time

[View all visualizations](../../../)
```

### Page 2: `Electron-Genealogy`
```markdown
# Electron Genealogy

How electrons fill orbitals according to the Aufbau Principle.

![Orbital Tree](../electron_tree_static.png)

## The Aufbau Principle

Electrons fill orbitals in this order:
1s → 2s → 2p → 3s → 3p → 4s → 3d → 4p → ...

Each orbital is a container for electrons:
- **s-orbital:** 2 electrons max
- **p-orbital:** 6 electrons max
- **d-orbital:** 10 electrons max
- **f-orbital:** 14 electrons max

## Visualization

See `electron_tree_static.png` for the complete filling order.
```

### Page 3: `Element-Evolution`
```markdown
# Element Evolution

How electron configurations evolve across the periodic table.

![Element Tree](../electron_element_tree.png)

## From Hydrogen to Krypton

Each element builds on the previous one:
- **H (Z=1):** 1 electron → 1s¹
- **He (Z=2):** 2 electrons → 1s²
- **Li (Z=3):** 3 electrons → 1s² 2s¹
- ...continuing through all 118 elements

The periodic table is a record of **compositional genealogy**.
```

### Page 4: `Composition-Hierarchy`
```markdown
# Composition Hierarchy

Each level is a container for the previous level.

![Composition Tree](../composition_hierarchy_tree.png)

## The Container Stack

- Electrons → Atoms (electron containers)
- Atoms → Molecules (atom containers)
- Molecules → Materials (molecule containers)
- Materials → Biomolecules (functional containers)
- Biomolecules → Organelles
- Organelles → Cells
- Cells → Tissues
- Tissues → Organs
- Organs → Organisms

**Key insight:** New properties EMERGE at each level.
```

### Page 5: `Binary-Genealogy`
```markdown
# Binary Genealogy

How composition creates binary signatures.

![Binary Tree](../binary_genealogy_tree.png)

## Binary Encoding

Each composition level has a binary representation:

- **Electron:** `1`
- **Hydrogen:** `1` (1 electron)
- **Carbon:** `111111` (6 electrons)
- **Oxygen:** `11111111` (8 electrons)
- **Water (H₂O):** `1+1+11111111` (10 electrons total)
- **Glucose (C₆H₁₂O₆):** Binary presence + atom counts

The entire genealogy is **encodable in binary**.
```

---

## ✅ Step 7: Upload and Deploy

### Local Setup

```powershell
cd WikiFieldFactopedia

# Initialize git if needed
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: WikiFieldFactopedia with electron genealogy visualizations"

# Push to GitHub
git push -u origin main
```

### Verify

1. Visit: `https://github.com/Acidfang/WikiFieldFactopedia`
2. Check **Code** tab - all files present? ✓
3. Check **Wiki** tab - all 5 pages visible? ✓

---

## 🎯 What You Now Have

✅ **Public GitHub Repository** with:
- 7 visualization files (PNG + GIF)
- Complete README
- 5 wiki pages
- Binary genealogy tree
- Compositional hierarchy
- Electron orbital filling order

✅ **Live at:**
- Repository: `https://github.com/Acidfang/WikiFieldFactopedia`
- Wiki: `https://github.com/Acidfang/WikiFieldFactopedia/wiki`

---

## 🚀 Next Steps (Optional)

1. **Add Python Source Code**
   - Upload `electron_tree_generator.py`
   - Include requirements.txt
   - Add instructions for dynamic generation

2. **GitHub Pages** (for interactive viewer)
   - Enable in Settings
   - Create web viewer for visualizations

3. **Expand to All 128+ Fields**
   - Add field-specific cards
   - Build interactive parameter explorer

---

## ❓ Troubleshooting

**Problem:** Wiki tab doesn't appear
- **Solution:** Go to Settings → Features → Enable Wikis

**Problem:** Images not showing on wiki
- **Solution:** Use relative paths: `../image.png`

**Problem:** Git push fails
- **Solution:** Ensure SSH key is configured or use HTTPS with token

---

**Created:** March 31, 2026  
**Account:** Acidfang  
**Repository:** WikiFieldFactopedia  
**Status:** Ready to Deploy ✓
