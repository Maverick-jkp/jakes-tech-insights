#!/usr/bin/env python3
"""
Fetch Unsplash images for existing posts with placeholder images.

This script finds all posts using placeholder SVG images and replaces them
with real Unsplash photos based on the post's keyword and category.

Usage:
    python scripts/fetch_images_for_posts.py
"""

import os
import sys
import re
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Unsplash API setup
UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")
if not UNSPLASH_ACCESS_KEY:
    print("❌ Error: UNSPLASH_ACCESS_KEY not set")
    print("   Set with: export UNSPLASH_ACCESS_KEY='your-key'")
    sys.exit(1)

# Keyword translations for Unsplash search
TRANSLATIONS = {
    # Korean
    '챗봇': 'chatbot', 'AI': 'artificial intelligence', '도입': 'implementation',
    '실패': 'failure', '이유': 'reasons', '스타트업': 'startup', '투자': 'investment',
    '전략': 'strategy', '디지털': 'digital', '노마드': 'nomad', '라이프': 'lifestyle',
    '미니멀': 'minimalism', '트렌드': 'trends',
    # Japanese
    'AIコーディング': 'AI coding', 'アシスタント': 'assistant', 'スタートアップ': 'startup',
    '資金調達': 'fundraising', '戦略': 'strategy', 'デジタル': 'digital',
    'ノマド': 'nomad', 'トレンド': 'trends', 'ミニマリズム': 'minimalism'
}

def translate_to_english(text):
    """Translate non-English keywords to English for Unsplash search"""
    # Remove year patterns
    text = re.sub(r'20[2-3][0-9]년?', '', text)
    text = re.sub(r'【.*?】', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = text.strip()

    # Split and translate
    words = text.split()
    translated = []
    for word in words:
        if word in TRANSLATIONS:
            translated.append(TRANSLATIONS[word])
        else:
            # Check for substring matches
            found = False
            for kr, en in TRANSLATIONS.items():
                if kr in word:
                    translated.append(en)
                    found = True
                    break
            if not found:
                try:
                    word.encode('ascii')
                    translated.append(word)
                except UnicodeEncodeError:
                    pass

    return ' '.join(translated) if translated else 'technology'

def fetch_unsplash_image(keyword, category):
    """Fetch image from Unsplash API"""
    # Clean and translate keyword
    english_query = translate_to_english(keyword)
    query = f"{category} {english_query}".strip()

    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    params = {
        "query": query,
        "per_page": 5,
        "orientation": "landscape"
    }

    print(f"  🔍 Searching Unsplash for: {query}")

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get('results'):
            print(f"  ⚠️  No images found, trying category only...")
            # Fallback to category-only search
            params['query'] = category
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data.get('results'):
                print(f"  ❌ Still no images found")
                return None

        photo = data['results'][0]

        return {
            'url': photo['urls']['regular'],
            'download_url': photo['links']['download_location'],
            'photographer': photo['user']['name'],
            'photographer_url': photo['user']['links']['html'],
            'unsplash_url': photo['links']['html']
        }

    except Exception as e:
        print(f"  ❌ Error fetching image: {e}")
        return None

def download_image(image_url, output_path):
    """Download image from URL"""
    try:
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.content)

        return True
    except Exception as e:
        print(f"  ❌ Download failed: {e}")
        return False

def parse_frontmatter(content):
    """Extract frontmatter from markdown content"""
    if not content.startswith('---'):
        return {}, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content

    frontmatter_text = parts[1]
    body = parts[2]

    frontmatter = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip().strip('"').strip("'")

    return frontmatter, body

def process_post(post_path):
    """Process a single post file"""
    print(f"\n📄 Processing: {post_path.name}")

    # Read post content
    content = post_path.read_text(encoding='utf-8')
    frontmatter, body = parse_frontmatter(content)

    # Check if using placeholder
    image_path = frontmatter.get('image', '')
    if 'placeholder' not in image_path:
        print(f"  ℹ️  Already has real image: {image_path}")
        return False

    # Extract info from frontmatter
    title = frontmatter.get('title', '')
    categories = frontmatter.get('categories', '["tech"]')

    # Parse category
    category_match = re.search(r'\["?(\w+)"?\]', categories)
    category = category_match.group(1) if category_match else 'tech'

    # Extract keyword from filename or title
    filename = post_path.stem
    # Remove date prefix (YYYY-MM-DD-)
    keyword = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename)

    print(f"  📝 Title: {title[:50]}...")
    print(f"  🏷️  Category: {category}")
    print(f"  🔑 Keyword: {keyword}")

    # Fetch image
    image_info = fetch_unsplash_image(keyword, category)
    if not image_info:
        print(f"  ⏭️  Skipping (no image found)")
        return False

    print(f"  ✓ Found image by {image_info['photographer']}")

    # Generate image filename (use date from filename if available)
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if date_match:
        date_str = date_match.group(1).replace('-', '')
    else:
        date_str = datetime.now().strftime('%Y%m%d')

    # Sanitize keyword for filename
    safe_keyword = re.sub(r'[^\w\-]', '', keyword)[:30]
    image_filename = f"{date_str}-{safe_keyword}.jpg"
    image_output_path = Path(f"/Users/jakepark/projects/jakes-tech-insights/static/images/{image_filename}")

    # Download image
    print(f"  ⬇️  Downloading to: {image_filename}")
    if not download_image(image_info['url'], image_output_path):
        return False

    # Update frontmatter
    new_image_path = f"/images/{image_filename}"
    content = content.replace(image_path, new_image_path)

    # Write updated content
    post_path.write_text(content, encoding='utf-8')

    print(f"  ✅ Updated post with new image: {new_image_path}")

    # Trigger download tracking (Unsplash requirement)
    try:
        requests.get(image_info['download_url'], headers={
            "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
        }, timeout=5)
    except:
        pass

    return True

def main():
    """Main function"""
    print("🖼️  Fetching Unsplash images for posts with placeholders\n")

    # Find all markdown files in content directory
    content_dir = Path("/Users/jakepark/projects/jakes-tech-insights/content")
    markdown_files = list(content_dir.rglob("*.md"))

    print(f"Found {len(markdown_files)} markdown files\n")

    updated_count = 0
    skipped_count = 0

    for post_path in markdown_files:
        try:
            if process_post(post_path):
                updated_count += 1
            else:
                skipped_count += 1
        except Exception as e:
            print(f"  ❌ Error processing {post_path.name}: {e}")
            skipped_count += 1

    print(f"\n{'='*60}")
    print(f"✅ Complete!")
    print(f"   Updated: {updated_count}")
    print(f"   Skipped: {skipped_count}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
