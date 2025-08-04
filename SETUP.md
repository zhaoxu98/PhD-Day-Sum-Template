# Daily Summary System Setup

This repository is set up for automated daily summary creation and README updates.

## Files Overview

- `template.md` - Template for daily summaries
- `create_daily_summary.py` - Python script to create daily summary files
- `create_today.sh` - Shell script for easy daily summary creation
- `.github/workflows/update-readme.yml` - GitHub Actions workflow
- `.github/scripts/update_readme.py` - Script to update README with summary links

## Quick Start

### 1. Create Today's Summary
```bash
# Option 1: Using the shell script (recommended)
./create_today.sh

# Option 2: Using Python directly
python3 create_daily_summary.py

# Option 3: For a specific date
python3 create_daily_summary.py 2024-01-15
```

### 2. Edit Your Summary
Open the generated file in the `Summary/` directory and fill in your daily progress.

### 3. Commit and Push
```bash
git add Summary/
git commit -m "Add daily summary for 2024-01-15"
git push
```

## GitHub Actions Workflow

The workflow automatically triggers when:
- Files are pushed to the `Summary/` directory
- Manual trigger via GitHub Actions UI

The workflow will:
1. Update the README.md with links to all summary files
2. Show the 10 most recent summaries
3. Display word count for completed summaries
4. Commit and push the updated README

## Customization

### Modify Template
Edit `template.md` to change the structure of your daily summaries.

### Change Summary Directory
Update the paths in:
- `create_daily_summary.py` (line with `output_path`)
- `.github/scripts/update_readme.py` (line with `glob.glob`)

### Modify README Format
Edit `.github/scripts/update_readme.py` to change how the README is generated.

## Troubleshooting

### Script Permissions
If you get permission errors, make sure scripts are executable:
```bash
chmod +x create_daily_summary.py create_today.sh .github/scripts/update_readme.py
```

### Python Version
The scripts require Python 3.6+. Check your version:
```bash
python3 --version
```

### GitHub Actions Issues
- Ensure the workflow file is in `.github/workflows/`
- Check that the repository has Actions enabled
- Verify the workflow has proper permissions to push commits

## File Naming Convention

Daily summary files follow the format: `YYYY-MM-DD.md`
- Example: `2024-01-15.md`
- Files are automatically sorted by date (newest first)
- Invalid date formats will be ignored

## Template Variables

The template supports these variables:
- `{{DATE}}` - Current date (YYYY-MM-DD)
- `{{DATETIME}}` - Current date and time (YYYY-MM-DD HH:MM:SS)

These are automatically replaced when creating new summary files. 