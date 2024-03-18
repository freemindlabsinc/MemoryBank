import streamlit as st
import src.utils.prompt_fetcher as prompt_fetcher
import src.utils.llm as llm
import src.utils.transcript_fetcher as transcript_fetcher 
import src.utils.webpage_fetcher as webpage_fetcher
import src.components.page_configurator as page_config
import src.components.formatting_utils as formatting_utils
import pandas as pd

page_config.initialize_page(
     "🪄", 
     "Prompt Wizard", 
     """This module lets you import resources from the web 
     and run one or multiple prompts on the imported data""")

page_config.initialize_session_state({
     'youtube_id': 'https://www.youtube.com/watch?v=iVbN95ica_k',
     'transcript': '',
     'url': '',
     'openai_key': 'lemmein',
     'model': 'gpt-3.5-turbo'
     })

prompts = prompt_fetcher.get_predefined_prompts()

def download_transcript(video_id: str):    
     transcript = transcript_fetcher.fetch_transcript(video_id)
     st.session_state['youtube_id'] = video_id
     st.session_state['transcript'] = transcript

def fetch_url(url: str):
     content =  webpage_fetcher.fetch_webpage(url)
     st.session_state['url'] = url    
     st.session_state['transcript'] = content

# -------------------


# add a text box to enter openai_key as a password
st.text_input('OpenAI API Key', 
              type='password', 
              placeholder='Enter your OpenAI API Key here...',
              key='openai_key')

st.selectbox('Model',
             ("gpt-3.5-turbo", "gpt-4-1106-preview"),
             key='model')

# create tabs for youtube and url
youtube_tab, webpage_tab = st.tabs(["YouTube", "Web Page"])

with youtube_tab:
     st.text_input('YouTube Video',                
                   placeholder='Enter YouTube Video url or the id of the video.',
                   key='youtube_id')
     
     st.button('Download Transcript', 
               on_click=download_transcript,
               disabled=st.session_state['youtube_id'] == '',
               args=[st.session_state['youtube_id']])

with webpage_tab:
     st.text_input(
          'Web Page', 
          placeholder='Enter the url of the web page to scrape.',
          key='url')

     st.button('Scrape Web Page', 
               on_click=fetch_url,
               disabled=st.session_state['url'] == '',
               args=[st.session_state['url']])

# Text
st.divider()     

with st.expander(f"Downloaded Text", 
                 expanded= st.session_state['transcript'] != ''):     
     st.text_area('Text', 
                  max_chars=25000, 
                  height=300,                                                                                   
                  key='transcript')

st.divider()
     
# Convert the list of PredefinedPrompt objects to a DataFrame
prompts_df = pd.DataFrame([vars(prompt) for prompt in prompts])

selections = formatting_utils.get_fancy_captions(prompts)                  
st.multiselect('Prompts Pipeline',
               selections,
               [selections[0]],   
               key='selected_prompt_names')

fancy_names = st.session_state['selected_prompt_names']

pipeline = []
for fancy_name in fancy_names:
     prompt = formatting_utils.get_prompt_by_fancy_caption(fancy_name, prompts)     
     pipeline.append(prompt)
     
process = st.button('Process Prompt')
if process:    
     st.divider()
     def stream_response():
          tab_names = [prompt.title for prompt in pipeline]
          tabs = st.tabs(tab_names)
          
          tab_idx = 0
          for prompt in pipeline:               
               tab = tabs[tab_idx]               
               tab_idx += 1
               with tab:
                    st.subheader(prompt.title)
                         
                    # open api key hack
                    if st.session_state.openai_key == 'lemmein':
                         key = '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'    
                    else:
                         key = st.session_state.openai_key                    
                              
                    stream = llm.get_completion_stream(
                         prompt=prompt, 
                         input_data=st.session_state.transcript,
                         openai_key=key,
                         model=st.session_state.model
                         )     
                    for chunk in stream:
                         choice = chunk.choices[0].delta.content
                         yield choice          
                         
                    st.divider()
          
     st.write_stream(stream_response)