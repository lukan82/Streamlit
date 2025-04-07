import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

st.set_page_config(page_title="Ask Anything - Mini LLM", page_icon="❓")

@st.cache_resource
def load_model():
    model_name = "distilgpt2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

st.title("❓ Ask Anything - Lightweight LLM")
st.markdown("Ask a question or give a prompt. Powered by a tiny local model (`distilgpt2`).")

user_input = st.text_area("Your question:", placeholder="e.g. What’s the capital of Mars?")

if st.button("Get Answer"):
    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        input_ids = tokenizer.encode(user_input, return_tensors="pt")[:, :512]

        with st.spinner("Thinking..."):
            with torch.no_grad():
                output = model.generate(
                    input_ids,
                    max_length=input_ids.shape[1] + 100,  # ensure new tokens are added
                    do_sample=True,
                    top_k=50,
                    top_p=0.95,
                    temperature=0.7,
                    pad_token_id=tokenizer.eos_token_id  # avoids warning about no pad token
                )

        full_output = tokenizer.decode(output[0], skip_special_tokens=True)

        # Attempt to remove prompt from beginning, else fallback to full output
        if full_output.startswith(user_input):
            response = full_output[len(user_input):].strip()
        else:
            response = full_output.strip()

        st.markdown("### 🧠 Answer:")
        st.write(response if response else "*[No meaningful output generated. Try rephrasing your question.]*")
