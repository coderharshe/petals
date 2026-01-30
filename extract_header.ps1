$path = "index.html"
$content = Get-Content $path -Raw -Encoding UTF8

# Extract Header
$headerMatch = [regex]::Match($content, '(?ms)<header id="header">.*?</header>')
if ($headerMatch.Success) {
    $headerBlock = $headerMatch.Value
    $headerBlock | Set-Content "header_template.html" -Encoding UTF8
    Write-Host "Header extracted."
}
else {
    Write-Host "Header not found!"
}

# Extract CSS link for header 3884 if present
$cssMatch = [regex]::Match($content, '<link[^>]*href=[^>]*post-3884\.css[^>]*>')
if ($cssMatch.Success) {
    $cssLink = $cssMatch.Value
    $cssLink | Set-Content "header_css_link.html" -Encoding UTF8
    Write-Host "CSS Link extracted."
}
