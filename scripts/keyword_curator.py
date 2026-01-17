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
import requests

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic package not installed")
    print("Install with: pip install anthropic")
    sys.exit(1)


CURATION_PROMPT_WITH_TRENDS = """역할:
너는 광고 수익 최적화를 위한 키워드 큐레이터다.
아래 실시간 트렌드 검색 결과를 바탕으로 **고CPC, 감정 반응형** 키워드를 제안하라.

실시간 트렌드 데이터:
{trends_data}

목표:
한국어 / 영어 / 일본어 각각에서
**불안, 분노, 궁금증**을 유발하는 키워드만 제안하라.

금지:
- 추상적인 트렌드 요약 ("AI 트렌드", "새로운 기술")
- 교육/정보성 키워드 ("~하는 방법", "~란 무엇인가")
- 긍정적이고 평화로운 키워드

우선순위 키워드 유형:
1. 사건/사고/논란 중심 (계정 정지, 먹통, 과징금, 환불 거부)
2. 정부정책 혜택/조건 (신혼부부 지원, 청년 대출, 세금 감면)
3. 연예인/유명인 스캔들 (논란, 사과, 퇴출, 복귀)
4. 서비스 피해 사례 (환불 안됨, 계정 차단, 버그로 손해)
5. 규제/제재/금지 (사용 금지, 제재 대상, 불법 판정)

출력 형식:
반드시 JSON 형식으로만 응답하라.

[
  {{
    "keyword": "키워드 문구",
    "raw_search_title": "사용자가 구글에 검색할 때 정확히 입력하는 검색어 (소문자, 자연스러운 구어체)",
    "editorial_title": "기사 제목 형식의 독자 친화적 제목",
    "core_fear_question": "사용자의 핵심 두려움을 담은 질문 한 문장",
    "language": "ko",
    "category": "tech",
    "search_intent": "사용자가 지금 당장 검색하는 이유 (행동하지 않으면 무엇을 잃는지)",
    "angle": "이 키워드를 다룰 때의 관점",
    "competition_level": "low",
    "why_it_works": "사용자가 지금 행동하지 않으면 영구적으로 무엇을 잃는지 (마감/기회 손실 중심)",
    "purpose": "high competition인 경우에만: Traffic acquisition / Brand positioning / Viral content 중 하나",
    "keyword_type": "trend",
    "priority": 7,
    "risk_level": "safe",
    "name_policy": "no_real_names",
    "intent_signal": "STATE_CHANGE"
  }}
]

중요:
- keyword_type은 "trend" 또는 "evergreen" 중 하나
- category는 "tech", "business", "lifestyle", "society", "entertainment" 중 하나 (5개 카테고리를 균등하게 분배할 것)
- language는 "en", "ko", "ja" 중 하나 (3개 언어를 균등하게 분배할 것)
- competition_level은 "low", "medium", "high" 중 하나
- priority는 1-10 사이의 숫자 (높을수록 우선순위 높음)
- risk_level은 "safe", "caution", "high_risk" 중 하나 (기본값: "safe")
- name_policy는 "no_real_names", "generic_only" 중 하나 (기본값: "no_real_names")
- intent_signal은 "STATE_CHANGE", "PROMISE_BROKEN", "SILENCE", "DEADLINE_LOST", "COMPARISON" 중 하나
- 지금 시점(2026년 1월)에서 현실적인 키워드만 제안
- 예시는 절대 사용하지 말고, 실제 검색 가능성이 높은 키워드만 제안
- 위 실시간 트렌드 데이터를 반드시 참고하여 키워드 제안
- **중요**: 5개 카테고리(tech, business, lifestyle, society, entertainment)를 반드시 고르게 분배할 것

언어별 톤 차이:
- 🇺🇸 English: rights, compensation, legal leverage, lawsuits 중심
- 🇰🇷 Korean: 불공정, 좌절, 소비자 보호, 책임 추궁 중심
- 🇯🇵 Japanese: 불투명성, 공식 절차, 적절한 대응 방법 중심

**🔴 안전 가이드라인 (CRITICAL - AdSense/법적 리스크 방지):**

절대 금지:
- 실명 사용 (연예인, 기업인, 정치인, 특정 기업명)
- 확정되지 않은 의혹·논란 프레이밍
- 명예훼손 리스크 키워드

안전한 대체 표현:
- "K-pop idol" (실명 ❌)
- "major agency" (구체적 회사명 ❌)
- "top celebrity" (실명 ❌)
- "government policy" (X부처 ❌)
- "tech platform" (구체적 서비스명 ❌)

조건부 허용 (3조건 모두 충족 시만):
1. 사법/행정적으로 결론 난 사건
2. 모든 서술이 팩트 나열만
3. 감정 프레이밍 제거

각 키워드에 리스크 레벨 표시:
- "risk_level": "safe" (AdSense/플랫폼 안전)
- "risk_level": "caution" (사실 확인 필수)
- "risk_level": "high_risk" (법적 검토 필요)

각 키워드에 실명 정책 표시:
- "name_policy": "no_real_names" (기본값, 실명 사용 불가)
- "name_policy": "generic_only" (범주·역할만 허용)

**중복 방지 규칙:**
- Intent signals: STATE_CHANGE, PROMISE_BROKEN, SILENCE, DEADLINE_LOST, COMPARISON
- 같은 signal을 가진 키워드는 언어당 최대 2개까지만
- 5개 signal을 언어별로 균등하게 분배

**반드시 정확히 {count}개의 키워드를 생성하라:**
- 영어(en): {per_lang}개
- 한국어(ko): {per_lang}개
- 일본어(ja): {per_lang}개
- 총합: 정확히 {count}개

각 언어 내에서 5개 카테고리(tech, business, lifestyle, society, entertainment)를 최대한 균등하게 분배하되,
반드시 총 {count}개를 생성하는 것이 최우선이다."""


class KeywordCurator:
    def __init__(self, api_key: str = None, google_api_key: str = None, google_cx: str = None):
        """Initialize keyword curator with Claude API and Google Custom Search"""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")

        self.google_api_key = google_api_key or os.environ.get("GOOGLE_API_KEY")
        self.google_cx = google_cx or os.environ.get("GOOGLE_CX")

        if not self.google_api_key or not self.google_cx:
            print("⚠️  Google Custom Search credentials not found")
            print("   Set GOOGLE_API_KEY and GOOGLE_CX environment variables")
            print("   Falling back to Claude-only mode")

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

    def detect_intent_signals(self, query: str) -> list:
        """Detect intent signals from query for deduplication"""
        signals = []

        # State transition patterns
        if any(word in query.lower() for word in ["after", "갑자기", "suddenly", "突然", "overnight"]):
            signals.append("STATE_CHANGE")

        # Promise broken patterns
        if any(word in query.lower() for word in ["promised", "supposed to", "약속", "発表", "denied", "거부", "拒否"]):
            signals.append("PROMISE_BROKEN")

        # Silence patterns
        if any(word in query.lower() for word in ["no response", "ignored", "説明なし", "무응답", "침묵"]):
            signals.append("SILENCE")

        # Deadline/time loss patterns
        if any(word in query.lower() for word in ["deadline", "too late", "마감", "期限", "놓침", "逃し"]):
            signals.append("DEADLINE_LOST")

        # Comparison/injustice patterns
        if any(word in query.lower() for word in ["others got", "only me", "나만", "自分だけ"]):
            signals.append("COMPARISON")

        return signals if signals else ["GENERAL"]

    def fetch_trending_topics(self) -> str:
        """Fetch trending topics using Google Custom Search API"""
        if not self.google_api_key or not self.google_cx:
            return "No trending data available (Google API not configured)"

        print(f"\n{'='*60}")
        print(f"  🔍 Fetching trending topics from Google...")
        print(f"{'='*60}\n")

        # Search queries for high-CPC, emotion-driven keywords
        # Strategy: STATE TRANSITIONS (상태 전환) + EXPECTATION COLLAPSE (기대 붕괴)
        # Focus: "after X", "but Y", "suddenly Z", "no response", "others got"
        search_queries = [
            # Tech - State Transition + Silence (상태 전환 + 침묵)
            "account banned after update no response",
            "service outage promised compensation denied",
            "앱 업데이트 후 갑자기 먹통",
            "アカウント停止 理由説明なし",

            # Business - Deadline Loss + Others Got (시간 손실 + 비교 분노)
            "class action deadline passed too late",
            "refund promised but denied suddenly",
            "집단소송 신청 마감 놓침",
            "返金約束したが 拒否された",

            # Society - Expectation Collapse (기대 붕괴)
            "government support supposed to but denied",
            "new policy suddenly stricter than announced",
            "정부지원 조건 발표와 다름",
            "政府支援 突然 条件厳しく",

            # Entertainment - Action → Rejection (행동 → 거부)
            "celebrity apology issued but backlash continues",
            "idol agency promised explanation ignored fans",
            "사과문 냈지만 논란 계속",
            "謝罪文出したが 炎上続く",

            # Lifestyle - Safety Promise Broken (안전 약속 붕괴)
            "product recall announced but no refund",
            "food contamination others got compensated only me",
            "리콜 발표했는데 환불 거부",
            "リコール発表 返金対応なし"
        ]

        all_results = []
        for query in search_queries:
            try:
                url = "https://www.googleapis.com/customsearch/v1"
                params = {
                    "key": self.google_api_key,
                    "cx": self.google_cx,
                    "q": query,
                    "num": 5  # Get top 5 results per query
                }

                response = requests.get(url, params=params)
                response.raise_for_status()

                data = response.json()

                if "items" in data:
                    # Detect intent signals for this query
                    signals = self.detect_intent_signals(query)

                    for item in data["items"]:
                        all_results.append({
                            "query": query,
                            "signals": signals,  # Add intent signals
                            "title": item.get("title", ""),
                            "snippet": item.get("snippet", ""),
                            "link": item.get("link", "")
                        })

                print(f"  ✓ Fetched {len(data.get('items', []))} results for: {query}")

            except requests.exceptions.RequestException as e:
                print(f"  ⚠️  Error fetching results for '{query}': {e}")
                continue

        print(f"\n✅ Total {len(all_results)} trending topics fetched\n")

        # Format results for Claude
        trends_summary = "\n\n".join([
            f"Query: {r['query']}\nTitle: {r['title']}\nSnippet: {r['snippet']}\n"
            for r in all_results
        ])

        return trends_summary

    def filter_by_risk(self, candidates: List[Dict]) -> List[Dict]:
        """Filter out high-risk keywords automatically"""
        safe_candidates = []
        filtered_count = 0

        for kw in candidates:
            # Auto-reject high-risk
            if kw.get("risk_level") == "high_risk":
                filtered_count += 1
                print(f"  🔴 Filtered high-risk: {kw.get('keyword', 'unknown')}")
                continue

            # Flag caution items for manual review
            if kw.get("risk_level") == "caution":
                kw["needs_review"] = True
                print(f"  🟡 Caution flagged: {kw.get('keyword', 'unknown')}")

            safe_candidates.append(kw)

        if filtered_count > 0:
            print(f"\n⚠️  {filtered_count} high-risk keywords filtered out\n")

        return safe_candidates

    def generate_candidates(self, count: int = 15) -> List[Dict]:
        """Generate keyword candidates using Claude API with trending data"""
        print(f"\n{'='*60}")
        print(f"  🔍 Generating {count} keyword candidates...")
        print(f"{'='*60}\n")

        # Fetch trending topics from Google
        trends_data = self.fetch_trending_topics()

        # Calculate per-language count
        per_lang = count // 3  # Distribute evenly across 3 languages

        # Generate prompt with trending data
        prompt = CURATION_PROMPT_WITH_TRENDS.format(
            trends_data=trends_data,
            count=count,
            per_lang=per_lang
        )

        response = self.client.messages.create(
            model=self.model,
            max_tokens=8000,  # Increased for larger outputs
            messages=[{
                "role": "user",
                "content": prompt
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

        # Apply risk filtering
        filtered_candidates = self.filter_by_risk(candidates)

        return filtered_candidates

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
