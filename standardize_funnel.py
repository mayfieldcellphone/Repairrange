import os
import re

# Configuration
REPAIR_DIRS = [
    r"C:\Users\dell lattitude\.accio\accounts\1728917364\agents\MID-29917364U1780312-3FBB0C-8987-5BD472\project\repair",
    r"C:\Users\dell lattitude\.accio\accounts\1728917364\agents\MID-29917364U1780312-3FBB0C-8987-5BD472\project\repairrange-final-push\repair"
]

def standardize_funnel():
    count = 0
    for target_dir in REPAIR_DIRS:
        if not os.path.exists(target_dir):
            continue
            
        for file in os.listdir(target_dir):
            if not file.endswith(".html") or file in ["phone-repair-costs-australia.html", "google-pixel-repair-guide.html"]:
                continue
                
            path = os.path.join(target_dir, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 1. Standardize the Hero Grid (lg:col-span-12)
            content = re.sub(r'<div class="lg:col-span-8">\s*<nav', r'<div class="lg:col-span-12">\n                <nav', content)
            
            # 2. Add the 3-card stat grid if missing or outdated
            # Extract the market average value if possible
            mkt_avg = re.search(r'Market Average</p>\s*<p class="display[^>]*>(.*?)</p>', content)
            mkt_val = mkt_avg.group(1) if mkt_avg else "$259"
            
            stat_grid = f"""<div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-10">
                    <div class="card p-6 border-l-4 border-teal-700">
                        <p class="text-[10px] uppercase font-bold text-muted mb-1">Market Avg</p>
                        <p class="text-2xl font-bold text-ink">{mkt_val}</p>
                        <p class="text-[10px] text-muted">Screen Repair</p>
                    </div>
                    <div class="card p-6 border-l-4 border-amber-500">
                        <p class="text-[10px] uppercase font-bold text-muted mb-1">DIY Save</p>
                        <p class="text-2xl font-bold text-amber-600">-$100</p>
                        <p class="text-[10px] text-muted">Using Toolkits</p>
                    </div>
                    <div class="card p-6 border-l-4 border-ink">
                        <p class="text-[10px] uppercase font-bold text-muted mb-1">Repair Time</p>
                        <p class="text-2xl font-bold text-ink">45m</p>
                        <p class="text-[10px] text-muted">Aussie Bench Avg</p>
                    </div>
                </div>"""
            
            # Replace the old max-w-sm div or specific market average block
            content = re.sub(r'<div class="max-w-sm">\s*<div class="bg-white border border-line p-8 rounded-2xl shadow-xl">.*?</div>\s*</div>', stat_grid, content, flags=re.DOTALL)

            # 3. Handle Sidebar Move (Next to Table)
            # Find the Self Repair Kit card
            card_match = re.search(r'(<div class="sidebar-card bg-teal-900.*?>.*?selfrepairkit\.com\.au.*?</div>)', content, re.DOTALL)
            if card_match:
                kit_card = card_match.group(1)
                content = content.replace(kit_card, "") # Remove from old spot
                
                # Identify the sidebar next to the table
                sidebar_pos = content.find('<div class="sticky top-32 space-y-6">')
                if sidebar_pos == -1: sidebar_pos = content.find('<div class="sticky top-32 space-y-8">')
                
                if sidebar_pos != -1:
                    insertion_point = content.find('>', sidebar_pos) + 1
                    content = content[:insertion_point] + "\n                " + kit_card + content[insertion_point:]

            # 4. Standardize Pricing Table Rows (Add Buy Kit links if missing)
            # This is complex, we target the specific "DIY Kit" column cells
            content = re.sub(
                r'(\d+)</td>\s*<td class="px-5 py-4 font-mono tnum text-muted text-right hidden md:table-cell">(\$[\d\–\-]+)</td>', 
                r'\1</td><td class="text-right"><div class="flex flex-col items-end gap-1"><span class="font-mono font-bold text-teal-700">\2</span><span class="savings-badge">Save ~$60</span><a href="https://selfrepairkit.com.au" class="text-[10px] font-bold text-amber-600 hover:underline uppercase mt-2">Buy Kit →</a></div></td>', 
                content
            )

            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
            
    print(f"Standardized {count} guide pages to the high-conversion iPhone 17 template.")

if __name__ == "__main__":
    standardize_funnel()
