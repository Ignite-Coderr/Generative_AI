from langchain_core.messages import HumanMessageChunk
import streamlit as st
from langgraph_backend import chatbot, llm
from langchain_core.messages import HumanMessage
import uuid

# Utility Function
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_convo(thread_id):
    return chatbot.get_state(config={'configurable':{'thread_id':thread_id}}).values.get('messages', [])

def generate_thread_name(user_message):
    """Use the LLM to generate a short conversation title from the first user message."""
    response = llm.invoke(f"Generate a very short title (max 5 words) for a conversation that starts with: '{user_message}'. Reply with ONLY the title, no quotes or punctuation.")
    return response.content.strip()

# st.session_state -> dict -> 
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

if 'thread_names' not in st.session_state:
    st.session_state['thread_names'] = {}

add_thread(st.session_state['thread_id'])

# Sidebar
st.sidebar.title("Langgraph Chatbot")
if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Conversations")

for thread_id in st.session_state['chat_threads'][::-1]:
    display_name = st.session_state['thread_names'].get(str(thread_id), 'New Chat')
    if st.sidebar.button(display_name, key=str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_convo(thread_id)

        temp_messages = []
        for msg in messages:
            if isinstance(msg,HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_messages.append({'role':role,'content':msg.content})
        st.session_state['message_history'] = temp_messages

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

#{'role': 'user', 'content': 'Hi'}
#{'role': 'assistant', 'content': 'Hi=ello'}

user_input = st.chat_input('Type here')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    config = {'configurable': {'thread_id': st.session_state['thread_id']}}

    # first add the message to message_history
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= config,
                stream_mode= 'messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

    # Generate a thread name from the first message if not already named
    tid = str(st.session_state['thread_id'])
    if tid not in st.session_state['thread_names']:
        st.session_state['thread_names'][tid] = generate_thread_name(user_input)
        st.rerun()