$path = "index.html"
$content = Get-Content $path -Raw -Encoding UTF8

# Define replacements
$replacements = @{
    'https://wdtregalia.wpengine.com/home-2/'                                                = 'index.html'
    'https://wdtregalia.wpengine.com/about/'                                                 = 'pages/about.html'
    'https://wdtregalia.wpengine.com/about-us/'                                              = 'pages/about.html'
    'https://wdtregalia.wpengine.com/shop/'                                                  = 'shop/shop.html'
    'https://wdtregalia.wpengine.com/contact/'                                               = 'pages/contact.html'
    'https://wdtregalia.wpengine.com/contact-us/'                                            = 'pages/contact.html'
    'https://wdtregalia.wpengine.com/faq/'                                                   = 'pages/faq.html'
    'https://wdtregalia.wpengine.com/blog/'                                                  = 'blog/blog.html'
    'https://wdtregalia.wpengine.com/wishlist/'                                              = 'shop/wishlist.html'
    'https://wdtregalia.wpengine.com/my-account/'                                            = 'shop/account.html'
    'https://wdtregalia.wpengine.com/cart/'                                                  = 'shop/cart.html'
    'https://wdtregalia.wpengine.com/checkout/'                                              = 'shop/checkout.html'
    'home-layouts/home-2.html'                                                               = 'index.html'
    
    # Text Logo Fix (Ensure these point to valid local files or the one we downloaded)
    'https://wdtregalia.wpengine.com/wp-content/themes/regalia/assets/images/light-logo.svg' = 'wp-content/uploads/2024/03/logo-new.svg'
    'https://wdtregalia.wpengine.com/wp-content/uploads/2024/03/logo-new.svg'                = 'wp-content/uploads/2024/03/logo-new.svg'
    
    # Handle wp-content to keep relative structure for assets
    'https://wdtregalia.wpengine.com/wp-content/'                                            = 'wp-content/'
    'https://wdtregalia.wpengine.com/wp-includes/'                                           = 'wp-includes/'
    
    # Base domain fallback (must be last in sorted list)
    'https://wdtregalia.wpengine.com/'                                                       = 'index.html'
}

# Sort keys by length descending
$sortedKeys = $replacements.Keys | Sort-Object { $_.Length } -Descending

foreach ($key in $sortedKeys) {
    $content = $content.Replace($key, $replacements[$key])
}

$content | Set-Content $path -Encoding UTF8
Write-Host "Links updated successfully with logo fix."
