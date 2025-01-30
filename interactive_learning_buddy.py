import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os



# Initialize Gemini API

API_KEY = os.getenv("GEMINI_API_KEY")  # Retrieve actual API key from .env
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

def get_response(prompt, difficulty="intermediate"):
    """Generate educational response based on difficulty level"""
    difficulty_prompts = {
        "beginner": "Explain this in simple terms for a beginner: ",
        "intermediate": "Provide a detailed explanation of: ",
        "advanced": "Give an in-depth technical analysis of: "
    }
    
    full_prompt = f"{difficulty_prompts[difficulty]}{prompt}"
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
    

# Streamlit UI
st.title("Interactive Learning Buddy")

# Difficulty selector
difficulty = st.select_slider(
    "Select difficulty level",
    options=["beginner", "intermediate", "advanced"],
    value="intermediate"
)

# User input
user_prompt = st.text_area("What would you like to learn about?")

if st.button("Get Answer"):
    if user_prompt:
        try:
            response = get_response(user_prompt, difficulty)
            st.write(response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a question.")