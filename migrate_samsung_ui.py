import os
import re

repair_dir = 'repair'
samsung_files = [f for f in os.listdir(repair_dir) if f.startswith('samsung-galaxy-')]

sidebar_html = """
<div class="lg:col-span-4">
<div class="sticky top-32 space-y-8">
<div class="sidebar-card bg-teal-900 text-white border-none shadow-xl">
<p class="eyebrow text-amber mb-2 block">Premium Option</p>
<h3 class="font-serif text-2xl mb-3 text-white">Self Repair Service</h3>
<p class="text-sm text-white/70 mb-6 leading-relaxed">Fix your Galaxy at home. Engineer-approved kits with professional tools.</p>
<a href="https://selfrepairkit.com.au" class="btn btn-primary w-full justify-center">Browse Kits</a>
</div>
<div class="sidebar-card">
<h3 class="font-bold text-lg mb-4 flex items-center gap-2 text-ink"><i data-lucide="map-pin" class="w-5 h-5 text-teal"></i> Local Shops</h3>
<p class="text-xs text-muted mb-4">Find a verified Australian repairer in your city for same-day service.</p>
<a href="../locations.html" class="text-teal font-bold text-xs hover:underline flex items-center gap-1 uppercase tracking-widest">Find a Shop <i data-lucide="chevron-right" class="w-3 h-3"></i></a>
</div>
</div>
</div>
"""

for filename in samsung_files:
    path = os.path.join(repair_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has a sidebar
    if 'lg:col-span-8' in content:
        print(f"Skipping {filename} - already has sidebar grid.")
        continue

    # Identify the pricing section
    # <section class="bg-white border-b border-line">
    # <div class="max-w-6xl mx-auto px-6 md:px-8 py-16 md:py-20">
    
    pattern = r'(<section class="bg-white border-b border-line">\s*<div class="max-w-6xl mx-auto px-6 md:px-8 py-16 md:py-20">)(.*?)(</div>\s*</section>)'
    
    def replace_pricing(match):
        prefix = match.group(1)
        inner = match.group(2)
        suffix = match.group(3)
        
        new_inner = f"""
<div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
<div class="lg:col-span-8">
{inner}
</div>
{sidebar_html}
</div>
"""
        return prefix + new_inner + suffix

    new_content = re.sub(pattern, replace_pricing, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename} to two-column layout.")
    else:
        print(f"Could not find pricing section in {filename}.")
