import openai
import streamlit as st


pre_message_to_openai = ('im sending you a history  of transactions and the last transaction is the current one. let me know if it looks fraud or not'
                         'if the last transaction looks suspicious to you (for example if the amount extreme or its from an unknown seller etc.) than say it looks like a fraud.')

MODEL = "gpt-3.5-turbo"

with st.sidebar:
    st.title('🤖💬 OpenAI Chatbot')
    st.success('API key already provided!', icon='✅')
    openai.api_key = st.secrets['OPENAI_API_KEY']

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.insert(0, {"role":"system", "content": pre_message_to_openai})
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=MODEL,
            messages=[{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages], stream=True):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})