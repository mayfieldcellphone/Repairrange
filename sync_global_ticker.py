import os
import re

TICKER_HTML = """
    <!-- TICKER -->
    <div class="ticker-wrap border-b border-lab-teal/20">
        <div class="ticker">
            <span class="px-8 text-white font-bold">FREE AU POST ON ORDERS OVER $99</span><span class="px-8">&bull;</span>
            <span class="px-8 text-white font-bold">IN STOCK: IPHONE 17 SERIES KITS</span><span class="px-8">&bull;</span>
            <span class="px-8 text-white font-bold">SAME DAY DISPATCH FROM NEWCASTLE</span><span class="px-8">&bull;</span>
            <span class="px-8 text-white font-bold">DIAGNOSABLE BATTERIES AVAILABLE</span><span class="px-8">&bull;</span>
            <span class="px-8 text-white font-bold">90-DAY WARRANTY ON ALL PARTS</span><span class="px-8">&bull;</span>
            <span class="px-8 text-white font-bold">FREE AU POST ON ORDERS OVER $99</span><span class="px-8">&bull;</span>
            <span class="px-8 text-white font-bold">IN STOCK: IPHONE 17 SERIES KITS</span><span class="px-8">&bull;</span>
            <span class="px-8 text-white font-bold">SAME DAY DISPATCH FROM NEWCASTLE</span><span class="px-8">&bull;</span>
            <span class="px-8 text-white font-bold">DIAGNOSABLE BATTERIES AVAILABLE</span><span class="px-8">&bull;</span>
            <span class="px-8 text-white font-bold">90-DAY WARRANTY ON ALL PARTS</span><span class="px-8">&bull;</span>
        </div>
    </div>
"""

TICKER_CSS = """
        .ticker-wrap{overflow:hidden;background:#212629;padding:6px 0}
        .ticker{display:flex;white-space:nowrap;animation:scroll 30s linear infinite;font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:white !important}
        @keyframes scroll{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
"""

files = [
    "selfrepairkit/index.html",
    "selfrepairkit/shop.html",
    "selfrepairkit/blog.html",
    "selfrepairkit/guides.html",
    "selfrepairkit/privacy.html",
    "selfrepairkit/terms.html",
    "selfrepairkit/shipping.html",
    "selfrepairkit/support.html"
]

for file_path in files:
    if not os.path.exists(file_path): continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update/Add CSS
    if '.ticker-wrap' in content:
        # Update existing CSS
        content = re.sub(r'\.ticker-wrap\{[^}]*\}', '.ticker-wrap{overflow:hidden;background:#212629;padding:6px 0}', content)
        content = re.sub(r'\.ticker\{[^}]*\}', '.ticker{display:flex;white-space:nowrap;animation:scroll 30s linear infinite;font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:white !important}', content)
    else:
        # Add CSS before </style>
        content = content.replace('</style>', TICKER_CSS + '</style>')
    
    # 2. Add/Update HTML
    if '<!-- TICKER -->' in content:
        # Replace existing ticker
        content = re.sub(r'<!-- TICKER -->.*?</div>\s*</div>', TICKER_HTML.strip(), content, flags=re.DOTALL)
    else:
        # Add ticker after <body>
        content = content.replace('<body class="bg-lab-dark text-slate-100 antialiased font-sans">', '<body class="bg-lab-dark text-slate-100 antialiased font-sans">\n' + TICKER_HTML)
        content = content.replace('<body class="antialiased font-sans bg-lab-dark text-slate-100">', '<body class="antialiased font-sans bg-lab-dark text-slate-100">\n' + TICKER_HTML)
        # Fallback for pages with different body classes
        if '<!-- TICKER -->' not in content:
            content = re.sub(r'<body[^>]*>', r'\g<0>\n' + TICKER_HTML, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Synced ticker in {file_path}")

print("Global ticker synchronization complete.")
