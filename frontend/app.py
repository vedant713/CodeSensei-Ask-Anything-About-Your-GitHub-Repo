import streamlit as st
import requests

# Backend API URL
BACKEND_URL = "http://localhost:8000"

# Set up the page
st.set_page_config(page_title="GitHub Repo Chat", layout="wide")

st.title("🤖 Chat with a GitHub Repo")

# Sidebar: Input for GitHub URL & Processing
st.sidebar.header("📂 Process a GitHub Repo")
repo_url = st.sidebar.text_input("Enter GitHub URL:")
if st.sidebar.button("Process Repository"):
    if repo_url:
        with st.spinner("Processing repository..."):  # Thinking animation
            response = requests.post(f"{BACKEND_URL}/process_repo", json={"url": repo_url})
            if response.status_code == 200:
                st.sidebar.success("Repository processed successfully! Start chatting below. ✅")
                st.session_state["repo_ready"] = True
            else:
                st.sidebar.error(f"Error: {response.json().get('detail', 'Unknown error')}")
    else:
        st.sidebar.warning("Please enter a GitHub URL first.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
st.subheader("💬 Chat with your Repo")

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask a question about the repository...")

if user_input:
    # Append user input to chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # Display user input immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send question to backend with a thinking animation
    with st.spinner("Thinking..."):  # Thinking animation
        response = requests.post(f"{BACKEND_URL}/chat", json={"question": user_input})
    
    if response.status_code == 200:
        bot_reply = response.json().get("answer", "No response received.")
    else:
        bot_reply = f"Error: {response.json().get('detail', 'Unknown error')}"
    
    # Append AI response to chat history
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(bot_reply)