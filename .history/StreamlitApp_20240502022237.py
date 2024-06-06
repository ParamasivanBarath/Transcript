"""
import streamlit as st
from dotenv import load_dotenv
import json
import html

load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("Google_Api_Key"))

prompt=You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  


## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if len(splitted_html) <= 1:
        if video_id.startswith('http://') or video_id.startswith('https://'):
            raise InvalidVideoId(video_id)
        if 'class="g-recaptcha"' in html:
            raise TooManyRequests(video_id)
        splitted_html = html.split('"playabilityStatus":')
        if len(splitted_html) <= 1:
            raise VideoUnavailable(video_id)
        
        playability_status_json = json.loads(
            splitted_html[1].split(',"WHAT_EVER_THE_NEXT_PROPERTY_IS')[0].replace('\n', '')
        )

        # ... handle playability_status_json ...

        # fallback if we don't know the status
        raise TranscriptsDisabled(video_id)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)

"""
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai
from google.cloud import speech_v1p1beta1 as speech

load_dotenv()  # load all the environment variables

genai.configure(api_key=os.getenv("Google_Api_Key"))

prompt = """You are YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """


# Transcribe video audio to text using Google Cloud Speech-to-Text
def transcribe_video(youtube_video_url):
    video_id = youtube_video_url.split("=")[1]
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    client = speech.SpeechClient()
    config = {
        "language_code": "en-US",
    }
    audio = {"uri": video_url}

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "

    return transcript


# Generate notes using Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text


st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

    if st.button("Get Detailed Notes"):
        transcript_text = transcribe_video(youtube_link)

        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("## Detailed Notes:")
            st.write(summary)
