param([string]$RootPath = ".")

$count = 0
Get-ChildItem -Path $RootPath -Include "*.md" -Recurse -Force | ForEach-Object {
    $file = $_
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    $original = $content
    
    # Replace {{ site.baseurl }}/ with /Trust/
    $content = $content -replace '\{\{\s*site\.baseurl\s*\}\}/', '/Trust/'
    
    # Also handle cases without trailing slash
    $content = $content -replace '\{\{\s*site\.baseurl\s*\}\}', '/Trust'
    
    if ($content -ne $original) {
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8 -Force
        Write-Host "✓ $($file.FullName)"
        $count++
    }
}

Write-Host ""
Write-Host "Fixed $count files" -ForegroundColor Green
