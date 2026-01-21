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

            if not has_references:
                posts_without_references += 1
                validation_errors.append(f"❌ No references: {filename}")
                print(f"  ❌ No references: {filename}")
            else:
                print(f"  ✓ Has references: {filename}")

            # Check 2: Placeholder images
            if 'placeholder-' in content:
                posts_with_placeholders += 1
                validation_errors.append(f"❌ Placeholder image: {filename}")
                print(f"  ❌ Placeholder image: {filename}")
            else:
                print(f"  ✓ Real image: {filename}")

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
    has_critical_issues = posts_without_references > 0 or posts_with_placeholders > 0

    if has_critical_issues:
        print("\n🚨 QUALITY GATE: FAILED\n")

        if posts_without_references > 0:
            print(f"❌ CRITICAL: {posts_without_references}/{len(generated_files)} posts lack references")
            print("   ROOT CAUSE: Google Custom Search API not configured")
            print("   FIX: Add GOOGLE_API_KEY and GOOGLE_CX to GitHub Secrets")
            print("   See: docs/API_SETUP_GUIDE.md\n")

        if posts_with_placeholders > 0:
            print(f"❌ CRITICAL: {posts_with_placeholders}/{len(generated_files)} posts use placeholder images")
            print("   ROOT CAUSE: Unsplash API key not configured")
            print("   FIX: Add UNSPLASH_ACCESS_KEY to GitHub Secrets")
            print("   See: docs/API_SETUP_GUIDE.md\n")

        print("=" * 60)
        print("WORKFLOW WILL FAIL - Fix API credentials before retrying")
        print("=" * 60 + "\n")

        # Exit with error code to fail CI/CD
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
