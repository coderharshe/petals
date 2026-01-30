import re

with open('pages/about.html', 'r', encoding='utf-8') as f:
    content = f.read()

links = set(re.findall(r'href=["\'](https://wdtregalia.wpengine.com[^"\']*)["\']', content))

print("Found Links:")
for link in sorted(links):
    print(link)
