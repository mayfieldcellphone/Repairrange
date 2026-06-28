import os
import re

# Directory containing the RepairRange project
root_dir = r"C:/Users/dell lattitude/.accio/accounts/1728917364/agents/MID-18917364U1780341-3FBB0C-1458-56E97A/project"

# Walk through all directories and files
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            
            # Use fixed absolute path for the CSS or relative
            # Since these sites are typically hosted as a single flat dir or small hierarchy
            # I'll use relative pathing for better portability
            rel_root = root.replace(root_dir, "").strip(os.sep)
            depth = rel_root.count(os.sep) + (1 if rel_root else 0)
            css_path = ("../" * depth) + "css/main.css"
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except:
                print(f"Skipped {file_path} (could not read).")
                continue
            
            new_link = f'<link rel="stylesheet" href="{css_path}">'
            new_content = re.sub(r'<script src="https://cdn.tailwindcss.com"></script>', new_link, content)
            
            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {file_path} with static CSS link.")
            else:
                pass # Already updated or no tailwind

print("Finished updating HTML files in RepairRange project.")
