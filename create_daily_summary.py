#!/usr/bin/env python3
"""
Script to create daily summary files from template
Usage: python create_daily_summary.py [date]
If no date is provided, uses today's date
"""

import os
import sys
from datetime import datetime
import argparse

def create_daily_summary(date_str=None, start_date_str=None):
    """Create a daily summary file for the specified date"""
    
    # Determine the date
    if date_str:
        try:
            # Parse the provided date string (expected format: YYYY-MM-DD)
            target_date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            print(f"Error: Invalid date format. Please use YYYY-MM-DD format.")
            return False
    else:
        target_date = datetime.now()
    
    # Get start date from config if not provided
    if not start_date_str:
        try:
            from config import START_DATE
            start_date_str = START_DATE
        except ImportError:
            start_date_str = None
    
    # Calculate day counter if start date is provided
    day_counter = ""
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            days_diff = (target_date - start_date).days
            if days_diff >= 0:
                day_counter = f" [Day {days_diff + 1}]"
        except ValueError:
            print(f"Warning: Invalid start date format. Please use YYYY-MM-DD format.")
    
    # Format date for filename and content
    date_filename = target_date.strftime('%Y-%m-%d')
    date_content = target_date.strftime('%Y-%m-%d')
    datetime_content = target_date.strftime('%Y-%m-%d %H:%M:%S')
    
    # Define file paths
    template_path = 'template.md'
    output_path = f'Summary/{date_filename}.md'
    
    # Check if template exists
    if not os.path.exists(template_path):
        print(f"Error: Template file '{template_path}' not found.")
        return False
    
    # Check if output file already exists
    if os.path.exists(output_path):
        print(f"Warning: File '{output_path}' already exists. Skipping creation.")
        return False
    
    # Create Summary directory if it doesn't exist
    os.makedirs('Summary', exist_ok=True)
    
    # Read template and replace placeholders
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace placeholders
        content = content.replace('{{DATE}}', date_content)
        content = content.replace('{{DATETIME}}', datetime_content)
        content = content.replace('{{DAY_COUNTER}}', day_counter)
        
        # Write the new file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Successfully created daily summary: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error creating file: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Create daily summary file from template')
    parser.add_argument('date', nargs='?', help='Date in YYYY-MM-DD format (default: today)')
    parser.add_argument('--start-date', help='Start date in YYYY-MM-DD format for day counting')
    
    args = parser.parse_args()
    
    success = create_daily_summary(args.date, args.start_date)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 