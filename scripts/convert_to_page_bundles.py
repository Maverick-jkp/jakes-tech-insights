#!/usr/bin/env python3
"""
Convert posts to page bundles for Hugo image processing.

Before:
  content/en/tech/ai-coding-tools.md
  static/images/ai-coding-tools.jpg

After:
  content/en/tech/ai-coding-tools/index.md
  content/en/tech/ai-coding-tools/cover.jpg
"""
import os
import shutil
from pathlib import Path

def convert_to_page_bundle(md_file_path: str, static_images_dir: str):
    """Convert a single markdown file to a page bundle."""

    md_path = Path(md_file_path)

    # Create bundle directory
    bundle_dir = md_path.parent / md_path.stem
    bundle_dir.mkdir(exist_ok=True)

    # Move markdown to index.md
    index_path = bundle_dir / "index.md"
    shutil.move(str(md_path), str(index_path))

    # Read frontmatter to find image
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract image path from frontmatter
    import re
    image_match = re.search(r'image:\s*["\']?([^"\'\n]+)["\']?', content)

    if image_match:
        image_path = image_match.group(1)
        # /images/ai-coding-tools.jpg -> ai-coding-tools.jpg
        image_filename = Path(image_path).name

        # Find image in static/images/
        source_image = Path(static_images_dir) / image_filename

        if source_image.exists():
            # Copy image to bundle as cover.jpg
            dest_image = bundle_dir / "cover.jpg"
            shutil.copy2(str(source_image), str(dest_image))

            # Update frontmatter to use relative path
            new_content = content.replace(
                f'image: {image_path}',
                'image: cover.jpg'
            )

            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"✅ Converted: {md_path.name} → {bundle_dir.name}/")
        else:
            print(f"⚠️  Image not found: {source_image}")
    else:
        print(f"⚠️  No image found in frontmatter: {md_path}")

def main():
    """Convert all posts to page bundles."""

    content_dir = Path("content")
    static_images_dir = "static/images"

    # Process all markdown files
    for lang in ['en', 'ko', 'ja']:
        lang_dir = content_dir / lang

        for category_dir in lang_dir.iterdir():
            if not category_dir.is_dir():
                continue

            for md_file in category_dir.glob("*.md"):
                # Skip if already a bundle (index.md)
                if md_file.name == "index.md":
                    continue

                convert_to_page_bundle(str(md_file), static_images_dir)

    print("\n✅ Conversion complete!")
    print("Next steps:")
    print("1. Test locally: hugo server -D")
    print("2. Verify images display correctly")
    print("3. Commit changes")

if __name__ == '__main__':
    main()
