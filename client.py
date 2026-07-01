import os
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("AIzaSyA5RKdhabt0LmwE88UuHLOO65xQRvCtkws"))

# Use fast model
model = genai.GenerativeModel("gemini-1.5-flash")

# Conversation memory
chat = model.start_chat(history=[])

def ask_jarvis(user_input):
    response = chat.send_message(user_input)
    return response.text
