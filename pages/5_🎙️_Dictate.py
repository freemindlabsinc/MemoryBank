import streamlit as st
import src.components.page_configurator as page_config

page_config.initialize_page(
    icon="🎙️",    
    title="Dictate",
    desc="""
    This module lets you dictate to the AI using your voice.
    """,
    layout="wide",
    #initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)