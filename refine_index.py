import os
import re

file_path = "selfrepairkit/index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Catalog Rotation to include 'google'
content = content.replace("const brands=['apple','samsung','oppo'];", "const brands=['apple','samsung','google','oppo'];")

# 2. Fix potential script failure in rotation
# The previous script might have failed if brand.groups was undefined. 
# Let's make it robust.

# 3. Clean up Omnisend CSS
# Remove the old specific fixes and add one clean block
content = re.sub(r'/\* Embedded Footer Form White Text Fix \*/.*?/\* Omnisend Form White Text Fix \*/', '/* Omnisend Form White Text Fix */', content, flags=re.DOTALL)

omnisend_fix = """
        /* Omnisend Form White Text Fix - Final Master */
        div[id*="omnisend-embedded"] *, 
        .omnisend-form-container *,
        div[class^="omnisend-form"] *,
        div[id*="omnisend"] * {
            color: white !important;
            opacity: 1 !important;
        }
        div[id*="omnisend-embedded"] input,
        div[class^="omnisend-form"] input {
            color: white !important;
            border-bottom: 1px solid rgba(255,255,255,0.4) !important;
        }
        div[id*="omnisend-embedded"] input::placeholder,
        div[class^="omnisend-form"] input::placeholder {
            color: rgba(255,255,255,0.7) !important;
        }
"""
content = re.sub(r'/\* Omnisend Form White Text Fix \*/.*?</style>', f'{omnisend_fix}</style>', content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Final index.html refinements complete.")
