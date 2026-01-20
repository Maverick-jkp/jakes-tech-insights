#!/usr/bin/env python3
"""
Quality Gate - Content Quality Checker

Validates generated content against quality criteria.
Returns PASS/FAIL with detailed report.

Usage:
    python quality_gate.py
    python quality_gate.py --strict
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.security import safe_print, mask_secrets


class QualityGate:
    def __init__(self, strict_mode: bool = False):
        self.strict_mode = strict_mode

        # AI phrases to detect
        self.ai_phrases = {
            "en": [
                "it's important to note",
                "it is important to",
                "certainly",
                "moreover",
                "furthermore",
                "in conclusion",
                "to summarize",
                "in summary",
                "revolutionary",
                "game-changer",
                "cutting-edge",
                "state-of-the-art",
                "leverage",
                "synergy"
            ],
            "ko": [
                "물론",
                "~할 수 있습니다",
                "중요합니다",
                "혁신적",
                "게임체인저",
                "주목할만한",
                "~하는 것이 중요하다"
            ],
            "ja": [
                "もちろん",
                "重要です",
                "革新的",
                "ゲームチェンジャー",
                "注目すべき"
            ]
        }

    def check_file(self, filepath: Path) -> Dict:
        """Check a single markdown file"""

        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse frontmatter and body
        frontmatter, body = self._parse_markdown(content)

        # Detect language from filepath
        lang = self._detect_language(filepath)

        # Run checks
        checks = {
            "file": str(filepath),
            "language": lang,
            "critical_failures": [],
            "warnings": [],
            "info": {}
        }

        # CRITICAL checks (FAIL)
        self._check_word_count(body, checks)
        self._check_ai_phrases(body, lang, checks)
        self._check_frontmatter(frontmatter, checks)

        # WARNING checks (don't fail, just warn)
        self._check_links(body, checks)
        self._check_readability(body, checks)
        self._check_image(frontmatter, checks)

        # Info
        self._add_info(body, frontmatter, checks)

        return checks

    def _parse_markdown(self, content: str) -> Tuple[Dict, str]:
        """Parse frontmatter and body"""
        if not content.startswith('---'):
            return {}, content

        parts = content.split('---', 2)
        if len(parts) < 3:
            return {}, content

        # Parse frontmatter (simple key: value)
        frontmatter = {}
        for line in parts[1].strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip().strip('"').strip("'")

        body = parts[2].strip()
        return frontmatter, body

    def _detect_language(self, filepath: Path) -> str:
        """Detect language from filepath"""
        path_str = str(filepath)
        if '/ko/' in path_str:
            return 'ko'
        elif '/ja/' in path_str:
            return 'ja'
        return 'en'

    def _check_word_count(self, body: str, checks: Dict):
        """Check if word count is within range"""
        lang = checks['language']

        # Remove markdown syntax for accurate count
        clean_text = re.sub(r'[#*`\[\]()_]', '', body)

        # Japanese and Korean use character count instead of word count
        if lang in ['ja', 'ko']:
            # Count all non-whitespace characters
            char_count = len(re.sub(r'\s+', '', clean_text))
            checks['info']['char_count'] = char_count
            checks['info']['word_count'] = f"{char_count} chars"

            if lang == 'ja':
                # Japanese: Target 2800-4200, WARN if outside range
                if char_count < 2200:
                    checks['warnings'].append(
                        f"Character count too low: {char_count} chars (recommended: 2200+)"
                    )
                elif 2200 <= char_count < 2800:
                    checks['warnings'].append(
                        f"Character count on the lower end: {char_count} chars (target: 2800-4200)"
                    )
                elif 4200 <= char_count <= 7000:
                    checks['warnings'].append(
                        f"Character count high: {char_count} chars (target: 2800-4200, Editor should compress)"
                    )
                elif char_count > 11000:
                    checks['warnings'].append(
                        f"Character count extremely high: {char_count} chars (strongly recommend compressing)"
                    )
            else:  # ko
                # Korean: Target 2000-3200, WARN if outside range
                # (Korean has ~20% fewer chars than Japanese for same reading time)
                if char_count < 1500:
                    checks['warnings'].append(
                        f"Character count too low: {char_count} chars (recommended: 1500+)"
                    )
                elif 1500 <= char_count < 2000:
                    checks['warnings'].append(
                        f"Character count on the lower end: {char_count} chars (target: 2000-3200)"
                    )
                elif 3200 <= char_count <= 5000:
                    checks['warnings'].append(
                        f"Character count high: {char_count} chars (target: 2000-3200, Editor should compress)"
                    )
                elif char_count > 8000:
                    checks['warnings'].append(
                        f"Character count extremely high: {char_count} chars (strongly recommend compressing)"
                    )
        else:
            # English uses word count
            words = clean_text.split()
            word_count = len(words)
            checks['info']['word_count'] = word_count

            # Target 700-1200, WARN if outside range
            if word_count < 500:
                checks['warnings'].append(
                    f"Word count too low: {word_count} words (recommended: 500+)"
                )
            elif 500 <= word_count < 700:
                checks['warnings'].append(
                    f"Word count on the lower end: {word_count} words (target: 700-1200)"
                )
            elif 1200 <= word_count <= 1800:
                checks['warnings'].append(
                    f"Word count high: {word_count} words (target: 700-1200, Editor should compress)"
                )
            elif word_count > 2500:
                checks['warnings'].append(
                    f"Word count extremely high: {word_count} words (strongly recommend compressing)"
                )

    def _check_ai_phrases(self, body: str, lang: str, checks: Dict):
        """Check for AI-sounding phrases"""
        body_lower = body.lower()

        phrases_to_check = self.ai_phrases.get(lang, self.ai_phrases['en'])
        found_phrases = []

        for phrase in phrases_to_check:
            if phrase.lower() in body_lower:
                found_phrases.append(phrase)

        checks['info']['ai_phrases_found'] = found_phrases

        # WARN if AI phrases found (not critical failure anymore)
        if found_phrases:
            checks['warnings'].append(
                f"AI phrases detected: {', '.join(found_phrases[:3])}{'...' if len(found_phrases) > 3 else ''}"
            )

    def _check_frontmatter(self, frontmatter: Dict, checks: Dict):
        """Check frontmatter completeness"""
        required_fields = ['title', 'date', 'categories', 'description']

        for field in required_fields:
            if field not in frontmatter or not frontmatter[field]:
                checks['critical_failures'].append(
                    f"Missing required frontmatter field: {field}"
                )

        # Check description length
        if 'description' in frontmatter:
            desc_len = len(frontmatter['description'])
            checks['info']['description_length'] = desc_len

            if desc_len < 120 or desc_len > 160:
                checks['warnings'].append(
                    f"Description length not optimal: {desc_len} chars (ideal: 120-160)"
                )

    def _check_links(self, body: str, checks: Dict):
        """Check for external links (WARNING only)"""
        # Count markdown links
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', body)
        link_count = len(links)

        checks['info']['link_count'] = link_count

        # Warn if no links (not a failure)
        if link_count < 2:
            checks['warnings'].append(
                f"Low link count: {link_count} (recommended: 2+)"
            )

    def _check_readability(self, body: str, checks: Dict):
        """Basic readability check"""
        # Count sentences
        sentences = re.split(r'[.!?]+', body)
        sentences = [s.strip() for s in sentences if s.strip()]

        # Average sentence length
        words = body.split()
        avg_sentence_length = len(words) / len(sentences) if sentences else 0

        checks['info']['avg_sentence_length'] = round(avg_sentence_length, 1)

        # Warn if sentences are too long
        if avg_sentence_length > 25:
            checks['warnings'].append(
                f"Sentences may be too long (avg: {avg_sentence_length:.1f} words)"
            )

    def _check_image(self, frontmatter: Dict, checks: Dict):
        """Check for featured image (WARNING only)"""
        has_image = 'image' in frontmatter and frontmatter['image']
        checks['info']['has_image'] = has_image

        # Warn if no image (not a failure)
        if not has_image:
            checks['warnings'].append(
                "No featured image (recommended for better engagement)"
            )

    def _add_info(self, body: str, frontmatter: Dict, checks: Dict):
        """Add additional info"""
        # Count headings
        headings = re.findall(r'^##+ .+$', body, re.MULTILINE)
        checks['info']['heading_count'] = len(headings)

        # Title
        checks['info']['title'] = frontmatter.get('title', 'N/A')


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Quality Gate for generated content")
    parser.add_argument('--strict', action='store_true', help="Strict mode (warnings become failures)")
    args = parser.parse_args()

    # Load generated files list
    generated_files_path = Path("generated_files.json")

    if not generated_files_path.exists():
        safe_print("Error: generated_files.json not found")
        safe_print("Run generate_posts.py first to create content")
        sys.exit(1)

    with open(generated_files_path, 'r') as f:
        generated_files = json.load(f)

    if not generated_files:
        safe_print("No files to check")
        sys.exit(0)

    # Initialize quality gate
    qg = QualityGate(strict_mode=args.strict)

    safe_print(f"\n{'='*60}")
    safe_print(f"  Quality Gate - Checking {len(generated_files)} files")
    safe_print(f"{'='*60}\n")

    all_results = []
    total_failures = 0
    total_warnings = 0

    for filepath in generated_files:
        path = Path(filepath)

        if not path.exists():
            safe_print(f"⚠️  File not found: {filepath}")
            continue

        safe_print(f"Checking: {path.name}")

        result = qg.check_file(path)
        all_results.append(result)

        # Print results
        if result['critical_failures']:
            total_failures += len(result['critical_failures'])
            safe_print(f"  ❌ FAILURES:")
            for failure in result['critical_failures']:
                safe_print(f"     - {failure}")

        if result['warnings']:
            total_warnings += len(result['warnings'])
            safe_print(f"  ⚠️  WARNINGS:")
            for warning in result['warnings']:
                safe_print(f"     - {warning}")

        if not result['critical_failures'] and not result['warnings']:
            safe_print(f"  ✅ PASS")

        # Print info
        info = result['info']
        safe_print(f"  📊 Info: {info['word_count']} words, {info['heading_count']} headings, {info.get('link_count', 0)} links")
        safe_print()

    # Summary
    safe_print(f"{'='*60}")
    safe_print(f"  Summary")
    safe_print(f"{'='*60}")
    safe_print(f"Files checked: {len(all_results)}")
    safe_print(f"Critical failures: {total_failures}")
    safe_print(f"Warnings: {total_warnings}")

    # Save detailed report
    report_path = Path("quality_report.json")
    with open(report_path, 'w') as f:
        json.dump({
            "summary": {
                "total_files": len(all_results),
                "total_failures": total_failures,
                "total_warnings": total_warnings
            },
            "results": all_results
        }, f, indent=2)

    safe_print(f"\nDetailed report saved to: {report_path}")

    # Exit code
    if total_failures > 0:
        safe_print("\n❌ Quality Gate: FAILED")
        sys.exit(1)
    else:
        safe_print("\n✅ Quality Gate: PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
