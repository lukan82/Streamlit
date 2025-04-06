import streamlit as st
import httpx
from openai import OpenAI
import time

# ----- Config -----
KEY_TIMEOUT_MINUTES = 4

st.set_page_config(page_title="Custom GPT App", page_icon="🤖")

st.title("🤖 Ask GPT Anything")
st.markdown("Talk to a custom GPT assistant!")

# Sidebar title
st.sidebar.title("🔐 API Configuration")

# Initialize session state variables
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "api_key_timestamp" not in st.session_state:
    st.session_state.api_key_timestamp = 0

# Timeout check
current_time = time.time()
elapsed_minutes = (current_time - st.session_state.api_key_timestamp) / 60

# Invalidate key after timeout
if st.session_state.api_key and elapsed_minutes > KEY_TIMEOUT_MINUTES:
    st.warning("Your session has expired for security reasons. Please re-enter your API key.")
    st.session_state.api_key = ""
    st.session_state.api_key_timestamp = 0

# Ask for API key
api_key = st.sidebar.text_input(
    "Enter your OpenAI API key",
    type="password",
    value=st.session_state.api_key,
    help="Used only for this session. Never stored or logged."
)

# If key is entered or updated, reset the timer
if api_key and api_key != st.session_state.api_key:
    st.session_state.api_key = api_key
    st.session_state.api_key_timestamp = time.time()

# If key is valid, proceed with app logic
if st.session_state.api_key:
    model = st.sidebar.selectbox("Choose a model:", ["gpt-3.5-turbo", "gpt-4"])

    httpx_client = httpx.Client(verify=False)
    client = OpenAI(api_key=st.session_state.api_key, http_client=httpx_client)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    user_input = st.chat_input("Ask me something...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=st.session_state.messages,
                    )
                    reply = response.choices[0].message.content
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"⚠️ An error occurred: {str(e)}")
else:
    st.info("Please enter your OpenAI API key in the sidebar to begin.")
