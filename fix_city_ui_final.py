import os
import re

TARGET_DIR = r"C:\Users\dell lattitude\.accio\accounts\1728917364\agents\MID-29917364U1780312-3FBB0C-8987-5BD472\project\locations"

INDUSTRIAL_STYLE = """<style>
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
    .btn-primary { background:var(--rr-amber-500); color:var(--rr-ink); box-shadow: 4px 4px 0 var(--rr-amber-600); }
    .btn-primary:hover { background:var(--rr-amber-600); color:white; transform:translate(1px, 1px); box-shadow: 2px 2px 0 var(--rr-amber-600); }
    
    .card, .sidebar-card, .shadow-box { 
        background:white; border:1px solid var(--rr-ink); transition:all 300ms ease; display:block; 
        box-shadow: 6px 6px 0px rgba(0, 0, 0, 0.1) !important; 
        border-radius: 4px;
        padding: 2rem;
    }
    .card:hover { 
        transform:translate(-2px, -2px); 
        box-shadow: 10px 10px 0px rgba(15, 118, 110, 0.2) !important; 
    }
    
    .bg-mesh-hero { 
        background-color: var(--rr-hero); 
        background-image: radial-gradient(rgba(15, 118, 110, 0.15) 1.5px, transparent 0); 
        background-size: 32px 32px; 
        border-bottom: 2px solid var(--rr-ink); 
    }

    /* REFINED PRICE TABLE - INDUSTRIAL LOOK */
    .price-table { width: 100%; border-collapse: separate; border-spacing: 0; background: white; border-radius: 4px; overflow: hidden; border: 1px solid var(--rr-ink); box-shadow: 6px 6px 0px rgba(0,0,0,0.1); }
    .price-table th { background: var(--rr-paper-2); padding: 1.25rem; text-align: left; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; color: var(--rr-ink); border-bottom: 2px solid var(--rr-ink); }
    .price-table td { padding: 1.25rem; border-bottom: 1px solid var(--rr-line); vertical-align: middle; line-height: 1.4; }
    .price-table tr:last-child td { border-bottom: none; }
    .price-table tr:hover { background: var(--rr-paper); }
    
    .model-name { font-weight: 700; color: var(--rr-ink); }
    .price-indie { font-family: ui-monospace, monospace; color: var(--rr-ink); font-weight: 600; }
    .price-diy { font-family: ui-monospace, monospace; color: var(--rr-teal-700); font-weight: 700; }
    .save-badge { display: inline-block; background: #FEF3C7; color: #92400E; font-size: 0.65rem; font-weight: 800; padding: 0.25rem 0.625rem; border-radius: 99px; margin-top: 0.25rem; border: 1px solid #FDE68A; }

    .content-grid { display: grid; grid-template-columns: 1fr; gap: 3rem; }
    @media (min-width: 1024px) { .content-grid { grid-template-columns: 2fr 1fr; } }

    .mobile-menu { transition:all 300ms ease-in-out; }
    @media (max-width: 768px) {
        .price-table th, .price-table td { padding: 0.75rem; font-size: 0.8125rem; }
        .card, .sidebar-card { padding: 1.25rem; }
    }
</style>"""

def fix_city_ui_final():
    count = 0
    for file in os.listdir(TARGET_DIR):
        if not file.endswith(".html"):
            continue
            
        path = os.path.join(TARGET_DIR, file)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Apply Industrial Style (Padding fix, Hard Shadows, Alignment)
        content = re.sub(r'<style>.*?</style>', INDUSTRIAL_STYLE, content, flags=re.DOTALL)
        
        # 2. Fix the Table Structure if broken (ensure it uses proper classes)
        # Replacing simple <table> with our themed .price-table
        content = content.replace('<table>', '<table class="price-table">')
        
        # 3. Sidebar Card Specific Formatting
        # Make the SelfRepairKit card pop in the sidebar
        content = re.sub(r'<div class="sidebar-card bg-teal-900.*?>', '<div class="sidebar-card bg-teal-900 text-white border-none shadow-2xl" style="box-shadow: 8px 8px 0px var(--rr-teal-900) !important;">', content)

        # 4. Clean up the hero section layout one last time
        content = re.sub(r'<section class="bg-mesh-hero">\s*<div class="max-w-6xl mx-auto px-6 md:px-8 py-10 md:py-16">', 
                        '<section class="bg-mesh-hero">\n<div class="max-w-6xl mx-auto px-6 md:px-8 py-12 md:py-20">', content)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
            
    print(f"Successfully applied Industrial UI fix to {count} city pages.")

if __name__ == "__main__":
    fix_city_ui_final()
