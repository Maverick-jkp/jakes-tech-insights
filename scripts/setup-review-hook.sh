#!/bin/bash
# Setup Git pre-commit hook for ChatGPT code review

echo "🔧 Setting up ChatGPT code review hook..."

# Create .git/hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# ChatGPT Code Review Pre-commit Hook

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  OPENAI_API_KEY not set. Skipping ChatGPT review.${NC}"
    echo "Set it with: export OPENAI_API_KEY='your-key-here'"
    exit 0
fi

# Check if there are staged changes
if ! git diff --cached --quiet; then
    echo -e "${GREEN}🤖 Running ChatGPT code review...${NC}"

    # Run the review script
    python3 scripts/chatgpt-review.py

    REVIEW_EXIT_CODE=$?

    if [ $REVIEW_EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✅ ChatGPT review completed${NC}"
        echo ""
        echo "Review saved in reviews/ directory"
        echo ""
        read -p "Do you want to proceed with the commit? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        else
            echo -e "${RED}Commit aborted by user${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ ChatGPT review failed${NC}"
        exit 1
    fi
fi

exit 0
EOF

# Make hook executable
chmod +x .git/hooks/pre-commit

echo "✅ Git pre-commit hook installed!"
echo ""
echo "Now, every time you commit, ChatGPT will review your code."
echo "To skip the review, use: git commit --no-verify"
echo ""
echo "Make sure to set OPENAI_API_KEY:"
echo "  export OPENAI_API_KEY='your-key-here'"
