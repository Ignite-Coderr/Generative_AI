from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Give me the 5 pointer summary of the following text {text}',
    input_variables=['text']
)

model = ChatOpenAI()

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

output = chain.invoke({'topic':'Unemployment in india'})

print(output)

chain.get_graph().print_ascii()
