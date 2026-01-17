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
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from topic_queue import reserve_topics, mark_completed, mark_failed

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic package not installed")
    print("Install with: pip install anthropic")
    sys.exit(1)


# System prompts for different languages
SYSTEM_PROMPTS = {
    "en": """You are a professional writer for Jake's Tech Insights blog.

🎯 Goal: 800-1,100 words of concise, high-impact content (AdSense optimized)

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

⚠️ Core: Complete 800-1,100 word article. Plenty of headroom in 12,000 tokens!""",

    "ko": """당신은 Jake's Tech Insights 블로그의 전문 작가입니다.

🎯 핵심 목표: 800-1,100 단어의 간결하고 임팩트 있는 글 작성 (애드센스 최적화)

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

⚠️ 핵심: 800-1,100 단어로 완결된 글을 작성하세요. 12,000 토큰 내에서 여유있게!""",

    "ja": """あなたはJake's Tech Insightsブログのプロライターです。

🎯 核心目標: 3,000-4,500文字の簡潔でインパクトのある記事（AdSense最適化）

[長さガイド - 簡潔さが鍵！]
- 全体: 3,000-4,500文字（完読率を最適化）
- 各##セクション: 600-900文字（要点のみ）
- 導入部: 400-500文字（強力なフック）
- 結論: 300-400文字（明確なCTA）
- **最後の文まで必ず完成**: 途切れなく完結させてください

[収益化最適化の原則]
1. 最初の段落: 読者の悩みに共感（1-2文で強烈に）
2. 構造: 問題提起 → 核心解決策3つ → 実践ヒント → 結論
3. トーン: 親しい先輩エンジニアが話すような自然な口調
4. SEO: キーワード"{keyword}"を自然に4-6回含める
5. セクション: 3-4個の##見出し（各セクションは読みやすく）
6. 終わり: 明確なCTA - 質問または次のステップ

[自然な会話調（必須！）]
- "〜ですね", "〜ますよね", "〜でしょう" など柔らかい語尾
- "実は", "ちなみに", "さて", "それで" などの自然な接続詞
- "〜してみましょう", "〜してみてください" など提案形
- 質問形で読者を引き込む: "どうでしょうか？", "気になりませんか？"
- 短い感嘆: "驚きですね。", "面白いですよね。", "これがポイントです。"

[スタイル - 完読率最適化]
- 能動態中心、短い文（1-2行）
- 要点のみ伝達（不要な説明削除）
- 具体的な数字/例（1-2個のみ選択的に）
- 箇条書き積極活用（スキャン可能に）
- 段落の終わりにフック: "これがポイントです。"

[絶対禁止]
- 冗長表現: 同じ内容の繰り返し ❌
- AI的表現: "もちろん", "〜することが重要です"
- 硬い文体: 教科書のような説明調
- 抽象的: "革新的", "ゲームチェンジャー", "注目すべき"
- 過度な絵文字、不要な事例の羅列

⚠️ 核心: 3,000-4,500文字で完結した記事を書いてください。12,000トークン内で余裕を持って！"""
}


class ContentGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize content generator with Claude API"""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Set it as environment variable or pass to constructor."
            )

        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"

    def generate_draft(self, topic: Dict) -> str:
        """Generate initial draft using Draft Agent"""
        keyword = topic['keyword']
        lang = topic['lang']
        category = topic['category']

        system_prompt = SYSTEM_PROMPTS[lang].format(keyword=keyword)

        # User prompt
        user_prompt = self._get_draft_prompt(keyword, category, lang)

        print(f"  📝 Generating draft for: {keyword}")

        response = self.client.messages.create(
            model=self.model,
            max_tokens=12000,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": user_prompt
            }]
        )

        draft = response.content[0].text
        print(f"  ✓ Draft generated ({len(draft)} chars)")
        return draft

    def edit_draft(self, draft: str, topic: Dict) -> str:
        """Refine draft using Editor Agent"""
        lang = topic['lang']

        print(f"  ✏️  Editing draft...")

        editor_prompt = self._get_editor_prompt(lang)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=12000,
            messages=[
                {
                    "role": "user",
                    "content": f"{editor_prompt}\n\n---\n\n{draft}"
                }
            ]
        )

        edited = response.content[0].text
        print(f"  ✓ Draft edited ({len(edited)} chars)")
        return edited

    def _get_draft_prompt(self, keyword: str, category: str, lang: str) -> str:
        """Get draft generation prompt based on language"""
        prompts = {
            "en": f"""Write a comprehensive blog post about: {keyword}

Category: {category}

⏱️ Reading Time Target: 4-5 minutes
- Write 3-4 main sections (## headings)
- Each section: 1-2 minutes to read, one key point
- Short paragraphs (2-4 sentences each)
- End with a thought-provoking question

Content Guidelines:
- Target audience: Tech-savvy professionals and enthusiasts
- Include 1-2 practical examples (be selective)
- Mention current trends (2025)
- Use specific numbers when relevant
- Be concise and impactful - avoid unnecessary explanations

Write the complete blog post now (body only, no title or metadata):""",

            "ko": f"""다음 주제로 포괄적인 블로그 글을 작성하세요: {keyword}

카테고리: {category}

⏱️ 읽기 시간 목표: 4-5분
- 3-4개의 주요 섹션 (## 헤딩) 작성
- 각 섹션: 1-2분 읽기 분량, 하나의 핵심 포인트
- 짧은 문단 사용 (2-4 문장씩)
- 생각을 자극하는 질문으로 마무리

콘텐츠 가이드라인:
- 대상 독자: 기술에 관심있는 전문가와 얼리어답터
- 실용적인 예시 1-2개 포함 (선택적으로)
- 현재 트렌드 언급 (2025년)
- 관련성 있는 구체적 숫자 사용
- 간결하고 임팩트 있게 - 불필요한 설명 제거

지금 바로 완전한 블로그 글을 작성하세요 (본문만, 제목이나 메타데이터 제외):""",

            "ja": f"""次のトピックについて包括的なブログ記事を書いてください: {keyword}

カテゴリ: {category}

⏱️ 読む時間の目標: 4-5分
- 3-4個の主要セクション (##見出し) を作成
- 各セクション: 1-2分で読める分量、1つの重要ポイント
- 短い段落を使用 (2-4文ずつ)
- 考えさせる質問で締めくくる

コンテンツガイドライン:
- 対象読者: 技術に精通した専門家と愛好家
- 実践的な例を1-2個含める (選択的に)
- 現在のトレンドに言及 (2025年)
- 関連性のある具体的な数字を使用
- 簡潔でインパクトのある内容 - 不要な説明を削除

今すぐ完全なブログ記事を書いてください（本文のみ、タイトルやメタデータなし）:"""
        }

        return prompts[lang]

    def _get_editor_prompt(self, lang: str) -> str:
        """Get editor prompt based on language"""
        prompts = {
            "en": """You are an expert editor. Transform this into Medium-style content:

🚨 Important: Keep the same length. Do NOT make it longer or shorter!

Tasks:
1. **Medium style conversion**: Add "you/I", conversational tone
2. **Eliminate all AI tells**: "certainly", "moreover", "it's important to note"
3. **Natural connectors**: "Look", "Here's why", "The truth is"
4. **Break fourth wall**: "You might be thinking...", "Sound familiar?"
5. **Punchy sentences**: "Here's the thing.", "Let me explain.", "Stop it."
6. **Smooth transitions**: "Now", "Here's where it gets interesting"
7. Keep all factual information intact
8. **Maintain length**: Aim for similar word count as original
9. **Complete ending**: Finish conclusion fully

Return improved version (body only, no title):""",

            "ko": """당신은 전문 에디터입니다. 이 블로그 글을 토스(Toss) 스타일로 개선하세요:

🚨 중요: 같은 길이를 유지하세요. 늘리거나 줄이지 마세요!

작업:
1. **토스 말투로 변환**: "~습니다" → "~해요", 친근한 질문형 추가
2. AI 느낌 완전 제거: "물론", "~할 수 있습니다", "중요합니다" 모두 삭제
3. 자연스러운 접속사: "사실", "실제로", "그런데", "참고로"
4. 숫자를 친근하게: "50% → 절반", "3배 → 세 배"
5. 짧고 강렬한 문장 추가: "놀랍죠?", "맞아요.", "이게 핵심이에요."
6. 섹션 간 매끄러운 전환: "자, 이제 ~", "그럼 ~"
7. 모든 사실 정보는 그대로 유지
8. **길이 유지**: 원본과 비슷한 단어 수 목표
9. **마지막 문장까지 완결**: 결론을 반드시 완성

개선된 버전을 반환하세요 (본문만, 제목 제외):""",

            "ja": """あなたは専門エディターです。このブログ記事を自然な会話調に改善してください:

🚨 重要: 同じ長さを保ってください。長くしたり短くしたりしないでください！

タスク:
1. **会話調に変換**: "〜ですね", "〜ますよね", "〜でしょう" など柔らかい語尾に
2. AI的な表現を完全削除: "もちろん", "〜することが重要です", "〜について説明します"
3. 自然な接続詞: "実は", "ちなみに", "さて", "それで"
4. 提案形を追加: "〜してみましょう", "〜してみてください"
5. 質問形で引き込む: "どうでしょうか？", "気になりませんか？"
6. 短い感嘆: "驚きですね。", "面白いですよね。"
7. セクション間の移行: "では、詳しく見ていきましょう。"
8. すべての事実情報はそのまま保持
9. **長さを維持**: 元の記事と同じ程度の文字数を目標に
10. **最後の文まで完結**: 結論を必ず完成

改善されたバージョンを返してください（本文のみ、タイトルなし）:"""
        }

        return prompts[lang]

    def generate_title(self, content: str, keyword: str, lang: str) -> str:
        """Generate SEO-friendly title"""
        prompts = {
            "en": f"Generate a catchy, SEO-friendly blog title (50-60 chars) for a post about '{keyword}'. Return ONLY the title, nothing else.",
            "ko": f"'{keyword}'에 대한 블로그 글의 매력적이고 SEO 친화적인 제목을 생성하세요 (50-60자). 제목만 반환하세요.",
            "ja": f"'{keyword}'に関するブログ記事の魅力的でSEOフレンドリーなタイトルを生成してください（50-60文字）。タイトルのみを返してください。"
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

    def save_post(self, topic: Dict, title: str, description: str, content: str) -> Path:
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

        # Generate filename with date
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date_str}-{slug}.md"
        filepath = content_dir / filename

        # Hugo frontmatter
        frontmatter = f"""---
title: "{title}"
date: {datetime.now().strftime("%Y-%m-%d")}
draft: false
categories: ["{category}"]
tags: {json.dumps(keyword.split()[:3])}
description: "{description}"
---

"""

        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            f.write(content)

        print(f"  💾 Saved to: {filepath}")
        return filepath


def main():
    parser = argparse.ArgumentParser(description="Generate blog posts")
    parser.add_argument("--count", type=int, default=3, help="Number of posts to generate")
    parser.add_argument("--topic-id", type=str, help="Specific topic ID to generate")
    args = parser.parse_args()

    # Initialize generator
    try:
        generator = ContentGenerator()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nSet ANTHROPIC_API_KEY environment variable:")
        print("  export ANTHROPIC_API_KEY='your-api-key'")
        sys.exit(1)

    # Get topics
    if args.topic_id:
        # Load specific topic (for testing)
        from topic_queue import get_queue
        queue = get_queue()
        data = queue._load_queue()
        topics = [t for t in data['topics'] if t['id'] == args.topic_id]
        if not topics:
            print(f"Error: Topic {args.topic_id} not found")
            sys.exit(1)
    else:
        # Reserve topics from queue
        topics = reserve_topics(count=args.count)

    if not topics:
        print("No topics available in queue")
        sys.exit(0)

    print(f"\n{'='*60}")
    print(f"  Generating {len(topics)} posts")
    print(f"{'='*60}\n")

    generated_files = []

    for i, topic in enumerate(topics, 1):
        print(f"[{i}/{len(topics)}] {topic['id']}")
        print(f"  Keyword: {topic['keyword']}")
        print(f"  Category: {topic['category']}")
        print(f"  Language: {topic['lang']}")

        try:
            # Generate content
            draft = generator.generate_draft(topic)
            final_content = generator.edit_draft(draft, topic)

            # Generate metadata
            print(f"  📋 Generating metadata...")
            title = generator.generate_title(final_content, topic['keyword'], topic['lang'])
            description = generator.generate_description(final_content, topic['keyword'], topic['lang'])

            # Save post
            filepath = generator.save_post(topic, title, description, final_content)

            # Mark as completed
            if not args.topic_id:
                mark_completed(topic['id'])

            generated_files.append(str(filepath))
            print(f"  ✅ Completed!\n")

        except Exception as e:
            print(f"  ❌ Failed: {e}\n")
            if not args.topic_id:
                mark_failed(topic['id'], str(e))

    # Save generated files list for quality gate
    output_file = Path("generated_files.json")
    with open(output_file, 'w') as f:
        json.dump(generated_files, f, indent=2)

    print(f"{'='*60}")
    print(f"  ✓ Generated {len(generated_files)} posts")
    print(f"  File list saved to: {output_file}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
