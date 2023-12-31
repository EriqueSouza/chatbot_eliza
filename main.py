import openai
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

st.title("💬 Elisza - Your chatbot therapist")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "Please simulate an interaction with a compassionate "
                                                                 "therapist guided by the Rogerian approach. Address "
                                                                 "current concerns and feelings with empathy and "
                                                                 "reflection. Feel free to explore topics such as "
                                                                 "anxiety, stress, or personal challenges, "
                                                                 "offering guidance and insights based on your "
                                                                 "knowledge."},
                                    {"role": "assistant", "content": "How do you feel today?"}]

for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)
