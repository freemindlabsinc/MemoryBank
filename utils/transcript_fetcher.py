from youtube_transcript_api import YouTubeTranscriptApi 


def fetch_transcript(videoId: str):    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(videoId, languages=['en'])
        return transcript
    except Exception as e:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(videoId, languages=['en-GB'])
            return transcript
        except Exception as e:
            return f'Error: {e}'