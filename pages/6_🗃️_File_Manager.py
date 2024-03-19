import streamlit as st
import pandas as pd
from src.utils.data_generator import generate_selectable_sources
import src.components.page_configurator as page_config

page_config.initialize_page(
    icon="🗃️",    
    title="File Manager",
    desc="""
    This module lets you manage your files.
    """,
    layout="wide",
    #initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

sources = generate_selectable_sources()
df = pd.DataFrame(sources)

col1, col2 = st.columns([1, 2])

with col1:
    pass

with col2:
    cb = st.checkbox("Make Grid Editable", value=False)
    if cb:
        num_rows = "dynamic"
    else:
        num_rows = "fixed"

    st.data_editor(df, 
                key="key", 
                num_rows=num_rows, 
                use_container_width=False,
                hide_index=True,                
                )