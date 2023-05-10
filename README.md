# Robby-chatbot 🤖

[![Twitter Follow](https://img.shields.io/twitter/follow/yvann_hub?style=social)](https://twitter.com/yvann_hub)
[![Last Commit](https://img.shields.io/github/last-commit/yvann-hub/Robby-chatbot)](https://github.com/yvann-hub/Robby-chatbot/commits/main)


### An AI chatbot featuring conversational memory, designed to enable users to discuss their CSV, PDF and TXT data in a more intuitive manner. 📄
![Robby](robby-pic.png)
Robby the Robot from [Forbidden Planet](https://youtu.be/bflfQN_YsTM)

By integrating the strengths of Langchain and OpenAI, Robby employs large language models to provide users with seamless, 
context-aware natural language interactions for a better understanding of their data.🧠
#### For better understanding, see my medium article 🖖 : [Build a chat-bot over your CSV data](https://medium.com/@yvann-hub/build-a-chatbot-on-your-csv-data-with-langchain-and-openai-ed121f85f0cd)
## Quick Start 🚀

[![Robby-Chatbot](https://img.shields.io/static/v1?label=Robby-Chatbot&message=Visit%20Website&color=ffffff&labelColor=ADD8E6&style=for-the-badge)](https://robby-chatbot.com)

## TO-DO :
- [x] enable print tokens utilizations for the conversation
- [x] Use CSV Agent for chat with the entire csv file
- [ ] Add lots of files accepted like GitHub repo, Excel etc...
- [ ] Add free models like vicuna and free embeddings
- [ ] Replace chain of the chatbot by a custom agent for handling more features | memory + vectorstore + custom prompt

## Running Locally 💻
Follow these steps to set up and run the service locally :

### Prerequisites
- Python 3.8 or higher
- Git

### Installation
Clone the repository :

`git clone https://github.com/yvann-hub/Robby-chatbot.git`


Navigate to the project directory :

`cd Robby-chatbot`


Create a virtual environment :
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

Install the required dependencies in the virtual environment :

`pip install -r requirements.txt`


Launch the chat service locally :

`streamlit run src/Home.py`

#### That's it! The service is now up and running locally. 🤗

## Contributing 🙌
Contributions are always welcome! If you want to contribute to this project, please open an issue, submit a pull request or contact me at barbot.yvann@gmail.com (:


