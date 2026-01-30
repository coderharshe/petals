import os
import re
import urllib.request
import urllib.parse
from urllib.error import URLError

BASE_URL = "https://wdtregalia.wpengine.com"
HTML_FILE = "index.html"

# Ensure directories exist
for folder in ["css", "js", "images", "fonts"]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def download_file(url, local_path):
    # Handle protocol relative URLs
    if url.startswith("//"):
        url = "https:" + url
    
    if not url.startswith("http"):
        return False

    try:
        # Don't download if exists
        if os.path.exists(local_path):
            return True
            
        print(f"Downloading {url} to {local_path}...")
        # Add headers to mimic browser
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )
        with urllib.request.urlopen(req) as response:
            with open(local_path, "wb") as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def sanitize_links(content):
    # Map external pages to local files based on previous exploration
    # .../shop/ -> shop/shop.html
    # .../blog/ -> blog/blog.html
    # .../art-events/ -> events/events.html
    # .../about/ -> pages/about.html
    # .../contact/ -> pages/contact.html
    # .../faq/ -> pages/faq.html
    # .../login-page/ -> pages/login.html
    # .../404error -> pages/404.html
    
    replacements = [
        (r'https://wdtregalia\.wpengine\.com/shop/?', 'shop/shop.html'),
        (r'https://wdtregalia\.wpengine\.com/blog/?', 'blog/blog.html'),
        (r'https://wdtregalia\.wpengine\.com/art-events/?', 'events/events.html'),
        (r'https://wdtregalia\.wpengine\.com/about/?', 'pages/about.html'),
        (r'https://wdtregalia\.wpengine\.com/contact/?', 'pages/contact.html'),
        (r'https://wdtregalia\.wpengine\.com/faq/?', 'pages/faq.html'),
        (r'https://wdtregalia\.wpengine\.com/login-page/?', 'pages/login.html'),
        (r'https://wdtregalia\.wpengine\.com/404error/?', 'pages/404.html'),
        (r'https://wdtregalia\.wpengine\.com/home-2/?', 'index.html'),
        (r'https://wdtregalia\.wpengine\.com/?', 'index.html'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
    return content

def process_assets(content):
    # Regex for assets
    # CSS: <link ... href="...">
    # JS: <script ... src="...">
    # Images: <img ... src="..."> <img ... srcset="...">
    
    # We will look for anything starting with the base url or protocol relative
    # But specifically targeting extensions for cleaner separation
    
    # 1. Stylesheets
    link_pattern = r'(<link[^>]+href=["\'])([^"\']+)(["\'][^>]*>)'
    
    def replace_css(match):
        prefix, url, suffix = match.groups()
        if "wp-content" in url or "fonts.googleapis" in url: # basic filter
            # Simplify filename
            filename = os.path.basename(urllib.parse.urlparse(url).path)
            if not filename.endswith(".css"): 
                # maybe a query string, ignore or handle? 
                # If it's a google font, it might not end in css
                filename = "style_" + str(abs(hash(url))) + ".css"
            
            local_path = f"css/{filename}"
            if download_file(url, local_path):
                return f'{prefix}{local_path}{suffix}'
        return match.group(0)

    content = re.sub(link_pattern, replace_css, content)

    # 2. Scripts
    script_pattern = r'(<script[^>]+src=["\'])([^"\']+)(["\'][^>]*>)'
    
    def replace_js(match):
        prefix, url, suffix = match.groups()
        if "wp-content" in url or "wp-includes" in url:
            filename = os.path.basename(urllib.parse.urlparse(url).path)
            if not filename.endswith(".js"):
                filename = "script_" + str(abs(hash(url))) + ".js"
            
            local_path = f"js/{filename}"
            if download_file(url, local_path):
                return f'{prefix}{local_path}{suffix}'
        return match.group(0)

    content = re.sub(script_pattern, replace_js, content)

    # 3. Images (src and data-src)
    img_pattern = r'(src=["\'])([^"\']+)(["\'])'
    
    def replace_img(match):
        prefix, url, suffix = match.groups()
        if BASE_URL in url:
            filename = os.path.basename(urllib.parse.urlparse(url).path)
            # handle empty filename (root)
            if not filename: return match.group(0)
            
            local_path = f"images/{filename}"
            if download_file(url, local_path):
                return f'{prefix}{local_path}{suffix}'
        return match.group(0)
    
    content = re.sub(img_pattern, replace_img, content)
    
    # 4. Images in srcset
    # srcset="url 100w, url 200w"
    srcset_pattern = r'(srcset=["\'])([^"\']+)(["\'])'
    
    def replace_srcset(match):
        prefix, srcset_val, suffix = match.groups()
        new_parts = []
        for part in srcset_val.split(','):
            part = part.strip()
            if not part: continue
            
            subparts = part.split(' ')
            url = subparts[0]
            desc = ' '.join(subparts[1:]) if len(subparts) > 1 else ''
            
            if BASE_URL in url:
                filename = os.path.basename(urllib.parse.urlparse(url).path)
                local_path = f"images/{filename}"
                download_file(url, local_path)
                new_parts.append(f"{local_path} {desc}")
            else:
                new_parts.append(part)
        
        return f'{prefix}{", ".join(new_parts)}{suffix}'

    content = re.sub(srcset_pattern, replace_srcset, content)

    return content

def remove_redundant_nav(content):
    # Remove "Home-1", "Home-2", "Home-3", "RTL Version" menu items
    # These are usually in <li> items.
    
    # We can try to use regex to find and remove specific list items containing these texts.
    # This is risky with regex but we can try to be specific.
    
    to_remove = [
        "Home-1", "Home-2", "Home-3", "RTL Version"
    ]
    
    for item in to_remove:
        # Pattern looks for <li ...> ... <a ...>Item</a> ... </li>
        # This is hard with regex since <li> can be nested.
        # But looking at the source, they seem to be simple items.
        
        # Simple approach: Replace the link text with empty or remove the <li> if possible.
        # Let's just create a cleaner regex for the specific HTML structure we saw
        # <li class="..."><a ...><span data-text="Home-1">Home-1</span></a></li>
        
        pattern = r'<li[^>]*>.*?<span[^>]*>' + re.escape(item) + r'</span>.*?</li>'
        content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
        
    return content

with open(HTML_FILE, "r", encoding="utf-8") as f:
    content = f.read()

print("Sanitizing links...")
content = sanitize_links(content)

print("Processing assets...")
content = process_assets(content)

print("Cleaning navigation...")
content = remove_redundant_nav(content)

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print("Done.")
