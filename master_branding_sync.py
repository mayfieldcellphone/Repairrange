import os
import re

# Comprehensive list of HTML files to update
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

# Replacement pattern for emails
OLD_EMAIL = r'engrkhalil77@gmail.com'
NEW_EMAIL = 'support@selfrepairkit.com.au'

# Replacement pattern for broken links and old GitLab URLs
OLD_GITLAB_BASE = r'https?://(?:mayfield276\.gitlab\.io/selfrepairkit|selfrepairkit-a1fa93\.gitlab\.io)/?'
NEW_DOMAIN_BASE = 'https://selfrepairkit.com.au/'

for file_path in files:
    if not os.path.exists(file_path):
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update emails
    new_content = re.sub(OLD_EMAIL, NEW_EMAIL, content)
    
    # 2. Update GitLab links to custom domain
    new_content = re.sub(OLD_GITLAB_BASE, NEW_DOMAIN_BASE, new_content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Synced {file_path}")

print("Master domain and email synchronization complete.")
