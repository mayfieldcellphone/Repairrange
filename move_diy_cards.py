import os
import re

TARGET_DIRS = [
    r"C:\Users\dell lattitude\.accio\accounts\1728917364\agents\MID-29917364U1780312-3FBB0C-8987-5BD472\project\repair",
    r"C:\Users\dell lattitude\.accio\accounts\1728917364\agents\MID-29917364U1780312-3FBB0C-8987-5BD472\project\repairrange-final-push\repair"
]

def move_kit_card():
    count = 0
    for target_dir in TARGET_DIRS:
        if not os.path.exists(target_dir):
            continue
            
        for file in os.listdir(target_dir):
            if not file.endswith(".html"):
                continue
                
            path = os.path.join(target_dir, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 1. Extract the selfrepairkit card
            card_match = re.search(r'(<div class="sidebar-card bg-teal-900.*?>.*?selfrepairkit\.com\.au.*?</div>)', content, re.DOTALL)
            if not card_match:
                continue
                
            kit_card = card_match.group(1)
            
            # 2. Remove the card from its current location
            content = content.replace(kit_card, "")
            
            # 3. Clean up the hero section layout if it was in a 8/4 grid
            # If we see <div class="lg:col-span-8"> followed by an empty <div class="lg:col-span-4">, collapse it
            content = re.sub(r'<div class="lg:col-span-8">\s*<nav', r'<div class="lg:col-span-12">\n                <nav', content)
            
            # 4. Find the main sidebar (the one next to the table)
            # It usually starts with <aside class="lg:col-span-4"> or <div class="lg:col-span-4">\n                <div class="sticky top-32
            sidebar_pos = content.find('<div class="sticky top-32 space-y-6">')
            if sidebar_pos == -1:
                sidebar_pos = content.find('<div class="sticky top-32 space-y-8">')
            
            if sidebar_pos != -1:
                # Insert at the top of the sticky container
                insertion_point = content.find('>', sidebar_pos) + 1
                content = content[:insertion_point] + "\n                " + kit_card + content[insertion_point:]
            else:
                # Fallback: find the first lg:col-span-4 in the second section
                # (Highly simplified for this specific codebase structure)
                second_section = content.find('Component Price Index')
                if second_section != -1:
                    sidebar_match = re.search(r'<div class="lg:col-span-4">', content[second_section:])
                    if sidebar_match:
                        insertion_point = second_section + sidebar_match.end()
                        content = content[:insertion_point] + "\n                " + kit_card + content[insertion_point:]

            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
            
    print(f"Successfully moved DIY Kit cards next to tables in {count} files.")

if __name__ == "__main__":
    move_kit_card()
