import streamlit as st

def initialize_page(
    icon: str, 
    title: str, 
    desc: str = 'No description',
    **kwargs):
    # Streamlit page configuration
    st.set_page_config(page_title=title, page_icon=icon, **kwargs)
    
    # UI
    st.markdown(f"## {icon}{title}")
    with st.container(border=True):
        st.write(f"""*:white[{desc}]*""")
    
def initialize_session_state(default_values: dict):    
    for key, value in default_values.items():
        if key not in st.session_state:
            #st.write(f"Setting {key} to {value}")
            st.session_state[key] = value  
        #else:
            #st.write(f"Session state {key} already set to {st.session_state[key]}")