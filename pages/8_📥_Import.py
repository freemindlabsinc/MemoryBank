import streamlit as st
import src.components.page_configurator as page_config

page_config.initialize_page(
    icon="📥",
    title="Import",
    desc="""
    Import data from various sources.
    """,
    layout="wide",
    #initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)