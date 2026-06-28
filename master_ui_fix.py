import os
import re

# Comprehensive list of HTML files to update
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

# Master CSS block to ensure high-contrast white text for Ticker and Omnisend
MASTER_UI_FIX = """
        /* Ticker White Text Fix */
        .ticker, .ticker span {
            color: white !important;
            opacity: 1 !important;
        }

        /* Omnisend Form White Text Fix - Comprehensive */
        div[id*="omnisend"] *, 
        div[class*="omnisend"] *,
        .omnisend-form-container *,
        input::placeholder {
            color: white !important;
            opacity: 1 !important;
        }
        
        input:-webkit-autofill,
        input:-webkit-autofill:hover, 
        input:-webkit-autofill:focus {
            -webkit-text-fill-color: white !important;
            transition: background-color 5000s ease-in-out 0s;
        }
"""

for file_path in files:
    if not os.path.exists(file_path): continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Inject/Update the master fix in the <style> tag
    if '</style>' in content:
        # Check if already partially injected, if so, replace. Else, append before closing </style>
        if '/* Ticker White Text Fix */' in content:
            # Replace old block
            content = re.sub(r'/\* Ticker White Text Fix \*/.*?/\* End Ticker Fix \*/', '', content, flags=re.DOTALL)
            content = content.replace('</style>', f'/* Ticker White Text Fix */{MASTER_UI_FIX}/* End Ticker Fix */</style>')
        else:
            content = content.replace('</style>', f'/* Ticker White Text Fix */{MASTER_UI_FIX}/* End Ticker Fix */</style>')
    
    # 2. Hard-clean the .ticker inline or class if found
    content = re.sub(r'color:rgba\(0,194,168,0\.6\)', 'color: white !important', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Finalized Master UI Style in {file_path}")

print("Master UI Fix push complete.")
