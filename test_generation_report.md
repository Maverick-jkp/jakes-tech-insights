# 16-Post Generation Test Report
**Date**: 2026-01-24 12:08 KST  
**Test Purpose**: Validate quality gate effectiveness after enhancements

---

## Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| **Total Generated** | 16 | 100% |
| **Passed Quality Gate** | 7 | 43.75% |
| **Failed & Deleted** | 9 | 56.25% |

---

## Passed Posts (7)

### English (4 posts)
1. ✅ **dow-jones-futures** (Business)
   - 1304 words, 5 headings, 2 links
   - ⚠️ Word count high, AI phrase "leverage"
   
2. ✅ **snooki** (Entertainment)
   - 1034 words, 5 headings, 2 links
   - No critical issues

3. ✅ **todd-burkhalter** (Finance)
   - 1252 words, 6 headings, 2 links
   - ⚠️ Word count high, AI phrase "leverage"
   
4. ✅ **todays-weather** (Society)
   - 1052 words, 6 headings, 1 link
   - ⚠️ Low link count

### Korean (2 posts)
5. ✅ **그록** (Tech)
   - 2300 chars, 6 headings, 4 links
   - ⚠️ AI phrase "물론"

6. ✅ **u23** (Society)
   - 2764 chars, 7 headings, 2 links
   - No critical issues

### Japanese (1 post)
7. ✅ **宝くじ-当選番号-ロト6** (Finance)
   - 2756 chars, 7 headings, 5 links
   - ⚠️ Character count slightly low

---

## Failed Posts (9) - Returned to Queue

### Title-Content Mismatch (5 posts)
Title keywords not found in content body (< 30% threshold)

1. ❌ **地震速報** (JA) - 0% keyword match
2. ❌ **衆議院-選挙区** (JA) - 0% keyword match (appeared twice)
3. ❌ **村田充** (JA) - 0% keyword match
4. ❌ **티빙** (KO) - 20% keyword match
5. ❌ **氷のホテル** (JA) - 0% keyword match

### Duplicate Keywords (4 posts)
Same topic generated within 7 days

1. ❌ **hyundai-recalls** (EN) - Duplicate detected
2. ❌ **썬더스-대-대구-한국가스공사** (KO) - Duplicate of 2026-01-23 post

---

## Quality Gate Performance

### Enhanced Checks Working ✅
1. **Duplicate Detection**: Caught 2 exact duplicates (hyundai-recalls appeared twice in same batch)
2. **Title-Content Consistency**: Blocked 5 posts with keyword mismatch
3. **Levenshtein Similarity**: Ready for near-duplicate detection

### Common Issues Detected
- **Title-content mismatch**: 5/16 posts (31%) - Draft agent not following keyword
- **Duplicate topics**: 4/16 posts (25%) - Queue management issue
- **AI phrases**: 3/7 passed posts contain "물론", "leverage", "重要です"
- **Placeholder images**: 7/16 posts used placeholders (UNSPLASH_ACCESS_KEY issue)
- **Missing references**: 1/16 posts had no references

---

## System Health

### Topic Queue Status
- Started with: 56 available topics
- Reserved: 16 topics
- Completed: 7 topics  
- Returned to queue: 9 topics
- **Current available**: 49 topics

### Validation Fixes Applied
✅ Fixed `VALID_STATUSES` - Added 'available' status  
✅ Fixed `reserve_topics()` - Now accepts both 'pending' and 'available'

### API Usage (16 posts)
- Draft generation: ~28k input, ~20k output tokens
- Editing: ~30k input, ~26k output tokens
- **Total estimated cost**: ~$2-3 USD

---

## Recommendations

### High Priority
1. **Fix Title-Content Mismatch** (31% failure rate)
   - Draft Agent not respecting keyword requirements
   - Need to strengthen prompt: "MUST mention keyword '{keyword}' in body text"

2. **Improve Duplicate Prevention**
   - 2 topics generated twice in same batch (hyundai-recalls)
   - Add pre-generation check before reserving topics

### Medium Priority
3. **AI Phrase Detection**
   - "물론", "leverage", "重要です" appearing in content
   - Add to blacklist in quality_gate.py

4. **Unsplash API Issues**
   - 7/16 posts using placeholder images
   - Verify UNSPLASH_ACCESS_KEY in GitHub Actions

### Low Priority
5. **Word Count Optimization**
   - 2 English posts exceed 1200 words
   - Editor Agent should compress more aggressively

---

## Conclusion

**Quality Gate is Working Effectively** ✅

- Partial success pattern working: 7 good posts deployed, 9 poor posts blocked
- No more "all-or-nothing" deployment risk
- Failed topics safely returned to queue for retry
- Enhanced duplicate detection catching issues

**Next Steps**:
1. Monitor Cloudflare Pages deployment
2. Fix title-content mismatch issue in Draft Agent
3. Review duplicate detection logic for same-batch duplicates
4. Wait for user feedback on content quality

**Live Site**: https://jakes-tech-insights.pages.dev

---

*Generated automatically by test run at 2026-01-24 12:08 KST*
