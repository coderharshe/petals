import os
import re

root_dir = r"e:\petals"
target_name = "Petals"
old_name = "Regalia"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Replace <title>Regalia Site
    content = re.sub(r'<title>Regalia Site', f'<title>{target_name}', content)
    
    # 2. Replace RSS titles
    content = re.sub(r'title="Regalia Site', f'title="{target_name}', content)
    
    # 3. Replace Alt text
    content = re.sub(r'alt="Regalia Site"', f'alt="{target_name}"', content)
    
    # 4. Replace Copyright text
    # Handle multi-line "Regalia Site" with whitespace
    content = re.sub(r'©\s*Regalia\s+Site', f'©{target_name}', content, flags=re.DOTALL | re.IGNORECASE)
    
    # 5. Replace "About Regalia" text
    content = re.sub(r'>About\s+Regalia<', f'>About {target_name}<', content, flags=re.IGNORECASE)
    
    # "Regalia Site" in text (handling newlines)
    content = re.sub(r'Regalia\s+Site', target_name, content, flags=re.IGNORECASE)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
        return True
    return False

count = 0
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".html"):
            if process_file(os.path.join(root, file)):
                count += 1

print(f"Renaming complete. Updated {count} files.")
