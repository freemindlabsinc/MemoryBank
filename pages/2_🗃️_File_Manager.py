import streamlit as st
import pandas as pd
from src.utils.data_generator import generate_selectable_sources

st.set_page_config(
    page_title="File Manager",
    page_icon="🗃️",    
)

st.write("# 🗃️File Manager")

sources = generate_selectable_sources()
df = pd.DataFrame(sources)

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
st.write("Here's the value in Session State:")
st.write(st.session_state["key"]) # 👈 Show the value in Session State