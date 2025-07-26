#!/bin/bash
set -e

# Step 1: Run your setup command
echo "Running setup step..."
python agent.py download-files

python gradio_assistant.py

# Step 2: Start your main process
# echo "Starting watchmedo..."
# exec watchmedo auto-restart --directory=. --pattern=agent.py --recursive -- python agent.py console
