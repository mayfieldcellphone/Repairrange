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
            
            # Update .ticker color to white
            new_content = re.sub(r'(?i)color:rgba\(0,194,168,0\.6\)', 'color: white', content)
            new_content = re.sub(r'(?i)color:\s*rgba\(0,194,168,0\.6\)', 'color: white', new_content)
            
            # Also handle any other variations just in case
            new_content = re.sub(r'(?i)\.ticker\{([^}]*?)color:rgba\(0,194,168,0\.6\)', r'.ticker{\1color: white', new_content)
            
            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {file_path}")

print("Ticker text color updates complete.")
