from youtube_transcript_api import YouTubeTranscriptApi 


def fetch_transcript(videoId: str):    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(videoId)
        return transcript
    except Exception as e:
        return f'Error: {e}'