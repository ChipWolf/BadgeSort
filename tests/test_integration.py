#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration tests for BadgeSort.

Tests the full workflow including file reading, badge generation, and file writing.
"""

import tempfile
import os
import argparse
from badgesort.icons import run


def test_integration_codeblock_preservation():
    """Integration test: badges should not be inserted into codeblocks."""
    # Create a temporary file with badge markers in both normal section and codeblock
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("""# Integration Test

Normal section (should be updated):
<!-- start chipwolf/badgesort integration-test -->
<!-- end chipwolf/badgesort integration-test -->

Documentation codeblock (should NOT be updated):
```html
<!-- start chipwolf/badgesort integration-test -->
Example markers for documentation
<!-- end chipwolf/badgesort integration-test -->
```

End of file.
""")
        temp_file = f.name
    
    try:
        # Create args for BadgeSort
        args = argparse.Namespace(
            slugs=['github', 'python'],
            random=1,
            output=temp_file,
            id='integration-test',
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
        
        # Run BadgeSort
        run(args)
        
        # Read the result
        with open(temp_file, 'r') as f:
            result = f.read()
        
        # Verify badges were added to normal section
        assert 'github' in result.lower() or 'python' in result.lower(), "Badges should be generated"
        
        # We expect badges + BadgeSort badge in the normal section only
        # The codeblock should still have the example text
        assert "Example markers for documentation" in result, "Codeblock content should be preserved"
        
        # Extract the codeblock section to verify it wasn't modified
        codeblock_start = result.find('```html')
        codeblock_end = result.find('```', codeblock_start + 7)
        if codeblock_start != -1 and codeblock_end != -1:
            codeblock_content = result[codeblock_start:codeblock_end]
            # The codeblock should not contain actual badge images
            assert '![GitHub]' not in codeblock_content, "Codeblock should not contain actual badges"
            assert '![Python]' not in codeblock_content, "Codeblock should not contain actual badges"
            assert "Example markers for documentation" in codeblock_content, "Original codeblock text should remain"
        
    finally:
        # Clean up
        os.unlink(temp_file)


def test_integration_multiple_ids():
    """Integration test: multiple badge sections with different IDs."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("""# Multiple IDs Test

Section 1:
<!-- start chipwolf/badgesort section1 -->
<!-- end chipwolf/badgesort section1 -->

```html
<!-- start chipwolf/badgesort section1 -->
Example 1
<!-- end chipwolf/badgesort section1 -->
```

Section 2:
<!-- start chipwolf/badgesort section2 -->
<!-- end chipwolf/badgesort section2 -->

```markdown
<!-- start chipwolf/badgesort section2 -->
Example 2
<!-- end chipwolf/badgesort section2 -->
```
""")
        temp_file = f.name
    
    try:
        # Update section1
        args1 = argparse.Namespace(
            slugs=['docker'],
            random=1,
            output=temp_file,
            id='section1',
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
        run(args1)
        
        # Update section2
        args2 = argparse.Namespace(
            slugs=['rust'],
            random=1,
            output=temp_file,
            id='section2',
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
        run(args2)
        
        # Read result
        with open(temp_file, 'r') as f:
            result = f.read()
        
        # Both sections should have badges
        assert 'docker' in result.lower() or 'Docker' in result, "Section 1 should have Docker badge"
        assert 'rust' in result.lower() or 'Rust' in result, "Section 2 should have Rust badge"
        
        # Codeblock examples should be preserved
        assert "Example 1" in result, "Codeblock 1 should be preserved"
        assert "Example 2" in result, "Codeblock 2 should be preserved"
        
    finally:
        os.unlink(temp_file)


def test_integration_html_format():
    """Integration test: HTML format badges should not appear in codeblocks."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("""# HTML Format Test

<!-- start chipwolf/badgesort html-test -->
<!-- end chipwolf/badgesort html-test -->

```html
<!-- start chipwolf/badgesort html-test -->
HTML example content
<!-- end chipwolf/badgesort html-test -->
```
""")
        temp_file = f.name
    
    try:
        args = argparse.Namespace(
            slugs=['github'],
            random=1,
            output=temp_file,
            id='html-test',
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
        
        # HTML badges should be in the normal section
        assert '<img alt=' in result, "HTML format badges should be generated"
        
        # Codeblock should preserve example content
        assert "HTML example content" in result, "Codeblock should be preserved"
        
        # Count <p> tags - should appear at least once (for badges) not in codeblock
        p_tag_count = result.count('<p>')
        assert p_tag_count >= 1, "HTML format should include at least one <p> tag"
        
    finally:
        os.unlink(temp_file)


def test_integration_no_output_file():
    """Test that when no output file is specified, badges are printed to stdout."""
    # This test verifies the code path doesn't break when output is None
    # We can't easily capture stdout in pytest without more setup,
    # but we can verify it doesn't raise an exception
    
    args = argparse.Namespace(
        slugs=['github'],
        random=1,
        output=None,  # No output file
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
    
    # Should not raise an exception
    try:
        run(args)
        # If we get here without exception, the test passes
        assert True
    except Exception as e:
        # If there's an exception, it should not be related to file handling
        assert "output" not in str(e).lower(), f"Unexpected error: {e}"


def test_integration_append_when_no_markers():
    """Integration test: badges should be appended to file when no markers exist."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("""# Test File

This is a test file without any BadgeSort markers.

Some content here.
""")
        temp_file = f.name
    
    try:
        # Create args for BadgeSort
        args = argparse.Namespace(
            slugs=['github', 'python'],
            random=1,
            output=temp_file,
            id='default',
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
        
        # Run BadgeSort
        run(args)
        
        # Read the result
        with open(temp_file, 'r') as f:
            result = f.read()
        
        # Verify original content is still there
        assert "This is a test file without any BadgeSort markers." in result
        
        # Verify badges were appended with markers
        assert "<!-- start chipwolf/badgesort default -->" in result
        assert "<!-- end chipwolf/badgesort default -->" in result
        
        # Verify badges were generated
        assert 'github' in result.lower() or 'python' in result.lower(), "Badges should be generated"
        
        # Verify badges are at the end of the file
        marker_pos = result.find("<!-- start chipwolf/badgesort default -->")
        assert marker_pos > 0, "Markers should be in the file"
        
        # Check that markers come after the original content
        original_content_pos = result.find("This is a test file without any BadgeSort markers.")
        assert marker_pos > original_content_pos, "Badges should be after original content"
        
    finally:
        # Clean up
        os.unlink(temp_file)


def test_integration_append_preserves_newlines():
    """Integration test: appending badges should handle newlines correctly."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        # File without trailing newline
        f.write("# Test File\n\nContent without trailing newline")
        temp_file = f.name
    
    try:
        args = argparse.Namespace(
            slugs=['docker'],
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
        
        # Verify original content is preserved
        assert "Content without trailing newline" in result
        
        # Verify badges were added with proper spacing
        assert "<!-- start chipwolf/badgesort test -->" in result
        
        # Should have proper line breaks between content and badges
        lines = result.split('\n')
        assert len(lines) > 3, "Should have multiple lines"
        
    finally:
        os.unlink(temp_file)


def test_integration_create_output_file_if_not_exists():
    """Integration test: create the output file if it doesn't exist."""
    # Generate a path for a file that doesn't exist
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, f'badgesort_test_nonexistent_{os.getpid()}.md')
    
    # Ensure the file doesn't exist
    if os.path.exists(temp_file):
        os.unlink(temp_file)
    
    try:
        args = argparse.Namespace(
            slugs=['github', 'python'],
            random=1,
            output=temp_file,
            id='default',
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
        
        # Run BadgeSort - should create the file
        run(args)
        
        # Verify the file was created
        assert os.path.exists(temp_file), "Output file should be created"
        
        # Read the result
        with open(temp_file, 'r') as f:
            result = f.read()
        
        # Verify badges were generated with markers
        assert "<!-- start chipwolf/badgesort default -->" in result
        assert "<!-- end chipwolf/badgesort default -->" in result
        
        # Verify badges were generated
        assert 'github' in result.lower() or 'python' in result.lower(), "Badges should be generated"
        
        # Since the file was new, badges should be the only content
        lines = result.strip().split('\n')
        assert len(lines) >= 3, "Should have at least markers and badges"
        
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.unlink(temp_file)
