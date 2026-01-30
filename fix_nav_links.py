import os

file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Expanded replacements list based on typical WP site structure and user needs
replacements = {
    'https://wdtregalia.wpengine.com/home-2/': 'index.html',
    'https://wdtregalia.wpengine.com/': 'index.html',
    'https://wdtregalia.wpengine.com/about/': 'pages/about.html',
    'https://wdtregalia.wpengine.com/about-us/': 'pages/about.html',
    'https://wdtregalia.wpengine.com/shop/': 'shop/shop.html',
    'https://wdtregalia.wpengine.com/contact/': 'pages/contact.html',
    'https://wdtregalia.wpengine.com/contact-us/': 'pages/contact.html',
    'https://wdtregalia.wpengine.com/faq/': 'pages/faq.html',
    'https://wdtregalia.wpengine.com/blog/': 'blog/blog.html',
    'https://wdtregalia.wpengine.com/wishlist/': 'shop/wishlist.html',
    'https://wdtregalia.wpengine.com/my-account/': 'shop/account.html',
    'https://wdtregalia.wpengine.com/cart/': 'shop/cart.html',
    'https://wdtregalia.wpengine.com/checkout/': 'shop/checkout.html',
    'home-layouts/home-2.html': 'index.html', # Internal reference if any
}

# Replace specific navigation links
for old, new in replacements.items():
    content = content.replace(f'"{old}"', f'"{new}"')
    content = content.replace(f"'{old}'", f"'{new}'")
    # Also handle trailing slash variations just in case
    if old.endswith('/'):
        old_no_slash = old[:-1]
        content = content.replace(f'"{old_no_slash}"', f'"{new}"')
        content = content.replace(f"'{old_no_slash}'", f"'{new}'")

# Generic catch-all for remaining wdtregalia links to point to # (placeholder) or keep as is?
# Better to leave them or log them.
# content = content.replace('https://wdtregalia.wpengine.com', '#') 

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated links in {file_path}")
