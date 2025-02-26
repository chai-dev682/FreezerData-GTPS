import streamlit as st
from app.services.chat import chat_service

st.title("💬 AI-Driven GTPS for Technical Troubleshooting")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are helpful assistant to assist user providing information about freezing and cooling systems."},
        {"role": "assistant", "content": "How can I help you?"}
    ]

if "current_object" not in st.session_state:
    st.session_state["current_object"] = None

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    
    # Process message with chat service
    result = chat_service.process_message(prompt, st.session_state.messages, st.session_state["current_object"])
    
    # Update session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": result["response"]})
    
    # Update current object if changed
    if result["state"]["object"]:
        st.session_state["current_object"] = result["state"]["object"]
    
    st.chat_message("assistant").write(result["response"])
