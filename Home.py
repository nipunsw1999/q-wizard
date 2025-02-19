import streamlit as st
import os
from dotenv import load_dotenv
import openai
import time
import json

st.sidebar.image("logo.png", width=800) 

if 'quiz' not in st.session_state:
    st.session_state['quiz'] = "" 
# Load environment variables
load_dotenv()

if 'stat' not in st.session_state:
    st.session_state['stat'] = 0

openai_api_key = os.getenv("OPENAI_API_KEY")
# openai_api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = openai_api_key
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def check_possibility(text):
    with st.spinner("Checking..."):
        prompt = f"""
        Analyze the following text and determine if it is possible to generate meaningful questions based on it. 

        ### Criteria:
        1. If the text is random characters, gibberish, or completely unrelated topics, respond with "NO."
        2. If the text is a person’s name:
        - Respond with "NO" if the person is unknown or lacks information available on the internet.
        - Respond with "YES" if the person is famous or well-documented online.
        3. If the text is the name of an app:
        - Respond with "NO" if the app is unknown or not widely recognized.
        - Respond with "YES" if the app is popular or has notable information available online.
        4. Otherwise, if the text is a valid topic, keyword, or sentence suitable for generating meaningful questions, respond with "YES."

        Text: {text}
        """



        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        ) 
        # st.write(response.choices[0].message['content'])
    return response.choices[0].message['content']

def generate_questions_from_text(text, question_count,per):
    prompt = f"""
    You are an intelligent person to generate questions. Your answers and correct answers must be correct 100% and meaningful. Generate questions dificultally level should {per}/3.
    Generate {question_count} multiple-choice questions from the following text.
    Format the output as JSON with the structure:
    {{
        "1": {{
            "question": "What is the question?",
            "answers": [
                "Option 1",
                "Option 2",
                "Option 3",
                "Option 4"
            ],
            "correct_answers": ["Option 1", "Option 3"],  # Include one or more correct answers
            "explanation": "Explanation of the correct answers",
            "status": "NO"  # Always set to 'NO' initially
        }},
        "2": {{
            ...
        }},
        ...
    }}

    There are one or more correct answers. Few questions should have multiple correct answers. Do not provide anything else except the JSON. Your topic is 
    topic: {text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    content = response.choices[0].message['content']
    # Parse JSON response safely
    try:
        parsed_json = json.loads(content)
        return parsed_json
    except json.JSONDecodeError:
        st.error("Failed to parse the response as valid JSON. Please try again.")
        return None

def inf(text:str,seconds:int,done_display_time: int = 2):
    done_message = st.empty()
    done_message.info(text, icon="ℹ️")
    time.sleep(seconds)
    time.sleep(done_display_time)
    done_message.empty()

def completed(text:str,done_display_time:int = 2):
    done_message = st.empty()
    done_message.success(text, icon="✅")
    time.sleep(done_display_time)
    done_message.empty()
    
st.title("Q-Wizard")

if st.session_state['stat'] == 0:

    st.subheader("Customize Your Quiz")
    difficulty_level = st.select_slider(
        "Choose Your Challenge Mode",
        ["Easy", "Intermediate", "Hard"],
        key="difficulty_level_slider"
    )
    
    questions = st.select_slider(
        "Choose Number of Questions",
        [5,10, 15, 20,25,30,40,50],
        key="questions_slider"
    )


    topic = st.text_area("Enter a topic (Tip: Use a clear and specific topic for the best results!)")

    start = st.button("Generate Quiz")

    per = 1
    if start:
        if difficulty_level == "Easy": per = 1
        elif difficulty_level == "Intermediate": per = 2
        elif difficulty_level == "Hard": per = 3
        if topic == "":
            inf("Please enter a topic to continue",2)
        else:
            if check_possibility(topic)=="NO":
                inf("Sorry, we cannot generate a quiz on this topic. Please try another one.",2)
            else:
                with st.spinner("Generating..."):
                    st.session_state['quiz'] = (generate_questions_from_text(topic,questions,per))
                    st.session_state['stat'] = 1
                completed("Quiz Generated")
                st.page_link("pages/Quiz.py", label=":green[Start]", icon="✍️")

else:
    if st.session_state['stat'] == 2:
        reset = st.button(":red[Restart new quiz]")
        if reset:
            st.session_state['stat'] = 0
            st.toast("Refresh the page...🔄")
    elif st.session_state['stat'] == 1:
        st.page_link("pages/Quiz.py", label=":green[Back to quiz]", icon="✍️")
        reset = st.button(":red[Give up and Restart new quiz]")
        if reset:
            st.session_state['stat'] = 0
            st.toast("Refresh the page...🔄")