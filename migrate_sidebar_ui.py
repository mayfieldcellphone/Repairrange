import os
import re

repair_dir = 'repair'
# List all files that need the sidebar update
target_files = [f for f in os.listdir(repair_dir) if f.endswith('.html') and f not in ['index.html', 'model.html', 'phone-repair-costs-australia.html']]

sidebar_html = """
<div class="lg:col-span-4">
<div class="sticky top-32 space-y-8">
<div class="sidebar-card bg-teal-900 text-white border-none shadow-xl">
<p class="eyebrow text-amber mb-2 block font-bold">Premium Option</p>
<h3 class="font-serif text-2xl mb-3 text-white">Self Repair Service</h3>
<p class="text-sm text-white/70 mb-6 leading-relaxed">Fix your device at home. Engineer-approved kits with professional tools.</p>
<a href="https://selfrepairkit.com.au" class="btn btn-primary w-full justify-center text-sm font-bold">Shop Repair Kits</a>
</div>
<div class="sidebar-card">
<h3 class="font-bold text-lg mb-4 flex items-center gap-2 text-ink"><i data-lucide="map-pin" class="w-5 h-5 text-teal"></i> Local Shops</h3>
<p class="text-xs text-muted mb-4 leading-relaxed">Find a verified Australian repairer in your city for same-day service.</p>
<a href="../locations.html" class="text-teal font-bold text-xs hover:underline flex items-center gap-1 uppercase tracking-widest">Find a Shop <i data-lucide="chevron-right" class="w-3 h-3"></i></a>
</div>
</div>
</div>
"""

# Adjusting device type for the sidebar text
def get_sidebar(filename):
    if "samsung" in filename: device = "Galaxy"
    elif "iphone" in filename: device = "iPhone"
    elif "pixel" in filename: device = "Pixel"
    else: device = "phone"
    return sidebar_html.replace("your device", f"your {device}")

for filename in target_files:
    path = os.path.join(repair_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'lg:col-span-8' in content and 'lg:col-span-4' in content and 'class="sidebar-card"' in content:
        print(f"Skipping {filename} - already has sidebar in body.")
        continue

    # Identify the pricing section (handling both max-w-6xl and max-w-7xl)
    pattern = r'(<section class="max-w-[67]xl mx-auto px-6 md:px-8 py-16 md:py-2[04]">|<section class="bg-white border-b border-line">\s*<div class="max-w-[67]xl mx-auto px-6 md:px-8 py-16 md:py-2[04]">)(.*?)(</div>\s*</section>)'
    
    match = re.search(pattern, content, re.DOTALL)
    if match:
        prefix = match.group(1)
        inner = match.group(2)
        suffix = match.group(3)
        
        # If it's a flex layout, strip the flex wrappers first
        inner_clean = inner.strip()
        if 'flex flex-col lg:flex-row' in inner_clean:
            # Extract content from lg:w-2/3
            flex_match = re.search(r'<div class="lg:w-2/3">(.*?)</div>\s*<aside', inner_clean, re.DOTALL)
            if flex_match:
                inner_clean = flex_match.group(1).strip()
        
        # Ensure max-w-6xl for consistency
        prefix = prefix.replace('max-w-7xl', 'max-w-6xl')
        
        new_inner = f"""
<div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
<div class="lg:col-span-8">
{inner_clean}
</div>
{get_sidebar(filename)}
</div>
"""
        new_content = content[:match.start()] + prefix + new_inner + suffix + content[match.end():]
        
        # Fix the S24 Ultra breadcrumb if needed
        if filename == 'samsung-galaxy-s24-ultra.html':
            new_content = new_content.replace('<a href="../brands.html" class="ed-link hover:text-teal">Brands</a><span>/</span><a href="../brands.html" class="ed-link hover:text-teal">Brands</a>', '<a href="../brands.html" class="ed-link hover:text-teal">Brands</a>')
            new_content = new_content.replace('<span>/</span><a href="../brands.html" class="ed-link hover:text-teal">Samsung</a>', '<span>/</span><a href="../brands/samsung.html" class="ed-link hover:text-teal">Samsung</a>')

        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename} to two-column layout.")
    else:
        print(f"Could not find pricing section in {filename}.")
