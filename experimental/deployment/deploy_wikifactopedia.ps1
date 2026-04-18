#!/usr/bin/env pwsh
<#
.SYNOPSIS
    WikiFieldFactopedia GitHub Setup and Deployment Script
    Automates cloning, copying files, and pushing to GitHub

.DESCRIPTION
    This script handles:
    1. Cloning the GitHub repository
    2. Copying all visualization files
    3. Creating wiki pages
    4. Committing and pushing to GitHub

.PARAMETER RepositoryUrl
    Full URL of your WikiFieldFactopedia repository
    Example: https://github.com/Acidfang/WikiFieldFactopedia.git

.PARAMETER LocalPath
    Where to clone the repository locally
    Default: C:\WikiFieldFactopedia

.EXAMPLE
    .\deploy_wikifactopedia.ps1 -RepositoryUrl "https://github.com/Acidfang/WikiFieldFactopedia.git"
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$RepositoryUrl = "https://github.com/Acidfang/WikiFieldFactopedia.git",
    
    [Parameter(Mandatory=$false)]
    [string]$LocalPath = "C:\WikiFieldFactopedia",
    
    [Parameter(Mandatory=$false)]
    [string]$SourcePath = "C:\Determined"
)

# Color output
function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Cyan
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

# Start
Write-Info "WikiFieldFactopedia Deployment Script"
Write-Info "======================================="

# Step 1: Clone repository
if (Test-Path $LocalPath) {
    Write-Warning "Directory $LocalPath already exists"
    $response = Read-Host "Overwrite? (yes/no)"
    if ($response -eq "yes") {
        Remove-Item -Path $LocalPath -Recurse -Force
        Write-Info "Removed existing directory"
    } else {
        Write-Warning "Keeping existing directory"
    }
}

Write-Info "Cloning repository..."
try {
    git clone $RepositoryUrl $LocalPath
    Write-Success "Repository cloned"
} catch {
    Write-Error "Failed to clone: $_"
    exit 1
}

cd $LocalPath

# Step 2: Copy visualization files
Write-Info "Copying visualization files..."

$files_to_copy = @(
    "electron_tree_static.png",
    "electron_element_tree.png",
    "orbital_filling_order.png",
    "electron_growth_animation.gif",
    "composition_hierarchy_tree.png",
    "branching_genealogy.png",
    "binary_genealogy_tree.png",
    "electron_tree_generator.py"
)

foreach ($file in $files_to_copy) {
    $source = Join-Path $SourcePath $file
    $dest = Join-Path $LocalPath $file
    
    if (Test-Path $source) {
        Copy-Item -Path $source -Destination $dest -Force
        Write-Success "Copied $file"
    } else {
        Write-Warning "Not found: $file"
    }
}

# Step 3: Create README.md
Write-Info "Creating README.md..."

$readme_content = @"
# WikiFieldFactopedia

Universal Field Genealogy: How electrons evolve into complexity.

## Quick Navigation

- [Electron Genealogy](./docs/electron-genealogy.md)
- [Element Evolution](./docs/element-evolution.md)
- [Composition Hierarchy](./docs/composition-hierarchy.md)
- [Binary Genealogy](./docs/binary-genealogy.md)

## Key Visualizations

### Electron Orbital Genealogy
![Electron Tree](./electron_tree_static.png)

### Compositional Hierarchy
![Composition Tree](./composition_hierarchy_tree.png)

### Binary Genealogy
![Binary Tree](./binary_genealogy_tree.png)

## The Universal Law

\`\`\`
dρ/dt = D·∇²ρ + α·f_external + β·ρ²
\`\`\`

Every field evolves according to this diffusion equation. From electrons to atoms to molecules to life—one law governs all composition.

## About

This repository documents the **genealogy of compositional hierarchy**:
- How electrons fill orbitals (Aufbau principle)
- How elements emerge from electron configurations
- How atoms combine into molecules
- How materials emerge from molecular interactions
- All encoded in binary representations

Generated March 31, 2026 with universal diffusion law framework.
"@

$readme_content | Set-Content -Path (Join-Path $LocalPath "README.md") -Encoding UTF8
Write-Success "Created README.md"

# Step 4: Commit and prepare for push
Write-Info "Preparing git commit..."

git add .

$commit_message = "WikiFieldFactopedia: Initial electron genealogy visualizations`n`n- Electron orbital filling order (Aufbau principle)`n- Periodic table element evolution`n- Compositional hierarchy (electrons→atoms→molecules→life)`n- Binary genealogy encoding`n- Interactive animations`n`nGenerated with universal diffusion law framework"

git commit -m ([string]::Format('"{0}"', $commit_message.Replace("`n", "\n")))
Write-Success "Commit prepared"

Write-Info ""
Write-Success "Setup Complete!"
Write-Info ""
Write-Info "📁 Files ready at: $LocalPath"
Write-Info ""
Write-Info "📤 To push to GitHub, run:"
Write-Info ""
Write-Host "   cd $LocalPath" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Info ""
Write-Info "🌐 Then enable GitHub Wiki in repository settings"
Write-Info ""
Write-Info "✓ Repository URL: $RepositoryUrl"
Write-Info ""
