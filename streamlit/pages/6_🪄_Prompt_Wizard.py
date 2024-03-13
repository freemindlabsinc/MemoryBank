import streamlit as st
from utils.prompt_fetcher import get_predefined_prompts
from utils.llm import get_completion_stream
from utils.transcript_fetcher import fetch_transcript
from utils.webpage_fetcher import fetch_webpage
import time

st.set_page_config(
     page_title="Prompt Wizard",
     page_icon="🪄"
     )

prompts, def_prompt_index = get_predefined_prompts(
     prompt_dir='prompts',
     default_prompt='extract_wisdom')

col1, col2 = st.columns([4, 1])

# -Xtf6dk0ngI
if 'youtube_id' not in st.session_state:
    st.session_state.youtube_id = '-Xtf6dk0ngI'
if 'transcript' not in st.session_state:
    st.session_state.transcript= ''
if 'url' not in st.session_state:
    st.session_state.url = 'https://alessandros-blog.ghost.io/'

def download_transcript():
     vid = st.session_state.youtube_id
     trans = fetch_transcript(vid)
     st.session_state.transcript = trans

def fetch_url():
     url = st.session_state.url
     content = fetch_webpage(url)
     st.session_state.transcript = content

# -------------------


st.header("🪄Prompt Wizard")

with col1:               
     selected = st.selectbox(
          label='Select a prompt', 
          options=[prompt for prompt in prompts],
          index=def_prompt_index,
          format_func=lambda x: x.title,)

if not selected:    
     exit()
          
with col2:
     with st.popover("Click to see Prompt"):
          if (selected.system_content is not None):
               st.markdown(f'### System Prompt')
               st.markdown(selected.system_content)



st.session_state.youtube_id = st.text_input('YouTube Video Id', 
                                            value=st.session_state.youtube_id)

st.button('Download Transcript', 
          on_click=download_transcript)

st.session_state.url = st.text_input('Web Page URL', 
                                      value=st.session_state.url)

st.button('Scrape Web Page', 
          on_click=fetch_url)


user_content = st.text_area('User Text', max_chars=25000, height=300, 
                             value=st.session_state.transcript)
     
process = st.button('Process Prompt')
if process:                            
     def stream_response():
          stream = get_completion_stream(selected, user_content)     
          for chunk in stream:
               choice = chunk.choices[0].delta.content
               yield choice          
     
     st.write_stream(stream_response)