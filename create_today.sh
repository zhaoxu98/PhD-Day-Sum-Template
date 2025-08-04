#!/bin/bash

# Script to create today's daily summary
# Usage: ./create_today.sh [start_date]
# Example: ./create_today.sh 2024-01-01

echo "Creating today's daily summary..."

# Check if start date is provided
if [ $# -eq 1 ]; then
    echo "Using start date: $1"
    python3 create_daily_summary.py --start-date "$1"
else
    python3 create_daily_summary.py
fi

# Check if the script was successful
if [ $? -eq 0 ]; then
    echo "✅ Daily summary created successfully!"
    echo "📝 Edit the file in the Summary/ directory to add your content."
else
    echo "❌ Failed to create daily summary."
    exit 1
fi 