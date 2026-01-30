import re
import os

file_path = r'e:\petals\index.html'

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Normalize line endings to \n locally for processing
    content = content.replace('\r\n', '\n')

    # Trim trailing whitespace from each line
    # This also converts lines containing only whitespace to empty strings
    lines = [line.rstrip() for line in content.split('\n')]
    content = '\n'.join(lines)

    # Replace 3 or more newlines with 2 (max 1 blank line between content)
    # This loop collapses multiple consecutive blank lines
    while '\n\n\n' in content:
        content = content.replace('\n\n\n', '\n\n')

    # Ensure the file ends with a single newline
    content = content.strip() + '\n'

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully cleaned up whitespace in {file_path}")

except Exception as e:
    print(f"Error: {e}")
