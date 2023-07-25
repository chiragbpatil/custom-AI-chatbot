# https://github.com/marshmellow77/streamlit-chatgpt-ui


import streamlit as st
from streamlit_chat import message
from model import get_response

# Setting page title and header
st.set_page_config(page_title="Chatbot")
st.markdown("<h1 style='text-align: center;'>Custom AI Chatbot </h1>",
            unsafe_allow_html=True)


# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

clear_button = st.sidebar.button("Clear Conversation", key="clear")

# reset everything
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# container for chat history
response_container = st.container()

# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100,)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        response = get_response(user_input)
        st.session_state['messages'].append(
            {"role": "assistant", "content": response})
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(response['answer'])


if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i],
                    is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
