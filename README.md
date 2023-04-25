# ChatBot-CSV 🤖

### An AI chatbot featuring conversational memory, designed to enable users to discuss their CSV data in a more intuitive manner. 📄
By integrating the strengths of Langchain and OpenAI, ChatBot-CSV employs large language models to provide users with seamless, context-aware natural language interactions for a better understanding of their CSV data.🧠
#### For better understanding, see my medium article 🖖 : [Build a chat-bot over your CSV data](https://medium.com/@yvann-ba/build-a-chatbot-on-your-csv-data-with-langchain-and-openai-ed121f85f0cd)
## Quick Start 🚀
To use ChatBot-CSV, simply visit the following link :

### [chatbot-csv.com](https://chatbot-csv.com/)

## Task List 📝:
- [x] Implementation of CSV agent (enable precises responses on the csv file structure)
- [ ] Custom prompt for the chatbot (let the user choose the behavior of the chatbot)
- [ ] Rebuild the site in typescript instead of streamlit
- [ ] add a database and a login for the user to have a permanent chatbot on these csv data
## Running Locally 💻
Follow these steps to set up and run the service locally :

### Prerequisites
- Python 3.8 or higher
- Git

### Installation
Clone the repository :

`git clone https://github.com/yvann-hub/ChatBot-CSV.git`


Navigate to the project directory :

`cd ChatBot-CSV`


Create a virtual environment :
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

Install the required dependencies in the virtual environment :

`pip install -r requirements.txt`


Launch the chat service locally :

`streamlit run src/chatbot_csv.py`

#### That's it! The service is now up and running locally. 🤗

## Contributing 🙌
Contributions are always welcome! If you want to contribute to this project, please open an issue, submit a pull request or contact me at barbot.yvann@gmail.com (:


