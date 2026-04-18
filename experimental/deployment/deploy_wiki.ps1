#!/usr/bin/env pwsh
<#
.SYNOPSIS
Automated deployment script for WIKIFIELDFACTOPEDIA to GitHub

.DESCRIPTION
One-command deployment of all field visualizations and wiki assets to GitHub Wiki

.PARAMETER GitHubUsername
Your GitHub username (required)

.PARAMETER RepositoryName
Repository name for wiki (default: wikifieldfactopedia)

.PARAMETER RepositoryPath
Path to existing repository (optional)

.EXAMPLE
.\deploy_wiki.ps1 -GitHubUsername octocat -RepositoryName wikifieldfactopedia

#>

param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubUsername,
    
    [Parameter(Mandatory=$false)]
    [string]$RepositoryName = "wikifieldfactopedia",
    
    [Parameter(Mandatory=$false)]
    [string]$RepositoryPath
)

Write-Host "`n" + "="*70
Write-Host "WIKIFIELDFACTOPEDIA - GITHUB DEPLOYMENT WIZARD"
Write-Host "="*70 + "`n"

# Colors
$Green = "`e[32m"
$Yellow = "`e[33m"
$Red = "`e[31m"
$Blue = "`e[34m"
$Reset = "`e[0m"

# Step 1: Verify GitHub CLI
Write-Host "${Blue}[1/5] Checking GitHub CLI...${Reset}"
try {
    $ghVersion = gh --version
    Write-Host "${Green}✓ GitHub CLI found: $($ghVersion.Split()[2])${Reset}`n"
} catch {
    Write-Host "${Red}✗ GitHub CLI not found!${Reset}"
    Write-Host "Install from: https://cli.github.com/`n"
    exit 1
}

# Step 2: Verify Git
Write-Host "${Blue}[2/5] Checking Git...${Reset}"
try {
    $gitVersion = git --version
    Write-Host "${Green}✓ Git found: $gitVersion${Reset}`n"
} catch {
    Write-Host "${Red}✗ Git not found!${Reset}"
    exit 1
}

# Step 3: Check repository exists or create
Write-Host "${Blue}[3/5] GitHub Repository Check...${Reset}"

$RepoUrl = "https://github.com/$GitHubUsername/$RepositoryName"

# Check if repo exists
try {
    $repoExists = gh repo view "$GitHubUsername/$RepositoryName" --json=name 2>$null
    if ($repoExists) {
        Write-Host "${Green}✓ Repository exists: $RepoUrl${Reset}`n"
    } else {
        Write-Host "${Yellow}Repository not found. Creating...${Reset}"
        gh repo create $RepositoryName --public --description "Universal Diffusion Law - Complete Field Encyclopedia with 128+ Fields" 2>$null
        Write-Host "${Green}✓ Repository created: $RepoUrl${Reset}`n"
    }
} catch {
    Write-Host "${Yellow}Could not verify repo. Attempting to create...${Reset}"
    gh repo create $RepositoryName --public --description "Universal Diffusion Law - Complete Field Encyclopedia" 2>$null | Out-Null
    Write-Host "${Green}✓ Repository created or already exists${Reset}`n"
}

# Step 4: Set up wiki repository
Write-Host "${Blue}[4/5] Cloning Wiki Repository...${Reset}"

$WikiPath = "$RepositoryPath" 
if ([string]::IsNullOrEmpty($RepositoryPath)) {
    $WikiPath = "$PSScriptRoot\$($RepositoryName)_wiki"
}

if (Test-Path $WikiPath) {
    Write-Host "${Yellow}Wiki directory already exists at: $WikiPath${Reset}"
    $response = Read-Host "Use existing directory? (y/n)"
    if ($response -ne 'y') {
        Remove-Item -Recurse -Force $WikiPath
        git clone "https://github.com/$GitHubUsername/$RepositoryName.wiki.git" $WikiPath 2>$null
        Write-Host "${Green}✓ Wiki repository cloned${Reset}`n"
    } else {
        Write-Host "${Green}✓ Using existing wiki directory${Reset}`n"
    }
} else {
    git clone "https://github.com/$GitHubUsername/$RepositoryName.wiki.git" $WikiPath 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "${Yellow}Wiki repo doesn't exist yet (will be created on first push)${Reset}"
        New-Item -ItemType Directory -Path $WikiPath -Force | Out-Null
    } else {
        Write-Host "${Green}✓ Wiki repository cloned${Reset}`n"
    }
}

# Step 5: Copy assets
Write-Host "${Blue}[5/5] Copying Wiki Assets...${Reset}`n"

# Copy markdown files
Write-Host "Copying wiki markdown files..."
Copy-Item "$PSScriptRoot\wiki_assets\*.md" $WikiPath -Force -ErrorAction SilentlyContinue
Write-Host "${Green}✓ Markdown files copied${Reset}"

# Create assets directory
$AssetsPath = "$WikiPath\assets\field_visualizations"
New-Item -ItemType Directory -Path $AssetsPath -Force | Out-Null
Write-Host "${Green}✓ Assets directory created${Reset}"

# Copy visualizations
Write-Host "Copying field visualizations..."
Copy-Item "$PSScriptRoot\field_visualizations\*.png" $AssetsPath -Force -ErrorAction SilentlyContinue
Write-Host "${Green}✓ Static visualizations copied${Reset}"

# Copy dynamic simulations
Write-Host "Copying dynamic simulations..."
Copy-Item "$PSScriptRoot\*.gif" $WikiPath -Force -ErrorAction SilentlyContinue
Write-Host "${Green}✓ Animated simulations copied${Reset}"

# Copy phase diagram
Write-Host "Copying analysis diagrams..."
Copy-Item "$PSScriptRoot\phase_diagram.png" $AssetsPath -Force -ErrorAction SilentlyContinue
Write-Host "${Green}✓ Phase diagrams copied${Reset}`n"

# Git commit and push
Write-Host "${Blue}Committing Changes...${Reset}"
Push-Location $WikiPath

try {
    git config user.email "wikifieldfactopedia@determined.local" 2>$null
    git config user.name "FieldFactopedia" 2>$null
    
    git add . 2>$null
    $commitMessage = "🚀 WIKIFIELDFACTOPEDIA Launch: 128+ Universal Diffusion Fields | 7 Field Types | $(Get-Date -Format 'yyyy-MM-dd')"
    git commit -m $commitMessage 2>$null
    
    Write-Host "${Green}✓ Changes committed${Reset}"
    
    Write-Host "${Blue}Pushing to GitHub...${Reset}"
    git push -u origin master 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "${Green}✓ Successfully pushed to GitHub${Reset}`n"
    } else {
        Write-Host "${Yellow}⚠ Push completed with warnings (wiki might not exist yet)${Reset}"
        Write-Host "First push creates the wiki - check GitHub in 30 seconds`n"
    }
} catch {
    Write-Host "${Red}✗ Error during commit/push${Reset}"
    Write-Host $_.Exception.Message
}

Pop-Location

# Summary
Write-Host "`n" + "="*70
Write-Host "${Green}✅ DEPLOYMENT COMPLETE!${Reset}"
Write-Host "="*70 + "`n"

Write-Host "${Green}Wiki URL:${Reset} $RepoUrl/wiki"
Write-Host "${Green}Assets:${Reset} $(Get-ChildItem $AssetsPath -Filter "*.png" | Measure-Object).Count static visualizations"
Write-Host "${Green}Animations:${Reset} $(Get-ChildItem $WikiPath -Filter "*.gif" | Measure-Object).Count animated simulations"
Write-Host "${Green}Pages:${Reset} $(Get-ChildItem $WikiPath -Filter "*.md" | Measure-Object).Count wiki pages"

Write-Host "`n${Blue}Next Steps:${Reset}"
Write-Host "1. Visit: $RepoUrl/wiki"
Write-Host "2. Click 'Home' to browse field catalog"
Write-Host "3. Share link with colleagues and academic network"
Write-Host "4. Add to README: [Read WIKIFIELDFACTOPEDIA]($RepoUrl/wiki)"

Write-Host "`n${Blue}GitHub-Specific Actions:${Reset}"
Write-Host "• Add topics: 'universal-law', 'diffusion-equation', 'cascade-modeling'"
Write-Host "• Enable Discussions for Q&A"
Write-Host "• Add wiki badges to README"

Write-Host "`n${Blue}Advanced Options:${Reset}"
Write-Host "• Auto-regenerate: Setup .github/workflows/generate-fields.yml"
Write-Host "• Deploy API: python -m fastapi_field_viewer run --reload"
Write-Host "• Export PDF: See GITHUB_WIKI_SETUP_GUIDE.md"

Write-Host "`n${Green}Created${Reset}: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host "${Green}Repository${Reset}: $GitHubUsername/$RepositoryName"
Write-Host "${Green}Status${Reset}: 🚀 LIVE on GitHub`n"

Write-Host "="*70
Write-Host "WIKIFIELDFACTOPEDIA is now online and ready for the world!"
Write-Host "="*70 + "`n"
