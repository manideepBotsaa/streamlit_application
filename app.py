import streamlit as st
import requests
import json
import logging
import time
from datetime import datetime
import traceback
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gym_chatbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add default constants
DEFAULT_MODEL = "llama2"
DEFAULT_TEMPERATURE = 0.7
OLLAMA_BASE_URL = "http://localhost:11434"
REQUEST_TIMEOUT = 30  # seconds
MAX_RETRIES = 3

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
/* Error message styling */
.error-message {
    background-color: #ff4444;
    color: white;
    padding: 10px;
    border-radius: 5px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

def log_user_interaction(action: str, details: Dict[str, Any] = None):
    """Log user interactions for monitoring and debugging"""
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details or {}
        }
        logger.info(f"User Interaction: {json.dumps(log_entry)}")
    except Exception as e:
        logger.error(f"Failed to log user interaction: {e}")

def check_ollama_connection() -> tuple[bool, str]:
    """Check if Ollama service is available"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            logger.info("Ollama service is available")
            return True, "Connected"
        else:
            logger.warning(f"Ollama service returned status code: {response.status_code}")
            return False, f"Service unavailable (Status: {response.status_code})"
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Ollama service")
        return False, "Cannot connect to Ollama service. Make sure it's running on localhost:11434"
    except requests.exceptions.Timeout:
        logger.error("Ollama service connection timeout")
        return False, "Connection timeout. Ollama service may be slow to respond"
    except Exception as e:
        logger.error(f"Unexpected error checking Ollama connection: {e}")
        return False, f"Unexpected error: {str(e)}"

def validate_input(prompt: str) -> tuple[bool, str]:
    """Validate user input"""
    if not prompt or not prompt.strip():
        return False, "Empty message"
    
    if len(prompt) > 10000:  # Reasonable limit
        return False, "Message too long (max 10,000 characters)"
    
    # Check for potentially harmful content (basic filtering)
    harmful_patterns = ['<script', '<?php', 'javascript:', 'eval(']
    prompt_lower = prompt.lower()
    for pattern in harmful_patterns:
        if pattern in prompt_lower:
            logger.warning(f"Potentially harmful input detected: {pattern}")
            return False, "Input contains potentially harmful content"
    
    return True, "Valid"

def query_ollama(prompt: str, model_name: str, temp: float) -> Dict[str, Any]:
    """
    Enhanced Ollama query function with comprehensive error handling and logging
    Returns a dictionary with success status, response, and error details
    """
    start_time = time.time()
    
    # Log the request
    log_user_interaction("ollama_request", {
        "model": model_name,
        "temperature": temp,
        "prompt_length": len(prompt)
    })
    
    # Validate input
    is_valid, validation_message = validate_input(prompt)
    if not is_valid:
        logger.warning(f"Input validation failed: {validation_message}")
        return {
            "success": False,
            "error_type": "validation_error",
            "error_message": f"Input validation failed: {validation_message}",
            "response": None
        }
    
    # Check Ollama connection first
    is_connected, connection_status = check_ollama_connection()
    if not is_connected:
        return {
            "success": False,
            "error_type": "connection_error",
            "error_message": connection_status,
            "response": None
        }
    
    # Retry logic
    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Ollama request attempt {attempt + 1}/{MAX_RETRIES}")
            
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "temperature": temp,
                    "stream": False
                },
                timeout=REQUEST_TIMEOUT
            )
            
            # Log response status
            logger.info(f"Ollama response status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    response_time = time.time() - start_time
                    
                    # Log successful response
                    log_user_interaction("ollama_response", {
                        "model": model_name,
                        "response_time": round(response_time, 2),
                        "response_length": len(response_data.get("response", "")),
                        "attempt": attempt + 1
                    })
                    
                    logger.info(f"Ollama request successful in {response_time:.2f}s")
                    return {
                        "success": True,
                        "response": response_data.get("response", ""),
                        "error_type": None,
                        "error_message": None
                    }
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse Ollama response JSON: {e}")
                    return {
                        "success": False,
                        "error_type": "json_error",
                        "error_message": "Failed to parse response from Ollama service",
                        "response": None
                    }
            
            elif response.status_code == 404:
                logger.error(f"Model '{model_name}' not found")
                return {
                    "success": False,
                    "error_type": "model_error",
                    "error_message": f"Model '{model_name}' not found. Please check if the model is installed.",
                    "response": None
                }
            
            elif response.status_code == 500:
                logger.error("Ollama internal server error")
                if attempt < MAX_RETRIES - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    return {
                        "success": False,
                        "error_type": "server_error",
                        "error_message": "Ollama service is experiencing internal errors",
                        "response": None
                    }
            
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                return {
                    "success": False,
                    "error_type": "api_error",
                    "error_message": f"Ollama API returned error code: {response.status_code}",
                    "response": None
                }
                
        except requests.exceptions.Timeout:
            logger.error(f"Ollama request timeout on attempt {attempt + 1}")
            if attempt < MAX_RETRIES - 1:
                continue
            else:
                return {
                    "success": False,
                    "error_type": "timeout_error",
                    "error_message": f"Request timed out after {REQUEST_TIMEOUT} seconds. Ollama may be processing a heavy request.",
                    "response": None
                }
        
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error on attempt {attempt + 1}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(1)
                continue
            else:
                return {
                    "success": False,
                    "error_type": "connection_error",
                    "error_message": "Cannot connect to Ollama service. Please ensure it's running.",
                    "response": None
                }
        
        except Exception as e:
            logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
            logger.error(traceback.format_exc())
            if attempt < MAX_RETRIES - 1:
                continue
            else:
                return {
                    "success": False,
                    "error_type": "unexpected_error",
                    "error_message": f"An unexpected error occurred: {str(e)}",
                    "response": None
                }
    
    return {
        "success": False,
        "error_type": "max_retries_exceeded",
        "error_message": f"Failed after {MAX_RETRIES} attempts",
        "response": None
    }

# Initialize session state for chat history and error tracking
if 'messages' not in st.session_state:
    st.session_state.messages = []
    logger.info("Initialized new chat session")

if 'error_count' not in st.session_state:
    st.session_state.error_count = 0

if 'last_error_time' not in st.session_state:
    st.session_state.last_error_time = None

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Configuration")
    
    # Connection status check
    is_connected, status_msg = check_ollama_connection()
    if is_connected:
        st.success(f"🟢 Ollama: {status_msg}")
    else:
        st.error(f"🔴 Ollama: {status_msg}")
    
    # Determine current values (use defaults if just reset or not set)
    model_options = ["llama2", "mistral", "codellama"]
    
    # Get current values from widgets or use defaults
    current_model = st.session_state.get('model_widget', DEFAULT_MODEL)
    current_temp = st.session_state.get('temp_widget', DEFAULT_TEMPERATURE)
    
    # Handle reset functionality
    if st.button("Reset to Defaults"):
        try:
            # Delete the widget keys to force reset
            for key in ['model_widget', 'temp_widget']:
                if key in st.session_state:
                    del st.session_state[key]
            
            log_user_interaction("settings_reset")
            st.success("✅ Settings reset to defaults!")
            logger.info("Settings reset to defaults")
            st.rerun()
        except Exception as e:
            logger.error(f"Error resetting settings: {e}")
            st.error("❌ Failed to reset settings")
    
    # Create widgets with proper default handling
    try:
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
            key="temp_widget",
            help="Higher values make output more random, lower values more focused"
        )
        
        # Show current settings info
        st.info(f"📊 Current Settings:\n- Model: {model}\n- Temperature: {temperature}")
        
        # Error statistics
        if st.session_state.error_count > 0:
            st.warning(f"⚠️ Errors this session: {st.session_state.error_count}")
        
    except Exception as e:
        logger.error(f"Error creating sidebar widgets: {e}")
        st.error("❌ Error configuring settings")
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This chatbot uses Ollama for local AI processing with enhanced error handling and logging.")
    
    # Debug info (collapsible)
    with st.expander("🔧 Debug Info"):
        st.text(f"Ollama URL: {OLLAMA_BASE_URL}")
        st.text(f"Timeout: {REQUEST_TIMEOUT}s")
        st.text(f"Max Retries: {MAX_RETRIES}")
        st.text(f"Session Errors: {st.session_state.error_count}")

# Main chat interface
st.title("🤖 personal gym chat bot")

# Display connection warning if needed
if not is_connected:
    st.error(f"⚠️ **Connection Issue**: {status_msg}")
    st.info("💡 **Troubleshooting Tips:**\n- Make sure Ollama is installed and running\n- Check if the service is available at http://localhost:11434\n- Try restarting the Ollama service")

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
    label_visibility="collapsed",
    max_chars=10000
)

# Create columns for Send and Clear Chat buttons
col1, col2 = st.columns([1, 1])

with col1:
    send_clicked = st.button("Send", type="primary", disabled=not is_connected)

with col2:
    clear_clicked = st.button("Clear Chat")

# Handle send button click
if send_clicked and user_input.strip():
    try:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        log_user_interaction("user_message", {"message_length": len(user_input)})
        
        # Get AI response with enhanced error handling
        with st.spinner("🤔 Thinking..."):
            result = query_ollama(user_input, model, temperature)
            
            if result["success"]:
                st.session_state.messages.append({"role": "assistant", "content": result["response"]})
                logger.info("Successfully processed user message")
            else:
                # Handle different types of errors
                error_type = result["error_type"]
                error_msg = result["error_message"]
                
                # Increment error counter
                st.session_state.error_count += 1
                st.session_state.last_error_time = datetime.now()
                
                # Log the error
                logger.error(f"Ollama query failed: {error_type} - {error_msg}")
                
                # Show user-friendly error message
                if error_type == "connection_error":
                    st.error(f"🔌 **Connection Error**: {error_msg}")
                    st.info("💡 Try refreshing the page or check if Ollama is running")
                elif error_type == "timeout_error":
                    st.error(f"⏱️ **Timeout Error**: {error_msg}")
                    st.info("💡 The model may be busy. Try a shorter message or wait a moment")
                elif error_type == "model_error":
                    st.error(f"🤖 **Model Error**: {error_msg}")
                    st.info("💡 Try selecting a different model from the sidebar")
                elif error_type == "validation_error":
                    st.error(f"✏️ **Input Error**: {error_msg}")
                else:
                    st.error(f"❌ **Error**: {error_msg}")
                    st.info("💡 Please try again or contact support if the issue persists")
                
                # Add error message to chat for context
                error_response = f"Sorry, I encountered an error: {error_msg}"
                st.session_state.messages.append({"role": "assistant", "content": error_response})
        
        st.rerun()
        
    except Exception as e:
        logger.error(f"Unexpected error in send handler: {e}")
        logger.error(traceback.format_exc())
        st.error(f"❌ An unexpected error occurred: {str(e)}")
        st.session_state.error_count += 1

elif send_clicked and not user_input.strip():
    st.warning("⚠️ Please enter a message before sending.")
    log_user_interaction("empty_message_attempt")

# Handle clear chat button click
if clear_clicked:
    try:
        message_count = len(st.session_state.messages)
        st.session_state.messages = []
        st.session_state.error_count = 0  # Reset error counter too
        st.session_state.last_error_time = None
        
        log_user_interaction("chat_cleared", {"messages_cleared": message_count})
        st.success("💬 Chat history cleared!")
        logger.info(f"Chat history cleared ({message_count} messages)")
        st.rerun()
    except Exception as e:
        logger.error(f"Error clearing chat: {e}")
        st.error("❌ Failed to clear chat history")

# Footer with session info
if st.session_state.messages:
    st.markdown("---")
    st.caption(f"💬 {len(st.session_state.messages)} messages in this session | 🚨 {st.session_state.error_count} errors")