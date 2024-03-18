import streamlit as st
import src.components.page_configurator as page_config
import src.utils.prompt_fetcher as prompt_fetcher
from models.Prompts import PredefinedPrompt
import src.components.formatting_utils as formatting_utils
import pandas as pd

# Data

page_config.initialize_page(
    icon="📚",
    title="Prompt Library",
    desc="""
    Explore and modify your prompt collection.
    """)

def save_prompt(prompt: PredefinedPrompt):        
    st.toast(f"[NOT REALLY] Saved {prompt.title} to the database.", icon="✅")    

prompts = prompt_fetcher.get_predefined_prompts()     

# UI
col1, col2 = st.columns([3, 1])

with col1:
    st.selectbox(label='Select Prompt', 
                 label_visibility="collapsed",
                 options=prompts, 
                 key='prompt',                  
                 format_func=lambda x: f"{x.icon} {x.title}")
        
prompt = st.session_state['prompt']

with col2:
    if st.button("💾Save"):
        save_prompt(prompt)
    
do_expand = True

with st.expander(f":green[📋Details]", expanded=do_expand):
    st.text_input(label="Name", value= f"{prompt.title}", key='title')    
    st.text_area(label="Description",
                value= f"{prompt.description}",
                height=100,              
                help="This is the description of the prompt",
                key='description'
                )

with st.expander(":blue[🤖System Prompt]", expanded=do_expand):
    st.text_area(
        label="Text",
        #label_visibility="collapsed",
        value= f"{prompt.system_prompt}",
        height=300,              
        help="This is the prompt that will be sent to the LLM",
        key='system_prompt'
        )

with st.expander(":gray[🧾User Content]", expanded=False):
    st.text_area(label="Text",
                 #label_visibility="collapsed",
                 value= f"{prompt.user_content}",
                 height=100,              
                 help="Not sure at this point what this is for",
                 key='user_content',                               
                )
    