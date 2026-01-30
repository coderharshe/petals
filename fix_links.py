import os
import re

html_path = r"e:\petals\index.html"
css_dir = r"e:\petals\css"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Regex to find links
# <link rel='stylesheet' ... href='URL' ...>
# We want to capture the URL.
regex = r"<link[^>]+rel=['\"]stylesheet['\"][^>]+href=['\"]([^'\"]+)['\"][^>]*>"

matches = re.finditer(regex, content, re.IGNORECASE)

new_content = content

for match in matches:
    url = match.group(1)
    filename = url.split("?")[0].split("/")[-1]
    local_path = os.path.join(css_dir, filename)
    
    # Check if we downloaded it
    if os.path.exists(local_path):
        print(f"Replacing {url} with css/{filename}")
        new_content = new_content.replace(url, f"css/{filename}")
    else:
        print(f"Warning: {filename} not found locally for {url}")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Done updating HTML.")
