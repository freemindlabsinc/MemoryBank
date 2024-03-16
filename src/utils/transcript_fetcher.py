from youtube_transcript_api import YouTubeTranscriptApi 


def fetch_transcript(video_id: str):        
    try:
        # https://youtu.be/xZgZLOq1JKU?more=stuff
        # https://www.youtube.com/watch?v=xZgZLOq1JKU?more=stuff
        # then extract the value of the query parameter v
        if 'youtu.be' in video_id:
            video_id = video_id.split('/')[-1].split('?')[0]
        elif 'youtube.com' in video_id:
            video_id = video_id.split('v=')[-1].split('&')[0]         
    
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        return transcript
    except Exception as e:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en-GB'])
            return transcript
        except Exception as e:
            return f'Error: {e}'