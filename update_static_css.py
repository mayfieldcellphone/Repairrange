import os
import re

# Directory containing the selfrepairkit project
root_dir = "selfrepairkit"

# Walk through all directories and files
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            
            # Determine the relative path to the CSS folder
            # If in root_dir, it's 'css/main.css'
            # If in a sub-directory, it's '../css/main.css'
            depth = root.replace(root_dir, "").count(os.sep)
            css_path = ("../" * depth) + "css/main.css"
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Find and replace the Tailwind CDN script
            # <script src="https://cdn.tailwindcss.com"></script>
            new_link = f'<link rel="stylesheet" href="{css_path}">'
            
            # Handle different variations of the script tag (e.g. with extra scripts on the same line)
            new_content = re.sub(r'<script src="https://cdn.tailwindcss.com"></script>', new_link, content)
            
            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {file_path} with static CSS link.")
            else:
                print(f"Skipped {file_path} (Tailwind script not found or already replaced).")

print("Finished updating HTML files with static CSS links.")
