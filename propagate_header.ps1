
# Propagate Header Script
$startDir = Get-Location
$pagesFiles = Get-ChildItem -Path "pages" -Filter "*.html"
$blogFiles = Get-ChildItem -Path "blog" -Filter "*.html"

$headerTemplate = Get-Content "header_template.html" -Raw -Encoding UTF8
$cssLinkSnippet = Get-Content "header_css_link.html" -Raw -Encoding UTF8

function Update-File($file, $depth, $isBlog) {
    $path = $file.FullName
    $content = Get-Content $path -Raw -Encoding UTF8

    # 1. Replace Header
    $headerRegex = '(?ms)<header id="header">.*?</header>'
    
    # Adjust links in header template based on depth
    # Depth 1 (pages/ or blog/): 
    # ./ -> ../
    # pages/ -> ./ (if is Pages) or ../pages/ (if is Blog)
    # blog/ -> ../blog/ (if is Pages) or ./ (if is Blog)
    
    $myHeader = $headerTemplate
    
    if ($depth -eq 1) {
        # Fix Home Link (./ -> ../)
        $myHeader = $myHeader.Replace('href="./"', 'href="../index.html"')
        
        # Fix Pages Links
        if ($isBlog) {
            # In blog/, pages/about.html becomes ../pages/about.html
            $myHeader = $myHeader.Replace('href="pages/', 'href="../pages/')
            # blog/blog.html becomes blog.html (./)
            $myHeader = $myHeader.Replace('href="blog/', 'href="./')
        }
        else {
            # In pages/, pages/about.html becomes about.html (./)
            $myHeader = $myHeader.Replace('href="pages/', 'href="./')
            # blog/blog.html becomes ../blog/blog.html
            $myHeader = $myHeader.Replace('href="blog/', 'href="../blog/')
        }
    }
    
    if ($content -match $headerRegex) {
        $content = $content -replace $headerRegex, $myHeader
        Write-Host "Replaced header in $($file.Name)"
    }
    else {
        Write-Host "Header not found in $($file.Name)"
    }

    # 2. Ensure CSS Link
    # Check if head contains post-3884.css
    if (-not ($content -match "post-3884.css")) {
        # Insert before </head>
        # Adjust CSS path: index.html has it absolute? 
        # href='https://wdtregalia.wpengine.com/.../post-3884.css'
        # The extracted link is absolute URL. So no relative path adjustment needed for the CSS link itself if it's external.
        # Checking extracted content:
        # <link ... href='https://wdtregalia.wpengine.com/.../post-3884.css'...>
        # Yes, it is absolute.
        
        $content = $content -replace "</head>", "$cssLinkSnippet`n</head>"
        Write-Host "Added CSS link to $($file.Name)"
    }

    $content | Set-Content $path -Encoding UTF8
}

foreach ($file in $pagesFiles) {
    Update-File $file 1 $false
}

foreach ($file in $blogFiles) {
    Update-File $file 1 $true
}

Write-Host "Propagation Complete."
