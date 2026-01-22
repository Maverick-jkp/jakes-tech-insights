#!/usr/bin/env python3
"""
Re-download existing images from Unsplash with optimized size.

This script:
1. Scans all post bundles for cover.jpg
2. Extracts Unsplash photo ID from image credits in markdown
3. Re-downloads with optimized parameters (w=1200, q=85)
4. Replaces existing image
"""
import os
import re
import requests
from pathlib import Path
from time import sleep

# Load .env file if it exists
env_file = Path(".env")
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

def extract_photo_id_from_post(post_path: Path) -> str:
    """Extract Unsplash photo ID from post frontmatter or content."""

    try:
        with open(post_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for Unsplash URL in credits or frontmatter
        # Example patterns:
        # - https://unsplash.com/photos/title-ViC0envGdTU (ID is last part after last -)
        # - https://unsplash.com/photos/abc123xyz
        # - https://images.unsplash.com/photo-abc123xyz

        # Try full photo URL with title (most common format)
        # Example: unsplash.com/photos/the-word-ai-spelled-ViC0envGdTU
        # ID is the part after the last hyphen (usually 11 chars)
        match = re.search(r'unsplash\.com/photos/[^)]+?-([a-zA-Z0-9_-]{8,15})(?:[)\s]|$)', content)
        if match:
            return match.group(1)

        # Try simple photo URL
        match = re.search(r'unsplash\.com/photos/([a-zA-Z0-9_-]{8,15})(?:[)\s]|$)', content)
        if match:
            return match.group(1)

        # Try image URL with photo- prefix
        match = re.search(r'images\.unsplash\.com/photo-([a-zA-Z0-9_-]+)', content)
        if match:
            return f"photo-{match.group(1)}"

        return None

    except Exception as e:
        print(f"Error reading {post_path}: {e}")
        return None

def redownload_image(bundle_dir: Path):
    """Re-download optimized image for a post bundle."""

    index_md = bundle_dir / "index.md"
    cover_jpg = bundle_dir / "cover.jpg"

    if not index_md.exists():
        return False

    if not cover_jpg.exists():
        print(f"⚠️  No cover.jpg: {bundle_dir.name}")
        return False

    # Get original size for comparison
    original_size = cover_jpg.stat().st_size / 1024

    photo_id = extract_photo_id_from_post(index_md)

    if not photo_id:
        print(f"⚠️  No Unsplash ID found: {bundle_dir.name}")
        return False

    try:
        # Trigger download event (required by Unsplash API)
        if UNSPLASH_ACCESS_KEY:
            trigger_url = f"https://api.unsplash.com/photos/{photo_id}/download"
            requests.get(
                trigger_url,
                headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"},
                timeout=5
            )

        # Download optimized version (1200px width, quality 85)
        # Ensure photo_id has 'photo-' prefix for direct image URLs
        if not photo_id.startswith('photo-'):
            photo_id = f"photo-{photo_id}"

        optimized_url = f"https://images.unsplash.com/{photo_id}?w=1200&q=85&fm=jpg"
        response = requests.get(optimized_url, timeout=30)
        response.raise_for_status()

        # Save
        with open(cover_jpg, 'wb') as f:
            f.write(response.content)

        # Get new file size
        new_size = cover_jpg.stat().st_size / 1024
        savings = ((original_size - new_size) / original_size) * 100 if original_size > 0 else 0

        print(f"✅ {bundle_dir.name}: {original_size:.1f} KB → {new_size:.1f} KB ({savings:.1f}% savings)")

        # Rate limiting
        sleep(1)
        return True

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"❌ {bundle_dir.name}: Image not found (404)")
        else:
            print(f"❌ {bundle_dir.name}: HTTP {e.response.status_code}")
        return False
    except Exception as e:
        print(f"❌ {bundle_dir.name}: {e}")
        return False

def main():
    """Re-download all images with optimization."""

    if not UNSPLASH_ACCESS_KEY:
        print("⚠️  UNSPLASH_ACCESS_KEY not set (continuing without download tracking)")

    content_dir = Path("content")

    total = 0
    success = 0
    failed = 0

    print("🔄 Re-downloading images with optimization (w=1200, q=85)...\n")

    for lang in ['en', 'ko', 'ja']:
        lang_dir = content_dir / lang

        if not lang_dir.exists():
            continue

        print(f"\n📁 Processing {lang.upper()} posts...")

        for category_dir in lang_dir.iterdir():
            if not category_dir.is_dir():
                continue

            for bundle_dir in category_dir.iterdir():
                if not bundle_dir.is_dir():
                    continue

                if not (bundle_dir / "index.md").exists():
                    continue

                total += 1
                if redownload_image(bundle_dir):
                    success += 1
                else:
                    failed += 1

    print(f"\n{'='*60}")
    print(f"✅ Summary:")
    print(f"   Total bundles: {total}")
    print(f"   Success: {success}")
    print(f"   Failed: {failed}")
    print(f"   Success rate: {(success/total*100):.1f}%" if total > 0 else "")
    print(f"\n💡 Next: hugo server -D")

if __name__ == '__main__':
    main()
