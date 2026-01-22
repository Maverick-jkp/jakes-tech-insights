#!/usr/bin/env python3
"""
Fix duplicate images in existing posts and update used_images.json
"""
import os
import json
import hashlib
import re
from pathlib import Path
from collections import defaultdict

def get_file_hash(filepath):
    """Get MD5 hash of file"""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def extract_unsplash_id(md_file):
    """Extract Unsplash image ID from markdown file"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # Look for Unsplash photo URL pattern: unsplash.com/photos/...-{ID})
        match = re.search(r'unsplash\.com/photos/[^)]*-([a-zA-Z0-9_-]+)\)', content)
        if match:
            return match.group(1)
    return None

def main():
    project_root = Path(__file__).parent.parent
    images_dir = project_root / "static" / "images"
    content_dir = project_root / "content"

    # Find all duplicate images
    hash_to_files = defaultdict(list)

    print("🔍 Scanning for duplicate images...")
    for img_file in images_dir.glob("*.jpg"):
        file_hash = get_file_hash(img_file)
        hash_to_files[file_hash].append(img_file)

    # Find duplicates
    duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}

    if not duplicates:
        print("✅ No duplicate images found!")
        return

    print(f"\n📊 Found {len(duplicates)} sets of duplicate images:")

    # Collect all used Unsplash IDs from existing posts
    used_ids = set()
    print("\n🔍 Extracting Unsplash IDs from existing posts...")

    for md_file in content_dir.rglob("*.md"):
        image_id = extract_unsplash_id(md_file)
        if image_id:
            used_ids.add(image_id)
            print(f"  Found ID: {image_id} in {md_file.name}")

    # Save to used_images.json
    used_images_file = project_root / "data" / "used_images.json"
    used_images_file.parent.mkdir(parents=True, exist_ok=True)

    with open(used_images_file, 'w') as f:
        json.dump(list(used_ids), f, indent=2)

    print(f"\n✅ Updated {used_images_file}")
    print(f"   Total unique Unsplash IDs: {len(used_ids)}")

    # Show duplicate report
    print("\n📋 Duplicate Image Report:")
    for file_hash, files in duplicates.items():
        print(f"\n  Hash: {file_hash[:8]}... ({len(files)} files)")
        for f in files:
            print(f"    - {f.name}")

if __name__ == "__main__":
    main()
