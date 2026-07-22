import streamlit as st
import tkinter as tk
from tkinter import Text, END

# Create a function to update text in a Streamlit app
def update_text_area(text):
    # Initialize the chat history in session state if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Add new text to the chat history
    st.session_state.chat_history.append(text)

    # Force a rerun to update the display
    st.experimental_rerun()


# Main Streamlit app layout function
def create_streamlit_gui():
    st.set_page_config(
        page_title="Smart Talk Assistant",
        page_icon="🤖",
        layout="wide"
    )

    # Apply custom CSS to match the dark theme from Tkinter
    st.markdown("""
    <style>
        .stApp {
            background-color: #0D1117;
            color: #C9D1D9;
        }
        .text-area {
            background-color: #0D1117;
            color: #C9D1D9;
            font-family: Arial, sans-serif;
            font-size: 10pt;
            padding: 10px;
            border-radius: 5px;
            min-height: 400px;
            overflow-y: auto;
        }
        .stButton > button {
            background-color: #21262D;
            color: #FFFFFF;
            border: none;
        }
        .stButton > button:hover {
            background-color: #58A6FF;
        }
    </style>
    """, unsafe_allow_html=True)

    # App title
    st.title("Smart Talk - Your AI Assistant")

    # Display the text area (chat history)
    text_container = st.container()
    with text_container:
        chat_box = st.empty()

        # Get chat history from session state
        if 'chat_history' in st.session_state:
            all_text = "\n".join(st.session_state.chat_history)
            chat_box.markdown(f'<div class="text-area">{all_text}</div>', unsafe_allow_html=True)

    # Input area for commands
    user_input = st.text_input("Enter your command:")
    if st.button("Submit") or user_input:
        if user_input:
            # Process the command here (similar to your processCommand function)
            update_text_area(f"User: {user_input}")
            # Clear the input box after submission (requires rerun)
            st.session_state.user_input = ""

root = tk.Tk()
# Create text area for displaying messages
text_area = Text(root, width=40, height=20, bg="#0D1117", fg="#C9D1D9",
                font=("Arial", 10), state='disabled')

def update_text_area(message):
    """Update the text area with new messages"""
    text_area.configure(state='normal')
    text_area.insert(END, f"{message}\n")
    text_area.configure(state='disabled')
    text_area.see(END)

if __name__ == "__main__":
    create_streamlit_gui()
