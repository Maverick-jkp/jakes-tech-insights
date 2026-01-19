#!/usr/bin/env python3
"""
Replace a post's image by downloading from Unsplash API properly

Usage:
    python replace_image_via_api.py <post-path> <search-query>
"""

import os
import sys
import json
import requests
from pathlib import Path

def download_image_from_unsplash(query: str, exclude_ids: list = None) -> dict:
    """Download image from Unsplash API avoiding duplicates"""

    access_key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not access_key:
        print("❌ UNSPLASH_ACCESS_KEY not found in environment")
        sys.exit(1)

    # Load used images
    project_root = Path(__file__).parent.parent
    used_images_file = project_root / "data" / "used_images.json"

    if used_images_file.exists():
        with open(used_images_file, 'r') as f:
            used_images = set(json.load(f))
    else:
        used_images = set()

    if exclude_ids:
        used_images.update(exclude_ids)

    print(f"🔍 Searching Unsplash for: {query}")
    print(f"📋 Excluding {len(used_images)} already-used images")

    # Search Unsplash
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {access_key}"}
    params = {
        "query": query,
        "per_page": 30,
        "order_by": "relevant"
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    if not data.get('results'):
        print(f"❌ No images found for query: {query}")
        sys.exit(1)

    # Find first unused image
    photo = None
    for result in data['results']:
        if result['id'] not in used_images:
            photo = result
            break

    if not photo:
        print(f"❌ All images for '{query}' have been used already")
        sys.exit(1)

    print(f"✅ Found unused image: {photo['id']}")

    # Download image
    image_url = photo['urls']['regular']
    image_response = requests.get(image_url)
    image_response.raise_for_status()

    # Update used_images
    used_images.add(photo['id'])
    with open(used_images_file, 'w') as f:
        json.dump(sorted(list(used_images)), f, indent=2)

    return {
        'id': photo['id'],
        'image_data': image_response.content,
        'photographer': photo['user']['name'],
        'photographer_url': photo['user']['links']['html'],
        'unsplash_url': photo['links']['html']
    }

def main():
    if len(sys.argv) < 3:
        print("Usage: python replace_image_via_api.py <post-path> <search-query>")
        print("Example: python replace_image_via_api.py content/en/finance/2026-01-19-mlk-day-market-closure-effects.md 'stock market trading finance'")
        sys.exit(1)

    post_path = Path(sys.argv[1])
    query = sys.argv[2]

    if not post_path.exists():
        print(f"❌ Post not found: {post_path}")
        sys.exit(1)

    # Read post to get image filename
    with open(post_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract image path from frontmatter
    import re
    match = re.search(r'image:\s*"([^"]+)"', content)
    if not match:
        print(f"❌ No image path found in post frontmatter")
        sys.exit(1)

    image_path = match.group(1)
    image_filename = Path(image_path).name

    # Extract current Unsplash ID if exists (to exclude from search)
    exclude_ids = []
    unsplash_match = re.search(r'unsplash\.com/photos/[^)]*-([a-zA-Z0-9_-]+)\)', content)
    if unsplash_match:
        exclude_ids.append(unsplash_match.group(1))
        print(f"🚫 Excluding current image ID: {exclude_ids[0]}")

    # Download new image
    result = download_image_from_unsplash(query, exclude_ids)

    # Save image
    project_root = Path(__file__).parent.parent
    image_file = project_root / "static" / "images" / image_filename

    with open(image_file, 'wb') as f:
        f.write(result['image_data'])

    print(f"💾 Saved image: {image_file}")
    print(f"📝 Size: {len(result['image_data']) / 1024:.0f}KB")

    # Update post with new photo credit
    old_credit_pattern = r'\n---\n\n\*Photo by \[.*?\]\(.*?\) on \[Unsplash\]\(.*?\)\*\n'
    new_credit = f"\n---\n\n*Photo by [{result['photographer']}]({result['photographer_url']}) on [Unsplash]({result['unsplash_url']})*\n"

    if re.search(old_credit_pattern, content):
        content = re.sub(old_credit_pattern, new_credit, content)
    else:
        # Add credit at end
        content = content.rstrip() + '\n' + new_credit

    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Updated post with new photo credit")
    print(f"🎨 Photographer: {result['photographer']}")
    print(f"🔗 Unsplash URL: {result['unsplash_url']}")

if __name__ == "__main__":
    main()
