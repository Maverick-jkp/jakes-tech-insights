#!/usr/bin/env python3
"""
Affiliate Link Configuration and Management

Supports multiple affiliate programs:
- Coupang Partners (Korea)
- Amazon Associates (International)
- Rakuten Affiliate (Japan)
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

# Affiliate Program IDs
COUPANG_PARTNERS_ID = os.getenv("COUPANG_PARTNERS_ID", "")
AMAZON_ASSOCIATES_TAG = os.getenv("AMAZON_ASSOCIATES_TAG", "")
RAKUTEN_AFFILIATE_ID = os.getenv("RAKUTEN_AFFILIATE_ID", "")

# Product keyword mapping for auto-detection
AFFILIATE_KEYWORDS = {
    "tech": {
        "en": ["iphone", "macbook", "laptop", "headphone", "speaker", "camera",
               "keyboard", "mouse", "monitor", "tablet", "ipad", "airpods",
               "smartwatch", "gaming pc", "graphics card", "ssd", "external drive"],
        "ko": ["아이폰", "맥북", "노트북", "헤드폰", "스피커", "카메라",
               "키보드", "마우스", "모니터", "태블릿", "아이패드", "에어팟",
               "스마트워치", "게이밍 PC", "그래픽카드", "SSD", "외장하드"],
        "ja": ["iPhone", "MacBook", "ノートPC", "ヘッドホン", "スピーカー", "カメラ",
               "キーボード", "マウス", "モニター", "タブレット", "iPad", "AirPods"]
    },
    "finance": {
        "en": ["book", "financial planning", "investing guide", "credit card"],
        "ko": ["책", "재테크", "투자", "신용카드"],
        "ja": ["本", "投資ガイド", "クレジットカード"]
    },
    "entertainment": {
        "en": ["movie", "book", "game", "subscription", "streaming service"],
        "ko": ["영화", "책", "게임", "구독", "스트리밍"],
        "ja": ["映画", "本", "ゲーム", "サブスク"]
    }
}

# Affiliate link templates by program and language
AFFILIATE_TEMPLATES = {
    "coupang": {
        "base_url": "https://www.coupang.com/np/search",
        "template": "https://link.coupang.com/a/{partner_id}",
        "search_template": "https://www.coupang.com/np/search?q={query}&channel=user",
        "languages": ["ko"],
        "disclosure_ko": "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."
    },
    "amazon": {
        "base_url": "https://www.amazon.com/s",
        "template": "https://www.amazon.com/s?k={query}&tag={tag}",
        "languages": ["en"],
        "disclosure_en": "As an Amazon Associate, I earn from qualifying purchases."
    },
    "rakuten": {
        "base_url": "https://search.rakuten.co.jp/search/mall",
        "template": "https://search.rakuten.co.jp/search/mall/{query}/?f=1&grp=product",
        "languages": ["ja"],
        "disclosure_ja": "この記事にはアフィリエイトリンクが含まれています。"
    }
}


def detect_product_mentions(content: str, lang: str, category: str) -> List[str]:
    """
    Detect product mentions in content based on keywords.

    Args:
        content: The blog post content
        lang: Language code (en, ko, ja)
        category: Content category (tech, finance, entertainment)

    Returns:
        List of detected product keywords
    """
    content_lower = content.lower()
    detected = []

    if category in AFFILIATE_KEYWORDS and lang in AFFILIATE_KEYWORDS[category]:
        keywords = AFFILIATE_KEYWORDS[category][lang]
        for keyword in keywords:
            if keyword.lower() in content_lower:
                detected.append(keyword)

    return detected


def generate_affiliate_link(product: str, lang: str, program: str = "auto") -> Optional[Dict[str, str]]:
    """
    Generate affiliate link for a product.

    Args:
        product: Product name or keyword
        lang: Language code (en, ko, ja)
        program: Affiliate program ('coupang', 'amazon', 'rakuten', or 'auto')

    Returns:
        Dictionary with 'url' and 'disclosure' keys, or None if not applicable
    """
    # Auto-select program based on language
    if program == "auto":
        if lang == "ko" and COUPANG_PARTNERS_ID:
            program = "coupang"
        elif lang == "en" and AMAZON_ASSOCIATES_TAG:
            program = "amazon"
        elif lang == "ja" and RAKUTEN_AFFILIATE_ID:
            program = "rakuten"
        else:
            return None

    # Generate link based on program
    if program == "coupang" and COUPANG_PARTNERS_ID:
        template = AFFILIATE_TEMPLATES["coupang"]
        url = template["search_template"].format(query=product.replace(" ", "+"))
        return {
            "url": url,
            "disclosure": template["disclosure_ko"],
            "program": "coupang"
        }

    elif program == "amazon" and AMAZON_ASSOCIATES_TAG:
        template = AFFILIATE_TEMPLATES["amazon"]
        url = template["template"].format(
            query=product.replace(" ", "+"),
            tag=AMAZON_ASSOCIATES_TAG
        )
        return {
            "url": url,
            "disclosure": template["disclosure_en"],
            "program": "amazon"
        }

    elif program == "rakuten" and RAKUTEN_AFFILIATE_ID:
        template = AFFILIATE_TEMPLATES["rakuten"]
        url = template["template"].format(query=product.replace(" ", "+"))
        return {
            "url": url,
            "disclosure": template["disclosure_ja"],
            "program": "rakuten"
        }

    return None


def create_affiliate_box(product: str, lang: str, link_data: Dict[str, str]) -> str:
    """
    Create HTML affiliate box to insert in content.

    Args:
        product: Product name
        lang: Language code
        link_data: Dictionary from generate_affiliate_link()

    Returns:
        HTML string for affiliate box
    """
    translations = {
        "en": {
            "check_prices": "Check prices on",
            "related_product": "Related Product"
        },
        "ko": {
            "check_prices": "가격 확인하기",
            "related_product": "관련 제품"
        },
        "ja": {
            "check_prices": "価格をチェック",
            "related_product": "関連商品"
        }
    }

    t = translations.get(lang, translations["en"])
    program_name = {
        "coupang": "쿠팡",
        "amazon": "Amazon",
        "rakuten": "楽天市場"
    }.get(link_data["program"], "")

    return f"""
<div class="affiliate-box" style="
    border: 2px solid var(--accent, #00ff88);
    border-radius: 8px;
    padding: 1rem;
    margin: 1.5rem 0;
    background: var(--surface, #151515);
">
    <p style="margin: 0 0 0.5rem 0; font-weight: 600;">
        💡 {t['related_product']}: {product}
    </p>
    <a href="{link_data['url']}"
       target="_blank"
       rel="nofollow sponsored noopener"
       style="
           display: inline-block;
           padding: 0.5rem 1rem;
           background: var(--accent, #00ff88);
           color: var(--bg-primary, #0a0a0a);
           text-decoration: none;
           border-radius: 4px;
           font-weight: 600;
       ">
        {t['check_prices']} {program_name} →
    </a>
</div>
"""


def get_affiliate_disclosure(lang: str, programs: List[str]) -> str:
    """
    Get full affiliate disclosure text for footer.

    Args:
        lang: Language code
        programs: List of affiliate programs used

    Returns:
        Disclosure text in appropriate language
    """
    disclosures = []

    if "coupang" in programs:
        disclosures.append(AFFILIATE_TEMPLATES["coupang"]["disclosure_ko"])

    if "amazon" in programs:
        disclosures.append(AFFILIATE_TEMPLATES["amazon"]["disclosure_en"])

    if "rakuten" in programs:
        disclosures.append(AFFILIATE_TEMPLATES["rakuten"]["disclosure_ja"])

    if not disclosures:
        return ""

    # Create disclosure box
    disclosure_text = "\n\n".join(disclosures)

    return f"""
---

<div class="affiliate-disclosure" style="
    font-size: 0.875rem;
    color: var(--text-secondary, #a0a0a0);
    border-top: 1px solid var(--border, #2a2a2a);
    padding-top: 1rem;
    margin-top: 2rem;
">
    <p><strong>⚠️ Disclosure</strong></p>
    <p>{disclosure_text}</p>
</div>
"""


# Configuration: Which categories should include affiliate links
# DISABLED: Focusing on Google AdSense first for better ROI
AFFILIATE_ENABLED_CATEGORIES = {
    "tech": False,  # Disabled: AdSense priority
    "finance": False,
    "entertainment": False,  # Disabled: AdSense priority
    "business": False,
    "science": False,
    "travel": False
}


def should_add_affiliate_links(category: str) -> bool:
    """Check if affiliate links should be added for this category."""
    return AFFILIATE_ENABLED_CATEGORIES.get(category, False)
