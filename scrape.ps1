$htmlPath = "e:\petals\index.html"
$cssDir = "e:\petals\css"
New-Item -ItemType Directory -Force -Path $cssDir | Out-Null

$content = Get-Content $htmlPath -Raw
$newContent = $content

# Regex to find stylesheet links. Handles single and double quotes.
$regex = '<link[^>]+rel=[''"]stylesheet[''"][^>]+href=[''"]([^''"]+)[''"][^>]*>'
$matches = [regex]::Matches($content, $regex)

foreach ($match in $matches) {
    $url = $match.Groups[1].Value
    # Handle protocol-relative URLs
    if ($url.StartsWith("//")) {
        $url = "https:" + $url
    }
    
    # Generate local filename
    $fileName = Split-Path $url -Leaf
    $fileName = $fileName.Split('?')[0] # Remove query string
    $localPath = Join-Path $cssDir $fileName
    
    Write-Host "Downloading $url to $localPath..."
    try {
        Invoke-WebRequest -Uri $url -OutFile $localPath
        
        # Replace in HTML
        # We need to escape the URL for regex replacement or string replacement
        # Simple string replacement is safer for exact matches
        $newContent = $newContent.Replace($match.Groups[1].Value, "css/$fileName")
    }
    catch {
        Write-Host "Failed to download $url : $_"
    }
}

$newContent | Set-Content $htmlPath
Write-Host "Done. CSS files downloaded and HTML updated."
