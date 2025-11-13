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
├── tests/
│   ├── __init__.py         # Test package initialization
│   ├── test_codeblock_handling.py  # Unit tests for codeblock detection
│   └── test_integration.py # Integration tests for full workflow
├── action.yml              # GitHub Action definition
├── Dockerfile              # Docker container configuration
├── entrypoint.sh           # Container entrypoint script
├── pyproject.toml          # Poetry dependencies and project metadata
├── pytest.ini              # Pytest configuration
└── README.md               # Project documentation with examples
```

## Technology Stack

- **Language**: Python 3.9+
- **Package Manager**: Poetry
- **Testing**: pytest with pytest-cov for coverage
- **Dependencies**:
  - `requests`: HTTP requests to Shields.io
  - `simpleicons`: Access to Simple Icons database
  - `pytest`, `pytest-cov`: Testing framework (dev dependencies)
  - Standard library: `argparse`, `colorsys`, `urllib`, etc.
- **Container**: Docker (based on `duffn/python-poetry:3.11-slim`)
- **Platform**: GitHub Actions

## Coding Standards and Conventions

### Commit Message Format (REQUIRED)
**All commits MUST follow semantic commit conventions with ONLY these allowed types:**

Format: `<type>(<scope>): <description>`

**Allowed Types (ONLY these three):**
- `feat`: A new feature (e.g., `feat(icons): add support for Badgen.net provider`)
- `fix`: A bug fix (e.g., `fix(icons): prevent badge injection into codeblocks`)
- `chore`: Changes to build process, dependencies, tests, docs, or auxiliary tools (e.g., `chore(deps): update simpleicons to 7.21.0`, `chore(tests): add codeblock handling tests`, `chore(docs): update README instructions`)

**Scope (optional but recommended):**
- `icons`: Badge generation and file manipulation
- `hilbert`: Hilbert curve sorting
- `actions`: GitHub Actions integration
- `docker`: Docker/container changes
- `deps`: Dependency updates
- `workflow`: CI/CD workflows
- `readme`: README documentation
- `tests`: Test infrastructure
- `docs`: Documentation updates
- `copilot`: Copilot instructions

**Examples:**
- ✅ `feat(icons): add codeblock detection to skip documentation examples`
- ✅ `fix(icons): handle unclosed codeblocks gracefully`
- ✅ `chore(tests): add integration tests for multiple badge IDs`
- ✅ `chore(readme): clarify comment marker requirements`
- ✅ `chore(deps): add pytest and pytest-cov dev dependencies`
- ✅ `chore(copilot): update commit message guidelines`
- ❌ `Fix bug` (too vague, missing type)
- ❌ `Update icons.py` (missing type and description)
- ❌ `docs(readme): update` (docs type not allowed, use chore)
- ❌ `test(icons): add tests` (test type not allowed, use chore)
- ❌ `Fixed the codeblock issue` (should be: `fix(icons): prevent...`)

**Pull Request Titles:**
PR titles MUST also follow the same semantic format with only feat, fix, or chore types.

### Testing Requirements (REQUIRED)
**All new features and bug fixes MUST include tests:**

1. **New Features**: 
   - Add unit tests covering the new functionality
   - Add integration tests if the feature affects the full workflow
   - Minimum 80% code coverage for new code

2. **Bug Fixes**:
   - Add a test that reproduces the bug (should fail before the fix)
   - Verify the test passes after the fix
   - Add regression tests to prevent the bug from reoccurring

3. **Test Location**:
   - Unit tests: `tests/test_<module_name>.py`
   - Integration tests: `tests/test_integration.py`
   - Test fixtures: `tests/fixtures/` (if needed)

4. **Running Tests**:
   ```bash
   # Run all tests
   pytest tests/ -v
   
   # Run with coverage
   pytest tests/ --cov=badgesort --cov-report=term-missing
   
   # Run specific test file
   pytest tests/test_codeblock_handling.py -v
   ```

5. **Test Guidelines**:
   - Use descriptive test names: `test_<what>_<condition>_<expected_result>`
   - Each test should test one specific behavior
   - Use meaningful assertions with custom error messages
   - Clean up any temporary files/resources in tests
   - Mock external dependencies (HTTP requests, file I/O when appropriate)

6. **CI Integration**:
   - All tests run automatically in the CI pipeline
   - PRs cannot be merged if tests fail
   - Coverage reports are generated for each test run

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
1. **Design**: Plan the minimal changes needed
2. **Write Tests First** (TDD approach recommended):
   - Write failing tests that describe the expected behavior
   - Implement the feature to make tests pass
   - Refactor while keeping tests green
3. **Implementation**:
   - **New Sorting Algorithm**: Add to the `if/elif` chain in `run()` function
   - **New Output Format**: Add case in badge generation section
   - **New Options**: Add to argparse in `main()` and update `action.yml`
4. **Testing**: Ensure all tests pass and coverage is adequate
5. **Documentation**: Update README.md if user-facing changes
6. **Commit**: Use semantic commit messages (see Coding Standards)

### Testing Approach
- **Primary**: pytest-based unit and integration tests
- **Location**: All tests in `tests/` directory
- **Coverage**: Aim for 80%+ coverage on new code
- **CI Pipeline**: Tests run automatically on every push
- Test both CLI and GitHub Actions interfaces
- Validate output in both Markdown and HTML formats
- Include edge cases and error conditions

### Test File Organization
```
tests/
├── __init__.py                    # Test package
├── test_codeblock_handling.py    # Codeblock detection tests
├── test_integration.py            # Full workflow integration tests
└── fixtures/                      # Test data files (if needed)
```

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
5. **Add tests** to verify the option works correctly
6. Document in README.md
7. Commit with semantic message: `feat(icons): add <option-name> option`

### Fixing a Bug
1. **Write a failing test** that reproduces the bug
2. Implement the fix in the appropriate module
3. **Verify the test now passes**
4. Add additional tests for edge cases
5. Update documentation if behavior changed
6. Commit with semantic message: `fix(<scope>): <description of what was fixed>`

### Adding a New Feature
1. **Plan and document** the feature requirements
2. **Write tests** describing expected behavior (TDD)
3. Implement the feature incrementally
4. Ensure all tests pass with good coverage
5. Update README.md with examples and usage
6. Commit with semantic message: `feat(<scope>): <feature description>`

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
3. **Write Tests First**: Create tests that define expected behavior (TDD recommended)
4. **Implement Changes**: Make the minimal code changes to pass tests
5. **Run Tests Locally**: `pytest tests/ -v --cov=badgesort`
6. **Update Documentation**: Modify README.md examples if adding user-facing features
7. **Commit with Semantic Messages**: Follow Conventional Commits format
   - Example: `feat(icons): add badgen.net provider support`
8. **Verify GitHub Action**: Test action interface if changing inputs/outputs
9. **Check CI Pipeline**: Ensure all workflow tests pass

### Commit Checklist
- [ ] All tests pass locally
- [ ] New code has test coverage (80%+ for new features)
- [ ] Commit message follows semantic format: `<type>(<scope>): <description>`
- [ ] PR title follows semantic format
- [ ] Documentation updated (if user-facing changes)
- [ ] No security vulnerabilities introduced

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
