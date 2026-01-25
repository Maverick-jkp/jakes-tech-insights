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
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            safe_print(f"  ❌ ERROR: File not found: {filepath}")
            return {
                "file": str(filepath),
                "language": "unknown",
                "critical_failures": [f"File not found: {filepath}"],
                "warnings": [],
                "info": {}
            }
        except IOError as e:
            safe_print(f"  ❌ ERROR: Cannot read file: {filepath}")
            safe_print(f"     Error: {str(e)}")
            return {
                "file": str(filepath),
                "language": "unknown",
                "critical_failures": [f"Cannot read file: {str(e)}"],
                "warnings": [],
                "info": {}
            }
        except Exception as e:
            safe_print(f"  ❌ ERROR: Unexpected error reading file: {filepath}")
            safe_print(f"     Error: {str(e)}")
            return {
                "file": str(filepath),
                "language": "unknown",
                "critical_failures": [f"Unexpected error: {str(e)}"],
                "warnings": [],
                "info": {}
            }

        # Parse frontmatter and body
        try:
            frontmatter, body = self._parse_markdown(content)
        except Exception as e:
            safe_print(f"  ⚠️  WARNING: Failed to parse markdown structure")
            safe_print(f"     File: {filepath}")
            safe_print(f"     Error: {str(e)}")
            frontmatter = {}
            body = content

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
        self._check_date_consistency(frontmatter, filepath, checks)
        self._check_duplicate_topic(frontmatter, filepath, checks)
        self._check_title_content_consistency(frontmatter, body, checks)
        self._check_clickbait(frontmatter, body, checks)

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

    def _check_date_consistency(self, frontmatter: Dict, filepath: Path, checks: Dict):
        """Check year consistency between filename, frontmatter, and title"""
        # Extract year from filename (format: YYYY-MM-DD-*.md)
        filename = filepath.name
        filename_year_match = re.match(r'(\d{4})-\d{2}-\d{2}', filename)

        if not filename_year_match:
            # No date in filename, skip this check
            return

        filename_year = int(filename_year_match.group(1))

        # Extract year from frontmatter date
        frontmatter_year = None
        if 'date' in frontmatter:
            date_str = frontmatter['date']
            # Try to extract year from various date formats
            date_year_match = re.match(r'(\d{4})', date_str)
            if date_year_match:
                frontmatter_year = int(date_year_match.group(1))

        # Extract years from title
        title_years = []
        if 'title' in frontmatter:
            title = frontmatter['title']
            # Match 4-digit years (2020-2030 range)
            title_year_matches = re.findall(r'20[2-3][0-9]', title)
            title_years = [int(y) for y in title_year_matches]

        # Validate consistency
        errors = []

        # Check if title years are older than filename year
        if title_years:
            oldest_title_year = min(title_years)
            if oldest_title_year < filename_year:
                errors.append(
                    f"Title contains outdated year {oldest_title_year} "
                    f"(e.g., '{oldest_title_year}年最新' or 'Latest {oldest_title_year}') "
                    f"but filename is dated {filename_year}. "
                    f"Update title to use {filename_year}."
                )

        # Check if frontmatter year mismatches filename year
        if frontmatter_year and frontmatter_year != filename_year:
            errors.append(
                f"Frontmatter date year {frontmatter_year} doesn't match "
                f"filename year {filename_year}"
            )

        # Add errors as critical failures
        for error in errors:
            checks['critical_failures'].append(f"Date mismatch: {error}")

        # Add info
        checks['info']['filename_year'] = filename_year
        checks['info']['title_years'] = title_years if title_years else None
        checks['info']['frontmatter_year'] = frontmatter_year

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

    def _check_duplicate_topic(self, frontmatter: Dict, filepath: Path, checks: Dict):
        """Check for duplicate topics in recent posts (CRITICAL)"""
        # Extract keyword from current file
        filename = filepath.stem
        # Remove YYYY-MM-DD- prefix to get keyword
        parts = filename.split('-')
        if len(parts) >= 4:
            keyword = '-'.join(parts[3:])
        else:
            keyword = filename

        # Get language from filepath
        lang = checks['language']

        # Find all posts in the same language from the last 7 days
        content_dir = Path(f"content/{lang}")
        if not content_dir.exists():
            return

        # Get current file date and title
        current_date = frontmatter.get('date', '')
        current_title = frontmatter.get('title', '').lower()

        if not current_date or not current_title:
            return

        from datetime import datetime, timedelta
        try:
            current_dt = datetime.fromisoformat(current_date.replace('Z', '+00:00'))
            cutoff_date = current_dt - timedelta(days=7)
        except (ValueError, AttributeError):
            return

        # Check for duplicates
        keyword_duplicates = []
        title_duplicates = []

        for md_file in content_dir.rglob('*.md'):
            if md_file == filepath:
                continue

            # Extract keyword from other file
            other_filename = md_file.stem
            other_parts = other_filename.split('-')
            if len(other_parts) >= 4:
                other_keyword = '-'.join(other_parts[3:])
            else:
                other_keyword = other_filename

            # Check if keywords match
            if other_keyword == keyword:
                # Check date to see if it's within 7 days
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Extract frontmatter date
                    if content.startswith('---'):
                        fm_match = re.search(r'date:\s*(.+)', content)
                        title_match = re.search(r'title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)

                        if fm_match:
                            other_date = fm_match.group(1).strip().strip('"').strip("'")
                            other_dt = datetime.fromisoformat(other_date.replace('Z', '+00:00'))

                            if other_dt >= cutoff_date:
                                keyword_duplicates.append(str(md_file))

                                # Check title similarity
                                if title_match:
                                    other_title = title_match.group(1).strip().lower()
                                    similarity = self._calculate_title_similarity(current_title, other_title)

                                    # If titles are >70% similar, it's likely a duplicate
                                    if similarity > 0.7:
                                        title_duplicates.append((str(md_file), similarity))
                except Exception:
                    continue

        if keyword_duplicates:
            checks['critical_failures'].append(
                f"Duplicate keyword '{keyword}' found in recent posts (last 7 days): {', '.join([Path(d).name for d in keyword_duplicates])}"
            )

        if title_duplicates:
            dup_details = ', '.join([f"{Path(d).name} ({sim*100:.0f}% similar)" for d, sim in title_duplicates])
            checks['critical_failures'].append(
                f"Similar title detected: {dup_details}"
            )

    def _calculate_title_similarity(self, title1: str, title2: str) -> float:
        """Calculate similarity between two titles using Levenshtein distance"""
        # Normalize titles
        t1 = title1.lower().strip()
        t2 = title2.lower().strip()

        if t1 == t2:
            return 1.0

        # Levenshtein distance
        len1, len2 = len(t1), len(t2)
        if len1 == 0 or len2 == 0:
            return 0.0

        # Create distance matrix
        distances = [[0] * (len2 + 1) for _ in range(len1 + 1)]

        for i in range(len1 + 1):
            distances[i][0] = i
        for j in range(len2 + 1):
            distances[0][j] = j

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                cost = 0 if t1[i-1] == t2[j-1] else 1
                distances[i][j] = min(
                    distances[i-1][j] + 1,      # deletion
                    distances[i][j-1] + 1,      # insertion
                    distances[i-1][j-1] + cost  # substitution
                )

        max_len = max(len1, len2)
        distance = distances[len1][len2]

        # Convert to similarity (0-1)
        similarity = 1 - (distance / max_len)
        return similarity

    def _check_title_content_consistency(self, frontmatter: Dict, body: str, checks: Dict):
        """Check if title matches content (CRITICAL)"""
        title = frontmatter.get('title', '').lower()
        body_lower = body.lower()

        if not title:
            return

        # Extract main keywords from title (remove common words)
        common_words = {
            'en': {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during'},
            'ko': {'의', '이', '가', '을', '를', '에', '와', '과', '도', '는', '은', '까지', '부터', '에서'},
            'ja': {'の', 'に', 'を', 'は', 'が', 'で', 'と', 'から', 'まで', 'より', 'へ'}
        }

        lang = checks['language']
        stop_words = common_words.get(lang, set())

        # Split title into words and filter
        title_words = re.findall(r'\w+', title)
        significant_words = [w for w in title_words if w not in stop_words and len(w) > 2]

        if not significant_words:
            return

        # Check if at least 30% of title keywords appear in body
        matches = sum(1 for word in significant_words if word in body_lower)
        match_ratio = matches / len(significant_words)

        if match_ratio < 0.3:
            checks['critical_failures'].append(
                f"Title-content mismatch: Only {match_ratio*100:.0f}% of title keywords found in body (expected >30%)"
            )

        # Additional check: detect obvious topic mismatch using category
        category = frontmatter.get('categories', [''])[0] if 'categories' in frontmatter else ''
        description = frontmatter.get('description', '').lower()

        # If title suggests one topic but description/content suggests another
        # Example: Title mentions celebrity name but content is about finance
        if category == 'finance' and any(keyword in title for keyword in ['음악', 'music', '아이돌', 'idol', '가수', 'singer']):
            if '암호화폐' in body_lower or 'crypto' in body_lower or '투자' in body_lower or 'trading' in body_lower:
                checks['critical_failures'].append(
                    "Suspected clickbait: Title suggests entertainment/celebrity content but body is about finance/crypto"
                )

    def _check_clickbait(self, frontmatter: Dict, body: str, checks: Dict):
        """Detect clickbait and SEO manipulation (CRITICAL)"""
        title = frontmatter.get('title', '')
        description = frontmatter.get('description', '')

        # Pattern 1: Title mentions person/celebrity but content doesn't
        celebrity_patterns = {
            'ko': r'(강타|김연아|김연경|손흥민|아이유|방탄소년단)',
            'ja': r'(芸能人|アイドル|歌手)',
            'en': r'(celebrity|star|singer|idol)'
        }

        lang = checks['language']
        pattern = celebrity_patterns.get(lang)

        if pattern and re.search(pattern, title, re.IGNORECASE):
            # Check if the mentioned entity appears in body
            matches = re.findall(pattern, title, re.IGNORECASE)
            for match in matches:
                # If title mentions celebrity but body doesn't discuss them
                if match not in body and len(body) > 500:
                    # Exception: if it's actually about that person
                    body_lower = body.lower()
                    match_lower = match.lower()

                    # Count occurrences in body
                    occurrences = body_lower.count(match_lower)

                    if occurrences < 2:  # Should mention at least twice if title is about them
                        checks['critical_failures'].append(
                            f"Clickbait detected: Title mentions '{match}' but content barely discusses this topic"
                        )

        # Pattern 2: Meta description doesn't match content
        if description and len(body) > 300:
            # Extract first 300 chars of body
            body_preview = body[:300].lower()
            desc_lower = description.lower()

            # Get significant words from description
            desc_words = re.findall(r'\w+', desc_lower)
            desc_words = [w for w in desc_words if len(w) > 3][:5]  # Top 5 significant words

            if desc_words:
                matches = sum(1 for word in desc_words if word in body_preview)
                if matches < len(desc_words) * 0.3:
                    checks['warnings'].append(
                        "Meta description may not accurately reflect content"
                    )

    def _add_info(self, body: str, frontmatter: Dict, checks: Dict):
        """Add additional info"""
        # Count headings
        headings = re.findall(r'^##+ .+$', body, re.MULTILINE)
        checks['info']['heading_count'] = len(headings)

        # Title
        checks['info']['title'] = frontmatter.get('title', 'N/A')


def return_failed_topics_to_queue(failed_files: List[str]):
    """Return failed topics back to available status in the queue"""
    queue_path = Path("data/topics_queue.json")

    if not queue_path.exists():
        return

    try:
        with open(queue_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        queue = data.get('topics', [])

        # Extract topic IDs from failed files
        for filepath in failed_files:
            path = Path(filepath)
            filename = path.stem

            # Extract keyword from filename (YYYY-MM-DD-keyword)
            parts = filename.split('-')
            if len(parts) >= 4:
                keyword = '-'.join(parts[3:])

                # Get language from filepath
                if '/en/' in str(filepath):
                    lang = 'en'
                elif '/ko/' in str(filepath):
                    lang = 'ko'
                elif '/ja/' in str(filepath):
                    lang = 'ja'
                else:
                    continue

                # Find and reset the topic
                for topic in queue:
                    if (topic.get('keyword') == keyword and
                        topic.get('lang') == lang and
                        topic.get('status') in ['in_progress', 'completed']):

                        topic['status'] = 'pending'  # Changed from 'available' to 'pending'
                        topic['reserved_at'] = None
                        if 'completed_at' in topic:
                            del topic['completed_at']
                        break

        # Save updated queue
        with open(queue_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    except Exception as e:
        safe_print(f"     ⚠️ Error returning topics to queue: {str(e)}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Quality Gate for generated content")
    parser.add_argument('--strict', action='store_true', help="Strict mode (warnings become failures)")
    args = parser.parse_args()

    # Load generated files list
    generated_files_path = Path("generated_files.json")

    if not generated_files_path.exists():
        safe_print("❌ ERROR: generated_files.json not found")
        safe_print("   Run generate_posts.py first to create content")
        safe_print("   Expected path: generated_files.json")
        sys.exit(1)

    try:
        with open(generated_files_path, 'r') as f:
            generated_files = json.load(f)
    except json.JSONDecodeError as e:
        safe_print(f"❌ ERROR: Invalid JSON in generated_files.json")
        safe_print(f"   Error: {str(e)}")
        safe_print(f"   The file may be corrupted")
        sys.exit(1)
    except IOError as e:
        safe_print(f"❌ ERROR: Cannot read generated_files.json")
        safe_print(f"   Error: {str(e)}")
        sys.exit(1)

    if not generated_files:
        safe_print("⚠️  No files to check in generated_files.json")
        safe_print("   This is not an error - the file list is empty")
        sys.exit(0)

    # Initialize quality gate
    qg = QualityGate(strict_mode=args.strict)

    safe_print(f"\n{'='*60}")
    safe_print(f"  Quality Gate - Checking {len(generated_files)} files")
    safe_print(f"{'='*60}\n")

    all_results = []
    passed_files = []
    failed_files = []
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
            failed_files.append(filepath)
            safe_print(f"  ❌ FAILURES:")
            for failure in result['critical_failures']:
                safe_print(f"     - {failure}")
        else:
            passed_files.append(filepath)

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
        safe_print("")

    # Handle failed files
    if failed_files:
        safe_print(f"\n{'='*60}")
        safe_print(f"  ⚠️ Processing Failed Files")
        safe_print(f"{'='*60}\n")

        for filepath in failed_files:
            path = Path(filepath)
            safe_print(f"  🗑️ Deleting: {path.name}")

            # Delete the markdown file
            try:
                if path.exists():
                    path.unlink()
                    safe_print(f"     ✓ Deleted {path.name}")
            except Exception as e:
                safe_print(f"     ⚠️ Failed to delete {path.name}: {str(e)}")

            # Delete associated image
            try:
                # Extract date and keyword from filename
                filename = path.stem
                parts = filename.split('-')
                if len(parts) >= 4:
                    date_keyword = filename  # e.g., "2026-01-24-keyword"
                    image_path = Path(f"static/images/{date_keyword}.jpg")
                    if image_path.exists():
                        image_path.unlink()
                        safe_print(f"     ✓ Deleted image: {image_path.name}")
            except Exception as e:
                safe_print(f"     ⚠️ Failed to delete image: {str(e)}")

        # Return failed topics to queue
        safe_print(f"\n  🔄 Returning {len(failed_files)} topics to queue...")
        return_failed_topics_to_queue(failed_files)
        safe_print(f"     ✓ Topics returned to available status\n")

    # Summary
    safe_print(f"{'='*60}")
    safe_print(f"  Summary")
    safe_print(f"{'='*60}")
    safe_print(f"Files checked: {len(all_results)}")
    safe_print(f"Passed: {len(passed_files)}")
    safe_print(f"Failed: {len(failed_files)}")
    safe_print(f"Critical failures: {total_failures}")
    safe_print(f"Warnings: {total_warnings}")

    # Save passed files list (for workflow to commit)
    passed_files_path = Path("passed_files.json")
    try:
        with open(passed_files_path, 'w') as f:
            json.dump(passed_files, f, indent=2)
        safe_print(f"\n✓ Passed files list saved to: {passed_files_path}")
    except IOError as e:
        safe_print(f"\n⚠️  WARNING: Failed to save passed files list")
        safe_print(f"   Path: {passed_files_path}")
        safe_print(f"   Error: {str(e)}")

    # Save detailed report
    report_path = Path("quality_report.json")
    try:
        with open(report_path, 'w') as f:
            json.dump({
                "summary": {
                    "total_files": len(all_results),
                    "passed_files": len(passed_files),
                    "failed_files": len(failed_files),
                    "total_failures": total_failures,
                    "total_warnings": total_warnings
                },
                "passed_files": passed_files,
                "failed_files": failed_files,
                "results": all_results
            }, f, indent=2)
        safe_print(f"✓ Detailed report saved to: {report_path}")
    except IOError as e:
        safe_print(f"\n⚠️  WARNING: Failed to save quality report")
        safe_print(f"   Path: {report_path}")
        safe_print(f"   Error: {str(e)}")
        safe_print(f"   Continuing anyway...")

    # Exit code: Success if at least one file passed
    if len(passed_files) > 0:
        safe_print(f"\n✅ Quality Gate: PASSED ({len(passed_files)} file(s))")
        sys.exit(0)
    else:
        safe_print(f"\n❌ Quality Gate: FAILED (all {len(failed_files)} file(s) failed)")
        sys.exit(1)


if __name__ == "__main__":
    main()
