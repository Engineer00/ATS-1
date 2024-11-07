import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import pdf2image
import google.generativeai as genai
import base64
import io

# Load environment variables from .env file
load_dotenv()

# Set the Google API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Function to extract the content from the uploaded PDF
def input_pdf_setup(uploaded_file):
    # Check if file is uploaded
    if not uploaded_file:
        raise FileNotFoundError("No file uploaded")
    
    # Convert the PDF to images using pdf2image
    images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=r"C:\Program Files (x86)\poppler\library\bin")
    
    first_page = images[0]
    
    # Convert the first page image to bytes
    img_byte_arr = io.BytesIO()
    first_page.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    pdf_parts = [
        {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
        }
    ]
    return pdf_parts

# Function to interact with Google's Gemini AI model
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

# Streamlit app setup
st.set_page_config(page_title="ATS")
st.header("ATS Tracking System")

# User inputs
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload PDF File", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

# Submission buttons
submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")

# Prompts for the AI model
input_prompt1 = """
You are an experienced Technical Human Resource Manager focused on hiring team leads and managers. Your task is to review the provided resume against the job description for the uploaded resume.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of Management and Team Leadership roles and the years of experience required for the mentioned roles regarding the uploaded resume and ATS functionality.
Your task is to evaluate the resume against the provided job description. Provide a match percentage, followed by missing keywords, and conclude with final thoughts.
"""

# Handle button submissions
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("Response:")
        st.write(response)
    else:
        st.warning("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("Response:")
        st.write(response)
    else:
        st.warning("Please upload the resume")

