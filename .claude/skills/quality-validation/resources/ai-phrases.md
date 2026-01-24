# AI Phrase Blacklist

Complete list of banned phrases that trigger quality gate failures.

---

## English Banned Phrases

**Generic AI Phrases**:
- "revolutionary"
- "game-changer"
- "cutting-edge"
- "state-of-the-art"
- "paradigm shift"
- "disruptive innovation"

**Filler Phrases**:
- "it's important to note"
- "it's worth mentioning"
- "it should be noted that"
- "in today's digital landscape"
- "in this day and age"
- "at the end of the day"

**Conclusion Phrases** (allowed only in conclusion section):
- "in conclusion"
- "in summary"
- "to sum up"
- "all in all"

**Detection Logic**:
- Case-insensitive search
- Fails if found anywhere except conclusion (for conclusion phrases)
- Reports phrase and line number

---

## Korean Banned Phrases (한국어)

**AI 특유 표현**:
- "물론"
- "혁신적"
- "게임체인저"
- "패러다임 전환"

**불필요한 강조**:
- "디지털 시대"
- "현대 사회"
- "중요한 점은"
- "말할 필요도 없이"

**결론 표현** (결론 섹션에서만 허용):
- "결론적으로"
- "요약하자면"
- "정리하면"

---

## Japanese Banned Phrases (日本語)

**AI特有の表現**:
- "もちろん"
- "革新的"
- "ゲームチェンジャー"
- "パラダイムシフト"

**不要な強調**:
- "デジタル時代"
- "現代社会"
- "重要なのは"
- "言うまでもなく"

**結論表現** (結論セクションのみ許可):
- "結論として"
- "要約すると"
- "まとめると"

---

## Usage in Quality Gate

**Script**: `scripts/quality_gate.py`

**Detection Method**:
```python
def check_ai_phrases(content, language):
    """Search for blacklisted phrases."""
    phrases = AI_PHRASES_EN if language == 'en' else AI_PHRASES_KO

    for phrase in phrases:
        if phrase.lower() in content.lower():
            # Check if in conclusion section
            if phrase in CONCLUSION_PHRASES:
                if not in_conclusion_section(content, phrase):
                    return {"status": "FAIL", "phrase": phrase}
            else:
                return {"status": "FAIL", "phrase": phrase}

    return {"status": "PASS"}
```

**Result**:
- **PASS**: No banned phrases found
- **FAIL**: Banned phrase detected, reports phrase and line number

---

## Adding New Phrases

**To add a new banned phrase**:

1. Edit `scripts/quality_gate.py`
2. Add to appropriate list (EN/KO/JA)
3. Test with existing content

**Example**:
```python
# In scripts/quality_gate.py, line ~50-100

AI_PHRASES_EN = [
    "revolutionary",
    "game-changer",
    # Add here:
    "synergy",
    "leverage",
    "utilize" (prefer "use"),
]
```

---

## Rationale

**Why ban these phrases?**
- ✅ Sound robotic/AI-generated
- ✅ Overused in generic content
- ✅ Add no real value
- ✅ Hurt authenticity scores

**Goal**: Human-like, natural writing that provides genuine insights.

---

**Version**: 1.2
**Last Updated**: 2026-01-24
**Maintained By**: Jake's Tech Insights project
