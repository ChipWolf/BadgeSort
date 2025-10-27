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

1. Generate the icons data:
```bash
python3 -c "
import json
from simpleicons.all import icons

icons_list = []
for slug in sorted(list(icons.keys())):
    icon = icons.get(slug)
    icons_list.append({
        'slug': slug,
        'title': icon.title,
        'hex': icon.hex,
        'path': icon.path
    })

print(json.dumps({'icons': icons_list}))
" > icons_data.json
```

2. Serve the directory with a web server:
```bash
python3 -m http.server 8000
```

3. Open http://localhost:8000/ in your browser

### Deployment

To deploy this microsite:

1. Generate the `icons_data.json` file as shown above
2. Host the directory on any static web hosting service (GitHub Pages, Netlify, Vercel, etc.)

The microsite is a single-page application with no backend dependencies.

## Features

- **2400+ Icons**: Browse and select from all Simple Icons
- **Search**: Filter icons by name
- **Quick Select**: "Popular Tech" button for common technology badges
- **Real-time Preview**: See badge appearance as you configure
- **YAML Generation**: Copy-paste ready GitHub Actions configuration
- **All Badge Styles**: Support for all Shields.io badge styles
- **All Sort Algorithms**: Hilbert, HSV, Step, Luminance, and Random sorting

## Technical Details

- Pure HTML, CSS, and JavaScript (no build step required)
- Uses Simple Icons data loaded from `icons_data.json`
- Shields.io for badge rendering
- Responsive design for mobile and desktop
