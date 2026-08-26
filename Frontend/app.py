import requests
import streamlit as st

API = "http://localhost:8000"

st.title("Aria — Aster & Row Support")

if "session_id" not in st.session_state:
    st.session_state.session_id = None
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if query := st.chat_input("Ask something…"):
    st.chat_message("user").write(query)
    st.session_state.messages.append({"role": "user", "content": query})

    try:
        res = requests.post(f"{API}/chat", json={
            "query": query,
            "session_id": st.session_state.session_id,
        }).json()
        answer = res["answer"]
        st.session_state.session_id = res["session_id"]
    except Exception as e:
        answer = f"Error: {e}"

    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
