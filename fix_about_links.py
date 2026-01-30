import re

input_file = r"e:\petals\pages\about.html"
output_file = r"e:\petals\pages\about.html"
base_url = "https://wdtregalia.wpengine.com"

# Exact Mappings (URLs found in the previous step)
# Note: All paths are relative to 'pages/' directory
exact_map = {
    # Home
    f"{base_url}/": "../index.html",
    f"{base_url}": "../index.html",
    f"{base_url}/home-2/": "../home_layouts/home-2.html",
    f"{base_url}/home-3/": "../home_layouts/home-3.html",

    # RTL
    f"{base_url}/rtl-demo": "../pages/rtl-demo.html",
    f"{base_url}/rtl-demo/": "../pages/rtl-demo.html",
    f"{base_url}/rtl-demo/home-2/": "../home_layouts/home-2.html",
    f"{base_url}/rtl-demo/home-3/": "../home_layouts/home-3.html",
    
    # Shop
    f"{base_url}/cart/": "../shop/cart.html",
    f"{base_url}/checkout/": "../shop/checkout.html",
    f"{base_url}/my-account/": "../shop/my-account.html",
    f"{base_url}/wishlist/": "../shop/wishlist.html",
    f"{base_url}/shop/": "../shop/shop.html",
    
    # Shop Types
    f"{base_url}/shop-type-1/": "../shop/shop-type-1.html",
    f"{base_url}/shop-type-2/": "../shop/shop-type-2.html",
    f"{base_url}/shop-type-3/": "../shop/shop-type-3.html",

    # Products (Map all specific products to the generic detail page)
    f"{base_url}/product/simple-product/": "../shop/product-details.html",
    f"{base_url}/product/italian-men-portrait/": "../shop/product-details.html",
    f"{base_url}/product/old-village-modern-art/": "../shop/product-details.html",
    f"{base_url}/product/man-with-a-dog-portrait/": "../shop/product-details.html",
    f"{base_url}/product/roman-man-portrait/": "../shop/product-details.html",
    f"{base_url}/product/gift-card-product/": "../shop/product-details.html",
    
    # Blog
    f"{base_url}/blog/": "../blog/blog.html",
    f"{base_url}/blog-listing/": "../blog/blog-listing.html",
    f"{base_url}/blog-left-sidebar/": "../blog/blog-left-sidebar.html",
    f"{base_url}/blog-right-sidebar/": "../blog/blog-right-sidebar.html",
    f"{base_url}/blog-without-sidebar/": "../blog/blog-without-sidebar.html",
    
    # Blog Posts (Map all posts to generic details)
    f"{base_url}/how-to-enhance-your-color-mixing-skills-to-get-perfect-color-paintings/": "../blog/blog-details.html",
    f"{base_url}/10-essential-drawing-materials-and-tools-required-for-artist/": "../blog/blog-details.html",
    f"{base_url}/easy-watercolor-painting-ideas-and-techniques-for-beginners/": "../blog/blog-details.html",

    # Events
    f"{base_url}/art-events/": "../events/events.html",
    f"{base_url}/events/2024-photography-exhibition/": "../events/event-details.html",
    
    # Pages
    f"{base_url}/about/": "about.html",
    f"{base_url}/contact/": "contact.html",
    f"{base_url}/faq/": "faq.html",
    f"{base_url}/login-page/": "login.html",
    f"{base_url}/404error": "404.html",
}

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Define replacement function
def replace_url(match):
    full_str = match.group(0) # href="..."
    quote = match.group(1)
    url = match.group(2)
    
    # Check exact map
    if url in exact_map:
        return f'href={quote}{exact_map[url]}{quote}'
    
    # Generalized replacements for categories not explicitly listed
    if "/product/" in url:
        return f'href={quote}../shop/product-details.html{quote}'
    if "/events/" in url:
        return f'href={quote}../events/event-details.html{quote}'
    
    # For assets (wp-content, etc.), we KEEP them external for now as per design fidelity
    # UNLESS we have a local replacement logic (like style.css which is already local).
    # The user asked to remove "links which are connected to internet".
    # If they are navigation links (not ending in .css, .js, .png, .jpg), we try to handle them.
    
    is_asset = any(url.endswith(ext) or ext in url for ext in ['.css', '.js', '.png', '.jpg', '.jpeg', '.svg', '.woff', '.woff2', '.ttf'])
    if not is_asset and base_url in url:
        # Default fallback for unknown pages -> Home or 404? 
        # Let's map to index for safety, or leave it if it's really unknown.
        # But user wants them REMOVED.
        return f'href={quote}../index.html{quote}' # Fallback
        
    return full_str

# Regex to find hrefs with the base URL
# matches href="https://wdtregalia..." or href='...'
content = re.sub(r'href=(["\'])(https://wdtregalia.wpengine.com[^"\']*)["\']', replace_url, content)

# Remove RSS feeds and unnecessary meta links from head if they point to external
content = re.sub(r'<link rel="alternate"[^>]+wpengine.com[^>]+>', '', content)
content = re.sub(r'<link rel="EditURI"[^>]+wpengine.com[^>]+>', '', content)
content = re.sub(r'<link rel="https://api.w.org/"[^>]+>', '', content)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Fixed links in {output_file}")
