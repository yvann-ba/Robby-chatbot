import os
import streamlit as st
import re
from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

st.set_page_config(layout="wide", page_icon="💬", page_title="Robby | Chat-Bot 🤖")

# Instantiate the main components
layout, sidebar, utils = Layout(), Sidebar(), Utilities()

st.markdown(
    f"""
    <h1 style='text-align: center;'> Ask Robby to summarize youtube video ! 😁</h1>
    """,
    unsafe_allow_html=True,
)

user_api_key = utils.load_api_key()

sidebar.about()

if not user_api_key:
    layout.show_api_key_missing()

else:
    utils.set_api_key_env(user_api_key)

    def get_youtube_id(url):
        video_id = None
        match = re.search(r"(?<=v=)[^&#?]+", url)
        if match:
            video_id = match.group()
        else: 
            match = re.search(r"(?<=youtu.be/)[^&#?]+", url)
            if match:
                video_id = match.group()
        return video_id

    def get_transcript(video_id):
        """
        Get transcript using youtube-transcript-api v1.0+ API
        """
        from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
        
        # Create instance of YouTubeTranscriptApi
        ytt_api = YouTubeTranscriptApi()
        
        try:
            # Fetch transcript - try different languages
            transcript = ytt_api.fetch(
                video_id, 
                languages=['en', 'fr', 'es', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh-Hans']
            )
        except (TranscriptsDisabled, NoTranscriptFound):
            # Try auto-generated captions
            try:
                transcript = ytt_api.fetch(video_id)  # Try any available transcript
            except Exception as e:
                raise ValueError(f"No transcript available for this video. The video may have disabled subtitles or no captions exist.") from e
        except VideoUnavailable:
            raise ValueError("This video is unavailable or private.")
        
        # Build transcript text from snippets
        transcript_text = ""
        for snippet in transcript:
            transcript_text += snippet.text + " "
        
        return transcript_text.strip()

    video_url = st.text_input(placeholder="Enter Youtube Video URL", label_visibility="hidden", label=" ")
    if video_url:
        video_id = get_youtube_id(video_url)

        if video_id:
            try:
                with st.spinner("Fetching transcript and summarizing..."):
                    # Get transcript as string
                    transcript_text = get_transcript(video_id)
                    
                    # Create a summarization LLM using the selected provider
                    provider = st.session_state.get("provider", "OpenAI")
                    model = st.session_state.get("model", "gpt-4o-mini")

                    if provider == "MiniMax":
                        llm = ChatOpenAI(
                            temperature=0.01,
                            model=model,
                            openai_api_key=os.environ.get("MINIMAX_API_KEY", ""),
                            openai_api_base="https://api.minimax.io/v1",
                        )
                    else:
                        llm = ChatOpenAI(temperature=0, model=model)
                    
                    prompt = PromptTemplate(
                        input_variables=["text"],
                        template="""Please provide a comprehensive summary of the following YouTube video transcript. 
                        
Include:
- Main topics discussed
- Key points and takeaways
- Any important details or conclusions

Transcript:
{text}

Summary:"""
                    )
                    
                    # For longer transcripts, chunk it
                    max_chars = 15000
                    if len(transcript_text) > max_chars:
                        transcript_text = transcript_text[:max_chars] + "..."
                    
                    chain = prompt | llm
                    response = chain.invoke({"text": transcript_text})
                    
                    st.subheader("Summary")
                    st.write(response.content)
                    
                    with st.expander("View Transcript"):
                        st.write(transcript_text)
                        
            except Exception as e:
                st.error(f"Error processing video: {str(e)}")
        else:
            st.error("Invalid YouTube URL. Please enter a valid URL.")
