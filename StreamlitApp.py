import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable, TooManyRequests
import pandas as pd
import io

load_dotenv()  # Load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """ You are a YouTube video summarizer. You will be taking the transcript 
text from a chess tutorial video and summarizing the entire video. Your summary should 
provide the key points and important details, focusing on the positions of the chess 
pieces and the moves described in the tutorial. Ensure that the summary is 
concise and within 250 words.  

Input:

A transcript of the chess tutorial video, where the tutor explains various moves on a chessboard.
Output:

A summary of the video in bullet points, highlighting the critical moves and positions of the chess pieces on the board.

Instructions:

* Read through the transcript of the chess tutorial video.
* Extract the key moves and positions described by the tutor.
* Summarize these points in a clear and concise manner, using bullet points.
* Ensure the summary is within 250 words and captures the essence of the tutorial.

Tutor: "Let's start with the opening move, pawn to e4. Now, black responds with pawn to e5. 
White knight goes to f3, attacking the pawn on e5. Black knight to c6 to defend the pawn. 
Next, white bishop to b5, putting pressure on the knight..."

Example Output:

Opening move: White pawn to e4.
Black responds with pawn to e5.
White knight moves to f3, attacking black's e5 pawn.
Black knight moves to c6, defending the pawn.
White bishop moves to b5, applying pressure on black's knight on c6.

Note:

Use standard algebraic notation for chess moves (e.g., "e4", "Nf3", "Bb5").
Focus on summarizing the sequence of moves and their implications on the game.
Ensure the summary is coherent and provides a clear understanding of the tutorial's key points.

"""

# Function to extract the video ID from a YouTube URL
def extract_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        return None

# Getting the transcript data from YouTube videos
def extract_transcript_details(video_id):
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item["text"] for item in transcript_data])
        return transcript
    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except NoTranscriptFound:
        return "No transcripts found for this video."
    except VideoUnavailable:
        return "Video is unavailable."
    except TooManyRequests:
        return "Too many requests. Please try again later."
    except Exception as e:
        return f"An error occurred: {e}"

# Getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Function to convert response to CSV format
def convert_to_csv(response):
    df = pd.DataFrame({"Response": [response]})
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

st.sidebar.title("Rishi Academy")
youtube_link = st.sidebar.text_input("Enter YouTube Video Link:")

video_id = None
if youtube_link:
    video_id = extract_video_id(youtube_link)
    if video_id:
        st.sidebar.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    else:
        st.sidebar.error("Invalid YouTube link. Please provide a valid URL.")

if st.sidebar.button("Get Detailed Notes"):
    if not video_id:
        st.sidebar.error("Invalid YouTube link. Please provide a valid URL.")
    else:
        transcript_text = extract_transcript_details(video_id)
        if "An error occurred" in transcript_text or "Transcripts are disabled" in transcript_text or "No transcripts found" in transcript_text or "Video is unavailable" in transcript_text or "Too many requests" in transcript_text:
            st.sidebar.error(transcript_text)
        else:
            summary = generate_gemini_content(transcript_text, prompt)
            st.title("Rishi Academy")
            st.markdown("## Detailed Notes:")
            st.write(summary)
            csv_data = convert_to_csv(summary)
            st.download_button(
                label="Download",
                data=csv_data,
                file_name='Notes.txt',
                mime='text/csv'
            )
