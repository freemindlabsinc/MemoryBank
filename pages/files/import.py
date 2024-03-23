import streamlit as st
import src.components.page_header as page_config
import st_pages as stp

stp.add_page_title()


page_config.initialize_page(
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