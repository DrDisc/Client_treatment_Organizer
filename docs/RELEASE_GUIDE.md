# Release Guide

This guide explains how to create releases for Client Treatment Organizer with automatic .exe generation.

## Automated Release Process (Recommended)

### Step 1: Prepare Your Code
1. Make sure all changes are committed
2. Update version numbers in:
   - `setup.py` (version parameter)
   - `src/__init__.py` (__version__)
   - `README.md` (if needed)

```python
# setup.py
setup(
    name="Client_Treatment_Organizer",
    version="0.1.0",  # Update this
    ...
)

# src/__init__.py
__version__ = "0.1.0"  # Update this
```

### Step 2: Create a GitHub Release

Using GitHub Web Interface:
1. Go to your repository: https://github.com/DrDisc/Client_treatment_Organizer/releases
2. Click "Create a new release"
3. Choose a tag (e.g., `v0.1.0`)
4. Add release title (e.g., "v0.1.0 - Feature Release")
5. Add release description
6. Click "Publish release"

Using GitHub CLI (`gh`):
```bash
gh release create v0.1.0 \
  --title "v0.1.0 - Feature Release" \
  --notes "Release description here..."
```

### Step 3: Automated Build

When you publish the release:
1. GitHub Actions automatically triggers the build workflow
2. The workflow:
   - Checks out your code
   - Installs Python and dependencies
   - Runs PyInstaller to create the .exe
   - Uploads the .exe to the release

### Step 4: Download the .exe

1. Wait 5-10 minutes for the build to complete
2. Go to the release page
3. Download `Client Treatment Organizer.exe` from the release assets
4. Test the executable before distribution

## Manual Local Build

If you need to build locally without GitHub:

### Step 1: Install Build Tools
```bash
pip install pyinstaller pillow
```

### Step 2: Run Build Script
```bash
python build_exe.py
```

The script will:
- Check for dependencies
- Create an application icon
- Build the executable
- Clean up temporary files

### Step 3: Find Your .exe
```
dist/Client Treatment Organizer.exe
```

## Version Numbering

Use Semantic Versioning (MAJOR.MINOR.PATCH):

- **v0.0.1**: Initial release, pre-alpha
- **v0.1.0**: First beta release, basic features
- **v1.0.0**: First stable release
- **v1.1.0**: Feature addition
- **v1.1.1**: Bug fix

## Release Checklist

Before releasing:

- [ ] All code committed
- [ ] Version numbers updated
- [ ] README.md is current
- [ ] CHANGELOG.md updated (if applicable)
- [ ] All tests passing
- [ ] Documentation reviewed
- [ ] No sensitive data in repository

## Release Notes Template

```markdown
## v0.1.0 - [Release Name]

### New Features
- Feature 1 description
- Feature 2 description

### Improvements
- Improvement 1
- Improvement 2

### Bug Fixes
- Bug fix 1
- Bug fix 2

### Known Issues
- Known issue 1
- Known issue 2

### Installation
1. Download `Client Treatment Organizer.exe`
2. Run the executable
3. Follow the setup wizard

**Note:** This is a beta release. Please report issues on GitHub.
```

## Troubleshooting Build Issues

### Build Fails: "Python not found"
- Ensure Python is installed on your system
- Add Python to your PATH
- Use GitHub Actions for automated builds

### Build Fails: "PyInstaller not found"
```bash
pip install pyinstaller
python build_exe.py
```

### Build Fails: "Icon not found"
- The script will skip icon if not found
- To add icon: Create `assets/icon.ico`
- Recommended size: 256x256 or 512x512 pixels

### .exe is too large (>50MB)
- PyInstaller bundles Python interpreter
- This is normal; can be reduced with:
  - UPX compression (advanced)
  - Removing unused dependencies
  - Using onedir instead of onefile (larger folder, smaller exe)

### .exe runs but shows command line window
- Add `--windowed` flag to PyInstaller (already included in our scripts)

## Distribution

### For Users
1. Provide the `.exe` file
2. Include a README with system requirements:
   - Windows 7 or later
   - 100 MB disk space
   - No Python installation needed

### For Developers
1. Provide source code link
2. Installation instructions in README.md
3. Setup.py for pip installation

## GitHub Actions Configuration

The automated build is configured in `.github/workflows/build-exe.yml`:

```yaml
on:
  release:
    types: [published]
  workflow_dispatch:
```

This means builds trigger when:
- A release is published (manual)
- Manually via GitHub Actions tab (workflow_dispatch)

## Monitoring Build Status

1. Go to your repository
2. Click "Actions" tab
3. Select the latest workflow run
4. Check the logs for any errors

## Rollback Procedure

If a release has issues:
1. Delete the problematic release on GitHub
2. Fix the code
3. Create a new release with the corrected version

## Next Steps After Release

1. Test the distributed .exe on multiple Windows versions
2. Gather user feedback
3. Create issues for reported bugs
4. Plan next release features
5. Keep CHANGELOG.md updated
