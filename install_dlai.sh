#!/bin/bash

# Define the directory where the script will be installed
BASE_SCRIPT_DIR="/home/nikk/MyApps" # set your preferred folder or leave blank for current
if [ -z "$BASE_SCRIPT_DIR" ]; then # set to current if blank
    echo "DEST_DIR is empty. Setting to current folder."
    BASE_SCRIPT_DIR="`pwd`"
fi
SCRIPT_DIR="$BASE_SCRIPT_DIR/My_Email_Scanner_DLAI" # final target includes app

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 could not be found. Please install Python3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "pip is not installed. Please install pip first."
    exit 1
fi

# Check if virtualenv is installed
if ! python3 -m pip show virtualenv &> /dev/null; then
    echo "virtualenv is not installed. Please install virtualenv first."
    exit 1
fi

# Create target folder
if [[ ! -d "$SCRIPT_DIR" ]]; then
    echo "Directory $SCRIPT_DIR does not exist. Creating directory..."
    mkdir -p $SCRIPT_DIR
else
    echo "Directory $SCRIPT_DIR exists."
fi

# Create virtual environment
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Creating virtual environment in $SCRIPT_DIR/venv"
    python3 -m virtualenv "$SCRIPT_DIR/venv"
 else
    echo "Virtual environment already exists in $SCRIPT_DIR/venv"
fi

# Activate the virtual environment and install dependencies
echo "Installing dependencies from requirements.txt"
source "$SCRIPT_DIR/venv/bin/activate"
pip install -r requirements.txt

# Move Python code to target folder
cp ./dlai_scan.py $SCRIPT_DIR/
cp ./dlai_config.py $SCRIPT_DIR/
cp ./dlai_scanner.py $SCRIPT_DIR/
cp ./dlai_summarizer.py $SCRIPT_DIR/
cp ./.env $SCRIPT_DIR/
cp ./run_dlai.sh $BASE_SCRIPT_DIR/
mkdir $SCRIPT_DIR/output
echo "Installation complete."