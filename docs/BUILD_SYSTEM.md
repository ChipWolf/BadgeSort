# Microsite Build and Deployment System

## Summary

This document describes the automated build and deployment system for the BadgeSort microsite.

## Problem

Previously, the BadgeSort microsite at `/docs/index.html` contained a complete copy of the application code embedded directly in the HTML file. When the main BadgeSort application was updated, the microsite needed to be manually synchronized, leading to:

- Code duplication
- Maintenance burden
- Risk of the microsite falling out of sync with the main application

## Solution

An automated build and deployment system that:

1. **Separates template from generated output**: The microsite source is now in `docs/index.template.html` with a placeholder for dynamic content (commit hash)
2. **Automates the build**: A Python script (`scripts/build_microsite.py`) generates the final `docs/index.html` by injecting the current commit hash
3. **Automates deployment**: A GitHub Actions workflow (`.github/workflows/deploy-pages.yml`) builds and deploys the microsite to GitHub Pages automatically
4. **Displays build information**: The deployed site shows the commit hash it was built from

## Architecture

### Files

- **`docs/index.template.html`** (source, tracked in git)
  - Contains the complete microsite HTML, CSS, JavaScript, and PyScript code
  - Includes placeholder `{{COMMIT_HASH}}` for build information
  - This is the file to edit when making changes to the microsite

- **`docs/index.html`** (generated, NOT tracked in git)
  - Generated from the template by `scripts/build_microsite.py`
  - Has the commit hash placeholder replaced with the actual git commit hash
  - Excluded from version control via `.gitignore`

- **`scripts/build_microsite.py`**
  - Python script that builds the microsite
  - Reads `docs/index.template.html`
  - Injects the current git commit hash
  - Writes to `docs/index.html`

- **`.github/workflows/deploy-pages.yml`**
  - GitHub Actions workflow for automated deployment
  - Triggered on push to `main` branch when relevant files change
  - Can also be manually triggered via workflow_dispatch
  - Builds the microsite and deploys to GitHub Pages

### Build Process

```
┌─────────────────────────┐
│  docs/index.template.html│
│  (source with {{...}})  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ scripts/build_microsite.py│
│  - Get git commit hash  │
│  - Replace placeholders │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   docs/index.html       │
│   (generated output)    │
└─────────────────────────┘
```

### Deployment Process

```
┌─────────────────────────┐
│  Push to main branch    │
│  (docs/**, badgesort/** │
│   or build scripts)     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  GitHub Actions         │
│  deploy-pages.yml       │
│  1. Checkout code       │
│  2. Setup Python        │
│  3. Build microsite     │
│  4. Configure Pages     │
│  5. Upload artifact     │
│  6. Deploy to Pages     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  GitHub Pages           │
│  https://chipwolf.      │
│  github.io/BadgeSort/   │
└─────────────────────────┘
```

## Usage

### Making Changes to the Microsite

1. Edit `docs/index.template.html`
2. Test locally:
   ```bash
   python3 scripts/build_microsite.py
   cd docs && python3 -m http.server 8000
   ```
3. Commit and push to `main` branch
4. GitHub Actions will automatically build and deploy

### Local Development

```bash
# Build the microsite
python3 scripts/build_microsite.py

# Serve locally
cd docs && python3 -m http.server 8000
# Visit http://localhost:8000/
```

### Manual Deployment

If needed, the workflow can be manually triggered:
1. Go to the repository's Actions tab
2. Select "Deploy GitHub Pages" workflow
3. Click "Run workflow"
4. Select the branch (usually `main`)
5. Click "Run workflow"

## Code Maintenance

### Microsite vs CLI Code

The microsite Python code (embedded in `docs/index.template.html`) is a **browser-adapted version** of the BadgeSort CLI logic. Key differences:

- **Microsite**: Uses PyScript, DOM manipulation, JavaScript interop
- **CLI**: Uses standard Python libraries, file I/O, CLI arguments

When updating badge generation or sorting algorithms:
1. Update `badgesort/icons.py` for CLI functionality
2. Update the corresponding code in `docs/index.template.html` for the microsite
3. Both implementations should be kept conceptually in sync

The microsite is not automatically generated from the CLI code because:
- Different execution environments (browser vs Python interpreter)
- Different interfaces (DOM vs command-line)
- Different dependencies (PyScript vs system packages)

### Keeping Code in Sync

When making changes to badge generation or sorting algorithms, follow this checklist:

**For CLI Changes** (`badgesort/icons.py`):
- [ ] Update the CLI function (e.g., `run()`, sorting algorithms, badge URL generation)
- [ ] Test the CLI locally: `python -m badgesort.icons -s github python`
- [ ] Update corresponding logic in `docs/index.template.html` (see checklist below)

**For Microsite Changes** (`docs/index.template.html`):
- [ ] Locate the equivalent function in the embedded Python code (after line 637)
- [ ] Update the logic to match the CLI changes
- [ ] Account for browser-specific differences (PyScript, no file I/O, DOM updates)
- [ ] Test locally: `python3 scripts/build_microsite.py && cd docs && python3 -m http.server`
- [ ] Verify in browser at http://localhost:8000/

**Key Areas to Keep in Sync**:
1. **Badge URL generation**: Search for `icon_url =` in both files
2. **Sorting algorithms**: Functions `Hilbert_to_int`, `lum`, `step`, color sort logic
3. **SVG embedding logic**: `svg_to_base64_data_uri` and related functions
4. **Color calculations**: RGB to HSV, brightness calculations, logo color selection

**Testing Both**:
- [ ] CLI: Run with various options and verify output
- [ ] Microsite: Test all sorting algorithms, badge styles, and providers
- [ ] Compare badge URLs generated by both (should be identical for same inputs)

## Benefits

1. **No manual synchronization**: Deployment is fully automated
2. **Version transparency**: Build commit hash visible on the site
3. **Consistent deployments**: Every push to main triggers rebuild
4. **Easy rollback**: Can redeploy any previous commit
5. **Clear separation**: Template vs generated file
6. **No code in git**: Generated file excluded from version control

## Configuration

### GitHub Repository Settings

For the workflow to work, ensure:

1. **GitHub Pages is enabled**:
   - Go to Settings → Pages
   - Source: GitHub Actions (not branch-based deployment)

2. **Workflow permissions**:
   - Go to Settings → Actions → General
   - Workflow permissions: "Read and write permissions"
   - Allow GitHub Actions to create and approve pull requests: Enabled

### Workflow Triggers

The workflow triggers on:
- Push to `main` branch when these paths change:
  - `docs/**`
  - `badgesort/**`
  - `scripts/build_microsite.py`
  - `.github/workflows/deploy-pages.yml`
- Manual trigger via `workflow_dispatch`

## Troubleshooting

### Build fails with "Could not get git commit hash"

This shouldn't happen in GitHub Actions (git is always available), but if running locally in a non-git directory, the script will use "unknown" as the commit hash.

### Page not updating after push

1. Check the Actions tab for workflow runs
2. Verify the workflow completed successfully
3. GitHub Pages may cache content - wait a few minutes or force refresh (Ctrl+F5)
4. Check that the workflow triggers are configured correctly

### Local build fails

Ensure you're running from the repository root:
```bash
python3 scripts/build_microsite.py
```

## Future Enhancements

Possible future improvements:

1. **Minification**: Add HTML/CSS/JS minification to reduce file size
2. **Asset optimization**: Optimize any images or assets
3. **Build caching**: Cache build artifacts for faster deployments
4. **Preview deployments**: Deploy PR previews for testing changes
5. **Code extraction**: Extract shared algorithm logic into a common module that both CLI and microsite can import (would require PyScript package support)
