import os
import re

# Directory containing the selfrepairkit project
root_dir = "selfrepairkit"

# Walk through all directories and files
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 1. Force Header Background to Pure Black
            # Looking for current nav background patterns
            new_content = re.sub(r'bg-\[#\w+\](?:/95)?', 'bg-black', content)
            new_content = re.sub(r'bg-black/95', 'bg-black', new_content)
            
            # 2. Ensure navbar links are white
            new_content = re.sub(r'text-white/70', 'text-white', new_content)
            
            # 3. Specific fix for the logo slogan mt (increase spacing if needed)
            
            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {file_path}")

print("Header background updates complete.")
