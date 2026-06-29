import os
import re

TARGET_DIR = r"C:\Users\dell lattitude\.accio\accounts\1728917364\agents\MID-29917364U1780312-3FBB0C-8987-5BD472\project\locations"

MASTER_STYLE = """<style>
    :root { 
        --rr-teal-900:#0c4a45; --rr-teal-700:#0F766E; --rr-amber-600:#d97706; --rr-amber-500:#F59E0B; 
        --rr-ink:#1C1917; --rr-muted:#78716C; --rr-line:#D6D3D1; --rr-paper:#F3F4F1; --rr-paper-2:#E7E5E4; --rr-hero:#E7E9E2; 
    }
    html { scroll-behavior: smooth; }
    body { font-family:'Inter',system-ui,sans-serif; color:var(--rr-ink); background:var(--rr-paper); -webkit-font-smoothing:antialiased; }
    .font-serif { font-family:'Fraunces','Iowan Old Style','Palatino',serif; font-feature-settings:'ss01'; }
    .display { font-family:'Fraunces',serif; font-weight:400; letter-spacing:-0.025em; line-height:1.05; font-variation-settings:'opsz' 144; }
    .eyebrow { font-size:0.75rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:var(--rr-teal-700); }
    
    .header-sticky { backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px); background:rgba(255,255,255,0.9); }
    .btn { display:inline-flex; align-items:center; gap:0.5rem; padding:0.75rem 1.25rem; font-weight:700; font-size:0.9375rem; transition:all 200ms ease; border-radius:4px; }
    .btn-primary { background:var(--rr-amber-500); color:var(--rr-ink); box-shadow: 0 4px 0 var(--rr-amber-600); }
    .btn-primary:hover { background:var(--rr-amber-600); color:white; transform:translateY(-1px); box-shadow: 0 6px 0 var(--rr-amber-600); }
    
    .card, .post-card, .sidebar-card, .shadow-box { 
        background:white; border:1px solid var(--rr-line); transition:all 300ms ease; display:block; 
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); 
        border-radius: 4px;
    }
    .card:hover, .post-card:hover { 
        border-color:var(--rr-ink); transform:translateY(-2px); 
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.15); 
    }
    
    .bg-mesh-hero { 
        background-color: var(--rr-hero); 
        background-image: radial-gradient(rgba(15, 118, 110, 0.1) 1.5px, transparent 0); 
        background-size: 32px 32px; 
        border-bottom: 2px solid var(--rr-line); 
    }

    .price-table { width: 100%; border-collapse: separate; border-spacing: 0; background: white; border-radius: 4px; overflow: hidden; border: 1px solid var(--rr-line); }
    .price-table th { background: var(--rr-paper-2); padding: 1rem; text-align: left; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; color: var(--rr-muted); border-bottom: 1px solid var(--rr-line); }
    .price-table td { padding: 1rem; border-bottom: 1px solid var(--rr-line); vertical-align: middle; }
    
    .save-badge { background: #FEF3C7; color: #92400E; font-size: 0.625rem; font-weight: 800; padding: 0.2rem 0.5rem; border-radius: 99px; margin-left: 0.5rem; }
    
    .content-grid { display: grid; grid-template-columns: 1fr; gap: 3rem; }
    @media (min-width: 1024px) { .content-grid { grid-template-columns: 2fr 1fr; } }

    .mobile-menu { transition:all 300ms ease-in-out; }
</style>"""

def fix_city_pages():
    count = 0
    for file in os.listdir(TARGET_DIR):
        if not file.endswith(".html"):
            continue
            
        path = os.path.join(TARGET_DIR, file)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Force Master Style
        content = re.sub(r'<style>.*?</style>', MASTER_STYLE, content, flags=re.DOTALL)
        
        # 2. Fix Header and Footer paths (since they are in a subfolder)
        content = content.replace('href="index.html"', 'href="../index.html"')
        content = content.replace('href="brands.html"', 'href="../brands.html"')
        content = content.replace('href="fix.html"', 'href="../fix.html"')
        content = content.replace('href="calculator.html"', 'href="../calculator.html"')
        content = content.replace('href="locations.html"', 'href="../locations.html"')
        content = content.replace('href="blog.html"', 'href="../blog.html"')
        
        # 3. Compact Hero and Removal of Mess
        content = re.sub(r'<section class="bg-mesh-hero">.*?(<nav.*?</nav>)', r'<section class="bg-mesh-hero">\n<div class="max-w-6xl mx-auto px-6 md:px-8 py-10 md:py-16">\n\1', content, flags=re.DOTALL)
        
        # 4. Standardize the SelfRepairKit card and move to top of sidebar
        kit_card_match = re.search(r'(<div class="sidebar-card dark.*?</div>)', content, re.DOTALL)
        if kit_card_match:
            kit_card = kit_card_match.group(1)
            # Make the card "standout" with dark theme
            kit_card = kit_card.replace('class="sidebar-card dark', 'class="sidebar-card bg-teal-900 text-white border-none')
            content = content.replace(kit_card_match.group(1), "") # Remove from current pos
            
            # Find the sidebar container
            sidebar_start = content.find('<aside class="sidebar-sticky">')
            if sidebar_start != -1:
                insertion_point = content.find('>', sidebar_start) + 1
                content = content[:insertion_point] + "\n        " + kit_card + content[insertion_point:]

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
            
    print(f"Successfully fixed and unified {count} city location pages.")

if __name__ == "__main__":
    fix_city_pages()
