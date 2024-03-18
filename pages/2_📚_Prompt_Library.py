import streamlit as st
import src.components.page_configurator as page_config
import src.utils.prompt_fetcher as prompt_fetcher
import pandas as pd

page_config.initialize_page(
    icon="📚",
    title="Prompt Library",
    desc="""
    Explore and modify your prompt collection.
    """)

page_config.initialize_session_state({
    'prompt': 'summarize_micro',  
    })

prompts = prompt_fetcher.get_predefined_prompts()     

blah = st.data_editor(data=pd.DataFrame([vars(p) for p in prompts]),
             #height=180,
             hide_index=True,       
             column_config={
                 "id": None,
                 "title": st.column_config.TextColumn(),
                 "description": st.column_config.TextColumn(),
                 "system_prompt": None,
                 "user_content": None,
             })

