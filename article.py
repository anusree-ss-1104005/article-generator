import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")
print(f"Loaded API Key: {API_KEY}")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("API key is not set. Please configure the GEMINI_API_KEY environment variable.")

def generate_article(keywords, writing_style, word_count):
    try:
        prompt = f"Write a {writing_style} article of approximately {word_count} words about {keywords}."
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)       
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return ""

st.title("Article Generator")

keywords = st.text_input("Enter keywords:")
writing_style = st.selectbox("Choose writing style:", ["Formal", "Informal", "Technical", "Narrative"])
word_count = st.slider("Select word count:", 100, 2000)

if st.button("Generate"):
    if not API_KEY:
        st.error("API key is not set. Please configure the GEMINI_API_KEY environment variable.")
    else:
        article = generate_article(keywords, writing_style, word_count)
        if article:
            st.write(article)
            st.download_button(label="Download Article", data=article,file_name='article.txt', mime="text/txt")
