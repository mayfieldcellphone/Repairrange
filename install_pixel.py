# List of HTML files to inject Meta Pixel into
import os
import re

PIXEL_CODE = """
    <!-- Meta Pixel Code -->
    <script>
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '2007947063181918');
    fbq('track', 'PageView');
    </script>
    <noscript><img height="1" width="1" style="display:none"
    src="https://www.facebook.com/tr?id=2007947063181918&ev=PageView&noscript=1"
    /></noscript>
    <!-- End Meta Pixel Code -->
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
    if not os.path.exists(file_path):
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Avoid duplicate injection
    if '2007947063181918' in content:
        print(f"Skipping {file_path}, Pixel already installed.")
        continue

    # Inject before </head>
    new_content = content.replace('</head>', f'{PIXEL_CODE}</head>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully installed Pixel in {file_path}")
