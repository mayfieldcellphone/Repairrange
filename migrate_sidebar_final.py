import os
import re

repair_dir = 'repair'
target_files = [f for f in os.listdir(repair_dir) if f.endswith('.html') and f not in ['index.html', 'model.html', 'phone-repair-costs-australia.html']]

sidebar_html_template = """
<div class="lg:col-span-4">
<div class="sticky top-32 space-y-8">
<div class="sidebar-card bg-teal-900 text-white border-none shadow-xl">
<p class="eyebrow text-amber mb-2 block font-bold">Premium Option</p>
<h3 class="font-serif text-2xl mb-3 text-white">Self Repair Service</h3>
<p class="text-sm text-white/70 mb-6 leading-relaxed">Fix your {device} at home. Engineer-approved kits with professional tools.</p>
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

def get_sidebar(filename):
    if 'samsung' in filename: device = 'Galaxy'
    elif 'iphone' in filename: device = 'iPhone'
    elif 'pixel' in filename: device = 'Pixel'
    else: device = 'phone'
    return sidebar_html_template.format(device=device)

for filename in target_files:
    path = os.path.join(repair_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    found = False
    sections = re.findall(r'<section.*?</section>', content, re.DOTALL)
    for section in sections:
        if ('Pricing' in section or 'Component Price Index' in section) and '<table' in section:
            # Match! Identify inner container
            container_match = re.search(r'(<(section|div) [^>]*class="([^"]*max-w-[67]xl[^"]*)"[^>]*>)(.*?)(</\2>)', section, re.DOTALL)
            if container_match:
                prefix = container_match.group(1)
                inner = container_match.group(4)
                suffix = container_match.group(5)
                
                # Cleanup inner content from previous layouts
                inner_content = inner.strip()
                # Check for existing flex layout
                flex_match = re.search(r'<div class="lg:w-2/3">(.*?)</div>\s*<aside', inner_content, re.DOTALL)
                if flex_match:
                    inner_content = flex_match.group(1).strip()
                # Check for existing grid layout (from my previous failed runs)
                grid_match = re.search(r'<div class="lg:col-span-8">(.*?)</div>\s*<div class="lg:col-span-4"', inner_content, re.DOTALL)
                if grid_match:
                    inner_content = grid_match.group(1).strip()
                
                new_container = prefix + '\n<div class="grid grid-cols-1 lg:grid-cols-12 gap-12">\n<div class="lg:col-span-8">\n' + inner_content + '\n</div>\n' + get_sidebar(filename) + '\n</div>\n' + suffix
                new_section = section.replace(container_match.group(0), new_container)
                
                # Normalize max-w to 6xl and standardize classes
                new_section = new_section.replace('max-w-7xl', 'max-w-6xl')
                
                content = content.replace(section, new_section)
                found = True
                break

    if found:
        # S24 Ultra breadcrumb fix
        if filename == 'samsung-galaxy-s24-ultra.html':
            content = content.replace('<a href="../brands.html" class="ed-link hover:text-teal">Brands</a><span>/</span><a href="../brands.html" class="ed-link hover:text-teal">Brands</a>', '<a href="../brands.html" class="ed-link hover:text-teal">Brands</a>')
            content = content.replace('<span>/</span><a href="../brands.html" class="ed-link hover:text-teal">Samsung</a>', '<span>/</span><a href="../brands/samsung.html" class="ed-link hover:text-teal">Samsung</a>')

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully migrated {filename}")
    else:
        print(f"Could not migrate {filename}")
