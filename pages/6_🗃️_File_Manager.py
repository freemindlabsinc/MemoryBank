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

if 'sources' not in st.session_state:
    st.session_state['sources'] = generate_selectable_sources()
    st.write(":red[Read sources]")
    
uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    
    
    
    st.write("filename:", uploaded_file.name)        
    
    # generate a random id like "FA1C2187AFD"
    import random 
    import string

    id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    
    new_entry = { 
        "key": id, 
        "is_selected": True, 
        "type": "Uploaded File", 
        "title": uploaded_file.name,         
        "source": "//" + uploaded_file.name
        }        
    
    st.session_state['sources'].append(new_entry)
    

df = pd.DataFrame(st.session_state['sources'])

st.data_editor(df, 
            key="key", 
            num_rows="fixed", 
            use_container_width=False,
            hide_index=True,)