import os
from dotenv import load_dotenv
import streamlit as st
import pyttsx3
import google.generativeai as genai
import speech_recognition as sr

# Load environment variables
load_dotenv()

# Configure the API key for Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key for Google Generative AI is missing. Please check your .env file.")
else:
    genai.configure(api_key=api_key)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set the voice to the default system voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Function to load Gemini Pro_Model and get a response
def get_gemini_response(question):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(question)
        return response.text if response else "Sorry, I couldn't find an answer."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to capture voice input
def capture_voice_input():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.write(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")
        return ""

# Initialize Streamlit application
st.set_page_config(page_title="Summer Internship Poornima")
st.header("Chat with Me")

input_method = st.radio("Input Method:", ('Text', 'Voice'))

if input_method == 'Text':
    input_text = st.text_input("Input:", key="input")
    submit = st.button("Ask the Question:")
    if submit and input_text:
        response = get_gemini_response(input_text)
        st.subheader("The response is:")
        st.write(response)
        
        # Use text-to-speech to say the response
        engine.say(response)
        engine.runAndWait()

        
elif input_method == 'Voice':
    if st.button("Capture Voice Input"):
        input_text = capture_voice_input()
        if input_text:
            response = get_gemini_response(input_text)
            st.subheader("The response is:")
            st.write(response)
            
            # Use text-to-speech to say the response
            engine.say(response)
            engine.runAndWait()
else:
    st.write("Please enter a question or capture voice input.")