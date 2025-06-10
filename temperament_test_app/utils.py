import streamlit as st
from fpdf import FPDF
import base64

def generate_pdf_report(name, temperament, description):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Temperament Test Result", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Temperament: {temperament}", ln=True)
    pdf.multi_cell(0, 10, txt=f"\nDescription:\n{description}")

    file_path = f"{name}_temperament_report.pdf"
    pdf.output(file_path)
    return file_path


def set_background(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
    }}
    .content-wrapper {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 12px;
        max-width: 800px;
        margin: auto;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)    
