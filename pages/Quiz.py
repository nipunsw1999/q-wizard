import streamlit as st
import json 

if 'stat' not in st.session_state:
    st.session_state['stat'] = 0

if st.session_state['stat'] == 0:
    st.subheader("Create quiz first")
    st.page_link("Home.py", label=":red[Click here]", icon="👉")

elif st.session_state['stat'] == 1:
    if 'quiz' not in st.session_state:
        st.session_state['quiz'] = "" 
    # Parse quiz_data correctly
    st.page_link("Home.py", label=":green[Wanna customize again? Click here]")
    if isinstance(st.session_state['quiz'], str):
        quiz_data = json.loads(st.session_state['quiz'])
    else:
        quiz_data = st.session_state['quiz']


    # Initialize session state for answers
    if 'given_answers' not in st.session_state:
        st.session_state.given_answers = {}

    # Function to display a question
    def show_question(id, question, answers, correct_answers, explanation, status):
        with st.container(border=True):
            st.write(f":blue[({id}). {question}]")
            selected_answers = []
            
            if status == "YES":
                for i, answer in enumerate(answers, start=1):
                    st.write(f"({i}). {answer}")
            else:
                for i, answer in enumerate(answers, start=1):
                    if st.checkbox(f"({i}). {answer}", key=f"{id}_{answer}"):
                        selected_answers.append(answer)
            
            # Display explanation and correct answers after submission (optional, controlled elsewhere)
            return {
                "selected": selected_answers,
                "correct_answers": correct_answers,
                "explanation": explanation,
            }


    for id, data in quiz_data.items():
        result = show_question(
            id, 
            data["question"], 
            data["answers"], 
            data["correct_answers"], 
            data["explanation"], 
            data["status"]
        )
        st.session_state.given_answers[id] = result

    if st.button("Submit"):
        st.session_state['stat'] = 2
        st.toast(":green[Quiz Completed!]🎉🎉🎉")
        st.page_link("pages/Quiz Result.py", label=":red[Check answers]", icon="👉")

else:
    st.subheader("You completed the quiz!")
    st.page_link("pages/Quiz Result.py", label=":red[Check marks]", icon="👉")  