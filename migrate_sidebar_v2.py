import os
import re

repair_dir = 'repair'
target_files = [f for f in os.listdir(repair_dir) if f.endswith('.html') and f not in ['index.html', 'model.html', 'phone-repair-costs-australia.html']]

def get_sidebar(filename):
    device = "Galaxy" if "samsung" in filename else "iPhone" if "iphone" in filename else "Pixel" if "pixel" in filename else "phone"
    return f"""
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

for filename in target_files:
    path = os.path.join(repair_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Look for the section containing the pricing table
    # This pattern is more flexible to catch "Component Price Index" and different section structures
    section_pattern = r'(<section[^>]*>.*?(?:Pricing|Component Price Index).*?<table.*?</section>)'
    
    match_section = re.search(section_pattern, content, re.DOTALL)
    if not match_section:
        print(f"Skipping {filename} - no pricing section found.")
        continue

    target_section = match_section.group(1)
    
    # Identify the inner container (max-w-6xl or max-w-7xl)
    container_pattern = r'(<(section|div) [^>]*class="[^"]*max-w-[67]xl[^"]*"[^>]*>)(.*?)(</\2>)'
    
    match_container = re.search(container_pattern, target_section, re.DOTALL)
    if not match_container:
        print(f"Skipping {filename} - could not identify max-width container.")
        continue
        
    prefix = match_container.group(1)
    inner = match_container.group(3)
    suffix = match_container.group(4)
    
    # Extract original content if it already has a two-column or flex layout
    inner_content = inner.strip()
    if 'flex flex-col lg:flex-row' in inner_content:
        flex_match = re.search(r'<div class="lg:w-2/3">(.*?)</div>\s*<aside', inner_content, re.DOTALL)
        if flex_match:
            inner_content = flex_match.group(1).strip()
    elif 'lg:col-span-8' in inner_content:
        span_match = re.search(r'<div class="lg:col-span-8">(.*?)</div>\s*<div class="lg:col-span-4"', inner_content, re.DOTALL)
        if span_match:
            inner_content = span_match.group(1).strip()

    # Normalize max-w to 6xl and ensure consistent classes
    new_prefix = prefix.replace('max-w-7xl', 'max-w-6xl')

    new_container = f"""{new_prefix}
<div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
<div class="lg:col-span-8">
{inner_content}
</div>
{get_sidebar(filename)}
</div>
{suffix}"""

    new_section = target_section.replace(match_container.group(0), new_container)
    new_content = content.replace(target_section, new_section)
    
    # S24 Ultra breadcrumb fix
    if filename == 'samsung-galaxy-s24-ultra.html':
        new_content = new_content.replace('<a href="../brands.html" class="ed-link hover:text-teal">Brands</a><span>/</span><a href="../brands.html" class="ed-link hover:text-teal">Brands</a>', '<a href="../brands.html" class="ed-link hover:text-teal">Brands</a>')
        new_content = new_content.replace('<span>/</span><a href="../brands.html" class="ed-link hover:text-teal">Samsung</a>', '<span>/</span><a href="../brands/samsung.html" class="ed-link hover:text-teal">Samsung</a>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully migrated {filename} to sidebar layout.")
