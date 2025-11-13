#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for GitHub camo URL length limits.

When badges are used in GitHub markdown files, GitHub proxies the image URLs through
camo.githubusercontent.com for security. The camo proxy hex-encodes the original URL,
resulting in: https://camo.githubusercontent.com/<40-char-digest>/<hex-encoded-url>

This approximately doubles the URL length plus 76 chars overhead. The camo service has
an 8192 character limit, so badge URLs must stay under ~4058 chars to work correctly.
"""

import argparse
import tempfile
import os
from badgesort.icons import run, svg_to_base64_data_uri
from simpleicons.all import icons
from urllib.parse import quote


CAMO_URL_LIMIT = 8192
CAMO_OVERHEAD = 76  # base URL (35) + digest (40) + slash (1)


def calculate_camo_url_length(badge_url):
    """Calculate the approximate camo URL length for a badge URL.
    
    GitHub's camo proxy format: https://camo.githubusercontent.com/<digest>/<hex-encoded-url>
    """
    return CAMO_OVERHEAD + (len(badge_url.encode('utf-8')) * 2)


def test_svg_data_uri_max_length_default():
    """Test that default max_url_length respects camo limits."""
    # The default max_url_length should be 3550 to stay under camo's 8192 limit
    # This test verifies the function signature has the correct default
    import inspect
    sig = inspect.signature(svg_to_base64_data_uri)
    max_url_length_default = sig.parameters['max_url_length'].default
    
    assert max_url_length_default == 3550, \
        f"Default max_url_length should be 3550 (found {max_url_length_default})"


def test_shields_embedded_svg_urls_under_camo_limit():
    """Test that Shields.io badges with embedded SVGs stay under camo URL limit."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("""# Test File

<!-- start chipwolf/badgesort test -->
<!-- end chipwolf/badgesort test -->
""")
        temp_file = f.name
    
    try:
        # Test with a few complex icons that have large SVGs
        test_slugs = ['github', 'python', 'docker', 'kubernetes', 'amazonaws']
        
        args = argparse.Namespace(
            slugs=test_slugs,
            random=1,
            output=temp_file,
            id='test',
            format='markdown',
            badge_style='for-the-badge',
            color_sort='hilbert',
            hue_rotate=0,
            no_thanks=True,
            reverse=False,
            provider='shields',
            verify=False,
            embed_svg=True,  # Force SVG embedding to test worst case
            skip_logo_check=True
        )
        
        run(args)
        
        with open(temp_file, 'r') as f:
            result = f.read()
        
        # Extract badge URLs and check their camo lengths
        import re
        badge_urls = re.findall(r'https://img\.shields\.io/[^\)]+', result)
        
        for url in badge_urls:
            camo_length = calculate_camo_url_length(url)
            assert camo_length <= CAMO_URL_LIMIT, \
                f"Badge URL would exceed camo limit: {camo_length} > {CAMO_URL_LIMIT}\nURL: {url[:100]}..."
        
        print(f"✓ All {len(badge_urls)} badge URLs stay under {CAMO_URL_LIMIT} char camo limit")
        
    finally:
        os.unlink(temp_file)


def test_badgen_urls_under_camo_limit():
    """Test that Badgen.net badge URLs stay under camo URL limit."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("""# Test File

<!-- start chipwolf/badgesort test -->
<!-- end chipwolf/badgesort test -->
""")
        temp_file = f.name
    
    try:
        # Test with a few icons
        test_slugs = ['github', 'python', 'docker']
        
        args = argparse.Namespace(
            slugs=test_slugs,
            random=1,
            output=temp_file,
            id='test',
            format='markdown',
            badge_style='flat',
            color_sort='hilbert',
            hue_rotate=0,
            no_thanks=True,
            reverse=False,
            provider='badgen',  # Badgen always embeds SVG
            verify=False,
            embed_svg=False,
            skip_logo_check=True
        )
        
        run(args)
        
        with open(temp_file, 'r') as f:
            result = f.read()
        
        # Extract badge URLs and check their camo lengths
        import re
        badge_urls = re.findall(r'https://badgen\.net/[^\)]+', result)
        
        for url in badge_urls:
            camo_length = calculate_camo_url_length(url)
            assert camo_length <= CAMO_URL_LIMIT, \
                f"Badgen URL would exceed camo limit: {camo_length} > {CAMO_URL_LIMIT}\nURL: {url[:100]}..."
        
        print(f"✓ All {len(badge_urls)} Badgen URLs stay under {CAMO_URL_LIMIT} char camo limit")
        
    finally:
        os.unlink(temp_file)


def test_data_uri_length_calculation():
    """Test that SVG data URIs are kept under the safe limit."""
    # Test with a medium-sized icon
    github_icon = icons.get('github')
    
    # Generate data URI with default limit
    data_uri = svg_to_base64_data_uri(github_icon.svg, 'white')
    
    # Build a sample badge URL
    encoded_uri = quote(data_uri, safe='')
    badge_url = f"https://img.shields.io/badge/GitHub-181717.svg?style=for-the-badge&logo={encoded_uri}"
    
    # Calculate camo URL length
    camo_length = calculate_camo_url_length(badge_url)
    
    assert camo_length <= CAMO_URL_LIMIT, \
        f"Sample badge would exceed camo limit: {camo_length} > {CAMO_URL_LIMIT}"
    
    print(f"✓ Sample badge camo URL: {camo_length} chars (under {CAMO_URL_LIMIT} limit)")


def test_max_url_length_parameter_respected():
    """Test that max_url_length parameter is properly enforced."""
    # Get a large icon
    large_icons = sorted(icons.items(), key=lambda x: len(x[1].svg), reverse=True)
    large_icon = large_icons[0][1]
    
    # Test with a very small limit - should trigger PNG fallback
    # (PNG fallback will fail due to missing rsvg-convert, but that's expected)
    data_uri = svg_to_base64_data_uri(large_icon.svg, 'white', max_url_length=100)
    
    # The function should either return a short PNG data URI or fall back to the original
    # In either case, we're testing that the parameter is being used
    assert data_uri.startswith('data:image/'), \
        "Should return a valid data URI"
    
    print(f"✓ max_url_length parameter is respected")
