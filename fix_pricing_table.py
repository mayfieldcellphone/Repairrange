import os
import re

# Configuration
ROOT_DIR = r"C:\Users\dell lattitude\.accio\accounts\1728917364\agents\MID-29917364U1780312-3FBB0C-8987-5BD472\project"
FINAL_PUSH_PATH = os.path.join(ROOT_DIR, "repairrange-final-push", "repair", "phone-repair-costs-australia.html")
LIVE_ROOT_PATH = os.path.join(ROOT_DIR, "repair", "phone-repair-costs-australia.html")

def fix_pricing_guide():
    # 1. Read the full-data version from final-push
    with open(FINAL_PUSH_PATH, 'r', encoding='utf-8') as f:
        full_content = f.read()

    # 2. Inject the ROBUST CSS and GRID HTML
    # We define the fixed layout here
    robust_css = """
    .card, .post-card, .sidebar-card, .shadow-box { 
        background:white; border:1px solid var(--rr-line); transition:all 300ms ease; display:block; 
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.15), 0 4px 6px -2px rgba(0, 0, 0, 0.1) !important; 
    }
    .card:hover, .post-card:hover { 
        border-color:var(--rr-ink); transform:translateY(-4px); 
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25) !important; 
    }
    .table-container { border: 1px solid var(--rr-line); background: white; border-radius: 4px; overflow: hidden; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
    .model-row { 
        display: grid; 
        grid-template-columns: 2fr 1fr 1fr 1fr; 
        align-items: center; 
        padding: 1rem 1.5rem; 
        border-bottom: 1px solid var(--rr-line); 
        background: white;
    }
    .model-row:last-child { border-bottom: none; }
    .model-row:hover { background: var(--rr-paper); }
    .brand-header { 
        background: var(--rr-paper-2); 
        padding: 0.75rem 1.5rem; 
        font-weight: 800; 
        color: var(--rr-teal-700); 
        text-transform: uppercase; 
        letter-spacing: 0.1em; 
        font-size: 0.7rem; 
        border-bottom: 1px solid var(--rr-line); 
    }
    """
    
    # Insert robust CSS into the style block
    updated_content = re.sub(r'</style>', robust_css + "\n    </style>", full_content)

    # 3. Update the JS render function to match the grid columns
    js_fix = """
    filtered.forEach(m=>{
        const link = m.g ? `<a href="${m.g}.html" style="color:var(--rr-teal-700); font-weight:700;">Full guide &rarr;</a>` : `<a href="model.html?m=${slugify(m.b,m.n)}" style="color:var(--rr-teal-700); font-size:0.75rem;">View pricing</a>`;
        html+=`<div class="model-row">
            <span class="text-sm font-bold text-ink">${m.n}</span>
            <span class="font-mono text-right text-ink">${m.scr}</span>
            <span class="font-mono text-right text-muted">${m.bat}</span>
            <span class="text-right">${link}</span>
        </div>`;
    });
    """
    
    # We find the render loop in the original file and replace it
    updated_content = re.sub(r'filtered\.forEach\(m=>\{.*?\}\);', js_fix, updated_content, flags=re.DOTALL)

    # Write back to LIVE ROOT
    with open(LIVE_ROOT_PATH, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("Pricing Guide Table and Shadows fixed with full data preservation.")

if __name__ == "__main__":
    fix_pricing_guide()
