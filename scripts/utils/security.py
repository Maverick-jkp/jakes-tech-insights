"""
Security utilities for masking sensitive data in logs.
"""
import os
import re
from typing import List

def get_sensitive_patterns() -> List[str]:
    """Get list of sensitive environment variables to mask."""
    return [
        os.getenv("ANTHROPIC_API_KEY", ""),
        os.getenv("UNSPLASH_ACCESS_KEY", ""),
        os.getenv("GOOGLE_API_KEY", ""),
        os.getenv("GOOGLE_CX", ""),
    ]

def mask_secrets(text: str) -> str:
    """
    Mask sensitive information in text before logging.

    Args:
        text: Text that may contain sensitive data

    Returns:
        Text with sensitive data replaced by ***MASKED***
    """
    masked = text

    # Mask environment variables
    for secret in get_sensitive_patterns():
        if secret and len(secret) > 0:
            masked = masked.replace(secret, "***MASKED***")

    # Mask API key patterns (sk-ant-..., or other common formats)
    masked = re.sub(r'sk-ant-[a-zA-Z0-9-_]{20,}', '***MASKED_API_KEY***', masked)

    # Mask bearer tokens
    masked = re.sub(r'Bearer [a-zA-Z0-9-_]{20,}', 'Bearer ***MASKED***', masked)

    return masked

def safe_print(message: str):
    """Print message with secrets masked."""
    print(mask_secrets(message))
