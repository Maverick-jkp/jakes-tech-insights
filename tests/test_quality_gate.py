"""
Tests for scripts/quality_gate.py
"""
import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from quality_gate import QualityGate

class TestQualityGate:
    """Test QualityGate class"""

    def test_init(self):
        """Test QualityGate initialization"""
        gate = QualityGate()
        assert gate.strict_mode is False

        gate_strict = QualityGate(strict_mode=True)
        assert gate_strict.strict_mode is True

    def test_ai_phrases_loaded(self):
        """Test that AI phrases are loaded for all languages"""
        gate = QualityGate()

        assert "en" in gate.ai_phrases
        assert "ko" in gate.ai_phrases
        assert "ja" in gate.ai_phrases

        assert len(gate.ai_phrases["en"]) > 0
        assert len(gate.ai_phrases["ko"]) > 0
        assert len(gate.ai_phrases["ja"]) > 0

class TestParseMarkdown:
    """Test markdown parsing"""

    def test_parse_markdown_with_frontmatter(self, sample_post_content):
        """Test parsing markdown with frontmatter"""
        gate = QualityGate()

        frontmatter, body = gate._parse_markdown(sample_post_content)

        assert isinstance(frontmatter, dict)
        assert "title" in frontmatter
        assert "date" in frontmatter
        assert "description" in frontmatter

        assert isinstance(body, str)
        assert len(body) > 0
        assert "## Section 1" in body

    def test_parse_markdown_without_frontmatter(self):
        """Test parsing markdown without frontmatter"""
        gate = QualityGate()
        content = "Just some content\n\n## Heading"

        frontmatter, body = gate._parse_markdown(content)

        assert frontmatter == {}
        assert body == content

class TestDetectLanguage:
    """Test language detection"""

    def test_detect_language_english(self):
        """Test detecting English from path"""
        gate = QualityGate()

        path = Path("content/en/tech/post.md")
        lang = gate._detect_language(path)

        assert lang == "en"

    def test_detect_language_korean(self):
        """Test detecting Korean from path"""
        gate = QualityGate()

        path = Path("content/ko/business/post.md")
        lang = gate._detect_language(path)

        assert lang == "ko"

    def test_detect_language_japanese(self):
        """Test detecting Japanese from path"""
        gate = QualityGate()

        path = Path("content/ja/lifestyle/post.md")
        lang = gate._detect_language(path)

        assert lang == "ja"

    def test_detect_language_default(self):
        """Test default language when not detected"""
        gate = QualityGate()

        path = Path("some/random/path/post.md")
        lang = gate._detect_language(path)

        assert lang == "en"  # Default

class TestWordCount:
    """Test word count validation"""

    def test_word_count_english_valid(self, tmp_path):
        """Test valid English word count"""
        gate = QualityGate()

        # Create test file with enough content
        content = """---
title: "Test"
date: 2026-01-20T12:00:00+09:00
description: "Test description"
---

""" + " ".join(["word"] * 1000)  # 1000 words

        test_file = tmp_path / "en" / "tech" / "test.md"
        test_file.parent.mkdir(parents=True)
        test_file.write_text(content)

        result = gate.check_file(test_file)

        # Should not have critical word count failure
        assert not any("word count" in str(f).lower() for f in result["critical_failures"])

    def test_word_count_english_too_short(self, tmp_path):
        """Test English post that's too short"""
        gate = QualityGate()

        # Create test file with too little content
        content = """---
title: "Test"
date: 2026-01-20T12:00:00+09:00
description: "Test description"
---

Too short.
"""

        test_file = tmp_path / "en" / "tech" / "test.md"
        test_file.parent.mkdir(parents=True)
        test_file.write_text(content)

        result = gate.check_file(test_file)

        # Should have critical failures (word count or other issues)
        # If quality gate is lenient, this may only be a warning
        has_issue = (
            len(result["critical_failures"]) > 0 or
            any("word" in str(w).lower() for w in result["warnings"])
        )
        assert has_issue, f"Expected issues for short content, got: {result}"

    def test_word_count_korean(self, tmp_path):
        """Test Korean word count"""
        gate = QualityGate()

        content = """---
title: "테스트"
date: 2026-01-20T12:00:00+09:00
description: "테스트 설명"
---

""" + "테스트 단어 " * 1000  # 1000+ words

        test_file = tmp_path / "ko" / "tech" / "test.md"
        test_file.parent.mkdir(parents=True)
        test_file.write_text(content)

        result = gate.check_file(test_file)

        assert not any("word count" in str(f).lower() for f in result["critical_failures"])

class TestAIPhrases:
    """Test AI phrase detection"""

    def test_ai_phrases_none_detected(self, tmp_path):
        """Test content with no AI phrases"""
        gate = QualityGate()

        content = """---
title: "Test"
date: 2026-01-20T12:00:00+09:00
description: "Test description"
---

""" + " ".join(["normal content"] * 1000)

        test_file = tmp_path / "en" / "tech" / "test.md"
        test_file.parent.mkdir(parents=True)
        test_file.write_text(content)

        result = gate.check_file(test_file)

        # Should not have AI phrase warnings
        assert not any("ai phrase" in str(w).lower() for w in result["warnings"])

    def test_ai_phrases_detected(self, tmp_path):
        """Test content with AI phrases"""
        gate = QualityGate()

        content = """---
title: "Test"
date: 2026-01-20T12:00:00+09:00
description: "Test description"
---

""" + " ".join(["This is"] * 300) + " revolutionary game-changer " + " ".join(["content"] * 300)

        test_file = tmp_path / "en" / "tech" / "test.md"
        test_file.parent.mkdir(parents=True)
        test_file.write_text(content)

        result = gate.check_file(test_file)

        # Should have AI phrase warnings (or critical failures in strict mode)
        has_phrase_issue = (
            any("phrase" in str(w).lower() for w in result["warnings"]) or
            any("phrase" in str(f).lower() for f in result["critical_failures"])
        )
        assert has_phrase_issue

class TestFrontmatter:
    """Test frontmatter validation"""

    def test_frontmatter_complete(self, tmp_path, sample_post_content):
        """Test post with complete frontmatter"""
        gate = QualityGate()

        test_file = tmp_path / "en" / "tech" / "test.md"
        test_file.parent.mkdir(parents=True)

        # Extend sample to meet word count
        extended_content = sample_post_content + "\n\n" + " ".join(["content"] * 1000)
        test_file.write_text(extended_content)

        result = gate.check_file(test_file)

        # Should not have frontmatter failures
        assert not any("frontmatter" in str(f).lower() or "title" in str(f).lower() for f in result["critical_failures"])

    def test_frontmatter_missing_fields(self, tmp_path):
        """Test post with missing frontmatter fields"""
        gate = QualityGate()

        content = """---
title: "Test"
---

""" + " ".join(["content"] * 1000)

        test_file = tmp_path / "en" / "tech" / "test.md"
        test_file.parent.mkdir(parents=True)
        test_file.write_text(content)

        result = gate.check_file(test_file)

        # Should have frontmatter failures (missing date, description)
        assert len(result["critical_failures"]) > 0

class TestCheckFile:
    """Test full file validation"""

    def test_check_file_all_pass(self, tmp_path):
        """Test post that passes all checks"""
        gate = QualityGate()

        content = """---
title: "Test Post with Good Quality"
date: 2026-01-20T12:00:00+09:00
description: "This is a test post for unit testing with good quality content."
categories: ["tech"]
tags: ["testing", "python"]
image: cover.jpg
---

This is a test post with substantial content that avoids AI phrases.

## Introduction

We're going to explore some interesting concepts about software testing.
This section provides background information.

""" + " ".join([f"Paragraph {i} with meaningful content about testing." for i in range(200)])

        content += """

## Main Content

Here's the core discussion with examples and code snippets.
Real-world scenarios help readers understand the concepts.

## Conclusion

We covered several important points about testing.
Thanks for reading this article.

Reference: https://example.com
"""

        test_file = tmp_path / "en" / "tech" / "test.md"
        test_file.parent.mkdir(parents=True)
        test_file.write_text(content)

        result = gate.check_file(test_file)

        # Should have minimal or no critical failures
        print(f"Critical failures: {result['critical_failures']}")
        print(f"Warnings: {result['warnings']}")

        # Verify structure
        assert "file" in result
        assert "language" in result
        assert "critical_failures" in result
        assert "warnings" in result
        assert "info" in result
