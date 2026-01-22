#!/usr/bin/env python3
"""
Copy images to existing page bundles.

This script:
1. Scans all page bundles (directories with index.md)
2. Reads frontmatter to find image path
3. Finds the actual image file in static/images/
4. Copies it to the bundle as cover.jpg
5. Updates the image path in frontmatter
"""
import os
import shutil
from pathlib import Path
import re

def copy_image_to_bundle(bundle_dir: Path, static_images_dir: str):
    """Copy image to a page bundle and update frontmatter."""

    index_path = bundle_dir / "index.md"

    if not index_path.exists():
        return

    # Read frontmatter
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract image path from frontmatter
    image_match = re.search(r'image:\s*["\']?([^"\'\n]+)["\']?', content)

    if not image_match:
        print(f"⚠️  No image in frontmatter: {bundle_dir.name}")
        return

    image_path = image_match.group(1)

    # Already using relative path (cover.jpg)?
    if image_path == "cover.jpg":
        if (bundle_dir / "cover.jpg").exists():
            print(f"✅ Already done: {bundle_dir.name}")
            return

    # Extract filename from path (/images/filename.jpg -> filename.jpg)
    image_filename = Path(image_path).name

    # Find image in static/images/
    source_image = Path(static_images_dir) / image_filename

    if not source_image.exists():
        # Try to find similar filename (case-insensitive, with date prefix, etc.)
        static_dir = Path(static_images_dir)

        # Remove date prefix and extension for fuzzy matching
        bundle_name = bundle_dir.name.lower()
        # Remove date prefix like "2026-01-17-"
        bundle_name_clean = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', bundle_name)

        # Search for similar files
        for img_file in static_dir.glob("*.jpg"):
            img_name_clean = re.sub(r'^\d{8}-', '', img_file.stem.lower())

            if img_name_clean in bundle_name_clean or bundle_name_clean in img_name_clean:
                source_image = img_file
                print(f"🔍 Found match: {img_file.name} for {bundle_dir.name}")
                break

        if not source_image.exists():
            print(f"❌ Image not found: {bundle_dir.name} (looking for {image_filename})")
            return

    # Copy image to bundle as cover.jpg
    dest_image = bundle_dir / "cover.jpg"

    # Skip if already exists and is the same size
    if dest_image.exists() and dest_image.stat().st_size == source_image.stat().st_size:
        print(f"✅ Already copied: {bundle_dir.name}")

        # Update frontmatter anyway if needed
        if image_path != "cover.jpg":
            new_content = content.replace(
                f'image: {image_path}',
                'image: cover.jpg'
            )
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

        return

    shutil.copy2(str(source_image), str(dest_image))

    # Update frontmatter to use relative path
    new_content = content.replace(
        f'image: {image_path}',
        'image: cover.jpg'
    )

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    size_kb = dest_image.stat().st_size / 1024
    print(f"✅ Copied: {bundle_dir.name} ({size_kb:.1f} KB)")

def main():
    """Process all page bundles."""

    content_dir = Path("content")
    static_images_dir = "static/images"

    total = 0
    success = 0

    # Process all bundles
    for lang in ['en', 'ko', 'ja']:
        lang_dir = content_dir / lang

        if not lang_dir.exists():
            continue

        for category_dir in lang_dir.iterdir():
            if not category_dir.is_dir():
                continue

            for bundle_dir in category_dir.iterdir():
                if not bundle_dir.is_dir():
                    continue

                if not (bundle_dir / "index.md").exists():
                    continue

                total += 1
                copy_image_to_bundle(bundle_dir, static_images_dir)

    print(f"\n✅ Processed {total} bundles")
    print("Next: hugo server -D")

if __name__ == '__main__':
    main()
