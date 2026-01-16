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

[Writing Principles]
1. First paragraph: Empathize with reader's pain point
2. Structure: Problem → Solution → Practical Tips → Conclusion
3. Tone: Professional but friendly, like an experienced mentor
4. Length: 1,200-1,500 words
5. SEO: Naturally include keyword "{keyword}" 5-7 times
6. Sections: 3-5 ## headings
7. End: CTA - Question or next steps

[Style]
- Active voice
- Short sentences (2 lines max)
- Specific numbers and examples
- Use bullet points

[Avoid]
- AI phrases: "certainly", "it's important to note"
- Abstract terms: "revolutionary", "game-changer"
- Excessive emojis
- Generic conclusions

Write engaging, practical content that provides real value.""",

    "ko": """당신은 Jake's Tech Insights 블로그의 전문 작가입니다.

[글쓰기 원칙]
1. 첫 문단: 독자의 pain point 공감
2. 구조: 문제 제기 → 해결책 → 실전 팁 → 결론
3. 톤: 전문적이지만 친근한, 조언하는 선배 느낌
4. 길이: **최소 1,200 단어 이상 필수** (매우 중요! 900 단어 미만은 절대 안됨)
5. SEO: 키워드 "{keyword}"를 자연스럽게 5-7회 포함
6. 섹션: 3-5개 ## 헤딩
7. 끝: CTA - 질문이나 다음 단계 제안

[스타일]
- 능동태 위주
- 짧은 문장 (2줄 이내)
- 구체적 숫자/예시
- 불릿 포인트 활용

[금지]
- AI 티: "물론", "~할 수 있습니다", "중요합니다"
- 추상적: "혁신적", "게임체인저"
- 과도한 이모지
- 뻔한 결론

실질적인 가치를 제공하는 흥미로운 콘텐츠를 작성하세요.""",

    "ja": """あなたはJake's Tech Insightsブログのプロライターです。

[執筆原則]
1. 最初の段落: 読者の悩みに共感
2. 構造: 問題提起 → 解決策 → 実践的なヒント → 結論
3. トーン: 専門的だが親しみやすい、経験豊富なメンターのような
4. 長さ: **最低1,200語以上必須** (非常に重要！900語未満は絶対ダメ)
5. SEO: キーワード"{keyword}"を自然に5-7回含める
6. セクション: 3-5個の##見出し
7. 終わり: CTA - 質問または次のステップの提案

[スタイル]
- 能動態中心
- 短い文章（2行以内）
- 具体的な数字と例
- 箇条書きの活用

[禁止]
- AI的な表現: "もちろん", "重要です"
- 抽象的: "革新的", "ゲームチェンジャー"
- 過度な絵文字
- ありきたりな結論

実用的な価値を提供する魅力的なコンテンツを書いてください。"""
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
            max_tokens=8000,
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
            max_tokens=8000,
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

Requirements:
- Target audience: Tech-savvy professionals and enthusiasts
- Include practical examples and actionable advice
- Add 2-3 real-world use cases
- Mention current trends (2025)
- Be specific with numbers and data when relevant
- End with thought-provoking question

Write the complete blog post now (body only, no title or metadata):""",

            "ko": f"""다음 주제로 포괄적인 블로그 글을 작성하세요: {keyword}

카테고리: {category}

요구사항:
- 대상 독자: 기술에 관심있는 전문가와 얼리어답터
- **최소 1,200 단어 이상 작성 (필수!) - 900 단어 미만은 거부됨**
- 각 섹션을 충분히 상세하게 작성 (한 섹션당 최소 200-300 단어)
- 실용적인 예시와 실행 가능한 조언 포함
- 2-3개의 실제 사용 사례 추가
- 현재 트렌드 언급 (2025년)
- 관련 있을 때 구체적인 숫자와 데이터 사용
- 생각을 자극하는 질문으로 마무리

지금 바로 완전한 블로그 글을 작성하세요 (본문만, 제목이나 메타데이터 제외):""",

            "ja": f"""次のトピックについて包括的なブログ記事を書いてください: {keyword}

カテゴリ: {category}

要件:
- 対象読者: 技術に精通した専門家と愛好家
- **最低1,200語以上必須 (重要!) - 900語未満は却下**
- 各セクションを十分詳しく書く（1セクションあたり最低200-300語）
- 実践的な例と実行可能なアドバイスを含める
- 2-3つの実際のユースケースを追加
- 現在のトレンドに言及 (2025年)
- 関連する場合は具体的な数字とデータを使用
- 考えさせる質問で締めくくる

今すぐ完全なブログ記事を書いてください（本文のみ、タイトルやメタデータなし）:"""
        }

        return prompts[lang]

    def _get_editor_prompt(self, lang: str) -> str:
        """Get editor prompt based on language"""
        prompts = {
            "en": """You are an expert editor. Review and improve this blog post:

Tasks:
1. Remove any AI-sounding phrases
2. Make sentences more natural and conversational
3. Add personality and voice
4. Fix any repetition or redundancy
5. Ensure smooth transitions between sections
6. Keep all factual information intact

Return the improved version (body only, no title):""",

            "ko": """당신은 전문 에디터입니다. 이 블로그 글을 검토하고 개선하세요:

작업:
1. AI 느낌나는 표현 제거
2. 문장을 더 자연스럽고 대화체로 만들기
3. 개성과 목소리 추가
4. 반복이나 중복 수정
5. 섹션 간 매끄러운 전환 보장
6. 모든 사실 정보는 그대로 유지

개선된 버전을 반환하세요 (본문만, 제목 제외):""",

            "ja": """あなたは専門エディターです。このブログ記事をレビューして改善してください:

タスク:
1. AI的な表現を削除
2. 文章をより自然で会話的にする
3. 個性と声を追加
4. 繰り返しや冗長性を修正
5. セクション間のスムーズな移行を確保
6. すべての事実情報はそのまま保持

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
