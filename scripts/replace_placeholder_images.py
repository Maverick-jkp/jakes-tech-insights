#!/usr/bin/env python3
"""
Find posts with placeholder images and replace them with real Unsplash images.
This script is meant to be run by GitHub Actions with UNSPLASH_ACCESS_KEY available.
"""

import os
import sys
import re
import json
import requests
from pathlib import Path
from typing import Optional, Dict

def find_posts_with_placeholders():
    """Find all posts that have placeholder images"""
    content_dir = Path("content")
    placeholder_posts = []

    for md_file in content_dir.rglob("*.md"):
        if md_file.name in ["all-posts.md", "archives.md"]:
            continue

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            if re.search(r'image: "/images/placeholder-[^"]+\.jpg"', content):
                placeholder_posts.append(md_file)
        except:
            continue

    return placeholder_posts

def fetch_unsplash_image(keyword: str, category: str, api_key: str) -> Optional[Dict]:
    """Fetch image from Unsplash API"""
    # Translation dictionary for better English queries
    translations = {
        # Japanese
        "大相撲": "sumo wrestling",
        "結果速報": "tournament results  ",
        "見逃し": "highlights",
        "速報": "breaking news",
        "最新": "latest",
        "日本": "japan",
        # Korean
        "속보": "breaking news",
        "최신": "latest",
        # Common terms
        "ニュース": "news",
        "뉴스": "news",
    }

    # Translate keyword to English
    english_query = keyword
    for foreign, english in translations.items():
        english_query = english_query.replace(foreign, english)

    # Clean up the query
    english_query = re.sub(r'[【】\[\]「」]', '', english_query)
    english_query = ' '.join(english_query.split())

    query = f"{category} {english_query}".strip()

    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {api_key}"}
    params = {
        "query": query,
        "per_page": 10,  # Get more results to find unused ones
        "orientation": "landscape"
    }

    print(f"  🔍 Searching Unsplash: {query}")

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get('results'):
            # Fallback to category only
            print(f"    ⚠️  No results, trying category only")
            params['query'] = category
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data.get('results'):
                print(f"    ❌ No images found")
                return None

        # Load used images tracking
        used_images_file = Path("data/used_images.json")
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
            if result['id'] not in used_images:
                photo = result
                used_images.add(result['id'])
                break

        # If all are used, pick random from results
        if photo is None:
            import random
            photo = random.choice(data['results'])
            used_images.add(photo['id'])
            print(f"    ⚠️  All images used, picking random")

        # Save updated used_images
        used_images_file.parent.mkdir(parents=True, exist_ok=True)
        with open(used_images_file, 'w') as f:
            json.dump(list(used_images), f, indent=2)

        return {
            'url': photo['urls']['regular'],
            'download_url': photo['links']['download_location'],
            'photographer': photo['user']['name'],
            'photographer_url': photo['user']['links']['html'],
            'unsplash_url': photo['links']['html'],
            'image_id': photo['id']
        }

    except Exception as e:
        print(f"    ❌ Unsplash API error: {e}")
        return None

def download_image(image_info: Dict, output_path: Path, api_key: str) -> bool:
    """Download image from Unsplash"""
    try:
        response = requests.get(image_info['url'], timeout=30)
        response.raise_for_status()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.content)

        # Trigger Unsplash download event
        if image_info.get('download_url'):
            requests.get(
                image_info['download_url'],
                headers={"Authorization": f"Client-ID {api_key}"},
                timeout=5
            )

        return True
    except Exception as e:
        print(f"    ❌ Download failed: {e}")
        return False

def update_post(post_path: Path, new_image_path: str, image_credit: Dict) -> bool:
    """Update post with new image"""
    try:
        with open(post_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace placeholder image path
        content = re.sub(
            r'image: "/images/placeholder-[^"]+\.jpg"',
            f'image: "{new_image_path}"',
            content
        )

        # Remove old photo credit if exists
        content = re.sub(r'\n\n\*Photo by \[.*?\]\(.*?\) on \[Unsplash\]\(.*?\)\*\n?', '', content)

        # Add new photo credit
        credit_line = f"\n\n*Photo by [{image_credit['photographer']}]({image_credit['photographer_url']}) on [Unsplash]({image_credit['unsplash_url']})*\n"
        if not content.endswith('\n'):
            content += '\n'
        content += credit_line

        with open(post_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    except Exception as e:
        print(f"    ❌ Failed to update post: {e}")
        return False

def main():
    api_key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not api_key:
        print("❌ UNSPLASH_ACCESS_KEY not set")
        print("   This script must be run with Unsplash API access")
        sys.exit(1)

    print("🔍 Finding posts with placeholder images...")
    posts = find_posts_with_placeholders()

    if not posts:
        print("✅ No posts with placeholder images found")
        return

    print(f"📝 Found {len(posts)} post(s) with placeholders\n")

    fixed_count = 0
    failed_posts = []

    for post_path in posts:
        print(f"📄 Processing: {post_path.relative_to('content')}")

        # Extract title and category from frontmatter
        with open(post_path, 'r', encoding='utf-8') as f:
            content = f.read()

        title_match = re.search(r'title: "([^"]+)"', content)
        category_match = re.search(r'categories: \["([^"]+)"\]', content)

        if not title_match or not category_match:
            print(f"  ⚠️  Could not extract title/category, skipping")
            failed_posts.append(str(post_path))
            continue

        title = title_match.group(1)
        category = category_match.group(1)

        # Fetch new image
        image_info = fetch_unsplash_image(title, category, api_key)
        if not image_info:
            print(f"  ⚠️  Failed to fetch image, skipping")
            failed_posts.append(str(post_path))
            continue

        print(f"  ✓ Found image by {image_info['photographer']}")

        # Generate filename from post
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', post_path.stem)
        if date_match:
            base_name = post_path.stem
        else:
            base_name = f"20260120-{post_path.stem}"

        image_filename = f"{base_name}.jpg"
        image_path = Path("static/images") / image_filename

        # Download image
        if not download_image(image_info, image_path, api_key):
            print(f"  ⚠️  Failed to download, skipping")
            failed_posts.append(str(post_path))
            continue

        print(f"  ✓ Downloaded: {image_path}")

        # Update post
        relative_path = f"/images/{image_filename}"
        if update_post(post_path, relative_path, image_info):
            print(f"  ✅ Updated post\n")
            fixed_count += 1
        else:
            failed_posts.append(str(post_path))

    print(f"\n{'='*60}")
    print(f"✅ Fixed {fixed_count}/{len(posts)} posts")
    if failed_posts:
        print(f"⚠️  Failed posts:")
        for fp in failed_posts:
            print(f"   - {fp}")

if __name__ == "__main__":
    main()
