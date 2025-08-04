# streamlit_application

# AI Chatbot Documentation

## Overview
This project is a Streamlit-based web application that implements a personal gym chatbot. It uses the Ollama API for local AI processing and provides a user-friendly interface for interacting with different language models.

## Features
- Dark-themed user interface with custom CSS styling
- Configurable model selection (llama2, mistral, codellama)
- Adjustable temperature setting for AI responses
- Chat history persistence using Streamlit session state
- Real-time chat interface with user and assistant messages
- Clear chat functionality
- Error handling for API requests

## Prerequisites
- Python 3.8+
- Streamlit
- Requests library
- Ollama server running locally on port 11434

## Installation
1. Install required Python packages:
```bash
pip install streamlit requests
```

2. Ensure Ollama is installed and running locally:
- Follow Ollama's official documentation for installation
- Start the Ollama server: `ollama serve`

## Project Structure
```
project_directory/
│
├── app.py           # Main application code
├── README.md        # This documentation file
```

## Usage
1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Access the application through your web browser (typically at `http://localhost:8501`)

3. Configure settings in the sidebar:
- Select desired model
- Adjust temperature slider
- View application information

4. Interact with the chatbot:
- Enter messages in the text input field
- Click "Send" to get AI responses
- Use "Clear Chat" to reset the conversation

## Code Explanation

### Imports
- `streamlit`: For creating the web interface
- `requests`: For making API calls to Ollama
- `json`: For handling JSON data

### Page Configuration
```python
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)
```
Sets up the Streamlit page with a title, icon, and wide layout.

### CSS Styling
Custom CSS is applied using `st.markdown` with `unsafe_allow_html=True` to create a dark theme and style various UI components.

### Session State
```python
if 'messages' not in st.session_state:
    st.session_state.messages = []
```
Initializes chat history storage using Streamlit's session state.

### Sidebar Configuration
```python
with st.sidebar:
    st.title("⚙️ Configuration")
    model = st.selectbox(...)
    temperature = st.slider(...)
```
Creates a sidebar for model selection and temperature adjustment.

### Main Interface
- Displays the chat history in a container
- Shows user and assistant messages with proper formatting
- Uses markdown for styling

### Ollama Integration
```python
def query_ollama(prompt, model_name, temp):
    response = requests.post("http://localhost:11434/api/generate", ...)
```
Handles API calls to the local Ollama server for generating responses.

### Chat Functionality
- Text input for user messages
- Send button to trigger AI response
- Clear chat button to reset conversation
- Spinner during API processing

## Error Handling
- Checks for valid user input
- Handles API request errors
- Displays warning messages when appropriate

## Limitations
- Requires local Ollama server
- Limited to supported models (llama2, mistral, codellama)
- No persistent storage for chat history
- Basic error handling for API failures

## Future Improvements
- Add persistent storage for chat history
- Implement message streaming
- Add support for more models
- Enhance error handling
- Add conversation export functionality

## Troubleshooting
- Ensure Ollama server is running on port 11434
- Verify model availability in Ollama
- Check internet connection for package installation
- Monitor Streamlit logs for errors
