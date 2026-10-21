from langchain_core.messages import HumanMessage
import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# st.session -> dict ->
config = {'configurable':{'thread_id':'thread-1'}}
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Loading the convo history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# {'role':'user','content':'Hi'}
# {'role':'assistant','content':'Hello'}
user_input = st.chat_input("Type Here")

if user_input:

    #first add the message to message history
    st.session_state['message_history'].append({'role':'user','content':user_input})

    #display the messages
    with st.chat_message("user", avatar="👤"):
        st.text(user_input)

    response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]},config=config)
    ai_message = response['messages'][-1].content

    st.session_state['message_history'].append({'role':'assistant','content':ai_message})
    with st.chat_message("assistant", avatar="🤖"): 
        st.text(ai_message)
    

