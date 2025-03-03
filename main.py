# API key website :- https://ai.google.dev/pricing
### WellnessAI Advisior
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

## configure the "genai" library by providing API key
genai.configure(api_key=os.getenv("API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="WellnessAI Advisior")

st.header("WellnessAI Advisior 👨‍⚕️")
uploaded_file = st.file_uploader("Choose an image..", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me about my meal")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
and calculate the total calories, also provide the details of every food items with calories intake
is below format
1. Item 1 - no of calories
2. Item 2 - no of calories
----
----
After that mention that the meal is healthy meal or not and also mention the percentage split of ratio of
carbohydrates,proteins, fats, sugar and calories in meal.
finally give suggestion which item should me removed and which items should be added it meal to make the
meal healthy if it's unhealthy
"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data)
    st.subheader("The Response is")
    st.write(response)


