import os
import re

# Configuration
TARGET_DIR = r"C:\Users\dell lattitude\.accio\accounts\1728917364\agents\MID-29917364U1780312-3FBB0C-8987-5BD472\project\repairrange-final-push"

NEW_STYLE = """<style>
        :root { --rr-teal-900:#0c4a45; --rr-teal-700:#0F766E; --rr-amber-600:#d97706; --rr-amber-500:#F59E0B; --rr-ink:#1C1917; --rr-muted:#78716C; --rr-line:#D6D3D1; --rr-paper:#F3F4F1; --rr-paper-2:#E7E5E4; --rr-hero:#E7E9E2; }
        html { scroll-behavior: smooth; }
        body { font-family:'Inter',system-ui,sans-serif; color:var(--rr-ink); background:var(--rr-paper); -webkit-font-smoothing:antialiased; }
        .font-serif { font-family:'Fraunces','Iowan Old Style','Palatino',serif; font-feature-settings:'ss01'; }
        .font-mono { font-family:'JetBrains Mono',ui-monospace,monospace; }
        .text-teal{color:var(--rr-teal-700);} .bg-teal-900{background:var(--rr-teal-900);}
        .text-amber{color:var(--rr-amber-600);} .bg-amber{background:var(--rr-amber-500);}
        .text-ink{color:var(--rr-ink);} .text-muted{color:var(--rr-muted);} .border-line{border-color:var(--rr-line);}
        .bg-paper{background:var(--rr-paper);} .bg-paper-2{background:var(--rr-paper-2);}
        .display { font-family:'Fraunces',serif; font-weight:400; letter-spacing:-0.025em; line-height:1.05; font-variation-settings:'opsz' 144; }
        .eyebrow { font-size:0.75rem; font-weight:600; letter-spacing:0.18em; text-transform:uppercase; color:var(--rr-teal-700); }
        .header-sticky { backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px); background:rgba(255,255,255,0.9); }
        .ed-link { background-image:linear-gradient(currentColor,currentColor); background-position:0 100%; background-repeat:no-repeat; background-size:0% 1px; transition:background-size 220ms ease; }
        .ed-link:hover { background-size:100% 1px; }
        .btn { display:inline-flex; align-items:center; gap:0.5rem; padding:0.75rem 1.25rem; font-weight:600; font-size:0.9375rem; transition:all 200ms ease; border-radius:2px; }
        .btn-primary { background:var(--rr-amber-500); color:var(--rr-ink); box-shadow:0 1px 0 var(--rr-amber-600); }
        .btn-primary:hover { background:var(--rr-amber-600); color:white; transform:translateY(-1px); box-shadow:0 4px 0 var(--rr-amber-600); }
        .card, .post-card, .sidebar-card { background:white; border:1px solid var(--rr-line); transition:all 300ms ease; display:block; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); }
        .card:hover, .post-card:hover { border-color:var(--rr-ink); transform:translateY(-4px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.1); }
        .bg-mesh-hero { background-color: var(--rr-hero); background-image: radial-gradient(rgba(15, 118, 110, 0.15) 1.5px, transparent 0); background-size: 32px 32px; border-bottom: 2px solid var(--rr-line); }
        .mobile-menu { transition:all 300ms ease-in-out; }
        @media (max-width: 768px) { .mobile-menu.hidden{display:none;} .mobile-menu:not(.hidden){display:block;} }
    </style>"""

def update_html_files():
    count = 0
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 1. Update Style Block
                # Find <style>...</style> and replace
                content = re.sub(r'<style>.*?</style>', NEW_STYLE, content, flags=re.DOTALL)

                # 2. Update Hero Section Class
                # Many pages use <section class="bg-paper border-b border-line"> or <section class="bg-mesh..."> for hero
                # We want to replace the FIRST occurrence of a hero-like section with bg-mesh-hero
                content = re.sub(r'<section class="(bg-paper|bg-mesh|bg-mesh-2)[^"]*"', r'<section class="bg-mesh-hero"', content, count=1)

                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
    
    print(f"Successfully updated {count} files with the new standout UI theme.")

if __name__ == "__main__":
    update_html_files()
