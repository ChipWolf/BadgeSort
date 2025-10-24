# GitHub Copilot Instructions for BadgeSort

## Project Overview

BadgeSort is a Python 3 command-line tool and GitHub Action that automates the generation and color sorting of badges from [Shields.io](https://shields.io) with brand logos from [Simple Icons](https://simpleicons.org/).

### Purpose
- Generate branded badges automatically from Simple Icons slugs
- Sort badges by color using various algorithms (Hilbert walk, HSV, step, luminance, etc.)
- Output badges in Markdown or HTML format
- Support both CLI and GitHub Actions workflows

## Project Structure

```
BadgeSort/
├── .github/
│   └── workflows/          # GitHub Actions workflows
├── badgesort/
│   ├── __init__.py         # Package initialization (empty)
│   ├── icons.py            # Main badge generation and sorting logic
│   ├── hilbert.py          # Hilbert curve implementation for color sorting
│   └── gh_actions_entrypoint.py  # GitHub Actions integration
├── action.yml              # GitHub Action definition
├── Dockerfile              # Docker container configuration
├── entrypoint.sh           # Container entrypoint script
├── pyproject.toml          # Poetry dependencies and project metadata
└── README.md               # Project documentation with examples
```

## Technology Stack

- **Language**: Python 3.9+
- **Package Manager**: Poetry
- **Dependencies**:
  - `requests`: HTTP requests to Shields.io
  - `simpleicons`: Access to Simple Icons database
  - Standard library: `argparse`, `colorsys`, `urllib`, etc.
- **Container**: Docker (based on `duffn/python-poetry:3.11-slim`)
- **Platform**: GitHub Actions

## Coding Standards and Conventions

### Python Style
- Use Python 3.9+ syntax and features
- Follow PEP 8 style guidelines
- Use meaningful variable names (e.g., `icon_list`, `badge_style`)
- Include type hints where it improves clarity
- Keep functions focused on a single responsibility

### File Headers
- Use UTF-8 encoding declaration: `# -*- coding: utf-8 -*-`
- Include shebang for executable scripts: `#!/usr/bin/env python3`

### Logging
- Use Python's `logging` module (already configured)
- Log at appropriate levels:
  - `DEBUG`: Detailed information for debugging (icon details, sort operations)
  - `INFO`: General informational messages (operation summaries)
  - `FATAL`: Critical errors that require exit

### Code Organization
- Main logic in `icons.py` with `main()` and `run()` functions
- Keep algorithm implementations separate (e.g., `hilbert.py`)
- Use descriptive function names that indicate purpose

## Key Functionality

### Badge Generation (`badgesort/icons.py`)
1. **Input Processing**: Accept slugs, random selection, or all icons
2. **URL Generation**: Create Shields.io URLs with proper encoding
3. **Color Sorting**: Apply selected algorithm (hilbert, hsv, step, luminance, random)
4. **Output Formatting**: Generate Markdown or HTML markup
5. **File Updates**: Replace content between `<!-- start/end -->` markers

### Color Sorting Algorithms
- **hilbert** (default): Hilbert curve walk for visually appealing color distribution
- **hsv**: Sort by HSV color space
- **step/step_invert**: Step function with optional hue rotation
- **luminance**: Sort by brightness
- **random**: Randomize order

### GitHub Actions Integration (`gh_actions_entrypoint.py`)
- Parse environment variables prefixed with `INPUT_`
- Convert action inputs to CLI arguments
- Capture output for `GITHUB_OUTPUT`
- Preserve exit codes

## Development Guidelines

### Adding New Features
1. **New Sorting Algorithm**: Add to the `if/elif` chain in `run()` function
2. **New Output Format**: Add case in badge generation section
3. **New Options**: Add to argparse in `main()` and update `action.yml`

### Testing Approach
- Manual testing through the build-and-test workflow
- Verify badge generation with multiple scenarios (see `.github/workflows/build-and-test.yaml`)
- Test both CLI and GitHub Actions interfaces
- Validate output in both Markdown and HTML formats

### Building and Testing

#### Local Development
```bash
# Install dependencies
poetry install

# Run CLI
python -m badgesort.icons -s github python docker

# Test with specific options
python -m badgesort.icons -c hilbert -f markdown -b for-the-badge -s osu github
```

#### Docker Build
```bash
# Build container
docker build -t badgesort .

# Run as GitHub Action locally
docker run -e INPUT_SLUGS="github python docker" badgesort
```

#### GitHub Actions
- Push to main triggers build-and-test workflow
- Workflow builds Docker image and tests badge generation
- See `.github/workflows/build-and-test.yaml` for examples

## Important Considerations

### URL Encoding
- Brand names must be URL-encoded properly
- Handle special characters in icon titles
- Use `quote()` from `urllib.parse` with appropriate safe characters
- Double hyphens in URLs: replace `-` with `--`

### Color Calculations
- Brightness calculation: `(R*299 + G*587 + B*114) / 255000`
- Logo color (white/black) based on brightness threshold of 0.7
- RGB values parsed from 6-character hex strings

### Badge Markers
- Always preserve `<!-- start chipwolf/badgesort {id} -->` and `<!-- end chipwolf/badgesort {id} -->` markers
- Use regex with `re.S` flag to handle multi-line replacements
- Support multiple badge sections with different IDs

### Error Handling
- Validate slugs exist in Simple Icons database
- Log missing slugs and continue with valid ones
- Exit with proper error codes on failures
- Optional badge verification via HTTP requests to Shields.io

## Common Tasks

### Adding a New Command-Line Option
1. Add argument to parser in `main()` function
2. Update `args` handling in `run()` function
3. If for GitHub Actions, add mapping in `gh_actions_entrypoint.py`
4. Update `action.yml` inputs section
5. Document in README.md

### Modifying Badge Output
- Markdown format: `![{title}]({url})`
- HTML format: `<a href="#"><img alt="{title}" src="{url}"></a>`
- Always include alt text for accessibility
- BadgeSort badge links to GitHub repository

### Working with Simple Icons
- Access via `simpleicons.all.icons` dictionary
- Keys are slugs (lowercase, no spaces)
- Each icon has: `title`, `hex`, `slug`, `svg` properties
- Check slug existence before processing

## Dependencies and Version Management

### Poetry
- Use `poetry add` to add new dependencies
- Keep `pyproject.toml` and `poetry.lock` in sync
- Specify Python version constraints: `^3.9`

### Docker
- Base image: `duffn/python-poetry:3.11-slim`
- Install dependencies in two stages (cache efficiency)
- Activate venv before running Python commands

### GitHub Actions
- Use pinned action versions with SHA for security
- Update via Renovate bot (configured in `.github/renovate.json5`)

## Contribution Workflow

1. **Understand the Change**: Review issue/feature request thoroughly
2. **Plan Minimal Changes**: Identify the smallest change needed
3. **Test Locally**: Run CLI with various options before committing
4. **Update Documentation**: Modify README.md examples if adding features
5. **Verify GitHub Action**: Test action interface if changing inputs/outputs
6. **Check Workflows**: Ensure build-and-test workflow passes

## Security Considerations

- Never log or expose API keys, tokens, or sensitive data
- Filter environment variables in `gh_actions_entrypoint.py` (exclude `API_KEY`, `TOKEN`, `EVENT`)
- Validate all external inputs (slugs, URLs)
- Use latest security patches for dependencies (managed by Renovate)

## GitHub Actions Best Practices

- Use environment variables via `INPUT_` prefix
- Write multi-line outputs using heredoc delimiter
- Preserve exit codes from underlying CLI
- Provide clear step names in workflows
- Cache Docker layers for faster builds

## Resources

- [Shields.io Documentation](https://shields.io/)
- [Simple Icons](https://simpleicons.org/)
- [Hilbert Curve Color Sorting Article](https://www.alanzucconi.com/2015/09/30/colour-sorting/)
- Repository: https://github.com/ChipWolf/BadgeSort
