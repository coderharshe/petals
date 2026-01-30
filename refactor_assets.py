
import re
import os

HTML_FILE = r"e:\petals\index.html"
CSS_DIR = r"e:\petals\css"
CSS_OUT = os.path.join(CSS_DIR, "cleaned_styles.css")

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def refactor():
    if not os.path.exists(HTML_FILE):
        print(f"File not found: {HTML_FILE}")
        return

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- Extract CSS ---
    # Find all <style> tags (handling attributes like id, type)
    # Regex: <style[^>]*>(.*?)</style> with dotall
    style_pattern = re.compile(r'<style[^>]*>(.*?)</style>', re.DOTALL | re.IGNORECASE)
    
    extracted_css = []
    
    def replace_style(match):
        css_code = match.group(1).strip()
        if css_code:
            extracted_css.append(f"/* Extracted style */\n{css_code}")
        return "" # Remove the tag

    new_content = style_pattern.sub(replace_style, content)

    ensure_dir(CSS_OUT)
    
    if extracted_css:
        with open(CSS_OUT, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(extracted_css))
        print(f"Extracted {len(extracted_css)} style blocks to {CSS_OUT}")
        
        # Insert Link in HEAD
        # Try to find </head>
        head_end_idx = new_content.lower().find('</head>')
        if head_end_idx != -1:
            link_tag = f'<link rel="stylesheet" href="css/cleaned_styles.css" type="text/css" media="all" />\n'
            new_content = new_content[:head_end_idx] + link_tag + new_content[head_end_idx:]
        else:
            print("Warning: No </head> tag found. Appending to top.")
            link_tag = f'<link rel="stylesheet" href="css/cleaned_styles.css" type="text/css" media="all" />\n'
            new_content = link_tag + new_content

    # Write back HTML
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Refactoring complete.")

if __name__ == "__main__":
    refactor()
