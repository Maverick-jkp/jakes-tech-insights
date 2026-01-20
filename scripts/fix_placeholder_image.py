#!/usr/bin/env python3
"""
Fix placeholder image for a specific post by fetching from Unsplash.
"""

import os
import sys
import re
import json
import requests
from pathlib import Path

def fetch_unsplash_image(keyword, category):
    """Fetch image from Unsplash API"""
    api_key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not api_key:
        print("❌ Error: UNSPLASH_ACCESS_KEY not set")
        return None

    # Translation dictionary
    translations = {
        # Japanese
        "大相撲": "sumo wrestling",
        "結果速報": "tournament results",
        "見逃し": "highlights",
        # Common Japanese words
        "速報": "breaking news",
        "最新": "latest",
    }

    # Translate keyword
    english_query = keyword
    for jp, en in translations.items():
        english_query = english_query.replace(jp, en)

    query = f"{category} {english_query}".strip()

    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {api_key}"}
    params = {
        "query": query,
        "per_page": 5,
        "orientation": "landscape"
    }

    print(f"🔍 Searching Unsplash for: {query}")

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get('results'):
            # Fallback to category only
            print(f"  ⚠️  No images found, trying category only...")
            params['query'] = category
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data.get('results'):
                print(f"  ❌ Still no images found")
                return None

        # Load used images
        used_images_file = Path(__file__).parent.parent / "data" / "used_images.json"
        used_images = set()
        if used_images_file.exists():
            try:
                with open(used_images_file, 'r') as f:
                    used_images = set(json.load(f))
            except:
                pass

        # Find first unused image
        photo = None
        for result in data['results']:
            image_id = result['id']
            if image_id not in used_images:
                photo = result
                used_images.add(image_id)
                break

        # If all used, pick random from top 5
        if photo is None:
            import random
            photo = random.choice(data['results'][:5])
            used_images.add(photo['id'])

        # Save used images
        used_images_file.parent.mkdir(parents=True, exist_ok=True)
        with open(used_images_file, 'w') as f:
            json.dump(list(used_images), f)

        return {
            'url': photo['urls']['regular'],
            'download_url': photo['links']['download_location'],
            'photographer': photo['user']['name'],
            'photographer_url': photo['user']['links']['html'],
            'unsplash_url': photo['links']['html'],
            'image_id': photo['id']
        }

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

def download_image(image_url, output_path, api_key, download_url):
    """Download image from URL"""
    try:
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.content)

        # Trigger download event
        if download_url:
            requests.get(
                download_url,
                headers={"Authorization": f"Client-ID {api_key}"},
                timeout=5
            )

        return True
    except Exception as e:
        print(f"  ❌ Download failed: {e}")
        return False

def update_post_frontmatter(post_path, image_path, image_credit):
    """Update post frontmatter with new image"""
    try:
        with open(post_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update image field in frontmatter
        content = re.sub(
            r'image: "/images/placeholder-[^"]+\.jpg"',
            f'image: "{image_path}"',
            content
        )

        # Add image credit at end
        credit_line = f"\n\n*Photo by [{image_credit['photographer']}]({image_credit['photographer_url']}) on [Unsplash]({image_credit['unsplash_url']})*\n"

        # Remove old credit if exists
        content = re.sub(r'\n\n\*Photo by.*\*\n', '', content)

        # Add new credit
        if not content.endswith('\n'):
            content += '\n'
        content += credit_line

        with open(post_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    except Exception as e:
        print(f"  ❌ Failed to update post: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_placeholder_image.py <post_path>")
        sys.exit(1)

    post_path = Path(sys.argv[1])
    if not post_path.exists():
        print(f"❌ Post not found: {post_path}")
        sys.exit(1)

    # Extract keyword and category from post
    with open(post_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract from frontmatter
    title_match = re.search(r'title: "([^"]+)"', content)
    category_match = re.search(r'categories: \["([^"]+)"\]', content)

    if not title_match or not category_match:
        print("❌ Failed to extract title or category from post")
        sys.exit(1)

    title = title_match.group(1)
    category = category_match.group(1)

    print(f"📝 Post: {title}")
    print(f"📂 Category: {category}")

    # Fetch image
    image_info = fetch_unsplash_image(title, category)
    if not image_info:
        print("❌ Failed to fetch image")
        sys.exit(1)

    print(f"✓ Found image by {image_info['photographer']}")

    # Generate filename from post filename
    post_filename = post_path.stem  # e.g., 2026-01-20-大相撲結果速報見逃し
    image_filename = f"{post_filename}.jpg"
    image_path = Path("static/images") / image_filename

    # Download image
    api_key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if download_image(image_info['url'], image_path, api_key, image_info.get('download_url')):
        print(f"✓ Downloaded to {image_path}")
    else:
        print("❌ Failed to download image")
        sys.exit(1)

    # Update post
    relative_image_path = f"/images/{image_filename}"
    if update_post_frontmatter(post_path, relative_image_path, image_info):
        print(f"✓ Updated post frontmatter")
    else:
        print("❌ Failed to update post")
        sys.exit(1)

    print("✅ Done!")

if __name__ == "__main__":
    main()
