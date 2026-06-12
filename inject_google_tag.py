import os
import re

TAG_FILE = "google_tag.html"
if not os.path.exists(TAG_FILE):
    print("Google Tag file not found. Skipping injection.")
    exit(0)

with open(TAG_FILE, "r") as f:
    tag_content = f.read()

count = 0
for root, dirs, files in os.walk("public"):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                if "G-CWRGPBDWZD" not in content:
                    new_content = re.sub(r'(<head[^>]*>)', r'\1\n' + tag_content, content, count=1, flags=re.IGNORECASE)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    count += 1
            except Exception as e:
                print(f"Error processing {path}: {e}")

print(f"Successfully injected Google Tag into {count} pages.")
