**streamlit_application**

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/manideepBotsaa/streamlit_application)

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

**AI Chatbot Documentation**

**Overview**
>This project is a Streamlit-based web application that implements a personal gym chatbot. It uses the Ollama API for local AI processing and provides a user-friendly interface for interacting with different language models.

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=24&duration=3000&pause=1000&color=00C853&center=true&vCenter=true&width=900&linesThanks+for+visiting+streamlit_application!+🙌;Start+the+repo+✅;Share+it+with+others+🌍;Contribute+and+grow+🛠️;Happy+Coding+✨!" alt="Thanks Banner Typing SVG" />
</div>

**📊 Project Insights**

<table align="center">
    <thead align="center">
        <tr>
            <td><b>🌟 Stars</b></td>
            <td><b>🍴 Forks</b></td>
            <td><b>🐛 Issues</b></td>
            <td><b>🔔 Open PRs</b></td>
            <td><b>🔕 Closed PRs</b></td>
            <td><b>🛠️ Languages</b></td>
            <td><b>👥 Contributors</b></td>
        </tr>
     </thead>
    <tbody>
         <tr>
            <td><img alt="Stars" src="https://img.shields.io/github/stars/manideepBotsaa/streamlit_application?style=flat&logo=github"/></td>
            <td><img alt="Forks" src="https://img.shields.io/github/forks/manideepBotsaa/streamlit_application?style=flat&logo=github"/></td>
            <td><img alt="Issues" src="https://img.shields.io/github/issues/manideepBotsaa/streamlit_application?style=flat&logo=github"/></td>
            <td><img alt="Open PRs" src="https://img.shields.io/github/issues-pr/Ayushjhawar8/Flavor-ai?style=flat&logo=github"/></td>
            <td><img alt="Closed PRs" src="https://img.shields.io/github/issues-pr-closed/manideepBotsaa/streamlit_application?style=flat&color=critical&logo=github"/></td>
            <td><img alt="Languages Count" src="https://img.shields.io/github/languages/count/manideepBotsaa/streamlit_application?style=flat&color=green&logo=github"></td>
            <td><img alt="Contributors Count" src="https://img.shields.io/github/contributors/manideepBotsaa/streamlit_application?style=flat&color=blue&logo=github"/></td>
        </tr>
    </tbody>
</table>

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="150%">

**Features**
- Dark-themed user interface with custom CSS styling
- Configurable model selection (llama2, mistral, codellama)
- Adjustable temperature setting for AI responses
- Chat history persistence using Streamlit session state
- Real-time chat interface with user and assistant messages
- Clear chat functionality
- Error handling for API requests

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="150%">

![GSSoC Logo](/streamlit_application/gssoc%20logo.png)

**🌟 Exciting News...**

🚀 This project is now an official part of GirlScript Summer of Code – GSSoC'25! 💃🎉💻 We're thrilled to welcome contributors from all over India and beyond to collaborate, build, and grow streamlit application! Let’s make learning and career development smarter – together! 🌟👨‍💻👩‍💻

👩‍💻 GSSoC is one of India’s **largest 3-month-long open-source programs** that encourages developers of all levels to contribute to real-world projects 🌍 while learning, collaborating, and growing together. 🌱

🌈 With **mentorship, community support**, and **collaborative coding**, it's the perfect platform for developers to:

- ✨ Improve their skills
- 🤝 Contribute to impactful projects
- 🏆 Get recognized for their work
- 📜 Receive certificates and swag!

🎉 **I can’t wait to welcome new contributors** from GSSoC 2025 to this streamlit application project family! Let's build, learn, and grow together — one commit at a time. 🔥👨‍💻👩‍💻

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

**Prerequisites**
- Python 3.8+
- Streamlit
- Requests library
- Ollama server running locally on port 11434

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

**Installation**
1. Install required Python packages:
```bash
pip install streamlit requests
```

2. Ensure Ollama is installed and running locally:
- Follow Ollama's official documentation for installation
- Start the Ollama server: `ollama serve`

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

**Project Structure**

```bash
project_directory/
│
├── app.py           # Main application code
├── README.md        # This documentation file
```

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

**Usage**
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

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

**Code Explanation**

***Imports***
- `streamlit`: For creating the web interface
- `requests`: For making API calls to Ollama
- `json`: For handling JSON data

***Page Configuration***
```python
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)
```
Sets up the Streamlit page with a title, icon, and wide layout.

***CSS Styling***
Custom CSS is applied using `st.markdown` with `unsafe_allow_html=True` to create a dark theme and style various UI components.

***Session State***
```python
if 'messages' not in st.session_state:
    st.session_state.messages = []
```
Initializes chat history storage using Streamlit's session state.

***Sidebar Configuration***
```python
with st.sidebar:
    st.title("⚙️ Configuration")
    model = st.selectbox(...)
    temperature = st.slider(...)
```
Creates a sidebar for model selection and temperature adjustment.

***Main Interface***
- Displays the chat history in a container
- Shows user and assistant messages with proper formatting
- Uses markdown for styling

***Ollama Integration***
```python
def query_ollama(prompt, model_name, temp):
    response = requests.post("http://localhost:11434/api/generate", ...)
```
Handles API calls to the local Ollama server for generating responses.

***Chat Functionality***
- Text input for user messages
- Send button to trigger AI response
- Clear chat button to reset conversation
- Spinner during API processing

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

**Error Handling**
- Checks for valid user input
- Handles API request errors
- Displays warning messages when appropriate

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

**Limitations**
- Requires local Ollama server
- Limited to supported models (llama2, mistral, codellama)
- No persistent storage for chat history
- Basic error handling for API failures

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

**Future Improvements**
- Add persistent storage for chat history
- Implement message streaming
- Add support for more models
- Enhance error handling
- Add conversation export functionality

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

**Troubleshooting**
- Ensure Ollama server is running on port 11434
- Verify model availability in Ollama
- Check internet connection for package installation
- Monitor Streamlit logs for errors

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

**📜 Code of Conduct**

Please refer to the [`Code of Conduct`](https://github.com/manideepBotsaa/streamlit_application/blob/main/CODE_OF_CONDUCT.md) for details on contributing guidelines and community standards.

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

**🤝👤 Contribution Guidelines**

We love our contributors! If you'd like to help, please check out our [`CONTRIBUTE.md`](https://github.com/manideepBotsaa/streamlit_application/blob/main/CONTRIBUTING.md) file for guidelines.

>Thank you once again to all our contributors who has contributed to **streamlit application!** Your efforts are truly appreciated. 💖👏

<!-- Contributors badge (auto-updating) -->

[![Contributors](https://img.shields.io/github/contributors/manideepBotsaa/streamlit_application?style=for-the-badge)](https://github.com/manideepBotsaa/streamlit_application/graphs/contributors)

<!-- Contributors avatars (auto-updating) -->
<p align="left">
  <a href="https://github.com/manideepBotsaa/streamlit_application/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=manideepBotsaa/streamlit_application" alt="Contributors" />
  </a>
</p>

See the full list of contributors and their contributions on the [`GitHub Contributors Graph`](https://github.com/manideepBotsaa/streamlit_application/graphs/contributors).

<h2 align="center">
<p style="font-family:var(--ff-philosopher);font-size:3rem;"><b> Show some <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Smilies/Red%20Heart.png" alt="Red Heart" width="40" height="40" /> by starring this awesome repository!
</p>
</h2>

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="150%">

**💡 Suggestions & Feedback**

Feel free to open issues or discussions if you have any feedback, feature suggestions, or want to collaborate!

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="150%">

**🙌 Support & Star**

***If you find this project helpful, please give it a star ⭐ to support more such educational initiatives!***

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

**📄 License**

This project is licensed under the MIT License - see the [`License`](https://github.com/manideepBotsaa/streamlit_application/blob/main/License) file for details.

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="150%">

**⭐ Stargazers**

<div align="center">
  <a href="https://github.com/manideepBotsaa/streamlit_application/stargazers">
    <img src="https://reporoster.com/stars/manideepBotsaa/streamlit_application?type=svg&limit=100&names=false" alt="Stargazers" />
  </a>
</div>

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="150%">

**🍴 Forkers**

<div align="center">
  <a href="https://github.com/manideepBotsaa/streamlit_application/network/members">
    <img src="https://reporoster.com/forks/manideepBotsaa/streamlit_application?type=svg&limit=100&names=false" alt="Forkers" />
  </a>

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="150%">

<h2>🧑‍💻Project Admin:</h2>
<table>
<tr>
<td align="center">
<a href="https://github.com/manideepBotsaa"><img src="https://avatars.githubusercontent.com/u/197450945?v=4" height="140px" width="140px" alt="Manideep Botsa"></a><br><sub><b>Manideep Botsa</b><br><a href="https://www.linkedin.com/in/manideep-botsa/"><img src="https://github-production-user-asset-6210df.s3.amazonaws.com/73993775/278833250-adb040ea-e3ef-446e-bcd4-3e8d7d4c0176.png" width="45px" height="45px"></a></sub>
</td>
</tr>
</table>

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

**👨‍🏫 Mentors – streamlit application (GSSoC'25)**

| Role          | Name               | GitHub Profile                                      | LinkedIn Profile                                                        |
| ------------- | ------------------ | --------------------------------------------------- | ----------------------------------------------------------------------- |
| Mentor 1   | Aayush Kumar Gupta  |  [AayushKGupta12](https://github.com/AayushKGupta12)  | [aayush-kumar-gupta](https://www.linkedin.com/in/aayush-kumar-gupta-2b7952219/) |

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

<h1 align="center"><img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Glowing%20Star.png" alt="Glowing Star" width="25" height="25" /> Give us a Star and let's make magic! <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Glowing%20Star.png" alt="Glowing Star" width="25" height="25" /></h1>

<p align="center">
     <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Mirror%20Ball.png" alt="Mirror Ball" width="150" height="150" />
</p>

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="150%">

**👨‍💻 Built with ❤️ by streamlit application Team**

**❤️ Manideep Botsa and Contributors ❤️** [open an issue](https://github.com/manideepBotsaa/streamlit_application/issues)

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="150%">

<div align="center">
    <a href="#top">
        <img src="https://img.shields.io/badge/Back%20to%20Top-000000?style=for-the-badge&logo=github&logoColor=white" alt="Back to Top">
    </a>
</div>

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=65&section=footer"/>

**Ready to show off your coding achievements? Get started with streamlit application today! 🚀**
