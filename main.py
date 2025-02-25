import streamlit as st
from app.services.upload import upload_service
from app.services.chat import chat_service

st.title("💬 AI-Driven GTPS for Technical Troubleshooting")

# Chat interface
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are helpful assistant to assist user providing information about freezing and cooling systems."},
        {"role": "assistant", "content": "How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    
    result = chat_service.process_message(prompt, st.session_state.messages)
    
    st.session_state.messages.append({"role": "assistant", "content": result["response"]})
    st.chat_message("assistant").write(result["response"])
