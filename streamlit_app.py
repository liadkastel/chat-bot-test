import openai
import streamlit as st


mail_types = "SRE,IT,Cyber,Data"
pre_message_to_openai = ('For all of the following message, the message is an email, and i want you to classify it. your response should '
                       f'be 1 word from the following set: {mail_types} ' 
                         'and we have the following definition of each type: '
                         'SRE = Site reliability engineering responsible for infrastructures, rabbit queues, etc '
                         'Cyper = cyber security, manages finishing mails and grant access to installing programs'
                         'Data = responsible for databases, SQL,Mongo,Elastic etc. '
                         'IT = responsible for computer problems, system updates etc.')

MODEL = "gpt-3.5-turbo"


with st.sidebar:
    st.title('Payoneer email bot')
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        openai.api_key = st.secrets['OPENAI_API_KEY']
    else:
        openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
        if not (openai.api_key.startswith('sk-') and len(openai.api_key)==51):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.insert(0, {"role": "system", "content": pre_message_to_openai})

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages], stream=True)
        full_response += response.choices[0].delta.get("content", "")
        message_placeholder.markdown(full_response + " ")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

