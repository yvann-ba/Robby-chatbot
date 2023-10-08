#!/bin/bash

# Create the .streamlit directory if it doesn't exist
mkdir -p ./.streamlit/

# Create the credentials.toml file
cat > ./.streamlit/credentials.toml <<EOL
[general]
email = "yvannbarbotts@gmail.com"
EOL

# Create the config.toml file
cat > ./.streamlit/config.toml <<EOL
[server]
headless = true
enableCORS = false
port = $PORT

[theme]
base = "light"
primaryColor = "#89CFF0"
backgroundColor = "#E0F7FE"
secondaryBackgroundColor = "#FFFCE4"
textColor = "#000000"
font = "sans serif"
EOL
