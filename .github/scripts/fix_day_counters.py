#!/usr/bin/env python3
"""
Script to validate and fix day counters in summary files
Checks if day counters match the current START_DATE configuration
"""

import os
import glob
import re
from datetime import datetime
import sys

def get_current_start_date():
    """Get the current start date from config"""
    try:
        import sys
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        from config import START_DATE
        return START_DATE
    except ImportError:
        return None

def calculate_correct_day_counter(date_str, start_date_str):
    """Calculate the correct day counter for a given date"""
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

def extract_date_from_filename(filename):
    """Extract date from filename"""
    basename = os.path.basename(filename)
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})\.md$', basename)
    return date_match.group(1) if date_match else None

def extract_current_day_counter(content):
    """Extract current day counter from file content"""
    # Look for pattern: # Daily Summary - YYYY-MM-DD [Day XXX]
    match = re.search(r'# Daily Summary - \d{4}-\d{2}-\d{2} \[Day (\d+)\]', content)
    if match:
        return match.group(1)
    # If no day counter found, return "None" to indicate missing
    return "None"

def fix_day_counter_in_file(filepath, correct_day_counter):
    """Fix the day counter in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the title line with correct day counter
        if correct_day_counter:
            # First try to replace existing day counter
            new_content = re.sub(
                r'(# Daily Summary - \d{4}-\d{2}-\d{2}) \[Day \d+\]',
                r'\1' + correct_day_counter,
                content
            )
            
            # If no change, try to add day counter to title without one
            if new_content == content:
                new_content = re.sub(
                    r'(# Daily Summary - \d{4}-\d{2}-\d{2})',
                    r'\1' + correct_day_counter,
                    content
                )
        else:
            # Remove day counter if not needed
            new_content = re.sub(
                r'(# Daily Summary - \d{4}-\d{2}-\d{2}) \[Day \d+\]',
                r'\1',
                content
            )
        
        # Only write if content changed
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error fixing file {filepath}: {e}")
        return False

def validate_and_fix_day_counters():
    """Validate and fix day counters in all summary files"""
    start_date_str = get_current_start_date()
    
    if not start_date_str:
        print("No START_DATE configured. Skipping day counter validation.")
        return
    
    print(f"Validating day counters with START_DATE: {start_date_str}")
    
    # Get all summary files
    summary_files = glob.glob('Summary/*.md')
    if not summary_files:
        print("No summary files found.")
        return
    
    fixed_files = []
    issues_found = []
    
    for filepath in summary_files:
        date_str = extract_date_from_filename(filepath)
        if not date_str:
            continue
        
        # Calculate correct day counter
        correct_day_counter = calculate_correct_day_counter(date_str, start_date_str)
        
        # Read current file content
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            continue
        
        # Extract current day counter
        current_day_counter = extract_current_day_counter(content)
        
        # Determine what the correct day counter should be
        expected_day_counter = correct_day_counter.replace(" [Day ", "").replace("]", "") if correct_day_counter else "None"
        
        if current_day_counter != expected_day_counter:
            issues_found.append({
                'file': filepath,
                'date': date_str,
                'current': current_day_counter,
                'expected': expected_day_counter
            })
            
            # Fix the file
            if fix_day_counter_in_file(filepath, correct_day_counter):
                fixed_files.append(filepath)
                print(f"✅ Fixed {filepath}: Day {current_day_counter} → Day {expected_day_counter}")
    
    # Summary
    if issues_found:
        print(f"\n📊 Summary:")
        print(f"   - Files with incorrect day counters: {len(issues_found)}")
        for issue in issues_found:
            print(f"     - {issue['file']}: Day {issue['current']} → Day {issue['expected']}")
        print(f"   - Files fixed: {len(fixed_files)}")
        
        if fixed_files:
            print(f"\n✅ Successfully fixed day counters in {len(fixed_files)} files.")
            return True
        else:
            print(f"\n❌ Failed to fix some files.")
            return False
    else:
        print(f"\n✅ All day counters are correct!")
        return True

def main():
    """Main function"""
    try:
        success = validate_and_fix_day_counters()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 