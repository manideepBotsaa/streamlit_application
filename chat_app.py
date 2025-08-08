import streamlit as st
import requests
import json

DEFAULT_MODEL = 'llama2'
DEFAULT_TEMP = 0.7


if "messages" not in st.session_state:
    st.session_state.messages = []
if "model" not in st.session_state:
    st.session_state.model = DEFAULT_MODEL
if "temperature" not in st.session_state:
    st.session_state.temperature = DEFAULT_TEMP

# Configure Streamlit page and initilazition  
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Apply custom CSS
st.markdown("""
<style>
.stApp {
    background-color: #000000;
}
.chat-container {N
    background-color: #1a1a1a;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 2px 4px rgba(255,255,255,0.1);
}

/* Customize text colors for better visibility on dark background */
p, .stMarkdown, .stText {
    color: #ffffff !important;
}

/* Style the sidebar */
.css-1d391kg, .css-12oz5g7 {
    background-color: #1a1a1a;
}

/* Style input fields */
.stTextInput input {
    background-color: #333333;
    color: #ffffff;
    border-color: #4a4a4a;
}

/* Style buttons */
.stButton button {
    background-color: #4a4a4a;
    color: #ffffff;
    border: none;
}

.stButton button:hover {
    background-color: #666666;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar configuration
with st.sidebar:
    import streamlit as st
import requests

# Step 1: Define defaults
DEFAULT_MODEL = 'llama2'
DEFAULT_TEMP = 0.7

# Step 2: Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "model" not in st.session_state:
    st.session_state.model = DEFAULT_MODEL
if "temperature" not in st.session_state:
    st.session_state.temperature = DEFAULT_TEMP

# Step 3: Sidebar UI
with st.sidebar:
    st.title("Settings")
    
    st.session_state.model = st.selectbox(
        "Choose model:",
        ["llama2", "mistral", "codellama"],
        index=["llama2", "mistral", "codellama"].index(st.session_state.model)
    )

    st.session_state.temperature = st.slider(
        "Temperature:",
        0.0, 1.0, st.session_state.temperature, step=0.1
    )

    if st.button("🔁 Reset to Default"):
        st.session_state.model = DEFAULT_MODEL
        st.session_state.temperature = DEFAULT_TEMP
        st.session_state.messages = []
        st.experimental_rerun()


# Main chat interface
st.title("🤖 personal gym chat bot")

# Function to query Ollama
def query_ollama(prompt, model_name, temp):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "temperature": temp,
                "stream": False
            }
        )
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

# Display chat history
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Assistant:** {message['content']}")
    st.markdown("---")

# Initialize session state for user 
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

def clear_input():
    st.session_state.user_input = ""

# Chat input
user_input = st.text_input("Your message:", key="user_input_widget", placeholder="Type your message here...", on_change=clear_input)

if st.button("Send", type="primary"):
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get AI response
        with st.spinner("Thinking..."):
            response = query_ollama(user_input, model, temperature)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.rerun()
    else:
        st.warning("Please enter a message.")

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []

    st.rerun()

