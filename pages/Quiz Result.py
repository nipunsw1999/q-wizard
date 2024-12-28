import streamlit as st
import json 

if 'stat' not in st.session_state:
    st.session_state['stat'] = 0


def get_grade_and_message(percentage):
    if percentage >= 90:
        grade = "A+"
        message = "Excellent work! You're a true expert."
    elif percentage >= 85:
        grade = "A"
        message = "Great job! You nailed it!"
    elif percentage >= 80:
        grade = "A-"
        message = "Fantastic effort! You're almost at the top."
    elif percentage >= 75:
        grade = "B+"
        message = "Good work! Keep it up."
    elif percentage >= 70:
        grade = "B"
        message = "Nice job! You're doing well."
    elif percentage >= 65:
        grade = "B-"
        message = "Not bad! A little more effort will go a long way."
    elif percentage >= 60:
        grade = "C+"
        message = "Fair attempt! Keep pushing."
    elif percentage >= 55:
        grade = "C"
        message = "You passed, but there's room for improvement."
    elif percentage >= 50:
        grade = "C-"
        message = "Just made it! Aim higher next time."
    elif percentage >= 45:
        grade = "D+"
        message = "Below average. Focus on improving."
    elif percentage >= 40:
        grade = "D"
        message = "Needs improvement. Don't give up!"
    elif percentage >= 35:
        grade = "D-"
        message = "Struggling. Time to hit the books."
    else:
        grade = "E"
        message = "Poor performance. Let's work on this together."
    return grade, message

if st.session_state['stat'] == 0:
    st.subheader("Create quiz first")
    st.page_link("Home.py", label=":red[Click here]", icon="👉")

elif st.session_state['stat'] == 1:
    st.subheader("Complete quiz first")
    st.page_link("pages/Quiz.py", label=":red[Click here]", icon="👉")

else:
    if 'quiz' not in st.session_state:
        st.session_state['quiz'] = "" 

    if isinstance(st.session_state['quiz'], str):
        quiz_data = json.loads(st.session_state['quiz'])
    else:
        quiz_data = st.session_state['quiz']
        
    if 'given_answers' not in st.session_state:
        st.session_state.given_answers = {}
    st.subheader("Submitted Answers:")
    total = 0
    grand_total = 0
    for id, result in st.session_state.given_answers.items():
        with st.container(border=True):
            st.write(f":blue[({id}). {quiz_data[str(id)]['question']}]")  # Ensure id is treated as a string
            wrong_answers = 0
            correct_answers = 0
            weight = float(len(result['correct_answers']))
            for i, answer in enumerate(quiz_data[str(id)]['answers'], start=1):
                if answer in result['selected']:
                    if answer in result['correct_answers']:
                        correct_answers += 1
                        st.write(f":green[({i}). {answer} ✓]")
                    else:
                        wrong_answers += 1
                        st.write(f":red[({i}). {answer} ✗]")
                else:
                    if answer in result['correct_answers']:
                        st.write(f":green[({i}). {answer}]")
                    else:
                        st.write(f"({i}). {answer}")
            st.write(f"Explanation: {result['explanation']}")
            marks = correct_answers - (wrong_answers * 0.5)
            st.write(f":orange[Marks: {marks}/{weight}]")
            total += marks
            grand_total += weight
            percentage = total * 100 / grand_total
            grade, message = get_grade_and_message(percentage)
    if percentage > 50:
        st.header(f":green[Full marks: {percentage:.2f}%]")
        st.subheader(f":green[Grade: {grade}] 🎉")
        st.write(f":violet[{message}]")
    else:
        st.header(f":red[Full marks: {percentage:.2f}%]")
        st.subheader(f":red[Grade: {grade}] 😕")
        st.write(f":violet[{message}]")
    st.divider()
    st.page_link("Home.py", label=":green[Try Again]", icon="✍️")
