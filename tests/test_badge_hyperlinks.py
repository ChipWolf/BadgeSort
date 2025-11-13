#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for badge hyperlink behavior.

Tests that badges without custom URLs are hyperlinked to # in both Markdown and HTML formats.
"""

import argparse
import tempfile
import os
from badgesort.icons import run


def test_markdown_badges_without_custom_url_hyperlinked():
    """Test that Markdown badges without custom URLs are hyperlinked to #."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("""# Test File

<!-- start chipwolf/badgesort test -->
<!-- end chipwolf/badgesort test -->
""")
        temp_file = f.name
    
    try:
        args = argparse.Namespace(
            slugs=['github', 'python'],
            random=1,
            output=temp_file,
            id='test',
            format='markdown',
            badge_style='flat',
            color_sort='hilbert',
            hue_rotate=0,
            no_thanks=True,  # Exclude BadgeSort badge for simpler test
            reverse=False,
            provider='shields',
            verify=False,
            embed_svg=False,
            skip_logo_check=True
        )
        
        run(args)
        
        with open(temp_file, 'r') as f:
            result = f.read()
        
        # Badges without custom URLs should be wrapped with [...]`(#)`
        # Pattern: [![Title](badge_url)](#)
        assert '[![GitHub]' in result or '[![Python]' in result, \
            "Markdown badges should start with [!["
        assert '(#)' in result, \
            "Markdown badges without custom URLs should have (#) at the end"
        
        # Should NOT have unwrapped badges (just ![Title](url) without link wrapper)
        # Count occurrences - if badges are properly wrapped, we should have:
        # - One ![GitHub](...) inside [![GitHub](...)](#)
        # - One ![Python](...) inside [![Python](...)](#)
        lines = result.split('\n')
        badge_lines = [line for line in lines if '![' in line and 'img.shields.io' in line]
        
        for line in badge_lines:
            # Each badge line should have the pattern: [![...](...)](#)
            if '![GitHub]' in line:
                assert line.strip().startswith('[![GitHub]'), \
                    f"GitHub badge should be wrapped with link: {line}"
                assert line.strip().endswith('(#)'), \
                    f"GitHub badge link should end with (#): {line}"
            if '![Python]' in line:
                assert line.strip().startswith('[![Python]'), \
                    f"Python badge should be wrapped with link: {line}"
                assert line.strip().endswith('(#)'), \
                    f"Python badge link should end with (#): {line}"
        
    finally:
        os.unlink(temp_file)


def test_markdown_badges_with_custom_url_not_double_wrapped():
    """Test that Markdown badges with custom URLs are not double-wrapped."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("""# Test File

<!-- start chipwolf/badgesort test -->
<!-- end chipwolf/badgesort test -->
""")
        temp_file = f.name
    
    try:
        # Badge with custom URL parameter
        args = argparse.Namespace(
            slugs=['github?url=https://github.com/ChipWolf'],
            random=1,
            output=temp_file,
            id='test',
            format='markdown',
            badge_style='flat',
            color_sort='hilbert',
            hue_rotate=0,
            no_thanks=True,
            reverse=False,
            provider='shields',
            verify=False,
            embed_svg=False,
            skip_logo_check=True
        )
        
        run(args)
        
        with open(temp_file, 'r') as f:
            result = f.read()
        
        # Badge with custom URL should be wrapped with custom URL, not (#)
        assert 'https://github.com/ChipWolf' in result, \
            "Badge should use custom URL"
        
        # Should NOT have (#) when custom URL is provided
        badge_lines = [line for line in result.split('\n') if '![GitHub]' in line]
        for line in badge_lines:
            assert '(#)' not in line, \
                f"Badge with custom URL should not have (#): {line}"
            assert 'https://github.com/ChipWolf' in line, \
                f"Badge should use custom URL: {line}"
        
    finally:
        os.unlink(temp_file)


def test_badgesort_badge_has_correct_link():
    """Test that the BadgeSort badge itself has the correct GitHub link."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("""# Test File

<!-- start chipwolf/badgesort test -->
<!-- end chipwolf/badgesort test -->
""")
        temp_file = f.name
    
    try:
        args = argparse.Namespace(
            slugs=['github'],
            random=1,
            output=temp_file,
            id='test',
            format='markdown',
            badge_style='flat',
            color_sort='hilbert',
            hue_rotate=0,
            no_thanks=True,  # Note: no_thanks=True means INCLUDE the badge (action='store_false')
            reverse=False,
            provider='shields',
            verify=False,
            embed_svg=False,
            skip_logo_check=True
        )
        
        run(args)
        
        with open(temp_file, 'r') as f:
            result = f.read()
        
        # BadgeSort badge should link to GitHub repo
        assert 'https://github.com/ChipWolf/BadgeSort' in result, \
            "BadgeSort badge should link to GitHub repository"
        
        # Regular badges (without custom URL) should link to #
        badge_lines = result.split('\n')
        github_badge_lines = [line for line in badge_lines if '![GitHub]' in line and 'BadgeSort' not in line]
        
        for line in github_badge_lines:
            assert '(#)' in line, \
                f"Regular GitHub badge should link to #: {line}"
        
    finally:
        os.unlink(temp_file)


def test_html_badges_without_custom_url_hyperlinked():
    """Test that HTML badges without custom URLs are hyperlinked to # (existing behavior)."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("""# Test File

<!-- start chipwolf/badgesort test -->
<!-- end chipwolf/badgesort test -->
""")
        temp_file = f.name
    
    try:
        args = argparse.Namespace(
            slugs=['github', 'python'],
            random=1,
            output=temp_file,
            id='test',
            format='html',
            badge_style='flat',
            color_sort='hilbert',
            hue_rotate=0,
            no_thanks=True,
            reverse=False,
            provider='shields',
            verify=False,
            embed_svg=False,
            skip_logo_check=True
        )
        
        run(args)
        
        with open(temp_file, 'r') as f:
            result = f.read()
        
        # HTML badges should be wrapped with <a href="#">
        assert '<a href="#">' in result, \
            "HTML badges without custom URLs should have <a href='#'>"
        
        # All badge images should be inside anchor tags
        badge_lines = [line for line in result.split('\n') if '<img alt=' in line]
        for line in badge_lines:
            assert '<a href="' in line, \
                f"HTML badge should be inside anchor tag: {line}"
        
    finally:
        os.unlink(temp_file)


def test_html_badges_with_custom_url():
    """Test that HTML badges with custom URLs use the custom URL."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("""# Test File

<!-- start chipwolf/badgesort test -->
<!-- end chipwolf/badgesort test -->
""")
        temp_file = f.name
    
    try:
        args = argparse.Namespace(
            slugs=['github?url=https://github.com/ChipWolf'],
            random=1,
            output=temp_file,
            id='test',
            format='html',
            badge_style='flat',
            color_sort='hilbert',
            hue_rotate=0,
            no_thanks=True,
            reverse=False,
            provider='shields',
            verify=False,
            embed_svg=False,
            skip_logo_check=True
        )
        
        run(args)
        
        with open(temp_file, 'r') as f:
            result = f.read()
        
        # HTML badge with custom URL should use that URL
        assert '<a href="https://github.com/ChipWolf">' in result, \
            "HTML badge should use custom URL"
        
    finally:
        os.unlink(temp_file)
