from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI()

messages = [
    SystemMessage(content='You are a helpful assitant'),
    HumanMessage(content="Tell me about Python"),
]

response = model.invoke(messages)
messages.append(AIMessage(content=response.content))

print(messages)