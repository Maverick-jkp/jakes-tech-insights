#!/usr/bin/env python3
"""
Keyword Curator - Semi-automated keyword research for blog content

Generates keyword candidates using Claude API based on KEYWORD_STRATEGY.md
Provides interactive selection interface for human filtering (5 minutes weekly)

Usage:
    python scripts/keyword_curator.py
    python scripts/keyword_curator.py --count 15
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic package not installed")
    print("Install with: pip install anthropic")
    sys.exit(1)


CURATION_PROMPT = """역할:
너는 SEO 자동화 블로그를 위한 키워드 전략가다.
단, 일반적인 트렌드 키워드는 제외한다.

목표:
한국어 / 영어 / 일본어 각각에서
"결정 단계(Decision stage)"에 있는 사용자가
검색할 가능성이 높은 키워드만 제안하라.

금지:
- 단순 트렌드 요약 키워드
- 뉴스성 키워드
- 이미 대형 미디어가 점령한 키워드
- "2025 트렌드", "최신 동향" 같은 표현

우선순위 키워드 유형:
1. 트렌드 + 실제 사용 후 판단 (pros/cons, 언제 비효율적인가)
2. 트렌드의 한계, 실패 사례, 오해
3. 비교 키워드 (A vs B) 중 "결정 포인트" 중심
4. 지역/언어/문화 차이 관점
5. 1–3개월 후 검색될 가능성이 높은 후행 키워드

출력 형식:
언어별로 5개씩 제안하라. 반드시 JSON 형식으로만 응답하라.

[
  {
    "keyword": "키워드 문구",
    "language": "ko",
    "category": "tech",
    "search_intent": "왜 검색하는지 한 문장",
    "angle": "이 키워드를 다룰 때의 관점",
    "competition_level": "low",
    "why_it_works": "이 키워드가 자동화 블로그에 적합한 이유",
    "keyword_type": "trend",
    "priority": 7
  }
]

중요:
- keyword_type은 "trend" 또는 "evergreen" 중 하나
- category는 "tech", "business", "lifestyle" 중 하나
- language는 "en", "ko", "ja" 중 하나
- competition_level은 "low", "medium", "high" 중 하나
- priority는 1-10 사이의 숫자 (높을수록 우선순위 높음)
- 지금 시점(2026년 1월)에서 현실적인 키워드만 제안
- 예시는 절대 사용하지 말고, 실제 검색 가능성이 높은 키워드만 제안

각 언어별 5개씩 총 15개를 JSON 배열로 출력하라."""


class KeywordCurator:
    def __init__(self, api_key: str = None):
        """Initialize keyword curator with Claude API"""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")

        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"

        # Load existing queue
        self.queue_path = Path("data/topics_queue.json")
        self.queue_data = self._load_queue()

    def _load_queue(self) -> Dict:
        """Load existing topic queue"""
        if not self.queue_path.exists():
            return {"topics": []}

        with open(self.queue_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_queue(self):
        """Save updated topic queue"""
        with open(self.queue_path, 'w', encoding='utf-8') as f:
            json.dump(self.queue_data, f, indent=2, ensure_ascii=False)

    def generate_candidates(self, count: int = 15) -> List[Dict]:
        """Generate keyword candidates using Claude API"""
        print(f"\n{'='*60}")
        print(f"  🔍 Generating {count} keyword candidates...")
        print(f"{'='*60}\n")

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{
                "role": "user",
                "content": CURATION_PROMPT
            }]
        )

        # Parse JSON response
        content = response.content[0].text.strip()

        # Extract JSON from markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        try:
            candidates = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON response: {e}")
            print(f"Raw response:\n{content[:500]}")
            sys.exit(1)

        print(f"✅ Generated {len(candidates)} candidates\n")
        return candidates

    def display_candidates(self, candidates: List[Dict]):
        """Display candidates with numbered list"""
        print(f"{'='*60}")
        print(f"  📋 Keyword Candidates")
        print(f"{'='*60}\n")

        # Group by language
        by_lang = {"en": [], "ko": [], "ja": []}
        for c in candidates:
            lang = c.get("language", "en")
            by_lang[lang].append(c)

        idx = 1
        lang_names = {"en": "English", "ko": "Korean", "ja": "Japanese"}

        for lang in ["en", "ko", "ja"]:
            if by_lang[lang]:
                print(f"\n[{lang_names[lang]}]")
                print("-" * 60)

                for candidate in by_lang[lang]:
                    type_emoji = "🔥" if candidate.get("keyword_type") == "trend" else "🌲"
                    comp_emoji = {
                        "low": "🟢",
                        "medium": "🟡",
                        "high": "🔴"
                    }.get(candidate.get("competition_level", "medium"), "⚪")

                    print(f"\n{idx}. {type_emoji} {candidate['keyword']}")
                    print(f"   Category: {candidate['category']} | Competition: {comp_emoji} {candidate.get('competition_level', 'N/A')}")
                    print(f"   Intent: {candidate['search_intent']}")
                    print(f"   Angle: {candidate['angle']}")
                    print(f"   Why: {candidate.get('why_it_works', 'N/A')[:80]}...")

                    idx += 1

        print(f"\n{'='*60}\n")

    def interactive_selection(self, candidates: List[Dict]) -> List[Dict]:
        """Interactive selection of keywords"""
        print("어떤 키워드를 큐에 추가할까요?")
        print("숫자를 쉼표로 구분해서 입력하세요 (예: 1,3,5,7,10)")
        print("또는 'all'을 입력하면 전부 추가됩니다.")
        print("'q'를 입력하면 취소합니다.\n")

        while True:
            user_input = input("선택: ").strip()

            if user_input.lower() == 'q':
                print("❌ 취소되었습니다.")
                return []

            if user_input.lower() == 'all':
                return candidates

            try:
                # Parse selected indices
                selected_indices = [int(x.strip()) for x in user_input.split(',')]

                # Validate indices
                if any(idx < 1 or idx > len(candidates) for idx in selected_indices):
                    print(f"⚠️  잘못된 번호입니다. 1-{len(candidates)} 범위로 입력하세요.\n")
                    continue

                # Convert to 0-based index and return selected candidates
                selected = [candidates[idx - 1] for idx in selected_indices]
                return selected

            except ValueError:
                print("⚠️  잘못된 형식입니다. 예: 1,3,5\n")

    def add_to_queue(self, selected: List[Dict]):
        """Add selected keywords to topic queue"""
        if not selected:
            print("선택된 키워드가 없습니다.")
            return

        print(f"\n{'='*60}")
        print(f"  💾 큐에 {len(selected)}개 키워드 추가 중...")
        print(f"{'='*60}\n")

        # Get next ID
        existing_ids = [int(t['id'].split('-')[0]) for t in self.queue_data['topics'] if t['id'].split('-')[0].isdigit()]
        next_id = max(existing_ids) + 1 if existing_ids else 1

        added_count = 0
        for candidate in selected:
            # Generate topic ID
            topic_id = f"{next_id:03d}-{candidate['language']}-{candidate['category']}-{candidate['keyword'][:20].replace(' ', '-')}"

            # Create topic entry
            topic = {
                "id": topic_id,
                "keyword": candidate['keyword'],
                "category": candidate['category'],
                "lang": candidate['language'],
                "priority": candidate.get('priority', 7),
                "status": "pending",
                "created_at": datetime.now().isoformat(),
                "retry_count": 0,
                "keyword_type": candidate.get('keyword_type', 'evergreen'),
                "search_intent": candidate.get('search_intent', ''),
                "angle": candidate.get('angle', ''),
                "competition_level": candidate.get('competition_level', 'medium')
            }

            # Add expiry_days for trend keywords
            if topic['keyword_type'] == 'trend':
                topic['expiry_days'] = 21  # 3 weeks expiry

            self.queue_data['topics'].append(topic)

            type_label = "🔥 Trend" if topic['keyword_type'] == 'trend' else "🌲 Evergreen"
            print(f"  ✓ Added: {type_label} | {candidate['keyword']}")

            added_count += 1
            next_id += 1

        # Save queue
        self._save_queue()

        print(f"\n✅ {added_count}개 키워드가 큐에 추가되었습니다!")
        print(f"📊 Total topics in queue: {len(self.queue_data['topics'])}")

        # Show statistics
        self._show_queue_stats()

    def _show_queue_stats(self):
        """Show queue statistics"""
        topics = self.queue_data['topics']

        # Count by status
        by_status = {"pending": 0, "in_progress": 0, "completed": 0}
        for t in topics:
            by_status[t.get('status', 'pending')] += 1

        # Count by type
        by_type = {"trend": 0, "evergreen": 0, "unknown": 0}
        for t in topics:
            ktype = t.get('keyword_type', 'unknown')
            by_type[ktype] = by_type.get(ktype, 0) + 1

        # Count by language
        by_lang = {"en": 0, "ko": 0, "ja": 0}
        for t in topics:
            lang = t.get('lang', 'en')
            by_lang[lang] = by_lang.get(lang, 0) + 1

        print(f"\n{'='*60}")
        print(f"  📊 Queue Statistics")
        print(f"{'='*60}")
        print(f"  Status: Pending={by_status['pending']}, In Progress={by_status['in_progress']}, Completed={by_status['completed']}")
        print(f"  Type: 🔥 Trend={by_type['trend']}, 🌲 Evergreen={by_type['evergreen']}, Unknown={by_type['unknown']}")
        print(f"  Language: EN={by_lang['en']}, KO={by_lang['ko']}, JA={by_lang['ja']}")
        print(f"{'='*60}\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Keyword Curator for blog content")
    parser.add_argument('--count', type=int, default=15, help="Number of candidates to generate (default: 15)")
    args = parser.parse_args()

    # Check API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    # Initialize curator
    curator = KeywordCurator()

    # Generate candidates
    candidates = curator.generate_candidates(count=args.count)

    # Display candidates
    curator.display_candidates(candidates)

    # Interactive selection
    selected = curator.interactive_selection(candidates)

    # Add to queue
    if selected:
        curator.add_to_queue(selected)

    print("\n✨ Done!\n")


if __name__ == "__main__":
    main()
