import streamlit as st
import src.utils.prompt_fetcher as prompt_fetcher
import src.utils.llm as llm
import src.utils.transcript_fetcher as transcript_fetcher 
import src.utils.webpage_fetcher as webpage_fetcher
import src.components.page_configurator as page_config
import src.components.formatting_utils as formatting_utils

page_config.initialize_page(
     "🪄", 
     "Prompt Wizard", 
     """This module lets you prompts from your library against your data.     
You can either :green[type some text], :orange[download transcripts from YouTube videos] or :blue[scrape web pages], and then 
use them to generate completions using one or more prompts.""")

page_config.initialize_session_state({
     'youtube_id': 'https://www.youtube.com/watch?v=iVbN95ica_k',
     'transcript': '',
     'url': 'https://alessandros-blog.ghost.io/',
     #'openai_key': 'lemmein',
     'model': 'gpt-4-1106-preview',
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
#st.text_input('OpenAI API Key', 
#              type='password', 
#              placeholder='Enter your OpenAI API Key here...',
#              key='openai_key')

expander_color = ":blue"
label_color = ":orange"

with st.expander(f"{expander_color}[LLM Options]", expanded=True):
     model_col, temperature_col = st.columns([3, 1])
     
     with model_col:
          st.selectbox('Model',
             ("gpt-3.5-turbo", "gpt-4-1106-preview"),             
             key='model')
     
     with temperature_col:
          st.slider('Temperature :gray[[soon]]', 
                    min_value=0.0, 
                    max_value=1.0, 
                    value=0.7,
                    step=0.1,                    
                    key='temperature',
                    help="Affects randomness: lower values make the model more deterministic and confident.")
     
with st.expander(f"{expander_color}[Advanced] :gray[[soon]]", expanded=False):
     top_p_col, frequency_penalty_col, presence_penalty = st.columns([1, 1, 1])
     with top_p_col:
          st.slider('Top P', 
                    min_value=0.0, 
                    max_value=1.0, 
                    value=0.9,
                    step=0.1,
                    key='top_p',
                    help="Controls diversity via nucleus sampling: lower values make responses more deterministic.")
          
     with frequency_penalty_col:
          st.slider('Frequency Penalty', 
                    min_value=-2.0, 
                    max_value=2.0, 
                    value=0.1,
                    step=0.1,
                    key='frequency_penalty',
                    help="Discourages repetition of words: higher values prevent repeating the same information.")
          
     with presence_penalty:
          st.slider('Presence Penalty', 
                    min_value=-2.0, 
                    max_value=+2.0, 
                    value=0.1,
                    step=0.1,
                    key='presence_penalty',
                    help="Encourages the model to mention new concepts: higher values make repetitions less likely.")                    

with st.expander(f"{expander_color}[Download Tools]", expanded=False):
     # create tabs for youtube and url
     youtube_tab, webpage_tab = st.tabs(["▶️YouTube", "🕸️Web Page"])

     with youtube_tab:
          st.text_input('YouTube Video',                
                    placeholder='Enter the address or id of a YouTube Video.',
                    #help="Download the video transcript (e.g. ).",
                    key='youtube_id')
          
          st.button('Download Transcript', 
                    on_click=download_transcript,
                    help="Downloads the transcript of the YouTube video.",
                    disabled=st.session_state['youtube_id'] == '',
                    args=[st.session_state['youtube_id']])

     with webpage_tab:
          st.text_input(
               'Web Page', 
               placeholder='Enter the address of the web page to scrape.',               
               key='url')

          st.button('Scrape Web Page', 
                    help="Download the content of the web page.",
                    on_click=fetch_url,
                    disabled=st.session_state['url'] == '',
                    args=[st.session_state['url']])

with st.expander(f"{expander_color}[Text]", expanded=True):
     st.text_area('Text', 
                  label_visibility="collapsed",
                  max_chars=25000, 
                  height=300,                                                                                   
                  key='transcript')

     
# Convert the list of PredefinedPrompt objects to a DataFrame
#prompts_df = pd.DataFrame([vars(prompt) for prompt in prompts])
#selections = formatting_utils.get_fancy_captions(prompts)                  
with st.expander(f"{expander_color}[Prompts Pipeline]", expanded=True):
     col1, col2 = st.columns([4, 1])
     
     with col1:
          def_prompt = next((x for x in prompts if x.title == 'Summarize'), None)
          
          st.multiselect(' ',
                         prompts,
                         [def_prompt],  
                         format_func=lambda x: f"{x.icon} {x.title}",
                         key='selected_prompts',
                         label_visibility='collapsed',
                         )

     with col2:
          pipeline = st.session_state['selected_prompts']    
          process = st.button('Execute')
          
if process:         
     def stream_response():
          tab_names = [prompt.title for prompt in pipeline]
          
          tabs = st.tabs(tab_names)
          
          tab_idx = 0
          for prompt in pipeline:               
               tab = tabs[tab_idx]               
               tab_idx += 1
                              
               with tab:
                    st.subheader(prompt.title)
                         
                    # FIXME open api key hack
                    key = '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'    
                    tab_txt = ""
                                   
                    stream = llm.get_completion_stream(
                         prompt=prompt, 
                         input_data=st.session_state.transcript,
                         openai_key=key,
                         model=st.session_state.model)
                    
                    for chunk in stream:
                         choice = chunk.choices[0].delta.content
                         tab_txt += choice or ''
                         yield choice                    
                                        
     st.write_stream(stream_response)          
     