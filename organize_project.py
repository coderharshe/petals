import os
import re
import shutil

base_dir = r"e:\petals"

# Define the desired structure
# Filename -> Folder Name (relative to base_dir)
structure_map = {
    # Shop
    "shop.html": "shop",
    "shop-type-1.html": "shop",
    "shop-type-2.html": "shop",
    "shop-type-3.html": "shop",
    "shop-single.html": "shop",
    "product-details.html": "shop",
    "cart.html": "shop",
    "checkout.html": "shop",
    "wishlist.html": "shop",
    "my-account.html": "shop",
    
    # Blog
    "blog.html": "blog",
    "blog-details.html": "blog",
    "blog-listing.html": "blog",
    "blog-left-sidebar.html": "blog",
    "blog-right-sidebar.html": "blog",
    "blog-without-sidebar.html": "blog",
    
    # Events
    "events.html": "events",
    "event-details.html": "events",
    
    # Utilities/Pages
    "about.html": "pages",
    "contact.html": "pages",
    "faq.html": "pages",
    "login.html": "pages",
    "404.html": "pages",
    "rtl-demo.html": "pages",
    
    # Home Variations
    "home-2.html": "home_layouts",
    "home-3.html": "home_layouts",
    
    # Root (Explicitly listed to be safe)
    "index.html": "."
}

# Create directories
unique_folders = set(structure_map.values())
for folder in unique_folders:
    if folder != ".":
        path = os.path.join(base_dir, folder)
        os.makedirs(path, exist_ok=True)
        print(f"Ensured directory exists: {folder}")

# Function to calculate new relative path
def calculate_new_link(source_file, original_link):
    # source_file: The filename currently being processed (e.g., 'cart.html')
    # original_link: The content of the href/src attribute (e.g., 'index.html', 'css/style.css', 'http://...')
    
    # Ignore absolute links, anchors, javascript, mailto, etc.
    if original_link.startswith(("http:", "https:", "#", "mailto:", "tel:", "javascript:", "data:")):
        return original_link
    
    # Strip potential queries/fragments for mapping check but keep them for final string
    clean_link = original_link.split('?')[0].split('#')[0]
    suffix = original_link[len(clean_link):]
    
    source_folder = structure_map.get(source_file, ".")
    
    # Case 1: Linking to one of our managed HTML files
    if clean_link in structure_map:
        target_folder = structure_map[clean_link]
        
        if source_folder == target_folder:
            # Same folder, link is just filename
            return clean_link + suffix
        
        if source_folder == ".":
            # Root to Subfolder
            return f"{target_folder}/{clean_link}{suffix}"
        
        if target_folder == ".":
            # Subfolder to Root
            return f"../{clean_link}{suffix}"
            
        # Subfolder to Subfolder (e.g. shop/cart.html -> pages/about.html)
        return f"../{target_folder}/{clean_link}{suffix}"

    # Case 2: Linking to assets (css, js, images) or unmanaged files
    # If we are in the root, leave it alone.
    if source_folder == ".":
        return original_link
        
    # If we are in a subfolder, we likely need to prepend "../"
    # ONLY if it doesn't already look like a relative path going up
    if not original_link.startswith("../"):
        return f"../{original_link}"
        
    return original_link

# Regex to find href and src attributes
# Matches href="value" or src="value"
link_pattern = re.compile(r'(href|src)=["\']([^"\']+)["\']')

# Process files
files_processed = 0

for filename, target_folder in structure_map.items():
    source_path = os.path.join(base_dir, filename)
    
    # Check if file exists (it should, but safety first)
    if not os.path.exists(source_path):
        print(f"Skipping {filename}, not found.")
        continue
        
    print(f"Processing {filename}...")
    
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Python's re.sub with a callback function
    def replace_match(match):
        attr = match.group(1) # href or src
        link = match.group(2) # the url
        new_link = calculate_new_link(filename, link)
        return f'{attr}="{new_link}"'
        
    new_content = link_pattern.sub(replace_match, content)
    
    # Determine output path
    dest_path = os.path.join(base_dir, target_folder, filename)
    
    # Write to destination
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    # If we moved the file (i.e., not index.html remaining in root), delete old one
    if target_folder != ".":
        os.remove(source_path)
        
    files_processed += 1

print(f"Organization complete. Processed {files_processed} files.")
