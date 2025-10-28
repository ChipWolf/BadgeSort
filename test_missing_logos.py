#!/usr/bin/env python3
"""
Test script to demonstrate the missing logo detection and embedding functionality.

This script tests the new feature that automatically detects when icons are missing 
from Shields.io and embeds the SVG data URI instead.
"""

import subprocess
import sys

def run_badgesort(args):
    """Run BadgeSort with the given arguments and return the output."""
    cmd = [sys.executable, '-m', 'badgesort.icons'] + args
    result = subprocess.run(cmd, capture_output=True, text=True, cwd='/workspaces/BadgeSort')
    return result.stdout, result.stderr, result.returncode

def test_missing_logo_detection():
    """Test automatic detection and embedding of missing logos."""
    print("=" * 60)
    print("Testing automatic missing logo detection and embedding")
    print("=" * 60)
    
    # Test with Microsoft (missing logo) and GitHub (available logo)
    stdout, stderr, returncode = run_badgesort([
        '-s', 'microsoft', 'github',
        '-p', 'shields',
        '--no-thanks'
    ])
    
    print("Command: badgesort -s microsoft github -p shields --no-thanks")
    print("Return code:", returncode)
    print("\nOutput:")
    print(stdout)
    
    # Check that Microsoft uses data URI and GitHub uses slug
    if 'data%3Aimage%2Fsvg%2Bxml' in stdout and 'Microsoft' in stdout:
        print("✅ Microsoft logo correctly embedded as data URI")
    else:
        print("❌ Microsoft logo embedding failed")
    
    if 'logo=github&logoColor=white' in stdout and 'GitHub' in stdout:
        print("✅ GitHub logo correctly uses slug parameter")
    else:
        print("❌ GitHub logo slug usage failed")

def test_force_embed_svg():
    """Test forcing SVG embedding for all icons."""
    print("\n" + "=" * 60)
    print("Testing --embed-svg flag (force embedding for all icons)")
    print("=" * 60)
    
    stdout, stderr, returncode = run_badgesort([
        '-s', 'github', 'python',
        '-p', 'shields',
        '--embed-svg',
        '--no-thanks'
    ])
    
    print("Command: badgesort -s github python -p shields --embed-svg --no-thanks")
    print("Return code:", returncode)
    print("\nOutput:")
    print(stdout)
    
    # Check that both icons use data URIs
    github_embedded = 'data%3Aimage%2Fsvg%2Bxml' in stdout and 'GitHub' in stdout
    python_embedded = 'data%3Aimage%2Fsvg%2Bxml' in stdout and 'Python' in stdout
    
    if github_embedded and python_embedded:
        print("✅ All icons correctly embedded as data URIs")
    else:
        print("❌ Force embedding failed")

def test_skip_logo_check():
    """Test skipping logo checks."""
    print("\n" + "=" * 60)
    print("Testing --skip-logo-check flag")
    print("=" * 60)
    
    stdout, stderr, returncode = run_badgesort([
        '-s', 'microsoft',
        '-p', 'shields',
        '--skip-logo-check',
        '--no-thanks'
    ])
    
    print("Command: badgesort -s microsoft -p shields --skip-logo-check --no-thanks")
    print("Return code:", returncode)
    print("\nOutput:")
    print(stdout)
    
    # Check that Microsoft uses slug parameter (won't show icon but that's expected)
    if 'logo=microsoft&logoColor=white' in stdout and 'Microsoft' in stdout:
        print("✅ Logo check correctly skipped - using slug parameter")
    else:
        print("❌ Skip logo check failed")

def test_badgen_compatibility():
    """Test that Badgen provider still works as expected."""
    print("\n" + "=" * 60)
    print("Testing Badgen provider (should always embed SVGs)")
    print("=" * 60)
    
    stdout, stderr, returncode = run_badgesort([
        '-s', 'github', 'microsoft',
        '-p', 'badgen',
        '--no-thanks'
    ])
    
    print("Command: badgesort -s github microsoft -p badgen --no-thanks")
    print("Return code:", returncode)
    print("\nOutput:")
    print(stdout)
    
    # Check that Badgen URLs are generated correctly
    if 'badgen.net/badge' in stdout and 'data%3Aimage%2Fsvg%2Bxml' in stdout:
        print("✅ Badgen provider correctly uses embedded SVGs")
    else:
        print("❌ Badgen provider test failed")

if __name__ == '__main__':
    print("BadgeSort Missing Logo Detection Test Suite")
    print("==========================================")
    print()
    
    test_missing_logo_detection()
    test_force_embed_svg()
    test_skip_logo_check()
    test_badgen_compatibility()
    
    print("\n" + "=" * 60)
    print("Test suite completed!")
    print("=" * 60)