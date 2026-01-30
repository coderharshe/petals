$htmlPath = "e:\petals\index.html"
$cssDir = "e:\petals\css"

# Read with UTF8
$content = Get-Content $htmlPath -Raw -Encoding UTF8
$newContent = $content

# Regex to find stylesheet links
$regex = '<link[^>]+rel=[''"]stylesheet[''"][^>]+href=[''"]([^''"]+)[''"][^>]*>'
$matches = [regex]::Matches($content, $regex)

Write-Host "Found $($matches.Count) matches."

foreach ($match in $matches) {
    $originalUrl = $match.Groups[1].Value
    $url = $originalUrl
    
    # Handle protocol-relative URLs
    if ($url.StartsWith("//")) {
        $url = "https:" + $url
    }
    
    # Generate local filename logic (must match download script)
    $fileName = Split-Path $url -Leaf
    $fileName = $fileName.Split('?')[0] 
    
    $localPath = Join-Path $cssDir $fileName
    
    if (Test-Path $localPath) {
        Write-Host "Replacing $originalUrl with css/$fileName"
        # Use String.Replace which replaces all occurrences
        $newContent = $newContent.Replace($originalUrl, "css/$fileName")
    } else {
        Write-Host "Skipping $fileName (not found locally)"
    }
}

# Write with UTF8
$newContent | Set-Content $htmlPath -Encoding UTF8
Write-Host "Done."
