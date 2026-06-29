import os
import re

# Configuration for Fixing Mobile Navigation and Header Alignment
TARGET_DIR = r"C:\Users\dell lattitude\.accio\accounts\1728917364\agents\MID-29917364U1780312-3FBB0C-8987-5BD472\project"

MOBILE_MENU_HTML = """
<div class="mobile-menu hidden md:hidden border-t border-line bg-white shadow-xl">
    <div class="max-w-7xl mx-auto px-6 py-4 flex flex-col gap-4 text-sm font-medium">
        <a href="../brands.html" class="hover:text-teal-700">Brands</a>
        <a href="../repair/phone-repair-costs-australia.html" class="hover:text-teal-700">Repairs</a>
        <a href="../fix.html" class="hover:text-teal-700">Troubleshoot</a>
        <a href="../blog.html" class="hover:text-teal-700">Blog</a>
        <a href="../calculator.html" class="text-teal-700 font-bold">Get a Quote</a>
    </div>
</div>
"""

NAV_JS = """
<script>
    if(window.lucide) window.lucide.createIcons();
    document.addEventListener('DOMContentLoaded', () => {
        const btn = document.querySelector('.mobile-menu-button');
        const menu = document.querySelector('.mobile-menu');
        if(btn && menu) {
            btn.addEventListener('click', () => {
                menu.classList.toggle('hidden');
            });
        }
    });
</script>
"""

def fix_mobile_ui():
    count = 0
    for root, dirs, files in os.walk(TARGET_DIR):
        if "node_modules" in root or ".git" in root or "repairrange-final-push" in root:
            continue
            
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 1. Fix Header Alignment (Ensure nav is full width / centered)
                content = content.replace('<nav class="max-w-7xl mx-auto px-6 md:px-8', '<nav class="w-full max-w-7xl mx-auto px-6 md:px-8')
                content = content.replace('<nav class="max-w-6xl mx-auto px-6 md:px-8', '<nav class="w-full max-w-7xl mx-auto px-6 md:px-8')

                # 2. Inject/Update Mobile Menu (Place it after the </nav> tag)
                if '<div class="mobile-menu' not in content:
                    content = content.replace('</nav>', '</nav>\n' + MOBILE_MENU_HTML)
                else:
                    # Update existing menu to ensure consistency
                    content = re.sub(r'<div class="mobile-menu.*?</div>\s*</div>', MOBILE_MENU_HTML, content, flags=re.DOTALL)

                # 3. Fix/Update JavaScript logic
                # Find the existing script or end of body and replace
                if '<script>' in content and 'mobile-menu-button' in content:
                    content = re.sub(r'<script>.*?mobile-menu-button.*?</script>', NAV_JS, content, flags=re.DOTALL)
                else:
                    content = content.replace('</body>', NAV_JS + '\n</body>')

                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                count += 1
    
    print(f"Successfully fixed Mobile Navigation and Header Alignment in {count} files.")

if __name__ == "__main__":
    fix_mobile_ui()
