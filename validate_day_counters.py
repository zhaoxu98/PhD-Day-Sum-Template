#!/usr/bin/env python3
"""
Standalone script to validate day counters in summary files
Run this script to check and fix day counters manually
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

# Import the validation function
sys.path.append(os.path.join(os.path.dirname(__file__), '.github', 'scripts'))
from fix_day_counters import validate_and_fix_day_counters

def main():
    """Main function for standalone execution"""
    print("🔍 Day Counter Validation Tool")
    print("=" * 40)
    
    success = validate_and_fix_day_counters()
    
    if success:
        print("\n🎉 Validation completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Validation completed with errors.")
        sys.exit(1)

if __name__ == '__main__':
    main() 