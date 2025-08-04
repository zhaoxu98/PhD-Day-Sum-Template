#!/usr/bin/env python3
"""
Script to update README.md with links to daily summary files
"""

import os
import glob
from datetime import datetime
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

def generate_readme_content():
    """Generate the complete README content"""
    
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
                stats = get_file_stats(filename)
                
                # Create status indicator
                if stats['has_content']:
                    status = "📝"
                else:
                    status = "📄"
                
                content += f"- {status} [{display_date}]({filename})"
                
                # Add stats if file has content
                if stats['has_content']:
                    content += f" ({stats['word_count']} words)"
                
                content += "\n"
        
        if len(summary_files) > 10:
            content += f"\n... and {len(summary_files) - 10} more summaries\n"
    
    # Add footer
    content += """
## How to Use

1. **Create a new daily summary**: Run `python create_daily_summary.py` to create today's summary file
2. **Create for a specific date**: Run `python create_daily_summary.py 2024-01-15`
3. **Edit the summary**: Open the generated file in `Summary/` directory and fill in your daily progress
4. **Automatic README updates**: The README will be automatically updated when you push changes to the Summary directory

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