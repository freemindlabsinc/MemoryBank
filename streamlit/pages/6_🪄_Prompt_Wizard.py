import streamlit as st
from utils.prompt_fetcher import get_predefined_prompts, PredefinedPrompt
from utils.llm import complete
from utils.transcript_fetcher import fetch_transcript

st.set_page_config(
     page_title="Prompt Wizard",
     page_icon="🪄"
     )

st.header("🪄Prompt Wizard")
prompts = get_predefined_prompts('prompts')

col1, col2 = st.columns([4, 1])

with col1:
     # get the index of the prompt with title 'xxx'
     idx = next((i for i, prompt in enumerate(prompts) if prompt.title == 'extract_wisdom'), None)
     
     selected = st.selectbox(
          label='Select a prompt', 
          options=[prompt for prompt in prompts],
          index=idx,
          format_func=lambda x: x.title,)

if not selected:    
     exit()
          
with col2:
     with st.popover("See Prompt"):
          if (selected.system_content is not None):
               st.markdown(f'### System Prompt')
               st.markdown(selected.system_content)

# -Xtf6dk0ngI
if 'youtube_id' not in st.session_state:
    st.session_state.youtube_id = ''
if 'transcript' not in st.session_state:
    st.session_state.transcript= ''

def download_transcript():
     vid = st.session_state.youtube_id
     trans = fetch_transcript(vid)
     st.session_state.transcript = trans

st.session_state.youtube_id = st.text_input('YouTube Video Id')

st.button('Download Transcript', 
          on_click=download_transcript)

user_content = st.text_area('User Text', max_chars=25000, height=300, value=st.session_state.transcript)
     
process = st.button('Process Prompt')
if process:               
     response = complete(selected, user_content)
     st.markdown(response)


#st.dataframe(prompts)