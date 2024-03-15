import streamlit as st
from utils.prompt_fetcher import get_predefined_prompts
from utils.llm import get_completion_stream
from utils.transcript_fetcher import fetch_transcript
from utils.webpage_fetcher import fetch_webpage
import pandas as pd

st.set_page_config(
     page_title="Prompt Wizard",
     page_icon="🪄"
     )

prompts, def_prompt_index = get_predefined_prompts(
     prompt_dir='prompts',
     default_prompt='summarize_micro')
     #default_prompt='extract_wisdom')

# -Xtf6dk0ngI
if 'youtube_id' not in st.session_state:
    st.session_state.youtube_id = 'https://www.youtube.com/watch?v=iVbN95ica_k'
if 'transcript' not in st.session_state:
    st.session_state.transcript= ''
if 'url' not in st.session_state:
    st.session_state.url = ''
if 'openai_key' not in st.session_state:
    st.session_state.openai_key = '#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'    
if 'model' not in st.session_state:
    st.session_state.model = 'gpt-3.5-turbo'

def download_transcript(video_id: str):
     # if the video id is a url, then if the domain is youtu.be (like https://youtu.be/xZgZLOq1JKU)
     # then the video id is the last part of the url, excluding anything after a ? 
     # otherwise, if the video is of www.youtube.com (like ) https://www.youtube.com/watch?v=xZgZLOq1JKU)
     # then extract the value of the query parameter v
     if 'youtu.be' in video_id:
          video_id = video_id.split('/')[-1].split('?')[0]
     elif 'youtube.com' in video_id:
          video_id = video_id.split('v=')[-1].split('&')[0]
     
     transcript = fetch_transcript(video_id)
     st.session_state.youtube_id = video_id
     st.session_state.transcript = transcript

def fetch_url(url: str):
     #url = st.session_state.url
     content = fetch_webpage(url)
     st.session_state.url = url    
     st.session_state.transcript = content

# -------------------

st.header("🪄Prompt Wizard")

# add a text box to enter openai_key as a password
st.session_state.openai_key = st.text_input(
     'OpenAI API Key', 
     type='password', 
     placeholder='Enter your OpenAI API Key here...',
     value=st.session_state.openai_key)

st.session_state.model = st.selectbox(
          'Model',
          ("gpt-4-1106-preview", "gpt-4-32k-0613", "gpt-3.5-turbo"),
          
          )

if (st.session_state.openai_key == ''):
     #st.warning('Please enter your OpenAI API Key')
     exit()

# create tabs for youtube and url
youtube_tab, webpage_tab = st.tabs(["YouTube", "Web Page"])
with youtube_tab:
     st.session_state.youtube_id = st.text_input(
          'YouTube Video', 
          placeholder='Enter YouTube Video url or the id of the video.',
          value=st.session_state.youtube_id)

     st.button('Download Transcript', 
               on_click=download_transcript,
               args=[st.session_state.youtube_id]
               )

with webpage_tab:
     st.session_state.url = st.text_input(
          'Web Page', 
          placeholder='Enter the url of the web page to scrape.',
          value=st.session_state.url)

     st.button('Scrape Web Page', 
               on_click=fetch_url,
               args=[st.session_state.url])
     


if not st.session_state.youtube_id and not st.session_state.url:    
     exit()  

if st.session_state.transcript == '':
     exit()
     
     
# Text
st.divider()     

with st.expander(f"Downloaded Text"):
     st.session_state.transcript = st.text_area('Text', 
                                           max_chars=25000, 
                                           height=300, 
                                           value=st.session_state.transcript)

st.divider()
     
# Convert the list of PredefinedPrompt objects to a DataFrame
prompts_df = pd.DataFrame([vars(prompt) for prompt in prompts])

              
prompt_sequence = st.multiselect(
          'Prompts Pipeline',
          prompts_df,
          ["summarize_micro"],
          #["a_facebook_post_creator"],   
          )
     
with st.expander("Pipelines Instructions"):
     for selected in prompt_sequence:
          selected = prompts_df[prompts_df['title'] == selected].iloc[0]
          
          # write the title as a green header in markdown               
          st.markdown(f'### 📜:green[{selected.title}]')                            
          st.markdown(f'{selected.system_content}')
          st.divider()

st.write('You selected:', prompt_sequence)


# End of df

if not prompt_sequence:    
     exit()          

     
process = st.button('Process Prompt')
if process:    
     st.divider()
     def stream_response():
          tabs = st.tabs(prompt_sequence)
          
          tab_idx = 0
          for selected in prompt_sequence:               
               tab = tabs[tab_idx]               
               tab_idx += 1
               with tab:
                    #find the matching Prompt from prompts where the title is the same as selected
                    selected = prompts_df[prompts_df['title'] == selected].iloc[0]
                                                            
                    st.subheader(selected.title)
                              
                    stream = get_completion_stream(
                         prompt=selected, 
                         input_data=st.session_state.transcript,
                         openai_key=st.session_state.openai_key,
                         model=st.session_state.model
                         )     
                    for chunk in stream:
                         choice = chunk.choices[0].delta.content
                         yield choice          
                         
                    st.divider()
          
     st.write_stream(stream_response)