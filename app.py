import os
import streamlit as st
import google.generativeai as genai

# Configure the Gemini API key using your environment variable
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key is not set. Please set the GOOGLE_API_KEY environment variable.")
else:
    genai.configure(api_key=api_key)

# Function to upload files to Gemini
def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    try:
        file = genai.upload_file(path, mime_type=mime_type)
        st.success(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",  # Update this to the model you're working with
    generation_config=generation_config,
)

# Streamlit interface
st.title("Image to Text Generator with Gemini API")
st.write("Upload an image and generate the corresponding text using Optical Character Recognition (OCR).")

# Upload image file
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png", "gif"])
if uploaded_file:
    # Save the uploaded file locally
    with open("temp_image.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Upload the file to Gemini
    file = upload_to_gemini("temp_image.jpg", mime_type="image/jpeg")

    # Start the chat session
    if file:
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": ["image to text\n"],
                },
                {
                    "role": "model",
                    "parts": [file],
                },
                {
                    "role": "user",
                    "parts": ["image to text generator\n"],
                },
                {
                    "role": "model",
                    "parts": [
                        "Okay, let's talk about image-to-text generation. You're asking about tools that can extract text from images, which is commonly known as **Optical Character Recognition (OCR)**. Here's a breakdown of what that means and some tools you can use:\n\n**What is Image-to-Text (OCR)?**\n\n* **Optical Character Recognition (OCR):** This is the technology that analyzes an image and identifies characters (letters, numbers, symbols) to convert them into editable and searchable text.\n* **How it works:** OCR software uses algorithms to:\n    * **Preprocess the image:** This involves cleaning up the image, enhancing contrast, and removing noise.\n    * **Identify characters:** It looks for patterns and shapes that correspond to known characters.\n    * **Reconstruct words and sentences:** It arranges the identified characters in the correct order to form meaningful text.\n    * **Correct errors:** Some OCR software uses dictionaries and context to correct any misidentified characters.\n\n**Why Use Image-to-Text?**\n\n* **Digitizing documents:** Convert scanned documents, PDFs, or photos of text into editable digital files.\n* **Extracting text from images:** Pull out text from screenshots, photos of signs, or other images where the text is not readily accessible.\n* **Making text searchable:**  Turn image-based text into something you can search, copy, and paste.\n* **Accessibility:** Makes text available to screen readers for people with visual impairments.\n\n**Types of Image-to-Text Generators**\n\nYou'll find a variety of tools for image-to-text, each with its own strengths and weaknesses:\n\n**1. Online OCR Tools:**\n\n* **Pros:**\n    * **Easy to use:** No installation required, accessible directly through your web browser.\n    * **Free options available:** Many offer free tiers for basic usage.\n    * **Convenient for occasional use:** Great for quick conversions.\n* **Cons:**\n    * **May have limitations:** Some free versions limit file sizes, page counts, or accuracy.\n    * **Privacy concerns:** Be mindful of uploading sensitive documents to online services.\n    * **Dependent on internet access:** You need an internet connection to use them.\n* **Examples:**\n    * **Google Docs:** Upload an image into Google Docs and the OCR processing is often automatic, allowing you to copy the converted text.\n    * **OnlineOCR.net:** A simple and straightforward online tool.\n    * **NewOCR.com:** Another good option for quick conversions.\n    * **i2OCR.com:** Supports many different languages.\n    * **FreeOCR.net:** A basic, free solution.\n\n**2. Software Applications (Desktop):**\n\n* **Pros:**\n    * **More powerful features:** Often offer more advanced settings and greater accuracy.\n    * **Offline processing:** Don't require an internet connection to run.\n    * **Better privacy:** Your data remains on your computer.\n* **Cons:**\n    * **Cost:** Most professional-grade software requires a purchase or subscription.\n    * **Installation required:** Needs to be installed on your computer.\n    * **May have a learning curve:** Some features can be complex.\n* **Examples:**\n    * **Adobe Acrobat Pro DC:** Includes a robust OCR engine for PDF and image conversion.\n    * **ABBYY FineReader:** One of the most accurate OCR software options available.\n    * **Microsoft OneNote:** Built-in OCR functionality for images and notes.\n    * **Readiris:** Another popular OCR software solution.\n\n**3. Mobile Apps:**\n\n* **Pros:**\n    * **Portable and convenient:** Ideal for scanning documents or images on the go.\n    * **Often free or low-cost:** Many free apps offer basic OCR functionality.\n* **Cons:**\n    * **Accuracy can vary:** May be less accurate than desktop software.\n    * **Limited features",
                    ],
                },
            ]
        )

        # Send a message to the model and display the result
        response = chat_session.send_message("INSERT_INPUT_HERE")
        st.write(response.text)
