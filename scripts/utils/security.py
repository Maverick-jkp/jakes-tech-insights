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

    # Mask API key patterns (sk-ant-..., sk-proj-..., or other common formats)
    # Order matters: specific patterns first, then generic
    masked = re.sub(r'sk-ant-[\w-]{10,}', '***MASKED_API_KEY***', masked)
    masked = re.sub(r'sk-proj-[\w-]{8,}', '***MASKED_API_KEY***', masked)  # Shorter threshold for sk-proj
    masked = re.sub(r'sk-[\w-]{20,}', '***MASKED_API_KEY***', masked)  # Catch any other sk-... pattern

    # Mask bearer tokens (including shorter ones like sk-proj-...)
    masked = re.sub(r'Bearer\s+[a-zA-Z0-9-_]{10,}', 'Bearer ***MASKED***', masked)

    # Mask access tokens in URLs
    masked = re.sub(r'access_token=[a-zA-Z0-9-_]{15,}', 'access_token=***MASKED***', masked)

    return masked

def safe_print(message: str):
    """Print message with secrets masked."""
    print(mask_secrets(message))
