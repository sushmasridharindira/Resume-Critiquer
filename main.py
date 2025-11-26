import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() #Load environment variable from dotenv file

st.set_page_config(page_title = "AI Resume Critiquer" , layout = "centered") #Configure name of the tab or page

st.title("AI Resume Critiquer")
st.markdown("Upload your resume and get AI-powered feedback tailored to your needs!")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload your resume (PDF or Text)" , type = ["pdf","txt"])
job_role = st.text_input("Enter the job role you are targetting")

analyze = st.button("Analyze Resume")

def extract_text_from_pdf(pdf_file): #Extracts the data from pdf and appends to the text field
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type =="application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read())) #Load the uploaded file and convert it to BytesIO and call the function
    return uploaded_file.read().decode("utf-8") #If it's not a pdf then read the txt file

if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("File doesn't have any content")
            st.stop()

        prompt = f"""Please analyze this resume and provide constructive feedback. 
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience descriptions
        4. Specific improvements for {job_role if job_role else 'general job applications'}
        
        Resume content:
        {file_content}
        
        Please provide your analysis in a clear, structured format with specific recommendations."""
    
        client = OpenAI(api_key = OPENAI_API_KEY)
        response = client.chat.completions.create(
            model = "gpt-4o-mini" , 
             messages=[
                    {"role": "system", "content": "You are an expert resume reviewer with years of experience in HR and recruitment."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
        )
        #st.markdown ("Analysis Results")
        st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"An error occured: {str(e)}")
    
