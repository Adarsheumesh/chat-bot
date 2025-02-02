import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Debug print to verify API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Warning: API key not found!")
else:
    print("API key found:", api_key[:6] + "..." if api_key else "None")

app = Flask(__name__)

class OmniGuide:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat_history = []
        
        # System prompt
        self.system_prompt = """You are OmniGuide, a helpful AI assistant. 
        You provide clear, concise, and accurate responses."""
        
    def get_response(self, user_input):
        try:
            self.chat_history.append({"role": "user", "content": user_input})
            
            # Create context
            context = f"{self.system_prompt}\nUser: {user_input}"
            
            # Generate response using Gemini
            response = self.model.generate_content(context)
            
            if response.text:
                assistant_message = response.text.strip()
                self.chat_history.append({"role": "assistant", "content": assistant_message})
                return assistant_message
            else:
                return "I apologize, but I couldn't generate a response."
            
        except Exception as e:
            print(f"Error details: {str(e)}")
            return f"An error occurred: {str(e)}"

chatbot = OmniGuide()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    response = chatbot.get_response(user_message)
    return jsonify({'response': response})

# Remove the if __name__ == '__main__' block for Vercel deployment
app = app
