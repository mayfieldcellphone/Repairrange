#!/usr/bin/env python3
"""
publish_scheduled_blogs.py — Automated Blog Scheduler for RepairRange.io

Reads scheduled_blogs/manifest.json, checks for posts due on or before today,
publishes them to blog/<slug>.html, updates blog.html, and regenerates sitemap.xml.
"""

import os
import sys
import json
import shutil
import argparse
import datetime as dt
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "scheduled_blogs" / "manifest.json"
SCHEDULED_DIR = ROOT / "scheduled_blogs"
BLOG_DIR = ROOT / "blog"
BLOG_INDEX = ROOT / "blog.html"
SITEMAP_SCRIPT = ROOT / "generate_sitemap.py"

def load_manifest():
    if not MANIFEST_PATH.exists():
        print(f"Error: Manifest not found at {MANIFEST_PATH}", file=sys.stderr)
        return []
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_manifest(manifest):
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")

def format_card(post, pub_date):
    month_year = pub_date.strftime("%B %Y")
    return f'''            <a href="blog/{post['slug']}.html" class="post-card group">
                <p class="eyebrow mb-3">{post['category']} &bull; {post['read_time']} &bull; {month_year}</p>
                <h2 class="font-serif text-2xl md:text-3xl text-ink mb-3 leading-tight">{post['title']}</h2>
                <p class="text-muted leading-relaxed mb-4">{post['meta_description']}</p>
                <span class="inline-flex items-center gap-2 text-sm font-medium text-teal">Read the post <i data-lucide="arrow-right" class="w-4 h-4"></i></span>
            </a>\n\n'''

def update_blog_index(post, pub_date):
    if not BLOG_INDEX.exists():
        print("Warning: blog.html not found, skipping index update.")
        return False
    with open(BLOG_INDEX, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if link already present
    if f'href="blog/{post["slug"]}.html"' in content:
        print(f"  Note: Card for {post['slug']} already present in blog.html.")
        return True

    marker = "<!-- BLOG_GRID_START -->"
    if marker not in content:
        print("Warning: <!-- BLOG_GRID_START --> marker not found in blog.html.")
        return False

    card = format_card(post, pub_date)
    new_content = content.replace(marker, f"{marker}\n{card}")
    with open(BLOG_INDEX, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True

def run_sitemap_gen():
    if SITEMAP_SCRIPT.exists():
        try:
            print("Regenerating sitemap.xml...")
            subprocess.run([sys.executable, str(SITEMAP_SCRIPT)], check=True, cwd=str(ROOT))
        except Exception as e:
            print(f"Warning: generate_sitemap.py failed: {e}")

def show_status(manifest):
    today = dt.date.today()
    print("\n=== RepairRange Automated Blog Schedule Status ===")
    print(f"Current Date: {today.isoformat()}\n")
    print(f"{'Status':<12} {'Publish Date':<14} {'Days Left':<10} {'Slug':<45}")
    print("-" * 85)
    for p in manifest:
        p_date = dt.date.fromisoformat(p["publish_date"])
        diff = (p_date - today).days
        if p.get("published"):
            status = "PUBLISHED"
            diff_str = "Done"
        elif diff <= 0:
            status = "DUE NOW"
            diff_str = f"{abs(diff)}d ago" if diff < 0 else "Today"
        else:
            status = "SCHEDULED"
            diff_str = f"in {diff}d"
        print(f"{status:<12} {p['publish_date']:<14} {diff_str:<10} {p['slug']:<45}")
    print()

def main():
    parser = argparse.ArgumentParser(description="RepairRange Automated Blog Publisher")
    parser.add_argument("--dry-run", action="store_true", help="Simulate publish without modifying files")
    parser.add_argument("--force", type=str, help="Force-publish a specific post slug regardless of date")
    parser.add_argument("--all", action="store_true", help="Publish all pending scheduled posts immediately")
    parser.add_argument("--status", action="store_true", help="Show scheduled queue status")
    args = parser.parse_args()

    manifest = load_manifest()
    if not manifest:
        sys.exit(1)

    if args.status:
        show_status(manifest)
        return

    today = dt.date.today()
    published_count = 0

    for post in manifest:
        slug = post["slug"]
        already_pub = post.get("published", False)
        p_date = dt.date.fromisoformat(post["publish_date"])

        is_due = (p_date <= today) or args.all or (args.force == slug)

        if not is_due:
            continue

        if already_pub and not (args.force == slug):
            continue

        print(f"Processing: [{slug}] (Target Date: {post['publish_date']})...")

        src_file = SCHEDULED_DIR / f"{slug}.html"
        dest_file = BLOG_DIR / f"{slug}.html"

        if not src_file.exists():
            print(f"  Error: Source file {src_file} does not exist!", file=sys.stderr)
            continue

        if args.dry_run:
            print(f"  [DRY-RUN] Would publish {src_file} -> {dest_file}")
            print(f"  [DRY-RUN] Would add card to blog.html")
            published_count += 1
            continue

        # 1. Copy to blog/
        BLOG_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_file, dest_file)
        print(f"  Copied {src_file.name} -> blog/{dest_file.name}")

        # 2. Update blog.html
        if update_blog_index(post, today if args.force or args.all else p_date):
            print(f"  Added card to blog.html")

        # 3. Mark manifest
        post["published"] = True
        post["published_at"] = today.isoformat()
        published_count += 1

    if published_count > 0:
        if not args.dry_run:
            save_manifest(manifest)
            run_sitemap_gen()
            print(f"\nSuccessfully published {published_count} post(s).")
        else:
            print(f"\n[DRY-RUN] {published_count} post(s) would be published.")
    else:
        print("No scheduled posts due for publication today.")

if __name__ == "__main__":
    main()
