$htmlPath = "e:\petals\index.html"
$cssDir = "e:\petals\css"
$outputCss = "e:\petals\css\style.css"

$htmlContent = Get-Content $htmlPath -Raw -Encoding UTF8

# RegEx to find all linked CSS files in the 'css/' folder
# Case insensitive, single/double quotes
$pattern = '<link[^>]+href=[''"]css/([^''"]+)[''"][^>]*>'
$matches = [regex]::Matches($htmlContent, $pattern)

if ($matches.Count -eq 0) {
    Write-Error "No CSS links found to merge."
    exit
}

Write-Host "Found $($matches.Count) CSS files to merge."

$combinedCss = New-Object System.Text.StringBuilder

# Iterate through matches to merge content
foreach ($match in $matches) {
    $fileName = $match.Groups[1].Value
    $filePath = Join-Path $cssDir $fileName
    
    if (Test-Path $filePath) {
        Write-Host "Merging: $fileName"
        $combinedCss.AppendLine("/* --- Start of $fileName --- */") | Out-Null
        $fileContent = Get-Content $filePath -Raw -Encoding UTF8
        # Simple fix for imports or relative paths could go here, but skipping for now
        $combinedCss.AppendLine($fileContent) | Out-Null
        $combinedCss.AppendLine("/* --- End of $fileName --- */") | Out-Null
    }
    else {
        Write-Warning "File not found, skipping: $fileName"
    }
}

# Write the combined CSS
$combinedCss.ToString() | Set-Content $outputCss -Encoding UTF8
Write-Host "Created combined CSS at $outputCss"

# Update HTML
# We will remove all matched lines, and insert the new link at the position of the LAST match.
$newHtml = $htmlContent

# Identify the last match to replace it with the new link
$lastMatch = $matches[$matches.Count - 1]
$newLinkTag = "<link rel='stylesheet' href='css/style.css' type='text/css' media='all' />"

# Replace the last match with the new link
$newHtml = $newHtml.Remove($lastMatch.Index, $lastMatch.Length).Insert($lastMatch.Index, $newLinkTag)

# Remove all other matches (in reverse order to not mess up indices)
for ($i = $matches.Count - 2; $i -ge 0; $i--) {
    $m = $matches[$i]
    # Check if we already replaced this (unlikely since we iterate distinct matches unless duplicates exist)
    # We simply remove the tag string.
    # Note: Text manipulation by index on the *string* needs careful handling if indices shift.
    # Actually, simpler approach: String Replace?
    # No, duplicates might exist.
    # Safest: Use the StringBuilder approach or regex replace with callback?
    # PowerShell regex replace can't easily skip the last one.
    
    # We'll use the specific string logic:
    # Since we modified the string for the LAST match, previous match indices are still valid 
    # IF the last match was physically after them (which it is).
    # so we can just remove them.
    $newHtml = $newHtml.Remove($m.Index, $m.Length)
}

# Clean up empty lines left behind? 
# The removal leaves the line break if it was outside the match. 
# We'll do a quick regex pass to remove empty lines containing only whitespace if we care.
# But browsers handle it fine.

$newHtml | Set-Content $htmlPath -Encoding UTF8
Write-Host "Updated index.html"

# Delete old CSS files (except style.css)
Get-ChildItem $cssDir -Filter *.css | Where-Object { $_.Name -ne "style.css" } | Remove-Item
Write-Host "Cleaned up old CSS files."
