import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="A.I. Of You",
    page_icon="💠",    
)

# Create two columns
col1, space, col2 = st.columns([1,1, 4])

with col1:    
    st.image("https://i0.wp.com/freemindlabs.com/wp-content/uploads/2024/01/Free-Mind-Labs-logo.png?w=625&ssl=1", 
             width=150,)
with col2:
    st.write("# 💠Welcome to A.I. Of You! ")
    st.write("*The Swiss Army Knife for AI*")


# Write a brief description of the app
st.write("This is a test.")
st.write("Information about the application will come later...")

# Create a section for each page in the app
st.page_link("pages/0_🪄_Prompt_Wizard.py", label="Prompt Wizard", icon="🪄")
#st.write("Description of what Prompt Wizard does.")
# Add more sections as needed