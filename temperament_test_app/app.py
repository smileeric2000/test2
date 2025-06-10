import streamlit as st
from questions import questions
from score_logic import calculate_temperament, get_dominant_temperament
from utils import generate_pdf_report,  set_background
import time

st.set_page_config(page_title="Temperament Test", layout="centered")

set_background("Image_Data/temperaments1.png")


def intro():

    #Content area with semi-transparent background for readability
    st.markdown(
"""
        <div class="content-wrapper" style='text-align: center;'>
            <h1 style='color: #4B9CD3;'>🧠 Discover Your Temperament</h1>
            <p style='font-size: 1.1rem; color: #454545;'>
                Welcome to the <strong>Temperament Personality Test</strong> – a fun, insightful quiz designed to help you learn more about your natural behavior patterns, emotional tendencies, and social interactions.
            </p>
            <hr style='margin: 2rem 0;' />
            <h3 style='color: #6C63FF;'>📋 How It Works</h3>
            <ul style='text-align: left; color: #454545; max-width: 600px; margin: auto; font-size: 1.05rem;'>
                <li>💬 You’ll be asked <strong>20 questions</strong> about your behavior, reactions, and preferences.</li>
                <li>📊 At the end, we’ll analyze your answers and show you your <strong>dominant temperament</strong>.</li>
                <li>📄 You can optionally <strong>download your results</strong> as a PDF report.</li>
            </ul>
            <hr style='margin: 2rem 0;' />
            <p style='font-size: 1rem; color: #808080;'>
                Are you ready to learn more about yourself?
            </p>
        </div>
        <audio autoplay>
          <source src="https://www.soundjay.com/button/beep-07.wav" type="audio/wav">
        </audio>
        """,
        unsafe_allow_html=True
    )


    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.button("🚀 Start the Test", on_click=lambda: st.session_state.update({"page": 1}))
    st.markdown("</div>", unsafe_allow_html=True)




if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)
if "page" not in st.session_state:
    st.session_state.page = 0


#Animate text
def typing_effect(text, delay=0.03):
    container = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.markdown(f'<span style="font-size:{"30px"}; font-weight:bold;line-height: 1.5 ">{displayed_text}</span>', unsafe_allow_html = True)
        time.sleep(delay)


##CORRECTED
def questionnaire():
    #Initialize session state keys if they don't exist
    if "page" not in st.session_state:
        st.session_state.page = 1
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    
    q = questions[st.session_state.page - 1]
    question_key = f"q{st.session_state.page}_viewed"

    if not st.session_state.get(question_key, False):
        typing_effect(f"Question {st.session_state.page}: {q['question']}")
        st.session_state[question_key] = True
    else:
        st.subheader(f"Question {st.session_state.page}: {q['question']}")
    
    #Get current answer or default to None
    current_answer = st.session_state.answers[st.session_state.page - 1]
    
    #Create radio button with proper state management
    selected_option = st.radio(
        "Choose one:",
        options=list(q["options"].keys()),
        index=None if current_answer is None else list(q["options"].keys()).index(current_answer),
        key=f"question_{st.session_state.page}"  # Unique key per question
    )
    
    #Update answer only when a new selection is made
    if selected_option is not None:
        st.session_state.answers[st.session_state.page - 1] = selected_option
    
    col1, col2 = st.columns(2)
    
    #Back button with state protection
    if col1.button("Back"):
        # if st.session_state.page > 1:
        st.session_state.page -= 1
        st.rerun()
    
    #Next button with validation
    if col2.button("Next"):
        if selected_option is None:
            st.warning("Please select an option before proceeding")
        else:
            if st.session_state.page < len(questions):
                st.session_state.page += 1
            else:
                st.session_state.page += 1  #Proceed to see results
            st.rerun()
##CORRECTED

def results():
    mapped_answers = []
    for i, ans in enumerate(st.session_state.answers):
        temperament = questions[i]["options"].get(ans)
        if temperament:
            mapped_answers.append(temperament)
    
    score = calculate_temperament(mapped_answers)
    dominant = get_dominant_temperament(score)

    st.title("🎉 Your Temperament Result")
    if dominant:
        st.subheader(f"Dominant Temperament: {dominant}")
        descriptions = {
            "Choleric": "Natural leader, goal-oriented, confident.",
            "Sanguine": "Lively, social, expressive, people-person.",
            "Melancholic": "Thoughtful, analytical, often reserved.",
            "Phlegmatic": "Calm, steady, peaceful, diplomatic."
        }
        st.write(descriptions[dominant])

        
        if st.button("Try again", key="retry_button"):
            # Clear all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            # Force immediate rerun
            st.rerun()




        if st.download_button("📄 Download Report", file_name=f"{dominant}_report.pdf",
                              data=open(generate_pdf_report("User", dominant, descriptions[dominant]), "rb").read()):
            st.success("Report downloaded.")
    else:
        st.warning("Couldn't determine your temperament. Please complete all questions.")

#Page routing
if st.session_state.page == 0:
    intro()
elif 1 <= st.session_state.page <= len(questions):
    questionnaire()
else:
    results()
