# ChatBot-CSV 🤖

### An AI chatbot featuring conversational memory, designed to enable users to discuss their CSV data in a more intuitive manner. 📄
By integrating the strengths of Langchain and OpenAI, ChatBot-CSV employs large language models to provide users with seamless, context-aware natural language interactions for a better understanding of their CSV data.🧠
#### For better understanding, see my medium article 🖖 : [Build a chat-bot over your CSV data](https://medium.com/@yvann-ba/build-a-chatbot-on-your-csv-data-with-langchain-and-openai-ed121f85f0cd)
## Quick Start 🚀
To use ChatBot-CSV, simply visit the following link :

### [chatbot-csv.com](https://chatbot-csv.com/)

### TO-DO :
- [x] print tokens utilizations for the conversation
- [ ] Replace chain of the chatbot by a custom agent for handling more features ans ask questions about all informations of the files + memory + vectorstore
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

## Information 📝:
ChatBot-CSV features a chatbot with memory and a CSV agent. The chatbot is specialized in discussing unique elements within the CSV with the user in a friendly and conversational manner (limited to about 4 rows at a time due to the nature of the ConversationalRetrievalChain). It is more suitable for a use case where a company uses a CSV to feed their chatbot, so it can answer questions from a user seeking information without necessarily knowing the data behind the chatbot. You can modify the prompt template in the code to customize the chatbot's response phrasing for your specific case.

Example:
Q: I'm looking for a restaurant in New York, what do you suggest?
A: You can try Tower Restaurant, which offers an à la carte menu and has promotions on Tuesdays. You can contact them at 0654589874 for more information.

The CSV Agent, on the other hand, executes Python to answer questions about the content and structure of the CSV. It requires precise questions about the data and provides factual answers. It is not limited to a specific number of rows and can analyze the entire file, but it needs clear and accurate instructions. It also doesn't have memory.

Example:
Q: What's the square root of the average age?
A: '5.449689683556195'

## Contributing 🙌
Contributions are always welcome! If you want to contribute to this project, please open an issue, submit a pull request or contact me at barbot.yvann@gmail.com (:


