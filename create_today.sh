#!/bin/bash

# Script to create today's daily summary
# Usage: ./create_today.sh

echo "Creating today's daily summary..."

# Run the Python script
python3 create_daily_summary.py

# Check if the script was successful
if [ $? -eq 0 ]; then
    echo "✅ Daily summary created successfully!"
    echo "📝 Edit the file in the Summary/ directory to add your content."
else
    echo "❌ Failed to create daily summary."
    exit 1
fi 