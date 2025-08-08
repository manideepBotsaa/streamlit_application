import streamlit as st
import requests
import json

# Add default constants
DEFAULT_MODEL = "llama2"
DEFAULT_TEMPERATURE = 0.7

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
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # Determine current values (use defaults if just reset or not set)
    model_options = ["llama2", "mistral", "codellama"]
    
    # Get current values from widgets or use defaults
    current_model = st.session_state.get('model_widget', DEFAULT_MODEL)
    current_temp = st.session_state.get('temp_widget', DEFAULT_TEMPERATURE)
    
    # Handle reset functionality
    if st.button("Reset to Defaults"):
        # Delete the widget keys to force reset
        for key in ['model_widget', 'temp_widget']:
            if key in st.session_state:
                del st.session_state[key]
        st.success("✅ Settings reset to defaults!")
        st.rerun()
    
    # Create widgets with proper default handling
    model_index = model_options.index(current_model) if current_model in model_options else 0
    
    model = st.selectbox(
        "Select Model",
        model_options,
        index=model_index,
        key="model_widget"
    )
    
    temperature = st.slider(
        "Temperature", 
        0.0, 2.0, 
        current_temp, 
        key="temp_widget"
    )
    
    # Show current settings info
    st.info(f"📊 Current Settings:\n- Model: {model}\n- Temperature: {temperature}")
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This chatbot uses Ollama for local AI processing.")

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
if st.session_state.messages:
    st.markdown("### 💬 Chat History")
    for i, message in enumerate(st.session_state.messages):
        with st.container():
            if message["role"] == "user":
                st.markdown(f"**🧑 You:** {message['content']}")
            else:
                st.markdown(f"**🤖 Assistant:** {message['content']}")
        if i < len(st.session_state.messages) - 1:  # Don't add separator after last message
            st.markdown("---")

# Chat input section
st.markdown("### 📝 Send a Message")
user_input = st.text_input(
    "Your message:", 
    placeholder="Ask me about workouts, nutrition, or fitness tips...",
    label_visibility="collapsed"
)

# Create columns for Send and Clear Chat buttons
col1, col2 = st.columns([1, 1])

with col1:
    send_clicked = st.button("Send", type="primary")

with col2:
    clear_clicked = st.button("Clear Chat")

# Handle send button click
if send_clicked and user_input.strip():
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get AI response
    with st.spinner("🤔 Thinking..."):
        response = query_ollama(user_input, model, temperature)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.rerun()
elif send_clicked and not user_input.strip():
    st.warning("⚠️ Please enter a message before sending.")

# Handle clear chat button click
if clear_clicked:
    st.session_state.messages = []
    st.success("💬 Chat history cleared!")
    st.rerun()