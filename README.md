# Robby-chatbot 🤖

### An AI chatbot featuring conversational memory, designed to enable users to discuss their CSV and PDF data in a more intuitive manner. 📄
![Robby](robby-pic.png)
Robby the Robot from [Forbidden Planet](https://youtu.be/bflfQN_YsTM)

#### By integrating the strengths of Langchain and OpenAI, Robby-chatbot employs large language models to provide users with seamless, context-aware natural language interactions for a better understanding of their PDF and CSV data.🧠
#### For better understanding, see my medium article 🖖 : [Build a chat-bot over your CSV data](https://medium.com/@yvann-ba/build-a-chatbot-on-your-csv-data-with-langchain-and-openai-ed121f85f0cd)
## Quick Start 🚀
To use Robby-chatbot, simply visit the following link :

### [robby-chatbot.com](https://robby-chatbot.com)

### TO-DO :
- [x] enable print tokens utilizations for the conversation
- [x] Chatbot on PDF files (I need to change the name of the repo haha)
- [ ] Add lots of files accepted like GitHub repo, Excel etc...
- [ ] Add free models like vicuna and free embeddings
- [ ] Replace chain of the chatbot by a custom agent for handling more features ans ask questions about all informations of the files + memory + vectorstore

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

`streamlit run src/robby_chatbot.py`

#### That's it! The service is now up and running locally. 🤗

Robby-chatbot contains a chatbot with memory for differents types of files and a CSV-agent, both based on a given file. The chatbot discusses the elements of the file with the user in a user-friendly way from a vectorstore (max. 4 indexes at a time). 

Example of a chatbot:
Q: A restaurant in New York?
A: Try Tower Restaurant, a la carte menu and specials on Tuesdays. Contact: 0654589874.

The CSV Agent analyses the content and structure of the CSV without vectostore and answers questions in a factual manner. It requires clear and precise instructions and has no memory.

Example of a CSV agent:
Q: Square root of the average age?
A: 5.449689683556195

## Contributing 🙌
Contributions are always welcome! If you want to contribute to this project, please open an issue, submit a pull request or contact me at barbot.yvann@gmail.com (:


