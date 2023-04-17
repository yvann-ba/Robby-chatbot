#!/bin/bash

delimiters="------------------------------------------------------------"

echo $delimiters
echo "Launching 🚀"
echo $delimiters

# Get current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create virtualenv
if [ ! -d "$DIR/venv" ]; then
    python3 -m venv $DIR/venv
    echo $delimiters
    echo "Virtualenv created"
    echo $delimiters
fi

# Activate env
source $DIR/venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r $DIR/requirements.txt

# Run program
streamlit run $DIR/chatbot_csv.py

# Deactivate virtualenv
deactivate

echo $delimiters
echo "See you soon 👋"
echo $delimiters