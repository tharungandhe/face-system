import streamlit as st
import requests

# Inject custom CSS
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    .title {
        color: #2E86C1;
        font-size: 36px;
        font-weight: bold;
        text-align: center;
    }
    .success {
        color: #27AE60;
        font-weight: bold;
    }
    .error {
        color: #E74C3C;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 
# ... then continue with your registration/login code here ...


if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Face Authentication System")

# Registration
name = st.text_input("Enter Name")
file_reg = st.file_uploader("Upload Face Image for Registration")
if st.button("Register"):
    if name and file_reg:
        res = requests.post("http://127.0.0.1:8000/register",
                            data={"name": name},
                            files={"file": file_reg.getvalue()})
        st.session_state.messages.append(("assistant", res.json()["chat"]))

# Login
file_login = st.file_uploader("Upload Face Image for Login")
if st.button("Login"):
    if file_login:
        res = requests.post("http://127.0.0.1:8000/login",
                            files={"file": file_login.getvalue()})
        st.session_state.messages.append(("assistant", res.json()["chat"]))

# Display chat messages
for role, msg in st.session_state.messages:
    st.chat_message(role).write(msg)
