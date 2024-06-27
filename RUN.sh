#!/bin/bash
source bin/activate
echo "Starting script from directory: $(pwd)"
python src/main.py
echo "Script execution completed."
deactivate