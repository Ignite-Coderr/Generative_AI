import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from PIL import Image
from youtube_transcript_api import YouTubeTranscriptApi
import re
import io

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize client with API key
client = genai.Client(api_key=API_KEY)

# ---------------------- IMAGE GENERATOR ----------------------
st.title("AI Image Generator")
user_prompt = st.text_input("Enter a prompt for the image:")

if st.button("Generate Image"):
    if user_prompt:
        with st.spinner("Generating image..."):
            try:
                response = client.models.generate_images(
                    model="gemini-2.0-flash-exp-image-generation",
                    prompt=user_prompt,
                )

                if getattr(response, "images", None):
                    for idx, img in enumerate(response.images):
                        st.image(img.data, caption=f"Generated Image {idx + 1}")
                else:
                    st.warning("No image returned by the model.")
            except Exception as e:
                st.error(f"Error generating image: {e}")
    else:
        st.warning("Please enter a prompt to generate an image.")

# ---------------------- IMAGE CAPTIONING ----------------------
st.title("AI Image Caption Generator")

uploaded_image = st.file_uploader(
    "Upload an image for captioning:", type=["jpg", "jpeg", "png"]
)

if uploaded_image:
    img = Image.open(uploaded_image)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    if st.button("Generate Caption"):
        try:
            with st.spinner("Generating caption..."):
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                img_bytes = buf.getvalue()

                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[
                        "Describe the content of the image in a short caption.",
                        {
                            "inline_data": {
                                "data": img_bytes,
                                "mime_type": "image/png",
                            }
                        },
                    ],
                )

                st.subheader("Generated Caption:")
                st.write(response.text)
        except Exception as e:
            st.error(f"Error generating caption: {e}")

# ---------------------- YOUTUBE VIDEO SUMMARIZER ----------------------
st.title("AI YouTube Video Summarizer")
youtube_url = st.text_input("Enter YouTube Video URL")

if st.button("Summarize Video"):
    if not youtube_url:
        st.warning("No YouTube URL Present!")
    else:
        try:
            match = re.search(r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{11})", youtube_url)
            if not match:
                st.error("Could not extract video ID.")
            else:
                video_id = match.group(1)

                with st.spinner("Fetching transcript and generating summary..."):
                    # Get English transcript
                    transcript = YouTubeTranscriptApi.get_transcript(
                        video_id, languages=["en"]
                    )

                    transcript_text = " ".join(t["text"] for t in transcript)

                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[
                            "Summarize this YouTube video in concise paragraphs.",
                            transcript_text,
                        ],
                    )

                    st.subheader("Video Summary")
                    st.write(response.text)

        except Exception as e:
            st.error(f"Error generating summary: {e}")