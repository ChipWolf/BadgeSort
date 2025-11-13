#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for codeblock handling in BadgeSort.

This module tests that BadgeSort correctly handles markdown codeblocks
and does not modify comment markers inside them.
"""

import tempfile
import os
from badgesort.icons import _replace_badges_outside_codeblocks


def test_simple_codeblock_preservation():
    """Test that badges are not inserted into simple codeblocks."""
    content = """# Test File

Normal section:
<!-- start chipwolf/badgesort test -->
<!-- end chipwolf/badgesort test -->

Codeblock section:
```html
<!-- start chipwolf/badgesort test -->
Example content
<!-- end chipwolf/badgesort test -->
```
"""
    
    badges_header = "<!-- start chipwolf/badgesort test -->\n"
    badges_footer = "<!-- end chipwolf/badgesort test -->\n"
    badges = badges_header + "![Badge](http://example.com/badge.svg)\n" + badges_footer
    
    result = _replace_badges_outside_codeblocks(content, badges_header, badges_footer, badges)
    
    # The normal section should be updated
    assert "![Badge](http://example.com/badge.svg)" in result
    
    # Count occurrences - should appear only once (outside codeblock)
    badge_count = result.count("![Badge](http://example.com/badge.svg)")
    assert badge_count == 1, f"Expected 1 badge, found {badge_count}"
    
    # The codeblock should still contain "Example content"
    assert "Example content" in result


def test_multiple_codeblocks():
    """Test handling of multiple codeblocks with different markers."""
    content = """# Multiple Sections

First section:
<!-- start chipwolf/badgesort id1 -->
<!-- end chipwolf/badgesort id1 -->

First codeblock:
```html
<!-- start chipwolf/badgesort id1 -->
Should not change 1
<!-- end chipwolf/badgesort id1 -->
```

Second section:
<!-- start chipwolf/badgesort id2 -->
<!-- end chipwolf/badgesort id2 -->

Second codeblock:
```markdown
<!-- start chipwolf/badgesort id2 -->
Should not change 2
<!-- end chipwolf/badgesort id2 -->
```
"""
    
    # Replace id1
    badges_header_1 = "<!-- start chipwolf/badgesort id1 -->\n"
    badges_footer_1 = "<!-- end chipwolf/badgesort id1 -->\n"
    badges_1 = badges_header_1 + "![Badge1](http://example.com/badge1.svg)\n" + badges_footer_1
    
    result = _replace_badges_outside_codeblocks(content, badges_header_1, badges_footer_1, badges_1)
    
    # Replace id2
    badges_header_2 = "<!-- start chipwolf/badgesort id2 -->\n"
    badges_footer_2 = "<!-- end chipwolf/badgesort id2 -->\n"
    badges_2 = badges_header_2 + "![Badge2](http://example.com/badge2.svg)\n" + badges_footer_2
    
    result = _replace_badges_outside_codeblocks(result, badges_header_2, badges_footer_2, badges_2)
    
    # Both badges should appear once each
    assert result.count("![Badge1](http://example.com/badge1.svg)") == 1
    assert result.count("![Badge2](http://example.com/badge2.svg)") == 1
    
    # Original codeblock content should be preserved
    assert "Should not change 1" in result
    assert "Should not change 2" in result


def test_nested_codeblock_like_content():
    """Test that triple backticks toggle codeblock state correctly.
    
    Note: In real markdown, you cannot nest codeblocks. Triple backticks 
    toggle the codeblock state, so this test verifies that behavior.
    """
    content = """# Nested Content

<!-- start chipwolf/badgesort test -->
<!-- end chipwolf/badgesort test -->

Example showing codeblock syntax:
```markdown
You can use codeblocks like this (first codeblock)
```

Outside codeblocks now, showing another example:
```html
<!-- start chipwolf/badgesort test -->
Inside second codeblock
<!-- end chipwolf/badgesort test -->
```
End of example
"""
    
    badges_header = "<!-- start chipwolf/badgesort test -->\n"
    badges_footer = "<!-- end chipwolf/badgesort test -->\n"
    badges = badges_header + "![Badge](http://example.com/badge.svg)\n" + badges_footer
    
    result = _replace_badges_outside_codeblocks(content, badges_header, badges_footer, badges)
    
    # Only the first occurrence (at the top, outside any codeblock) should be replaced
    badge_count = result.count("![Badge](http://example.com/badge.svg)")
    assert badge_count == 1, f"Expected 1 badge, found {badge_count}"
    
    # The codeblock content should be preserved
    assert "Inside second codeblock" in result


def test_no_codeblocks():
    """Test that replacement works normally when there are no codeblocks."""
    content = """# No Codeblocks

<!-- start chipwolf/badgesort test -->
<!-- end chipwolf/badgesort test -->

More content

<!-- start chipwolf/badgesort test -->
<!-- end chipwolf/badgesort test -->
"""
    
    badges_header = "<!-- start chipwolf/badgesort test -->\n"
    badges_footer = "<!-- end chipwolf/badgesort test -->\n"
    badges = badges_header + "![Badge](http://example.com/badge.svg)\n" + badges_footer
    
    result = _replace_badges_outside_codeblocks(content, badges_header, badges_footer, badges)
    
    # Both occurrences should be replaced
    badge_count = result.count("![Badge](http://example.com/badge.svg)")
    assert badge_count == 2, f"Expected 2 badges, found {badge_count}"


def test_codeblock_with_language_specifier():
    """Test codeblocks with various language specifiers."""
    content = """# Language Specifiers

<!-- start chipwolf/badgesort test -->
<!-- end chipwolf/badgesort test -->

```python
<!-- start chipwolf/badgesort test -->
Python example
<!-- end chipwolf/badgesort test -->
```

```yaml
<!-- start chipwolf/badgesort test -->
YAML example
<!-- end chipwolf/badgesort test -->
```

```
<!-- start chipwolf/badgesort test -->
No language
<!-- end chipwolf/badgesort test -->
```
"""
    
    badges_header = "<!-- start chipwolf/badgesort test -->\n"
    badges_footer = "<!-- end chipwolf/badgesort test -->\n"
    badges = badges_header + "![Badge](http://example.com/badge.svg)\n" + badges_footer
    
    result = _replace_badges_outside_codeblocks(content, badges_header, badges_footer, badges)
    
    # Only the first occurrence should be replaced
    badge_count = result.count("![Badge](http://example.com/badge.svg)")
    assert badge_count == 1, f"Expected 1 badge, found {badge_count}"
    
    # All codeblock content should be preserved
    assert "Python example" in result
    assert "YAML example" in result
    assert "No language" in result


def test_empty_badge_section():
    """Test replacement of empty badge sections."""
    content = """# Empty Section

<!-- start chipwolf/badgesort test -->
<!-- end chipwolf/badgesort test -->
"""
    
    badges_header = "<!-- start chipwolf/badgesort test -->\n"
    badges_footer = "<!-- end chipwolf/badgesort test -->\n"
    badges = badges_header + "![Badge1](http://example.com/badge1.svg)\n![Badge2](http://example.com/badge2.svg)\n" + badges_footer
    
    result = _replace_badges_outside_codeblocks(content, badges_header, badges_footer, badges)
    
    # Should contain both badges
    assert "![Badge1](http://example.com/badge1.svg)" in result
    assert "![Badge2](http://example.com/badge2.svg)" in result


def test_existing_badges_replacement():
    """Test that existing badges are properly replaced."""
    content = """# Existing Badges

<!-- start chipwolf/badgesort test -->
![OldBadge1](http://example.com/old1.svg)
![OldBadge2](http://example.com/old2.svg)
<!-- end chipwolf/badgesort test -->
"""
    
    badges_header = "<!-- start chipwolf/badgesort test -->\n"
    badges_footer = "<!-- end chipwolf/badgesort test -->\n"
    badges = badges_header + "![NewBadge](http://example.com/new.svg)\n" + badges_footer
    
    result = _replace_badges_outside_codeblocks(content, badges_header, badges_footer, badges)
    
    # Old badges should be gone
    assert "OldBadge1" not in result
    assert "OldBadge2" not in result
    
    # New badge should be present
    assert "![NewBadge](http://example.com/new.svg)" in result


def test_markers_at_start_of_codeblock():
    """Test when markers appear right after codeblock opening."""
    content = """# Start of Codeblock

<!-- start chipwolf/badgesort test -->
<!-- end chipwolf/badgesort test -->

```html
<!-- start chipwolf/badgesort test -->
Content
<!-- end chipwolf/badgesort test -->
```
"""
    
    badges_header = "<!-- start chipwolf/badgesort test -->\n"
    badges_footer = "<!-- end chipwolf/badgesort test -->\n"
    badges = badges_header + "![Badge](http://example.com/badge.svg)\n" + badges_footer
    
    result = _replace_badges_outside_codeblocks(content, badges_header, badges_footer, badges)
    
    # Badge should appear only outside codeblock
    assert result.count("![Badge](http://example.com/badge.svg)") == 1
    
    # Codeblock content should be preserved
    assert "Content" in result


def test_unclosed_codeblock():
    """Test handling of unclosed codeblock (edge case)."""
    content = """# Unclosed Codeblock

<!-- start chipwolf/badgesort test -->
<!-- end chipwolf/badgesort test -->

```html
<!-- start chipwolf/badgesort test -->
This codeblock is never closed
<!-- end chipwolf/badgesort test -->

More content here
"""
    
    badges_header = "<!-- start chipwolf/badgesort test -->\n"
    badges_footer = "<!-- end chipwolf/badgesort test -->\n"
    badges = badges_header + "![Badge](http://example.com/badge.svg)\n" + badges_footer
    
    result = _replace_badges_outside_codeblocks(content, badges_header, badges_footer, badges)
    
    # Only the first occurrence (before unclosed codeblock) should be replaced
    badge_count = result.count("![Badge](http://example.com/badge.svg)")
    assert badge_count == 1, f"Expected 1 badge, found {badge_count}"
    
    # Content inside the unclosed codeblock should be preserved
    assert "This codeblock is never closed" in result


def test_html_format_badges():
    """Test with HTML format badges instead of markdown."""
    content = """# HTML Format

<!-- start chipwolf/badgesort test -->
<!-- end chipwolf/badgesort test -->

```html
<!-- start chipwolf/badgesort test -->
Example HTML badges
<!-- end chipwolf/badgesort test -->
```
"""
    
    badges_header = "<!-- start chipwolf/badgesort test -->\n"
    badges_footer = "<!-- end chipwolf/badgesort test -->\n"
    badges = badges_header + '<p>\n  <a href="#"><img alt="Badge" src="http://example.com/badge.svg"></a>\n</p>\n' + badges_footer
    
    result = _replace_badges_outside_codeblocks(content, badges_header, badges_footer, badges)
    
    # HTML badge should appear once
    assert result.count('<img alt="Badge" src="http://example.com/badge.svg">') == 1
    
    # Codeblock example content preserved
    assert "Example HTML badges" in result
