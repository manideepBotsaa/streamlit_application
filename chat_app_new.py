import streamlit as st
import requests
import json
from datetime import datetime

# Configure Streamlit page and initialization  
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
.chat-container {
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

/* Chat message styling */
.user-message {
    background-color: #2d5a7b;
    padding: 10px 15px;
    border-radius: 15px 15px 0 15px;
    margin: 10px 0;
    max-width: 80%;
    margin-left: auto;
}

.assistant-message {
    background-color: #4a4a4a;
    padding: 10px 15px;
    border-radius: 15px 15px 15px 0;
    margin: 10px 0;
    max-width: 80%;
}

.message-time {
    font-size: 0.7em;
    color: #888888;
    margin-top: 5px;
}

/* Form styling */
.stForm {
    background-color: #1a1a1a;
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Initialize session state for form key
if 'form_key' not in st.session_state:
    st.session_state.form_key = 0

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    model = st.selectbox(
        "Select Model",
        ["llama2", "mistral", "codellama"],
        index=0
    )
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7)
    
    st.markdown("---")
    
    # Chat management
    st.markdown("### Chat Management")
    if st.button("🗑️ Clear Chat History", type="secondary"):
        st.session_state.messages = []
        st.session_state.form_key += 1
        st.rerun() # ✅ fixed

    # Chat statistics
    if st.session_state.messages:
        st.markdown(f"**Messages:** {len(st.session_state.messages)}")
        user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.markdown(f"**Your messages:** {user_messages}")
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This chatbot uses Ollama for local AI processing.")

# Main chat interface
st.title("🤖 Personal Gym Chat Bot")

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

# Display chat history with improved styling
if st.session_state.messages:
    st.markdown("### 💬 Chat History")
    
    for i, message in enumerate(st.session_state.messages):
        with st.container():
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>You:</strong> {message['content']}
                    <div class="message-time">{message.get('timestamp', '')}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    <strong>Assistant:</strong> {message['content']}
                    <div class="message-time">{message.get('timestamp', '')}</div>
                </div>
                """, unsafe_allow_html=True)
else:
    st.info("👋 Start a conversation by typing a message below!")

# Form for chat input (prevents rerun on every keystroke)
with st.form(key=f"chat_form_{st.session_state.form_key}", clear_on_submit=True):
    st.markdown("### 💭 New Message")
    
    # Two-column layout for input and send button
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_area(
            "Your message:",
            placeholder="Type your message here...",
            height=100,
            key=f"user_input_{st.session_state.form_key}"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
        send_button = st.form_submit_button("🚀 Send", type="primary")
    
    # Handle form submission
    if send_button and user_input.strip():
        # Add timestamp to messages
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user", 
            "content": user_input.strip(),
            "timestamp": timestamp
        })
        
        # Get AI response
        with st.spinner("🤔 Thinking..."):
            response = query_ollama(user_input.strip(), model, temperature)
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
        
        # Increment form key to clear the form
        st.session_state.form_key += 1
        st.rerun()  # ✅ fixed
    
    elif send_button and not user_input.strip():
        st.error("Please enter a message before sending.")

# Display connection status
st.markdown("---")
with st.expander("🔧 Connection Status"):
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            st.success("✅ Connected to Ollama server")
            models = response.json().get("models", [])
            if models:
                st.markdown("**Available models:**")
                for model_info in models:
                    st.markdown(f"- {model_info.get('name', 'Unknown')}")
            else:
                st.warning("No models found. Please install models using `ollama pull <model_name>`")
        else:
            st.error(f"❌ Ollama server error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to Ollama server. Make sure Ollama is running on localhost:11434")
    except Exception as e:
        st.error(f"❌ Error checking connection: {str(e)}")
