# BadgeSort Interactive Generator

This directory contains the interactive web-based badge generator for BadgeSort.

## Overview

The interactive generator (`index.html`) provides a user-friendly interface to:
- Select badges from all available Simple Icons
- Configure badge styles and sorting algorithms  
- Preview badges in real-time
- Generate GitHub Actions YAML configuration

## Usage

### Local Development

1. Serve the directory with a web server:
```bash
python3 -m http.server 8000
```

2. Open http://localhost:8000/ in your browser

### Deployment

To deploy this microsite:

1. Host the directory on any static web hosting service (GitHub Pages, Netlify, Vercel, etc.)

The microsite is a single-page application with no backend dependencies. PyScript will automatically download and run the Python code in the browser.

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

## Technical Details

- Uses **PyScript** to run Python code directly in the browser
- Reuses the existing BadgeSort Python logic (no code duplication)
- Loads Simple Icons package via PyScript (simpleicons==7.21.0)
- Shields.io for badge rendering
- Responsive design for mobile and desktop
- No build step or backend required
