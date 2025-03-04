import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai

# Fetch Google API Key from environment variable
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini model (Updated to use 'gemini-1.5-flash')
def get_gemini_response(input, image, prompt):
    # Use the new 'gemini-1.5-flash' model
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to process the uploaded image
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize the Streamlit app
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini Application")

# Get input prompt from the user
input = st.text_input("Input Prompt: ", key="input")

# File uploader for the image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Submit button to trigger the request
submit = st.button("Tell me about the image")

# Default input prompt for understanding invoices
input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices & 
               you will have to answer questions based on the input image.
               """

# If the submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    
    # Display the response from Gemini API
    st.subheader("The Response is")
    st.write(response)
