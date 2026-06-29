import os
import re

# Comprehensive list of HTML files to restore
files = [
    "selfrepairkit/index.html",
    "selfrepairkit/shop.html",
    "selfrepairkit/blog.html",
    "selfrepairkit/guides.html",
    "selfrepairkit/privacy.html",
    "selfrepairkit/terms.html",
    "selfrepairkit/shipping.html",
    "selfrepairkit/support.html"
]

# Walk through all directories and files in selfrepairkit
for root, dirs, filenames in os.walk("selfrepairkit"):
    for file in filenames:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Revert the static link back to CDN
            # <link rel="stylesheet" href="...css/main.css"> -> <script src="https://cdn.tailwindcss.com"></script>
            new_content = re.sub(r'<link rel="stylesheet" href="[^"]*css/main.css">', '<script src="https://cdn.tailwindcss.com"></script>', content)
            
            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Restored {file_path}")

print("Restoration complete.")
