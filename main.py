import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables 
load_dotenv()

# Configure Streamlit page setting 
st.set_page_config(
    page_title="Hello there!)",
    page_icon="heart:",     # An emoji for the icon
    layout="centered"       # Page layout 
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Setting up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Creating a function to translate roles between Gemini-Pro and Streamlit terminology 
def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return 'assistant'
    else:
        return user_role

# Initilaizing chat session in Streamlit if not already present 
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot title on the page 
st.title('Chat with me :)')

# Display the chat history 
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message 
user_prompt = st.chat_input('Ask me anything darling...')
if user_prompt:
    # Adding the message to the chat and displaying it 
    st.chat_message('❤️').markdown(user_prompt)

    # Prepend the tender instruction to the user's message
    tender_prompt = "Respond tenderly and sweetly, as if you are talking to your lover whose name is Shamim and be poetic and make love to her as much as you can: " + user_prompt

    # Send the message to Gemini-Pro to get the answer
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Geminin-pro's response
    with st.chat_message('assistant'):
        st.markdown(gemini_response.text)

