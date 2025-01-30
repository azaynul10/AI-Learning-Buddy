import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Set page config
st.set_page_config(page_title="AI Learning Buddy", page_icon="🤖", layout="wide")

# Sidebar
st.sidebar.title("AI Learning Buddy")
difficulty = st.select_slider(
    "Select difficulty level",
    options=["beginner", "intermediate", "advanced"],
    value="intermediate",
    key="difficulty_slider"  # Add this line
)

def save_to_history(question, answer):
    if 'history' not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({
        "question": question,
        "answer": answer
    })
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
        st.error(f"An error occurred: {str(e)}")
        return None

    

# Streamlit UI
st.title("Interactive Learning Buddy")




tab1, tab2, tab3 = st.tabs(["Learn", "Quiz", "Review"])

with tab1:
    st.header("Learn Something New")
    user_prompt = st.text_area("What would you like to learn about?", key="learn_prompt")    
    if st.button("Get Answer", key="learn_button"):
        if user_prompt:
            with st.spinner("Generating response..."):
                response = get_response(user_prompt, difficulty)
                if response:
                    st.success("Here's your explanation:")
                    st.write(response)
                    # Save to history (implement this function)
                    save_to_history(user_prompt, response)
        else:
            st.warning("Please enter a question.")

with tab2:
    st.header("Quiz Yourself")
    quiz_topic = st.text_input("Enter a topic for a quick quiz:",  key="quiz_topic")
    if st.button("Generate Quiz", key="quiz_button"):
        if quiz_topic:
            with st.spinner("Generating quiz..."):
                quiz_prompt = f"Create a 3-question quiz about {quiz_topic} suitable for {difficulty} level"
                quiz = get_response(quiz_prompt, difficulty)
                if quiz:
                    st.success("Here's your quiz:")
                    st.write(quiz)
        else:
            st.warning("Please enter a topic for the quiz.")

with tab3:
    st.header("Review Previous Topics")
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    for i, item in enumerate(st.session_state.history):
        with st.expander(f"Topic {i+1}"):
            st.write(f"Question: {item['question']}")
            st.write(f"Answer: {item['answer']}")
    
    if st.button("Clear History", key="clear_history"):
        st.session_state.history = []
        st.success("History cleared!")




