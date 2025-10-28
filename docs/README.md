# BadgeSort Interactive Generator

This directory contains the interactive web-based badge generator for BadgeSort.

## Overview

The interactive generator (`index.html`) provides a user-friendly interface to:
- Select badges from all available Simple Icons
- Configure badge styles and sorting algorithms  
- Preview badges in real-time
- Generate GitHub Actions YAML configuration

## Build Process

The microsite is automatically built and deployed via GitHub Actions whenever changes are pushed to the `main` branch.

### Building Locally

To build the microsite locally:

```bash
python3 scripts/build_microsite.py
```

This will:
1. Read the template from `docs/index.template.html`
2. Inject the current git commit hash
3. Generate `docs/index.html`

**Note:** The generated `docs/index.html` file is excluded from version control (`.gitignore`) as it is automatically built during deployment.

### Template

The `index.template.html` file contains:
- HTML structure and styling
- PyScript configuration
- Python code for the interactive badge generator
- Placeholder `{{COMMIT_HASH}}` for build information

When making changes to the microsite, edit `index.template.html` rather than `index.html`.

## Deployment

The microsite is automatically deployed to GitHub Pages via the `.github/workflows/deploy-pages.yml` workflow. 

The workflow is triggered on:
- Push to `main` branch (when files in `docs/`, `badgesort/`, or the build script change)
- Manual workflow dispatch

## Usage

### Local Development

1. Make changes to `docs/index.template.html`
2. Build the site: `python3 scripts/build_microsite.py`
3. Serve the directory with a web server:
```bash
cd docs && python3 -m http.server 8000
```
4. Open http://localhost:8000/ in your browser

### Live Site

The microsite is deployed at: https://chipwolf.github.io/BadgeSort/

## Features

- **2400+ Icons**: Browse and select from all Simple Icons
- **Search**: Filter icons by name
- **Quick Select**: "Popular Tech" button for common technology badges
- **Real-time Preview**: See badge appearance as you configure
- **YAML Generation**: Copy-paste ready GitHub Actions configuration
- **All Badge Styles**: Support for all Shields.io badge styles
- **All Sort Algorithms**: Hilbert, HSV, Step, Luminance, and Random sorting
- **Missing Logo Detection**: Automatically detects and embeds missing Shields.io logos
- **Dual Provider Support**: Shields.io with automatic SVG embedding and Badgen.net
- **Build Information**: Displays the commit hash of the deployed version

## Technical Details

- Uses **PyScript** to run Python code directly in the browser
- Loads Simple Icons package via PyScript (simpleicons==7.21.0)
- Shields.io for badge rendering
- Responsive design for mobile and desktop
- No backend required
- Built and deployed automatically via GitHub Actions

## Maintenance

When updating BadgeSort algorithms or badge generation logic:
1. Update the Python code in `badgesort/icons.py` for the CLI
2. Update the corresponding code in `docs/index.template.html` for the microsite
3. Both implementations should be kept in sync for consistency

The microsite uses a browser-adapted version of the BadgeSort logic optimized for PyScript and DOM manipulation.
