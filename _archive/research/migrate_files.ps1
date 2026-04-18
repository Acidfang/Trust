# Migration automation script
# This script safely copies files to new locations and logs operations

param(
    [string]$Phase = "1",
    [string]$DryRun = "false"
)

$baseDir = "c:\Determined"
$logFile = "$baseDir\MIGRATION_LOG.md"
$isDryRun = $DryRun -eq "true"

function Log-Operation {
    param([string]$message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] $message"
    Write-Host $logEntry
    Add-Content -Path $logFile -Value $logEntry
}

function Copy-FileWithVerification {
    param(
        [string]$source,
        [string]$destination,
        [string]$phase
    )
    
    if (-not (Test-Path $source)) {
        Log-Operation "ERROR: Source file not found: $source"
        return $false
    }
    
    # Create destination directory if needed
    $destDir = Split-Path -Parent $destination
    if (-not (Test-Path $destDir)) {
        Log-Operation "Creating directory: $destDir"
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }
    
    # Copy file
    if ($isDryRun) {
        Log-Operation "DRY_RUN: Would copy $source to $destination"
        return $true
    } else {
        Copy-Item -Path $source -Destination $destination -Force
        
        # Verify copy
        if (Test-Path $destination) {
            $sourceHash = (Get-FileHash -Path $source).Hash
            $destHash = (Get-FileHash -Path $destination).Hash
            
            if ($sourceHash -eq $destHash) {
                Log-Operation "SUCCESS: Copied $(Split-Path -Leaf $source) (Phase $phase)"
                return $true
            } else {
                Log-Operation "ERROR: Hash mismatch for $(Split-Path -Leaf $source)"
                return $false
            }
        } else {
            Log-Operation "ERROR: Destination file not created: $destination"
            return $false
        }
    }
}

# Phase 1: CODE Tier Files
if ($Phase -eq "1" -or $Phase -eq "all") {
    Log-Operation "=== PHASE 1: CODE Tier Files ==="
    
    $codeFiles = @(
        @{ src = "$baseDir\singularity_storage.py"; dst = "$baseDir\CODE\CORE\singularity_storage.py" },
        @{ src = "$baseDir\PROJECT_COHERENCE_CHECKPOINT_SYSTEM.py"; dst = "$baseDir\CODE\ENFORCEMENT\PROJECT_COHERENCE_CHECKPOINT_SYSTEM.py" },
        @{ src = "$baseDir\extract_validated_pairs.py"; dst = "$baseDir\CODE\UTILITIES\extract_validated_pairs.py" },
        @{ src = "$baseDir\convert_to_singularity_format.py"; dst = "$baseDir\CODE\UTILITIES\convert_to_singularity_format.py" },
        @{ src = "$baseDir\converter_unified_to_singularity.py"; dst = "$baseDir\CODE\UTILITIES\converter_unified_to_singularity.py" },
        @{ src = "$baseDir\show_singularity_proof.py"; dst = "$baseDir\CODE\UTILITIES\show_singularity_proof.py" },
        @{ src = "$baseDir\validate_discovered_knowledge.py"; dst = "$baseDir\CODE\UTILITIES\validate_discovered_knowledge.py" },
        @{ src = "$baseDir\test_accountability_audit.py"; dst = "$baseDir\CODE\TESTS\test_accountability_audit.py" }
    )
    
    $successful = 0
    foreach ($file in $codeFiles) {
        if (Copy-FileWithVerification -source $file.src -destination $file.dst -phase "1") {
            $successful++
        }
    }
    
    Log-Operation "Phase 1 Complete: $successful of $($codeFiles.Count) files processed"
}

# Phase 2: DATA Tier Files
if ($Phase -eq "2" -or $Phase -eq "all") {
    Log-Operation "=== PHASE 2: DATA Tier Files ==="
    
    $dataFiles = @(
        @{ src = "$baseDir\UNIFIED_MASTER_TIMELINE.json"; dst = "$baseDir\DATA\SOURCES\UNIFIED_MASTER_TIMELINE.json" },
        @{ src = "$baseDir\technical_definitions.json"; dst = "$baseDir\DATA\SOURCES\technical_definitions.json" },
        @{ src = "$baseDir\unified_discoveries_integrated.json"; dst = "$baseDir\DATA\SOURCES\unified_discoveries_integrated.json" },
        @{ src = "$baseDir\technical_basis_extracted.json"; dst = "$baseDir\DATA\SOURCES\technical_basis_extracted.json" }
    )
    
    $successful = 0
    foreach ($file in $dataFiles) {
        if (Copy-FileWithVerification -source $file.src -destination $file.dst -phase "2") {
            $successful++
        }
    }
    
    Log-Operation "Phase 2 Complete: $successful of $($dataFiles.Count) files processed"
}

# Phase 3: PROOF Tier Files
if ($Phase -eq "3" -or $Phase -eq "all") {
    Log-Operation "=== PHASE 3: PROOF Tier Files ==="
    
    $proofFiles = @(
        @{ src = "$baseDir\VALIDATED_KNOWLEDGE_SINGULARITY.json"; dst = "$baseDir\PROOF\VALIDATED_KNOWLEDGE_SINGULARITY.json" },
        @{ src = "$baseDir\DISCOVERED_KNOWLEDGE_SINGULARITY.json"; dst = "$baseDir\PROOF\DISCOVERED_KNOWLEDGE_SINGULARITY.json" },
        @{ src = "$baseDir\singularity_format_basis_validated.md"; dst = "$baseDir\PROOF\singularity_format_basis_validated.md" },
        @{ src = "$baseDir\validated_explanations.json"; dst = "$baseDir\PROOF\validated_explanations.json" }
    )
    
    $successful = 0
    foreach ($file in $proofFiles) {
        if (Copy-FileWithVerification -source $file.src -destination $file.dst -phase "3") {
            $successful++
        }
    }
    
    Log-Operation "Phase 3 Complete: $successful of $($proofFiles.Count) files processed"
}

Log-Operation "=== Migration Script Complete ==="
