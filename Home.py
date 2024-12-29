import streamlit as st
import os
from dotenv import load_dotenv
import openai
import time

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
    prompt = f"""
    Analyze the following text and determine if it is possible to generate meaningful questions based on it. If the text is unsuitable for generating questions (e.g., random characters, gibberish, or completely unrelated topics), respond with NO. Otherwise, respond with YES. Examples of suitable text include topics, keywords, or sentences. Text: {text}
    """


    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    ) 
    # st.write(response.choices[0].message['content'])
    return response.choices[0].message['content']

def generate_questions_from_text(text, question_count,difficulty):
    prompt = f"""
    You are an intelligent person to generate questions. Your answers and correct answers must be correct 100% and meaningful. 
    Generate {question_count} multiple-choice {difficulty} questions from the following text.
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
    return response.choices[0].message['content']

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


    topic = st.text_area("Enter your topic")

    start = st.button("Generate Quiz")

    if start:
        if topic == "":
            inf("Please enter a topic to continue",2)
        else:
            if check_possibility(topic)=="NO":
                inf("Sorry, we cannot generate a quiz on this topic. Please try another one.",2)
            else:
                with st.spinner("Generating..."):
                    st.session_state['quiz'] = (generate_questions_from_text(topic,questions,difficulty_level))
                    st.session_state['stat'] = 1
                completed("Quiz generation completed")
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