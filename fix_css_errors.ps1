$cssFile = "e:\petals\css\style.css"
$content = Get-Content -Path $cssFile -Raw

# 1. Remove @charset declarations
# Regex to match @charset "UTF-8"; case insensitive, with possible spaces
$content = $content -replace '@charset "[^"]+";', ""

# 2. Fix potential issue with @import not being at the top
# For now, we will just log them if found not at the top, or maybe just leave them if they are imports of fonts which "should" work in some browsers but technically invalid.
# Actually, let's just move them to the top if we can, or just stripping charset is the main fix requested.

# Let's also check for the specific issue where minified files are concatenated without a newline separator which might cause issues if the previous file ended without a closing brace or with a comment that didn't close properly (though our merge script added newlines).
# Our merge script did: "$_`r`n" so there should be newlines.

Set-Content -Path $cssFile -Value $content -Encoding UTF8

Write-Host "Cleaned up style.css"
