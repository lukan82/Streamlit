import streamlit as st
import httpx
from openai import OpenAI

httpx_client = httpx.Client(verify=False)


# Initialize OpenAI client with API key
client = OpenAI(api_key="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",
                http_client=httpx_client
                 )                  # Replace with your actual key

st.set_page_config(page_title="Custom GPT App", page_icon="🤖")

st.title("🤖 Ask GPT Anything")
st.markdown("Talk to a custom GPT assistant!")

# Sidebar for settings
st.sidebar.title("Settings")
model = st.sidebar.selectbox("Choose a model:", ["gpt-3.5-turbo", "gpt-4"])

# Session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input from user
user_input = st.chat_input("Ask me something...")

if user_input:
    # Add user input to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate GPT response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    # Add GPT reply to history
