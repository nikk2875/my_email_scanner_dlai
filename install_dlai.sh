#!/bin/bash

# Define the directory where the script will be installed
BASE_SCRIPT_DIR="/home/nikk/MyApps" # set your preferred folder or leave blank for current
if [ -z "$BASE_SCRIPT_DIR" ]; then # set to current if blank
    echo "DEST_DIR is empty. Setting to current folder."
    BASE_SCRIPT_DIR="`pwd`"
fi
SCRIPT_DIR="$BASE_SCRIPT_DIR/My_Email_Scanner_DLAI" # final target includes app

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 could not be found. Please install Python3 first."
    exit 1
fi

# Create target folder
if [[ ! -d "$SCRIPT_DIR" ]]; then
    echo "Directory $SCRIPT_DIR does not exist. Creating directory..."
    mkdir -p $SCRIPT_DIR
else
    echo "Directory $SCRIPT_DIR exists."
fi

# Copy Python code and shell script to target folders
cp ./dlai_scan.py $SCRIPT_DIR/
cp ./dlai_config.py $SCRIPT_DIR/
cp ./dlai_scanner.py $SCRIPT_DIR/
cp ./dlai_summarizer.py $SCRIPT_DIR/
cp ./.env $SCRIPT_DIR/
cp ./run_dlai.sh $BASE_SCRIPT_DIR/

# Copy UV files and sync
cp ./pyproject.toml $SCRIPT_DIR/
cp ./uv.lock $SCRIPT_DIR/
cd $SCRIPT_DIR/
uv sync
mkdir $SCRIPT_DIR/output
echo "Installation complete."
