#!/bin/bash

# Set the target directory where the .streamlit directory will be created
target_directory="$PWD"

# Create the .streamlit directory if it doesn't exist in the current directory
mkdir -p "$target_directory/.streamlit/"

# Create the credentials.toml file
cat > "$target_directory/.streamlit/credentials.toml" <<EOL
[general]
email = "yvannbarbotts@gmail.com"
EOL

# Create the config.toml file
cat > "$target_directory/.streamlit/config.toml" <<EOL
[server]
headless = true
enableCORS = false
port = \$PORT

[theme]
base = "light"
primaryColor = "#89CFF0"
backgroundColor = "#E0F7FE"
secondaryBackgroundColor = "#FFFCE4"
textColor = "#000000"
font = "sans serif"
EOL

# Provide a message indicating that the files were successfully created
echo "Configuration files have been created in the current directory: $target_directory/.streamlit/"
