import base64
import zlib
import re

def create_kroki_url(diagram_code, diagram_type="mermaid"):
    compressed = zlib.compress(diagram_code.encode('utf-8'))
    b64 = base64.urlsafe_b64encode(compressed).decode('ascii')
    return f"https://kroki.io/{diagram_type}/svg/{b64}"

with open('/home/abd/work/team/media-service/README.md', 'r') as f:
    content = f.read()

# Find all mermaid blocks
mermaid_blocks = re.findall(r'```mermaid\n(.*?)\n```', content, re.DOTALL)

for block in mermaid_blocks:
    url = create_kroki_url(block.strip())
    # Replace the block with the image markdown
    replacement = f"![Diagram]({url})"
    content = content.replace(f"```mermaid\n{block}\n```", replacement)

with open('/home/abd/work/team/media-service/README.md', 'w') as f:
    f.write(content)
print("Updated README.md with Kroki URLs")
