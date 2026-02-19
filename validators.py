#!/usr/bin/env python3
"""
Input validation utilities for Property Deal Analyzer.
"""

import re
from urllib.parse import urlparse
from typing import Optional


def validate_url(url: str, allowed_domains: Optional[list] = None) -> tuple[bool, str]:
    """
    Validate a URL for security.
    
    Returns:
        (is_valid, error_message)
    """
    if not url or not isinstance(url, str):
        return False, "URL cannot be empty"
    
    try:
        parsed = urlparse(url)
    except Exception:
        return False, "Invalid URL format"
    
    # Check scheme
    if parsed.scheme not in ('http', 'https'):
        return False, f"Invalid URL scheme: {parsed.scheme}. Must be http or https"
    
    # Check netloc
    if not parsed.netloc:
        return False, "Invalid URL: missing domain"
    
    # Check allowed domains if specified
    if allowed_domains:
        allowed = any(parsed.netloc.endswith(domain) for domain in allowed_domains)
        if not allowed:
            return False, f"Domain not allowed: {parsed.netloc}"
    
    # Check for suspicious patterns
    dangerous_patterns = [
        r'\.\./',  # Path traversal
        r'\.\.\\\\',  # Windows path traversal
        r'\$\{',   # Command substitution
        r'`.*`',   # Backtick execution
        r'\|',     # Pipe
        r';',      # Command separator
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, url):
            return False, "URL contains potentially dangerous characters"
    
    return True, ""


def validate_price(price: float) -> tuple[bool, str]:
    """Validate property price."""
    if price is None:
        return False, "Price is required"
    
    try:
        price = float(price)
    except (ValueError, TypeError):
        return False, "Price must be a number"
    
    if price <= 0:
        return False, "Price must be greater than 0"
    
    if price > 100_000_000:  # $100M sanity check
        return False, "Price seems unrealistic (over $100M)"
    
    return True, ""


def validate_size(size: float) -> tuple[bool, str]:
    """Validate property size."""
    if size is None:
        return False, "Size is required"
    
    try:
        size = float(size)
    except (ValueError, TypeError):
        return False, "Size must be a number"
    
    if size <= 0:
        return False, "Size must be greater than 0"
    
    if size > 50_000:  # 50k sqft sanity check
        return False, "Size seems unrealistic (over 50,000 sqft)"
    
    return True, ""


def validate_district(district: int) -> tuple[bool, str]:
    """Validate Singapore district number."""
    if district is None:
        return False, "District is required"
    
    try:
        district = int(district)
    except (ValueError, TypeError):
        return False, "District must be a number"
    
    if not (1 <= district <= 28):
        return False, "District must be between 1 and 28"
    
    return True, ""


def sanitize_input(value: str) -> str:
    """Sanitize user input to prevent injection attacks."""
    if not isinstance(value, str):
        return str(value)
    
    # Remove null bytes
    value = value.replace('\x00', '')
    
    # Remove control characters except newlines and tabs
    value = ''.join(char for char in value if ord(char) >= 32 or char in '\n\t\r')
    
    # Strip whitespace
    value = value.strip()
    
    return value
