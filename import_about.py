import os
import re

# Config
input_file = r"e:\petals\fetched_about.html"
output_file = r"e:\petals\pages\about.html"
base_url = "https://wdtregalia.wpengine.com"

# URL to Local File Mapping (Relative to 'pages/' folder)
# We are in 'pages/', so 'index.html' is '../index.html'
url_map = {
    "/": "../index.html",
    base_url + "/": "../index.html",
    
    "/shop/": "../shop/shop.html",
    base_url + "/shop/": "../shop/shop.html",
    
    "/about/": "about.html",
    base_url + "/about/": "about.html",
    
    "/contact/": "contact.html",
    base_url + "/contact/": "contact.html",
    
    "/faq/": "faq.html",
    base_url + "/faq/": "faq.html",
    
    "/blog/": "../blog/blog.html",
    base_url + "/blog/": "../blog/blog.html",
    
    "/events/": "../events/events.html",
    base_url + "/events/": "../events/events.html",
    
    "/cart/": "../shop/cart.html",
    base_url + "/cart/": "../shop/cart.html",
    
    "/checkout/": "../shop/checkout.html",
    base_url + "/checkout/": "../shop/checkout.html",
    
    "/my-account/": "../shop/my-account.html",
    base_url + "/my-account/": "../shop/my-account.html",
    
    "/wishlist/": "../shop/wishlist.html",
    base_url + "/wishlist/": "../shop/wishlist.html",
}

# Regex for preloader
preloader_pattern = re.compile(r'<div class="pre-loader loader2">.*?</div>\s*</div>', re.DOTALL)

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove Preloader
# Simple string check first
if '<div class="pre-loader loader2">' in content:
    # Try regex for robust removal including children
    content = re.sub(r'<div class="pre-loader loader2">[\s\S]*?</div>\s*</div>', '', content)
    # Fallback cleanup if regex missed (sometimes nested divs are tricky)
    content = content.replace('<div class="pre-loader loader2">', '<div class="pre-loader loader2" style="display:none;">')

# 2. Update Navigation Links
# We look for href="..." and replace if it matches our map
def replace_link(match):
    full_match = match.group(0)
    quote = match.group(1)
    url = match.group(2)
    
    # Clean trailing slash for matching (optional, but good for consistency)
    clean_url = url
    if url.endswith('/') and len(url) > 1:
        clean_url = url # keep it for now, map has slashes
    
    # Check exact match in map
    if url in url_map:
        return f'href={quote}{url_map[url]}{quote}'
    
    # Check simplified match (e.g. ignoring trailing slash or query params)
    base_url_clean = url.split('?')[0].split('#')[0]
    if base_url_clean in url_map:
         return f'href={quote}{url_map[base_url_clean]}{quote}'

    return full_match

content = re.sub(r'href=(["\'])(.*?)["\']', replace_link, content)

# 3. Ensure CSS links to local style.css if possible, OR just add it if missing
# The user wants "all styles". The fetched page likely links to wp-content/themes/regalia/style.css
# We can inject our local specific CSS fix link for good measure or replace the main theme css.
# Let's see if we can find the main style link.
# Usually it's ends with /style.css
# We want to replace valid WP style links with our local logic ONLY if we downloaded them.
# Use '../css/style.css' as an override or addition.
# PROPOSAL: Add our local style.css at the end of <head> to ensure our overrides work, 
# but keep the external CSS for the "layout and design" fidelity.

head_end = "</head>"
local_style_link = '<link rel="stylesheet" href="../css/style.css" type="text/css" media="all" />'
if head_end in content:
    content = content.replace(head_end, f"{local_style_link}\n{head_end}")

# 4. Save to pages/about.html
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Processed {input_file} -> {output_file}")
