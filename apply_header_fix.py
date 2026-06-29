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
            
            # 1. Fix Header Background to Black
            new_content = re.sub(r'bg-\[#2b4561\]/95', 'bg-black/95', content)
            new_content = re.sub(r'bg-\[#1e2225\]', 'bg-black', new_content)
            
            # 2. Brighten Footer and Menu Text
            new_content = re.sub(r'text-slate-400', 'text-slate-300', new_content)
            new_content = re.sub(r'text-slate-500', 'text-slate-200', new_content)
            
            # 3. Ensure Navbar links are white (already should be, but let's check text-white/70)
            new_content = re.sub(r'text-white/70', 'text-white', new_content)
            
            # 4. Omnisend White Text Fix (Reinforce)
            if 'omnisend' in new_content:
                if '/* Omnisend Form White Text Fix */' not in new_content:
                    omnisend_css = """
        /* Omnisend Form White Text Fix */
        #omnisend-embedded-v2-6a36649833843eae466e6f9a *,
        #omnisend-embedded-v2-6a36649833843eae466e6f9a input::placeholder,
        div[class^="omnisend-form"] *,
        .omnisend-form-container * {
            color: white !important;
            opacity: 1 !important;
        }
        div[class^="omnisend-form"] input {
            color: white !important;
        }
        """
                    new_content = new_content.replace('</style>', f'{omnisend_css}</style>')

            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated {file_path}")

print("Header background and text color updates complete.")
