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

def create_daily_summary(date_str=None):
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
    
    args = parser.parse_args()
    
    success = create_daily_summary(args.date)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 