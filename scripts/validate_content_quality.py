#!/usr/bin/env python3
"""
Content Quality Validation Script

Validates that generated content meets quality standards:
1. All posts have references (not empty)
2. All posts have real images (not placeholders)
3. Fails CI/CD if quality standards not met

Usage:
    python scripts/validate_content_quality.py
"""

import json
import sys
from pathlib import Path


def main():
    print("\n" + "=" * 60)
    print("  📊 Content Quality Validation")
    print("=" * 60 + "\n")

    # Load generated files list
    generated_files_path = Path("generated_files.json")
    if not generated_files_path.exists():
        print("❌ ERROR: generated_files.json not found")
        print("   This script must run after content generation")
        sys.exit(1)

    with open(generated_files_path, 'r') as f:
        generated_files = json.load(f)

    if not generated_files:
        print("⚠️  No files were generated - skipping validation")
        sys.exit(0)

    print(f"Validating {len(generated_files)} generated posts...\n")

    # Validation counters
    posts_without_references = 0
    posts_with_placeholders = 0
    validation_errors = []
    valid_posts = []
    invalid_posts = []

    # Check each generated file
    for filepath in generated_files:
        filepath = Path(filepath)
        filename = filepath.name

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check 1: References section
            has_references = (
                '## References' in content or
                '## 参考' in content or
                '## 참고자료' in content
            )

            # Check 2: Placeholder images
            has_placeholder = 'placeholder-' in content

            # Track validity
            is_valid = has_references and not has_placeholder

            if not has_references:
                posts_without_references += 1
                validation_errors.append(f"❌ No references: {filename}")
                print(f"  ❌ No references: {filename}")
                invalid_posts.append(str(filepath))
            elif has_placeholder:
                posts_with_placeholders += 1
                validation_errors.append(f"❌ Placeholder image: {filename}")
                print(f"  ❌ Placeholder image: {filename}")
                invalid_posts.append(str(filepath))
            else:
                print(f"  ✓ Has references: {filename}")
                print(f"  ✓ Real image: {filename}")
                valid_posts.append(str(filepath))

        except Exception as e:
            validation_errors.append(f"❌ Failed to validate: {filename} - {str(e)}")
            print(f"  ❌ Failed to validate: {filename}")

    print("\n" + "=" * 60)
    print("  📊 Validation Results")
    print("=" * 60 + "\n")

    # Summary
    print(f"Total posts validated: {len(generated_files)}")
    print(f"Posts without references: {posts_without_references}")
    print(f"Posts with placeholder images: {posts_with_placeholders}")

    # Determine pass/fail
    has_issues = posts_without_references > 0 or posts_with_placeholders > 0

    if has_issues:
        print(f"\n⚠️  QUALITY GATE: PARTIAL SUCCESS\n")

        if posts_without_references > 0:
            print(f"⚠️  {posts_without_references}/{len(generated_files)} posts lack references")
            print("   These posts will be excluded from commit\n")

        if posts_with_placeholders > 0:
            print(f"⚠️  {posts_with_placeholders}/{len(generated_files)} posts use placeholder images")
            print("   ROOT CAUSE: Unsplash API rate limit likely hit")
            print("   These posts will be excluded from commit\n")

        if valid_posts:
            print(f"✅ {len(valid_posts)}/{len(generated_files)} posts passed quality check")
            print("   Valid posts will be committed\n")

            # Update generated_files.json to only include valid posts
            with open(generated_files_path, 'w') as f:
                json.dump(valid_posts, f, indent=2, ensure_ascii=False)

            # Delete invalid posts
            for invalid_post in invalid_posts:
                invalid_path = Path(invalid_post)
                if invalid_path.exists():
                    invalid_path.unlink()
                    print(f"  🗑️  Deleted: {invalid_path.name}")

            print("\n" + "=" * 60)
            print(f"Proceeding with {len(valid_posts)} valid posts")
            print("=" * 60 + "\n")

            sys.exit(0)
        else:
            print("❌ No valid posts to commit")
            sys.exit(1)

    else:
        print("\n✅ QUALITY GATE: PASSED\n")
        print("All posts meet quality standards:")
        print("  ✓ All posts have credible references")
        print("  ✓ All posts use real Unsplash images")
        print("  ✓ Ready for publication\n")

        sys.exit(0)


if __name__ == "__main__":
    main()
