#!/usr/bin/env python3
"""
Update image paths in frontmatter to use relative path (cover.jpg).
"""
from pathlib import Path
import re

def update_image_path(bundle_dir: Path):
    """Update image path in frontmatter to cover.jpg."""

    index_path = bundle_dir / "index.md"

    if not index_path.exists():
        return False

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already using cover.jpg
    if 'image: cover.jpg' in content or 'image: "cover.jpg"' in content or "image: 'cover.jpg'" in content:
        return False

    # Extract image path from frontmatter
    image_match = re.search(r'image:\s*["\']?([^"\'\n]+)["\']?', content)

    if not image_match:
        return False

    image_path = image_match.group(1)

    # Check if cover.jpg exists
    cover_path = bundle_dir / "cover.jpg"
    if not cover_path.exists():
        print(f"⚠️  No cover.jpg: {bundle_dir.name}")
        return False

    # Update frontmatter
    new_content = content.replace(
        f'image: {image_path}',
        'image: cover.jpg'
    )

    # Also handle quoted versions
    new_content = new_content.replace(
        f'image: "{image_path}"',
        'image: cover.jpg'
    )
    new_content = new_content.replace(
        f"image: '{image_path}'",
        'image: cover.jpg'
    )

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ Updated: {bundle_dir.name}")
    return True

def main():
    """Update all bundle image paths."""

    content_dir = Path("content")

    total = 0
    updated = 0

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
                if update_image_path(bundle_dir):
                    updated += 1

    print(f"\n✅ Updated {updated}/{total} bundles")

if __name__ == '__main__':
    main()
