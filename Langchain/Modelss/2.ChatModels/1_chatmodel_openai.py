from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(model="gpt-4",temperature=1.5,max_completion_tokens=4)

resp = chat.invoke("What is the capital of india?")
print(resp.content)
