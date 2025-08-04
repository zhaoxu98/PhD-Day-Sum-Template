#!/usr/bin/env python3
"""
Script to create missing daily summary files
Usage: python create_missing_summaries.py [start_date] [end_date]
If no dates provided, uses the range from existing files
"""

import os
import sys
import glob
from datetime import datetime, timedelta
import re
from create_daily_summary import create_daily_summary

def get_existing_dates():
    """Get all existing summary dates"""
    summary_files = glob.glob('Summary/*.md')
    existing_dates = set()
    
    for filename in summary_files:
        basename = os.path.basename(filename)
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})\.md$', basename)
        if date_match:
            existing_dates.add(date_match.group(1))
    
    return existing_dates

def get_missing_dates(start_date_str=None, end_date_str=None):
    """Get missing dates in the specified range"""
    existing_dates = get_existing_dates()
    
    if not existing_dates:
        print("No existing summary files found.")
        return []
    
    # Determine date range
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD format.")
            return []
    else:
        # Use range from existing files
        sorted_dates = sorted(existing_dates)
        start_date = datetime.strptime(sorted_dates[0], '%Y-%m-%d')
        end_date = datetime.strptime(sorted_dates[-1], '%Y-%m-%d')
    
    # Generate all expected dates in the range
    expected_dates = set()
    current_date = start_date
    while current_date <= end_date:
        expected_dates.add(current_date.strftime('%Y-%m-%d'))
        current_date = current_date + timedelta(days=1)
    
    # Find missing dates
    missing_dates = sorted(expected_dates - existing_dates)
    return missing_dates

def create_missing_summaries(start_date_str=None, end_date_str=None, start_date_for_counter=None):
    """Create missing summary files"""
    missing_dates = get_missing_dates(start_date_str, end_date_str)
    
    if not missing_dates:
        print("No missing dates found in the specified range.")
        return
    
    print(f"Found {len(missing_dates)} missing dates:")
    for date in missing_dates:
        print(f"  - {date}")
    
    # Ask for confirmation
    response = input(f"\nCreate {len(missing_dates)} missing summary files? (y/N): ")
    if response.lower() != 'y':
        print("Operation cancelled.")
        return
    
    # Create missing summaries
    created_count = 0
    for date in missing_dates:
        print(f"Creating summary for {date}...")
        if create_daily_summary(date, start_date_for_counter):
            created_count += 1
        else:
            print(f"Failed to create summary for {date}")
    
    print(f"\n✅ Successfully created {created_count} out of {len(missing_dates)} missing summaries.")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Create missing daily summary files')
    parser.add_argument('start_date', nargs='?', help='Start date in YYYY-MM-DD format')
    parser.add_argument('end_date', nargs='?', help='End date in YYYY-MM-DD format')
    parser.add_argument('--start-date-counter', help='Start date for day counting in YYYY-MM-DD format')
    
    args = parser.parse_args()
    
    # Validate date arguments
    if args.start_date and not args.end_date:
        print("Error: If start_date is provided, end_date must also be provided.")
        sys.exit(1)
    
    if args.end_date and not args.start_date:
        print("Error: If end_date is provided, start_date must also be provided.")
        sys.exit(1)
    
    create_missing_summaries(args.start_date, args.end_date, args.start_date_counter)

if __name__ == '__main__':
    main() 