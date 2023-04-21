mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"yvannbarbotts@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
\n\
[theme]\n\
base = \"light\"\n\
backgroundColor = \"#FFF1F9\"\n\
secondaryBackgroundColor = \"#FFDCF1\"\n\
" > ~/.streamlit/config.toml
