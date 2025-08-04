# Daily Summary System Setup

This repository is set up for automated daily summary creation and README updates.

## Files Overview

- `template.md` - Template for daily summaries
- `create_daily_summary.py` - Python script to create daily summary files
- `create_today.sh` - Shell script for easy daily summary creation
- `create_missing_summaries.py` - Script to create missing summary files
- `validate_day_counters.py` - Script to validate and fix day counters
- `config.py` - Configuration file for start date
- `.github/workflows/update-readme.yml` - GitHub Actions workflow
- `.github/scripts/update_readme.py` - Script to update README with summary links
- `.github/scripts/fix_day_counters.py` - Script to fix day counters in summary files

## Quick Start

### 1. Create Today's Summary
```bash
# Option 1: Using the shell script (recommended)
./create_today.sh

# Option 2: Using Python directly
python3 create_daily_summary.py

# Option 3: For a specific date
python3 create_daily_summary.py 2024-01-15

# Option 4: With start date for day counting
python3 create_daily_summary.py --start-date 2024-01-01
./create_today.sh 2024-01-01
```

### 2. Edit Your Summary
Open the generated file in the `Summary/` directory and fill in your daily progress.

### 3. Create Missing Summaries (Optional)
```bash
# Create all missing summaries in the existing date range
python3 create_missing_summaries.py

# Create missing summaries for a specific date range
python3 create_missing_summaries.py 2024-01-01 2024-01-31

# With start date for day counting
python3 create_missing_summaries.py --start-date-counter 2024-01-01
```

### 4. Validate Day Counters (Optional)
```bash
# Check and fix day counters manually
python3 validate_day_counters.py

# Or run the GitHub workflow which will do this automatically
```

### 5. Commit and Push
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
1. Validate and fix day counters in all summary files
2. Update the README.md with links to all summary files
3. Show the 10 most recent summaries with day counters (if start date is configured)
4. Display word count for completed summaries
5. Show missing summaries in a collapsible section
6. Commit and push the updated README and any fixed summary files

## Customization

### Modify Template
Edit `template.md` to change the structure of your daily summaries.

### Configure Start Date
Edit `config.py` to set your project start date for day counting:
```python
START_DATE = "2024-01-01"  # Your actual start date
```

**Note**: When you change the START_DATE, the system will automatically fix day counters in all existing summary files during the next GitHub Actions run.

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

### Day Counter Issues
If day counters seem incorrect after changing START_DATE:
```bash
# Run manual validation
python3 validate_day_counters.py

# Or wait for the next GitHub Actions run to fix automatically
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
- `{{DAY_COUNTER}}` - Day counter (e.g., " [Day 123]") if start date is configured

These are automatically replaced when creating new summary files. 