import streamlit as st
from questions import questions
from score_logic import calculate_temperament, get_dominant_temperament
from utils import generate_pdf_report,  set_background
import time

st.set_page_config(page_title="Temperament Test", layout="centered")


img_64 = "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"

set_background(img_64)


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
