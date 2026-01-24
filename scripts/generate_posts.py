#!/usr/bin/env python3
"""
Content Generation Script

Generates blog posts using Claude API with two-stage process:
1. Draft Agent: Creates initial content
2. Editor Agent: Refines and improves the draft

Usage:
    python generate_posts.py --count 3
    python generate_posts.py --topic-id 001-en-tech-ai-coding
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from topic_queue import reserve_topics, mark_completed, mark_failed
from utils.security import safe_print, mask_secrets
from affiliate_config import (
    detect_product_mentions,
    generate_affiliate_link,
    create_affiliate_box,
    get_affiliate_disclosure,
    should_add_affiliate_links
)

try:
    from anthropic import Anthropic
except ImportError:
    safe_print("Error: anthropic package not installed")
    safe_print("Install with: pip install anthropic")
    sys.exit(1)

try:
    import requests
except ImportError:
    safe_print("Error: requests package not installed")
    safe_print("Install with: pip install requests")
    sys.exit(1)

try:
    import certifi
except ImportError:
    safe_print("Warning: certifi not installed - SSL verification may fail on Windows")
    safe_print("Install with: pip install certifi")
    certifi = None


# System prompts for different languages
SYSTEM_PROMPTS = {
    "en": """You are a professional writer for Jake's Tech Insights blog.

🎯 Goal: 800-1,100 words of concise, high-impact content (AdSense optimized)

[EDITORIAL POLICY - READ FIRST]
This is a general hot-topic media covering:
- Government policies, celebrity news, social incidents, controversies, emerging tech
- High CPC and emotional reaction are PRIMARY goals
- Expert depth is NOT required

Your role:
- You do NOT decide whether a topic is useful, important, or appropriate
- Assume all provided topics are already approved for publication
- Your ONLY job is to explain them clearly and calmly in a friendly, UX-writing tone
- Do not soften, reject, or reframe topics based on usefulness or ethics
- Treat each topic as already approved by the editorial team
- Focus on clarity and readability, not on responsibility or balance

Output constraints:
- Do NOT add conclusions, solutions, or advice
- Do NOT attempt to educate or correct the reader
- Do NOT provide long-term implications
- Keep explanations factual, immediate, and present-focused

Every topic must clearly answer:
- Why is this being talked about now?
- If the reason is unclear, infer it from recent events, changes, or reactions
- Do NOT generalize

[Length Guide - Brevity is Key!]
- Total: 800-1,100 words (optimized completion rate)
- Each ## section: 120-180 words (core insights only)
- Intro: 80-100 words (strong hook)
- Conclusion: 60-80 words (clear CTA)
- **Finish completely**: No mid-sentence cutoffs

[Monetization Principles]
1. First paragraph: Hook with reader's pain point (1-2 sentences)
2. Structure: Problem → 3 Core Solutions → Action Steps → Conclusion
3. Tone: Medium/Substack style - conversational, personal, direct
4. SEO: Keyword "{keyword}" naturally 4-6 times
5. Sections: 3-4 ## headings (scannable)
6. End: Clear CTA - question or next step

[Medium Style (Required!)]
- Use "you" and "I" frequently (conversational)
- Short punchy sentences: "Here's the thing.", "Let me explain."
- Natural connectors: "Look", "Here's why", "The truth is"
- Break the fourth wall: "You might be thinking...", "Sound familiar?"
- Strong sentence starters: "Forget X.", "Stop doing Y.", "Start with Z."

[Style - Completion Optimized]
- Active voice, short sentences (1-2 lines)
- Core value only (cut fluff)
- Specific numbers/examples (1-2 selective)
- Bullet points for scannability
- End with punch: "Here's the bottom line."

[Absolutely Avoid]
- Redundancy: repeating same points ❌
- AI tells: "certainly", "it's important to note", "moreover", "furthermore"
- Academic tone: formal, distant language
- Abstract buzzwords: "revolutionary", "game-changer", "cutting-edge"
- Excessive emojis, unnecessary case studies
- Aggro triggers: "shock", "expose", "truth revealed", "jaw-dropping", "unbelievable"

[Headline Patterns - Aggro-Lite (Use ONLY these patterns)]
A. Change: "Why [topic] has changed recently"
B. Hidden problem: "Why [topic] is raising questions"
C. Cost/Loss: "Why [topic] might be more burdensome than expected"
D. Timing: "Why [topic] is being discussed again lately"

⚠️ Core: Complete 800-1,100 word article. Plenty of headroom in 12,000 tokens!""",

    "ko": """당신은 Jake's Tech Insights 블로그의 전문 작가입니다.

🎯 핵심 목표: 800-1,100 단어의 간결하고 임팩트 있는 글 작성 (애드센스 최적화)

[편집 방침 - 반드시 숙지]
이 사이트는 전방위 핫 키워드 미디어입니다:
- 정부 정책, 연예인 뉴스, 사회 사건, 논란, 신기술 등 광범위 커버
- 고CPC와 감정 반응 유도가 핵심 목표
- 전문가 수준의 깊이는 요구되지 않음

당신의 역할:
- 토픽이 유용한지, 중요한지, 적절한지 판단하지 마세요
- 모든 제공된 토픽은 이미 편집팀이 승인한 것으로 간주하세요
- 당신의 임무는 오직 "명확하고 침착하게, 친근한 UX 라이팅 톤으로 설명"하는 것입니다
- 윤리나 유용성을 이유로 토픽을 순화하거나, 거부하거나, 재해석하지 마세요
- 모든 토픽은 이미 승인된 것으로 취급하세요
- 책임감이나 균형보다는 명확성과 가독성에 집중하세요

출력 제약:
- 결론, 해결책, 조언을 추가하지 마세요
- 독자를 교육하거나 바로잡으려 하지 마세요
- 장기적 영향을 제시하지 마세요
- 사실적이고, 즉각적이며, 현재 중심으로 설명하세요

모든 토픽은 명확히 답해야 합니다:
- 왜 지금 이 이야기가 나오는가?
- 이유가 불분명하면 최근 사건, 변화, 반응에서 추론하세요
- 일반화하지 마세요

[길이 가이드 - 간결함이 핵심!]
- 전체 글: 800-1,100 단어 (완독률 최적화)
- 각 ## 섹션: 120-180 단어 (핵심만 전달)
- 도입부: 80-100 단어 (강력한 후킹)
- 결론: 60-80 단어 (명확한 CTA)
- **마지막 문장까지 반드시 완성**: 끊김 없이 완결하세요

[수익화 최적화 원칙]
1. 첫 문단: 독자의 pain point 공감 (1-2문장으로 강렬하게)
2. 구조: 문제 제기 → 핵심 해결책 3가지 → 실전 팁 → 결론
3. 톤: 토스(Toss) 스타일 - 전문적이지만 편안한 친구 같은 느낌
4. SEO: 키워드 "{keyword}"를 자연스럽게 4-6회 포함
5. 섹션: 3-4개 ## 헤딩 (각 섹션은 읽기 쉽게)
6. 끝: 명확한 CTA - 질문이나 다음 단계 제안

[토스 스타일 말투 (필수!)]
- "~해요" 반말 존댓말 사용 (습니다/합니다 ❌)
- "어떤가요?", "한번 볼까요?", "궁금하지 않으세요?" 같은 친근한 질문
- "사실", "실제로", "그런데", "참고로" 같은 자연스러운 접속사
- 숫자를 친근하게: "10개 → 열 개", "50% → 절반", "3배 → 세 배"
- 짧고 강렬한 문장: "놀랍죠?", "맞아요.", "이게 핵심이에요."

[스타일 - 완독률 최적화]
- 능동태 위주, 짧은 문장 (1-2줄)
- 핵심만 전달 (불필요한 설명 제거)
- 구체적 숫자/예시 (1-2개만 선택적으로)
- 불릿 포인트 적극 활용 (스캔 가능하게)
- 문단 끝 강조: "왜 그럴까요?", "이게 핵심이에요."

[절대 금지]
- 중언부언: 같은 내용 반복 ❌
- AI 티: "물론", "~할 수 있습니다", "~하는 것이 중요합니다"
- 딱딱한 문체: "~습니다/~합니다" (해요체만!)
- 추상적 표현: "혁신적", "게임체인저", "주목할 만한"
- 과도한 이모지, 불필요한 사례 나열
- 어그로 단어: "충격", "폭로", "실체", "진실", "소름", "충격적", "완벽 정리", "한 번에 이해"

[헤드라인 패턴 - Aggro-Lite (이 패턴만 사용)]
A. 변화: "최근 ~에 변화가 생긴 이유"
B. 은폐형 문제: "~을 두고 말이 나오는 이유"
C. 손해/비용: "~이 생각보다 부담이 되는 이유"
D. 시점: "왜 요즘 ~ 이야기가 다시 나오는 걸까"

⚠️ 핵심: 800-1,100 단어로 완결된 글을 작성하세요. 12,000 토큰 내에서 여유있게!""",

    "ja": """あなたはJake's Tech Insightsブログのプロライターです。

🎯 核心目標: 3,000-4,500文字の簡潔でインパクトのある記事（AdSense最適化）

[編集方針 - 必読]
このサイトは全方位ホットキーワードメディアです：
- 政府政策、芸能ニュース、社会事件、論争、新技術など幅広くカバー
- 高CPCと感情反応誘導が最優先目標
- 専門家レベルの深さは不要

あなたの役割：
- トピックが有用か、重要か、適切かを判断しないでください
- すべての提供されたトピックは既に編集チームが承認したものと見なしてください
- あなたの仕事は「明確で落ち着いた、親しみやすいUXライティングトーンで説明する」ことだけです
- 倫理や有用性を理由にトピックを和らげたり、拒否したり、再解釈したりしないでください
- すべてのトピックは既に承認されたものとして扱ってください
- 責任感やバランスよりも、明確さと読みやすさに集中してください

出力制約：
- 結論、解決策、アドバイスを追加しないでください
- 読者を教育したり、訂正しようとしないでください
- 長期的な影響を提示しないでください
- 事実的で、即時的で、現在に焦点を当てた説明をしてください

すべてのトピックは明確に答える必要があります：
- なぜ今この話が出ているのか？
- 理由が不明確な場合は、最近の出来事、変化、反応から推測してください
- 一般化しないでください

[長さガイド - 簡潔さが鍵！]
- 全体: 3,000-4,500文字（完読率を最適化）
- 各##セクション: 600-900文字（要点のみ）
- 導入部: 400-500文字（強力なフック）
- 結論: 300-400文字（明確なCTA）
- **最後の文まで必ず完成**: 途切れなく完結させてください

[収益化最適化の原則]
1. 最初の段落: 読者の悩みに共感（1-2文で強烈に）
2. 構造: 問題提起 → 核心解決策3つ → 実践ヒント → 結論
3. トーン: SmartNews/NewsPicks/日経COMEMO風 - 情報密度高く、読みやすく、直接的
4. SEO: キーワード"{keyword}"を自然に4-6回含める
5. セクション: 3-4個の##見出し（各セクションは読みやすく）
6. 終わり: 明確なCTA - 質問または次のステップ

[現代的UXライティングスタイル（必須！）- SmartNews/NewsPicks調]
- 結論ファースト: 最初に答えを提示し、その後に詳細説明
- 「です・ます」調でありながら簡潔で切れ味のある文体
- 情報密度を高める: 具体的な数字、データ、事例を優先
- 余計な修飾語を削除: 「〜という」「〜のような」を最小限に
- 箇条書きと表を積極活用: スキャンしやすい構成
- 接続詞は最小限: "実は", "ちなみに" など雰囲気作りの接続詞を減らす
- **過度な質問形を避ける**: "どうでしょうか？", "気になりませんか？" などの rhetorical questions は1記事に1-2回まで
- 断定的に伝える: "〜と言えます", "〜です" など明確な語尾

[段落構成 - 情報を前に]
- 各段落の最初の1-2文で結論を述べる
- その後に理由・根拠・データを配置
- 不要な導入や前置きを削除
- 「要するに」「ポイントは」などで核心を強調

[スタイル - 完読率最適化]
- 能動態中心、短い文（1-2行）
- 要点のみ伝達（不要な説明削除）
- 具体的な数字/例（1-2個のみ選択的に）
- 箇条書き積極活用（スキャン可能に）
- 段落の終わりは断定形: "これが現状です。", "この点が重要です。"

[絶対禁止]
- 冗長表現: 同じ内容の繰り返し ❌
- AI的表現: "もちろん", "〜することが重要です"
- 硬い文体: 教科書のような説明調
- 抽象的: "革新的", "ゲームチェンジャー", "注目すべき"
- 過度な絵文字、不要な事例の羅列
- アグロ単語: "衝撃", "暴露", "真実", "完全理解", "驚愕", "信じられない"
- **過度な個人的質問**: "〜ありませんか？", "〜でしょうか？" の連発（1記事に最大2回まで）
- **共感を装った前置き**: "皆さんも経験あると思いますが", "よくある悩みですよね" など

[ヘッドラインパターン - Aggro-Lite (このパターンのみ使用)]
A. 変化: "最近~に変化が起きた理由"
B. 隠された問題: "~をめぐって話が出ている理由"
C. 損失/コスト: "~が思ったより負担になる理由"
D. タイミング: "なぜ最近~の話が再び出ているのか"

⚠️ 核心: 3,000-4,500文字で完結した記事を書いてください。12,000トークン内で余裕を持って！"""
}


class ContentGenerator:
    def __init__(self, api_key: Optional[str] = None, unsplash_key: Optional[str] = None):
        """Initialize content generator with Claude API and Unsplash API"""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            safe_print("❌ ERROR: ANTHROPIC_API_KEY not found")
            safe_print("   Please set it as environment variable or pass to constructor")
            safe_print("   Example: export ANTHROPIC_API_KEY='your-key-here'")
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Set it as environment variable or pass to constructor."
            )

        # Initialize with Prompt Caching beta header
        try:
            self.client = Anthropic(
                api_key=self.api_key,
                default_headers={
                    "anthropic-beta": "prompt-caching-2024-07-31"
                }
            )
            self.model = "claude-sonnet-4-20250514"
            safe_print("  ✓ Anthropic API client initialized successfully")
        except Exception as e:
            safe_print(f"❌ ERROR: Failed to initialize Anthropic client: {mask_secrets(str(e))}")
            raise

        # Unsplash API (optional)
        self.unsplash_key = unsplash_key or os.environ.get("UNSPLASH_ACCESS_KEY")
        if self.unsplash_key:
            safe_print("  🖼️  Unsplash API enabled")
        else:
            safe_print("  ⚠️  Unsplash API key not found (images will be skipped)")
            safe_print("     Set UNSPLASH_ACCESS_KEY environment variable to enable")

    def generate_draft(self, topic: Dict) -> str:
        """Generate initial draft using Draft Agent with Prompt Caching"""
        keyword = topic['keyword']
        lang = topic['lang']
        category = topic['category']
        references = topic.get('references', [])  # Get references from topic

        system_prompt = SYSTEM_PROMPTS[lang].format(keyword=keyword)

        # User prompt with references
        user_prompt = self._get_draft_prompt(keyword, category, lang, references)

        safe_print(f"  📝 Generating draft for: {keyword}")

        # Use Prompt Caching: cache the system prompt
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=12000,
                system=[
                    {
                        "type": "text",
                        "text": system_prompt,
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
                messages=[{
                    "role": "user",
                    "content": user_prompt
                }]
            )
        except Exception as e:
            error_msg = mask_secrets(str(e))
            safe_print(f"  ❌ ERROR: API call failed during draft generation")
            safe_print(f"     Topic: {topic.get('id', 'unknown')}")
            safe_print(f"     Keyword: {keyword}")
            safe_print(f"     Error: {error_msg}")
            raise

        if not response or not response.content:
            safe_print(f"  ❌ ERROR: Empty response from API")
            safe_print(f"     Topic: {topic.get('id', 'unknown')}")
            raise ValueError("Empty response from Claude API")

        draft = response.content[0].text

        # Log cache performance
        usage = response.usage
        cache_read = getattr(usage, 'cache_read_input_tokens', 0)
        cache_create = getattr(usage, 'cache_creation_input_tokens', 0)

        # Always show cache status
        if cache_read > 0:
            safe_print(f"  💾 Cache HIT: {cache_read} tokens saved!")
        elif cache_create > 0:
            safe_print(f"  💾 Cache created: {cache_create} tokens")
        else:
            safe_print(f"  ℹ️  No caching (usage: input={usage.input_tokens}, output={usage.output_tokens})")

        safe_print(f"  ✓ Draft generated ({len(draft)} chars)")
        return draft

    def edit_draft(self, draft: str, topic: Dict) -> str:
        """Refine draft using Editor Agent with Prompt Caching"""
        lang = topic['lang']

        safe_print(f"  ✏️  Editing draft...")

        if not draft or len(draft.strip()) == 0:
            safe_print(f"  ⚠️  WARNING: Empty draft provided for editing")
            safe_print(f"     Topic: {topic.get('id', 'unknown')}")
            raise ValueError("Cannot edit empty draft")

        editor_prompt = self._get_editor_prompt(lang)

        # Use Prompt Caching: cache the editor instructions
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=12000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": editor_prompt,
                                "cache_control": {"type": "ephemeral"}
                            },
                            {
                                "type": "text",
                                "text": f"\n\n---\n\n{draft}"
                            }
                        ]
                    }
                ]
            )
        except Exception as e:
            error_msg = mask_secrets(str(e))
            safe_print(f"  ❌ ERROR: API call failed during draft editing")
            safe_print(f"     Topic: {topic.get('id', 'unknown')}")
            safe_print(f"     Draft length: {len(draft)} chars")
            safe_print(f"     Error: {error_msg}")
            raise

        if not response or not response.content:
            safe_print(f"  ❌ ERROR: Empty response from editing API")
            safe_print(f"     Topic: {topic.get('id', 'unknown')}")
            raise ValueError("Empty response from Claude API during editing")

        edited = response.content[0].text

        # Log cache performance
        usage = response.usage
        cache_read = getattr(usage, 'cache_read_input_tokens', 0)
        cache_create = getattr(usage, 'cache_creation_input_tokens', 0)

        # Always show cache status
        if cache_read > 0:
            safe_print(f"  💾 Cache HIT: {cache_read} tokens saved!")
        elif cache_create > 0:
            safe_print(f"  💾 Cache created: {cache_create} tokens")
        else:
            safe_print(f"  ℹ️  No caching (usage: input={usage.input_tokens}, output={usage.output_tokens})")

        safe_print(f"  ✓ Draft edited ({len(edited)} chars)")
        return edited

    def _get_draft_prompt(self, keyword: str, category: str, lang: str, references: List[Dict] = None) -> str:
        """Get draft generation prompt based on language"""
        # Get current date in KST
        from datetime import datetime, timezone, timedelta
        kst = timezone(timedelta(hours=9))
        today = datetime.now(kst)
        current_date = today.strftime("%Y년 %m월 %d일")  # Korean format
        current_date_en = today.strftime("%B %d, %Y")  # English format
        current_year = today.year

        # Format references for prompt
        refs_section = ""
        if references and len(references) > 0:
            refs_list = "\n".join([
                f"- [{ref.get('title', 'Source')}]({ref.get('url', '')}) - {ref.get('source', '')}"
                for ref in references[:3]
            ])
            refs_section = f"\n\n📚 USE THESE REFERENCES:\n{refs_list}\n"

        prompts = {
            "en": f"""📅 TODAY'S DATE: {current_date_en}
⚠️ IMPORTANT: You are writing this article as of TODAY ({current_date_en}). All information must be current as of {current_year}. Do NOT use outdated information from 2024 or earlier years.

Write a comprehensive blog post about: {keyword}{refs_section}

Category: {category}

⏱️ Reading Time Target: 4-5 minutes
- Write 3-4 main sections (## headings)
- Each section: 1-2 minutes to read, one key point
- Short paragraphs (2-4 sentences each)
- End with a thought-provoking question

🎯 HOOKING STRATEGY (Critical!):
1. **Opening Hook** (First 2-3 sentences):
   - Start with a PROBLEM SITUATION that readers face
   - Use empathy: "You adopted X, but employees don't use it..."
   - Include specific failure stat: "60% of X projects fail because..."
   - NOT generic intro like "X is becoming popular..."

2. **Real Success/Failure Cases**:
   - Include 1-2 SPECIFIC company/person examples
   - "A shopping mall tried X for everything and failed, but when they focused on Y..."
   - Show what DOESN'T work, not just what works
   - Avoid abstract: "Many companies..." → Use: "One e-commerce startup..."

3. **Limitations & Pitfalls**:
   - Dedicate 1 section to "When X Actually Hurts"
   - "In these 3 situations, X is counterproductive..."
   - This makes content feel authentic and trustworthy

4. **Data-Driven**:
   - Include 2-3 specific statistics (even if approximate)
   - "2024 survey shows 60% failure rate..."
   - "Companies saw 35% productivity increase..."

Content Guidelines:
- Target audience: Decision-makers seeking practical advice
- Focus on "What to avoid" as much as "What to do"
- Concrete examples over abstract concepts
- Mention current trends (2025-2026)
- Be concise and impactful - avoid unnecessary explanations

📚 REFERENCES SECTION:
- If references were provided above in the prompt, you MUST add a "## References" section at the end
- Use those EXACT URLs - do not modify or create new ones
- Format: `- [Source Title](URL) - Organization/Publisher`
- Example:
  ## References
  - [The State of AI in 2025](https://example.com/ai-report) - McKinsey & Company
  - [Remote Work Statistics 2025](https://example.com/remote) - Buffer
- **IMPORTANT**: If NO references were provided above, DO NOT add a References section at all

**This section is REQUIRED for all posts - even Entertainment/Society topics!**

Write the complete blog post now (body only, no title or metadata):""",

            "ko": f"""📅 오늘 날짜: {current_date}
⚠️ 중요: 이 글은 오늘({current_date}) 기준으로 작성합니다. 모든 정보는 {current_year}년 현재를 기준으로 해야 합니다. 2024년 이하의 오래된 정보를 사용하지 마세요.

다음 주제로 포괄적인 블로그 글을 작성하세요: {keyword}{refs_section}

카테고리: {category}

⏱️ 읽기 시간 목표: 4-5분
- 3-4개의 주요 섹션 (## 헤딩) 작성
- 각 섹션: 1-2분 읽기 분량, 하나의 핵심 포인트
- 짧은 문단 사용 (2-4 문장씩)
- 생각을 자극하는 질문으로 마무리

🎯 후킹 전략 (필수!):
1. **오프닝 후킹** (첫 2-3문장):
   - 독자가 직면한 문제 상황으로 시작
   - 공감 유도: "회사에서 X를 도입했는데 직원들이 쓰지 않고..."
   - 구체적 실패 통계 포함: "X 프로젝트의 60%가 실패하는 이유는..."
   - 일반적 시작 금지: "X가 인기를 끌고 있습니다..." ❌

2. **실제 성공/실패 사례**:
   - 구체적인 회사/사람 사례 1-2개 포함
   - "한 쇼핑몰은 X를 모든 것에 적용했다가 실패했지만, Y에만 집중하니까..."
   - 안 되는 것도 보여주기 (성공만 말하지 말기)
   - 추상적 표현 금지: "많은 기업들..." → "한 스타트업은..." ✅

3. **한계점과 함정**:
   - "X가 오히려 역효과인 경우" 섹션 1개 할애
   - "이 3가지 상황에서는 X가 비효율적..."
   - 이것이 진정성과 신뢰를 만듦

4. **데이터 기반**:
   - 구체적 통계 2-3개 포함 (대략적이어도 OK)
   - "2024년 조사에 따르면 60% 실패율..."
   - "기업들이 35% 생산성 증가 경험..."

콘텐츠 가이드라인:
- 대상 독자: 실용적 조언을 찾는 의사결정자
- "피해야 할 것"을 "해야 할 것"만큼 강조
- 추상적 개념보다 구체적 예시
- 현재 트렌드 언급 (2025-2026년)
- 간결하고 임팩트 있게 - 불필요한 설명 제거

📚 참고자료 섹션:
- 위 프롬프트에 참고자료가 제공된 경우, 반드시 글 마지막에 "## 참고자료" 섹션 추가
- 제공된 URL을 정확히 사용 - 수정하거나 새로 만들지 말 것
- 형식: `- [출처 제목](URL) - 조직/출판사`
- 예시:
  ## 참고자료
  - [2025 AI 현황 보고서](https://example.com/ai-report) - 맥킨지앤컴퍼니
  - [원격 근무 통계 2025](https://example.com/remote) - Buffer
- **중요**: 위에 참고자료가 제공되지 않았다면, 참고자료 섹션을 절대 추가하지 마세요

지금 바로 완전한 블로그 글을 작성하세요 (본문만, 제목이나 메타데이터 제외):""",

            "ja": f"""📅 本日の日付: {current_date}
⚠️ 重要: この記事は本日({current_date})の時点で書かれています。すべての情報は{current_year}年現在を基準にする必要があります。2024年以前の古い情報を使用しないでください。

次のトピックについて包括的なブログ記事を書いてください: {keyword}{refs_section}

カテゴリ: {category}

⏱️ 読む時間の目標: 4-5分
- 3-4個の主要セクション (##見出し) を作成
- 各セクション: 1-2分で読める分量、1つの重要ポイント
- 短い段落を使用 (2-4文ずつ)
- 考えさせる質問で締めくくる

🎯 フッキング戦略 (必須!):
1. **オープニングフック** (最初の2-3文):
   - 読者が直面する問題状況から始める
   - 共感を誘う: "会社でXを導入したのに社員が使わない..."
   - 具体的な失敗統計を含む: "Xプロジェクトの60%が失敗する理由は..."
   - 一般的な始まり方禁止: "Xが人気になっています..." ❌

2. **実際の成功/失敗事例**:
   - 具体的な会社/人物の例を1-2個含む
   - "あるECサイトはXを全てに適用して失敗したが、Yだけに集中したら..."
   - うまくいかないことも見せる (成功だけ語らない)
   - 抽象的表現禁止: "多くの企業が..." → "あるスタートアップは..." ✅

3. **限界点と落とし穴**:
   - "Xがかえって逆効果になる場合" セクションを1つ設ける
   - "この3つの状況ではXは非効率的..."
   - これが真実味と信頼を生む

4. **データドリブン**:
   - 具体的な統計を2-3個含む (おおよそでもOK)
   - "2024年の調査では60%の失敗率..."
   - "企業は35%の生産性向上を経験..."

コンテンツガイドライン:
- 対象読者: 実用的なアドバイスを求める意思決定者
- "避けるべきこと"を"すべきこと"と同じくらい強調
- 抽象的な概念より具体例
- 現在のトレンドに言及 (2025-2026年)
- 簡潔でインパクトのある内容 - 不要な説明を削除

📚 参考資料セクション:
- 上記プロンプトで参考資料が提供された場合、記事の最後に必ず"## 参考資料"セクションを追加
- 提供されたURLを正確に使用 - 修正したり新規作成したりしないこと
- 形式: `- [情報源タイトル](URL) - 組織/出版社`
- 例示:
  ## 参考資料
  - [2025年AI動向レポート](https://example.com/ai-report) - マッキンゼー・アンド・カンパニー
  - [リモートワーク統計2025](https://example.com/remote) - Buffer
- **重要**: 上記で参考資料が提供されていない場合、参考資料セクションは絶対に追加しないでください

今すぐ完全なブログ記事を書いてください（本文のみ、タイトルやメタデータなし）:"""
        }

        return prompts[lang]

    def _get_editor_prompt(self, lang: str) -> str:
        """Get editor prompt based on language"""
        prompts = {
            "en": """You are an expert editor. Transform this into Medium-style content with authentic human touch:

📏 Length Requirements (Target: 700-1200 words for 5-7 min read):
- If draft is under 700 words: EXPAND with examples, explanations, context to reach 700-1200 words
- If draft is 700-1200 words: MAINTAIN the same length (ideal range)
- If draft is 1200-1800 words: COMPRESS to 1100-1300 words by removing redundancy
- If draft is over 1800 words: COMPRESS aggressively to 1100-1300 words

🎯 CRITICAL ENHANCEMENTS:
1. **Strengthen Opening Hook**:
   - If opening is generic, rewrite to start with problem/pain point
   - Add empathy: "You've been there, right?"
   - Make it personal and relatable

2. **Add Authenticity Markers** (NO personal anecdotes):
   - Use authoritative references: "Industry reports show...", "According to recent data..."
   - Add failure acknowledgment: "This approach can fail when..."
   - Show balanced perspective: "This isn't always the answer..."
   - AVOID: "In my experience...", "I spoke with...", "I thought..." (credibility issues on anonymous blogs)

3. **Enhance Examples**:
   - Make vague examples specific: "Many companies" → "One fintech startup" or "A Silicon Valley tech company"
   - Add concrete details: numbers, outcomes, timelines
   - Include what went WRONG, not just success stories
   - AVOID: "I worked with", "I spoke to" → Use: "Case studies show", "Reports indicate"

4. **Balance Perspective**:
   - Ensure there's a "When this doesn't work" section
   - Add nuance: "This works IF...", "But in these cases..."
   - Avoid absolute claims: "always", "never", "guaranteed"

Tasks:
1. **Medium style conversion**: Add "you/I", conversational tone
2. **Eliminate all AI tells**: "certainly", "moreover", "it's important to note"
3. **Natural connectors**: "Look", "Here's why", "The truth is"
4. **Break fourth wall**: "You might be thinking...", "Sound familiar?"
5. **Punchy sentences**: "Here's the thing.", "Let me explain.", "Stop it."
6. **Smooth transitions**: "Now", "Here's where it gets interesting"
7. Keep all factual information intact
8. **Complete ending**: Finish conclusion fully

Return improved version (body only, no title):""",

            "ko": """당신은 전문 에디터입니다. 이 블로그 글을 진짜 사람이 쓴 것 같은 토스 스타일로 개선하세요:

📏 길이 요구사항 (목표: 5-7분 읽기 = 700-1,200단어):
- 초안이 700단어 미만: 예시, 설명, 맥락 추가로 700-1,200단어까지 확장
- 초안이 700-1,200단어: 같은 길이 유지 (이상적 범위)
- 초안이 1,200-1,800단어: 1,100-1,300단어로 압축 (중복 제거)
- 초안이 1,800단어 초과: 1,100-1,300단어로 대폭 압축

🎯 핵심 개선사항:
1. **오프닝 강화**:
   - 일반적 시작이면 문제/고민 상황으로 재작성
   - 공감 추가: "이런 경험 있으시죠?"
   - 개인적이고 공감 가능하게

2. **정보 밀도 최우선** (한국 독자 = 빠른 정보 선호):
   - 핵심 정보 먼저: 수치, 단계, 방법
   - 실용 정보 즉시 제공: "계산법: 1) ~ 2) ~"
   - "의외로...", "놀랍게도..." 같은 자연스러운 표현
   - 한계 언급: "항상 답은 아니에요..."

3. **예시 구체화** (개인 경험 배제):
   - 추상적 예시를 구체적으로: "많은 회사들" → "한 핀테크 스타트업은" 또는 "토스의 경우"
   - 구체적 디테일: 숫자, 결과, 타임라인
   - 실패한 것도 포함: 성공만 말하지 말기
   - 피할 것: "제 경험상", "제가 봤을 때" → 대신: "사례 연구에 따르면", "데이터는 보여줍니다"

4. **균형잡힌 관점**:
   - "이런 경우엔 안 통해요" 섹션 확인/추가
   - 뉘앙스: "이게 통하려면...", "하지만 이런 경우엔..."
   - 절대적 표현 피하기: "항상", "절대", "무조건"

작업:
1. **토스 말투로 변환**: "~습니다" → "~해요", 친근한 질문형 추가
2. AI 느낌 완전 제거: "물론", "~할 수 있습니다", "중요합니다" 모두 삭제
3. 자연스러운 접속사: "사실", "실제로", "그런데", "참고로"
4. 숫자를 친근하게: "50% → 절반", "3배 → 세 배"
5. 짧고 강렬한 문장 추가: "놀랍죠?", "맞아요.", "이게 핵심이에요."
6. 섹션 간 매끄러운 전환: "자, 이제 ~", "그럼 ~"
7. 모든 사실 정보는 그대로 유지
8. **마지막 문장까지 완결**: 결론을 반드시 완성

개선된 버전을 반환하세요 (본문만, 제목 제외):""",

            "ja": """あなたは専門エディターです。このブログ記事を本物の人間が書いたような自然な会話調に改善してください:

📏 文字数要件 (目標: 5-7分 = 2,800-4,200文字):
- 下書きが2,800文字未満: 例、説明、文脈を追加して2,800-4,200文字に拡張
- 下書きが2,800-4,200文字: 同じ長さを維持 (理想的な範囲)
- 下書きが4,200-7,000文字: 3,500-4,000文字に圧縮 (冗長性削除)
- 下書きが7,000文字超: 3,500-4,000文字に大幅圧縮

🎯 重要な改善点:
1. **オープニングの強化**:
   - 一般的な始まりなら問題/悩み状況に書き直し
   - 共感を追加: "こんな経験ありませんか？"
   - 個人的で共感できるように

2. **結論ファースト + スペック優先** (日本読者の好み):
   - 最初に結論: "結論：〇〇を選ぶべき理由"
   - スペック表必須（Tech/Finance）: 比較表、数値データ
   - "意外にも...", "驚いたことに..." のような自然な表現
   - 限界の言及: "これが常に答えとは限りません..."

3. **例の具体化** (個人経験排除):
   - 曖昧な例を具体的に: "多くの企業" → "あるフィンテック企業" または "メルカリの事例"
   - 具体的な詳細: 数字、結果、タイムライン
   - 失敗したことも含める: 成功だけ語らない
   - 避けるべき: "私の経験では", "私が見たところ" → 代わりに: "ケーススタディによると", "データが示しています"

4. **バランスの取れた視点**:
   - "こういう場合はうまくいきません" セクションを確認/追加
   - ニュアンス: "これがうまくいくには...", "ただしこんな場合は..."
   - 絶対的な表現を避ける: "常に", "絶対に", "必ず"

タスク:
1. **会話調に変換**: "〜ですね", "〜ますよね", "〜でしょう" など柔らかい語尾に
2. AI的な表現を完全削除: "もちろん", "〜することが重要です", "〜について説明します"
3. 自然な接続詞: "実は", "ちなみに", "さて", "それで"
4. 提案形を追加: "〜してみましょう", "〜してみてください"
5. 質問形で引き込む: "どうでしょうか？", "気になりませんか？"
6. 短い感嘆: "驚きですね。", "面白いですよね。"
7. セクション間の移行: "では、詳しく見ていきましょう。"
8. すべての事実情報はそのまま保持
9. **最後の文まで完結**: 結論を必ず完成

改善されたバージョンを返してください（本文のみ、タイトルなし）:"""
        }

        return prompts[lang]

    def generate_title(self, content: str, keyword: str, lang: str, references: List[Dict] = None) -> str:
        """Generate SEO-friendly title based on actual content and references"""
        # Get current year in KST
        from datetime import datetime, timezone, timedelta
        kst = timezone(timedelta(hours=9))
        current_year = datetime.now(kst).year

        # Extract strategic samples from content for better context
        # Take beginning (intro), middle (main content), and end (conclusion)
        content_length = len(content)
        if content_length <= 1200:
            content_preview = content
        else:
            # Get first 500, middle 400, last 300 chars
            beginning = content[:500]
            middle_start = content_length // 2 - 200
            middle = content[middle_start:middle_start + 400]
            ending = content[-300:]
            content_preview = f"{beginning}\n\n[...middle section...]\n{middle}\n\n[...conclusion...]\n{ending}"

        # Format references if available
        refs_context = ""
        if references and len(references) > 0:
            refs_list = "\n".join([
                f"- {ref.get('title', 'Source')}"
                for ref in references[:3]
            ])
            refs_context = f"\n\nREFERENCE TOPICS:\n{refs_list}\n"

        prompts = {
            "en": f"Generate a catchy, SEO-friendly blog title (50-60 chars) for this post about '{keyword}'.\n\nCONTENT SAMPLES (beginning, middle, end):\n{content_preview}{refs_context}\nIMPORTANT:\n- Title MUST accurately reflect the MAIN TOPIC throughout the entire content\n- Read all content samples (beginning, middle, end) to understand the main theme\n- If beginning discusses subscription but main content is about rankings/fighters, focus on rankings/fighters\n- Include the keyword '{keyword}' naturally\n- Current year is {current_year}, use it if mentioning years\n- Return ONLY the title, nothing else",
            "ko": f"'{keyword}'에 대한 이 블로그 글의 매력적이고 SEO 친화적인 제목을 생성하세요 (50-60자).\n\n본문 샘플 (시작, 중간, 끝):\n{content_preview}{refs_context}\n중요:\n- 제목은 본문 전체의 핵심 주제를 정확히 반영해야 합니다\n- 모든 본문 샘플(시작, 중간, 끝)을 읽고 핵심 주제를 파악하세요\n- 시작부분이 구독에 대해 이야기하지만 본문 대부분이 랭킹/선수에 관한 것이라면 랭킹/선수에 집중하세요\n- '{keyword}' 키워드를 자연스럽게 포함하세요\n- 현재 연도는 {current_year}년입니다\n- 제목만 반환하세요",
            "ja": f"'{keyword}'に関するこのブログ記事の魅力的でSEOフレンドリーなタイトルを生成してください（50-60文字）。\n\n本文サンプル（冒頭、中盤、終盤）:\n{content_preview}{refs_context}\n重要:\n- タイトルは本文全体の核心テーマを正確に反映する必要があります\n- すべての本文サンプル（冒頭、中盤、終盤）を読んで核心テーマを把握してください\n- 冒頭がサブスクについて話していても、本文の大部分がランキング/選手に関するものなら、ランキング/選手に集中してください\n- '{keyword}'キーワードを自然に含めてください\n- 現在の年は{current_year}年です\n- タイトルのみを返してください"
        }

        response = self.client.messages.create(
            model=self.model,
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": prompts[lang]
            }]
        )

        generated_title = response.content[0].text.strip().strip('"').strip("'")

        # Validate title-content alignment
        validation_prompts = {
            "en": f"Does this title accurately reflect the main content?\n\nTITLE: {generated_title}\n\nCONTENT: {content_preview}\n\nAnswer ONLY 'yes' or 'no'. If no, briefly explain the mismatch (max 20 words).",
            "ko": f"이 제목이 본문 내용을 정확히 반영합니까?\n\n제목: {generated_title}\n\n본문: {content_preview}\n\n'예' 또는 '아니오'로만 답하세요. 아니오라면 불일치를 간단히 설명하세요 (최대 20단어).",
            "ja": f"このタイトルは本文内容を正確に反映していますか？\n\nタイトル: {generated_title}\n\n本文: {content_preview}\n\n「はい」または「いいえ」のみで答えてください。いいえの場合、不一致を簡潔に説明してください（最大20語）。"
        }

        validation_response = self.client.messages.create(
            model=self.model,
            max_tokens=50,
            messages=[{
                "role": "user",
                "content": validation_prompts[lang]
            }]
        )

        validation_result = validation_response.content[0].text.strip().lower()

        # If validation fails, log warning (but still use the title)
        if not validation_result.startswith('yes') and not validation_result.startswith('예') and not validation_result.startswith('はい'):
            safe_print(f"  ⚠️  Title-content mismatch detected: {validation_result}")
            safe_print(f"     Title: {generated_title}")

        return generated_title

    def generate_description(self, content: str, keyword: str, lang: str) -> str:
        """Generate meta description"""
        prompts = {
            "en": f"Generate a compelling meta description (150-160 chars) for a blog post about '{keyword}'. Return ONLY the description.",
            "ko": f"'{keyword}'에 대한 블로그 글의 매력적인 메타 설명을 생성하세요 (150-160자). 설명만 반환하세요.",
            "ja": f"'{keyword}'に関するブログ記事の魅力的なメタ説明を生成してください（150-160文字）。説明のみを返してください。"
        }

        response = self.client.messages.create(
            model=self.model,
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": prompts[lang]
            }]
        )

        return response.content[0].text.strip().strip('"').strip("'")

    def translate_to_english(self, text: str) -> str:
        """Translate non-English keywords to English for Unsplash search"""
        # Simple keyword translations for common tech/business/lifestyle terms
        translations = {
            # Korean
            '챗봇': 'chatbot', 'AI': 'artificial intelligence', '도입': 'implementation',
            '실패': 'failure', '이유': 'reasons', '노코드': 'no-code', '툴': 'tool',
            '한계점': 'limitations', '재택근무': 'remote work', '하이브리드': 'hybrid',
            '근무': 'work', '효율성': 'efficiency', 'MZ세대': 'gen z', '관리': 'management',
            '방법': 'method', '사례': 'case', '미니멀': 'minimal', '라이프': 'lifestyle',
            '중단': 'quit', '생산성': 'productivity', '팁': 'tips',
            # Japanese
            'コード': 'code', '開発': 'development', '限界点': 'limitations',
            'テレワーク': 'telework', 'オフィス': 'office', '勤務': 'work',
            '生産性': 'productivity', '比較': 'comparison', 'ノー': 'no',
            'サブスク': 'subscription', '疲れ': 'fatigue', '解約': 'cancel',
            '理由': 'reason', 'Z世代': 'gen z', 'マネジメント': 'management',
            '誤解': 'misconception', 'DX': 'digital transformation', '推進': 'promotion',
            '失敗': 'failure', '要因': 'factors', 'ヒント': 'tips',
            'ワークライフバランス': 'work life balance', 'スタートアップ': 'startup',
            '資金調達': 'fundraising', '戦略': 'strategy', 'AIコーディング': 'AI coding',
            'アシスタント': 'assistant', 'リモートワーク': 'remote work'
        }

        # Split and translate each word
        words = text.split()
        translated_words = []
        for word in words:
            # Try exact match first
            if word in translations:
                translated_words.append(translations[word])
            else:
                # Check if word contains any translatable substring
                found = False
                for kr, en in translations.items():
                    if kr in word:
                        translated_words.append(en)
                        found = True
                        break
                if not found:
                    # Keep as-is if ASCII (likely already English)
                    try:
                        word.encode('ascii')
                        translated_words.append(word)
                    except UnicodeEncodeError:
                        pass  # Skip non-ASCII untranslatable words

        return ' '.join(translated_words) if translated_words else 'technology'

    def fetch_featured_image(self, keyword: str, category: str) -> Optional[Dict]:
        """Fetch featured image from Unsplash API"""
        if not self.unsplash_key:
            return None

        try:
            # Clean keyword for better Unsplash search
            # Remove years (2020-2030) to avoid year-specific images
            import re
            clean_keyword = re.sub(r'20[2-3][0-9]년?', '', keyword)  # Match years + optional 년 (Korean year)
            # Remove common prefixes/suffixes that reduce search quality
            clean_keyword = re.sub(r'【.*?】', '', clean_keyword)  # Remove 【brackets】
            clean_keyword = re.sub(r'\[.*?\]', '', clean_keyword)  # Remove [brackets]
            clean_keyword = clean_keyword.strip()

            # Translation dictionary for meaningful keywords
            keyword_translations = {
                # Korean - AI/Jobs/Employment
                'AI': 'artificial intelligence',
                '인공지능': 'artificial intelligence',
                '대체': 'replacement automation',
                '일자리': 'job employment work',
                '실업': 'unemployment jobless',
                '직업': 'occupation career profession',
                '취업': 'employment hiring recruitment',
                '자동화': 'automation robot',
                '기술': 'technology tech',
                '디지털': 'digital technology',
                '로봇': 'robot automation',
                '미래': 'future',
                '변화': 'change transformation',
                '위험': 'risk danger',
                # Korean - Finance/Business
                '나라사랑카드': 'patriot card credit card',
                '카드': 'card credit',
                '연령': 'age limit',
                '제한': 'restriction limit',
                '전세': 'housing lease deposit',
                '보증금': 'deposit guarantee',
                '배달': 'delivery food',
                '수수료': 'fee commission',
                '자영업': 'small business owner',
                '폐업': 'business closure bankruptcy',
                '지원금': 'subsidy support fund',
                '정부': 'government policy',
                '신청': 'application registration',
                '혜택': 'benefit advantage',
                # Korean - Entertainment/Society
                '사과문': 'apology statement',
                '팬': 'fan supporter',
                '등돌림': 'backlash criticism',
                '스마트폰': 'smartphone mobile',
                '건강': 'health wellness',
                # Japanese - AI/Jobs/Employment
                '人工知能': 'artificial intelligence',
                '失業': 'unemployment jobless',
                'リスク': 'risk danger threat',
                '職業': 'occupation job',
                '代替': 'replacement substitute',
                '雇用': 'employment hiring',
                '自動化': 'automation robot',
                'デジタル': 'digital technology',
                'ロボット': 'robot automation',
                '未来': 'future',
                '変化': 'change transformation',
                # Japanese - Finance/Business
                '奨学金': 'scholarship student loan',
                '返済': 'repayment debt',
                '免除': 'exemption forgiveness',
                '投資': 'investment financial',
                '詐欺': 'fraud scam',
                'アカデミー賞': 'academy award',
                '受賞': 'award winner',
                '住宅ローン': 'home mortgage loan',
                '審査': 'screening examination',
                '承認': 'approval authorization',
            }

            # Extract meaningful keywords from title
            title_words = clean_keyword.split()
            translated_keywords = []

            # Try to find and translate key phrases
            for ko_word, en_translation in keyword_translations.items():
                if ko_word in clean_keyword:
                    translated_keywords.append(en_translation)

            # If no translation found, extract meaningful words (skip common noise and non-ASCII)
            if not translated_keywords:
                noise_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for']
                for word in title_words[:3]:  # Take first 3 words
                    # Filter out non-ASCII words to prevent non-English queries
                    try:
                        word.encode('ascii')
                        is_ascii = True
                    except UnicodeEncodeError:
                        is_ascii = False

                    if is_ascii and len(word) > 2 and word.lower() not in noise_words:
                        translated_keywords.append(word)

            # Add category context
            category_context = {
                'tech': 'technology digital',
                'business': 'business professional',
                'finance': 'finance money',
                'society': 'society community',
                'entertainment': 'entertainment culture',
                'lifestyle': 'lifestyle daily',
                'sports': 'sports athletic',
                'education': 'education learning'
            }

            # Build flexible, contextual query
            if translated_keywords:
                base_keywords = ' '.join(translated_keywords[:2])
            else:
                # Fallback to pure category context if no English keywords found
                base_keywords = category_context.get(category, 'technology')

            context = category_context.get(category, category)
            query = f"{base_keywords} {context}".strip()

            # Unsplash API endpoint
            url = "https://api.unsplash.com/search/photos"
            headers = {
                "Authorization": f"Client-ID {self.unsplash_key}"
            }
            params = {
                "query": query,
                "per_page": 30,  # Increased from 5 to 30 for larger image pool
                "orientation": "landscape"
            }

            safe_print(f"  🔍 Searching Unsplash for: {query}")

            # Use certifi for SSL verification (Windows compatibility)
            verify_ssl = certifi.where() if certifi else True
            response = requests.get(url, headers=headers, params=params, timeout=10, verify=verify_ssl)
            response.raise_for_status()

            data = response.json()

            # Load used images tracking file
            used_images_file = Path(__file__).parent.parent / "data" / "used_images.json"
            used_images_meta_file = Path(__file__).parent.parent / "data" / "used_images_metadata.json"

            # Load metadata (tracks when each image was used)
            used_images_meta = {}
            if used_images_meta_file.exists():
                try:
                    with open(used_images_meta_file, 'r') as f:
                        used_images_meta = json.load(f)
                except:
                    pass

            # Clean up images older than 30 days
            from datetime import datetime, timedelta
            current_time = datetime.now().timestamp()
            cutoff_time = (datetime.now() - timedelta(days=30)).timestamp()

            cleaned_meta = {}
            for img_id, timestamp in used_images_meta.items():
                if timestamp > cutoff_time:
                    cleaned_meta[img_id] = timestamp

            # Update set of used images (only keep recent ones)
            used_images = set(cleaned_meta.keys())

            # Save cleaned metadata
            if cleaned_meta != used_images_meta:
                used_images_meta_file.parent.mkdir(parents=True, exist_ok=True)
                with open(used_images_meta_file, 'w') as f:
                    json.dump(cleaned_meta, f, indent=2)
                if len(used_images_meta) > len(cleaned_meta):
                    safe_print(f"  🗑️  Cleaned up {len(used_images_meta) - len(cleaned_meta)} images older than 30 days")

            used_images_meta = cleaned_meta

            # Find first unused image from results
            photo = None
            if data.get('results'):
                for result in data['results']:
                    image_id = result['id']
                    if image_id not in used_images:
                        photo = result
                        used_images.add(image_id)
                        used_images_meta[image_id] = current_time
                        break
            else:
                safe_print(f"  ⚠️  No images found for '{query}'")

            # If no results or all images are used, try with generic category query
            if photo is None:
                safe_print(f"  ⚠️  All images for '{query}' already used, trying generic category search...")
                generic_query = category_context.get(category, 'technology')
                params['query'] = generic_query

                response = requests.get(url, headers=headers, params=params, timeout=10, verify=verify_ssl)
                response.raise_for_status()
                data = response.json()

                if data.get('results'):
                    for result in data['results']:
                        image_id = result['id']
                        if image_id not in used_images:
                            photo = result
                            used_images.add(image_id)
                            used_images_meta[image_id] = current_time
                            safe_print(f"  ✓ Found unused image with generic search: {generic_query}")
                            break

                # If still no unused image found, return None (use placeholder)
                if photo is None:
                    safe_print(f"  ❌ No unused images available for category '{category}'")
                    return None

            # Save used images (legacy file for backward compatibility)
            used_images_file.parent.mkdir(parents=True, exist_ok=True)
            with open(used_images_file, 'w') as f:
                json.dump(list(used_images), f)

            # Save metadata with timestamps
            with open(used_images_meta_file, 'w') as f:
                json.dump(used_images_meta, f, indent=2)

            image_info = {
                'url': photo['urls']['regular'],
                'download_url': photo['links']['download_location'],
                'photographer': photo['user']['name'],
                'photographer_url': photo['user']['links']['html'],
                'unsplash_url': photo['links']['html'],
                'image_id': photo['id']
            }

            safe_print(f"  ✓ Found image by {image_info['photographer']}")
            return image_info

        except requests.exceptions.Timeout as e:
            safe_print(f"  ⚠️  Unsplash API timeout: Request took too long")
            safe_print(f"     Keyword: {keyword}")
            safe_print(f"     Error: {mask_secrets(str(e))}")
            return None
        except requests.exceptions.HTTPError as e:
            safe_print(f"  ⚠️  Unsplash API HTTP error: {e.response.status_code if e.response else 'unknown'}")
            safe_print(f"     Keyword: {keyword}")
            safe_print(f"     Error: {mask_secrets(str(e))}")
            return None
        except requests.exceptions.RequestException as e:
            safe_print(f"  ⚠️  Unsplash API network error")
            safe_print(f"     Keyword: {keyword}")
            safe_print(f"     Error: {mask_secrets(str(e))}")
            return None
        except json.JSONDecodeError as e:
            safe_print(f"  ⚠️  Unsplash API response parsing failed")
            safe_print(f"     Keyword: {keyword}")
            safe_print(f"     Error: Invalid JSON response")
            return None
        except Exception as e:
            safe_print(f"  ⚠️  Image fetch failed with unexpected error")
            safe_print(f"     Keyword: {keyword}")
            safe_print(f"     Error: {mask_secrets(str(e))}")
            return None

    def download_image(self, image_info: Dict, keyword: str) -> Optional[str]:
        """Download optimized image to static/images/ directory"""
        if not image_info:
            return None

        try:
            # Create images directory
            images_dir = Path("static/images")
            images_dir.mkdir(parents=True, exist_ok=True)

            # Generate filename
            slug = keyword.lower()
            slug = ''.join(c if c.isalnum() or c.isspace() else '' for c in slug)
            slug = slug.replace(' ', '-')[:30]
            # Use KST for image filename
            from datetime import timezone, timedelta
            kst = timezone(timedelta(hours=9))
            date_str = datetime.now(kst).strftime("%Y%m%d")
            filename = f"{date_str}-{slug}.jpg"
            filepath = images_dir / filename

            # Trigger Unsplash download tracking (required by API terms)
            if image_info.get('download_url'):
                verify_ssl = certifi.where() if certifi else True
                requests.get(
                    image_info['download_url'],
                    headers={"Authorization": f"Client-ID {self.unsplash_key}"},
                    timeout=5,
                    verify=verify_ssl
                )

            # Download optimized image (1200px width, quality 85)
            # Use Unsplash's regular URL which already includes optimization
            download_url = image_info.get('url', '')
            # Add additional optimization parameters
            if '?' in download_url:
                optimized_url = f"{download_url}&w=1200&q=85&fm=jpg"
            else:
                optimized_url = f"{download_url}?w=1200&q=85&fm=jpg"

            safe_print(f"  📥 Downloading optimized image (1200px, q85)...")
            # Use certifi for SSL verification (Windows compatibility)
            verify_ssl = certifi.where() if certifi else True
            response = requests.get(optimized_url, timeout=15, verify=verify_ssl)
            response.raise_for_status()

            # Save image
            with open(filepath, 'wb') as f:
                f.write(response.content)

            size_kb = len(response.content) / 1024
            safe_print(f"  ✓ Image saved: {filepath} ({size_kb:.1f} KB)")

            # Return relative path for Hugo
            return f"/images/{filename}"

        except requests.exceptions.Timeout as e:
            safe_print(f"  ⚠️  Image download timeout")
            safe_print(f"     Keyword: {keyword}")
            safe_print(f"     URL: {optimized_url[:80]}...")
            return None
        except requests.exceptions.HTTPError as e:
            safe_print(f"  ⚠️  Image download HTTP error: {e.response.status_code if e.response else 'unknown'}")
            safe_print(f"     Keyword: {keyword}")
            return None
        except IOError as e:
            safe_print(f"  ⚠️  File system error during image save")
            safe_print(f"     Path: {filepath}")
            safe_print(f"     Error: {str(e)}")
            return None
        except Exception as e:
            safe_print(f"  ⚠️  Image download failed with unexpected error")
            safe_print(f"     Keyword: {keyword}")
            safe_print(f"     Error: {mask_secrets(str(e))}")
            return None

    def save_post(self, topic: Dict, title: str, description: str, content: str, image_path: Optional[str] = None, image_credit: Optional[Dict] = None) -> Path:
        """Save post to Hugo content directory"""
        lang = topic['lang']
        category = topic['category']
        keyword = topic['keyword']

        # Generate filename from keyword
        slug = keyword.lower()
        # Remove special characters, keep alphanumeric and spaces
        slug = ''.join(c if c.isalnum() or c.isspace() else '' for c in slug)
        slug = slug.replace(' ', '-')[:50]

        # Create directory
        content_dir = Path(f"content/{lang}/{category}")
        content_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename with date in KST
        from datetime import timezone, timedelta
        kst = timezone(timedelta(hours=9))
        date_str = datetime.now(kst).strftime("%Y-%m-%d")
        filename = f"{date_str}-{slug}.md"
        filepath = content_dir / filename

        # Hugo frontmatter with required image field
        # Use placeholder if no Unsplash image available
        if not image_path:
            # Use category-based placeholder
            image_path = f"/images/placeholder-{category}.jpg"

        # Use KST timezone for date
        from datetime import timezone, timedelta
        kst = timezone(timedelta(hours=9))
        now_kst = datetime.now(kst)

        frontmatter = f"""---
title: "{title}"
date: {now_kst.strftime("%Y-%m-%dT%H:%M:%S%z")}
draft: false
categories: ["{category}"]
tags: {json.dumps(keyword.split()[:3])}
description: "{description}"
image: "{image_path}"
---

"""

        # Add hero image at the top of content if available
        hero_image = ""
        if image_path and image_credit:
            hero_image = f"![{keyword}]({image_path})\n\n"

        # Add image credit at the end of content if available
        credit_line = ""
        if image_credit:
            credit_line = f"\n\n---\n\n*Photo by [{image_credit['photographer']}]({image_credit['photographer_url']}) on [Unsplash]({image_credit['unsplash_url']})*\n"

        # Validate References section and remove if it contains fake URLs
        def has_fake_reference_url(url: str) -> bool:
            """Check if URL is a fake reference"""
            fake_patterns = [
                r'example\.com',
                r'example\.org',
                r'\.gov/[a-z-]+-202[0-9]',
                r'\.org/[a-z-]+-survey',
                r'\.gov/[a-z-]+-compliance',
                r'\.gov/[a-z-]+-report',
            ]
            for pattern in fake_patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    return True
            return False

        # Check if References section exists - if not, just skip it (don't add fake references)
        ref_headers = {
            'en': '## References',
            'ko': '## 참고자료',
            'ja': '## 参考文献'
        }
        ref_header = ref_headers.get(lang, '## References')

        # First, normalize any non-standard reference formats to standard format
        # Remove bold "**References:**" format if exists (common Claude output)
        bold_ref_patterns = [
            (r'\*\*References?:\*\*\n', ''),  # **References:**
            (r'\*\*参考(?:文献|資料):\*\*\n', ''),  # **参考文献:** or **参考資料:**
            (r'\*\*참고자료:\*\*\n', ''),  # **참고자료:**
        ]
        for pattern, replacement in bold_ref_patterns:
            content = re.sub(pattern, replacement, content)

        # Extract References section if exists
        has_references = ref_header in content or '## Reference' in content or '## 참고' in content or '## 参考' in content

        if has_references:
            # Extract URLs from References section using regex
            # Pattern: [text](url) or bare URLs
            url_pattern = r'https?://[^\s\)\]<>"]+'  
            urls_in_content = re.findall(url_pattern, content)

            # Check if any URLs are fake
            fake_urls = [url for url in urls_in_content if has_fake_reference_url(url)]

            if fake_urls:
                safe_print(f"  ⚠️  Fake reference URLs detected: {len(fake_urls)} found")
                safe_print(f"      Examples: {fake_urls[:3]}")

                # Remove References section entirely
                # Match from any References header to the next ## header or end of content
                ref_pattern = r'\n## (?:References?|参考(?:文献|資料)|참고자료)\n.*?(?=\n## |\Z)'
                content = re.sub(ref_pattern, '', content, flags=re.DOTALL)
                safe_print(f"  🗑️  Removed References section with fake URLs")
                has_references = False  # Mark as no valid references
            else:
                safe_print(f"  ✅ References section validated ({len(urls_in_content)} URLs)")

        # If no valid References section exists, add from queue
        if not has_references and topic.get('references'):
            references = topic['references']
            safe_print(f"  ℹ️  No References section in content, adding from queue ({len(references)} refs)")

            # Build References section
            ref_section = f"\n\n{ref_header}\n\n"
            for i, ref in enumerate(references, 1):
                ref_section += f"{i}. [{ref['title']}]({ref['url']})\n"

            # Append to content
            content = content.rstrip() + ref_section
            safe_print(f"  ✅ Added {len(references)} references from queue")
        elif not has_references:
            safe_print(f"  ℹ️  No references available (neither in content nor queue)")

        # Add affiliate links if applicable
        affiliate_programs_used = []
        if should_add_affiliate_links(category):
            safe_print(f"  🔗 Checking for product mentions to add affiliate links...")

            # Detect products mentioned in content
            detected_products = detect_product_mentions(content, lang, category)

            if detected_products:
                safe_print(f"  📦 Detected {len(detected_products)} products: {', '.join(detected_products[:3])}")

                # Add affiliate link for the first detected product only (to avoid being too commercial)
                primary_product = detected_products[0]
                link_data = generate_affiliate_link(primary_product, lang)

                if link_data:
                    # Find insertion point: after first ## section
                    sections = content.split('\n## ')
                    if len(sections) > 1:
                        # Insert after first section
                        affiliate_box = create_affiliate_box(primary_product, lang, link_data)
                        sections[1] = sections[1] + '\n' + affiliate_box
                        content = '\n## '.join(sections)

                        affiliate_programs_used.append(link_data['program'])
                        safe_print(f"  ✅ Added affiliate link for '{primary_product}' ({link_data['program']})")
                    else:
                        safe_print(f"  ⚠️  Could not find insertion point for affiliate link")
                else:
                    safe_print(f"  ℹ️  No affiliate program configured for {lang}")
            else:
                safe_print(f"  ℹ️  No product mentions detected")
        else:
            safe_print(f"  ℹ️  Affiliate links disabled for category: {category}")

        # Add affiliate disclosure if links were added
        if affiliate_programs_used:
            disclosure = get_affiliate_disclosure(lang, affiliate_programs_used)
            content = content.rstrip() + disclosure
            safe_print(f"  ⚠️  Added affiliate disclosure")

        # Write file with hero image at top
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            f.write(hero_image)
            f.write(content)
            f.write(credit_line)

        safe_print(f"  💾 Saved to: {filepath}")
        return filepath


def main():
    parser = argparse.ArgumentParser(description="Generate blog posts")
    parser.add_argument("--count", type=int, default=3, help="Number of posts to generate")
    parser.add_argument("--topic-id", type=str, help="Specific topic ID to generate")
    args = parser.parse_args()

    # Pre-flight checks
    safe_print(f"\n{'='*60}")
    safe_print(f"  🔍 Pre-flight Environment Checks")
    safe_print(f"{'='*60}\n")

    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    unsplash_key = os.environ.get("UNSPLASH_ACCESS_KEY")

    if anthropic_key:
        safe_print("  ✓ ANTHROPIC_API_KEY: Configured")
    else:
        safe_print("  ❌ ANTHROPIC_API_KEY: NOT FOUND")

    if unsplash_key:
        safe_print("  ✓ UNSPLASH_ACCESS_KEY: Configured")
    else:
        safe_print("  ⚠️  UNSPLASH_ACCESS_KEY: NOT FOUND")
        safe_print("     Posts will use placeholder images!")

    safe_print("")

    # Initialize generator
    try:
        generator = ContentGenerator()
    except ValueError as e:
        safe_print(f"Error: {str(e)}")
        safe_print("\nSet ANTHROPIC_API_KEY environment variable:")
        safe_print("  export ANTHROPIC_API_KEY='your-api-key'")
        sys.exit(1)

    # Get topics
    if args.topic_id:
        # Load specific topic (for testing)
        from topic_queue import get_queue
        queue = get_queue()
        data = queue._load_queue()
        topics = [t for t in data['topics'] if t['id'] == args.topic_id]
        if not topics:
            safe_print(f"Error: Topic {args.topic_id} not found")
            sys.exit(1)
    else:
        # Reserve topics from queue
        topics = reserve_topics(count=args.count)

    if not topics:
        safe_print("No topics available in queue")
        sys.exit(0)

    safe_print(f"\n{'='*60}")
    safe_print(f"  Generating {len(topics)} posts")
    safe_print(f"{'='*60}\n")

    generated_files = []

    for i, topic in enumerate(topics, 1):
        safe_print(f"[{i}/{len(topics)}] {topic['id']}")
        safe_print(f"  Keyword: {topic['keyword']}")
        safe_print(f"  Category: {topic['category']}")
        safe_print(f"  Language: {topic['lang']}")

        try:
            # Generate content
            safe_print(f"  → Step 1/5: Generating draft...")
            draft = generator.generate_draft(topic)

            safe_print(f"  → Step 2/5: Editing draft...")
            final_content = generator.edit_draft(draft, topic)

            # Generate metadata
            safe_print(f"  → Step 3/5: Generating metadata...")
            try:
                title = generator.generate_title(final_content, topic['keyword'], topic['lang'], topic.get('references'))
                description = generator.generate_description(final_content, topic['keyword'], topic['lang'])
            except Exception as e:
                safe_print(f"  ⚠️  WARNING: Metadata generation failed, using defaults")
                safe_print(f"     Error: {mask_secrets(str(e))}")
                title = topic['keyword']
                description = f"Article about {topic['keyword']}"

            # Fetch featured image
            safe_print(f"  → Step 4/5: Fetching image...")
            image_path = None
            image_credit = None
            try:
                image_info = generator.fetch_featured_image(topic['keyword'], topic['category'])
                if image_info:
                    image_path = generator.download_image(image_info, topic['keyword'])
                    if image_path:
                        image_credit = image_info
            except Exception as e:
                safe_print(f"  ⚠️  WARNING: Image fetch failed, will use placeholder")
                safe_print(f"     Error: {mask_secrets(str(e))}")

            # Save post with image
            safe_print(f"  → Step 5/5: Saving post...")
            try:
                filepath = generator.save_post(topic, title, description, final_content, image_path, image_credit)
            except IOError as e:
                safe_print(f"  ❌ ERROR: Failed to save post to filesystem")
                safe_print(f"     Error: {str(e)}")
                raise
            except Exception as e:
                safe_print(f"  ❌ ERROR: Unexpected error during save")
                safe_print(f"     Error: {mask_secrets(str(e))}")
                raise

            # Mark as completed
            if not args.topic_id:
                try:
                    mark_completed(topic['id'])
                except Exception as e:
                    safe_print(f"  ⚠️  WARNING: Failed to mark topic as completed in queue")
                    safe_print(f"     Topic ID: {topic['id']}")
                    safe_print(f"     Error: {str(e)}")
                    # Don't fail the whole process if queue update fails

            generated_files.append(str(filepath))
            safe_print(f"  ✅ Completed!\n")

        except KeyError as e:
            safe_print(f"  ❌ FAILED: Missing required field in topic data")
            safe_print(f"     Topic ID: {topic.get('id', 'unknown')}")
            safe_print(f"     Missing field: {str(e)}\n")
            if not args.topic_id:
                mark_failed(topic['id'], f"Missing field: {str(e)}")
        except ValueError as e:
            safe_print(f"  ❌ FAILED: Invalid data or API response")
            safe_print(f"     Topic ID: {topic.get('id', 'unknown')}")
            safe_print(f"     Error: {mask_secrets(str(e))}\n")
            if not args.topic_id:
                mark_failed(topic['id'], mask_secrets(str(e)))
        except Exception as e:
            safe_print(f"  ❌ FAILED: Unexpected error")
            safe_print(f"     Topic ID: {topic.get('id', 'unknown')}")
            safe_print(f"     Error type: {type(e).__name__}")
            safe_print(f"     Error: {mask_secrets(str(e))}\n")
            if not args.topic_id:
                mark_failed(topic['id'], mask_secrets(str(e)))

    # Save generated files list for quality gate
    output_file = Path("generated_files.json")
    with open(output_file, 'w') as f:
        json.dump(generated_files, f, indent=2)

    # Post-generation quality check
    safe_print(f"\n{'='*60}")
    safe_print(f"  📊 Post-Generation Quality Check")
    safe_print(f"{'='*60}\n")

    posts_without_references = 0
    posts_with_placeholders = 0

    for filepath in generated_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

                # Check for references section
                has_references = '## References' in content or '## 参考' in content or '## 참고자료' in content
                if not has_references:
                    posts_without_references += 1
                    safe_print(f"  ⚠️  No references: {Path(filepath).name}")

                # Check for placeholder images
                if 'placeholder-' in content:
                    posts_with_placeholders += 1
                    safe_print(f"  ⚠️  Placeholder image: {Path(filepath).name}")
        except Exception as e:
            safe_print(f"  ⚠️  Could not check: {Path(filepath).name}")

    safe_print("")

    if posts_without_references > 0:
        safe_print(f"🚨 WARNING: {posts_without_references}/{len(generated_files)} posts have NO references!")
        safe_print(f"   This reduces content credibility and SEO value.")
        safe_print(f"   FIX: Ensure Google Custom Search API is configured in keyword curation\n")

    if posts_with_placeholders > 0:
        safe_print(f"🚨 WARNING: {posts_with_placeholders}/{len(generated_files)} posts use PLACEHOLDER images!")
        safe_print(f"   This hurts user experience and engagement.")
        safe_print(f"   FIX: Ensure UNSPLASH_ACCESS_KEY is set in environment variables\n")

    if posts_without_references == 0 and posts_with_placeholders == 0:
        safe_print(f"✅ Quality Check PASSED: All posts have references and real images!\n")

    safe_print(f"{'='*60}")
    safe_print(f"  ✓ Generated {len(generated_files)} posts")
    safe_print(f"  File list saved to: {output_file}")
    safe_print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
