#### `pleaseee add a star⭐️ to this repo if you like it, so I can keep improving it for free ((:`
---
# Robby-chatbot 🤖



### An AI chatbot featuring conversational memory, designed to enable users to discuss their CSV, PDF, TXT data and YouTube videos in a more intuitive manner. 🚀

#### *I'm currently working on making AI useful for geospatial -> building [TerraLab](https://www.terra-lab.ai/) with my dad and best friend, come take a look hehe*

![Robby](robby-pic.png)
Robby the Robot from [Forbidden Planet](https://youtu.be/bflfQN_YsTM)

#### For better understanding, see my Medium article 🖖 : [Build a chat-bot over your CSV data](https://medium.com/@yvann-hub/build-a-chatbot-on-your-csv-data-with-langchain-and-openai-ed121f85f0cd)

## Features ✨

- **Robby-Chat**: Chat with your documents (PDF, TXT, CSV) using vector embeddings and conversational memory
- **Robby-Sheet**: Analyze tabular data with natural language using PandasAI
- **Robby-Youtube**: Summarize YouTube videos using AI

## Tech Stack 🛠️

- **[LangChain](https://github.com/langchain-ai/langchain)** - LLM orchestration framework
- **[OpenAI](https://platform.openai.com/docs/models)** - GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-3.5-turbo
- **[PandasAI](https://github.com/sinaptik-ai/pandas-ai)** - Natural language data analysis
- **[Streamlit](https://github.com/streamlit/streamlit)** - Web application framework
- **[FAISS](https://github.com/facebookresearch/faiss)** - Vector similarity search

## Running Locally 💻

Follow these steps to set up and run the service locally:

### Prerequisites
- Python 3.10 or higher
- Git
- OpenAI API key

### Installation

Clone the repository:

```bash
git clone https://github.com/yvann-hub/Robby-chatbot.git
```

Navigate to the project directory:

```bash
cd Robby-chatbot
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Launch the chat service locally:

```bash
streamlit run src/Home.py
```

### Environment Variables (Optional)

You can set your OpenAI API key as an environment variable instead of entering it in the UI:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or create a `.env` file in the project root:

```
OPENAI_API_KEY=your-api-key-here
```

#### That's it! The service is now up and running locally. 🤗

## Models Available 🤖

- **GPT-4o-mini** - Fast and cost-effective (default)
- **GPT-4o** - Most capable model
- **GPT-4-turbo** - Balanced performance
- **GPT-3.5-turbo** - Legacy model

## Contributing 🙌
If you want to contribute to this project, please open an issue, submit a pull request or contact me at barbot.yvann@gmail.com (:
