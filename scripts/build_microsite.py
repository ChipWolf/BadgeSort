#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build script for the BadgeSort microsite.

This script generates the microsite HTML by combining:
1. The HTML/CSS/JS template from docs/index.template.html
2. The commit hash for display

The microsite Python code is kept separate from the CLI to handle browser-specific functionality.
"""

import sys
import subprocess
from pathlib import Path


def build_microsite(repo_root, commit_hash):
    """Build the microsite HTML file by injecting the commit hash."""
    repo_path = Path(repo_root)
    
    # Read the template
    template_path = repo_path / 'docs' / 'index.template.html'
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace commit hash placeholder
    html_content = template.replace('{{COMMIT_HASH}}', commit_hash[:8])
    
    # Write the output
    output_path = repo_path / 'docs' / 'index.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Microsite built successfully!")
    print(f"  Template: {template_path}")
    print(f"  Output: {output_path}")
    print(f"  Commit: {commit_hash[:8]}")


def main():
    """Main entry point for the build script."""
    # Get the repo root (parent of scripts directory)
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    
    # Get the current commit hash
    try:
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True
        )
        commit_hash = result.stdout.strip()
    except subprocess.CalledProcessError:
        print("Warning: Could not get git commit hash, using 'unknown'")
        commit_hash = 'unknown'
    
    # Build the microsite
    build_microsite(repo_root, commit_hash)


if __name__ == '__main__':
    main()
