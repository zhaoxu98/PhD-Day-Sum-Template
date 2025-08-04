#!/usr/bin/env python3
"""
Script to update README.md with links to daily summary files
"""

import os
import glob
from datetime import datetime, timedelta
import re

def get_summary_files():
    """Get all summary files from the Summary directory"""
    summary_files = glob.glob('Summary/*.md')
    # Sort files by date (newest first)
    summary_files.sort(reverse=True)
    return summary_files

def extract_date_from_filename(filename):
    """Extract date from filename (e.g., 'Summary/2024-01-15.md' -> '2024-01-15')"""
    basename = os.path.basename(filename)
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})\.md$', basename)
    return date_match.group(1) if date_match else None

def calculate_day_counter(date_str, start_date_str=None):
    """Calculate day counter for a given date"""
    if not start_date_str:
        return ""
    
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        days_diff = (date_obj - start_date).days
        if days_diff >= 0:
            return f" [Day {days_diff + 1}]"
    except ValueError:
        pass
    
    return ""

def format_date_for_display(date_str):
    """Format date for display (e.g., '2024-01-15' -> 'January 15, 2024')"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except ValueError:
        return date_str

def get_file_stats(filename):
    """Get basic stats about the summary file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count lines
        lines = content.split('\n')
        line_count = len(lines)
        
        # Count words
        word_count = len(content.split())
        
        # Check if file has content (not just template)
        has_content = any(line.strip() and not line.strip().startswith('- [ ]') 
                         for line in lines if line.strip())
        
        return {
            'line_count': line_count,
            'word_count': word_count,
            'has_content': has_content
        }
    except Exception:
        return {'line_count': 0, 'word_count': 0, 'has_content': False}

def generate_missing_summaries_section(summary_files):
    """Generate the missing summaries section"""
    if not summary_files:
        return ""
    
    # Extract all dates from existing files
    existing_dates = set()
    for filename in summary_files:
        date_str = extract_date_from_filename(filename)
        if date_str:
            existing_dates.add(date_str)
    
    if not existing_dates:
        return ""
    
    # Try to get start date from config
    start_date_str = None
    try:
        import sys
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        from config import START_DATE
        start_date_str = START_DATE
    except ImportError:
        pass
    
    # Find the date range
    sorted_dates = sorted(existing_dates)
    range_start_date = datetime.strptime(sorted_dates[0], '%Y-%m-%d')
    end_date = datetime.strptime(sorted_dates[-1], '%Y-%m-%d')
    
    # If we have a configured start date, use it as the range start
    if start_date_str:
        try:
            config_start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            # Use the earlier of config start date or first summary date
            start_date = min(config_start_date, range_start_date)
        except ValueError:
            start_date = range_start_date
    else:
        start_date = range_start_date
    
    # Generate all expected dates in the range
    expected_dates = set()
    current_date = start_date
    while current_date <= end_date:
        expected_dates.add(current_date.strftime('%Y-%m-%d'))
        current_date = current_date + timedelta(days=1)
    
    # Find missing dates
    missing_dates = sorted(expected_dates - existing_dates)
    
    if not missing_dates:
        return ""
    
    # Generate the section content
    content = "\n## Recent Missing Summaries\n\n"
    content += "<details>\n<summary>Click to expand missing summaries</summary>\n\n"
    content += "The following dates are missing from your daily summaries:\n\n"
    content += "```\n"
    
    # Group missing dates for better readability
    if len(missing_dates) <= 10:
        content += "\n".join(missing_dates)
    else:
        # Show first 5 and last 5 with ellipsis
        content += "\n".join(missing_dates[:5])
        content += "\n...\n"
        content += "\n".join(missing_dates[-5:])
        content += f"\n\nTotal missing: {len(missing_dates)} dates"
    
    content += "\n```\n\n"
    content += "To create missing summaries, use:\n"
    content += "```bash\n"
    content += "# For a single date\n"
    content += "python3 create_daily_summary.py YYYY-MM-DD\n\n"
    content += "# For multiple dates (example)\n"
    for date in missing_dates[-3:]:  # Show first 3 as examples
        content += f"python3 create_daily_summary.py {date}\n"
    if len(missing_dates) > 3:
        content += "# ... and so on for other missing dates\n"
    content += "```\n\n"
    content += "</details>\n\n"
    
    return content

def generate_readme_content():
    """Generate the complete README content"""
    
    # Try to get start date from environment, config file, or use default
    start_date_str = os.environ.get('START_DATE')
    
    if not start_date_str:
        # Try to import from config file
        try:
            import sys
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            from config import START_DATE
            start_date_str = START_DATE
        except ImportError:
            start_date_str = None
    
    # Header
    content = """# PhD Daily Summary

This repository contains my daily summaries during my PhD journey. Each day, I document my progress, challenges, and plans.

## Recent Summaries

"""
    
    # Get summary files
    summary_files = get_summary_files()
    
    if not summary_files:
        content += "No daily summaries found yet.\n\n"
    else:
        # Add links to recent summaries
        for filename in summary_files[:10]:  # Show last 10 summaries
            date_str = extract_date_from_filename(filename)
            if date_str:
                display_date = format_date_for_display(date_str)
                day_counter = calculate_day_counter(date_str, start_date_str)
                stats = get_file_stats(filename)
                
                # Create status indicator
                if stats['has_content']:
                    status = "📝"
                else:
                    status = "📄"
                
                content += f"- {status} [{display_date}{day_counter}]({filename})"
                
                # Add stats if file has content
                if stats['has_content']:
                    content += f" ({stats['word_count']} words)"
                
                content += "\n"
        
        if len(summary_files) > 10:
            content += f"\n... and {len(summary_files) - 10} more summaries\n"
    
    # Add missing summaries section
    content += generate_missing_summaries_section(summary_files)
    
    # Add footer
    content += """
## How to Use

1. **Create a new daily summary**: Run `python create_daily_summary.py` to create today's summary file
2. **Create for a specific date**: Run `python create_daily_summary.py 2024-01-15`
3. **Create with start date**: Run `python create_daily_summary.py --start-date 2024-01-01`
4. **Edit the summary**: Open the generated file in `Summary/` directory and fill in your daily progress
5. **Automatic README updates**: The README will be automatically updated when you push changes to the Summary directory

## Template Structure

Each daily summary includes:
- Today's completed work
- Issues encountered
- Solutions
- Tomorrow's plan
- Study notes
- Other records

---
*Last updated: {datetime}*
""".format(datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    return content

def main():
    """Main function to update README"""
    try:
        # Generate new content
        new_content = generate_readme_content()
        
        # Write to README.md
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("Successfully updated README.md")
        
    except Exception as e:
        print(f"Error updating README: {e}")
        exit(1)

if __name__ == '__main__':
    main() 