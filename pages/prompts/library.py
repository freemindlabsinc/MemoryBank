import streamlit as st
import src.components.page_header as page_config
import st_pages as stp
import pages.prompts.library_vm as vm

stp.add_page_title()

# Initialization

page_config.initialize_page(
    desc="""
    Explore and modify your prompt collection.
    """)
  

# UI
col1, col2 = st.columns([4, 1])

with col1:
    st.selectbox(label='Select Prompt', 
                 label_visibility="collapsed",
                 options=vm.prompts, 
                 key='prompt',                  
                 format_func=lambda x: f"{x.icon} {x.title}")
        
prompt = st.session_state['prompt']

with col2:
    if st.button("💾Save"):
        vm.save_prompt(prompt)
    
do_expand = True

expander_color = ":blue"
label_color = ":orange"

with st.expander(f"{expander_color}[📋Details]", expanded=do_expand):
    st.text_input(label=f"{label_color}[Name]", value= f"{prompt.title}", key='title')    
    st.text_area(label=f"{label_color}[Description]",
                value= f"{prompt.description}",
                height=100,              
                help="This is the description of the prompt",
                key='description'
                )

with st.expander(f"{expander_color}[🤖System Prompt]", expanded=do_expand):
    st.markdown(
    #st.text_area(
        #label=f"{label_color}[Text]",
        #label_visibility="collapsed",
        body= f"{prompt.system_prompt}",        
        #height=300,              
        help="This is the prompt that will be sent to the LLM",
        #key='system_prompt'
        )

with st.expander(f"{expander_color}[🧾User Content]", expanded=False):
    st.markdown(
    #st.text_area(
        #label=f"{label_color}[Text]",
        #label_visibility="collapsed",
        body= f"{prompt.user_content or 'None'}",
        #height=100,              
        help="Not sure at this point what this is for",
        #key='user_content',                               
    )
    