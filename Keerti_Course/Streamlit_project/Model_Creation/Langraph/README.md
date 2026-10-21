# LangGraph Euri Chatbot Example

This project demonstrates how to build a stateful conversational chatbot using LangChain, LangGraph, and the Euri API, with optional integration of Tavily for web search and LangSmith for experiment tracking.

## Project Structure
- **practice.ipynb**: Main notebook containing all code and explanations for building and running the chatbot.
- **.env**: Environment variables for API keys (GROQ, LangSmith, Tavily, etc.).

## Key Sections in the Notebook

### 1. Project Overview (Markdown Cell 1)
Describes the goal: a stateful CLI chatbot that remembers conversation, logs to LangSmith, and can answer recent/time-based questions using a search tool.

### 2. Architecture Diagram (Markdown Cells 2-4)
Visualizes the flow: User → LangGraph (state machine) → Conversation Memory → LLM (Euri API) → Tool (Tavily Search) → LangSmith (logging).

### 3. Environment Setup (Cell 5)
- Loads environment variables from `.env`.
- Installs required libraries: `langchain`, `langgraph`, `langsmith`, `langchain-community`, `tavily-python`, `python-dotenv`.

### 4. API Keys and Configuration
- **GROQ_API_KEY**: (Legacy, not used in Euri version)
- **LANGCHAIN_API_KEY**: For LangSmith experiment tracking.
- **TAVILY_API_KEY**: For Tavily web search tool (see below).

### 5. Euri API Integration (Cells 6, 7, 8)
- Defines the Euri API endpoint and token.
- Implements `euri_chat()` to send conversation history and get responses from Euri's LLM (e.g., `gpt-4.1-nano`).
- Handles message formatting and response parsing.

### 6. Conversation State (Cell 9)
Defines a `ChatState` class to maintain the full conversation history, enabling memory across turns.

### 7. Interactive CLI Chat (Cell 10)
- Runs a loop where the user can type questions.
- Each user message is appended to the conversation state.
- The Euri API is called with the full message history.
- The assistant's reply is printed and added to the state.

## Why These Technologies?

### LangChain
LangChain is a framework for developing applications powered by language models. It provides abstractions for LLMs, memory, tools, and agents, making it easy to build complex conversational systems.

### LangGraph
LangGraph is a state machine framework for orchestrating multi-step, stateful workflows in conversational AI. It allows you to define nodes (steps) and edges (transitions) for advanced control over conversation flow and memory.

### Tavily (TAVILY_API_KEY)
Tavily provides a web search API that can be used as a tool in your agent. By including your `TAVILY_API_KEY` in the `.env` file, you enable your chatbot to answer questions about current events or recent information by searching the web.

### LangSmith
LangSmith is a platform for experiment tracking, debugging, and evaluating LLM applications. By setting `LANGCHAIN_API_KEY` and related variables, all prompts, responses, and token usage are logged for later analysis and improvement.

## How to Use
1. **Set up your `.env` file** with the required API keys (Euri, Tavily, LangSmith).
2. **Run the notebook** (`practice.ipynb`).
3. **Interact with the chatbot** in the CLI. Type your questions; the bot will remember context and use the Euri API for responses.
4. **(Optional) Enable Tavily** by providing a valid `TAVILY_API_KEY` to allow web search.
5. **(Optional) Use LangSmith** for experiment tracking by providing a valid `LANGCHAIN_API_KEY`.

## Notes
- The Euri API is used as the LLM backend. You can swap in other LLM providers by changing the API call logic.
- The chatbot is CLI-based for simplicity, but you can adapt it for web or other interfaces.
- All code is structured in XML-based notebook cells for compatibility with VSCode and LangChain workflows.

---

For more details, see the comments and markdown explanations in each section of `practice.ipynb`.
