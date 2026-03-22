#!/bin/bash

# Define the directory where the script will be installed
SCRIPT_DIR="/home/nikk/MyApps" # set your preferred folder or leave blank for current
if [ -z "$SCRIPT_DIR" ]; then # set to current if blank
    echo "DEST_DIR is empty. Setting to current folder."
    SCRIPT_DIR="`pwd`"
fi
SCRIPT_DIR="$SCRIPT_DIR/My_Email_Scanner_DLAI" # final target folder of the app

# Check if virtual environment exists
VENV_PATH="$SCRIPT_DIR/venv"
if [ ! -d "$VENV_PATH" ]; then
    echo "Error: Virtual environment not found. Please run install.sh first."
    exit 1
fi

# Activate the virtual environment
echo "Starting chatbot using virtual environment from $VENV_PATH"
source "$VENV_PATH/bin/activate"

# Run the Python script
cd $SCRIPT_DIR
PYTHON_SCRIPT="$SCRIPT_DIR/dlai_scan.py"
echo "Running $PYTHON_SCRIPT..."
python "$PYTHON_SCRIPT"

# Deactivate the virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Virtual environment was not activated properly."
else
    deactivate
    echo "Virtual environment deactivated."
fi