import streamlit as st 

st.sidebar.image("logo.png", width=800) 
st.subheader("What is this app?")
st.write("This web app allows users to generate custom quizzes based on their chosen topic, difficulty level, and the number of questions. After completing the quiz, the app automatically grades the responses and provides a score, making it a convenient tool for learning and self-assessment.")
st.subheader("Who am I?")
st.image("pages/gen.jpg")
st.write("Hi, I'm :blue[Nipun Weerasinghe], a Computer Science undergraduate at the University of Jaffna. I’m passionate about technology, especially :green[machine learning, AI, and software development]. I’ve worked on a variety of projects, including chatbots and applications involving PDF embedding. I'm skilled in Python, Streamlit, and AI tools, and I enjoy tackling innovative challenges and exploring new solutions.")
st.subheader("Contact me")
st.page_link("https://www.linkedin.com/in/nipunweerasinghe?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app", label=":blue[Linkedin]")