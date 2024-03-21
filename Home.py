import streamlit as st
import src.components.page_configurator as page_config
from yaml.loader import SafeLoader

page_config.initialize_page(
    icon="💠",
    title="AI Of You",
    desc="""
    This is the home page of the application.
    """,
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.write("Welcome to A.I. Of You! ")
st.write("""
This is the home page of the application. At some point it will show useful information about the app
and some diagrams or charts.

You can navigate to different modules using the sidebar on the left.
Only the following modules are functional right now:
""")

st.page_link("pages/2_📚_Prompt_Library.py", label=":blue[Prompt Library]", icon="📚")
st.page_link("pages/3_🪄_Prompt_Wizard.py", label=":green[Prompt Wizard]", icon="🪄")