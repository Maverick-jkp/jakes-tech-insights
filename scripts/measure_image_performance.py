#!/usr/bin/env python3
"""
Measure image optimization impact.

Compares:
- Original: content/**/cover.jpg (source images)
- Generated: resources/_gen/images/**/* (Hugo-processed WebP + JPG)
"""
from pathlib import Path

def get_total_size(directory: Path, pattern: str) -> int:
    """Get total size of all files matching pattern."""
    total = 0
    count = 0
    if not directory.exists():
        return 0, 0

    for file in directory.rglob(pattern):
        total += file.stat().st_size
        count += 1
    return total, count

def format_size(bytes_size: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def main():
    content_dir = Path("content")
    resources_dir = Path("resources/_gen/images")

    print("=" * 70)
    print("📊 IMAGE OPTIMIZATION RESULTS")
    print("=" * 70)
    print()

    # Original source images (in page bundles)
    original_size, original_count = get_total_size(content_dir, "cover.jpg")

    print(f"📁 Source Images (Page Bundles)")
    print(f"   Location: content/**/cover.jpg")
    print(f"   Files: {original_count}")
    print(f"   Total Size: {format_size(original_size)}")
    print(f"   Avg Size: {format_size(original_size / original_count) if original_count > 0 else '0 B'}")
    print()

    if resources_dir.exists():
        # Hugo generated WebP images
        webp_size, webp_count = get_total_size(resources_dir, "*.webp")

        print(f"🎨 Generated WebP Images")
        print(f"   Location: resources/_gen/images/")
        print(f"   Files: {webp_count}")
        print(f"   Total Size: {format_size(webp_size)}")
        print(f"   Avg Size: {format_size(webp_size / webp_count) if webp_count > 0 else '0 B'}")
        print()

        # Hugo generated JPG fallbacks
        jpg_size, jpg_count = get_total_size(resources_dir, "*.jpg")

        print(f"📷 Generated JPG Fallbacks")
        print(f"   Files: {jpg_count}")
        print(f"   Total Size: {format_size(jpg_size)}")
        print(f"   Avg Size: {format_size(jpg_size / jpg_count) if jpg_count > 0 else '0 B'}")
        print()

        # Total generated
        total_generated = webp_size + jpg_size
        total_files = webp_count + jpg_count

        print(f"📦 Total Generated Images")
        print(f"   Files: {total_files} ({webp_count} WebP + {jpg_count} JPG)")
        print(f"   Total Size: {format_size(total_generated)}")
        print()

        # Savings calculation (comparing source to WebP only)
        if original_count > 0 and webp_count > 0:
            print("=" * 70)
            print("💰 OPTIMIZATION SAVINGS")
            print("=" * 70)
            print()

            # Average per-image comparison
            avg_original = original_size / original_count
            avg_webp = webp_size / webp_count
            avg_savings = ((avg_original - avg_webp) / avg_original * 100) if avg_original > 0 else 0

            print(f"   Average Original: {format_size(avg_original)}")
            print(f"   Average WebP: {format_size(avg_webp)}")
            print(f"   Average Savings: {avg_savings:.1f}%")
            print()

            # Multiple sizes generated from each source
            sizes_per_source = webp_count / original_count if original_count > 0 else 0
            print(f"   Responsive Variants: {sizes_per_source:.1f}x per image")
            print(f"   (Hugo generates multiple sizes for responsive display)")
            print()

        print("=" * 70)
        print("✅ BENEFITS")
        print("=" * 70)
        print()
        print("   ✓ WebP format: 60-80% smaller than original JPG")
        print("   ✓ Responsive images: Right size for each device")
        print("   ✓ Lazy loading: Faster initial page load")
        print("   ✓ JPG fallback: Compatible with all browsers")
        print()

    else:
        print("⚠️  No generated images found.")
        print("   Run 'hugo' or 'hugo server' to generate optimized images.")
        print()

    print("=" * 70)
    print("💡 Next Steps")
    print("=" * 70)
    print()
    print("   1. View site: http://localhost:1313")
    print("   2. Check Network tab in browser DevTools")
    print("   3. Verify WebP images are being served")
    print("   4. Test on mobile devices")
    print()

if __name__ == '__main__':
    main()
