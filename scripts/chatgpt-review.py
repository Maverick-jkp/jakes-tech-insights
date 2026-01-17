#!/usr/bin/env python3
"""
ChatGPT Code Review Script
Automatically reviews code changes using ChatGPT as Engineer and Designer
"""

import os
import sys
import subprocess
import json
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed")
    print("Install with: pip install openai")
    sys.exit(1)


def get_git_diff():
    """Get staged changes from git"""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error getting git diff: {e}")
        return None


def get_changed_files():
    """Get list of changed files"""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except subprocess.CalledProcessError as e:
        print(f"Error getting changed files: {e}")
        return []


def read_file_content(filepath):
    """Read content of a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None


def review_as_engineer(client, diff, files_content):
    """Review code as Senior Software Engineer"""

    prompt = f"""You are a Senior Software Engineer and CTO reviewing code changes.

CHANGED FILES:
{chr(10).join(files_content.keys())}

GIT DIFF:
{diff}

Please provide a comprehensive code review covering:

1. **Code Quality**
   - Clean code principles
   - Best practices followed/violated
   - Potential bugs or issues
   - Error handling

2. **Architecture & Design**
   - Structural decisions
   - Scalability considerations
   - Maintainability concerns
   - Technical debt

3. **Performance**
   - Potential bottlenecks
   - Optimization opportunities
   - Resource usage

4. **Security**
   - Security vulnerabilities
   - Data exposure risks
   - Input validation

5. **Testing**
   - Test coverage needed
   - Edge cases to consider

Format as:
- ✅ APPROVED / ⚠️ NEEDS CHANGES / 🚨 BLOCKING ISSUES
- List specific issues with file:line references
- Provide actionable recommendations

Be critical but constructive. Focus on facts, not opinions."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior software engineer conducting a thorough code review."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling ChatGPT API: {e}")
        return None


def review_as_designer(client, diff, files_content):
    """Review code as Senior Frontend Developer & UI/UX Designer"""

    prompt = f"""You are a Senior Frontend Developer and UI/UX Designer reviewing code changes.

CHANGED FILES:
{chr(10).join(files_content.keys())}

GIT DIFF:
{diff}

Please provide a comprehensive design review covering:

1. **Visual Design**
   - Layout and spacing consistency
   - Typography hierarchy
   - Color usage and contrast
   - Visual balance

2. **User Experience**
   - User flow improvements/issues
   - Interaction patterns
   - Accessibility (WCAG 2.1)
   - Mobile responsiveness

3. **Frontend Best Practices**
   - CSS organization
   - Semantic HTML
   - Performance (CSS/JS size)
   - Browser compatibility concerns

4. **Component Design**
   - Reusability
   - Consistency with design system
   - State management

5. **Responsive Design**
   - Mobile-first approach
   - Breakpoint logic
   - Touch targets (minimum 44px)

Format as:
- ✅ APPROVED / ⚠️ NEEDS CHANGES / 🚨 BLOCKING ISSUES
- List specific issues with file:line references
- Provide actionable recommendations

Be critical but constructive. Focus on user impact."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior frontend developer and UI/UX designer conducting a design review."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling ChatGPT API: {e}")
        return None


def save_review(engineer_review, designer_review):
    """Save reviews to markdown file"""
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"reviews/CHATGPT_REVIEW_{timestamp}.md"

    os.makedirs("reviews", exist_ok=True)

    content = f"""# ChatGPT Code Review - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 👨‍💻 Senior Software Engineer Review

{engineer_review}

---

## 🎨 Senior Frontend Developer & Designer Review

{designer_review}

---

**Generated by ChatGPT-4**
**Review Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✅ Review saved to: {filename}")
    return filename


def main():
    """Main function"""

    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)

    print("🔍 ChatGPT Code Review Tool")
    print("=" * 50)

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Get git changes
    print("\n📋 Getting staged changes...")
    diff = get_git_diff()
    if not diff:
        print("No staged changes found. Stage your changes with: git add")
        sys.exit(1)

    changed_files = get_changed_files()
    print(f"Found {len(changed_files)} changed file(s)")

    # Read file contents
    files_content = {}
    for filepath in changed_files:
        if os.path.exists(filepath):
            content = read_file_content(filepath)
            if content:
                files_content[filepath] = content

    # Run Engineer Review
    print("\n👨‍💻 Running Senior Software Engineer review...")
    engineer_review = review_as_engineer(client, diff, files_content)
    if engineer_review:
        print("✅ Engineer review completed")
    else:
        print("❌ Engineer review failed")
        sys.exit(1)

    # Run Designer Review
    print("\n🎨 Running Senior Frontend Developer & Designer review...")
    designer_review = review_as_designer(client, diff, files_content)
    if designer_review:
        print("✅ Designer review completed")
    else:
        print("❌ Designer review failed")
        sys.exit(1)

    # Save reviews
    review_file = save_review(engineer_review, designer_review)

    # Print summaries
    print("\n" + "=" * 50)
    print("📊 REVIEW SUMMARY")
    print("=" * 50)
    print("\n👨‍💻 ENGINEER REVIEW:\n")
    print(engineer_review[:500] + "..." if len(engineer_review) > 500 else engineer_review)
    print("\n" + "-" * 50)
    print("\n🎨 DESIGNER REVIEW:\n")
    print(designer_review[:500] + "..." if len(designer_review) > 500 else designer_review)

    print(f"\n\n📄 Full review saved to: {review_file}")
    print("\n✅ ChatGPT code review completed!")


if __name__ == "__main__":
    main()
